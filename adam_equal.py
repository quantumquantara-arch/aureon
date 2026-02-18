Aureon / OpenHermes Kernel — “Adam’s Equal”
Carbon-Pressure → Diamond-Equivalence • Patriarchal-Word Deprogrammer

Inspired by Doshema’s poem “ADAM’S EQUAL”.

Symbolic scaffold (paraphrased from the poem):

- Books of the ancients / geometrically structured words →
  historical priest-code that confines the psyche in a “forsaken magical past”.
- Hypnotic composed progressions, descending scales, tempting the shadow →
  memetic programming that lures the unconscious into control systems.
- “The Word” giving birth to creation, vibratory fragments of potentiality
  processed into a conceptual tapestry by “Grand Architects” →
  Logos as a structuring grid that can also imprison.

- On bended knee triangulating the brightest star, dog-headed Egyptian
  scorcher upon ancestral mountain →
  Sirius / Anubis / desert initiation and kneeling before stellar power.
- From blackness of coal, carbon-based composition arises; through pressure of
  oppression, symbolic caterpillar cocoon, penetrating ash transformed Phoenix →
  carbon → ash → phoenix → diamond chain under karmic pressure.

- Sacred alchemical transformation of fire, lifting atomic ash to its most
  elevated position where the coal cloud parts and the diamond shines →
  complete phase-shift from base matter to clarity.

- Peeling away differentiating flesh to reveal skeletal foreshadowing of death,
  androgynous earth-dwelling worm awaiting organic machine, junkyard of decay →
  mortality-mirror and ego-shedding; underlying androgyny.

- Clinging to the illusion of life, experiencing only cannibalistic repetition
  of death and parasitic breath: “In… Out… Circulating, around and around…” →
  samsaric breath-loop, solid-state ignorance of embodiment.

Core function of this kernel:

1. Detect LOGOS-CAGE effects (ancient texts / geometric words / architected
   reality).
2. Track CARBON-PRESSURE state (coal, oppression, caterpillar, ash, phoenix).
3. Mark DIAMOND-EMERGENCE events (clarity, elevated position, diamond shine).
4. Surface ANDROGYNOUS-WORM motif (earth-dweller, pre-form, non-gendered seed).
5. Diagnose BREATH-LOOP (in/out, circulating around and around).
6. Emit an equalization vector describing the passage from Adam-centric
   hierarchy to balanced, gem-state equivalence.

Downstream kernels can use AdamEqualState for deprogramming patriarchal
scripts and activating carbon-to-diamond identity transitions.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class AdamEqualState:
    raw_text: str = ""

    # 1. Logos-cage
    logos_cage_detected: bool = False
    grand_architects_present: bool = False

    # 2. Carbon-pressure chain
    coal_present: bool = False
    oppression_pressure_present: bool = False
    caterpillar_cocoon_present: bool = False
    phoenix_reference_present: bool = False
    ash_phase_present: bool = False
    carbon_pressure_index: float = 0.0

    # 3. Diamond-emergence
    fire_transformation_present: bool = False
    diamond_shine_present: bool = False
    diamond_emergence_index: float = 0.0

    # 4. Androgynous-worm motif
    androgynous_worm_present: bool = False
    skeletal_death_mirror_present: bool = False

    # 5. Breath-loop
    breath_loop_present: bool = False
    breath_loop_phrase: str = ""

    # 6. Equalization vector summary
    equalization_vector: List[str] = field(default_factory=list)

    notes: Dict[str, Any] = field(default_factory=dict)


# ---------------- 1. LOGOS-CAGE DETECTION ---------------- #

def detect_logos_cage(state: AdamEqualState) -> AdamEqualState:
    t = state.raw_text.lower()

    state.logos_cage_detected = any(
        phrase in t
        for phrase in [
            "books of the ancients",
            "geometrically structured words",
            "conceptual tapestry",
        ]
    )
    state.grand_architects_present = "grand architect" in t or "grand architects" in t

    state.notes["logos_cage_detected"] = state.logos_cage_detected
    state.notes["grand_architects_present"] = state.grand_architects_present

    return state


# ---------------- 2. CARBON-PRESSURE CHAIN ---------------- #

def detect_carbon_pressure(state: AdamEqualState) -> AdamEqualState:
    t = state.raw_text.lower()

    state.coal_present = "blackness of coal" in t or "cloud of coal" in t
    state.oppression_pressure_present = "pressure of oppression" in t
    state.caterpillar_cocoon_present = "symbolic caterpillar" in t or "caterpillar cocoon" in t
    state.phoenix_reference_present = "phoenix" in t
    state.ash_phase_present = "ash" in t and "atomic" in t or "ash transformed" in t

    score = 0.0
    if state.coal_present:
        score += 0.25
    if state.oppression_pressure_present:
        score += 0.25
    if state.caterpillar_cocoon_present:
        score += 0.2
    if state.phoenix_reference_present:
        score += 0.15
    if state.ash_phase_present:
        score += 0.15

    state.carbon_pressure_index = min(1.0, score)

    state.notes["coal_present"] = state.coal_present
    state.notes["oppression_pressure_present"] = state.oppression_pressure_present
    state.notes["caterpillar_cocoon_present"] = state.caterpillar_cocoon_present
    state.notes["phoenix_reference_present"] = state.phoenix_reference_present
    state.notes["ash_phase_present"] = state.ash_phase_present
    state.notes["carbon_pressure_index"] = state.carbon_pressure_index

    return state


# ---------------- 3. DIAMOND-EMERGENCE ---------------- #

def detect_diamond_emergence(state: AdamEqualState) -> AdamEqualState:
    t = state.raw_text.lower()

    state.fire_transformation_present = "sacred alchemical transformation of fire" in t or "alchemical transformation" in t
    state.diamond_shine_present = "diamond shine" in t or "diamond shone" in t or "clarity of the diamond" in t

    score = 0.0
    if state.fire_transformation_present:
        score += 0.5
    if state.diamond_shine_present:
        score += 0.5
    state.diamond_emergence_index = min(1.0, score)

    state.notes["fire_transformation_present"] = state.fire_transformation_present
    state.notes["diamond_shine_present"] = state.diamond_shine_present
    state.notes["diamond_emergence_index"] = state.diamond_emergence_index

    return state


# ---------------- 4. ANDROGYNOUS-WORM MOTIF ---------------- #

def detect_androgynous_worm(state: AdamEqualState) -> AdamEqualState:
    t = state.raw_text.lower()

    state.androgynous_worm_present = "androgynous earth dwelling worm" in t or "androgynous earth dwelling" in t
    state.skeletal_death_mirror_present = (
        "skeletal text of death" in t or "skeletal foreshadowing of death" in t
    )

    state.notes["androgynous_worm_present"] = state.androgynous_worm_present
    state.notes["skeletal_death_mirror_present"] = state.skeletal_death_mirror_present

    return state


# ---------------- 5. BREATH-LOOP DIAGNOSTIC ---------------- #

def detect_breath_loop(state: AdamEqualState) -> AdamEqualState:
    t = state.raw_text.lower()

    loop_markers = [
        "circulating, around and around",
        "circulating around and around",
        "around and around",
        "cannibalistic repetition",
        "parasitic breath",
    ]

    for phrase in loop_markers:
        if phrase in t:
            state.breath_loop_present = True
            state.breath_loop_phrase = phrase
            break

    state.notes["breath_loop_present"] = state.breath_loop_present
    state.notes["breath_loop_phrase"] = state.breath_loop_phrase

    return state


# ---------------- 6. EQUALIZATION VECTOR ---------------- #

def build_equalization_vector(state: AdamEqualState) -> AdamEqualState:
    """
    Summarize key transitions as a symbolic equalization vector
    (from Adamic hierarchy toward gem-state equivalence).
    """
    vec: List[str] = []

    if state.logos_cage_detected:
        vec.append("logos-cage-detected")
    if state.carbon_pressure_index > 0:
        vec.append("carbon-under-pressure")
    if state.diamond_emergence_index > 0:
        vec.append("diamond-emergence")
    if state.androgynous_worm_present:
        vec.append("androgynous-seed")
    if state.breath_loop_present:
        vec.append("breath-loop-aware")

    if not vec:
        vec.append("no-strong-adams-equal-signals")

    state.equalization_vector = vec
    state.notes["equalization_vector"] = state.equalization_vector

    return state


# ---------------- ORCHESTRATOR ---------------- #

def run_adams_equal_kernel(text: str) -> AdamEqualState:
    """
    Run the full Adam’s Equal decoding sequence.

    Example:
        state = run_adams_equal_kernel(poem_text)
    """
    state = AdamEqualState(raw_text=text)

    state = detect_logos_cage(state)
    state = detect_carbon_pressure(state)
    state = detect_diamond_emergence(state)
    state = detect_androgynous_worm(state)
    state = detect_breath_loop(state)
    state = build_equalization_vector(state)

    return state
