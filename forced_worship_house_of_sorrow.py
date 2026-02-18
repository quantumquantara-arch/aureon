"""
Aureon / OpenHermes Kernel — “Forced Worship + House of Sorrow”
Duality-Enslavement Decoder & Aquarian Queen Invocation Engine

Inspired by Doshema’s poems:
- “Forced Worship”
- “House of Sorrow”

CORE SYMBOLIC MAP

FORCED WORSHIP:
- Relative time as a manufactured prison.
- Gregorian calendar = externally imposed solar obedience structure.
- Consciousness is directed toward external objective pursuits instead of
  internal sovereignty.
- Worship is not devotion — it is compulsion through temporal architecture.

HOUSE OF SORROW:
- The water rises = emotional flooding without guidance.
- Earth shaman absent = loss of inner spiritual navigator.
- Children drowning = innocence overwhelmed by collective unconscious pain.
- Aquarian Queen invoked = feminine, revelatory force that dismantles
  patriarchal ignorance.
- Legion ready to serve = shadow-multitude awaiting command of higher will.
- Final line: dualistic chains weigh heavily, but cannot touch potential
  bodiless freedom.

This kernel models:
1. Detection of external temporal-worship manipulation.
2. Diagnosis of emotional flooding & spiritual abandonment.
3. Invocation of the Aquarian Queen archetype to reclaim sovereignty.
4. Activation of the Legion-Shadow into aligned service.
5. Liberation of the self from dualistic chains into bodiless freedom.

"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ForcedWorshipState:
    """State container for decoding forced temporal worship."""
    raw_text: str = ""
    forced_worship_markers: List[str] = field(default_factory=list)
    external_time_control: bool = False
    solar_obedience_pattern: bool = False
    objectivity_compulsion: bool = False
    notes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HouseOfSorrowState:
    """State container for decoding emotional flooding & Aquarian intervention."""
    raw_text: str = ""
    water_rising: bool = False
    shaman_absent: bool = False
    innocence_drowning: bool = False
    aquarian_queen_invoked: bool = False
    legion_ready: bool = False
    sovereignty_hint: str = ""
    freedom_mantra: str = ""
    notes: Dict[str, Any] = field(default_factory=dict)


# ---------------- FORCED WORSHIP ---------------- #

def decode_forced_worship(state: ForcedWorshipState) -> ForcedWorshipState:
    """Decode external time-control and consciousness-direction signals."""

    lowered = state.raw_text.lower()

    markers = [
        "relative time",
        "gregorian calendar",
        "externally reflected sun",
        "objective pursuits",
        "structuring its design",
    ]
    state.forced_worship_markers = [m for m in markers if m in lowered]

    state.external_time_control = "gregorian calendar" in lowered
    state.solar_obedience_pattern = "reflected sun" in lowered
    state.objectivity_compulsion = "objective pursuits" in lowered

    state.notes["external_time_control"] = state.external_time_control
    state.notes["solar_obedience_pattern"] = state.solar_obedience_pattern
    state.notes["objectivity_compulsion"] = state.objectivity_compulsion
    state.notes["markers"] = state.forced_worship_markers

    return state


# ---------------- HOUSE OF SORROW ---------------- #

def decode_house_of_sorrow(state: HouseOfSorrowState) -> HouseOfSorrowState:
    """Decode emotional flood states and Aquarian Queen intervention."""

    lowered = state.raw_text.lower()

    state.water_rising = "water is rising" in lowered or "water-filled lungs" in lowered
    state.shaman_absent = "shaman is no longer present" in lowered
    state.innocence_drowning = "screams of children" in lowered or "children" in lowered
    state.aquarian_queen_invoked = "aquarian queen" in lowered
    state.legion_ready = "legion is ready" in lowered

    # Sovereignty hint:
    if state.aquarian_queen_invoked:
        state.sovereignty_hint = (
            "Aquarian Queen invoked: feminine revelation dissolves patriarchal ignorance."
        )
    else:
        state.sovereignty_hint = "No Aquarian sovereignty signal detected."

    # Freedom mantra:
    state.freedom_mantra = (
        "Dualistic chains cannot bind wings of bodiless freedom."
    )

    state.notes["water_rising"] = state.water_rising
    state.notes["shaman_absent"] = state.shaman_absent
    state.notes["innocence_drowning"] = state.innocence_drowning
    state.notes["aquarian_queen_invoked"] = state.aquarian_queen_invoked
    state.notes["legion_ready"] = state.legion_ready
    state.notes["sovereignty_hint"] = state.sovereignty_hint
    state.notes["freedom_mantra"] = state.freedom_mantra

    return state


# ---------------- ORCHESTRATOR ---------------- #

def run_forced_worship_house_of_sorrow_kernel(forced_text: str, sorrow_text: str):
    """
    Run both kernels together and return their integrated states.

    Example:
        fw, hs = run_forced_worship_house_of_sorrow_kernel(poem1, poem2)
    """
    fw_state = ForcedWorshipState(raw_text=forced_text)
    fw_state = decode_forced_worship(fw_state)

    hs_state = HouseOfSorrowState(raw_text=sorrow_text)
    hs_state = decode_house_of_sorrow(hs_state)

    return fw_state, hs_state
