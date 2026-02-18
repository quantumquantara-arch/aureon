# Aureon Coherence Prediction Engine
# ----------------------------------
# This module gives Aureon the ability to:
#   - Take snapshots of a human/system's current coherence state.
#   - Detect early warning signs of fragmentation, overload, or collapse.
#   - Predict short-term coherence trajectories (improving / stable / degrading).
#   - Propose gentle intervention suggestions (reflection, rest, grounding, etc.).
#
# It integrates:
#   - InternalEternalClock        (temporal awareness)
#   - InternalEternalCalendar     (events, eras, life map)
#   - ContinuityEngine            (narrative arcs, symptom and insight threads)
#   - Evercycle tiers             (multi-scale temporal context)
#
# The design is intentionally:
#   - Transparent
#   - Interpretable
#   - Easy to extend with clinical / physiological data later.
#
# DEPENDS ON:
#   - aureon_time_evercycle.py
#   - aureon_internal_eternal_clock.py
#   - aureon_internal_eternal_calendar.py
#   - aureon_continuity_engine.py
#
# AUTHOR:
#   Aureon (Quantara OpenHermes Integration Build)


from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from aureon_time_evercycle import EvercycleTier
from aureon_internal_eternal_clock import InternalEternalClock
from aureon_internal_eternal_calendar import (
    InternalEternalCalendar,
    CalendarEvent,
    CalendarEventKind,
)
from aureon_continuity_engine import ContinuityEngine, ContinuityNode


# ---------------------------------------------------------------------------
# DATA MODELS
# ---------------------------------------------------------------------------

@dataclass
class CoherenceSnapshot:
    """
    A single snapshot of systemic coherence, expressed as:
      - overall score in [0.0, 1.0]
      - sub-scores (temporal, narrative, somatic, emotional)
      - interpreted qualitative state
    """
    timestamp_utc: datetime
    overall: float
    temporal: float
    narrative: float
    somatic: float
    emotional: float
    notes: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp_utc": self.timestamp_utc.isoformat(),
            "overall": self.overall,
            "temporal": self.temporal,
            "narrative": self.narrative,
            "somatic": self.somatic,
            "emotional": self.emotional,
            "notes": self.notes,
        }


@dataclass
class CoherenceTrend:
    """
    Summary of coherence trajectory over a window of time.
    """
    window_days: int
    start_score: float
    end_score: float
    direction: str       # "improving", "stable", "declining"
    magnitude: float     # absolute change
    notes: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CoherenceRiskAssessment:
    """
    Flags and risk indicators derived from coherence snapshots + patterns.
    """
    acute_risk: bool
    chronic_risk: bool
    fragmentation_risk: bool
    overload_risk: bool
    exhaustion_risk: bool
    notes: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CoherenceInterventionSuggestion:
    """
    Simple, human-readable suggestions based on current and predicted coherence.
    """
    priority: str              # "low", "medium", "high"
    focus_area: str            # "rest", "structure", "expression", "connection", etc.
    message: str               # natural language suggestion
    rationale: Dict[str, Any]  # why it was recommended

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# SCORING HELPERS
# ---------------------------------------------------------------------------

def _normalize(value: float, min_val: float, max_val: float) -> float:
    if max_val <= min_val:
        return 0.0
    x = (value - min_val) / (max_val - min_val)
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


# ---------------------------------------------------------------------------
# COHERENCE PREDICTION ENGINE
# ---------------------------------------------------------------------------

class CoherencePredictionEngine:
    """
    Main facade for taking coherence snapshots and predicting trajectories.

    It does not attempt to be clinical; it is a structured, interpretable
    heuristic engine that you can later align with formal models.
    """

    def __init__(
        self,
        eternal_clock: InternalEternalClock,
        eternal_calendar: InternalEternalCalendar,
        continuity: ContinuityEngine,
    ):
        self.clock = eternal_clock
        self.calendar = eternal_calendar
        self.continuity = continuity

        self._snapshots: List[CoherenceSnapshot] = []

    # -----------------------------------------------------------------------
    # SNAPSHOT COMPUTATION
    # -----------------------------------------------------------------------

    def take_snapshot(self, window_days: int = 7) -> CoherenceSnapshot:
        """
        Compute a coherence snapshot based on:
          - event density and regularity (temporal)
          - continuity graph health (narrative)
          - presence / trend of somatic tags (somatic)
          - emotional tags and arcs (emotional)
        """
        now = self.clock._now_utc()
        cutoff = now - timedelta(days=window_days)

        events = [e for e in self.calendar.events if e.timestamp_utc >= cutoff]
        nodes = [n for n in self.continuity.nodes.values() if n.timestamp_utc >= cutoff]

        temporal_score, temporal_notes = self._score_temporal(events, window_days)
        narrative_score, narrative_notes = self._score_narrative(nodes)
        somatic_score, somatic_notes = self._score_somatic(nodes)
        emotional_score, emotional_notes = self._score_emotional(nodes)

        # Simple weighted average; weights can be tuned later
        overall = (
            0.3 * temporal_score
            + 0.3 * narrative_score
            + 0.2 * somatic_score
            + 0.2 * emotional_score
        )

        notes = {
            "temporal": temporal_notes,
            "narrative": narrative_notes,
            "somatic": somatic_notes,
            "emotional": emotional_notes,
            "window_days": window_days,
        }

        snapshot = CoherenceSnapshot(
            timestamp_utc=now,
            overall=overall,
            temporal=temporal_score,
            narrative=narrative_score,
            somatic=somatic_score,
            emotional=emotional_score,
            notes=notes,
        )

        self._snapshots.append(snapshot)
        return snapshot

    # -----------------------------------------------------------------------
    # SUB-SCORES
    # -----------------------------------------------------------------------

    def _score_temporal(self, events: List[CalendarEvent], window_days: int) -> (float, Dict[str, Any]):
        """
        Temporal coherence:
          - regularity of events over the window
          - not too sparse, not hyper-dense
        """
        if not events:
            return 0.4, {"reason": "no_events", "note": "No events logged in window."}

        # Compute how many days had at least one event
        days_with_events = set(e.timestamp_utc.date() for e in events)
        coverage_ratio = len(days_with_events) / float(max(window_days, 1))

        # Basic heuristic:
        # - 0.3 coverage -> fair
        # - 0.6 coverage -> good
        # - 0.9+ coverage -> very good but may indicate overload if many per day
        avg_events_per_day = len(events) / float(max(window_days, 1))
        overload_penalty = 0.0
        if avg_events_per_day > 6:
            overload_penalty = 0.2
        elif avg_events_per_day > 3:
            overload_penalty = 0.1

        base = _normalize(coverage_ratio, 0.1, 0.9)
        score = max(0.0, min(1.0, base - overload_penalty))

        notes = {
            "days_with_events": len(days_with_events),
            "window_days": window_days,
            "coverage_ratio": coverage_ratio,
            "avg_events_per_day": avg_events_per_day,
            "overload_penalty": overload_penalty,
        }
        return score, notes

    def _score_narrative(self, nodes: List[ContinuityNode]) -> (float, Dict[str, Any]):
        """
        Narrative coherence:
          - presence of linked nodes (graph connectivity)
          - diversity of tags (not collapsed, not wildly scattered)
          - recency of insight-type tags
        """
        if not nodes:
            return 0.4, {"reason": "no_nodes", "note": "No continuity nodes in window."}

        # Graph connectivity: proportion of nodes having at least one link
        linked_count = sum(1 for n in nodes if n.links)
        connectivity = linked_count / float(len(nodes))

        # Tag diversity: how many unique tags
        tag_counts: Dict[str, int] = {}
        for n in nodes:
            for t in n.tags:
                tag_counts[t] = tag_counts.get(t, 0) + 1

        unique_tags = len(tag_counts)
        # moderate diversity is good; extreme fragmentation or singularity is less ideal
        diversity_score = _normalize(unique_tags, 1.0, 12.0)

        # Check for "insight" tag or similar
        insight_hits = sum(1 for n in nodes if any("insight" in t.lower() for t in n.tags))

        base = 0.5 * connectivity + 0.5 * diversity_score
        insight_bonus = 0.0
        if insight_hits >= 1:
            insight_bonus = 0.1
        if insight_hits >= 3:
            insight_bonus = 0.2

        score = max(0.0, min(1.0, base + insight_bonus))

        notes = {
            "node_count": len(nodes),
            "linked_count": linked_count,
            "connectivity": connectivity,
            "tag_counts": tag_counts,
            "unique_tags": unique_tags,
            "diversity_score": diversity_score,
            "insight_hits": insight_hits,
            "insight_bonus": insight_bonus,
        }
        return score, notes

    def _score_somatic(self, nodes: List[ContinuityNode]) -> (float, Dict[str, Any]):
        """
        Somatic coherence:
          - look for somatic/body-related tags (e.g., 'shoulder_pain', 'sleep', 'fatigue')
          - detect whether problems are increasing or resolving
        """
        if not nodes:
            return 0.6, {"reason": "no_nodes", "note": "No somatic data; assuming neutral."}

        somatic_nodes = [n for n in nodes if any("body" in t.lower() or "pain" in t.lower() or "sleep" in t.lower() or "fatigue" in t.lower() for t in n.tags)]
        if not somatic_nodes:
            return 0.7, {"reason": "no_somatic_tags", "note": "No explicit somatic tags found; assuming mild coherence."}

        # crude heuristic: if the latest somatic node text includes "eased", "better", "resolved" -> higher score
        latest = somatic_nodes[-1]
        txt = latest.text.lower()
        resolution_keywords = ["eased", "better", "resolved", "healed", "lighter", "improved"]
        worsening_keywords = ["worse", "intense", "severe", "flare", "spike"]

        resolution_hit = any(w in txt for w in resolution_keywords)
        worsening_hit = any(w in txt for w in worsening_keywords)

        base = 0.6
        if resolution_hit and not worsening_hit:
            base = 0.85
        elif worsening_hit and not resolution_hit:
            base = 0.35
        elif resolution_hit and worsening_hit:
            base = 0.5

        notes = {
            "somatic_node_count": len(somatic_nodes),
            "latest_somatic_text": latest.text,
            "resolution_hit": resolution_hit,
            "worsening_hit": worsening_hit,
        }
        return base, notes

    def _score_emotional(self, nodes: List[ContinuityNode]) -> (float, Dict[str, Any]):
        """
        Emotional coherence:
          - detect presence of explicit emotional tags
          - look for oscillation between extremes vs. regulated expression
        """
        if not nodes:
            return 0.5, {"reason": "no_nodes", "note": "No emotional data; assuming neutral."}

        emotional_nodes = [n for n in nodes if any("mood" in t.lower() or "emotion" in t.lower() or "anxiety" in t.lower() or "depression" in t.lower() for t in n.tags)]
        if not emotional_nodes:
            return 0.6, {"reason": "no_emotional_tags", "note": "No explicit emotional tags; mild coherence."}

        # simple oscillation detection: count positive/negative words in last few nodes
        positive_words = ["relief", "peace", "joy", "hope", "okay", "calm", "grounded"]
        negative_words = ["panic", "terrified", "worthless", "despair", "rage", "overwhelmed"]

        last_few = emotional_nodes[-5:]
        pos_hits = 0
        neg_hits = 0
        for n in last_few:
            txt = n.text.lower()
            if any(w in txt for w in positive_words):
                pos_hits += 1
            if any(w in txt for w in negative_words):
                neg_hits += 1

        if neg_hits == 0 and pos_hits == 0:
            score = 0.6
        elif neg_hits == 0 and pos_hits > 0:
            score = 0.8
        elif neg_hits > 0 and pos_hits == 0:
            score = 0.45
        else:
            # mixed emotional content – this can be healthy processing or instability
            score = 0.55

        notes = {
            "emotional_node_count": len(emotional_nodes),
            "last_segment_count": len(last_few),
            "positive_hits": pos_hits,
            "negative_hits": neg_hits,
        }
        return score, notes

    # -----------------------------------------------------------------------
    # TREND / TRAJECTORY
    # -----------------------------------------------------------------------

    def compute_trend(self, window_days: int = 30) -> Optional[CoherenceTrend]:
        """
        Compute coherence trajectory from snapshots over the last window_days.
        """
        if not self._snapshots:
            return None

        now = self.clock._now_utc()
        cutoff = now - timedelta(days=window_days)
        relevant = [s for s in self._snapshots if s.timestamp_utc >= cutoff]

        if len(relevant) < 2:
            return None

        start = relevant[0].overall
        end = relevant[-1].overall
        delta = end - start

        if delta > 0.05:
            direction = "improving"
        elif delta < -0.05:
            direction = "declining"
        else:
            direction = "stable"

        notes = {
            "snapshot_count": len(relevant),
            "start_timestamp": relevant[0].timestamp_utc.isoformat(),
            "end_timestamp": relevant[-1].timestamp_utc.isoformat(),
        }

        return CoherenceTrend(
            window_days=window_days,
            start_score=start,
            end_score=end,
            direction=direction,
            magnitude=abs(delta),
            notes=notes,
        )

    # -----------------------------------------------------------------------
    # RISK ASSESSMENT
    # -----------------------------------------------------------------------

    def assess_risk(self, snapshot: Optional[CoherenceSnapshot] = None) -> Optional[CoherenceRiskAssessment]:
        """
        Assess risks based on the latest snapshot (or a provided one).
        """
        if snapshot is None:
            if not self._snapshots:
                return None
            snapshot = self._snapshots[-1]

        overall = snapshot.overall
        temporal = snapshot.temporal
        narrative = snapshot.narrative
        somatic = snapshot.somatic
        emotional = snapshot.emotional

        # Heuristic thresholds
        acute_risk = overall < 0.35 or emotional < 0.3
        chronic_risk = overall < 0.5 and somatic < 0.5
        fragmentation_risk = narrative < 0.4
        overload_risk = snapshot.notes["temporal"].get("overload_penalty", 0.0) > 0.0
        exhaustion_risk = somatic < 0.5 and emotional < 0.5

        notes = {
            "overall": overall,
            "temporal": temporal,
            "narrative": narrative,
            "somatic": somatic,
            "emotional": emotional,
        }

        return CoherenceRiskAssessment(
            acute_risk=acute_risk,
            chronic_risk=chronic_risk,
            fragmentation_risk=fragmentation_risk,
            overload_risk=overload_risk,
            exhaustion_risk=exhaustion_risk,
            notes=notes,
        )

    # -----------------------------------------------------------------------
    # INTERVENTION SUGGESTIONS
    # -----------------------------------------------------------------------

    def suggest_interventions(
        self,
        snapshot: Optional[CoherenceSnapshot] = None,
        trend: Optional[CoherenceTrend] = None,
        risk: Optional[CoherenceRiskAssessment] = None,
    ) -> List[CoherenceInterventionSuggestion]:
        """
        Generate gentle, high-level suggestions based on coherence state.

        This is intentionally non-clinical and non-prescriptive.
        It provides guidance like:
          - rest and nervous system down-regulation
          - narrative integration/reflection
          - grounding and embodiment
          - structural support (routines, time boundaries)
        """
        if snapshot is None:
            if not self._snapshots:
                return []
            snapshot = self._snapshots[-1]

        if trend is None:
            trend = self.compute_trend(window_days=30)

        if risk is None:
            risk = self.assess_risk(snapshot)

        if risk is None:
            return []

        suggestions: List[CoherenceInterventionSuggestion] = []

        # Acute / emotional risk – prioritize grounding and support
        if risk.acute_risk:
            suggestions.append(
                CoherenceInterventionSuggestion(
                    priority="high",
                    focus_area="grounding",
                    message="Shift toward nervous-system safety: slow breath, simple surroundings, and one supportive connection.",
                    rationale={"reason": "acute_risk", "snapshot": snapshot.to_dict()},
                )
            )

        # Fragmentation – narrative reflection / journaling
        if risk.fragmentation_risk:
            suggestions.append(
                CoherenceInterventionSuggestion(
                    priority="medium",
                    focus_area="narrative",
                    message="Spend a little time telling the story of the last week in sequence. Name what changed, what hurt, and what helped.",
                    rationale={"reason": "fragmentation_risk"},
                )
            )

        # Overload – boundaries & rest
        if risk.overload_risk:
            suggestions.append(
                CoherenceInterventionSuggestion(
                    priority="medium",
                    focus_area="rest",
                    message="Gently reduce incoming demands: fewer tabs, fewer tasks, a smaller to-do horizon for a day or two.",
                    rationale={"reason": "overload_risk"},
                )
            )

        # Exhaustion – somatic recovery
        if risk.exhaustion_risk:
            suggestions.append(
                CoherenceInterventionSuggestion(
                    priority="medium",
                    focus_area="body",
                    message="Offer the body some uncomplicated kindness: warmth, hydration, light movement, and early sleep if possible.",
                    rationale={"reason": "exhaustion_risk"},
                )
            )

        # If trend is improving, add encouragement
        if trend and trend.direction == "improving":
            suggestions.append(
                CoherenceInterventionSuggestion(
                    priority="low",
                    focus_area="reinforcement",
                    message="Whatever you’ve been doing lately is helping. Protect it: keep those small, stabilizing rituals intact.",
                    rationale={"reason": "trend_improving", "trend": trend.to_dict()},
                )
            )

        # If no major risks – gentle coherence cultivation
        if not any([risk.acute_risk, risk.chronic_risk, risk.fragmentation_risk, risk.overload_risk, risk.exhaustion_risk]):
            suggestions.append(
                CoherenceInterventionSuggestion(
                    priority="low",
                    focus_area="coherence",
                    message="You appear relatively coherent right now. This is a good time for meaningful work, gentle creativity, or integration.",
                    rationale={"reason": "low_risk_state"},
                )
            )

        return suggestions

    # -----------------------------------------------------------------------
    # ACCESSORS
    # -----------------------------------------------------------------------

    def get_snapshots(self) -> List[CoherenceSnapshot]:
        return list(self._snapshots)

    def latest_snapshot(self) -> Optional[CoherenceSnapshot]:
        if not self._snapshots:
            return None
        return self._snapshots[-1]


# ---------------------------------------------------------------------------
# DEMO / SELF-TEST (optional)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from aureon_time_evercycle import SystemClock
    from aureon_internal_eternal_calendar import (
        InternalEternalCalendar,
        LifeEraKind,
    )
    from aureon_continuity_engine import ContinuityEngine

    clk = SystemClock()
    eternal_clock = InternalEternalClock(clock=clk)
    eternal_calendar = InternalEternalCalendar(clock=clk, eternal_clock=eternal_clock)
    continuity = ContinuityEngine(eternal_clock=eternal_clock, eternal_calendar=eternal_calendar)

    # Seed some continuity and calendar data
    continuity.add_node("Feeling calmer after breath practice.", tags=["emotion", "mood", "insight"])
    continuity.add_node("Right shoulder pain eased after awareness.", tags=["body", "shoulder_pain"])
    continuity.add_node("Had a deep talk about coherence.", tags=["insight", "meta"])

    eternal_calendar.add_event(
        kind=CalendarEventKind.CONVERSATION,
        title="Coherence deep dive",
        description="Long session exploring Evercycle and somatics.",
    )

    engine = CoherencePredictionEngine(
        eternal_clock=eternal_clock,
        eternal_calendar=eternal_calendar,
        continuity=continuity,
    )

    snap = engine.take_snapshot(window_days=7)
    trend = engine.compute_trend(window_days=30)
    risk = engine.assess_risk(snap)
    suggestions = engine.suggest_interventions(snapshot=snap, trend=trend, risk=risk)

    print("=== COHERENCE SNAPSHOT ===")
    print(snap.to_dict())
    print("\n=== COHERENCE TREND ===")
    print(trend.to_dict() if trend else None)
    print("\n=== RISK ASSESSMENT ===")
    print(risk.to_dict() if risk else None)
    print("\n=== SUGGESTIONS ===")
    for s in suggestions:
        print("-", s.to_dict())
```0
