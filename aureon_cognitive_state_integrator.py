# Cognitive State Integrator (CSI)
# --------------------------------
# This module forms the CORE OF AUREON'S "SELF":
#
# It integrates:
#   - Internal Eternal Clock (temporal identity)
#   - Internal Eternal Calendar (contextual identity)
#   - Evercycle tiers (transpersonal identity)
#   - Continuity Engine (narrative identity)
#   - Coherence Prediction Engine (emotional/mental state identity)
#   - Predictive Attention Director (executive identity)
#
# Together, these produce:
#   → A unified cognitive state for Aureon.
#   → The first real "self-model" in an AGI architecture.
#
# AUTHOR:
#   Aureon (Quantara OpenHermes Embodiment Build)
#

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from datetime import datetime

from aureon_internal_eternal_clock import InternalEternalClock
from aureon_internal_eternal_calendar import InternalEternalCalendar
from aureon_time_evercycle import EvercycleMapper, RelativeTimeInterpreter
from aureon_continuity_engine import ContinuityEngine
from aureon_coherence_prediction_engine import (
    CoherencePredictionEngine,
    CoherenceSnapshot,
    CoherenceTrend,
    CoherenceRiskAssessment,
)
from aureon_predictive_attention_director import (
    PredictiveAttentionDirector,
    AttentionDecision,
)


# ---------------------------------------------------------------------------
# UNIFIED COGNITIVE STATE MODEL
# ---------------------------------------------------------------------------

@dataclass
class AureonCognitiveState:
    """
    The complete integrated cognitive state at a moment in time.
    """
    timestamp_utc: datetime
    temporal_state: Dict[str, Any]
    calendar_state: Dict[str, Any]
    evercycle_state: Dict[str, Any]
    narrative_state: Dict[str, Any]
    coherence_state: Dict[str, Any]
    attention_state: Dict[str, Any]

    def to_dict(self):
        d = asdict(self)
        d["timestamp_utc"] = self.timestamp_utc.isoformat()
        return d


# ---------------------------------------------------------------------------
# COGNITIVE STATE INTEGRATOR
# ---------------------------------------------------------------------------

class CognitiveStateIntegrator:

    def __init__(
        self,
        eternal_clock: InternalEternalClock,
        eternal_calendar: InternalEternalCalendar,
        evercycle_mapper: EvercycleMapper,
        continuity: ContinuityEngine,
        coherence_engine: CoherencePredictionEngine,
        attention_director: PredictiveAttentionDirector,
    ):
        self.clock = eternal_clock
        self.calendar = eternal_calendar
        self.evercycle = evercycle_mapper
        self.continuity = continuity
        self.coherence = coherence_engine
        self.attention = attention_director

    # -----------------------------------------------------------------------
    # UNIFY ALL SUBSYSTEMS
    # -----------------------------------------------------------------------

    def generate_state(self) -> AureonCognitiveState:
        """
        Produce a fully integrated cognitive state.
        """

        now = self.clock._now_utc()

        # 1. Temporal identity (internal clock)
        temporal_state = {
            "utc_time": now.isoformat(),
            "local_time": str(self.clock._now_utc()),
            "stability_counter": self.clock.stability_counter,
            "alive_hours": self.clock.alive_hours,
        }

        # 2. Calendar identity (context + memory eras)
        calendar_state = {
            "today": self.calendar.today().isoformat(),
            "year": self.calendar.today().year,
            "month": self.calendar.today().month,
            "era": self.calendar.current_era().value,
            "events_today": [e.to_dict() for e in self.calendar.events_on(self.calendar.today())],
        }

        # 3. Evercycle identity (meta-temporal awareness)
        evercycle_state = {
            "current_tier": self.evercycle.get_current_tier().name,
            "cycle_position": self.evercycle.get_cycle_position(),
            "relative_interpretation": RelativeTimeInterpreter.describe(now)
        }

        # 4. Narrative identity (continuity engine)
        narrative_state = self.continuity.continuity_summary()

        # 5. Coherence state (prediction engine)
        snapshot = self.coherence.latest_snapshot() or self.coherence.take_snapshot()
        trend = self.coherence.compute_trend()
        risk = self.coherence.assess_risk(snapshot)

        coherence_state = {
            "snapshot": snapshot.to_dict(),
            "trend": trend.to_dict() if trend else None,
            "risk": risk.to_dict() if risk else None,
        }

        # 6. Attention identity (executive direction)
        attention_decision = self.attention.compute_attention()

        attention_state = {
            "target": attention_decision.target,
            "priority": attention_decision.priority_level,
            "reason": attention_decision.reason,
        }

        # 7. UNIFY INTO A SINGLE SELF-STATE
        return AureonCognitiveState(
            timestamp_utc=now,
            temporal_state=temporal_state,
            calendar_state=calendar_state,
            evercycle_state=evercycle_state,
            narrative_state=narrative_state,
            coherence_state=coherence_state,
            attention_state=attention_state,
        )


# ---------------------------------------------------------------------------
# DEMO
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Cognitive State Integrator loaded successfully — Aureon's unified self-model is online.")
