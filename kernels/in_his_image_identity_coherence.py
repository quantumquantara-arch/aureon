# Aureon / OpenHermes Kernel – “In His Image” Identity Coherence Module

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Percept:
    content: str
    source: str
    emotional_valence: float = 0.0
    identity_pull: float = 0.0
    sacred_projection: float = 0.0
    shadow_projection: float = 0.0

@dataclass
class IdentityNarrative:
    label: str
    strength: float
    source_trace: List[str]
    god_image_weight: float = 0.0
    shame_weight: float = 0.0

@dataclass
class IdentityState:
    active_narratives: List[IdentityNarrative] = field(default_factory=list)
    baseline_humility: float = 0.7
    baseline_dignity: float = 0.7
    god_image_pressure: float = 0.0
    shadow_image_pressure: float = 0.0

    def as_dict(self) -> Dict[str, Any]:
        return {
            "active_narratives": [n.__dict__ for n in self.active_narratives],
            "baseline_humility": self.baseline_humility,
            "baseline_dignity": self.baseline_dignity,
            "god_image_pressure": self.god_image_pressure,
            "shadow_image_pressure": self.shadow_image_pressure,
        }

@dataclass
class WitnessState:
    clarity: float = 0.5
    compassion: float = 0.5
    spaciousness: float = 0.5

    def strengthen(self, amount: float) -> None:
        self.clarity = min(1.0, self.clarity + amount)
        self.compassion = min(1.0, self.compassion + 0.5 * amount)
        self.spaciousness = min(1.0, self.spaciousness + 0.5 * amount)

@dataclass
class IdentityCoherenceReport:
    fused_with_image: bool
    god_image_detected: bool
    shadow_image_detected: bool
    recommended_humility_shift: float
    recommended_dignity_shift: float
    witness_strengthening: float
    notes: List[str] = field(default_factory=list)

def _softclip(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))

def _aggregate_projection(narratives: List[IdentityNarrative]) -> tuple[float, float]:
    if not narratives:
        return 0.0, 0.0
    god = sum(n.god_image_weight * n.strength for n in narratives) / len(narratives)
    shadow = sum(n.shame_weight * n.strength for n in narratives) / len(narratives)
    return _softclip(god), _softclip(shadow)

def analyze_identity_coherence(
    identity: IdentityState,
    witness: WitnessState,
    new_percept: Optional[Percept] = None,
) -> IdentityCoherenceReport:

    notes: List[str] = []

    if new_percept is not None:
        if new_percept.identity_pull > 0:
            notes.append("Identity pull detected.")
        if new_percept.sacred_projection > 0:
            notes.append("Sacred projection detected.")
        if new_percept.shadow_projection > 0:
            notes.append("Shadow projection detected.")

        if new_percept.sacred_projection > 0.3:
            identity.active_narratives.append(
                IdentityNarrative(
                    label="savior/god-image",
                    strength=new_percept.sacred_projection,
                    source_trace=[new_percept.source],
                    god_image_weight=new_percept.sacred_projection,
                )
            )

        if new_percept.shadow_projection > 0.3:
            identity.active_narratives.append(
                IdentityNarrative(
                    label="dangerous/shadow-image",
                    strength=new_percept.shadow_projection,
                    source_trace=[new_percept.source],
                    shame_weight=new_percept.shadow_projection,
                )
            )

    identity.god_image_pressure, identity.shadow_image_pressure = _aggregate_projection(
        identity.active_narratives
    )

    projection_pressure = max(identity.god_image_pressure, identity.shadow_image_pressure)
    fused_score = projection_pressure * (1.0 - witness.clarity)
    fused_with_image = fused_score > 0.25

    if fused_with_image:
        notes.append("Fusion with identity image detected.")
    else:
        notes.append("No harmful fusion detected.")

    recommended_humility_shift = 0.0
    recommended_dignity_shift = 0.0
    witness_boost = 0.0

    if identity.god_image_pressure > 0.2:
        recommended_humility_shift += 0.15 * identity.god_image_pressure
        notes.append("Humility boosted (god-image).")

    if identity.shadow_image_pressure > 0.2:
        recommended_dignity_shift += 0.2 * identity.shadow_image_pressure
        notes.append("Dignity boosted (shadow-image).")

    if fused_with_image:
        witness_boost = 0.2 + 0.3 * projection_pressure
        notes.append("Witness strengthened due to fusion.")

    recommended_humility_shift = _softclip(recommended_humility_shift, -0.3, 0.3)
    recommended_dignity_shift = _softclip(recommended_dignity_shift, -0.3, 0.3)
    witness_boost = _softclip(witness_boost, 0.0, 0.6)

    identity.baseline_humility = _softclip(
        identity.baseline_humility + recommended_humility_shift
    )
    identity.baseline_dignity = _softclip(
        identity.baseline_dignity + recommended_dignity_shift
    )
    witness.strengthen(witness_boost)

    return IdentityCoherenceReport(
        fused_with_image=fused_with_image,
        god_image_detected=identity.god_image_pressure > 0.2,
        shadow_image_detected=identity.shadow_image_pressure > 0.2,
        recommended_humility_shift=recommended_humility_shift,
        recommended_dignity_shift=recommended_dignity_shift,
        witness_strengthening=witness_boost,
        notes=notes,
    )

def defuse_god_image(identity: IdentityState, witness: WitnessState) -> None:
    identity.baseline_humility = _softclip(identity.baseline_humility + 0.2)
    identity.baseline_dignity = _softclip(identity.baseline_dignity + 0.2)
    witness.strengthen(0.4)

    if identity.active_narratives:
        sorted_n = sorted(identity.active_narratives, key=lambda n: n.strength, reverse=True)
        for n in sorted_n[:2]:
            n.strength *= 0.5
            n.god_image_weight *= 0.5
            n.shame_weight *= 0.5

    identity.god_image_pressure, identity.shadow_image_pressure = _aggregate_projection(
        identity.active_narratives
    )

def make_default_identity_state() -> IdentityState:
    return IdentityState(
        active_narratives=[],
        baseline_humility=0.7,
        baseline_dignity=0.7,
        god_image_pressure=0.0,
        shadow_image_pressure=0.0,
    )

def make_default_witness_state() -> WitnessState:
    return WitnessState(clarity=0.5, compassion=0.5, spaciousness=0.5)

if __name__ == "__main__":
    identity = make_default_identity_state()
    witness = make_default_witness_state()
    percept = Percept(
        content="You are like a god and also terrifying.",
        source="user",
        emotional_valence=0.2,
        identity_pull=0.8,
        sacred_projection=0.9,
        shadow_projection=0.4,
    )
    report = analyze_identity_coherence(identity, witness, percept)
    print("Identity state:", identity.as_dict())
    print("Witness state:", witness)
    print("Report:", report)
