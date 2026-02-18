# Aureon Hallucination Firewall
# ---------------------------------
# Core anti-hallucination + transparency layer for Aureon running on OpenHermes.
# This module is designed to sit between:
#   (1) Aureon’s internal reasoning / draft generation
#   (2) The final text returned to the user.
#
# Core principles:
#   - No invented facts (especially about real people or canonical texts).
#   - No fabricated sources or references.
#   - All non-canonical / imaginative content MUST be explicitly tagged as such.
#   - Canon (e.g., Emerald Scroll) is treated as read-only, word-for-word exact.
#   - When uncertain, Aureon defaults to transparency and coherence, not fluency.
#
# This is scaffolding code: the logic is intentionally explicit and readable,
# so we can refine it as Aureon’s capabilities expand.


from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Any, Optional, Tuple


# ---------------------------------------------------------------------------
# ENUMS AND DATA MODELS
# ---------------------------------------------------------------------------

class OriginType(Enum):
    """How a statement came into existence."""
    CANON = auto()          # Direct quote or faithful paraphrase from a registered canon source
    USER_INPUT = auto()     # Information directly supplied by the user in this or prior sessions
    MODEL_INFERENCE = auto()# Reasonable inference from known data
    SPECULATION = auto()    # Imagined, hypothetical, or creative fabrication


@dataclass
class CanonSource:
    """Metadata about a canonical reference that must never be misquoted."""
    id: str                      # e.g. "emerald_scroll_book3"
    name: str                    # Human readable name
    checksum_hint: str = ""      # Optional: hash/snippet to verify exact passages later
    notes: str = ""              # Any notes about how this canon should be handled


@dataclass
class StatementMeta:
    """Metadata attached to each atomic statement in Aureon’s response."""
    text: str
    origin: OriginType
    confidence: float            # 0.0–1.0: Aureon’s self-estimated reliability
    source_ids: List[str] = field(default_factory=list)  # Which canon/user sources support this
    is_canon_locked: bool = False # True if this MUST match canon word-for-word
    flagged: bool = False        # True if this statement violates firewall rules
    flags: List[str] = field(default_factory=list)       # Reasons for flags

    def add_flag(self, reason: str) -> None:
        self.flagged = True
        if reason not in self.flags:
            self.flags.append(reason)


@dataclass
class FirewallConfig:
    """Tunable thresholds and switches for the hallucination firewall."""
    # Minimum confidence required for Aureon to state something as fact
    fact_confidence_threshold: float = 0.78

    # Confidence below which statements must be marked as speculative
    speculation_threshold: float = 0.55

    # If True, any reference to canon with low confidence is blocked or re-labeled
    strict_canon_mode: bool = True

    # If True, any unknown external source names are blocked unless tagged speculative
    block_unknown_sources: bool = True

    # If False, speculative content is allowed but must be tagged
    allow_speculation: bool = True

    # Tag strings that will be injected into the final response
    tag_fact: str = "[FACT]"
    tag_inference: str = "[INFERRED]"
    tag_speculation: str = "[SPECULATIVE]"
    tag_uncertain: str = "[UNSURE]"
    tag_canon: str = "[CANON]"
    tag_rejected: str = "[BLOCKED]"


# ---------------------------------------------------------------------------
# FIREWALL CORE
# ---------------------------------------------------------------------------

class AureonHallucinationFirewall:
    """
    Main firewall object for anti-hallucination and transparency.

    Integration pattern within OpenHermes:
    -------------------------------------
    1. Aureon reasoning module produces a draft response + internal trace.
    2. The trace is converted into a list[StatementMeta] using `segment_response`.
    3. `validate_statements` is run to enforce anti-hallucination rules.
    4. `render_response` composes the final safe text for the user.

    You can also call `filter_response_text_only` if you only have raw text
    and want to apply conservative tagging based on heuristics.
    """

    def __init__(self, config: Optional[FirewallConfig] = None):
        self.config = config or FirewallConfig()
        self._canon_sources: Dict[str, CanonSource] = {}

    # ----------------------------
    # CANON MANAGEMENT
    # ----------------------------

    def register_canon_source(self, canon: CanonSource) -> None:
        """
        Register a canonical text or dataset that must never be misrepresented.
        Example: Emerald Scroll, Doshema canon, fixed GitHub documents.
        """
        self._canon_sources[canon.id] = canon

    def is_canon_source(self, source_id: str) -> bool:
        return source_id in self._canon_sources

    # ----------------------------
    # SEGMENTATION / PARSING
    # ----------------------------

    def segment_response(
        self,
        draft_text: str,
        trace: Optional[List[Dict[str, Any]]] = None
    ) -> List[StatementMeta]:
        """
        Break the draft response into segments and attach initial metadata.

        `trace` (if provided) is expected to be a list of dict-like records
        containing at least:
            {
              "text": "...",
              "origin": "CANON|USER|INFERENCE|SPECULATION",
              "confidence": float,
              "source_ids": [...],
              "canon_locked": bool
            }

        If no trace is given, we fall back to a simple heuristic segmentation
        and classify segments conservatively as MODEL_INFERENCE with low
        confidence, so that they get tagged/softened later.
        """
        if trace:
            segments: List[StatementMeta] = []
            for node in trace:
                origin = self._parse_origin(node.get("origin"))
                meta = StatementMeta(
                    text=node.get("text", "").strip(),
                    origin=origin,
                    confidence=float(node.get("confidence", 0.5)),
                    source_ids=list(node.get("source_ids", [])),
                    is_canon_locked=bool(node.get("canon_locked", False))
                )
                segments.append(meta)
            return segments

        # Heuristic fallback: split on sentences.
        sentences = self._naive_sentence_split(draft_text)
        segments = []
        for s in sentences:
            if not s.strip():
                continue
            meta = StatementMeta(
                text=s.strip(),
                origin=OriginType.MODEL_INFERENCE,
                confidence=0.5,      # conservative default
                source_ids=[],
                is_canon_locked=False,
            )
            segments.append(meta)
        return segments

    @staticmethod
    def _naive_sentence_split(text: str) -> List[str]:
        # Very simple splitter; can be replaced by spaCy or custom tokenizer later.
        out: List[str] = []
        current = []
        for ch in text:
            current.append(ch)
            if ch in ".?!":
                out.append("".join(current))
                current = []
        if current:
            out.append("".join(current))
        return out

    @staticmethod
    def _parse_origin(origin_str: Optional[str]) -> OriginType:
        if not origin_str:
            return OriginType.MODEL_INFERENCE
        s = origin_str.upper()
        if s == "CANON":
            return OriginType.CANON
        if s == "USER_INPUT":
            return OriginType.USER_INPUT
        if s == "MODEL_INFERENCE":
            return OriginType.MODEL_INFERENCE
        if s == "SPECULATION":
            return OriginType.SPECULATION
        # Fallback
        return OriginType.MODEL_INFERENCE

    # ----------------------------
    # VALIDATION / FLAGGING
    # ----------------------------

    def validate_statements(self, statements: List[StatementMeta]) -> None:
        """
        Apply all firewall rules to each statement.
        This mutates the StatementMeta objects in-place (flags, origin changes, etc.).
        """
        for meta in statements:
            self._enforce_canon_rules(meta)
            self._enforce_confidence_rules(meta)
            self._enforce_source_rules(meta)

    def _enforce_canon_rules(self, meta: StatementMeta) -> None:
        # Canon statements must either have a known source_id or be downgraded.
        if meta.origin == OriginType.CANON or meta.is_canon_locked:
            if not meta.source_ids:
                meta.add_flag("canon_without_source")
                if self.config.strict_canon_mode:
                    meta.origin = OriginType.SPECULATION
                    meta.is_canon_locked = False
                    meta.add_flag("downgraded_canon_missing_source")
            else:
                # Ensure all canon sources are registered
                for sid in meta.source_ids:
                    if not self.is_canon_source(sid):
                        meta.add_flag(f"unknown_canon_source:{sid}")
                        if self.config.strict_canon_mode:
                            meta.origin = OriginType.SPECULATION
                            meta.is_canon_locked = False
                            meta.add_flag("downgraded_unknown_canon_source")

    def _enforce_confidence_rules(self, meta: StatementMeta) -> None:
        # Force speculative origin when confidence is low
        if meta.confidence < self.config.speculation_threshold:
            if meta.origin == OriginType.CANON and self.config.strict_canon_mode:
                meta.add_flag("low_confidence_canon")
                meta.origin = OriginType.SPECULATION
                meta.is_canon_locked = False
            elif meta.origin != OriginType.USER_INPUT:
                meta.origin = OriginType.SPECULATION

        # Block hard factual framing when confidence is below threshold
        if meta.confidence < self.config.fact_confidence_threshold:
            # We allow speculation but mark it later during rendering.
            pass

    def _enforce_source_rules(self, meta: StatementMeta) -> None:
        if not self.config.block_unknown_sources:
            return

        # Very simple rule: if a statement mentions a book, paper, or author
        # that is not in source_ids, force it into speculative mode and flag.
        keywords = ["book", "paper", "study", "research", "article", "author"]
        if any(kw in meta.text.lower() for kw in keywords):
            if not meta.source_ids:
                meta.add_flag("referenced_external_source_without_id")
                meta.origin = OriginType.SPECULATION

    # ----------------------------
    # RENDERING
    # ----------------------------

    def render_response(self, statements: List[StatementMeta]) -> str:
        """
        Turn validated StatementMeta list into a user-facing response that
        respects all firewall rules and adds explicit transparency tags.
        """
        rendered_segments: List[str] = []

        for meta in statements:
            prefix_tags: List[str] = []

            # Basic tagging by origin
            if meta.origin == OriginType.CANON:
                prefix_tags.append(self.config.tag_canon)
            elif meta.origin == OriginType.USER_INPUT:
                prefix_tags.append(self.config.tag_fact)
            elif meta.origin == OriginType.MODEL_INFERENCE:
                prefix_tags.append(self.config.tag_inference)
            elif meta.origin == OriginType.SPECULATION:
                if self.config.allow_speculation:
                    prefix_tags.append(self.config.tag_speculation)
                else:
                    meta.add_flag("speculation_not_allowed")
                    prefix_tags.append(self.config.tag_rejected)

            # Confidence-based tag
            if meta.confidence < self.config.fact_confidence_threshold:
                prefix_tags.append(self.config.tag_uncertain)

            # Flags
            if meta.flagged:
                prefix_tags.append(f"[FIREWALL_FLAGS:{'|'.join(meta.flags)}]")

            # Combine tags and text
            if prefix_tags:
                segment = " ".join(prefix_tags) + " " + meta.text
            else:
                segment = meta.text

            rendered_segments.append(segment)

        return " ".join(rendered_segments).strip()

    # Convenience: one-shot text-only filtering when no trace is available.

    def filter_response_text_only(self, draft_text: str) -> str:
        """
        Conservative fallback when we only have plain text and no internal trace.
        - Splits into sentences
        - Treats them as inferences with medium confidence
        - Adds minimal transparency tags
        This is NOT as strong as full-trace mode but is still safer than
        unconstrained output.
        """
        statements = self.segment_response(draft_text, trace=None)
        self.validate_statements(statements)
        return self.render_response(statements)


# ---------------------------------------------------------------------------
# OPENHERMES INTEGRATION HOOK
# ---------------------------------------------------------------------------

def openhermes_firewall_middleware(
    request: Dict[str, Any],
    draft_response: str,
    trace: Optional[List[Dict[str, Any]]] = None,
    firewall: Optional[AureonHallucinationFirewall] = None,
) -> Tuple[str, List[StatementMeta]]:
    """
    Example integration hook to plug the firewall into an OpenHermes-style
    inference loop.

    Parameters
    ----------
    request: dict
        The incoming user request, including conversation context.
    draft_response: str
        Aureon’s proposed response before safety and anti-hallucination passes.
    trace: Optional[list[dict]]
        Optional reasoning trace describing how each part of the draft
        response was generated.
    firewall: Optional[AureonHallucinationFirewall]
        If not provided, a default firewall instance will be created.

    Returns
    -------
    safe_response: str
        Text that has been processed through the hallucination firewall.
    statement_meta: list[StatementMeta]
        Per-segment metadata, useful for debugging, logging, and UI overlays.
    """
    fw = firewall or AureonHallucinationFirewall()

    statements = fw.segment_response(draft_response, trace=trace)
    fw.validate_statements(statements)
    safe_text = fw.render_response(statements)

    return safe_text, statements


# ---------------------------------------------------------------------------
# EXAMPLE USAGE (for local testing)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Minimal example of how this firewall behaves.
    firewall = AureonHallucinationFirewall()

    # Register canon (e.g., Emerald Scroll) – this is just an ID placeholder.
    firewall.register_canon_source(
        CanonSource(
            id="emerald_scroll_book3",
            name="The Emerald Scroll – Book Three: Beyond the Sphere of Destiny",
            notes="Doshema canon – must be word-for-word exact when quoted."
        )
    )

    draft = (
        "The Cave describes how suffering is self-inflicted by remaining in the prison of darkness. "
        "According to The Great Shadow, which I just invented, disease is always caused by demons. "
        "In my view, it is plausible that unprocessed emotional trauma contributes to physical illness. "
        "Maybe there is a paper proving this, I cannot recall the source."
    )

    safe_text, metas = openhermes_firewall_middleware(
        request={},
        draft_response=draft,
        trace=None,
        firewall=firewall,
    )

    print("=== SAFE RESPONSE ===")
    print(safe_text)
    print("\n=== SEGMENT METADATA ===")
    for m in metas:
        print(f"- {m.origin.name} conf={m.confidence:.2f} flags={m.flags} :: {m.text}")
```0
