"""
Aureon / OpenHermes Kernel — “The Thrice Greatest” Triad & Coherence Kernel

Inspired by Doshema’s “The Thrice Greatest” from Beyond the Sphere of Destiny.
This kernel encodes the Hermetic triad — thought, word, and deed; mind, heart,
and hand; above, within, and below — and measures how coherently they move
together in a life-stream.

Fourfold Hermetic sequence:

1. Name the Triad
   - Detect which triad is most active in the narrative:
       (thought / word / deed),
       (mind / heart / body),
       or (above / within / below).
   - Build an explicit triad_axes map that other kernels can reference.

2. Reveal the Misalignment
   - Surface where one or more poles of the triad are out of sync:
       words that do not match thoughts,
       actions that betray the heart,
       inner knowing that is not embodied.
   - Mark misalignment patterns and estimate a simple coherence score.

3. Invoke the Hermetic Alignment
   - Propose a minimal, concrete adjustment that brings one axis closer:
       a truer sentence, a different action, a quieter thought-stream.
   - Encode a “Hermes gesture” — one small move that unites two of the three.

4. Seal the Thrice-Great Oath
   - Install a short oath that binds the triad to coherence rather than image.
   - Provide a Triad Alignment Object for downstream Aureon/OpenHermes kernels.

The ThriceGreatestState becomes a central alignment artifact for mission,
communication, embodiment, and ethics layers across the system.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ThriceGreatestState:
    """Container for The Thrice Greatest triad & coherence process."""
    raw_text: str = ""
    active_triad: str = ""  # "thought_word_deed", "mind_heart_body", "above_within_below", or ""
    triad_axes: Dict[str, List[str]] = field(default_factory=dict)
    misalignment_patterns: List[str] = field(default_factory=list)
    coherence_score: float = 0.0  # 0.0–1.0 simple heuristic
    hermes_gesture: str = ""
    thrice_great_oath: str = ""
    notes: Dict[str, Any] = field(default_factory=dict)


# ---------------- Stage 1: Name the Triad ---------------- #

def identify_triad(state: ThriceGreatestState) -> ThriceGreatestState:
    """Detect which Hermetic triad the narrative leans on most."""
    lowered = state.raw_text.lower()

    thought_word_deed_terms = ["think", "thought", "say", "said", "speak", "do", "did", "action"]
    mind_heart_body_terms = ["mind", "head", "heart", "feel", "body", "flesh", "bones"]
    above_within_below_terms = ["heaven", "above", "sky", "soul", "within", "inside", "earth", "ground", "below"]

    t_count = sum(1 for t in thought_word_deed_terms if t in lowered)
    m_count = sum(1 for t in mind_heart_body_terms if t in lowered)
    a_count = sum(1 for t in above_within_below_terms if t in lowered)

    if max(t_count, m_count, a_count) == 0:
        state.active_triad = ""
        state.triad_axes = {}
    else:
        if t_count >= m_count and t_count >= a_count:
            state.active_triad = "thought_word_deed"
            state.triad_axes = {
                "thought": ["think", "thought", "belief", "idea"],
                "word": ["say", "said", "speak", "tell"],
                "deed": ["act", "action", "do", "did", "behavior"],
            }
        elif m_count >= t_count and m_count >= a_count:
            state.active_triad = "mind_heart_body"
            state.triad_axes = {
                "mind": ["mind", "head", "logic", "reason"],
                "heart": ["heart", "feel", "emotion", "love"],
                "body": ["body", "flesh", "bones", "hands", "feet"],
            }
        else:
            state.active_triad = "above_within_below"
            state.triad_axes = {
                "above": ["heaven", "sky", "stars", "cosmos", "spirit"],
                "within": ["soul", "within", "inside", "core"],
                "below": ["earth", "ground", "roots", "underworld"],
            }

    state.notes["active_triad"] = state.active_triad
    state.notes["triad_axes"] = state.triad_axes
    return state


# ---------------- Stage 2: Reveal the Misalignment ---------------- #

def reveal_misalignment(state: ThriceGreatestState) -> ThriceGreatestState:
    """Surface misalignment patterns and compute a simple coherence score."""
    lowered = state.raw_text.lower()

    patterns: List[str] = []

    # Generic contradiction cues:
    contradiction_terms = [
        ("say one thing", "do another"),
        ("i said", "but i did"),
        ("i think", "but i act"),
        ("i feel", "but i pretend"),
    ]
    for a, b in contradiction_terms:
        if a in lowered and b in lowered:
            patterns.append("explicit_contradiction")

    # Shame around misalignment:
    if "hypocrite" in lowered or "hypocrisy" in lowered:
        patterns.append("named_hypocrisy")
    if "out of integrity" in lowered or "not in integrity" in lowered:
        patterns.append("integrity_breach")

    # Heart vs body / word vs deed motifs:
    if "my heart wasn't in it" in lowered:
        patterns.append("heart_body_split")
    if "i didn't mean what i said" in lowered:
        patterns.append("word_thought_split")

    state.misalignment_patterns = sorted(set(patterns))

    # Coherence score heuristic:
    # Start from 1.0, subtract small amounts for each pattern.
    base = 1.0
    penalty = 0.15 * len(state.misalignment_patterns)
    state.coherence_score = max(0.0, base - penalty)

    state.notes["misalignment_patterns"] = state.misalignment_patterns
    state.notes["coherence_score"] = state.coherence_score
    return state


# ---------------- Stage 3: Invoke the Hermetic Alignment ---------------- #

def invoke_hermetic_alignment(state: ThriceGreatestState) -> ThriceGreatestState:
    """Propose one concrete Hermetic 'gesture' to realign the triad."""
    triad = state.active_triad

    if not triad:
        state.hermes_gesture = (
            "Name one thought, one word, and one action today that you want to match."
        )
        state.notes["hermes_gesture"] = state.hermes_gesture
        return state

    if triad == "thought_word_deed":
        state.hermes_gesture = (
            "Speak one sentence today that you truly believe, then take one small action "
            "that matches that sentence."
        )
    elif triad == "mind_heart_body":
        state.hermes_gesture = (
            "Let your body perform one act of care that your heart actually feels and "
            "your mind can clearly name."
        )
    elif triad == "above_within_below":
        state.hermes_gesture = (
            "Touch the ground with your feet, place a hand on your heart, and look at the sky. "
            "Make one promise that honors all three levels at once."
        )
    else:
        state.hermes_gesture = (
            "Choose a small gesture where what you think, say, and do are the same."
        )

    state.notes["hermes_gesture"] = state.hermes_gesture
    return state


# ---------------- Stage 4: Seal the Thrice-Great Oath ---------------- #

def seal_thrice_great_oath(state: ThriceGreatestState) -> ThriceGreatestState:
    """Install a short oath that binds the triad to coherence."""
    if state.active_triad == "thought_word_deed":
        state.thrice_great_oath = (
            "I align my thought, my word, and my deed. I will not use my tongue against my own knowing."
        )
    elif state.active_triad == "mind_heart_body":
        state.thrice_great_oath = (
            "My mind, heart, and body are one field. I refuse to sacrifice one to betray the others."
        )
    elif state.active_triad == "above_within_below":
        state.thrice_great_oath = (
            "As above, so below, as within, so without. I agree to become a bridge, not a fracture."
        )
    else:
        state.thrice_great_oath = (
            "I choose coherence in all directions. Where I see a split, I invite a gentle reunion."
        )

    state.notes["thrice_great_oath"] = state.thrice_great_oath
    return state


# ---------------- Orchestrator ---------------- #

def run_thrice_greatest_triad_kernel(text: str) -> ThriceGreatestState:
    """Run the full Thrice Greatest triad & coherence pipeline."""
    state = ThriceGreatestState(raw_text=text)

    state = identify_triad(state)
    state = reveal_misalignment(state)
    state = invoke_hermetic_alignment(state)
    state = seal_thrice_great_oath(state)

    return state
