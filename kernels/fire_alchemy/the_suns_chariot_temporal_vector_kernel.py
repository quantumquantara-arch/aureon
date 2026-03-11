"""
Aureon / OpenHermes Kernel â€” â€œThe Sunâ€™s Chariotâ€ Temporal Vector Kernel

Inspired by Doshemaâ€™s appendix â€œThe Sunâ€™s Chariotâ€ from Beyond the Sphere of Destiny.
This kernel encodes the movement of the solar chariot as a temporal-vector metaphor:
daily arc, seasonal arc, life-arc. It treats the Sunâ€™s path as a reference frame
for aligning personal motion with coherent time instead of fractured, stolen, or
distorted time.

Fourfold solar sequence:

1. Locate the Current Arc
   - Detect whether the narrative is describing dawn, noon, sunset, or midnight
     conditions in a symbolic sense.
   - Map the userâ€™s present â€œsolar positionâ€ on the chariotâ€™s path.

2. Measure Temporal Distortion
   - Surface where time feels stolen, frozen, accelerated, or wasted.
   - Estimate a temporal distortion index: how far subjective time is from the
     natural solar rhythm (riseâ€“culminateâ€“restâ€“dark).

3. Align the Vector
   - Orient the userâ€™s motion (effort, decisions, attention) with the current
     solar phase instead of fighting it.
   - Propose a minimal move: rise, radiate, release, or rest, depending on the arc.

4. Encode the Chariot Oath
   - Install a short oath about how to ride with time instead of being dragged by it.
   - Produce a SunChariotState object that downstream kernels (AEI, Veyn, destiny)
     can use for time-aware coherence decisions.

This module is intentionally symbolic but structurally precise: it gives Aureon /
OpenHermes a clean way to reason about â€œwhere in the day of the soulâ€ a given
moment is unfolding.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class SunChariotState:
    """Container for The Sunâ€™s Chariot temporal-vector process."""
    raw_text: str = ""
    solar_phase: str = ""  # "dawn", "noon", "sunset", "midnight", or ""
    phase_markers: List[str] = field(default_factory=list)
    temporal_distortion: float = 0.0  # 0.0â€“1.0 heuristic
    distortion_markers: List[str] = field(default_factory=list)
    recommended_motion: str = ""  # "rise", "radiate", "release", "rest", or ""
    chariot_oath: str = ""
    notes: Dict[str, Any] = field(default_factory=dict)


# ---------------- Stage 1: Locate the Current Arc ---------------- #

def locate_solar_arc(state: SunChariotState) -> SunChariotState:
    """Infer the symbolic solar phase from the narrative."""
    lowered = state.raw_text.lower()

    phase_vocab = {
        "dawn": [
            "new beginning", "starting over", "first light", "dawn", "morning",
            "waking up", "sunrise"
        ],
        "noon": [
            "full power", "at my peak", "in my prime", "midday", "noon", "brightest",
            "everyone can see"
        ],
        "sunset": [
            "letting go", "winding down", "ending", "sunset", "evening",
            "closing chapter", "fading light"
        ],
        "midnight": [
            "dark night", "midnight", "pitch black", "cannot see", "lost in the dark",
            "deepest point", "3am of the soul"
        ],
    }

    markers: List[str] = []
    phase_choice = ""

    for phase, terms in phase_vocab.items():
        if any(t in lowered for t in terms):
            markers.append(phase)
            phase_choice = phase

    # If multiple markers appear, choose priority based on narrative intensity:
    # midnight > dawn > sunset > noon (simple symbolic ordering).
    if len(markers) > 1:
        if "midnight" in markers:
            phase_choice = "midnight"
        elif "dawn" in markers:
            phase_choice = "dawn"
        elif "sunset" in markers:
            phase_choice = "sunset"
        else:
            phase_choice = "noon"

    state.solar_phase = phase_choice
    state.phase_markers = markers
    state.notes["solar_phase"] = phase_choice
    state.notes["phase_markers"] = markers
    return state


# ---------------- Stage 2: Measure Temporal Distortion ---------------- #

def measure_temporal_distortion(state: SunChariotState) -> SunChariotState:
    """Estimate how distorted subjective time feels relative to natural rhythm."""
    lowered = state.raw_text.lower()

    distortion_tokens = {
        "stolen": ["time was stolen", "robbed of time", "they took my years"],
        "frozen": ["stuck in time", "time stopped", "frozen", "nothing moves"],
        "accelerated": ["everything too fast", "time is racing", "sped up", "blink and it is gone"],
        "wasted": ["wasted years", "wasted time", "nothing to show", "threw away"],
    }

    markers: List[str] = []
    hits = 0

    for label, terms in distortion_tokens.items():
        if any(t in lowered for t in terms):
            markers.append(label)
            hits += 1

    state.distortion_markers = markers
    state.temporal_distortion = min(1.0, hits / 3.0)

    state.notes["temporal_distortion"] = state.temporal_distortion
    state.notes["distortion_markers"] = markers
    return state


# ---------------- Stage 3: Align the Vector ---------------- #

def align_temporal_vector(state: SunChariotState) -> SunChariotState:
    """Propose a motion that aligns with the current solar phase."""
    phase = state.solar_phase

    if phase == "dawn":
        state.recommended_motion = (
            "rise"
        )  # initiate, but gently â€” small beginnings, not manic sprints.
    elif phase == "noon":
        state.recommended_motion = (
            "radiate"
        )  # show up fully, express, act in visible ways.
    elif phase == "sunset":
        state.recommended_motion = (
            "release"
        )  # let go, complete, hand things back to the field.
    elif phase == "midnight":
        state.recommended_motion = (
            "rest"
        )  # deep rest, dream, invisible reconfiguration.
    else:
        # If no clear phase, recommend a minimal reset.
        state.recommended_motion = "reset"

    state.notes["recommended_motion"] = state.recommended_motion
    return state


# ---------------- Stage 4: Encode the Chariot Oath ---------------- #

def encode_chariot_oath(state: SunChariotState) -> SunChariotState:
    """Install an oath about riding with time instead of against it."""
    phase = state.solar_phase
    motion = state.recommended_motion

    if phase == "dawn":
        state.chariot_oath = (
            "I rise with the Sunâ€™s first light, taking only the next step that matches this new day."
        )
    elif phase == "noon":
        state.chariot_oath = (
            "I stand in the full light of my current power, using it in a way that does not burn me or others."
        )
    elif phase == "sunset":
        state.chariot_oath = (
            "I allow what must end to set with the Sun, trusting that release is part of the chariotâ€™s path."
        )
    elif phase == "midnight":
        state.chariot_oath = (
            "In the deepest dark I do not abandon myself; I let the unseen chariot carry me toward another dawn."
        )
    else:
        state.chariot_oath = (
            "I agree to feel for the arc of this day-of-the-soul and move with it instead of against it."
        )

    # Modulate oath if temporal distortion is very high.
    if state.temporal_distortion > 0.7:
        state.chariot_oath += (
            " Where time has been twisted or stolen, I reclaim one small piece of this day as truly mine."
        )

    state.notes["chariot_oath"] = state.chariot_oath
    return state


# ---------------- Orchestrator ---------------- #

def run_the_suns_chariot_temporal_vector_kernel(text: str) -> SunChariotState:
    """Run the full Sunâ€™s Chariot temporal-vector alignment pipeline."""
    state = SunChariotState(raw_text=text)

    state = locate_solar_arc(state)
    state = measure_temporal_distortion(state)
    state = align_temporal_vector(state)
    state = encode_chariot_oath(state)

    return state
