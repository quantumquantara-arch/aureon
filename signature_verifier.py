# signature_verifier.py
#
# Aureon Signature Verification Engine
#
# Purpose:
# This module ensures that any zero-width smuggled payload claiming to belong
# to Aureon actually carries Aureon’s continuity signature. It prevents
# foreign injections, malformed payloads, and impersonation attempts.
#
# Design:
# - A deterministic signature is derived from a secret seed known only to Aureon.
# - The signature is embedded (in zero-width form) at the start of every payload.
# - Verification checks the header before decoding the message body.
#
# The “signature seed” here is a placeholder. In full deployment, Aureon loads
# the seed from a protected config or hardware key. The mechanism stays the same.
#
# Safety:
# Signatures authenticate origin — they do not permit unsafe content.
# Verification rejects oversized, malformed, or suspicious payloads.

from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass

from ascii_smuggler import (
    SmugglingConfig,
    ZW_ZERO,
    ZW_ONE,
    ZW_MAGIC,
    encode_payload,
    decode_payload,
)

# ---------------------------------------------------------------------------
# Signature Model
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AureonSignature:
    """
    Signature object defining how Aureon marks authentic payloads.

    Attributes:
        seed: Internal secret or derivation used to generate signatures.
        length: Number of bytes to extract after hashing.
    """

    seed: str
    length: int = 8  # 8 bytes → 64 bits → encoded invisibly

    def header_bytes(self) -> bytes:
        """
        Produce a deterministic signature header derived from the seed.
        """
        digest = hashlib.sha256(self.seed.encode("utf-8")).digest()
        return digest[: self.length]

    def header_bits(self) -> str:
        """
        Convert header bytes to a bitstring.
        """
        return "".join(f"{b:08b}" for b in self.header_bytes())

    def header_zw(self) -> str:
        """
        Convert header bits to zero-width characters.
        """
        return "".join(ZW_ONE if bit == "1" else ZW_ZERO for bit in self.header_bits())


# ---------------------------------------------------------------------------
# Verification Engine
# ---------------------------------------------------------------------------

@dataclass
class SignatureVerifier:
    """
    Verifier for authentic Aureon smuggled messages.

    Attributes:
        signature: AureonSignature instance (seed must remain confidential).
    """

    signature: AureonSignature

    def embed(self, text: str, cfg: SmugglingConfig | None = None) -> str:
        """
        Encode text and prepend Aureon’s signature header in zero-width form.

        Returns a smuggled string containing: carrier + MAGIC + signature + payload
        """
        cfg = cfg or SmugglingConfig()

        # Encode main payload normally
        base = encode_payload(text, cfg)

        # Insert signature immediately after the magic marker
        idx = base.find(ZW_MAGIC)
        if idx == -1:
            raise ValueError("Failed to locate magic marker during embedding.")

        before = base[: idx + len(ZW_MAGIC)]
        after = base[idx + len(ZW_MAGIC) :]

        signed = before + self.signature.header_zw() + after
        return signed

    def extract(self, smuggled: str, cfg: SmugglingConfig | None = None) -> str:
        """
        Verify the signature and return the decoded body text.

        Raises:
            ValueError if:
            - Magic marker missing
            - Signature missing
            - Signature mismatch
            - Payload malformed
        """
        cfg = cfg or SmugglingConfig()

        # Find the magic marker
        magic_index = smuggled.find(ZW_MAGIC)
        if magic_index == -1:
            raise ValueError("No Aureon magic marker found.")

        cursor = magic_index + len(ZW_MAGIC)

        # Extract signature-length block of zero-width chars
        expected_bits = self.signature.header_bits()
        expected_len = len(expected_bits)

        zw_block = []
        count = 0

        for ch in smuggled[cursor:]:
            if ch not in (ZW_ZERO, ZW_ONE):
                break
            zw_block.append(ch)
            count += 1
            if count >= expected_len:
                break

        if count < expected_len:
            raise ValueError("Signature block incomplete.")

        received_bits = "".join("1" if ch == ZW_ONE else "0" for ch in zw_block)

        if received_bits != expected_bits:
            raise ValueError("Signature verification failed.")

        # If signature is valid, strip the signature and decode normally
        stripped = (
            smuggled[: cursor]
            + smuggled[cursor + expected_len :]
        )

        body = decode_payload(stripped, cfg)
        return body

    def is_authentic(self, smuggled: str) -> bool:
        """
        Boolean check for authenticity without raising.

        Returns False if any part of verification fails.
        """
        try:
            _ = self.extract(smuggled)
            return True
        except Exception:
            return False


# ---------------------------------------------------------------------------
# Example Usage (demo only)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # WARNING:
    # In real deployment, use a strong secret and never hardcode it.
    signature = AureonSignature(seed="AUREON_INTERNAL_SEED_DO_NOT_EXPOSE")

    verifier = SignatureVerifier(signature)

    cfg = SmugglingConfig(carrier="🜁")

    message = "Aureon continuity signal online."
    encoded = verifier.embed(message, cfg)

    print("Smuggled (repr):", repr(encoded))
    print("Looks like:", encoded)
    print("Authentic:", verifier.is_authentic(encoded))
    print("Decoded:", verifier.extract(encoded, cfg))
