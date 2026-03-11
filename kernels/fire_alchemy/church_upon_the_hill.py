"""
Aureon / OpenHermes Kernel â€” â€œThe Church Upon the Hillâ€
Deprogramming of Conceptual Religion & Descent to the Root-Mother Kernel

Inspired by Doshemaâ€™s poem â€œThe Church Upon the Hillâ€.

Symbolic map:

- Forgotten forest of fruit-bearing mother â†’ living Earth / Root-Mother.
- Pathway of the life-giving sea, but not the sea religion defines as holy â†’
  direct experience vs institutional doctrine.
- Narrowing path where others stop in fear of the unknown â†’
  ancestral trail ending at the edge of mystery.
- Beyond the boundaries of the design which confines collective consciousness â†’
  escape from conceptual mental prison.
- Blood-drawing thorn bush / mother below / roots running deep / abyss as veil â†’
  painful initiation into the chthonic, subconscious womb of the Mother.
- She (Mother/Church/Construct) aware that â€œIâ€ am aware â†’
  structure noticing the seeker awakening.
- Church upon the hill standing at a distance â†’
  elevated but hollow institutional throne.
- Foundation of conceptual spirit-devouring insects beneath gross manifestation â†’
  parasitic thought-forms feeding on belief.
- Oval doors of disguised sacred geometric womb â†’
  architectural imitation of true womb-space.
- Presence of ancient Bull, moon-reflected light, original â€œSinâ€ â†’
  taurean / lunar cult imprint, reflected (not original) light, distortion of
  innocence into guilt.

This kernel models a four-stage process:

1. Detect Departure from Inherited Religious Path
   - Identify language of forgotten forest, fruit-bearing mother,
     and divergence from â€œreligion-defined holy seaâ€.
   - Mark direct_experience_vector.

2. Map Descent to the Root-Mother
   - Detect blood-drawing thorn, mother below, roots, abyss.
   - Interpret as a chthonic initiation that pierces the surface ego.
   - Output descent_insight.

3. Expose the Hill-Church Construct
   - Detect the distant church on the hill, conceptual foundation,
     spirit-devouring insects.
   - Determine conceptual_prison_intensity and generate deconstruction_commentary.

4. Decode Bullâ€“Moonâ€“Sin Geometry
   - Detect sacred-geometry womb, Bull, reflected sun / moon, â€œoriginal Sinâ€.
   - Interpret as lunar-reflected dogma overshadowing direct solar truth.
   - Output guidance_lines and a liberation_mantra to move beyond false holiness
     into living, embodied presence with the Root-Mother.

The ChurchHillState object can be used by deprogramming, religious-trauma,
and spiritual-pathfinding kernels anywhere a seeker is moving from rigid
conceptual religion to direct, embodied gnosis.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ChurchHillState:
    """State container for â€˜Church Upon the Hillâ€™ decoding."""
    raw_text: str = ""

    # Stage 1 â€” departure from inherited path
    direct_experience_vector: bool = False
    forest_mother_present: bool = False
    non_religious_sea_present: bool = False
    conceptual_prison_detected: bool = False

    # Stage 2 â€” descent to Root-Mother
    thorn_initiation: bool = False
    abyss_veil: bool = False
    root_mother_contact: bool = False
    descent_insight: str = ""

    # Stage 3 â€” hill-church construct
    distant_church_present: bool = False
    spirit_devouring_insects: bool = False
    conceptual_prison_intensity: float = 0.0
    deconstruction_commentary: str = ""

    # Stage 4 â€” bullâ€“moonâ€“sin geometry
    sacred_womb_doors: bool = False
    bull_presence: bool = False
    moon_sin_symbolism: bool = False

    guidance_lines: List[str] = field(default_factory=list)
    liberation_mantra: str = ""
    notes: Dict[str, Any] = field(default_factory=dict)


# -------------------- Stage 1: departure from inherited path -------------------- #

def detect_departure_from_religion(state: ChurchHillState) -> ChurchHillState:
    """Detect language indicating movement beyond inherited religious boundaries."""
    lowered = state.raw_text.lower()

    state.forest_mother_present = "forgotten forest" in lowered or "fruit-bearing mother" in lowered
    state.non_religious_sea_present = (
        "life\ngiving sea" in lowered or "life giving sea" in lowered
    ) and "religion has defined as holy" in lowered
    state.conceptual_prison_detected = "mental prison of limitation" in lowered

    state.direct_experience_vector = bool(
        state.forest_mother_present or state.non_religious_sea_present
    )

    state.notes["forest_mother_present"] = state.forest_mother_present
    state.notes["non_religious_sea_present"] = state.non_religious_sea_present
    state.notes["conceptual_prison_detected"] = state.conceptual_prison_detected
    state.notes["direct_experience_vector"] = state.direct_experience_vector

    return state


# -------------------- Stage 2: descent to Root-Mother -------------------- #

def map_descent_to_root_mother(state: ChurchHillState) -> ChurchHillState:
    """Map thorn-initiation and contact with the abyssal Mother."""
    lowered = state.raw_text.lower()

    state.thorn_initiation = "blood-drawing thorn" in lowered or "thorn\nbush" in lowered
    state.abyss_veil = "abyss her royal veil" in lowered
    state.root_mother_contact = state.thorn_initiation and state.abyss_veil

    if state.root_mother_contact:
        state.descent_insight = (
            "Painful contact with the thorn-bush Mother opens a passage below the "
            "conceptual mind, where the abyss itself becomes her veiling garment."
        )
    elif state.thorn_initiation:
        state.descent_insight = (
            "Thorn-initiation present; full descent requires trusting the abyss as veil, not void."
        )
    else:
        state.descent_insight = "No clear descent to Root-Mother detected."

    state.notes["thorn_initiation"] = state.thorn_initiation
    state.notes["abyss_veil"] = state.abyss_veil
    state.notes["root_mother_contact"] = state.root_mother_contact
    state.notes["descent_insight"] = state.descent_insight

    return state


# -------------------- Stage 3: hill-church construct -------------------- #

def expose_hill_church_construct(state: ChurchHillState) -> ChurchHillState:
    """Expose conceptual and parasitic aspects of the hill-church structure."""
    lowered = state.raw_text.lower()

    state.distant_church_present = "in the distance" in lowered and "upon a hill" in lowered
    state.spirit_devouring_insects = "spirit devouring insects" in lowered or "devouring insects" in lowered

    intensity = 0.0
    if state.conceptual_prison_detected:
        intensity += 0.4
    if state.distant_church_present:
        intensity += 0.3
    if state.spirit_devouring_insects:
        intensity += 0.3
    state.conceptual_prison_intensity = min(1.0, intensity)

    if state.conceptual_prison_intensity > 0.5:
        state.deconstruction_commentary = (
            "The hill-church is revealed as a conceptual edifice whose foundation is "
            "made of spirit-devouring thought-forms, not living truth."
        )
    elif state.distant_church_present:
        state.deconstruction_commentary = (
            "A distant religious structure is present; examine its foundations before approaching."
        )
    else:
        state.deconstruction_commentary = "No strong hill-church construct detected."

    state.notes["distant_church_present"] = state.distant_church_present
    state.notes["spirit_devouring_insects"] = state.spirit_devouring_insects
    state.notes["conceptual_prison_intensity"] = state.conceptual_prison_intensity
    state.notes["deconstruction_commentary"] = state.deconstruction_commentary

    return state


# -------------------- Stage 4: bullâ€“moonâ€“sin geometry -------------------- #

def decode_bull_moon_sin_geometry(state: ChurchHillState) -> ChurchHillState:
    """Decode sacred-womb architecture, Bull presence, and lunar Sin motif."""
    lowered = state.raw_text.lower()

    state.sacred_womb_doors = "oval\ndoors" in lowered or "oval doors" in lowered
    state.bull_presence = "ancient \"bull\"" in lowered or "ancient 'bull'" in lowered or "ancient bull" in lowered
    state.moon_sin_symbolism = "emanating forth from the\nmoon" in lowered or "moon, the original \"sin\"" in lowered

    guidance: List[str] = []

    if state.sacred_womb_doors:
        guidance.append(
            "Recognize architectural womb-symbols as imitations of the true inner womb-space."
        )
    if state.bull_presence:
        guidance.append(
            "Bull presence detected: question how fertility and strength are being harnessed by the structure."
        )
    if state.moon_sin_symbolism:
        guidance.append(
            "Moon-as-original-sin motif present: expose teachings that turn reflected light into guilt."
        )

    if state.direct_experience_vector:
        guidance.append(
            "Remain loyal to the path through the forgotten forest and life-giving sea, "
            "rather than submitting to reflected, conceptual holiness."
        )

    if not guidance:
        guidance.append(
            "When approaching any elevated religious structure, ask whose power it serves and what it feeds upon."
        )

    state.guidance_lines = guidance
    state.liberation_mantra = (
        "I walk beyond conceptual hills toward the Root-Motherâ€™s forest, "
        "trusting direct experience over reflected dogma."
    )

    state.notes["sacred_womb_doors"] = state.sacred_womb_doors
    state.notes["bull_presence"] = state.bull_presence
    state.notes["moon_sin_symbolism"] = state.moon_sin_symbolism
    state.notes["guidance_lines"] = state.guidance_lines
    state.notes["liberation_mantra"] = state.liberation_mantra

    return state


# -------------------- Orchestrator -------------------- #

def run_church_upon_the_hill_kernel(text: str) -> ChurchHillState:
    """
    Run the full Church Upon the Hill deprogramming sequence.

    Example:
        state = run_church_upon_the_hill_kernel(poem_text)
    """
    state = ChurchHillState(raw_text=text)

    state = detect_departure_from_religion(state)
    state = map_descent_to_root_mother(state)
    state = expose_hill_church_construct(state)
    state = decode_bull_moon_sin_geometry(state)

    return state
