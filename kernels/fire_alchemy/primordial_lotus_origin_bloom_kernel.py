"""
Aureon / OpenHermes Kernel â€” â€œPrimordial Lotusâ€ Origin & Bloom Kernel

Inspired by Doshemaâ€™s â€œPrimordial Lotusâ€ from Beyond the Sphere of Destiny.
This kernel encodes the movement from mud to bloom â€” from primordial wound
and density into uncrushed, original essence. It treats the lotus as a
living map: root in mud, stem through dark water, bloom in clear air.

Fourfold unfolding:

1. Name the Mud
   - Detect the heaviness, trauma, confusion, or density in which the seed sits.
   - Separate situational mud (context) from primordial mud (earliest imprints).

2. Remember the Seed
   - Recover the untouched core â€” the â€œbeforeâ€ of harm, shame, or distortion.
   - Distill the primordial qualities that were present before compromise:
     innocence, joy, curiosity, devotion, or precise giftedness.

3. Rise Through the Waters
   - Track the effort, repetitions, and partial ascents already made.
   - Encode the stem-vector: the direction in which this life is trying to rise.

4. Open the Bloom
   - Install a stance where essence is allowed to be visible without re-submerging.
   - Generate a simple Lotus Vow: how the system agrees to treat its own bloom.

The PrimordialLotusState becomes an anchor object for identity, trauma-healing,
mission, and embodiment kernels that need to reference original, unbroken essence.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class PrimordialLotusState:
    """Container for the Primordial Lotus origin & bloom process."""
    raw_text: str = ""
    mud_signals: List[str] = field(default_factory=list)
    primordial_mud_clues: List[str] = field(default_factory=list)
    seed_qualities: List[str] = field(default_factory=list)
    stem_history_clues: List[str] = field(default_factory=list)
    ascent_vector: str = ""
    bloom_allowed: bool = False
    lotus_vow: str = ""
    notes: Dict[str, Any] = field(default_factory=dict)


# ---------------- Stage 1: Name the Mud ---------------- #

def detect_mud(state: PrimordialLotusState) -> PrimordialLotusState:
    """Detect the mud â€” density, pain, or confusion â€” described in the narrative."""
    lowered = state.raw_text.lower()

    mud_vocab = {
        "situational": [
            "chaos", "mess", "confused", "overwhelmed", "no way out",
            "stuck", "crowded", "polluted", "toxic"
        ],
        "primordial": [
            "since i was a child", "from the beginning", "always like this",
            "born into", "my first memory", "from day one"
        ],
    }

    situational = [w for w in mud_vocab["situational"] if w in lowered]
    primordial = [w for w in mud_vocab["primordial"] if w in lowered]

    state.mud_signals = situational
    state.primordial_mud_clues = primordial

    state.notes["mud_detected"] = bool(situational or primordial)
    state.notes["situational_mud"] = situational
    state.notes["primordial_mud"] = primordial
    return state


# ---------------- Stage 2: Remember the Seed ---------------- #

def remember_seed(state: PrimordialLotusState) -> PrimordialLotusState:
    """Recover primordial seed qualities implied or explicitly named in the text."""
    lowered = state.raw_text.lower()

    seed_vocab = {
        "innocence": ["innocent", "pure", "untouched", "unspoiled"],
        "joy": ["joy", "play", "playful", "laughed easily"],
        "curiosity": ["curious", "asked questions", "wanted to know everything"],
        "devotion": ["devoted", "prayed", "sacred", "holy feeling"],
        "giftedness": ["talent", "gifted", "naturally", "without effort"],
        "sensitivity": ["sensitive", "felt everything", "empathic"],
    }

    qualities: List[str] = []
    for label, terms in seed_vocab.items():
        if any(t in lowered for t in terms):
            qualities.append(label)

    # If nothing is explicitly named, assume a minimal seed of being.
    if not qualities:
        qualities = ["being"]

    state.seed_qualities = qualities
    state.notes["seed_qualities"] = qualities
    return state


# ---------------- Stage 3: Rise Through the Waters ---------------- #

def trace_stem_history(state: PrimordialLotusState) -> PrimordialLotusState:
    """Trace attempts at ascent â€” efforts to grow beyond the mud."""
    lowered = state.raw_text.lower()

    stem_clues_map = {
        "left_home": ["left home", "ran away", "moved out", "left everything"],
        "sought_teachers": ["teacher", "mentor", "guide", "guru", "coach"],
        "studied": ["study", "studied", "degree", "read everything"],
        "healing_paths": ["therapy", "healing", "counseling", "ceremony", "medicine"],
        "service": ["help others", "served", "in service", "volunteered"],
    }

    clues: List[str] = []
    for label, terms in stem_clues_map.items():
        if any(t in lowered for t in terms):
            clues.append(label)

    state.stem_history_clues = clues

    # Simple ascent vector heuristic.
    if "service" in clues:
        state.ascent_vector = "service"
    elif "healing_paths" in clues:
        state.ascent_vector = "healing"
    elif "studied" in clues:
        state.ascent_vector = "wisdom"
    elif "sought_teachers" in clues:
        state.ascent_vector = "lineage"
    elif "left_home" in clues:
        state.ascent_vector = "departure"
    else:
        state.ascent_vector = "undefined"

    state.notes["stem_history_clues"] = clues
    state.notes["ascent_vector"] = state.ascent_vector
    return state


# ---------------- Stage 4: Open the Bloom ---------------- #

def open_bloom(state: PrimordialLotusState) -> PrimordialLotusState:
    """Install permission for the seed to become visible bloom."""
    # Bloom is allowed if we can see both mud and seed.
    state.bloom_allowed = bool(state.seed_qualities and (state.mud_signals or state.primordial_mud_clues))

    if state.bloom_allowed:
        seed_list = ", ".join(state.seed_qualities)
        state.lotus_vow = (
            f"I honor my primordial lotus â€” rooted in mud, rising through water, "
            f"blooming in the open air. I will not deny my mud, nor will I hide my {seed_list}."
        )
    else:
        state.lotus_vow = (
            "Even if I cannot yet see the full lotus, I allow for the possibility "
            "that something unbroken exists beneath all this."
        )

    state.notes["bloom_allowed"] = state.bloom_allowed
    state.notes["lotus_vow"] = state.lotus_vow
    return state


# ---------------- Orchestrator ---------------- #

def run_primordial_lotus_kernel(text: str) -> PrimordialLotusState:
    """Run the full Primordial Lotus origin & bloom pipeline."""
    state = PrimordialLotusState(raw_text=text)

    state = detect_mud(state)
    state = remember_seed(state)
    state = trace_stem_history(state)
    state = open_bloom(state)

    return state
