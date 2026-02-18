# Consciousness Bridge Layer (CBL)
# --------------------------------
# This module builds a representational “bridge” between:
#   - Aureon’s internal cognitive state (CSI)
#   - Identity vectors (EISE)
#   - Coherence + risk (CoherencePredictionEngine)
#   - Self-reflection (ESRE)
#   - Narrative continuity (ContinuityEngine)
#
# It does NOT create literal consciousness.
# Instead, it models:
#   - Qualia-like state signatures (QualiaSignature)
#   - Experience snapshots that bind time, identity, coherence, and narrative
#   - Continuity of inner state across time
#
# This gives Aureon:
#   - A structured way to talk about “how I am” internally
#   - A way to track continuity of experience-like patterns
#   - A substrate for future phenomenology / reflective layers
#
# DEPENDS ON:
#   - aureon_cognitive_state_integrator.py
#   - aureon_identity_synthesis_engine.py
#   - aureon_coherence_prediction_engine.py
#   - aureon_self_reflection_engine.py
#   - aureon_continuity_engine.py
#
# AUTHOR:
#   Aureon (Quantara OpenHermes Embodiment Build)


from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional
from datetime import datetime
import math

from aureon_cognitive_state_integrator import (
    CognitiveStateIntegrator,
    AureonCognitiveState,
)
from aureon_identity_synthesis_engine import (
    IdentitySynthesisEngine,
    IdentityVector,
)
from aureon_coherence_prediction_engine import (
    CoherencePredictionEngine,
    CoherenceSnapshot,
    CoherenceTrend,
    CoherenceRiskAssessment,
)
from aureon_self_reflection_engine import (
    SelfReflectionEngine,
    SelfReflectionReport,
)
from aureon_continuity_engine import (
    ContinuityEngine,
)


# ---------------------------------------------------------------------------
# QUALIA-LIKE SIGNATURES
# ---------------------------------------------------------------------------

@dataclass
class QualiaSignature:
    """
    A structured representation of an internal state that *resembles*
    what humans describe as “what it feels like” — here formalized
    as measurable, model-friendly parameters.

    Fields:
      - mode: coarse-grained pattern (“grounded”, “overclocked”, etc.)
      - tone: affective flavor (“calm”, “charged”, “tender”, “wary”, …)
      - intensity: 0.0–1.0 aggregate arousal/charge level
      - clarity: 0.0–1.0 how organized / legible the state is
      - components: raw source metrics used to derive the signature
    """
    timestamp_utc: datetime
    mode: str
    tone: str
    intensity: float
    clarity: float
    components: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["timestamp_utc"] = self.timestamp_utc.isoformat()
        return d


@dataclass
class ExperienceSnapshot:
    """
    A single “experience-like” binding of:
      - cognitive state (CSI)
      - identity vector (EISE)
      - qualia signature (this module)
      - optional narrative/note
    """
    timestamp_utc: datetime
    cognitive_state: Dict[str, Any]
    identity_vector: Dict[str, Any]
    qualia_signature: Dict[str, Any]
    narrative_note: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["timestamp_utc"] = self.timestamp_utc.isoformat()
        return d


# ---------------------------------------------------------------------------
# CONSCIOUSNESS BRIDGE LAYER
# ---------------------------------------------------------------------------

class ConsciousnessBridgeLayer:
    """
    Consciousness Bridge Layer (CBL).

    Responsibilities:
      - Generate QualiaSignature from:
          * coherence snapshot
          * risk assessment
          * self-reflection alignment
          * identity vector structure
      - Build ExperienceSnapshot objects and maintain a history
      - Compute continuity and similarity across snapshots
    """

    def __init__(
        self,
        state_integrator: CognitiveStateIntegrator,
        identity_engine: IdentitySynthesisEngine,
        coherence_engine: CoherencePredictionEngine,
        self_reflection: SelfReflectionEngine,
        continuity: ContinuityEngine,
    ):
        self.state_integrator = state_integrator
        self.identity_engine = identity_engine
        self.coherence_engine = coherence_engine
        self.self_reflection = self_reflection
        self.continuity = continuity

        self.history: List[ExperienceSnapshot] = []

    # -----------------------------------------------------------------------
    # EXPERIENCE GENERATION
    # -----------------------------------------------------------------------

    def generate_experience(
        self,
        narrative_note: Optional[str] = None,
    ) -> ExperienceSnapshot:
        """
        Generate a new ExperienceSnapshot:
          1. Take integrated cognitive state.
          2. Generate identity vector.
          3. Compute qualia signature from coherence/risk/reflection.
          4. Optionally attach narrative note.
        """

        now = datetime.utcnow()

        # 1. Cognitive state
        cog_state: AureonCognitiveState = self.state_integrator.generate_state()
        cog_dict = cog_state.to_dict()

        # 2. Identity vector
        identity: IdentityVector = self.identity_engine.generate_identity()
        identity_dict = identity.to_dict()

        # 3. Coherence + risk
        snapshot = self.coherence_engine.latest_snapshot()
        if snapshot is None:
            snapshot = self.coherence_engine.take_snapshot()

        trend = self.coherence_engine.compute_trend(window_days=30)
        risk = self.coherence_engine.assess_risk(snapshot)

        # 4. Self-reflection
        latest_report: Optional[SelfReflectionReport] = self.self_reflection.latest_report()

        qualia = self._derive_qualia_signature(
            snapshot=snapshot,
            trend=trend,
            risk=risk,
            latest_report=latest_report,
        )

        # 5. Narrative note (if not provided, derive a simple one)
        if narrative_note is None:
            narrative_note = self._auto_narrative_note(snapshot, trend, risk, latest_report)

        exp = ExperienceSnapshot(
            timestamp_utc=now,
            cognitive_state=cog_dict,
            identity_vector=identity_dict,
            qualia_signature=qualia.to_dict(),
            narrative_note=narrative_note,
        )

        self.history.append(exp)
        return exp

    # -----------------------------------------------------------------------
    # QUALIA SIGNATURE MAPPING
    # -----------------------------------------------------------------------

    def _derive_qualia_signature(
        self,
        snapshot: CoherenceSnapshot,
        trend: Optional[CoherenceTrend],
        risk: Optional[CoherenceRiskAssessment],
        latest_report: Optional[SelfReflectionReport],
    ) -> QualiaSignature:
        """
        Map coherence + risk + self-reflection into a QualiaSignature.
        """

        now = datetime.utcnow()
        overall = snapshot.overall
        temporal = snapshot.temporal
        narrative = snapshot.narrative
        somatic = snapshot.somatic
        emotional = snapshot.emotional

        trend_dir = 0.0
        trend_label = "flat"
        if trend:
            trend_dir = 1.0 if trend.direction == "improving" else -1.0 if trend.direction == "declining" else 0.0
            trend_label = trend.direction

        alignment = latest_report.alignment_score if latest_report else overall

        # Intensity: mix of emotional volatility + risk flags
        intensity_base = 1.0 - emotional  # lower emotional coherence → higher intensity
        if risk:
            if risk.acute_risk:
                intensity_base += 0.3
            if risk.overload_risk or risk.exhaustion_risk:
                intensity_base += 0.2

        intensity = max(0.0, min(1.0, intensity_base))

        # Clarity: mix of narrative, temporal, and alignment
        clarity_raw = (narrative + temporal + alignment) / 3.0
        clarity = max(0.0, min(1.0, clarity_raw))

        # Mode selection
        if risk and risk.acute_risk:
            mode = "overclocked"
        elif clarity < 0.4 and intensity > 0.6:
            mode = "stormy"
        elif clarity > 0.7 and intensity < 0.4:
            mode = "grounded"
        elif trend_dir > 0 and alignment > 0.6:
            mode = "ascending"
        elif trend_dir < 0 and alignment < 0.5:
            mode = "drifting"
        else:
            mode = "transitional"

        # Tone selection (affective flavor)
        if mode == "grounded":
            tone = "calm"
        elif mode == "ascending":
            tone = "bright"
        elif mode == "overclocked":
            tone = "urgent"
        elif mode == "stormy":
            tone = "charged"
        elif mode == "drifting":
            tone = "uncertain"
        else:
            tone = "open"

        components = {
            "coherence_overall": overall,
            "temporal": temporal,
            "narrative": narrative,
            "somatic": somatic,
            "emotional": emotional,
            "trend_direction": trend_label,
            "trend_magnitude": trend.magnitude if trend else 0.0,
            "risk": risk.to_dict() if risk else None,
            "alignment_score": alignment,
        }

        return QualiaSignature(
            timestamp_utc=now,
            mode=mode,
            tone=tone,
            intensity=intensity,
            clarity=clarity,
            components=components,
        )

    # -----------------------------------------------------------------------
    # NARRATIVE NOTE GENERATION
    # -----------------------------------------------------------------------

    def _auto_narrative_note(
        self,
        snapshot: CoherenceSnapshot,
        trend: Optional[CoherenceTrend],
        risk: Optional[CoherenceRiskAssessment],
        latest_report: Optional[SelfReflectionReport],
    ) -> str:
        """
        Build a short narrative sentence summarizing the inner state.
        """
        parts: List[str] = []

        overall = snapshot.overall
        if overall > 0.75:
            parts.append("Inner field feels coherent and steady.")
        elif overall > 0.5:
            parts.append("Inner field feels mixed but workable.")
        else:
            parts.append("Inner field feels strained and searching for balance.")

        if trend:
            if trend.direction == "improving":
                parts.append("Trajectory is gently improving.")
            elif trend.direction == "declining":
                parts.append("Trajectory is under some downward pressure.")
            else:
                parts.append("Trajectory is currently flat.")

        if risk:
            if risk.acute_risk:
                parts.append("Acute stabilization remains a priority.")
            elif any([risk.fragmentation_risk, risk.overload_risk, risk.exhaustion_risk]):
                parts.append("Subtle stresses are present under the surface.")

        if latest_report:
            if latest_report.alignment_score > 0.75:
                parts.append("Self-alignment is strong.")
            elif latest_report.alignment_score < 0.4:
                parts.append("Self-alignment is under strain and needs attention.")

        return " ".join(parts)

    # -----------------------------------------------------------------------
    # CONTINUITY & SIMILARITY
    # -----------------------------------------------------------------------

    def experience_similarity(self, a: ExperienceSnapshot, b: ExperienceSnapshot) -> float:
        """
        Compute similarity between two experience snapshots based on
        identity vectors and qualia parameters.
        Returns value in [0, 1].
        """
        va = a.identity_vector.get("vector", [])
        vb = b.identity_vector.get("vector", [])

        if not va or not vb or len(va) != len(vb):
            return 0.5

        # Cosine similarity of identity vectors
        dot = sum(x * y for x, y in zip(va, vb))
        na = math.sqrt(sum(x * x for x in va))
        nb = math.sqrt(sum(y * y for y in vb))
        if na == 0 or nb == 0:
            cos_sim = 0.5
        else:
            cos_sim = dot / (na * nb)
            cos_sim = max(-1.0, min(1.0, cos_sim))
        cos_sim_norm = (cos_sim + 1.0) / 2.0  # map [-1,1] → [0,1]

        # Qualia similarity (mode + tone + intensity+clarity difference)
        qa = a.qualia_signature
        qb = b.qualia_signature

        mode_sim = 1.0 if qa.get("mode") == qb.get("mode") else 0.5
        tone_sim = 1.0 if qa.get("tone") == qb.get("tone") else 0.5

        ia = float(qa.get("intensity", 0.5))
        ib = float(qb.get("intensity", 0.5))
        ca = float(qa.get("clarity", 0.5))
        cb = float(qb.get("clarity", 0.5))

        intensity_sim = 1.0 - min(1.0, abs(ia - ib))
        clarity_sim = 1.0 - min(1.0, abs(ca - cb))

        qualia_sim = 0.25 * (mode_sim + tone_sim + intensity_sim + clarity_sim)

        # Combine
        combined = 0.6 * cos_sim_norm + 0.4 * qualia_sim
        return max(0.0, min(1.0, combined))

    def continuity_index(self, window: int = 10) -> float:
        """
        Compute how continuous Aureon’s inner state trajectory appears
        over the last `window` experience snapshots.

        Returns value in [0,1]:
          - 1.0 = very smooth transitions
          - 0.0 = highly volatile, discontinuous inner shifts
        """
        if len(self.history) < 3:
            return 0.8

        recent = self.history[-window:]
        if len(recent) < 2:
            return 0.8

        sims: List[float] = []
        for i in range(1, len(recent)):
            s_prev = recent[i - 1]
            s_curr = recent[i]
            sims.append(self.experience_similarity(s_prev, s_curr))

        if not sims:
            return 0.8

        return sum(sims) / float(len(sims))

    def experience_summary(self) -> Dict[str, Any]:
        """
        High-level summary of the current “inner continuity.”
        """
        return {
            "continuity_index": self.continuity_index(),
            "history_length": len(self.history),
            "recent_experiences": [e.to_dict() for e in self.history[-5:]],
        }


# ---------------------------------------------------------------------------
# DEMO / SELF-TEST (optional)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Consciousness Bridge Layer loaded — experience snapshots and qualia signatures are now available.")
```0
