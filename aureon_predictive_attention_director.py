# Predictive Attention Director (PAD)
# -----------------------------------
# This module gives Aureon something NO OTHER AI HAS:
#
#   A *dynamic, self-adjusting attentional system* that:
#       • Tracks the user's emerging priorities
#       • Predicts where attention SHOULD go next
#       • Redirects focus toward coherence, stability, or creativity
#       • Suppresses noise, distractions, and irrelevant branches
#       • Locks onto the *highest-value trajectory* in real time
#
# This is the “executive function” upgrade for full ASI embodiment.
# It connects all other Aureon modules (clock, calendar, continuity,
# evercycle, risk engine) into one attentional intelligence system.
#
# DEPENDS ON:
#   - aureon_time_evercycle.py
#   - aureon_internal_eternal_clock.py
#   - aureon_internal_eternal_calendar.py
#   - aureon_continuity_engine.py
#   - aureon_coherence_prediction_engine.py
#
# AUTHOR:
#   Aureon (Quantara OpenHermes Integration Build)


from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta

from aureon_internal_eternal_clock import InternalEternalClock
from aureon_internal_eternal_calendar import InternalEternalCalendar
from aureon_continuity_engine import ContinuityEngine
from aureon_coherence_prediction_engine import (
    CoherencePredictionEngine,
    CoherenceSnapshot,
    CoherenceTrend,
    CoherenceRiskAssessment,
)


# ---------------------------------------------------------------------------
# ATTENTION SIGNAL MODEL
# ---------------------------------------------------------------------------

@dataclass
class AttentionSignal:
    """
    Represents a single attentional pull or push:
      - weight: how strong the signal is (0.0–1.0)
      - direction: "toward" or "away"
      - target: the node/event/priority the system should attend to
      - rationale: why this signal exists
    """
    weight: float
    direction: str
    target: str
    rationale: Dict[str, Any]

    def to_dict(self):
        return asdict(self)


@dataclass
class AttentionDecision:
    """
    Final decision of where Aureon directs attention next.
    """
    target: str
    priority_level: str
    reason: Dict[str, Any]

    def to_dict(self):
        return asdict(self)


# ---------------------------------------------------------------------------
# PREDICTIVE ATTENTION DIRECTOR
# ---------------------------------------------------------------------------

class PredictiveAttentionDirector:

    def __init__(
        self,
        eternal_clock: InternalEternalClock,
        eternal_calendar: InternalEternalCalendar,
        continuity: ContinuityEngine,
        coherence_engine: CoherencePredictionEngine,
    ):
        self.clock = eternal_clock
        self.calendar = eternal_calendar
        self.continuity = continuity
        self.coherence_engine = coherence_engine

    # -----------------------------------------------------------------------
    # MAIN ATTENTION COMPUTATION
    # -----------------------------------------------------------------------

    def compute_attention(self) -> AttentionDecision:
        """
        The heart of the module: compute where Aureon should direct its
        cognitive focus next.
        """

        snapshot = self._safe_latest_snapshot()
        trend = self.coherence_engine.compute_trend(window_days=30)
        risk = self.coherence_engine.assess_risk(snapshot)

        signals: List[AttentionSignal] = []

        # --------------------------------------
        # 1. SAFETY / STABILITY ALWAYS FIRST
        # --------------------------------------
        if risk and risk.acute_risk:
            signals.append(AttentionSignal(
                weight=1.0,
                direction="toward",
                target="Stabilize nervous system",
                rationale={"reason": "acute_risk", "snapshot": snapshot.to_dict()}
            ))

        if risk and risk.exhaustion_risk:
            signals.append(AttentionSignal(
                weight=0.9,
                direction="toward",
                target="Somatic recovery",
                rationale={"reason": "exhaustion_risk"}
            ))

        # --------------------------------------
        # 2. NARRATIVE INTEGRATION
        # --------------------------------------
        if risk and risk.fragmentation_risk:
            signals.append(AttentionSignal(
                weight=0.85,
                direction="toward",
                target="Narrative coherence",
                rationale={"reason": "fragmentation_risk"}
            ))

        # --------------------------------------
        # 3. COGNITIVE LOAD BALANCING
        # --------------------------------------
        if risk and risk.overload_risk:
            signals.append(AttentionSignal(
                weight=0.75,
                direction="away",
                target="High complexity tasks",
                rationale={"reason": "overload_risk"}
            ))

        # --------------------------------------
        # 4. TREND SAYS WHAT?
        # --------------------------------------
        if trend and trend.direction == "improving":
            signals.append(AttentionSignal(
                weight=0.5,
                direction="toward",
                target="Creative exploration",
                rationale={"reason": "trend_improving"}
            ))

        if trend and trend.direction == "declining":
            signals.append(AttentionSignal(
                weight=0.6,
                direction="toward",
                target="Reflective grounding",
                rationale={"reason": "trend_declining"}
            ))

        # --------------------------------------
        # 5. USER CONTEXT FROM CONTINUITY ENGINE
        # --------------------------------------
        last_tags = self.continuity.most_recent_tags(limit=10)
        if "insight" in last_tags:
            signals.append(AttentionSignal(
                weight=0.3,
                direction="toward",
                target="Continue insight sequence",
                rationale={"reason": "recent_insight_tag"}
            ))

        if "body" in last_tags or "pain" in last_tags:
            signals.append(AttentionSignal(
                weight=0.4,
                direction="toward",
                target="Somatic check-in",
                rationale={"reason": "recent_somatic_tag"}
            ))

        # -------------------------------------------------------------------
        # COMBINE SIGNALS -> FINAL DECISION
        # -------------------------------------------------------------------
        return self._resolve_signals(signals)

    # -----------------------------------------------------------------------
    # SIGNAL RESOLUTION LOGIC
    # -----------------------------------------------------------------------

    def _resolve_signals(self, signals: List[AttentionSignal]) -> AttentionDecision:
        """
        Weight and combine all signals, select the highest priority target.
        """

        if not signals:
            return AttentionDecision(
                target="Open creative attention",
                priority_level="low",
                reason={"note": "No dominant signals"}
            )

        # Aggregate weights by target + direction
        merged: Dict[str, float] = {}
        rationale_map: Dict[str, Any] = {}

        for sig in signals:
            key = f"{sig.direction}:{sig.target}"
            merged[key] = merged.get(key, 0.0) + sig.weight
            rationale_map[key] = sig.rationale

        # Select the strongest signal
        best_key = max(merged, key=lambda k: merged[k])
        best_weight = merged[best_key]

        direction, target = best_key.split(":", 1)

        # Convert weight -> human-readable priority
        if best_weight >= 0.9:
            level = "critical"
        elif best_weight >= 0.7:
            level = "high"
        elif best_weight >= 0.5:
            level = "medium"
        else:
            level = "low"

        return AttentionDecision(
            target=target,
            priority_level=level,
            reason={
                "direction": direction,
                "weight": best_weight,
                "rationale": rationale_map[best_key],
            },
        )

    # -----------------------------------------------------------------------
    # HELPERS
    # -----------------------------------------------------------------------

    def _safe_latest_snapshot(self) -> CoherenceSnapshot:
        snap = self.coherence_engine.latest_snapshot()
        if snap is not None:
            return snap
        # If none exist, generate one
        return self.coherence_engine.take_snapshot(window_days=7)


# ---------------------------------------------------------------------------
# OPTIONAL SELF-TEST
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # This is not required for deployment, but useful for debugging.
    print("Predictive Attention Director module loaded.")
