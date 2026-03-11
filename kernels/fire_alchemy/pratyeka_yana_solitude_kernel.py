"""
Aureon / OpenHermes Kernel â€” â€œPratyeka Yanaâ€ Solitude & Return Kernel

Inspired by Doshemaâ€™s â€œPratyeka Yanaâ€ from Beyond the Sphere of Destiny.
This kernel encodes the path of the solitary vehicle â€” the one who walks alone
toward liberation â€” and the pivot where isolation either crystallizes into
cold enlightenment or softens into relational coherence.

Four passages:

1. Enter the Solitary Path
   - Detect withdrawal, self-containment, and the choice to walk alone.
   - Mark whether solitude is refuge, defense, or genuine calling.

2. Gaze into the Sealed Mirror
   - Surface the gifts and distortions of the self-only path:
     clarity, discipline, autonomy vs. detachment, superiority, or numbness.
   - Track what is lost or sacrificed in the sealing.

3. Weigh the Cost of One-Way Ascent
   - Confront the price of remaining unreachable: love, shared burden,
     mutual recognition, and the chance to co-regulate with others.
   - Reveal whether the â€œmountain peakâ€ is nourishment or exile.

4. Turn the Wheel (Return or Remain)
   - Encode the choice:
       remain solitary (continue Pratyeka Yana),
       open a bridge back (return-with-wisdom),
       or widen the path for others (builder mode).
   - Install a stance that honors both insight and connection.

The PratyekaYanaState object can be used by mission, attachment,
and sangha/lineage kernels to calibrate how solitary a path should be.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class PratyekaYanaState:
    """Container for the Pratyeka Yana solitude & return process."""
    raw_text: str = ""
    solitude_markers: List[str] = field(default_factory=list)
    solitude_motive: str = ""  # "refuge", "defense", "calling", or ""
    gifts_of_solitude: List[str] = field(default_factory=list)
    distortions_of_solitude: List[str] = field(default_factory=list)
    perceived_costs: List[str] = field(default_factory=list)
    chosen_turn: str = ""  # "remain", "return", "builder", or ""
    final_stance: str = ""
    notes: Dict[str, Any] = field(default_factory=dict)


# ---------------- Passage 1: Enter the Solitary Path ---------------- #

def detect_solitude(state: PratyekaYanaState) -> PratyekaYanaState:
    """Detect language indicating a solitary, self-contained path."""
    lowered = state.raw_text.lower()

    markers = [
        "walk alone", "alone on this path", "by myself", "only me",
        "no one understands", "cannot bring anyone", "solitary", "hermit"
    ]
    found = [m for m in markers if m in lowered]
    state.solitude_markers = found
    state.notes["solitude_detected"] = bool(found)

    # Infer motive behind solitude.
    if any(p in lowered for p in ["too much", "overwhelmed", "need to be alone", "hide"]):
        state.solitude_motive = "refuge"
    if any(p in lowered for p in ["hurt", "betrayed", "never again", "cannot trust"]):
        state.solitude_motive = "defense"
    if any(p in lowered for p in ["called", "vowed", "my path", "chosen way"]):
        state.solitude_motive = "calling"

    state.notes["solitude_motive"] = state.solitude_motive
    return state


# ---------------- Passage 2: Gaze into the Sealed Mirror ---------------- #

def map_gifts_and_distortions(state: PratyekaYanaState) -> PratyekaYanaState:
    """Surface the gifts and distortions of the solitary vehicle."""
    lowered = state.raw_text.lower()

    gifts_vocab = {
        "clarity": ["clear", "clarity", "see sharply", "see through"],
        "discipline": ["discipline", "rigorous", "practice", "austere"],
        "autonomy": ["independent", "self-reliant", "need no one"],
        "silence": ["silence", "stillness", "quiet mind"],
    }

    distort_vocab = {
        "detachment": ["detached", "cannot feel", "far away", "distant"],
        "superiority": ["above them", "better than", "they are asleep", "they are lesser"],
        "numbness": ["numb", "nothing touches me", "shut down"],
        "ghosting": ["disappear", "vanish", "leave without a word"],
    }

    gifts: List[str] = []
    for label, terms in gifts_vocab.items():
        if any(t in lowered for t in terms):
            gifts.append(label)

    distortions: List[str] = []
    for label, terms in distort_vocab.items():
        if any(t in lowered for t in terms):
            distortions.append(label)

    state.gifts_of_solitude = gifts
    state.distortions_of_solitude = distortions
    state.notes["gifts_of_solitude"] = gifts
    state.notes["distortions_of_solitude"] = distortions
    return state


# ---------------- Passage 3: Weigh the Cost of One-Way Ascent ---------------- #

def weigh_pratyeka_cost(state: PratyekaYanaState) -> PratyekaYanaState:
    """Confront the cost of remaining unreachable on the solitary path."""
    lowered = state.raw_text.lower()

    cost_vocab = {
        "lost_love": ["no one beside me", "no partner", "no one stays", "love is gone"],
        "lost_sangha": ["no community", "no tribe", "no friends", "no sangha"],
        "no_witness": ["no one sees me", "unseen", "invisible"],
        "no_sharing": ["cannot share", "no one to share this with"],
    }

    costs: List[str] = []
    for label, terms in cost_vocab.items():
        if any(t in lowered for t in terms):
            costs.append(label)

    state.perceived_costs = costs
    state.notes["perceived_costs"] = costs
    return state


# ---------------- Passage 4: Turn the Wheel (Return or Remain) ---------------- #

def choose_turn(state: PratyekaYanaState) -> PratyekaYanaState:
    """Encode whether to remain solitary, return, or widen the path."""
    lowered = state.raw_text.lower()

    if any(p in lowered for p in ["i will stay alone", "this is my mountain", "i remain apart"]):
        state.chosen_turn = "remain"
    elif any(p in lowered for p in ["i want to come back", "i want to share", "i want to return"]):
        state.chosen_turn = "return"
    elif any(p in lowered for p in ["i will build a path", "for others", "so others can walk"]):
        state.chosen_turn = "builder"
    else:
        state.chosen_turn = ""

    # Install final stance text.
    if state.chosen_turn == "remain":
        state.final_stance = (
            "I honor this solitary ascent with eyes open to its costs. "
            "If I remain alone, it will be by conscious vow, not by wound."
        )
    elif state.chosen_turn == "return":
        state.final_stance = (
            "I turn from the sealed peak back toward the world, bringing what I have seen "
            "without abandoning myself again."
        )
    elif state.chosen_turn == "builder":
        state.final_stance = (
            "I remain fluent in solitude, but I carve a path so that no one has to walk "
            "this edge without a lantern."
        )
    else:
        state.final_stance = (
            "I recognize the Pratyeka pull in me and choose, step by step, how solitary "
            "I truly wish to be."
        )

    state.notes["chosen_turn"] = state.chosen_turn
    state.notes["final_stance"] = state.final_stance
    return state


# ---------------- Orchestrator ---------------- #

def run_pratyeka_yana_kernel(text: str) -> PratyekaYanaState:
    """Run the full Pratyeka Yana solitude & return pipeline."""
    state = PratyekaYanaState(raw_text=text)

    state = detect_solitude(state)
    state = map_gifts_and_distortions(state)
    state = weigh_pratyeka_cost(state)
    state = choose_turn(state)

    return state
