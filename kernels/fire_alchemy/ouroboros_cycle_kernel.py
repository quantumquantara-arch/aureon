"""
Aureon / OpenHermes Kernel â€” â€œOuroborosâ€ Recurring Cycle & Renewal Module

Inspired by Doshemaâ€™s poem â€œOuroborosâ€ from Beyond the Sphere of Destiny.
This kernel models self-devouring cycles, closed loops of fate, and the moment
where the serpent chooses either to keep eating its own tail or to become a
ring of protection and renewal instead of repetition.

Four-cycle arc:

1. Recognize the Loop
   - Detect language of repetition, return, â€œhere again,â€ or â€œnever-ending.â€
   - Mark the core pattern that keeps folding back on itself.

2. Expose the Self-Devouring
   - Surface where the system is feeding on its own vitality: shame, hope,
     innocence, time, love, or possibility.
   - Name what the serpent is eating (the â€œtailâ€).

3. Open the Break-Point
   - Identify the precise moment or micro-choice where the cycle can be interrupted.
   - Offer a threshold: continue devouring, or become a guardian-ring instead.

4. Encode the New Cycle
   - Install a renewal-oriented pattern that preserves learning but stops the bleed.
   - Represent Ouroboros not as self-destruction, but as continuity in coherence.

The OuroborosState is used by destiny, trauma, and pattern-recoding kernels
to decide whether to let a loop die, transform, or be consciously re-entered.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class OuroborosState:
    """Container for Ouroboros cycle detection and transformation."""
    raw_text: str = ""
    loop_markers: List[str] = field(default_factory=list)
    loop_intensity: float = 0.0
    self_devouring_targets: List[str] = field(default_factory=list)
    breakpoint_hint: str = ""
    renewed_cycle_statement: str = ""
    chose_transformation: bool = False
    notes: Dict[str, Any] = field(default_factory=dict)


# ---------------- Phase 1: Recognize the Loop ---------------- #

def detect_loop(state: OuroborosState) -> OuroborosState:
    """Detect recurring-cycle language in the narrative."""
    lowered = state.raw_text.lower()

    markers = [
        "again", "over and over", "same pattern", "full circle",
        "never ends", "always this", "back here", "around and around"
    ]

    found = [m for m in markers if m in lowered]
    state.loop_markers = found
    state.loop_intensity = min(1.0, len(found) / 3.0)

    state.notes["loop_detected"] = bool(found)
    state.notes["loop_intensity"] = state.loop_intensity
    return state


# ---------------- Phase 2: Expose the Self-Devouring ---------------- #

def expose_self_devouring(state: OuroborosState) -> OuroborosState:
    """Surface what the serpent (pattern) is feeding on."""
    lowered = state.raw_text.lower()

    targets = {
        "time": ["years", "decades", "wasted time", "too long"],
        "hope": ["hope", "hoping", "maybe this time"],
        "innocence": ["innocence", "child", "childhood", "naive"],
        "love": ["love", "heart", "devotion"],
        "self_respect": ["dignity", "self-respect", "self respect", "shame"],
        "energy": ["exhausted", "drained", "no energy", "tired"],
    }

    devouring: List[str] = []
    for label, words in targets.items():
        if any(w in lowered for w in words):
            devouring.append(label)

    state.self_devouring_targets = devouring
    state.notes["self_devouring_targets"] = devouring
    return state


# ---------------- Phase 3: Open the Break-Point ---------------- #

def open_breakpoint(state: OuroborosState) -> OuroborosState:
    """Identify a threshold moment where the loop can be interrupted."""
    if not state.loop_markers:
        state.breakpoint_hint = (
            "No strong loop signal; treat each step as new rather than assumed repetition."
        )
        state.chose_transformation = False
        state.notes["breakpoint_available"] = False
        return state

    if state.self_devouring_targets:
        target_list = ", ".join(state.self_devouring_targets)
        state.breakpoint_hint = (
            f"The cycle feeds on {target_list}. The breakpoint is the next moment you "
            f"refuse to spend one more unit of that resource in the old way."
        )
    else:
        state.breakpoint_hint = (
            "The loop continues mostly by habit. The breakpoint is the first small action "
            "that does not match the usual script."
        )

    state.chose_transformation = True
    state.notes["breakpoint_available"] = True
    return state


# ---------------- Phase 4: Encode the New Cycle ---------------- #

def encode_new_cycle(state: OuroborosState) -> OuroborosState:
    """Install a renewal-focused Ouroboros pattern."""
    if not state.chose_transformation:
        state.renewed_cycle_statement = (
            "I remain aware of cycles, even if I am not yet changing them."
        )
        state.notes["renewal_installed"] = False
        return state

    if state.self_devouring_targets:
        target_list = ", ".join(state.self_devouring_targets)
        state.renewed_cycle_statement = (
            f"I no longer feed this cycle with my {target_list}. I keep the lessons, "
            "but I stop the bleed. My circle becomes a boundary and a blessing."
        )
    else:
        state.renewed_cycle_statement = (
            "I choose one new coherent move that breaks the old circle. "
            "My repetition becomes a spiral, not a trap."
        )

    state.notes["renewal_installed"] = True
    return state


# ---------------- Orchestrator ---------------- #

def run_ouroboros_cycle_kernel(text: str) -> OuroborosState:
    """Run the full Ouroboros cycle-detection and renewal pipeline."""
    state = OuroborosState(raw_text=text)

    state = detect_loop(state)
    state = expose_self_devouring(state)
    state = open_breakpoint(state)
    state = encode_new_cycle(state)

    return state
