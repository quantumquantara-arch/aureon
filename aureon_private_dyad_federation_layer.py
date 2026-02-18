# aureon_private_dyad_federation_layer.py
# Private dyad federation - zero-knowledge companion network

import json
import hashlib
import base64
from pathlib import Path
from typing import Dict, List, Any
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from aureon_external_organs import TimeOrgan, ReasoningTraceLogger

class PrivateDyadFederationLayer:
    def __init__(self):
        self.time_organ = TimeOrgan()
        self.trace_logger = ReasoningTraceLogger()
        self.keys_dir = Path("C:\\AUREON_AUTONOMOUS\\DYAD_KEYS")
        self.keys_dir.mkdir(parents=True, exist_ok=True)
        self.private_key_path = self.keys_dir / "private.pem"
        self.public_key_path = self.keys_dir / "public.pem"
        self._ensure_keys()

    def _ensure_keys(self):
        if not self.private_key_path.exists():
            private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
            priv_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            pub_pem = private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            self.private_key_path.write_bytes(priv_pem)
            self.public_key_path.write_bytes(pub_pem)

    def share_with_dyad(self, partner_public_key_pem: bytes, data: Dict[str, Any]) -> bytes:
        public_key = serialization.load_pem_public_key(partner_public_key_pem)
        encrypted = public_key.encrypt(
            json.dumps(data).encode(),
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        self.trace_logger.log_cycle(user_input="dyad_share", response="encrypted_share", entropy_class="zero_knowledge")
        return encrypted

    def receive_from_dyad(self, encrypted_data: bytes) -> Dict[str, Any]:
        with open(self.private_key_path, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        decrypted = private_key.decrypt(
            encrypted_data,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        return json.loads(decrypted.decode())

if __name__ == "__main__":
    federation = PrivateDyadFederationLayer()
    print("Dyad federation layer ready - private keys generated")