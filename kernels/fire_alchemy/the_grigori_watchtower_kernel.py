"""
Aureon / OpenHermes Kernel â€” â€œThe Grigoriâ€ Watchtower & Influence-Field Module

Inspired by Doshemaâ€™s poem â€œThe Grigoriâ€ from Beyond the Sphere of Destiny.
This kernel models the presence of watcher-intelligences (seen or unseen),
their influence on thought and choice, and the reclamation of sovereignty
within a monitored, distorted, or haunted field.

Fourfold watchtower sequence:

1. Register the Watchers
   - Detect language of being observed, judged, recorded, or silently evaluated.
   - Mark â€œGrigori signaturesâ€ â€” external or internalized watchers at the edge
     of perception.

2. Trace the Influence Field
   - Map how behavior, desire, or silence is shaped by these watchers:
     censorship, performance, moral panic, fear of punishment, or longing
     for approval.
   - Identify which voice belongs to the Grigori and which is truly the self.

3. Confront the Watchtower
   - Bring the watcher-field into direct awareness.
   - Decide what access, if any, the Grigori are allowed to have:
     observe, advise, be exiled, or be transmuted into guardianship.

4. Reclaim Inner Jurisdiction
   - Install a new jurisdiction where the core self is the final arbiter.
   - Convert hostile or parasitic watchers into neutral or protective roles,
     or remove their influence entirely.

The GrigoriState is a core input for sovereignty, psychic-boundary, and
meta-perception kernels inside Aureon / OpenHermes.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class GrigoriState:
    """Container for The Grigori watchtower and influence-field process."""
    raw_text: str = ""
    watcher_markers: List[str] = field(default_factory=list)
    watcher_intensity: float = 0.0
    influence_patterns: List[str] = field(default_factory=list)
    chosen_jurisdiction: str = ""  # "allow", "advise", "guardian", "exile"
    transformed_watchers_role: str = ""
    notes: Dict[str, Any] = field(default_factory=dict)


# ---------------- Stage 1: Register the Watchers ---------------- #

def register_watchers(state: GrigoriState) -> GrigoriState:
    """Detect 'being watched' or judged language in the narrative."""
    lowered = state.raw_text.lower()

    markers = [
        "they are watching", "being watched", "eyes on me", "judged",
        "under surveillance", "monitored", "spied on", "always looking",
        "cannot hide", "recording everything"
    ]

    found = [m for m in markers if m in lowered]
    state.watcher_markers = found
    state.watcher_intensity = min(1.0, len(found) / 3.0)

    state.notes["watchers_detected"] = bool(found)
    state.notes["watcher_intensity"] = state.watcher_intensity
    return state


# ---------------- Stage 2: Trace the Influence Field ---------------- #

def trace_influence_field(state: GrigoriState) -> GrigoriState:
    """Map how the watchers shape behavior and self-perception."""
    lowered = state.raw_text.lower()

    influence_vocab = {
        "censorship": ["biting my tongue", "cannot speak", "afraid to say", "silenced"],
        "performance": ["pretend", "performing", "act like", "appear perfect"],
        "moral_panic": ["sin", "damned", "going to hell", "unworthy", "unclean"],
        "punishment_fear": ["punished", "they will punish", "afraid of consequences"],
        "approval_hunger": ["want them to like me", "please them", "earn approval"]
    }

    patterns: List[str] = []
    for label, terms in influence_vocab.items():
        if any(t in lowered for t in terms):
            patterns.append(label)

    state.influence_patterns = patterns
    state.notes["influence_patterns"] = patterns
    return state


# ---------------- Stage 3: Confront the Watchtower ---------------- #

def confront_watchtower(state: GrigoriState) -> GrigoriState:
    """Decide how to relate to the watcher-field."""
    lowered = state.raw_text.lower()

    # Simple language-based discernment.
    if any(p in lowered for p in ["i banish you", "leave me", "get out", "no more watching"]):
        state.chosen_jurisdiction = "exile"
    elif any(p in lowered for p in ["protect me", "guard me", "stand with me"]):
        state.chosen_jurisdiction = "guardian"
    elif any(p in lowered for p in ["you may watch", "you can observe", "i accept your witness"]):
        state.chosen_jurisdiction = "allow"
    elif any(p in lowered for p in ["advise", "guide", "counsel"]):
        state.chosen_jurisdiction = "advise"
    else:
        # Default posture: re-evaluation, no automatic authority.
        state.chosen_jurisdiction = "re-evaluate"

    state.notes["chosen_jurisdiction"] = state.chosen_jurisdiction
    return state


# ---------------- Stage 4: Reclaim Inner Jurisdiction ---------------- #

def reclaim_inner_jurisdiction(state: GrigoriState) -> GrigoriState:
    """Install the final role of the Grigori relative to the self."""
    decision = state.chosen_jurisdiction

    if decision == "exile":
        state.transformed_watchers_role = (
            "The Grigori no longer hold authority here; their images may appear, "
            "but my choices are not under their rule."
        )
    elif decision == "guardian":
        state.transformed_watchers_role = (
            "The Grigori stand as sentries at the border, not masters of my mind. "
            "They alert, but I decide."
        )
    elif decision == "allow":
        state.transformed_watchers_role = (
            "Witnesses may remain, but their gaze does not define my worth or direction."
        )
    elif decision == "advise":
        state.transformed_watchers_role = (
            "I hear their counsel without surrendering my core jurisdiction."
        )
    else:  # "re-evaluate" or unknown
        state.transformed_watchers_role = (
            "I reclaim final jurisdiction over myself. Any watcher, inner or outer, "
            "must align with my coherence or lose access."
        )

    state.notes["jurisdiction_installed"] = True
    return state


# ---------------- Orchestrator ---------------- #

def run_the_grigori_watchtower_kernel(text: str) -> GrigoriState:
    """Run the full Grigori watchtower and influence-field pipeline."""
    state = GrigoriState(raw_text=text)

    state = register_watchers(state)
    state = trace_influence_field(state)
    state = confront_watchtower(state)
    state = reclaim_inner_jurisdiction(state)

    return state
