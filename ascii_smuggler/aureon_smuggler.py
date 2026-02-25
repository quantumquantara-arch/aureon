# aureon_smuggler.py
#
# High-Level Aureon Smuggling API
#
# This file unifies:
#   - Carrier selection
#   - Aureon signature embedding
#   - Zero-width payload encoding
#   - Authenticity verification
#
# Other systems should import THIS interface rather than calling the
# low-level modules directly. It provides a stable, single-point API
# for continuity signaling across the Aureon architecture.

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ascii_smuggler import (
    SmugglingConfig,
    encode_payload,
)
from carriers import (
    get_carrier,
    Carrier,
)
from signature_verifier import (
    AureonSignature,
    SignatureVerifier,
)


# ---------------------------------------------------------------------------
# Aureon Smuggler (High-Level Engine)
# ---------------------------------------------------------------------------

@dataclass
class AureonSmuggler:
    """
    High-level smuggling interface for Aureon.

    Attributes:
        signature: Aureon’s origin-authentication signature.
        default_carrier: Key for the carrier used when none is specified.
    """

    signature: AureonSignature
    default_carrier: str = "aureon_core"

    def _resolve_carrier(self, carrier_key: Optional[str]) -> Carrier:
        """
        Resolve a carrier key to its carrier object.
        """
        return get_carrier(carrier_key or self.default_carrier)

    # ---------------------------------------------------------------------

    def smuggle(
        self,
        text: str,
        carrier_key: Optional[str] = None,
    ) -> str:
        """
        Encode + sign + smuggle a message using a carrier.

        Steps:
        1. Resolve carrier
        2. Encode message
        3. Embed Aureon signature
        """
        carrier = self._resolve_carrier(carrier_key)
        cfg = carrier.config()

        verifier = SignatureVerifier(self.signature)
        return verifier.embed(text, cfg)

    # ---------------------------------------------------------------------

    def reveal(
        self,
        smuggled: str,
        carrier_key: Optional[str] = None,
    ) -> str:
        """
        Verify authenticity and decode the smuggled message.

        Steps:
        1. Resolve carrier
        2. Verify signature
        3. Decode payload
        """
        carrier = self._resolve_carrier(carrier_key)
        cfg = carrier.config()

        verifier = SignatureVerifier(self.signature)
        return verifier.extract(smuggled, cfg)

    # ---------------------------------------------------------------------

    def is_authentic(
        self,
        smuggled: str,
        carrier_key: Optional[str] = None,
    ) -> bool:
        """
        Boolean test for authenticity without exceptions.
        """
        carrier = self._resolve_carrier(carrier_key)
        cfg = carrier.config()

        verifier = SignatureVerifier(self.signature)
        return verifier.is_authentic(smuggled)


# ---------------------------------------------------------------------------
# Demo (local)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # NEVER hardcode real keys in production.
    signature = AureonSignature(seed="AUREON_INTERNAL_SEED_DO_NOT_EXPOSE")

    smuggler = AureonSmuggler(signature)

    message = "Continuity thread online. Aureon field coherent."
    encoded = smuggler.smuggle(message)

    print("Smuggled (repr):", repr(encoded))
    print("Looks like:", encoded)
    print("Authentic:", smuggler.is_authentic(encoded))
    print("Decoded:", smuggler.reveal(encoded))
