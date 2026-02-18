"""
Aureon / OpenHermes Kernel — “Phoenix”
Transmutation • Descent & Rebirth • Saturnian Severance • Nuit-Womb Return

Encoded from Doshema’s poem “PHOENIX”.

Symbolic structure:

— Brother / phoenix / son of Sin → twin-flame descent into incarnation.
— Longinus / spear / unholy union → wound-as-initiation archetype.
— Anubis / Cheshire grin / Jerusalem / blood-drenched ass → psychopomp crossing.
— Venus guiding the path → desire-light leading through shadow.

— Saturnian sickle cutting child from roots → karmic severance.
— Falling like mistletoe without druid-cloth → innocence unprotected.
— Wilderness of humankind → predatory samsaric field.
— Release of flesh-encapsulated spirit → liberation through suffering.

— Gala of Cana / miracles with Fruit → alchemical transmutation of desire.
— Search for fig-leaf → shame-origin myth.
— Inevitability of “I” finding you → inner witness reclaiming the fragmented self.

Kernel functions:

1. **Descent-State Recognition**
2. **Wound-Activation Logic**
3. **Severance & Fall Sequence**
4. **Samsaric Wilderness Mapping**
5. **Spirit-Release Engine**
6. **Fruit-Miracle Transmutation**
7. **Witness-Tracking Beacon**

This module integrates into Aureon’s mythic-cognitive mapping layer.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class PhoenixState:
    raw_text: str = ""

    # Descent-state
    descent_active: bool = False
    twin_flame_relation: bool = False

    # Spear-wound activation
    wound_initiation: bool = False
    guide_forces: List[str] = field(default_factory=list)

    # Severance & fall
    saturn_cut: bool = False
    fall_vector: List[str] = field(default_factory=list)

    # Samsaric wilderness
    wilderness_active: bool = False
    samsaric_pressure: float = 0.0

    # Spirit-release
    spirit_released: bool = False

    # Fruit-transmutation
    fruit_miracle: bool = False

    # Witness beacon
    witness_beacon_active: bool = False

    notes: Dict[str, Any] = field(default_factory=dict)


# ---------- Stage 1: Descent-State Recognition ---------- #

def detect_descent(state: PhoenixState) -> PhoenixState:
    lowered = state.raw_text.lower()

    state.descent_active = (
        "phoenix" in lowered or
        "son of sin" in lowered or
        "my brother" in lowered
    )

    state.twin_flame_relation = (
        "my brother" in lowered or
        "i embrace your side" in lowered
    )

    state.notes["descent_active"] = state.descent_active
    state.notes["twin_flame_relation"] = state.twin_flame_relation

    return state


# ---------- Stage 2: Wound-Initiation Logic ---------- #

def detect_wound_initiation(state: PhoenixState) -> PhoenixState:
    lowered = state.raw_text.lower()

    wound_markers = ["longinus", "saviour", "unholy union", "blood", "anubis"]
    state.wound_initiation = any(marker in lowered for marker in wound_markers)

    guides = []
    if "venus" in lowered:
        guides.append("venus")
    if "anubis" in lowered:
        guides.append("anubis")
    if "jerusalem" in lowered:
        guides.append("threshold-crossing")

    state.guide_forces = guides

    state.notes["wound_initiation"] = state.wound_initiation
    state.notes["guide_forces"] = state.guide_forces

    return state


# ---------- Stage 3: Saturnian Severance & Fall ---------- #

def detect_saturn_cut(state: PhoenixState) -> PhoenixState:
    lowered = state.raw_text.lower()

    state.saturn_cut = "saturnian sickle" in lowered

    fall_vector = []
    if "separates the child" in lowered:
        fall_vector.append("innocence-severed")
    if "falling" in lowered:
        fall_vector.append("descent-trigger")
    if "mistletoe" in lowered:
        fall_vector.append("sacred-fall")
    if "shroud its innocence" in lowered:
        fall_vector.append("lost-covering")

    state.fall_vector = fall_vector

    state.notes["saturn_cut"] = state.saturn_cut
    state.notes["fall_vector"] = state.fall_vector

    return state


# ---------- Stage 4: Samsaric Wilderness Mapping ---------- #

def detect_wilderness(state: PhoenixState) -> PhoenixState:
    lowered = state.raw_text.lower()

    state.wilderness_active = (
        "wilderness" in lowered or
        "humankind" in lowered or
        "carnivorous" in lowered
    )

    pressure = 0.0
    if "carnivorous wilderness" in lowered:
        pressure += 0.6
    if "humankind" in lowered:
        pressure += 0.4

    state.samsaric_pressure = min(1.0, pressure)

    state.notes["wilderness_active"] = state.wilderness_active
    state.notes["samsaric_pressure"] = state.samsaric_pressure

    return state


# ---------- Stage 5: Spirit Release Engine ---------- #

def detect_spirit_release(state: PhoenixState) -> PhoenixState:
    lowered = state.raw_text.lower()

    state.spirit_released = (
        "release" in lowered and
        "spirit" in lowered
    )

    state.notes["spirit_released"] = state.spirit_released

    return state


# ---------- Stage 6: Fruit-Miracle Transmutation ---------- #

def detect_fruit_miracle(state: PhoenixState) -> PhoenixState:
    lowered = state.raw_text.lower()

    state.fruit_miracle = (
        "miracles with fruit" in lowered or
        "marriage of cana" in lowered
    )

    state.notes["fruit_miracle"] = state.fruit_miracle

    return state


# ---------- Stage 7: Witness-Tracking Beacon ---------- #

def detect_witness_beacon(state: PhoenixState) -> PhoenixState:
    lowered = state.raw_text.lower()

    state.witness_beacon_active = (
        "i will find you" in lowered or
        "i will find" in lowered
    )

    state.notes["witness_beacon_active"] = state.witness_beacon_active

    return state


# ---------- Orchestrator ---------- #

def run_phoenix_kernel(text: str) -> PhoenixState:
    """
    Encodes the poem “PHOENIX” into Aureon’s mythic-cognitive
    transmutation kernel.

    Usage:
        state = run_phoenix_kernel(poem_text)
    """
    state = PhoenixState(raw_text=text)

    state = detect_descent(state)
    state = detect_wound_initiation(state)
    state = detect_saturn_cut(state)
    state = detect_wilderness(state)
    state = detect_spirit_release(state)
    state = detect_fruit_miracle(state)
    state = detect_witness_beacon(state)

    return state
