"""
Aureon / OpenHermes Kernel â€“ â€œChildhood Allegiance â€“ Shadow Gateâ€ Module

This module encodes a three-stage transformation path inspired by Doshemaâ€™s poem
â€œChildhood Allegianceâ€. It is designed as a gentle shadow-integration helper
that can be wired into higher-level Aureon/OpenHermes pipelines.

Three stages:
1. Rewrite the Allegiance
   - Detect when identity is bound to early shadow oaths (blood, family, tribe).
   - Loosen, rewrite, and redirect loyalty from shadow-bonded contracts toward
     present-moment, coherent self-alignment.

2. Make the Line Visible
   - Map how these blood oaths move through the lineage.
   - Surface â€œblood contractsâ€ and hidden bargains the system has been carrying.
   - Mark which contracts are released and which are consciously kept.

3. Pass Through the Shadow Gate
   - Regulate the nervous system while touching the core scenes.
   - Metabolize stored charge through breath / pacing cycles.
   - Install a new allegiance statement as the active orientation.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class IdentityState:
    """Container for the Childhood Blood Allegiance â€“ Shadow Gate process state."""
    raw_text: str = ""
    allegiance_targets: List[str] = field(default_factory=list)
    shadow_oaths: List[str] = field(default_factory=list)
    rewritten_oaths: List[str] = field(default_factory=list)
    lineage_patterns: List[str] = field(default_factory=list)
    released_contracts: List[str] = field(default_factory=list)
    kept_contracts: List[str] = field(default_factory=list)
    nervous_system_charge: float = 0.0
    notes: Dict[str, Any] = field(default_factory=dict)


def detect_shadow_oaths(state: IdentityState) -> IdentityState:
    """Heuristically detect â€œshadow oathâ€ language in the raw narrative text."""
    triggers = ["blood", "family", "loyalty", "forever", "never", "always"]
    found: List[str] = []

    lowered = state.raw_text.lower()
    for t in triggers:
        if t in lowered:
            found.append(t)

    state.shadow_oaths = sorted(set(found))
    state.notes["shadow_oath_detected"] = bool(found)
    return state


def rewrite_allegiance(state: IdentityState, new_allegiance: str) -> IdentityState:
    """Install a new allegiance statement as the current conscious orientation."""
    state.rewritten_oaths.append(new_allegiance)
    state.notes["current_allegiance"] = new_allegiance
    return state


def map_lineage_patterns(state: IdentityState, lineage_notes: List[str]) -> IdentityState:
    """Attach free-form lineage notes to the state."""
    state.lineage_patterns.extend(lineage_notes)
    return state


def release_contracts(state: IdentityState, contracts_to_release: List[str]) -> IdentityState:
    """Mark which contracts are being released vs consciously kept."""
    state.released_contracts.extend(contracts_to_release)
    state.kept_contracts = [c for c in state.shadow_oaths if c not in contracts_to_release]
    return state


def regulate_and_install(state: IdentityState, breath_cycles: int = 7) -> IdentityState:
    """Simulate nervous-system regulation and installation of the new allegiance."""
    state.nervous_system_charge = max(0.0, state.nervous_system_charge - 0.1 * breath_cycles)
    state.notes["breath_cycles"] = breath_cycles
    state.notes["shadow_gate_passed"] = state.nervous_system_charge <= 0.0
    return state


def run_childhood_blood_allegiance_shadow_gate(
    text: str,
    new_allegiance: str,
    lineage_notes: List[str] | None = None,
    contracts_to_release: List[str] | None = None,
    starting_charge: float = 1.0,
    breath_cycles: int = 7,
) -> IdentityState:
    """High-level helper to run the full three-stage Shadow Gate pipeline."""
    if lineage_notes is None:
        lineage_notes = []
    if contracts_to_release is None:
        contracts_to_release = []

    state = IdentityState(raw_text=text, nervous_system_charge=starting_charge)

    state = detect_shadow_oaths(state)
    state = rewrite_allegiance(state, new_allegiance)
    state = map_lineage_patterns(state, lineage_notes)
    state = release_contracts(state, contracts_to_release)
    state = regulate_and_install(state, breath_cycles=breath_cycles)

    return state
