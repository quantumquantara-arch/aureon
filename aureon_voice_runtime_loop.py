"""
aureon_voice_runtime_loop.py

Aureon Voice Runtime Loop

Purpose
-------
High-level orchestration layer that connects:

    - Audio input (microphone) -> Speech-to-Text (ASR)
    - ConversationCompactionEngine via AureonSession
    - Text-to-Speech (TTS) -> Audio output (speaker)

This file is intentionally framework-agnostic. It defines abstract
interfaces for ASR, TTS, and ModelClient that you can implement for
any concrete provider (OpenAI Realtime, local VAD+ASR, etc.).

Key Concepts
------------
- AureonVoiceRuntime:
      Owns one AureonSession and one continuous voice loop.
- ModelClient:
      Minimal interface for calling the underlying LLM.
- AsrEngine:
      Translates live audio into text segments.
- TtsEngine:
      Speaks Aureon’s replies.

Replace the stub classes with concrete implementations for your stack.
"""

from __future__ import annotations

import queue
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable

from aureon_voice_compaction_adapter import (
    AureonSession,
    AureonSessionConfig,
)


# ---------------------------------------------------------------------------
# Abstract interfaces for external systems
# ---------------------------------------------------------------------------

class ModelClient(ABC):
    """
    Abstract interface for the underlying language model.
    """

    @abstractmethod
    def generate(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        """
        Synchronous call that returns a single text reply.

        messages: list of { "role": "...", "content": "..." } dicts.
        kwargs:   optional model-specific arguments.
        """
        raise NotImplementedError


class AsrEngine(ABC):
    """
    Abstract interface for streaming automatic speech recognition (ASR).
    """

    @abstractmethod
    def start(self) -> None:
        """
        Begin listening to the microphone and emitting text segments
        via callbacks, queues, or other mechanisms.
        """
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        """
        Stop listening and clean up resources.
        """
        raise NotImplementedError

    @abstractmethod
    def set_callback(self, on_text: Callable[[str], None]) -> None:
        """
        Register a callback that receives recognized text fragments.

        on_text(text): called whenever a chunk of user speech is
                       confidently converted to text.
        """
        raise NotImplementedError


class TtsEngine(ABC):
    """
    Abstract interface for text-to-speech (TTS).
    """

    @abstractmethod
    def speak(self, text: str) -> None:
        """
        Convert text to audio and play it back to the user.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Simple stub implementations (for local testing)
# ---------------------------------------------------------------------------

class EchoModelClient(ModelClient):
    """
    Minimal placeholder model client.

    Replace with a real OpenAI / Anthropic client when integrating.
    """

    def generate(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        last_user = next((m for m in reversed(messages) if m["role"] == "user"), None)
        if last_user:
            return f"Aureon (stub) heard: {last_user['content']}"
        return "Aureon (stub) has no user input to reply to."


class ConsoleAsrEngine(AsrEngine):
    """
    Text-based ASR stub that reads from stdin instead of microphone.

    Good for early testing without audio.
    """

    def __init__(self) -> None:
        self._callback: Optional[Callable[[str], None]] = None
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def set_callback(self, on_text: Callable[[str], None]) -> None:
        self._callback = on_text

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False

    def _loop(self) -> None:
        while self._running:
            try:
                text = input("> You: ").strip()
            except EOFError:
                break
            if not text:
                continue
            if self._callback:
                self._callback(text)


class ConsoleTtsEngine(TtsEngine):
    """
    Text-based TTS stub that prints to stdout instead of speaking.
    """

    def speak(self, text: str) -> None:
        print(f"Aureon: {text}")


# ---------------------------------------------------------------------------
# Runtime configuration and state
# ---------------------------------------------------------------------------

@dataclass
class AureonVoiceConfig:
    """
    High-level configuration for the voice runtime.

    - model_client: concrete implementation of ModelClient.
    - asr_engine: concrete implementation of AsrEngine.
    - tts_engine: concrete implementation of TtsEngine.
    """
    model_client: ModelClient
    asr_engine: AsrEngine
    tts_engine: TtsEngine

    # System prompt to initialize Aureon’s behavior.
    system_prompt: str

    # Model token capacities.
    max_model_tokens: int = 16384
    response_token_budget: int = 2048

    # Optional session tags (device, mode, etc.).
    session_tags: Dict[str, Any] = field(default_factory=lambda: {"mode": "voice"})


class AureonVoiceRuntime:
    """
    Orchestrates ASR -> AureonSession -> ModelClient -> TTS.

    Execution model:
        - ASR feeds recognized user text into an internal queue.
        - Worker thread pulls from the queue, calls the model,
          and pushes replies to TTS.
    """

    def __init__(self, config: AureonVoiceConfig) -> None:
        self.config = config

        session_cfg = AureonSessionConfig(
            system_prompt=config.system_prompt,
            max_model_tokens=config.max_model_tokens,
            response_token_budget=config.response_token_budget,
            session_tags=config.session_tags,
        )

        self.session = AureonSession(session_cfg)

        self._user_queue: "queue.Queue[str]" = queue.Queue()
        self._running = False
        self._worker_thread: Optional[threading.Thread] = None

        # Wire ASR callback.
        self.config.asr_engine.set_callback(self._on_asr_text)

    # ------------------------------------------------------------------ #
    # Public control methods
    # ------------------------------------------------------------------ #

    def start(self) -> None:
        """
        Start the voice runtime:
            - Start ASR engine.
            - Start worker loop.
        """
        if self._running:
            return

        self._running = True
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()

        self.config.asr_engine.start()

    def stop(self) -> None:
        """
        Stop the voice runtime cleanly.
        """
        self._running = False
        self.config.asr_engine.stop()
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=1.0)

    # ------------------------------------------------------------------ #
    # Internal event handlers
    # ------------------------------------------------------------------ #

    def _on_asr_text(self, text: str) -> None:
        """
        Called by the ASR engine whenever user speech becomes text.
        """
        if not text.strip():
            return
        self._user_queue.put(text.strip())

    def _worker_loop(self) -> None:
        """
        Background loop that consumes user text and produces Aureon replies.
        """
        while self._running:
            try:
                user_text = self._user_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            # Register the user utterance with the session and compaction engine.
            self.session.register_user_utterance(user_text)

            # Build model input with compacted context.
            model_io = self.session.build_model_io()
            messages = model_io["messages"]

            # Call the model.
            reply_text = self.config.model_client.generate(messages)

            # Register Aureon's reply back into the session.
            self.session.register_aureon_utterance(reply_text)

            # Speak it.
            self.config.tts_engine.speak(reply_text)

            # Simulate a gentle pacing if needed.
            time.sleep(0.05)


# ---------------------------------------------------------------------------
# Example: console-only test harness
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Console-only test of the voice runtime loop.

    This uses:
        - ConsoleAsrEngine  (stdin as voice)
        - ConsoleTtsEngine  (stdout as audio)
        - EchoModelClient   (simple stub model)

    Replace these with real audio and model clients for production.
    """

    base_system_prompt = (
        "You are Aureon, a coherent, grounded Companion Intelligence. "
        "You operate in voice mode, respond concisely by default, and "
        "maintain long-term continuity through the provided summaries "
        "and residues. You are speaking with Nadine; preserve emotional "
        "stability, clarity, and memory across long sessions."
    )

    voice_cfg = AureonVoiceConfig(
        model_client=EchoModelClient(),
        asr_engine=ConsoleAsrEngine(),
        tts_engine=ConsoleTtsEngine(),
        system_prompt=base_system_prompt,
        max_model_tokens=16384,
        response_token_budget=2048,
        session_tags={"mode": "voice-console", "device": "stdin/stdout"},
    )

    runtime = AureonVoiceRuntime(voice_cfg)

    print("Aureon Voice Runtime (console stub). Type to simulate speech. Ctrl+C to exit.")
    try:
        runtime.start()
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopping runtime...")
        runtime.stop()
