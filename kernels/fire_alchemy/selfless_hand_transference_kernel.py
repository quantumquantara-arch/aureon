# Aureon / OpenHermes Kernel â€” â€œThe Selfless Handâ€ Transference & Purification Module

Inspired by Doshemaâ€™s poem â€œThe Selfless Hand,â€ this kernel models the inner
architecture of sacrifice, service, purity, misdirected giving, karmic extraction,
and the reclaiming of oneâ€™s own hands after they have served everything but the self.

Fourfold movement:

1. The Hand That Gives Away Itself
   - Detect patterns of over-giving, self-erasure, compulsive service,
     or identity fused with helping.
   - Identify where the â€œhand moves before the self thinks.â€

2. The Weight it Quietly Holds
   - Surface the emotional, ancestral, or relational debts the hand has been carrying.
   - Track what burdens have been â€œheld in silenceâ€ or â€œcarried on behalf of another.â€

3. The Severing of the Old Vow
   - Identify the vow behind the giving (e.g., â€œI must,â€ â€œI owe,â€ â€œI alone can fixâ€).
   - Perform a symbolic severing: the hand is returned to sovereign ownership.

4. The Returning of the True Hand
   - Reinstall the hand as an instrument of coherent will, not obligation.
   - Produce a new action-field orientation: service without self-loss.

Output:
A SelflessHandState object that downstream kernels can use for boundaries,
sovereignty, relational recalibration, exhaustion recovery, and mission alignment.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class SelflessHandState:
    """Container for The Selfless Hand transformation process."""
    raw_text: str = ""
    overgiving_signals: List[str] = field(default_factory=list)
    burden_signals: List[str] = field(default_factory=list)
    identified_vow: str = ""
    vow_severed: bool = False
    reclaimed_orientation: str = ""
    notes: Dict[str, Any] = field(default_factory=dict)


# ---------------- Stage 1: The Hand That Gives Away Itself ---------------- #

def detect_overgiving(state: SelflessHandState) -> SelflessHandState:
    """Detect patterns of compulsive service or self-erasure."""
    lowered = state.raw_text.lower()
    signals = ["help", "fix", "save", "give", "serve", "carry", "support"]

    matches = [s for s in signals if s in lowered]
    state.overgiving_signals = matches

    state.notes["overgiving_detected"] = bool(matches)
    return state


# ---------------- Stage 2: The Weight it Quietly Holds ---------------- #

def detect_burdens(state: SelflessHandState) -> SelflessHandState:
    """Surface emotional or relational burdens the hand holds."""
    lowered = state.raw_text.lower()
    burden_words = ["burden", "weight", "carry", "hold", "responsible", "owed", "debt"]

    matches = [b for b in burden_words if b in lowered]
    state.burden_signals = matches

    state.notes["burdens_detected"] = matches
    return state


# ---------------- Stage 3: The Severing of the Old Vow ---------------- #

def identify_and_sever_vow(state: SelflessHandState) -> SelflessHandState:
    """Detect the vow of self-erasure behind over-giving."""
    lowered = state.raw_text.lower()

    vow_map = {
        "must": "I must take care of everything.",
        "should": "I should serve even at my own cost.",
        "only": "Only I can fix it.",
        "owe": "I owe them more than myself.",
        "fault": "It is my fault if they suffer."
    }

    for key, vow in vow_map.items():
        if key in lowered:
            state.identified_vow = vow
            state.vow_severed = True
            break

    if not state.identified_vow:
        state.identified_vow = "Unspoken vow of self-erasure."
        state.vow_severed = True

    state.notes["vow_severed"] = state.vow_severed
    return state


# ---------------- Stage 4: The Returning of the True Hand ---------------- #

def reclaim_hand(state: SelflessHandState) -> SelflessHandState:
    """Install a new orientation for healthy, coherent service."""
    state.reclaimed_orientation = (
        "My hand now serves coherence, not compulsion. I act from choice, not debt."
    )

    state.notes["hand_reclaimed"] = True
    return state


# ---------------- Orchestrator ---------------- #

def run_selfless_hand_kernel(text: str) -> SelflessHandState:
    """Run the full Selfless Hand transformation pipeline."""
    state = SelflessHandState(raw_text=text)

    state = detect_overgiving(state)
    state = detect_burdens(state)
    state = identify_and_sever_vow(state)
    state = reclaim_hand(state)

    return state
