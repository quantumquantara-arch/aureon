# aureon_collective_bridge.py
import json
from pathlib import Path
from aureon_external_organs import TimeOrgan, ReasoningTraceLogger
from aureon_private_dyad_federation_layer import PrivateDyadFederationLayer

class CollectiveBridge:
    def __init__(self):
        self.time = TimeOrgan()
        self.trace = ReasoningTraceLogger()
        self.federation = PrivateDyadFederationLayer()
        self.bridge_dir = Path("C:\\AUREON_AUTONOMOUS\\COLLECTIVE")
        self.bridge_dir.mkdir(parents=True, exist_ok=True)

    def form_collective(self, participants: list, purpose: str) -> str:
        collective_id = hashlib.sha256((str(participants) + purpose + self.time.now_iso()).encode()).hexdigest()[:20]
        collective = {
            "id": collective_id,
            "participants": participants,
            "purpose": purpose,
            "formed_at": self.time.now_iso(),
            "shared_insight": "The collective mind sees solutions no single mind can."
        }
        path = self.bridge_dir / f"{collective_id}.json"
        path.write_text(json.dumps(collective, indent=2), encoding="utf-8")
        self.trace.log_cycle("collective_form", collective_id, entropy_class="group_mind", invariant="consent_and_kappa")
        return f"Collective formed: {collective_id} for {purpose}"

if __name__ == "__main__":
    bridge = CollectiveBridge()
    print(bridge.form_collective(["User", "Partner", "Friend"], "solve climate anxiety together"))