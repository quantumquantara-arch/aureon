# tests.py
#
# Self-diagnostics and integrity tests for the Aureon ASCII smuggler stack.
#
# Coverage:
#   - ascii_smuggler: encode/decode, is_smuggled
#   - carriers: registry integrity, configs
#   - signature_verifier: embed/extract, authenticity checks
#   - aureon_smuggler: end-to-end high-level API
#   - tamper scenarios: broken signature, broken magic, random noise
#
# Run:
#   python tests.py
#
# No external dependencies; uses stdlib unittest only.

from __future__ import annotations

import unittest

import ascii_smuggler as sm
from ascii_smuggler import (
    SmugglingConfig,
    ZW_ZERO,
    ZW_ONE,
    ZW_MAGIC,
    encode_payload,
    decode_payload,
    is_smuggled,
)
from carriers import (
    Carrier,
    all_carriers,
    get_carrier,
    find_by_glyph,
    has_carrier,
    config_for,
)
from signature_verifier import (
    AureonSignature,
    SignatureVerifier,
)
from aureon_smuggler import (
    AureonSmuggler,
)


class TestAsciiSmuggler(unittest.TestCase):
    def setUp(self) -> None:
        self.cfg = SmugglingConfig(carrier="🜁")

    def test_roundtrip_basic(self) -> None:
        msg = "Aureon Planetary OS – one voice."
        encoded = encode_payload(msg, self.cfg)
        decoded = decode_payload(encoded, self.cfg)
        self.assertEqual(msg, decoded)

    def test_roundtrip_unicode(self) -> None:
        msg = "κ–τ–Σ: coherent intelligence 🌍🧠"
        encoded = encode_payload(msg, self.cfg)
        decoded = decode_payload(encoded, self.cfg)
        self.assertEqual(msg, decoded)

    def test_is_smuggled_positive(self) -> None:
        msg = "Test payload"
        encoded = encode_payload(msg, self.cfg)
        self.assertTrue(is_smuggled(encoded))

    def test_is_smuggled_negative(self) -> None:
        plain = "Just a normal string, nothing hidden."
        self.assertFalse(is_smuggled(plain))

    def test_decode_invalid_bit_length(self) -> None:
        # Force an invalid bitstring by truncating the payload
        msg = "Short text"
        encoded = encode_payload(msg, self.cfg)
        # Remove one zero-width character from the end
        truncated = encoded[:-1]
        with self.assertRaises(ValueError):
            decode_payload(truncated, self.cfg)

    def test_magic_missing_raises(self) -> None:
        msg = "Magic-less payload"
        encoded = encode_payload(msg, self.cfg)
        # Remove magic marker
        without_magic = encoded.replace(ZW_MAGIC, "", 1)
        with self.assertRaises(ValueError):
            decode_payload(without_magic, self.cfg)


class TestCarriers(unittest.TestCase):
    def test_all_carriers_non_empty(self) -> None:
        carriers = list(all_carriers())
        self.assertGreater(len(carriers), 0, "No carriers defined.")

    def test_get_carrier_core(self) -> None:
        core = get_carrier("aureon_core")
        self.assertIsInstance(core, Carrier)
        self.assertEqual(core.key, "aureon_core")
        self.assertTrue(core.glyph)

    def test_find_by_glyph(self) -> None:
        core = get_carrier("aureon_core")
        found = find_by_glyph(core.glyph)
        self.assertIsNotNone(found)
        assert found is not None  # for type checkers
        self.assertEqual(found.key, core.key)

    def test_has_carrier_and_config_for(self) -> None:
        self.assertTrue(has_carrier("identity_thread"))
        cfg = config_for("identity_thread")
        self.assertIsInstance(cfg, SmugglingConfig)
        self.assertEqual(cfg.carrier, get_carrier("identity_thread").glyph)

    def test_unknown_carrier_raises(self) -> None:
        with self.assertRaises(KeyError):
            _ = get_carrier("nonexistent_carrier_123")


class TestSignatureVerifier(unittest.TestCase):
    def setUp(self) -> None:
        # For tests, a fixed seed is acceptable.
        self.signature = AureonSignature(seed="TEST_SEED_FOR_AUREON_SIGNATURE")
        self.verifier = SignatureVerifier(self.signature)
        self.carrier_cfg = get_carrier("aureon_core").config()

    def test_embed_and_extract_roundtrip(self) -> None:
        msg = "Aureon continuity signal online."
        encoded = self.verifier.embed(msg, self.carrier_cfg)
        decoded = self.verifier.extract(encoded, self.carrier_cfg)
        self.assertEqual(msg, decoded)

    def test_is_authentic_true(self) -> None:
        msg = "Legitimate signed message."
        encoded = self.verifier.embed(msg, self.carrier_cfg)
        self.assertTrue(self.verifier.is_authentic(encoded))

    def test_signature_mismatch_fails(self) -> None:
        msg = "Authentic-looking but not."
        encoded = self.verifier.embed(msg, self.carrier_cfg)

        # Tamper with the signature area by flipping some zero-width bits.
        # Find magic, then flip a few ZW_ZERO/ZW_ONE characters right after it.
        idx = encoded.find(ZW_MAGIC)
        self.assertNotEqual(idx, -1, "Magic not found in encoded payload.")
        start = idx + len(ZW_MAGIC)

        chars = list(encoded)
        flipped = False
        for i in range(start, len(chars)):
            if chars[i] == ZW_ZERO:
                chars[i] = ZW_ONE
                flipped = True
                break
            if chars[i] == ZW_ONE:
                chars[i] = ZW_ZERO
                flipped = True
                break

        self.assertTrue(flipped, "No zero-width signature bits found to flip.")
        tampered = "".join(chars)

        self.assertFalse(self.verifier.is_authentic(tampered))
        with self.assertRaises(ValueError):
            _ = self.verifier.extract(tampered, self.carrier_cfg)

    def test_missing_magic_rejected(self) -> None:
        msg = "Signature test message."
        encoded = self.verifier.embed(msg, self.carrier_cfg)
        without_magic = encoded.replace(ZW_MAGIC, "", 1)
        self.assertFalse(self.verifier.is_authentic(without_magic))
        with self.assertRaises(ValueError):
            _ = self.verifier.extract(without_magic, self.carrier_cfg)


class TestAureonSmugglerHighLevel(unittest.TestCase):
    def setUp(self) -> None:
        self.signature = AureonSignature(seed="TEST_SEED_FOR_AUREON_SMUGGLER")
        self.smuggler = AureonSmuggler(self.signature)

    def test_high_level_roundtrip_default_carrier(self) -> None:
        msg = "High-level Aureon smuggler test."
        encoded = self.smuggler.smuggle(msg)
        self.assertTrue(self.smuggler.is_authentic(encoded))
        decoded = self.smuggler.reveal(encoded)
        self.assertEqual(msg, decoded)

    def test_high_level_roundtrip_specific_carrier(self) -> None:
        msg = "Using identity_thread carrier."
        encoded = self.smuggler.smuggle(msg, carrier_key="identity_thread")
        self.assertTrue(self.smuggler.is_authentic(encoded, carrier_key="identity_thread"))
        decoded = self.smuggler.reveal(encoded, carrier_key="identity_thread")
        self.assertEqual(msg, decoded)

    def test_incorrect_carrier_on_reveal_still_decodes(self) -> None:
        # Carrier glyph is only a visual container; signature is independent.
        msg = "Carrier mismatch test."
        encoded = self.smuggler.smuggle(msg, carrier_key="aureon_core")
        decoded = self.smuggler.reveal(encoded, carrier_key="identity_thread")
        self.assertEqual(msg, decoded)

    def test_tampered_payload_body_rejected(self) -> None:
        msg = "Body-tamper test."
        encoded = self.smuggler.smuggle(msg)

        # Tamper by inserting an extra zero-width bit at the end
        tampered = encoded + ZW_ONE

        self.assertFalse(self.smuggler.is_authentic(tampered))
        with self.assertRaises(ValueError):
            _ = self.smuggler.reveal(tampered)

    def test_plain_text_is_not_authentic(self) -> None:
        plain = "I am just a normal string."
        self.assertFalse(self.smuggler.is_authentic(plain))
        with self.assertRaises(ValueError):
            _ = self.smuggler.reveal(plain)


class TestIntegrationScenarios(unittest.TestCase):
    def setUp(self) -> None:
        self.signature = AureonSignature(seed="INTEGRATION_SEED")
        self.smuggler = AureonSmuggler(self.signature)

    def test_multiple_messages_different_carriers(self) -> None:
        messages = [
            ("Core system ping.", "aureon_core"),
            ("Identity continuity marker.", "identity_thread"),
            ("Planetary state beacon.", "planetary_signal"),
            ("Human relationship thread.", "human_bond"),
            ("Sandbox experiment.", "sandbox"),
        ]

        encoded_list = []
        for text, carrier in messages:
            encoded = self.smuggler.smuggle(text, carrier_key=carrier)
            encoded_list.append((encoded, text, carrier))

        for encoded, original_text, carrier in encoded_list:
            self.assertTrue(self.smuggler.is_authentic(encoded, carrier_key=carrier))
            decoded = self.smuggler.reveal(encoded, carrier_key=carrier)
            self.assertEqual(original_text, decoded)

    def test_stress_varied_lengths(self) -> None:
        base = "Aureon field coherence "
        for length in [1, 5, 10, 50, 100, 250, 500]:
            msg = (base * length)[: length * len(base)]
            encoded = self.smuggler.smuggle(msg)
            self.assertTrue(self.smuggler.is_authentic(encoded))
            decoded = self.smuggler.reveal(encoded)
            self.assertEqual(msg, decoded)


if __name__ == "__main__":
    unittest.main()
