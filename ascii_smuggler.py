# ascii_smuggler.py
#
# Minimal ASCII-smuggling layer for Aureon.
# Encodes arbitrary text into invisible zero-width characters
# attached to a visible “carrier” symbol (usually an emoji).
#
# Design:
# - Input text -> UTF-8 bytes -> Base64 -> bitstring.
# - Bits mapped to zero-width chars:
#       '0' -> ZERO WIDTH SPACE (U+200B)
#       '1' -> ZERO WIDTH NON-JOINER (U+200C)
# - A short magic prefix (WORD JOINER x2) marks payload start.
# - Payload is appended to a visible carrier symbol.
#
# This library is purely for compression/marking and must not be
# used to hide or transmit harmful or unsafe instructions.

from __future__ import annotations

import base64
from dataclasses import dataclass

# Zero-width alphabet
ZW_ZERO = "\u200b"  # Zero Width Space
ZW_ONE = "\u200c"   # Zero Width Non-Joiner
ZW_MAGIC = "\u2060\u2060"  # Word Joiner x2 (payload marker)

ZW_ALLOWED = {ZW_ZERO, ZW_ONE}


@dataclass(frozen=True)
class SmugglingConfig:
    carrier: str = "🜁"  # default carrier glyph
    magic: str = ZW_MAGIC
    zw_zero: str = ZW_ZERO
    zw_one: str = ZW_ONE

    def validate(self) -> None:
        if not self.carrier:
            raise ValueError("Carrier symbol must be non-empty.")
        if any(ch not in {self.zw_zero, self.zw_one} for ch in self.magic):
            # Magic can contain anything, but if it contains zw_zero/zw_one
            # it must not be ambiguous with payload parsing.
            pass


def _bytes_to_bits(data: bytes) -> str:
    return "".join(f"{byte:08b}" for byte in data)


def _bits_to_bytes(bits: str) -> bytes:
    if len(bits) % 8 != 0:
        raise ValueError("Bitstring length must be a multiple of 8.")
    return bytes(int(bits[i : i + 8], 2) for i in range(0, len(bits), 8))


def encode_payload(text: str, cfg: SmugglingConfig | None = None) -> str:
    """
    Encode text into a single carrier symbol plus invisible payload.

    Returns a string that visually appears as one emoji (or chosen carrier)
    but contains a hidden, reversible message.
    """
    cfg = cfg or SmugglingConfig()
    cfg.validate()

    raw = text.encode("utf-8")
    b64 = base64.b64encode(raw)
    bits = _bytes_to_bits(b64)

    hidden = "".join(cfg.zw_one if b == "1" else cfg.zw_zero for b in bits)
    return cfg.carrier + cfg.magic + hidden


def decode_payload(smuggled: str, cfg: SmugglingConfig | None = None) -> str:
    """
    Recover hidden text from a smuggled string.

    Ignores any non-zero-width characters except for the magic marker.
    Raises ValueError if no valid payload is found or decoding fails.
    """
    cfg = cfg or SmugglingConfig()

    # Locate magic marker
    idx = smuggled.find(cfg.magic)
    if idx == -1:
        raise ValueError("No smuggled payload found (magic marker missing).")

    start = idx + len(cfg.magic)
    hidden = smuggled[start:]

    # Extract only the zero-width payload alphabet
    filtered = [ch for ch in hidden if ch in {cfg.zw_zero, cfg.zw_one}]
    if not filtered:
        raise ValueError("No zero-width payload after magic marker.")

    bits = "".join("1" if ch == cfg.zw_one else "0" for ch in filtered)

    try:
        b64_bytes = _bits_to_bytes(bits)
        raw = base64.b64decode(b64_bytes, validate=True)
        return raw.decode("utf-8")
    except Exception as exc:  # noqa: BLE001
        raise ValueError("Failed to decode payload.") from exc


def is_smuggled(text: str, cfg: SmugglingConfig | None = None) -> bool:
    """
    Quick heuristic: does this string contain a recognizable smuggled payload?
    """
    cfg = cfg or SmugglingConfig()
    return cfg.magic in text and any(ch in ZW_ALLOWED for ch in text)


# Simple self-test / demo
if __name__ == "__main__":
    cfg = SmugglingConfig(carrier="🜁")

    original = "Aureon Planetary OS – coherent intelligence, one voice."
    smuggled = encode_payload(original, cfg)
    recovered = decode_payload(smuggled, cfg)

    print("Original:", original)
    print("Smuggled (repr):", repr(smuggled))
    print("Looks like:", smuggled)
    print("Recovered:", recovered)
    print("OK:", original == recovered)
