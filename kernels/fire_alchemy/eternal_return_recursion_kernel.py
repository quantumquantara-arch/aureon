"""
Aureon / OpenHermes Kernel â€” â€œEternal Returnâ€ Recursion & Choice Kernel

Inspired by Doshemaâ€™s poem â€œEternal Returnâ€ from Beyond the Sphere of Destiny.
This kernel models the experience of living through the same essential pattern
across multiple seasons, lifetimes, or epochs â€” and introduces conscious choice
about how to return.

Core movement:

1. Sense the Recurrence
   - Detect language of multi-era repetition: â€œlifetimes,â€ â€œages,â€ â€œagain in another body,â€
     or â€œsame story with new faces.â€
   - Mark the scale of return: daily, relational, generational, or mythic.

2. Identify the Invariant
   - Distill what truly repeats beneath surface detail: a specific wound, test, vow,
     desire, gift, or distortion.
   - Separate costume (form) from core motif (meaning).

3. Choose the Stance
   - Model the inner position toward the return: resignation, rebellion, numbness,
     or coherent engagement.
   - Allow for a new stance that honors the pattern without being consumed by it.

4. Encode the Return Mode
   - Encode how the system will now â€œcome back aroundâ€:
       loop (same), spiral (same axis, new altitude), exit (pattern complete),
       or guardian (stay to help others in the loop).
   - Produce a brief Eternal Return vow that can be used by downstream kernels.

The EternalReturnState becomes an anchor object for destiny, trauma-resolution,
timeline, and mission kernels that must negotiate repetition with agency.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class EternalReturnState:
    """Container for Eternal Return recursion & choice."""
    raw_text: str = ""
    recurrence_markers: List[str] = field(default_factory=list)
    time_scale_hint: str = ""  # "daily", "relational", "generational", "mythic", or ""
    invariant_motifs: List[str] = field(default_factory=list)
    chosen_stance: str = ""  # "resignation", "rebellion", "numbness", "engagement", or ""
    return_mode: str = ""  # "loop", "spiral", "exit", "guardian", or ""
    eternal_vow: str = ""
    notes: Dict[str, Any] = field(default_factory=dict)


# ---------------- Step 1: Sense the Recurrence ---------------- #

def detect_recurrence(state: EternalReturnState) -> EternalReturnState:
    """Detect language that encodes multi-scale repetition."""
    lowered = state.raw_text.lower()

    markers = [
        "every life", "another life", "past life", "again and again",
        "ages", "epochs", "over lifetimes", "same soul", "same role",
        "same story", "different faces", "full circle again"
    ]
    found = [m for m in markers if m in lowered]
    state.recurrence_markers = found
    state.notes["recurrence_detected"] = bool(found)

    # Heuristic time-scale hint
    if any(w in lowered for w in ["today", "every day", "each day", "daily"]):
        state.time_scale_hint = "daily"
    elif any(w in lowered for w in ["relationship", "partner", "friends", "family"]):
        state.time_scale_hint = "relational"
    elif any(w in lowered for w in ["ancestors", "generations", "lineage"]):
        state.time_scale_hint = "generational"
    elif any(w in lowered for w in ["lifetimes", "past life", "ages", "epochs"]):
        state.time_scale_hint = "mythic"
    else:
        state.time_scale_hint = ""

    state.notes["time_scale_hint"] = state.time_scale_hint
    return state


# ---------------- Step 2: Identify the Invariant ---------------- #

def identify_invariants(state: EternalReturnState) -> EternalReturnState:
    """Distill recurring motifs beneath surface details."""
    lowered = state.raw_text.lower()

    motif_map = {
        "abandonment": ["abandoned", "left behind", "no one stayed", "alone again"],
        "betrayal": ["betrayed", "stabbed in the back", "broken trust"],
        "sacrifice": ["sacrifice", "gave everything", "gave it all"],
        "silencing": ["silenced", "could not speak", "no one listened"],
        "mission": ["called to", "destiny", "mission", "purpose", "same calling"],
        "persecution": ["hunted", "burned", "killed for", "persecuted"],
        "love_test": ["unrequited", "unreturned love", "same heartbreak"],
    }

    motifs: List[str] = []
    for label, terms in motif_map.items():
        if any(t in lowered for t in terms):
            motifs.append(label)

    state.invariant_motifs = motifs
    state.notes["invariant_motifs"] = motifs
    return state


# ---------------- Step 3: Choose the Stance ---------------- #

def choose_stance(state: EternalReturnState) -> EternalReturnState:
    """Infer the stance toward the return from the language used."""
    lowered = state.raw_text.lower()

    if any(p in lowered for p in ["i give up", "what's the point", "nothing changes"]):
        state.chosen_stance = "resignation"
    elif any(p in lowered for p in ["never again", "i refuse", "i will fight this"]):
        state.chosen_stance = "rebellion"
    elif any(p in lowered for p in ["numb", "don't feel", "shut down", "cannot feel"]):
        state.chosen_stance = "numbness"
    elif any(p in lowered for p in ["i accept", "i will meet this", "i choose to learn"]):
        state.chosen_stance = "engagement"
    else:
        state.chosen_stance = ""

    state.notes["chosen_stance"] = state.chosen_stance
    return state


# ---------------- Step 4: Encode the Return Mode ---------------- #

def encode_return_mode(state: EternalReturnState) -> EternalReturnState:
    """Define how the pattern will now recur (or conclude)."""
    motifs = state.invariant_motifs
    stance = state.chosen_stance

    if not motifs and not stance:
        state.return_mode = "loop"
        state.eternal_vow = (
            "Even if I do not yet understand this cycle, I choose to notice it more clearly each time it returns."
        )
    else:
        # Simple mapping of stance â†’ mode.
        if stance == "resignation":
            state.return_mode = "loop"
            state.eternal_vow = (
                "I acknowledge that I have been looping in this pattern. "
                "My first step is simply to stop lying to myself about it."
            )
        elif stance == "rebellion":
            state.return_mode = "exit"
            state.eternal_vow = (
                "I break allegiance with the form of this pattern. I will no longer enact it in the old way, "
                "even if echoes remain."
            )
        elif stance == "numbness":
            state.return_mode = "spiral"
            state.eternal_vow = (
                "I allow small feelings back into view, trusting that I can rise one level at a time "
                "instead of reliving the whole storm."
            )
        elif stance == "engagement":
            # If mission/persecution motifs show up, this can become a guardian mode.
            if "mission" in motifs or "persecution" in motifs:
                state.return_mode = "guardian"
                state.eternal_vow = (
                    "I accept that I have walked this path before. This time, I walk it with eyes open, "
                    "for myself and for those who still feel trapped inside it."
                )
            else:
                state.return_mode = "spiral"
                state.eternal_vow = (
                    "I choose to meet this pattern as a teacher, not a jailer. Each return lifts me to a "
                    "higher coherence, not back into the same cage."
                )
        else:
            state.return_mode = "spiral"
            state.eternal_vow = (
                "Whatever this cycle has been, I allow it to become a spiral of learning instead of a flat loop."
            )

    state.notes["return_mode"] = state.return_mode
    state.notes["eternal_vow"] = state.eternal_vow
    return state


# ---------------- Orchestrator ---------------- #

def run_eternal_return_recursion_kernel(text: str) -> EternalReturnState:
    """Run the full Eternal Return recursion & choice pipeline."""
    state = EternalReturnState(raw_text=text)

    state = detect_recurrence(state)
    state = identify_invariants(state)
    state = choose_stance(state)
    state = encode_return_mode(state)

    return state
