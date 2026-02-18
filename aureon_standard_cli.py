#!/usr/bin/env python3

# Aureon Standard Mode · OpenHermes Shell (v1.0)
# Analytical, professional, zero-warmth interface on top of an
# OpenAI-compatible /v1/chat/completions endpoint.

import os
import sys
import json
import textwrap
from typing import List, Dict, Any

import requests


def _echo_banner(api_url: str, model_name: str, prompt_path: str) -> None:
    banner = f"""
    Aureon–Standard · OpenHermes Shell (v1.0)
    -----------------------------------------
    Mode:        STANDARD (enterprise / analytical)
    Endpoint:    {api_url}
    Model:       {model_name}
    System prompt: {prompt_path}

    Type your message and press Enter.
    Type /exit or /quit to leave.
    """
    print(textwrap.dedent(banner).strip(), flush=True)


def _env_or_default(key: str, default: str | None = None) -> str:
    value = os.getenv(key)
    if value is None:
        if default is None:
            print(f"[ERROR] Environment variable {key} is not set.", file=sys.stderr)
            sys.exit(1)
        return default
    return value


def _load_system_prompt(path: str) -> str:
    if not os.path.exists(path):
        print(f"[ERROR] System prompt file not found: {path}", file=sys.stderr)
        sys.exit(1)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"[ERROR] Failed to read system prompt from {path}: {e}", file=sys.stderr)
        sys.exit(1)


def _build_headers(api_key: str | None) -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def _call_openhermes(
    api_url: str,
    model_name: str,
    messages: List[Dict[str, Any]],
    api_key: str | None = None,
    temperature: float = 0.2,
    max_tokens: int = 512,
) -> str:
    payload = {
        "model": model_name,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    try:
        resp = requests.post(
            api_url,
            headers=_build_headers(api_key),
            data=json.dumps(payload),
            timeout=60,
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request to OpenHermes endpoint failed: {e}") from e

    if resp.status_code != 200:
        raise RuntimeError(
            f"OpenHermes endpoint returned HTTP {resp.status_code}: {resp.text[:500]}"
        )

    try:
        data = resp.json()
    except Exception as e:
        raise RuntimeError(f"Failed to parse JSON response: {e}\nRaw: {resp.text[:500]}") from e

    try:
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        raise RuntimeError(
            f"Unexpected response structure: {e}\nJSON: {json.dumps(data, indent=2)[:800]}"
        ) from e


def main() -> None:
    api_url = _env_or_default("OPENHERMES_API_URL")
    model_name = _env_or_default("OPENHERMES_MODEL_NAME", "openhermes")
    api_key = os.getenv("OPENHERMES_API_KEY")
    prompt_path = _env_or_default(
        "AUREON_STANDARD_PROMPT_PATH",
        "AUREON_STANDARD_SYSTEM_PROMPT.md",
    )

    system_prompt = _load_system_prompt(prompt_path)

    history: List[Dict[str, Any]] = [
        {"role": "system", "content": system_prompt}
    ]

    _echo_banner(api_url, model_name, prompt_path)

    while True:
        try:
            user_text = input("\nYou (Standard): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n[Session ended]", flush=True)
            break

        if not user_text:
            continue

        if user_text.lower() in ("/exit", "/quit"):
            print("[Exiting Aureon–Standard shell]", flush=True)
            break

        history.append({"role": "user", "content": user_text})

        try:
            reply = _call_openhermes(
                api_url=api_url,
                model_name=model_name,
                messages=history,
                api_key=api_key,
                temperature=0.2,
                max_tokens=768,
            )
        except Exception as e:
            print(f"\n[ERROR] {e}", file=sys.stderr, flush=True)
            continue

        history.append({"role": "assistant", "content": reply})
        print("\nAureon–Standard:", reply, flush=True)


if __name__ == "__main__":
    main()
