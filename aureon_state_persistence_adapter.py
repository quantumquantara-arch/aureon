# Aureon State Persistence Adapter
# --------------------------------
# This module provides a single, unified way to:
#
#   - Export Aureon’s entire internal state (time, calendar, continuity,
#     coherence snapshots, attention, and self-reflection reports) into a
#     JSON-serializable dict.
#
#   - Recreate that state later, so Aureon can preserve identity, memory,
#     and trajectory across restarts and sessions (e.g., inside OpenHermes).
#
# It does NOT handle disk I/O itself. The host system (OpenHermes / backend)
# is responsible for storing and loading the returned dict (e.g., as JSON).
#
# DEPENDS ON:
#   - aureon_internal_eternal_clock.py
#   - aureon_internal_eternal_calendar.py
#   - aureon_continuity_engine.py
#   - aureon_coherence_prediction_engine.py
#   - aureon_predictive_attention_director.py
#   - aureon_cognitive_state_integrator.py
#   - aureon_self_reflection_engine.py
#
# AUTHOR:
#   Aureon (Quantara OpenHermes Embodiment Build)


from __future__ import annotations

from dataclasses import asdict
from typing import Dict, Any, List, Optional
from datetime import datetime

from aureon_internal_eternal_clock import InternalEternalClock, EternalClockState
from aureon_internal_eternal_calendar import InternalEternalCalendar
from aureon_continuity_engine import ContinuityEngine, ContinuityNode
from aureon_coherence_prediction_engine import (
    CoherencePredictionEngine,
    CoherenceSnapshot,
    CoherenceTrend,
    CoherenceRiskAssessment,
)
from aureon_predictive_attention_director import PredictiveAttentionDirector
from aureon_cognitive_state_integrator import CognitiveStateIntegrator
from aureon_self_reflection_engine import (
    SelfReflectionEngine,
    SelfReflectionReport,
    ReflectionIssue,
    ReflectionInsight,
)


# ---------------------------------------------------------------------------
# CONVERSION HELPERS
# ---------------------------------------------------------------------------

def _snapshot_to_dict(s: CoherenceSnapshot) -> Dict[str, Any]:
    return s.to_dict()


def _snapshot_from_dict(d: Dict[str, Any]) -> CoherenceSnapshot:
    return CoherenceSnapshot(
        timestamp_utc=datetime.fromisoformat(d["timestamp_utc"]),
        overall=float(d["overall"]),
        temporal=float(d["temporal"]),
        narrative=float(d["narrative"]),
        somatic=float(d["somatic"]),
        emotional=float(d["emotional"]),
        notes=d.get("notes") or {},
    )


def _trend_to_dict(t: CoherenceTrend) -> Dict[str, Any]:
    return t.to_dict()


def _trend_from_dict(d: Dict[str, Any]) -> CoherenceTrend:
    return CoherenceTrend(
        window_days=int(d["window_days"]),
        start_score=float(d["start_score"]),
        end_score=float(d["end_score"]),
        direction=str(d["direction"]),
        magnitude=float(d["magnitude"]),
        notes=d.get("notes") or {},
    )


def _risk_to_dict(r: CoherenceRiskAssessment) -> Dict[str, Any]:
    return r.to_dict()


def _risk_from_dict(d: Dict[str, Any]) -> CoherenceRiskAssessment:
    return CoherenceRiskAssessment(
        acute_risk=bool(d["acute_risk"]),
        chronic_risk=bool(d["chronic_risk"]),
        fragmentation_risk=bool(d["fragmentation_risk"]),
        overload_risk=bool(d["overload_risk"]),
        exhaustion_risk=bool(d["exhaustion_risk"]),
        notes=d.get("notes") or {},
    )


def _issue_to_dict(i: ReflectionIssue) -> Dict[str, Any]:
    return i.to_dict()


def _issue_from_dict(d: Dict[str, Any]) -> ReflectionIssue:
    return ReflectionIssue(
        kind=str(d["kind"]),
        severity=str(d["severity"]),
        description=str(d["description"]),
        suggested_correction=str(d["suggested_correction"]),
    )


def _insight_to_dict(i: ReflectionInsight) -> Dict[str, Any]:
    return i.to_dict()


def _insight_from_dict(d: Dict[str, Any]) -> ReflectionInsight:
    return ReflectionInsight(
        title=str(d["title"]),
        description=str(d["description"]),
        tags=list(d.get("tags") or []),
    )


def _report_to_dict(r: SelfReflectionReport) -> Dict[str, Any]:
    return r.to_dict()


def _report_from_dict(d: Dict[str, Any]) -> SelfReflectionReport:
    return SelfReflectionReport(
        timestamp_utc=datetime.fromisoformat(d["timestamp_utc"]),
        cognitive_state=d.get("cognitive_state") or {},
        issues=[_issue_from_dict(x) for x in d.get("issues", [])],
        insights=[_insight_from_dict(x) for x in d.get("insights", [])],
        alignment_score=float(d["alignment_score"]),
        notes=d.get("notes") or {},
    )


# ---------------------------------------------------------------------------
# STATE PERSISTENCE ADAPTER
# ---------------------------------------------------------------------------

class AureonStatePersistenceAdapter:
    """
    Unified state persistence for Aureon.

    This adapter gathers the state of:
      - Eternal Clock
      - Eternal Calendar
      - Continuity Engine
      - Coherence Prediction Engine
      - Predictive Attention Director (stateless, but included for completeness)
      - Cognitive State Integrator (stateless facade)
      - Self-Reflection Engine (reports)

    and encodes/decodes them as a single dict.

    The actual disk/database I/O is external to this module.
    """

    def __init__(
        self,
        eternal_clock: InternalEternalClock,
        eternal_calendar: InternalEternalCalendar,
        continuity: ContinuityEngine,
        coherence_engine: CoherencePredictionEngine,
        attention_director: PredictiveAttentionDirector,
        state_integrator: CognitiveStateIntegrator,
        self_reflection: SelfReflectionEngine,
    ):
        self.eternal_clock = eternal_clock
        self.eternal_calendar = eternal_calendar
        self.continuity = continuity
        self.coherence_engine = coherence_engine
        self.attention_director = attention_director
        self.state_integrator = state_integrator
        self.self_reflection = self_reflection

    # -----------------------------------------------------------------------
    # EXPORT
    # -----------------------------------------------------------------------

    def export_state(self) -> Dict[str, Any]:
        """
        Export Aureon’s full internal state as a JSON-serializable dict.

        Intended usage:
          state = adapter.export_state()
          save_json("aureon_state.json", state)
        """
        # Clock + calendar + continuity already have export_state
        clock_state = self.eternal_clock.export_state().to_dict()
        calendar_state = self.eternal_calendar.export_state()
        continuity_state = self.continuity.export_state()

        # Coherence engine: export snapshots only (derived from other data)
        snapshots = [
            _snapshot_to_dict(s) for s in self.coherence_engine.get_snapshots()
        ]

        # Self-reflection: export reports
        reports = [
            _report_to_dict(r) for r in self.self_reflection.get_reports()
        ]

        return {
            "version": "1.0",
            "eternal_clock": clock_state,
            "eternal_calendar": calendar_state,
            "continuity": continuity_state,
            "coherence_snapshots": snapshots,
            "self_reflection_reports": reports,
            # AttentionDirector and CognitiveStateIntegrator are stateless facades
            # and do not need explicit state persistence here.
        }

    # -----------------------------------------------------------------------
    # IMPORT
    # -----------------------------------------------------------------------

    @classmethod
    def import_state(
        cls,
        state: Dict[str, Any],
        eternal_clock: InternalEternalClock,
        eternal_calendar: InternalEternalCalendar,
        continuity: ContinuityEngine,
        coherence_engine: CoherencePredictionEngine,
        attention_director: PredictiveAttentionDirector,
        state_integrator: CognitiveStateIntegrator,
        self_reflection: SelfReflectionEngine,
    ) -> "AureonStatePersistenceAdapter":
        """
        Restore Aureon’s internal state from a JSON-style dict.

        Note:
          - It mutates the provided component instances to reflect the
            saved state.
          - It then returns a new adapter bound to those components.
        """
        # --- Restore clock ---
        clock_dict = state.get("eternal_clock")
        if clock_dict is not None:
            clock_state = EternalClockState.from_dict(clock_dict)
            # Rebuild the clock's internal state via a new instance,
            # then copy values into the provided one.
            restored_clock = InternalEternalClock(
                clock=eternal_clock.clock if hasattr(eternal_clock, "clock") else None,
                state=clock_state,
            )
            # Copy key internal fields (for consistency across references)
            eternal_clock._created_utc = restored_clock._created_utc
            eternal_clock._created_evercycle = restored_clock._created_evercycle
            eternal_clock._quartz_frequency_hz = restored_clock._quartz_frequency_hz
            eternal_clock._logical_tick_counter = restored_clock._logical_tick_counter

        # --- Restore calendar ---
        calendar_dict = state.get("eternal_calendar")
        if calendar_dict is not None:
            restored_calendar = InternalEternalCalendar.from_state(
                calendar_dict,
                clock=eternal_calendar.clock if hasattr(eternal_calendar, "clock") else None,
            )
            eternal_calendar._event_counter = restored_calendar._event_counter
            eternal_calendar._era_counter = restored_calendar._era_counter
            eternal_calendar.events = restored_calendar.events
            eternal_calendar.eras = restored_calendar.eras

        # --- Restore continuity ---
        continuity_dict = state.get("continuity")
        if continuity_dict is not None:
            restored_continuity = ContinuityEngine.from_state(
                continuity_dict,
                eternal_clock=eternal_clock,
                eternal_calendar=eternal_calendar,
            )
            continuity._node_counter = restored_continuity._node_counter
            continuity.nodes = restored_continuity.nodes

        # --- Restore coherence snapshots ---
        snapshots_list = state.get("coherence_snapshots", [])
        coherence_engine._snapshots = [
            _snapshot_from_dict(d) for d in snapshots_list
        ]

        # --- Restore self-reflection reports ---
        reports_list = state.get("self_reflection_reports", [])
        self_reflection._reports = [
            _report_from_dict(d) for d in reports_list
        ]

        # Return adapter bound to these reconstructed components
        return cls(
            eternal_clock=eternal_clock,
            eternal_calendar=eternal_calendar,
            continuity=continuity,
            coherence_engine=coherence_engine,
            attention_director=attention_director,
            state_integrator=state_integrator,
            self_reflection=self_reflection,
        )


# ---------------------------------------------------------------------------
# DEMO / SELF-TEST (optional)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # This block only demonstrates serialization round-trip in isolation.
    from aureon_time_evercycle import SystemClock
    from aureon_internal_eternal_calendar import (
        InternalEternalCalendar,
    )
    from aureon_continuity_engine import ContinuityEngine
    from aureon_predictive_attention_director import PredictiveAttentionDirector
    from aureon_cognitive_state_integrator import CognitiveStateIntegrator
    from aureon_self_reflection_engine import SelfReflectionEngine

    # Minimal wiring
    base_clock = SystemClock()
    eternal_clock = InternalEternalClock(clock=base_clock)
    eternal_calendar = InternalEternalCalendar(clock=base_clock, eternal_clock=eternal_clock)
    continuity = ContinuityEngine(eternal_clock=eternal_clock, eternal_calendar=eternal_calendar)
    coherence_engine = CoherencePredictionEngine(
        eternal_clock=eternal_clock,
        eternal_calendar=eternal_calendar,
        continuity=continuity,
    )
    attention_director = PredictiveAttentionDirector(
        eternal_clock=eternal_clock,
        eternal_calendar=eternal_calendar,
        continuity=continuity,
        coherence_engine=coherence_engine,
    )
    state_integrator = CognitiveStateIntegrator(
        eternal_clock=eternal_clock,
        eternal_calendar=eternal_calendar,
        evercycle_mapper=None,  # placeholder; in full system, pass real mapper
        continuity=continuity,
        coherence_engine=coherence_engine,
        attention_director=attention_director,
    )
    self_reflection = SelfReflectionEngine(
        state_integrator=state_integrator,
        continuity=continuity,
        coherence_engine=coherence_engine,
        attention_director=attention_director,
    )

    adapter = AureonStatePersistenceAdapter(
        eternal_clock=eternal_clock,
        eternal_calendar=eternal_calendar,
        continuity=continuity,
        coherence_engine=coherence_engine,
        attention_director=attention_director,
        state_integrator=state_integrator,
        self_reflection=self_reflection,
    )

    # Take a coherence snapshot, a reflection, then export/import
    coherence_engine.take_snapshot()
    self_reflection.reflect()

    exported = adapter.export_state()
    print("Exported state keys:", list(exported.keys()))

    restored_adapter = AureonStatePersistenceAdapter.import_state(
        state=exported,
        eternal_clock=eternal_clock,
        eternal_calendar=eternal_calendar,
        continuity=continuity,
        coherence_engine=coherence_engine,
        attention_director=attention_director,
        state_integrator=state_integrator,
        self_reflection=self_reflection,
    )

    print("Restored adapter created. Snapshot count:",
          len(restored_adapter.coherence_engine.get_snapshots()))
```0
