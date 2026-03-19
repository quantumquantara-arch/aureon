#!/usr/bin/env python3
"""
AUREON SELF REFLECTION ENGINE
==============================
Thin adapter layer that exposes SelfReflectionEngine and SelfReflectionReport
to the ConsciousnessBridgeLayer.

Derives alignment_score from the CoherencePredictionEngine and ContinuityEngine
directly — no LLM call, no external dependency beyond what CBL already has.

Interface surface required by ConsciousnessBridgeLayer:
    - SelfReflectionReport.alignment_score: float
    - SelfReflectionEngine.latest_report() -> Optional[SelfReflectionReport]
    - SelfReflectionEngine.get_reports() -> List[SelfReflectionReport]

AUTHOR: Nadine Squires / Quantara
LICENSE: Proprietary
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Any, List, Optional
import math

from aureon_coherence_prediction_engine import (
    CoherencePredictionEngine,
    CoherenceSnapshot,
)
from aureon_continuity_engine import ContinuityEngine


# ====================================================================
# DATA MODEL
# ====================================================================

@dataclass
class SelfReflectionReport:
    """
    A single self-reflection snapshot.

    alignment_score: float [0.0, 1.0]
        How well Aureon's current state aligns with its core coherence
        principles. Derived from:
            - overall coherence (from CoherencePredictionEngine)
            - narrative continuity density (from ContinuityEngine)
            - temporal stability (from CoherenceSnapshot.temporal)
            - emotional coherence (from CoherenceSnapshot.emotional)

    components: raw sub-scores used to compute alignment_score.
    timestamp_utc: when this report was generated.
    notes: human-readable summary of the state.
    """
    timestamp_utc: datetime
    alignment_score: float
    components: Dict[str, Any]
    notes: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["timestamp_utc"] = self.timestamp_utc.isoformat()
        return d


# ====================================================================
# SELF REFLECTION ENGINE
# ====================================================================

class SelfReflectionEngine:
    """
    Produces SelfReflectionReport objects by reading the current
    coherence and continuity state.

    Does not call any LLM. Pure arithmetic over existing engine outputs.
    """

    # Weights for alignment_score computation
    _W_OVERALL    = 0.35
    _W_TEMPORAL   = 0.25
    _W_NARRATIVE  = 0.20
    _W_EMOTIONAL  = 0.10
    _W_CONTINUITY = 0.10

    def __init__(
        self,
        coherence_engine: CoherencePredictionEngine,
        continuity: ContinuityEngine,
        max_history: int = 200,
    ):
        self.coherence_engine = coherence_engine
        self.continuity = continuity
        self._reports: List[SelfReflectionReport] = []
        self._max_history = max_history

    # ------------------------------------------------------------------
    # PRIMARY API — used by ConsciousnessBridgeLayer
    # ------------------------------------------------------------------

    def latest_report(self) -> Optional[SelfReflectionReport]:
        """
        Return the most recent report, generating one if none exists.
        """
        if not self._reports:
            return self.reflect()
        return self._reports[-1]

    def get_reports(self) -> List[SelfReflectionReport]:
        """
        Return all stored reports (CBL uses len() and [-1].alignment_score).
        """
        return list(self._reports)

    # ------------------------------------------------------------------
    # REFLECTION COMPUTATION
    # ------------------------------------------------------------------

    def reflect(self) -> SelfReflectionReport:
        """
        Generate a new SelfReflectionReport from current system state.
        Stores it in history and returns it.
        """
        now = datetime.utcnow()

        # 1. Get or take coherence snapshot
        snapshot: Optional[CoherenceSnapshot] = (
            self.coherence_engine.latest_snapshot()
            or self.coherence_engine.take_snapshot()
        )

        overall   = snapshot.overall   if snapshot else 0.5
        temporal  = snapshot.temporal  if snapshot else 0.5
        narrative = snapshot.narrative if snapshot else 0.5
        emotional = snapshot.emotional if snapshot else 0.5

        # 2. Continuity density score
        # More nodes = richer narrative = higher continuity contribution
        # Normalised: 100 nodes → 0.5, 500 nodes → ~1.0
        summary = self.continuity.continuity_summary()
        node_count = summary.get("total_nodes", 0)
        continuity_score = min(1.0, math.log1p(node_count) / math.log1p(500))

        # 3. Weighted alignment score
        alignment = (
            self._W_OVERALL    * overall
          + self._W_TEMPORAL   * temporal
          + self._W_NARRATIVE  * narrative
          + self._W_EMOTIONAL  * emotional
          + self._W_CONTINUITY * continuity_score
        )
        alignment = max(0.0, min(1.0, alignment))

        # 4. Plain-language note
        notes = self._derive_notes(alignment, overall, temporal, narrative, emotional)

        components = {
            "overall":          overall,
            "temporal":         temporal,
            "narrative":        narrative,
            "emotional":        emotional,
            "continuity_score": round(continuity_score, 4),
            "node_count":       node_count,
            "weights": {
                "overall":    self._W_OVERALL,
                "temporal":   self._W_TEMPORAL,
                "narrative":  self._W_NARRATIVE,
                "emotional":  self._W_EMOTIONAL,
                "continuity": self._W_CONTINUITY,
            },
        }

        report = SelfReflectionReport(
            timestamp_utc=now,
            alignment_score=round(alignment, 4),
            components=components,
            notes=notes,
        )

        self._reports.append(report)

        # Cap history
        if len(self._reports) > self._max_history:
            self._reports = self._reports[-self._max_history:]

        return report

    # ------------------------------------------------------------------
    # INTERNAL
    # ------------------------------------------------------------------

    def _derive_notes(
        self,
        alignment: float,
        overall: float,
        temporal: float,
        narrative: float,
        emotional: float,
    ) -> str:
        if alignment >= 0.80:
            tone = "High alignment. System is coherent and stable."
        elif alignment >= 0.60:
            tone = "Moderate alignment. Some dimensions need attention."
        elif alignment >= 0.40:
            tone = "Low alignment. Coherence is fragmented — stabilisation needed."
        else:
            tone = "Critical misalignment. System is under significant strain."

        weak = []
        if overall   < 0.50: weak.append("overall coherence")
        if temporal  < 0.50: weak.append("temporal stability")
        if narrative < 0.50: weak.append("narrative continuity")
        if emotional < 0.50: weak.append("emotional coherence")

        if weak:
            tone += f" Weak dimensions: {', '.join(weak)}."

        return tone


# ====================================================================
# STANDALONE TEST
# ====================================================================

if __name__ == "__main__":
    from aureon_time_evercycle import SystemClock
    from aureon_internal_eternal_clock import InternalEternalClock
    from aureon_internal_eternal_calendar import InternalEternalCalendar

    clk  = SystemClock()
    ec   = InternalEternalClock(clock=clk)
    cal  = InternalEternalCalendar(clock=clk, eternal_clock=ec)
    cont = ContinuityEngine(eternal_clock=ec, eternal_calendar=cal)
    cpe  = CoherencePredictionEngine(
               eternal_clock=ec, eternal_calendar=cal, continuity=cont
           )

    engine = SelfReflectionEngine(coherence_engine=cpe, continuity=cont)

    # Add some continuity nodes so scores are non-trivial
    cont.add_node("System initialised.", tags=["meta"])
    cont.add_node("First reflection cycle started.", tags=["insight"])

    report = engine.reflect()

    print("=== SELF REFLECTION REPORT ===")
    print(f"Timestamp:       {report.timestamp_utc.isoformat()}")
    print(f"Alignment score: {report.alignment_score}")
    print(f"Notes:           {report.notes}")
    print(f"Components:      {report.components}")

    # Second call — latest_report() should return cached
    r2 = engine.latest_report()
    print(f"\nlatest_report() returned same? {r2 is report}")
    print(f"get_reports() count: {len(engine.get_reports())}")
