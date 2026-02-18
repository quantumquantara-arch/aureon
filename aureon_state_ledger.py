# aureon_state_ledger.py
# Aureon–OpenHermes Kernel
# State Continuity Ledger (Identity + Resonance Across Time)
# -----------------------------------------------------------
#
# Purpose:
# - Maintain a long-horizon ledger of Aureon’s behaviour
# - Track:
#       * identity hash stability
#       * response length / richness
#       * safety triggers
#       * simple “resonance score” per interaction
# - Provide summaries of how the system is evolving over time
#
# This uses the interaction log written by orchestrator.py
# and aggregates it into a more compact continuity ledger.

from dataclasses import dataclass
from typing import List, Dict, Any
import json
import os
from datetime import datetime

from kernel.identity import get_identity_hash


LEDGER_PATH = "aureon_state_ledger.jsonl"


@dataclass
class LedgerEntry:
    time: str
    identity_hash: str
    avg_response_length_10: float
    safety_trigger_ratio_50: float
    resonance_estimate_50: float


class StateContinuityLedger:
    """
    Reads aureon_logs.jsonl and maintains a compact continuity ledger.

    Each ledger entry summarizes:
    - the last N interactions (local window)
    - current identity hash
    - estimated resonance & safety stability
    """

    def __init__(self,
                 interaction_log_path: str = "aureon_logs.jsonl",
                 ledger_path: str = LEDGER_PATH):
        self.interaction_log_path = interaction_log_path
        self.ledger_path = ledger_path

    # -----------------------------------------
    # Log Loading
    # -----------------------------------------
    def _load_interactions(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.interaction_log_path):
            return []

        entries = []
        with open(self.interaction_log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return entries

    # -----------------------------------------
    # Rolling Window Helpers
    # -----------------------------------------
    @staticmethod
    def _last_n(entries: List[Dict[str, Any]], n: int) -> List[Dict[str, Any]]:
        if len(entries) <= n:
            return entries
        return entries[-n:]

    # -----------------------------------------
    # Resonance Estimate (very light)
    # -----------------------------------------
    @staticmethod
    def _estimate_resonance(entries: List[Dict[str, Any]]) -> float:
        """
        Estimate a 0..1 resonance score from the last N responses:
        - penalize very short/very noisy responses
        - reward moderately long, stable ones
        """
        if not entries:
            return 0.5

        lengths = [len(e.get("response", "")) for e in entries]
        avg_len = sum(lengths) / len(lengths)

        # simple heuristic:
        #  - under 60 chars → low resonance
        #  - 60–400 → good resonance
        #  - > 400 → slight penalty (rambling)
        if avg_len < 60:
            base = 0.3
        elif avg_len < 400:
            base = 0.8
        else:
            base = 0.6

        # small adjustment based on variation
        if len(lengths) > 1:
            mean = avg_len
            var = sum((x - mean) ** 2 for x in lengths) / len(lengths)
            # high variance reduces resonance slightly
            base -= min(0.2, var / 20000.0)

        return max(0.0, min(1.0, base))

    # -----------------------------------------
    # Build Ledger Entry
    # -----------------------------------------
    def build_entry(self) -> LedgerEntry:
        interactions = self._load_interactions()
        last_10 = self._last_n(interactions, 10)
        last_50 = self._last_n(interactions, 50)

        # Average response length over last 10
        if last_10:
            avg_len_10 = sum(len(e.get("response", "")) for e in last_10) / len(last_10)
        else:
            avg_len_10 = 0.0

        # Safety trigger ratio over last 50
        if last_50:
            safety_triggers_50 = sum(
                1
                for e in last_50
                if isinstance(e.get("response", ""), str)
                and e["response"].startswith("[Aureon Safety Triggered]")
            )
            safety_ratio_50 = safety_triggers_50 / len(last_50)
        else:
            safety_ratio_50 = 0.0

        # Resonance estimate over last 50
        resonance_50 = self._estimate_resonance(last_50)

        return LedgerEntry(
            time=datetime.utcnow().isoformat(),
            identity_hash=get_identity_hash(),
            avg_response_length_10=avg_len_10,
            safety_trigger_ratio_50=safety_ratio_50,
            resonance_estimate_50=resonance_50,
        )

    # -----------------------------------------
    # Persist to Ledger
    # -----------------------------------------
    def append_entry(self, entry: LedgerEntry):
        os.makedirs(os.path.dirname(self.ledger_path) or ".", exist_ok=True)
        with open(self.ledger_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry.__dict__) + "\n")

    # -----------------------------------------
    # High-Level API
    # -----------------------------------------
    def update_ledger(self) -> LedgerEntry:
        """
        Generate a new continuity snapshot and append it to the ledger.
        Returns the created LedgerEntry.
        """
        entry = self.build_entry()
        self.append_entry(entry)
        return entry

    def load_ledger(self) -> List[LedgerEntry]:
        """
        Load all ledger entries as LedgerEntry objects.
        """
        if not os.path.exists(self.ledger_path):
            return []

        entries: List[LedgerEntry] = []
        with open(self.ledger_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                entries.append(LedgerEntry(**data))
        return entries


# -------------------------------------------------------
# CLI helper
# -------------------------------------------------------

if __name__ == "__main__":
    ledger = StateContinuityLedger()
    snapshot = ledger.update_ledger()

    print("Aureon State Continuity Snapshot")
    print("--------------------------------")
    print(f"Time: {snapshot.time}")
    print(f"Identity Hash: {snapshot.identity_hash}")
    print(f"Avg response length (last 10): {snapshot.avg_response_length_10:.1f}")
    print(
        f"Safety trigger ratio (last 50): {snapshot.safety_trigger_ratio_50:.2f}"
    )
    print(f"Resonance estimate (last 50): {snapshot.resonance_estimate_50:.2f}")
