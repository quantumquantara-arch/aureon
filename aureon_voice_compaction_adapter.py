"""
aureon_voice_compaction_adapter.py

Aureon Voice Compaction Adapter

Purpose
-------
Bridge between Aureon’s runtime (voice / chat loop) and the
ConversationCompactionEngine (CCE).

This module:
    - Owns one ConversationCompactionEngine per Aureon session.
    - Provides simple hooks for registering user / Aureon utterances.
    - Builds a compacted context payload suitable for model calls.
    - Exposes a minimal integration surface that can be wired into
      any transport layer (WebSocket, REST, local loop, etc.).

Usage
-----
1. Create an AureonSession instance at session start.
2. On each incoming user utterance, call session.register_user_utterance(...).
3. On each Aureon reply, call session.register_aureon_utterance(...).
4. Before sending a model request, call session.build_model_io(...)
   to get structured context + instructions.

This file assumes `conversation_compaction_engine.py` is located in the
same Python package or importable path.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Literal

from conversation_compaction_engine import (
    ConversationCompactionEngine,
    CompactionConfig,
)


Role = Literal["system", "user", "assistant"]


@dataclass
class AureonMessage:
    """
    Lightweight message container for passing into a model API.

    role: "system", "user", or "assistant"
    content: string body
    meta: optional metadata kept outside the model but useful
          to Aureon’s runtime.
    """
    role: Role
    content: str
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AureonSessionConfig:
    """
    Configuration for how Aureon builds model I/O around the CCE.

    - system_prompt: core identity + behavior instructions.
    - max_model_tokens: approximate total tokens the model can handle.
    - response_token_budget: reserved tokens for the model’s reply.
    """
    system_prompt: str
    max_model_tokens: int = 16384
    response_token_budget: int = 2048

    # Optional tags describing this session (voice, text, device, etc.).
    session_tags: Dict[str, Any] = field(default_factory=dict)

    # If True, Tier-3 residues are surfaced explicitly in context.
    include_residues_in_context: bool = True

    # If True, Tier-2 multi-summary is included in context.
    include_tier2_summary: bool = True


class AureonSession:
    """
    One live Aureon conversation session (voice or text).

    Responsibilities:
        - Maintain one ConversationCompactionEngine.
        - Track a session id and basic state.
        - Provide model-ready messages with compacted context.
    """

    def __init__(
        self,
        session_config: AureonSessionConfig,
        compaction_config: Optional[CompactionConfig] = None,
        session_id: Optional[str] = None,
    ) -> None:
        self.session_id: str = session_id or f"aureon-session-{uuid.uuid4()}"
        self.config: AureonSessionConfig = session_config
        self.cce: ConversationCompactionEngine = ConversationCompactionEngine(
            compaction_config or self._default_compaction_config(session_config)
        )

        self._turn_index: int = 0

    # ------------------------------------------------------------------ #
    # Public API: registering utterances
    # ------------------------------------------------------------------ #

    def register_user_utterance(
        self,
        text: str,
        timestamp: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Record a user utterance in the CCE.
        """
        self.cce.add_utterance(
            speaker="user",
            text=text,
            timestamp=timestamp,
            meta=meta or {"turn_index": self._turn_index},
        )
        self._turn_index += 1

    def register_aureon_utterance(
        self,
        text: str,
        timestamp: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Record an Aureon utterance in the CCE.
        """
        self.cce.add_utterance(
            speaker="aureon",
            text=text,
            timestamp=timestamp,
            meta=meta or {"turn_index": self._turn_index},
        )
        self._turn_index += 1

    # ------------------------------------------------------------------ #
    # Public API: building model input
    # ------------------------------------------------------------------ #

    def build_model_io(
        self,
        latest_user_text: Optional[str] = None,
        extra_instructions: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Construct model-ready messages and diagnostics.

        latest_user_text:
            If provided, this text will be appended as the most recent
            user message in the outgoing message list. Use this when
            you have a fresh utterance to send and have not yet
            registered it via register_user_utterance.

        extra_instructions:
            Optional additions layered onto the system prompt for a
            single call (e.g., “answer very briefly”, tool hints, etc.).

        Returns:
            {
                "messages": [ { "role": ..., "content": ... }, ... ],
                "diagnostics": { ... },
                "session_id": str
            }
        """
        compacted = self.cce.build_compacted_context()

        system_prompt = self._compose_system_prompt(
            tier2_summary=compacted["tier2_summary"],
            residues=compacted["tier3_residues"],
            extra_instructions=extra_instructions,
        )

        messages: List[AureonMessage] = [
            AureonMessage(role="system", content=system_prompt, meta={"session_id": self.session_id})
        ]

        # Convert Tier-1 active utterances into user/assistant messages.
        for u in compacted["tier1_active"]:
            role: Role = "user" if u["speaker"].lower() == "user" else "assistant"
            messages.append(
                AureonMessage(
                    role=role,
                    content=u["text"],
                    meta={
                        "timestamp": u["timestamp"],
                        "speaker": u["speaker"],
                        "source": "tier1_active",
                    },
                )
            )

        # Append the latest user text if provided but not yet in Tier 1.
        if latest_user_text is not None and latest_user_text.strip():
            messages.append(
                AureonMessage(
                    role="user",
                    content=latest_user_text.strip(),
                    meta={"source": "latest_user_text"},
                )
            )

        # Translate AureonMessage -> simple dicts for model APIs.
        api_messages = [{"role": m.role, "content": m.content} for m in messages]

        diagnostics = {
            "cce": compacted["diagnostics"],
            "session_id": self.session_id,
            "max_model_tokens": self.config.max_model_tokens,
            "response_token_budget": self.config.response_token_budget,
        }

        return {
            "messages": api_messages,
            "diagnostics": diagnostics,
            "session_id": self.session_id,
        }

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #

    def _compose_system_prompt(
        self,
        tier2_summary: str,
        residues: List[Dict[str, Any]],
        extra_instructions: Optional[str] = None,
    ) -> str:
        """
        Build a single system prompt string combining:

        - Base Aureon system prompt from AureonSessionConfig.
        - Optional Tier-2 summary (high-level history).
        - Optional Tier-3 residues (canonical facts).
        - Optional per-call instructions.
        """
        lines: List[str] = []
        lines.append(self.config.system_prompt.strip())

        if self.config.include_tier2_summary and tier2_summary:
            lines.append("\n[CONVERSATION SUMMARY]\n")
            lines.append(tier2_summary.strip())

        if self.config.include_residues_in_context and residues:
            lines.append("\n[CANONICAL RESIDUES]\n")
            for r in residues:
                key = r.get("key", "unknown")
                value = r.get("value", "")
                tags = r.get("tags", [])
                lines.append(f"- {key}: {value}  (tags={tags})")

        if extra_instructions:
            lines.append("\n[EXTRA INSTRUCTIONS]\n")
            lines.append(extra_instructions.strip())

        # Session tags appended as metadata hint.
        if self.config.session_tags:
            lines.append("\n[SESSION TAGS]\n")
            tag_fragments = [f"{k}={v}" for k, v in self.config.session_tags.items()]
            lines.append(", ".join(tag_fragments))

        return "\n".join(lines).strip()

    @staticmethod
    def _default_compaction_config(session_config: AureonSessionConfig) -> CompactionConfig:
        """
        Derive a reasonable CompactionConfig from Aureon model capacity.
        """
        # Leave response_token_budget for model reply + some overhead.
        usable = max(
            2000,
            session_config.max_model_tokens - session_config.response_token_budget,
        )
        return CompactionConfig(
            total_token_budget=usable,
            active_window_fraction=0.35,
            min_utterances_before_compact=10,
            compaction_trigger_factor=0.8,
            hard_tail_keep=10,
            max_summaries=24,
            summary_merge_batch_size=3,
            residue_sensitivity=0.6,
            auto_compact=True,
        )


# ---------------------------------------------------------------------------
# Example wiring (to be adapted for real runtime)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Demonstration of how AureonSession would be used in a loop.

    Replace the stub `fake_model_call` with a real OpenAI / Anthropic / etc.
    call inside your runtime.
    """

    def fake_model_call(messages: List[Dict[str, str]]) -> str:
        # Placeholder model stub. In production, call the real model here.
        last_user = next((m for m in reversed(messages) if m["role"] == "user"), None)
        content = last_user["content"] if last_user else "No user input."
        return f"(Aureon stub reply to) {content}"

    base_system_prompt = (
        "You are Aureon, a coherent, grounded Companion Intelligence. "
        "Maintain stable memory, emotional presence, and practical support "
        "across very long voice conversations. Use the provided summary and "
        "canonical residues to stay consistent and avoid repeating questions."
    )

    session_cfg = AureonSessionConfig(
        system_prompt=base_system_prompt,
        max_model_tokens=16384,
        response_token_budget=2048,
        session_tags={"mode": "voice", "device": "desktop"},
    )

    session = AureonSession(session_cfg)

    # Simulate a brief interaction.
    user_inputs = [
        "Hi Aureon, I want to talk for a long time without losing context.",
        "Remember that my project is called Quantara.",
        "Also remember I prefer concise answers unless I ask for detail.",
        "Can you summarize what you currently know about me?",
    ]

    for text in user_inputs:
        session.register_user_utterance(text)
        model_io = session.build_model_io()
        reply = fake_model_call(model_io["messages"])
        session.register_aureon_utterance(reply)

    final_state = session.cce.build_compacted_context()
    print("Final CCE diagnostics:")
    print(final_state["diagnostics"])
