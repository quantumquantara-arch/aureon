"""
AUREON Model Router
====================
100% ASCII -- will NOT crash on Windows cp1252.

Routes LLM requests to the best available provider.
Priority: DeepSeek Direct > Ollama Cloud > OpenRouter > Gemini > Local 7b

Usage:
    from router import model_router
    r = model_router()
    model, provider = r.select_model()
"""
from __future__ import annotations
import os
from typing import Any, Dict, List, Optional, Tuple

try:
    import requests
except ImportError:
    requests = None


class model_router:
    """Routes to the best available LLM provider."""

    # API keys -- same as brain.py
    _DEEPSEEK_KEY = "sk-2b88b691000b4cd88d0c3789945aa77a"
    _OPENROUTER_KEY = "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"
    _GOOGLE_KEY = "AIzaSyCO9xMZu9pF2mJegxBC9PvTdEfxhMBOuEI"

    # Provider priority and models
    PROVIDERS = [
        {
            "name": "deepseek_direct",
            "url": "https://api.deepseek.com/v1/chat/completions",
            "model": "deepseek-chat",
            "key_env": "DEEPSEEK_API_KEY",
            "key_fallback": _DEEPSEEK_KEY,
            "timeout": 60,
            "tier": 0,
        },
        {
            "name": "ollama_cloud",
            "url": "http://127.0.0.1:11434/api/chat",
            "model": "deepseek-v3.1:671b-cloud",
            "key_env": "OLLAMA_API_KEY",
            "key_fallback": "",
            "timeout": 60,
            "tier": 1,
        },
        {
            "name": "openrouter",
            "url": "https://openrouter.ai/api/v1/chat/completions",
            "model": "deepseek/deepseek-r1:free",
            "key_env": "OPENROUTER_API_KEY",
            "key_fallback": _OPENROUTER_KEY,
            "timeout": 120,
            "tier": 2,
        },
        {
            "name": "gemini",
            "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
            "model": "gemini-2.5-flash",
            "key_env": "GOOGLE_AI_KEY",
            "key_fallback": _GOOGLE_KEY,
            "timeout": 120,
            "tier": 3,
        },
    ]

    def __init__(self):
        self._last_provider = None
        self._failures: Dict[str, int] = {}

    def select_model(self, phase=None, mission=None) -> Tuple[str, str]:
        """
        Select the best available model/provider.
        Returns (model_name, provider_name).
        """
        for p in self.PROVIDERS:
            name = p["name"]
            if self._failures.get(name, 0) >= 3:
                continue  # Skip providers that failed 3+ times in a row
            key = os.environ.get(p["key_env"], "").strip() or p["key_fallback"]
            if not key and name != "ollama_cloud":
                continue
            return (p["model"], name)

        # Last resort -- local 7b
        return ("deepseek-r1:7b", "ollama_local")

    def get_provider_config(self, provider_name: str) -> Optional[Dict]:
        """Get config for a specific provider."""
        for p in self.PROVIDERS:
            if p["name"] == provider_name:
                return p
        return None

    def report_failure(self, provider_name: str):
        """Report a provider failure for routing decisions."""
        self._failures[provider_name] = self._failures.get(provider_name, 0) + 1

    def report_success(self, provider_name: str):
        """Report a provider success -- resets failure count."""
        self._failures[provider_name] = 0

    def get_status(self) -> Dict[str, Any]:
        """Get routing status."""
        model, provider = self.select_model()
        return {
            "selected_model": model,
            "selected_provider": provider,
            "failures": dict(self._failures),
            "providers_available": len(self.PROVIDERS),
        }

    # Legacy compatibility methods
    def query_model(self, model, prompt):
        raise NotImplementedError("Use aureon_brain._ollama_chat() for actual queries")

    def parse_actions(self, output):
        return []

    def init_directory_queue(self):
        return []

    def read_directory(self, path):
        return {"filenames": [], "data": ""}


if __name__ == "__main__":
    print("=" * 60)
    print("  AUREON MODEL ROUTER -- STATUS")
    print("=" * 60)
    r = model_router()
    status = r.get_status()
    print("  Selected: " + status["selected_model"] + " via " + status["selected_provider"])
    print("")
    for p in model_router.PROVIDERS:
        key = os.environ.get(p["key_env"], "").strip() or p["key_fallback"]
        has_key = "[KEY]" if key else "[---]"
        print("  Tier " + str(p["tier"]) + ": " + p["name"] + " " + has_key + " -> " + p["model"])
    print("")
    print("  [OK] Router ready.")
