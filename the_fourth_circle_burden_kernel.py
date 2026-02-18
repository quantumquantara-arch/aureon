"""
Aureon / OpenHermes Kernel — “The Fourth Circle” Burden & Rotation Kernel

Inspired by Doshema’s poem “The Fourth Circle” from Beyond the Sphere of Destiny.
This kernel encodes the dynamics of a specific karmic orbit: the place where
burden, debt, and unfinished exchange keep cycling until a new principle of
movement is installed.

The “Fourth Circle” here is treated as:
- not hell, but a heavy orbit,
- not punishment, but a physics of unbalanced exchange.

Four rotational stages:

1. Name the Orbit
   - Detect language of recurring burden, debt, duty, or unresolved exchange.
   - Identify the “mass” that keeps the system circling: money, guilt, loyalty,
     unfinished work, or emotional IOUs.

2. Weigh the Load
   - Estimate the subjective burden carried in this circle.
   - Distinguish what truly belongs to the self vs. what was inherited,
     projected, or taken on without consent.

3. Break the Spin-Contract
   - Surface and symbolically dissolve the tacit contract that keeps the orbit going:
     “I must keep paying,” “I cannot stop,” “I owe them forever,” etc.
   - Introduce a new contract based on coherent exchange, not endless rotation.

4. Exit or Recalibrate the Circle
   - Decide whether to leave the circle entirely or transform it into a lighter orbit.
   - Install a new motion principle: contribution by choice, not by compulsion.

The FourthCircleState object can be consumed by financial, relational, and
karmic-pattern kernels that handle debt-logic, obligation, and long-running loops.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class FourthCircleState:
    """Container for The Fourth Circle burden & rotation process."""
    raw_text: str = ""
    orbit_markers: List[str] = field(default_factory=list)
    burden_types: List[str] = field(default_factory=list)
    self_burden: List[str] = field(default_factory=list)
    inherited_burden: List[str] = field(default_factory=list)
    spin_contract: str = ""
    spin_contract_released: bool = False
    new_motion_principle: str = ""
    exit_decision: str = ""  # "exit", "recalibrate", or ""
    notes: Dict[str, Any] = field(default_factory=dict)


# ---------------- Stage 1: Name the Orbit ---------------- #

def detect_orbit(state: FourthCircleState) -> FourthCircleState:
    """Detect recurring burden-orbit language in the text."""
    lowered = state.raw_text.lower()

    orbit_markers = [
        "round and round", "keep coming back", "same debt", "owe again",
        "back to zero", "start over", "circle of", "never finished"
    ]

    found = [m for m in orbit_markers if m in lowered]
    state.orbit_markers = found
    state.notes["orbit_detected"] = bool(found)

    burden_vocab = {
        "money": ["debt", "bills", "payments", "broke", "money"],
        "guilt": ["guilt", "guilty", "my fault", "i failed"],
        "loyalty": ["loyal", "betray", "cannot leave", "stay for them"],
        "duty": ["duty", "obligation", "responsible for them"],
        "work": ["work", "job", "task", "never done"],
        "emotional_iou": ["owe them", "make it up", "pay them back"]
    }

    burden_types: List[str] = []
    for label, words in burden_vocab.items():
        if any(w in lowered for w in words):
            burden_types.append(label)

    state.burden_types = burden_types
    state.notes["burden_types"] = burden_types
    return state


# ---------------- Stage 2: Weigh the Load ---------------- #

def weigh_load(state: FourthCircleState) -> FourthCircleState:
    """Separate self-burden from inherited or imposed burden."""
    lowered = state.raw_text.lower()

    self_cues = ["i chose", "my decision", "my mistake", "i agreed"]
    inherited_cues = ["they made me", "had to", "no choice", "family expectation",
                      "culture says", "they expect"]

    if any(c in lowered for c in self_cues):
        state.self_burden = state.burden_types.copy()

    if any(c in lowered for c in inherited_cues):
        state.inherited_burden = state.burden_types.copy()

    # If neither set of cues appears, assume mixed/unclear.
    if not state.self_burden and not state.inherited_burden and state.burden_types:
        state.inherited_burden = state.burden_types.copy()

    state.notes["self_burden"] = state.self_burden
    state.notes["inherited_burden"] = state.inherited_burden
    return state


# ---------------- Stage 3: Break the Spin-Contract ---------------- #

def break_spin_contract(state: FourthCircleState) -> FourthCircleState:
    """Identify and symbolically release the contract that keeps the orbit spinning."""
    lowered = state.raw_text.lower()

    contract_patterns = {
        "endless_payment": ["owe forever", "never enough", "can never repay"],
        "compulsory_loyalty": ["must stay", "cannot leave", "if i leave they will"],
        "self_erasure": ["i don't matter", "my needs don't count", "only they matter"],
    }

    for label, patterns in contract_patterns.items():
        if any(p in lowered for p in patterns):
            state.spin_contract = label
            break

    if not state.spin_contract and state.burden_types:
        state.spin_contract = "implicit_unending_burden"

    state.spin_contract_released = bool(state.spin_contract)
    state.notes["spin_contract"] = state.spin_contract
    state.notes["spin_contract_released"] = state.spin_contract_released
    return state


# ---------------- Stage 4: Exit or Recalibrate the Circle ---------------- #

def exit_or_recalibrate(state: FourthCircleState) -> FourthCircleState:
    """Install a new motion principle and decide on exit vs recalibration."""
    if not state.spin_contract_released:
        state.exit_decision = ""
        state.new_motion_principle = (
            "I begin to question why I am in this orbit at all."
        )
        state.notes["new_motion_installed"] = False
        return state

    # Simple heuristic: if inherited burden dominates, choose exit; if mixed, recalibrate.
    if state.inherited_burden and not state.self_burden:
        state.exit_decision = "exit"
        state.new_motion_principle = (
            "I step out of orbits built from others' debts. I only carry what is truly mine."
        )
    else:
        state.exit_decision = "recalibrate"
        state.new_motion_principle = (
            "I remain in this circle only where there is fair exchange. "
            "Obligation becomes choice; debt becomes clear agreement."
        )

    state.notes["new_motion_installed"] = True
    state.notes["exit_decision"] = state.exit_decision
    return state


# ---------------- Orchestrator ---------------- #

def run_the_fourth_circle_kernel(text: str) -> FourthCircleState:
    """Run the full Fourth Circle burden & rotation pipeline."""
    state = FourthCircleState(raw_text=text)

    state = detect_orbit(state)
    state = weigh_load(state)
    state = break_spin_contract(state)
    state = exit_or_recalibrate(state)

    return state
