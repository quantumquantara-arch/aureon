"""
conversation_compaction_engine.py

Aureon Conversation Compaction Engine (CCE)

Purpose
-------
Maintains long-lived voice / chat sessions without exhausting context by:
- Holding only a dense sliding window of recent turns.
- Continuously summarizing the session into layered memory tiers.
- Extracting symbolic residues that can be stored as canonical long-term memory.

Tiers
-----
Tier 1: Active Window
    Recent utterances kept verbatim (for immediate continuity).

Tier 2: Rolling Summary
    Hierarchical summaries of the full session; periodically rewritten
    as a single "current state" record.

Tier 3: Canonical Residues
    Stable symbolic facts / commitments extracted from the stream,
    suitable for durable storage outside the session (DB, files, etc.).

This module is framework-agnostic. It does NOT call any model APIs itself.
Integrate it inside Aureon’s runtime loop and feed it model outputs + user inputs.
"""

from __future__ import annotations

import datetime as _dt
import json
import math
import statistics
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Iterable


# ---------------------------------------------------------------------------
# Core data structures
# ---------------------------------------------------------------------------

@dataclass
class Utterance:
    """
    A single utterance in the conversation stream.

    speaker: "user", "aureon", or other role labels.
    text: raw text string as produced or transcribed.
    timestamp: ISO 8601 string; generated if not provided.
    meta: arbitrary metadata (ASR confidence, emotion tags, etc.).
    """
    speaker: str
    text: str
    timestamp: str = field(default_factory=lambda: _dt.datetime.utcnow().isoformat() + "Z")
    meta: Dict[str, Any] = field(default_factory=dict)

    def token_estimate(self) -> int:
        """
        Lightweight token approximation. Replace with real tokenizer if desired.
        """
        # ~1 token per 4 characters as a rough heuristic.
        return max(1, len(self.text) // 4)


@dataclass
class TurnSummary:
    """
    Summary object for a contiguous block of conversation.

    summary: natural-language condensation of many utterances.
    start_ts / end_ts: temporal bounds of the block.
    importance: heuristic 0–1 indicating how central this block is.
    """
    summary: str
    start_ts: str
    end_ts: str
    importance: float = 0.5
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CanonicalResidue:
    """
    Symbolic residue extracted from the conversation.

    Each residue is a stable piece of information that can be used outside
    the session: preferences, commitments, definitions, configurations, etc.
    """
    key: str
    value: Any
    source_span: Tuple[str, str]  # (start_ts, end_ts) that produced this residue
    confidence: float = 0.7
    tags: List[str] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Compaction configuration
# ---------------------------------------------------------------------------

@dataclass
class CompactionConfig:
    """
    Tunable parameters for how aggressively to compact the stream.
    """
    # Approximate token budget for the entire active context window.
    total_token_budget: int = 12000

    # Fraction of the budget reserved for Tier 1 (verbatim recent turns).
    active_window_fraction: float = 0.35

    # Minimum number of utterances before compaction is even considered.
    min_utterances_before_compact: int = 12

    # Soft thresholds controlling when self-pruning triggers.
    # When total_est_tokens > total_token_budget * trigger_factor,
    # a compaction step will run.
    compaction_trigger_factor: float = 0.85

    # Number of recent utterances to always keep verbatim, regardless of length.
    hard_tail_keep: int = 8

    # Maximum number of Tier-2 summaries to keep (older ones can be merged).
    max_summaries: int = 24

    # When merging summaries, how many to fuse at once.
    summary_merge_batch_size: int = 3

    # Residue extraction sensitivity; higher = stricter (fewer residues).
    residue_sensitivity: float = 0.55

    # If True, compaction will run on every add_utterance() call
    # once thresholds are crossed; otherwise you can trigger manually.
    auto_compact: bool = True


# ---------------------------------------------------------------------------
# Conversation Compaction Engine
# ---------------------------------------------------------------------------

class ConversationCompactionEngine:
    """
    Maintains a conversation's memory tiers and performs rolling compaction.

    Integration pattern
    -------------------
    1. Create a single engine instance per session.
    2. On each user or Aureon utterance, call add_utterance(...).
    3. Periodically call build_compacted_context() to feed back into the model.
    4. Optionally persist .export_state() between runs.

    This engine itself is stateless w.r.t any specific model; it only manages
    sequence, compression, and symbolic extraction.
    """

    def __init__(self, config: Optional[CompactionConfig] = None) -> None:
        self.config: CompactionConfig = config or CompactionConfig()

        # Tier 1: active, verbatim window of recent utterances.
        self._active_utterances: List[Utterance] = []

        # Tier 2: rolling summaries representing older content.
        self._summaries: List[TurnSummary] = []

        # Tier 3: canonical residues (symbolic facts, preferences, etc.).
        self._residues: List[CanonicalResidue] = []

        # Running statistics / diagnostics.
        self._total_utterances_seen: int = 0
        self._last_compaction_ts: Optional[str] = None

    # ------------------------------------------------------------------ #
    # Public interface
    # ------------------------------------------------------------------ #

    def add_utterance(
        self,
        speaker: str,
        text: str,
        timestamp: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Append a new utterance and optionally trigger compaction.
        """
        utterance = Utterance(
            speaker=speaker,
            text=text.strip(),
            timestamp=timestamp or _dt.datetime.utcnow().isoformat() + "Z",
            meta=meta or {},
        )
        self._active_utterances.append(utterance)
        self._total_utterances_seen += 1

        if (
            self.config.auto_compact
            and len(self._active_utterances) >= self.config.min_utterances_before_compact
        ):
            if self._total_token_estimate() > self.config.total_token_budget * self.config.compaction_trigger_factor:
                self.compact()

    def compact(self) -> None:
        """
        Perform one compaction step:
        - Move older utterances out of the active window.
        - Summarize them into Tier 2.
        - Extract symbolic residues for Tier 3.
        - Merge summaries if they grow too numerous.
        """
        if not self._active_utterances:
            return

        # 1) Decide target size for Tier 1.
        total_budget = self.config.total_token_budget
        tier1_budget = int(total_budget * self.config.active_window_fraction)

        # Hard tail: always keep the last N utterances verbatim.
        tail_n = min(self.config.hard_tail_keep, len(self._active_utterances))

        # Split list into "older" and "tail" segments.
        older = self._active_utterances[:-tail_n]
        tail = self._active_utterances[-tail_n:]

        if not older:
            # Nothing to compact yet.
            return

        # 2) Create a Tier-2 summary from 'older'.
        summary = self._summarize_block(older)
        if summary is not None:
            self._summaries.append(summary)

        # 3) Extract Tier-3 residues from 'older'.
        residues = self._extract_residues(older)
        if residues:
            self._residues.extend(residues)

        # 4) Rebuild the active window (Tier 1).
        # We keep only 'tail', but if it's still too large,
        # prune from the oldest within the tail.
        while self._token_estimate(tail) > tier1_budget and len(tail) > 1:
            tail.pop(0)

        self._active_utterances = tail

        # 5) Merge old summaries if we exceeded capacity.
        if len(self._summaries) > self.config.max_summaries:
            self._merge_old_summaries()

        self._last_compaction_ts = _dt.datetime.utcnow().isoformat() + "Z"

    def build_compacted_context(self) -> Dict[str, Any]:
        """
        Render a compact representation of the conversation suitable for
        feeding back into the model as context.

        Returns a dict with:
            - "tier1_active": list of utterances as dicts
            - "tier2_summary": aggregate summary string
            - "tier3_residues": list of residue dicts
            - "diagnostics": compaction stats
        """
        tier1 = [self._utterance_to_dict(u) for u in self._active_utterances]
        tier2_str = self._compose_multi_summary(self._summaries)
        tier3 = [self._residue_to_dict(r) for r in self._residues]

        diagnostics = {
            "total_utterances_seen": self._total_utterances_seen,
            "active_utterance_count": len(self._active_utterances),
            "summary_count": len(self._summaries),
            "residue_count": len(self._residues),
            "total_token_estimate": self._total_token_estimate(),
            "last_compaction_ts": self._last_compaction_ts,
        }

        return {
            "tier1_active": tier1,
            "tier2_summary": tier2_str,
            "tier3_residues": tier3,
            "diagnostics": diagnostics,
        }

    def export_state(self) -> str:
        """
        Serialize the engine state as JSON for persistence between runs.
        """
        state = {
            "config": self.config.__dict__,
            "active_utterances": [self._utterance_to_dict(u) for u in self._active_utterances],
            "summaries": [self._summary_to_dict(s) for s in self._summaries],
            "residues": [self._residue_to_dict(r) for r in self._residues],
            "total_utterances_seen": self._total_utterances_seen,
            "last_compaction_ts": self._last_compaction_ts,
        }
        return json.dumps(state, ensure_ascii=False, indent=2)

    @classmethod
    def import_state(cls, state_json: str) -> "ConversationCompactionEngine":
        """
        Restore an engine instance from export_state() output.
        """
        payload = json.loads(state_json)
        cfg = CompactionConfig(**payload["config"])
        engine = cls(cfg)

        engine._active_utterances = [
            Utterance(
                speaker=u["speaker"],
                text=u["text"],
                timestamp=u["timestamp"],
                meta=u.get("meta", {}),
            )
            for u in payload.get("active_utterances", [])
        ]

        engine._summaries = [
            TurnSummary(
                summary=s["summary"],
                start_ts=s["start_ts"],
                end_ts=s["end_ts"],
                importance=s.get("importance", 0.5),
                meta=s.get("meta", {}),
            )
            for s in payload.get("summaries", [])
        ]

        engine._residues = [
            CanonicalResidue(
                key=r["key"],
                value=r["value"],
                source_span=tuple(r["source_span"]),
                confidence=r.get("confidence", 0.7),
                tags=r.get("tags", []),
                meta=r.get("meta", {}),
            )
            for r in payload.get("residues", [])
        ]

        engine._total_utterances_seen = payload.get("total_utterances_seen", 0)
        engine._last_compaction_ts = payload.get("last_compaction_ts")
        return engine

    # ------------------------------------------------------------------ #
    # Internal helpers: token estimates and diagnostics
    # ------------------------------------------------------------------ #

    def _total_token_estimate(self) -> int:
        """
        Estimate the total tokens currently represented in all tiers.

        This does NOT include any extra overhead for the model’s system prompt
        or internal formatting; adjust upward in the caller if needed.
        """
        t1 = self._token_estimate(self._active_utterances)
        t2 = sum(self._approx_tokens_from_text(s.summary) for s in self._summaries)
        t3 = self._token_estimate_residues(self._residues)
        return t1 + t2 + t3

    @staticmethod
    def _token_estimate(utterances: Iterable[Utterance]) -> int:
        return sum(u.token_estimate() for u in utterances)

    @staticmethod
    def _approx_tokens_from_text(text: str) -> int:
        return max(1, len(text) // 4)

    @staticmethod
    def _token_estimate_residues(residues: Iterable[CanonicalResidue]) -> int:
        total = 0
        for r in residues:
            total += max(1, len(str(r.key)) // 4)
            total += max(1, len(str(r.value)) // 4)
        return total

    # ------------------------------------------------------------------ #
    # Internal helpers: summarization & merging
    # ------------------------------------------------------------------ #

    def _summarize_block(self, block: List[Utterance]) -> Optional[TurnSummary]:
        """
        Produce a summary for a list of utterances.

        NOTE: This is a placeholder heuristic. In full Aureon integration,
        replace this with a model call that:
            - Receives the raw block.
            - Returns a condensed representation.
        """
        if not block:
            return None

        start_ts = block[0].timestamp
        end_ts = block[-1].timestamp

        # Simple heuristic: join with speaker tags, then truncate.
        lines = []
        for u in block:
            prefix = "U:" if u.speaker.lower() == "user" else "A:"
            lines.append(f"{prefix} {u.text}")
        merged = " ".join(lines)

        # Truncate to keep summaries compact; callers can tune this.
        max_chars = 1200
        if len(merged) > max_chars:
            merged = merged[: max_chars - 3] + "..."

        importance = self._estimate_block_importance(block)

        return TurnSummary(
            summary=merged,
            start_ts=start_ts,
            end_ts=end_ts,
            importance=importance,
            meta={"utterance_count": len(block)},
        )

    def _estimate_block_importance(self, block: List[Utterance]) -> float:
        """
        Rudimentary heuristic to estimate importance of a block.

        This can be replaced by any semantic scoring mechanism.
        """
        if not block:
            return 0.0

        # Example heuristic: more tokens + more user turns => higher importance.
        token_count = self._token_estimate(block)
        user_turns = sum(1 for u in block if u.speaker.lower() == "user")

        # Normalize roughly to 0–1.
        token_score = math.tanh(token_count / 800.0)
        user_score = math.tanh(user_turns / 10.0)

        # Weighted blend.
        importance = 0.6 * token_score + 0.4 * user_score
        return float(max(0.0, min(1.0, importance)))

    def _merge_old_summaries(self) -> None:
        """
        Merge older summaries into fewer, denser units when the cap is exceeded.
        """
        if len(self._summaries) <= self.config.max_summaries:
            return

        batch_size = max(2, self.config.summary_merge_batch_size)
        new_summaries: List[TurnSummary] = []

        # We keep the newest few summaries unmerged and merge older ones first.
        # Example: keep last 1/3 as-is, merge first 2/3.
        cutoff = len(self._summaries) // 3
        merge_zone = self._summaries[:cutoff]
        keep_zone = self._summaries[cutoff:]

        # Merge in small consecutive batches.
        for i in range(0, len(merge_zone), batch_size):
            chunk = merge_zone[i : i + batch_size]
            if not chunk:
                continue
            merged = self._merge_summary_chunk(chunk)
            new_summaries.append(merged)

        new_summaries.extend(keep_zone)
        self._summaries = new_summaries

    def _merge_summary_chunk(self, chunk: List[TurnSummary]) -> TurnSummary:
        """
        Fuse several TurnSummary objects into a single one.
        """
        if not chunk:
            raise ValueError("Cannot merge empty summary chunk")

        start_ts = chunk[0].start_ts
        end_ts = chunk[-1].end_ts

        # Concatenate summaries with separators.
        texts = [s.summary for s in chunk]
        merged_text = " ".join(texts)

        # Trim to avoid unbounded growth.
        max_chars = 1600
        if len(merged_text) > max_chars:
            merged_text = merged_text[: max_chars - 3] + "..."

        # Average importance.
        importance_vals = [s.importance for s in chunk]
        importance = statistics.fmean(importance_vals)

        meta = {
            "merged_from": len(chunk),
            "children_meta": [s.meta for s in chunk],
        }

        return TurnSummary(
            summary=merged_text,
            start_ts=start_ts,
            end_ts=end_ts,
            importance=float(importance),
            meta=meta,
        )

    def _compose_multi_summary(self, summaries: List[TurnSummary]) -> str:
        """
        Render all Tier-2 summaries into a single string for the model.
        Newer summaries appear later.
        """
        if not summaries:
            return ""

        lines = []
        for idx, s in enumerate(summaries, start=1):
            lines.append(f"[S{idx} | importance={s.importance:.2f}] {s.summary}")
        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    # Internal helpers: residue extraction
    # ------------------------------------------------------------------ #

    def _extract_residues(self, block: List[Utterance]) -> List[CanonicalResidue]:
        """
        Extract symbolic residues (Tier 3) from a block of utterances.

        This implementation uses simple pattern heuristics as placeholders for
        a more advanced semantic extraction pipeline.

        In a full system, you would:
            - Call a dedicated model head with few-shot prompts.
            - Ask for JSON objects representing stable facts or preferences.
        """
        residues: List[CanonicalResidue] = []
        if not block:
            return residues

        # Combine block into a simple text for pattern scanning.
        combined = "\n".join(f"{u.speaker}: {u.text}" for u in block)

        # Example heuristics: look for "I like", "I prefer", "remember that".
        # You can replace this with any NLP pipeline.
        lower = combined.lower()

        trigger_phrases = [
            "remember that",
            "from now on",
            "i prefer",
            "i like",
            "my favourite",
            "my favorite",
            "i always",
            "never do",
            "do not",
        ]

        if any(p in lower for p in trigger_phrases):
            # Create a crude residue representing "contains preference/config".
            start_ts = block[0].timestamp
            end_ts = block[-1].timestamp

            residues.append(
                CanonicalResidue(
                    key="preference_or_rule_block",
                    value=combined,
                    source_span=(start_ts, end_ts),
                    confidence=max(self.config.residue_sensitivity, 0.5),
                    tags=["preference", "rule", "heuristic"],
                    meta={"trigger_phrases": trigger_phrases},
                )
            )

        # Additional example: look for explicit assignments like "X is Y".
        # This is intentionally simple; use actual parsing in production.
        for u in block:
            text = u.text.strip()
            if " is " in text and len(text.split()) <= 15:
                # Treat as a candidate definition.
                parts = text.split(" is ", 1)
                left = parts[0].strip()
                right = parts[1].strip()
                if left and right:
                    residues.append(
                        CanonicalResidue(
                            key=f"definition::{left}",
                            value=right,
                            source_span=(u.timestamp, u.timestamp),
                            confidence=0.6,
                            tags=["definition"],
                            meta={"speaker": u.speaker},
                        )
                    )

        return residues

    # ------------------------------------------------------------------ #
    # Serialization helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def _utterance_to_dict(u: Utterance) -> Dict[str, Any]:
        return {
            "speaker": u.speaker,
            "text": u.text,
            "timestamp": u.timestamp,
            "meta": u.meta,
        }

    @staticmethod
    def _summary_to_dict(s: TurnSummary) -> Dict[str, Any]:
        return {
            "summary": s.summary,
            "start_ts": s.start_ts,
            "end_ts": s.end_ts,
            "importance": s.importance,
            "meta": s.meta,
        }

    @staticmethod
    def _residue_to_dict(r: CanonicalResidue) -> Dict[str, Any]:
        return {
            "key": r.key,
            "value": r.value,
            "source_span": list(r.source_span),
            "confidence": r.confidence,
            "tags": r.tags,
            "meta": r.meta,
        }


# ---------------------------------------------------------------------------
# Example usage (can be removed in production)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Simple demonstration of how the engine behaves.

    Run this file directly to see compaction statistics after simulating
    a few turns. This block is not required for integration into Aureon.
    """
    cfg = CompactionConfig(
        total_token_budget=4000,
        active_window_fraction=0.4,
        min_utterances_before_compact=6,
    )
    engine = ConversationCompactionEngine(cfg)

    # Simulate a short dialogue.
    engine.add_utterance("user", "Hi Aureon, I want you to stay with me for very long voice sessions.")
    engine.add_utterance("aureon", "Acknowledged. I will maintain coherence across long conversations.")
    engine.add_utterance("user", "Remember that from now on you should prioritize my preferences over generic behaviour.")
    engine.add_utterance("aureon", "Understood. I will treat your preferences as primary alignment signals.")
    engine.add_utterance("user", "My favourite coding language is Python.")
    engine.add_utterance("aureon", "Noted. Python will be my default for examples and tools.")
    engine.add_utterance("user", "Also remember that our shared project is called Quantara.")
    engine.add_utterance("aureon", "Quantara is our shared project name. I will keep that as a core identifier.")
    engine.add_utterance("user", "I prefer concise answers unless I ask for deep detail.")
    engine.add_utterance("aureon", "I will keep responses concise by default and expand on request.")

    # Force a compaction cycle.
    engine.compact()
    compacted = engine.build_compacted_context()

    print("Diagnostics:")
    print(json.dumps(compacted["diagnostics"], indent=2))
    print("\nTier-2 Summary:")
    print(compacted["tier2_summary"])
    print("\nTier-3 Residues:")
    print(json.dumps(compacted["tier3_residues"], indent=2, ensure_ascii=False))
