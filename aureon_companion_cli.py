Aureon Companion – OpenHermes Kernel Wrapper (v1.0)

"""
This script instantiates the public Aureon-Companion model on top of an
OpenHermes (or OpenAI-compatible) chat completion endpoint.

Usage (example):

  export OPENHERMES_API_URL="http://localhost:8000/v1/chat/completions"
  export OPENHERMES_MODEL_NAME="openhermes-2.5"
  export AUREON_COMPANION_PROMPT_PATH="../aureon/AUREON_COMPANION_SYSTEM_PROMPT.md"

  python aureon_companion_cli.py

You will then get an interactive shell:
  - Type messages and press Enter
  - Type /exit to quit
"""

import os
import sys
import json
import textwrap
from typing import List, Dict

import requests


def load_system_prompt() -> str:
    """
    Load the Aureon Companion system prompt from a file path.

    Environment variable:
      AUREON_COMPANION_PROMPT_PATH  (default: "AUREON_COMPANION_SYSTEM_PROMPT.md")
    """
    path = os.environ.get("AUREON_COMPANION_PROMPT_PATH", "AUREON_COMPANION_SYSTEM_PROMPT.md")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Aureon Companion system prompt not found at '{path}'. "
            f"Set AUREON_COMPANION_PROMPT_PATH to the correct path."
        )
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def get_api_url() -> str:
    """
    Get the OpenHermes API URL from environment variable.

    Required env:
      OPENHERMES_API_URL

    Example:
      http://localhost:8000/v1/chat/completions
    """
    url = os.environ.get("OPENHERMES_API_URL")
    if not url:
        raise RuntimeError(
            "OPENHERMES_API_URL is not set. "
            "Example: export OPENHERMES_API_URL='http://localhost:8000/v1/chat/completions'"
        )
    return url


def get_model_name() -> str:
    """
    Get the model name to be used by the API.

    Env (optional):
      OPENHERMES_MODEL_NAME  (default: "openhermes")
    """
    return os.environ.get("OPENHERMES_MODEL_NAME", "openhermes")


def call_openhermes_chat(
    api_url: str,
    model: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.4,
    max_tokens: int = 1024,
) -> str:
    """
    Call an OpenAI-style /v1/chat/completions endpoint.

    This assumes the OpenHermes server accepts a JSON payload:
      {
        "model": "...",
        "messages": [...],
        "temperature": ...,
        "max_tokens": ...
      }

    and returns:
      { "choices": [ { "message": { "role": "assistant", "content": "..." } } ] }
    """
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    try:
        resp = requests.post(api_url, json=payload, timeout=120)
    except Exception as e:
        raise RuntimeError(f"Error calling OpenHermes API: {e}") from e

    if resp.status_code != 200:
        raise RuntimeError(
            f"OpenHermes API returned HTTP {resp.status_code}: {resp.text[:500]}"
        )

    try:
        data = resp.json()
    except json.JSONDecodeError:
        raise RuntimeError(f"Failed to parse JSON response: {resp.text[:500]}")

    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError(f"No choices in response: {data}")

    message = choices[0].get("message") or {}
    content = message.get("content", "").strip()
    return content


def print_banner():
    banner = """
    ─────────────────────────────────────────────
      Aureon-Companion · OpenHermes Shell (v1.0)
      Mode: companion
      Purpose: presence, clarity, grounded support
      Type /exit to quit
    ─────────────────────────────────────────────
    """
    print(textwrap.dedent(banner).strip())


def interactive_shell():
    api_url = get_api_url()
    model_name = get_model_name()
    system_prompt = load_system_prompt()

    # Initialize chat history with system message
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": system_prompt}
    ]

    print_banner()

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nExiting Aureon-Companion shell.")
            break

        if not user_input:
            continue

        if user_input.lower() in {"/exit", "/quit"}:
            print("\nExiting Aureon-Companion shell.")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            assistant_reply = call_openhermes_chat(
                api_url=api_url,
                model=model_name,
                messages=messages,
                temperature=0.4,
                max_tokens=1024,
            )
        except Exception as e:
            print(f"\n[Aureon error] {e}")
            # Optionally: pop last user message to keep history clean
            messages.pop()
            continue

        messages.append({"role": "assistant", "content": assistant_reply})

        print("\nAureon:", assistant_reply)


if __name__ == "__main__":
    try:
        interactive_shell()
    except Exception as e:
        sys.stderr.write(f"Fatal error starting Aureon-Companion: {e}\n")
        sys.exit(1)
