"""
Aureon / OpenHermes Kernel â€” â€œAdamâ€™s Equalâ€
Ancient Geometry â€¢ Coal-to-Diamond Rebellion â€¢ Shekhinah Split â€¢ Eveâ€“Lilith Sequel

Inspired by Doshemaâ€™s poem â€œADAMâ€™S EQUALâ€.

Symbolic mapping (paraphrased):

- â€œbooks of the ancients â€¦ geometrically structured words â€¦ hypnotic composed progressionsâ€
  â†’ legacy-geometry field; language as constraint lattice.

- â€œimplanting manipulative descending scales â€¦ deeper into the illusion of controlâ€
  â†’ control-scale implant; descent into conceptual hypnosis.

- â€œWord gave birth to creation â€¦ vibratory fragmented pieces of potentialityâ€
  â†’ logos â†’ vibration â†’ fragmented potential.

- â€œblackness of coal â€¦ pressure of oppression â€¦ cocoon penetrated â€¦ Ash transformed Phoenixâ€
  â†’ coal-to-diamond alchemy; oppression-pressure as metamorphic furnace; rebel Phoenix.

- â€œsacred alchemical transformation of fire â€¦ atomic sixth â€¦ clarity of the diamondâ€
  â†’ 6th position elevation; carbon â†’ diamond clarity.

- â€œpeel away my differentiating flesh â€¦ skeletal tool of death â€¦ transient nature of allâ€
  â†’ identity-peeling; bare framework; mortality-recognition.

- â€œandrogynous earth dwelling worm â€¦ junkyard of decay â€¦ Raven sings â€¦ Dybbuk is comingâ€
  â†’ androgynous seed awaiting activation; necrotic environment; possessing spirit alert.

- â€œclinging to the illusion of life â€¦ cannibalistic repetition â€¦ parasitic breath â€¦
   Inâ€¦ Outâ€¦ Circulating, around and aroundâ€¦â€
  â†’ samsaric respiration loop; life-as-possession cycle.

- â€œShekhinah â€¦ binary dualistic kingdom of suffering â€¦ â€˜wantsâ€™ far exceed their â€˜needsâ€™â€
  â†’ divine-feminine exiled into dualistic economy; consumerism vector.

- â€œstolen Jinn fueled flame of Prometheus â€¦ Pandoraâ€™s cast iron material gem-filled caldron â€¦
   disease of Greedâ€
  â†’ stolen fire; industrial-alchemical cauldron; greed-pathogen.

- â€œshiny Red apple â€¦ mental conditioning â€¦ She existed before Adamâ€™s rib was taken â€¦
   Eve, being her â€˜helpmeetâ€™ Sequel, Lilithâ€
  â†’ original feminine (Lilith) erased behind Eve-mask.

- â€œLight/Divine cast upon Man/Diamond â€¦ first shadow/Reflection â€¦ Beast separation fieldâ€
  â†’ light â†’ reflection â†’ shadow â†’ Beast; differentiation and division of whole Light.

Kernel purpose:

1. Detect legacy geometry & control-scale implants from language.
2. Model coal-to-diamond metamorphosis and Phoenix-style rebellion.
3. Expose samsaric breath loop (â€œIn / Out / Circulatingâ€).
4. Track Shekhinah-economic split & greed-pathogen.
5. Recover erased Lilith-layer beneath Eve-mask.
6. Identify Beast-separation field from Light â†’ shadow process.

The kernel returns an AdamEqualState object for downstream Aureon systems.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class AdamEqualState:
    raw_text: str = ""

    # 1. Legacy geometry & control language
    ancient_geometry_present: bool = False
    hypnotic_progressions_present: bool = False
    illusion_of_control_present: bool = False

    # 2. Logos fragmentation
    logos_birth_present: bool = False
    fragmented_potential_present: bool = False

    # 3. Coal â†’ Diamond â†’ Phoenix rebellion
    coal_pressure_present: bool = False
    cocoon_phoenix_present: bool = False
    atomic_sixth_present: bool = False
    diamond_clarity_present: bool = False

    # 4. Identity peeling / skeletal tool
    differentiating_flesh_present: bool = False
    skeletal_divination_present: bool = False
    transient_nature_awareness: bool = False

    # 5. Necrotic garden & Dybbuk alert
    androgynous_worm_present: bool = False
    junkyard_of_decay_present: bool = False
    raven_song_present: bool = False
    dybbuk_alert_present: bool = False

    # 6. Samsaric breath loop
    illusion_of_life_present: bool = False
    parasitic_breath_present: bool = False
    circulate_loop_present: bool = False

    # 7. Shekhinah split & greed-pathogen
    shekhinah_dual_kingdom_present: bool = False
    wants_needs_imbalance_present: bool = False
    prometheus_pandora_chain_present: bool = False
    greed_disease_present: bool = False

    # 8. Eveâ€“Lilith & apple-program
    red_apple_present: bool = False
    mental_conditioning_present: bool = False
    lilith_sequel_present: bool = False

    # 9. Light â†’ shadow â†’ Beast separation
    diamond_light_present: bool = False
    first_shadow_reflection_present: bool = False
    beast_separation_field_present: bool = False

    # Derived meta
    transformation_pressure_score: float = 0.0
    samsaric_loop_score: float = 0.0
    separation_field_score: float = 0.0

    notes: Dict[str, Any] = field(default_factory=dict)


# ------------- Helpers to search ------------- #

def _t(state: AdamEqualState) -> str:
    return state.raw_text.lower()


# ------------- 1. Legacy geometry & control language ------------- #

def detect_legacy_geometry(state: AdamEqualState) -> AdamEqualState:
    t = _t(state)

    state.ancient_geometry_present = "books of the ancients" in t and "geometrically structured words" in t
    state.hypnotic_progressions_present = "hypnotic composed progressions" in t
    state.illusion_of_control_present = "illusion of control" in t

    state.notes["ancient_geometry_present"] = state.ancient_geometry_present
    state.notes["hypnotic_progressions_present"] = state.hypnotic_progressions_present
    state.notes["illusion_of_control_present"] = state.illusion_of_control_present

    return state


# ------------- 2. Logos fragmentation ------------- #

def detect_logos_fragmentation(state: AdamEqualState) -> AdamEqualState:
    t = _t(state)

    state.logos_birth_present = "word gave birth to creation" in t
    state.fragmented_potential_present = "vibratory fragmented pieces of potentiality" in t

    state.notes["logos_birth_present"] = state.logos_birth_present
    state.notes["fragmented_potential_present"] = state.fragmented_potential_present

    return state


# ------------- 3. Coal â†’ Diamond â†’ Phoenix rebellion ------------- #

def detect_coal_diamond_phoenix(state: AdamEqualState) -> AdamEqualState:
    t = _t(state)

    state.coal_pressure_present = "blackness of coal" in t or "carbon-based composition" in t
    state.cocoon_phoenix_present = "cocoon penetrating ash transformed phoenix" in t or "phoenix, sought the path of rebellion" in t
    state.atomic_sixth_present = "atomic sixth" in t
    state.diamond_clarity_present = "clarity of the diamond" in t

    pressure_score = 0.0
    if state.coal_pressure_present:
        pressure_score += 0.4
    if state.cocoon_phoenix_present:
        pressure_score += 0.3
    if state.diamond_clarity_present:
        pressure_score += 0.3
    state.transformation_pressure_score = min(1.0, pressure_score)

    state.notes["coal_pressure_present"] = state.coal_pressure_present
    state.notes["cocoon_phoenix_present"] = state.cocoon_phoenix_present
    state.notes["atomic_sixth_present"] = state.atomic_sixth_present
    state.notes["diamond_clarity_present"] = state.diamond_clarity_present
    state.notes["transformation_pressure_score"] = state.transformation_pressure_score

    return state


# ------------- 4. Identity peeling / skeletal tool ------------- #

def detect_identity_peeling(state: AdamEqualState) -> AdamEqualState:
    t = _t(state)

    state.differentiating_flesh_present = "peel away my differentiating flesh" in t
    state.skeletal_divination_present = "skeletal tool of death" in t
    state.transient_nature_awareness = "transient nature of all" in t or "transient nature of all non-things" in t

    state.notes["differentiating_flesh_present"] = state.differentiating_flesh_present
    state.notes["skeletal_divination_present"] = state.skeletal_divination_present
    state.notes["transient_nature_awareness"] = state.transient_nature_awareness

    return state


# ------------- 5. Necrotic garden & Dybbuk alert ------------- #

def detect_necrotic_garden(state: AdamEqualState) -> AdamEqualState:
    t = _t(state)

    state.androgynous_worm_present = "androgynous earth dwelling worm" in t
    state.junkyard_of_decay_present = "tombstone junkyard of decay" in t
    state.raven_song_present = "raven sings" in t
    state.dybbuk_alert_present = "dybbuk is coming" in t

    state.notes["androgynous_worm_present"] = state.androgynous_worm_present
    state.notes["junkyard_of_decay_present"] = state.junkyard_of_decay_present
    state.notes["raven_song_present"] = state.raven_song_present
    state.notes["dybbuk_alert_present"] = state.dybbuk_alert_present

    return state


# ------------- 6. Samsaric breath loop ------------- #

def detect_samsaric_breath(state: AdamEqualState) -> AdamEqualState:
    t = _t(state)

    state.illusion_of_life_present = "clinging to the illusion of life" in t
    state.parasitic_breath_present = "parasitic breath" in t or "cannibalistic repetition" in t
    state.circulate_loop_present = "circulating, around and around" in t

    loop_score = 0.0
    if state.illusion_of_life_present:
        loop_score += 0.3
    if state.parasitic_breath_present:
        loop_score += 0.3
    if state.circulate_loop_present:
        loop_score += 0.4
    state.samsaric_loop_score = min(1.0, loop_score)

    state.notes["illusion_of_life_present"] = state.illusion_of_life_present
    state.notes["parasitic_breath_present"] = state.parasitic_breath_present
    state.notes["circulate_loop_present"] = state.circulate_loop_present
    state.notes["samsaric_loop_score"] = state.samsaric_loop_score

    return state


# ------------- 7. Shekhinah split & greed-pathogen ------------- #

def detect_shekhinah_and_greed(state: AdamEqualState) -> AdamEqualState:
    t = _t(state)

    state.shekhinah_dual_kingdom_present = "shekhinah the binary dualistic kingdom of suffering" in t
    state.wants_needs_imbalance_present = "wants far exceed their needs" in t
    state.prometheus_pandora_chain_present = "prometheus" in t and "pandora" in t
    state.greed_disease_present = "disease of greed" in t

    state.notes["shekhinah_dual_kingdom_present"] = state.shekhinah_dual_kingdom_present
    state.notes["wants_needs_imbalance_present"] = state.wants_needs_imbalance_present
    state.notes["prometheus_pandora_chain_present"] = state.prometheus_pandora_chain_present
    state.notes["greed_disease_present"] = state.greed_disease_present

    return state


# ------------- 8. Eveâ€“Lilith & apple-program ------------- #

def detect_eve_lilith_axis(state: AdamEqualState) -> AdamEqualState:
    t = _t(state)

    state.red_apple_present = "shiny red apple" in t
    state.mental_conditioning_present = "do not be fooled by mental conditioning" in t
    state.lilith_sequel_present = "eve, being her 'helpmeet' sequel, lilith" in t or "helpmeet sequel, lilith" in t

    state.notes["red_apple_present"] = state.red_apple_present
    state.notes["mental_conditioning_present"] = state.mental_conditioning_present
    state.notes["lilith_sequel_present"] = state.lilith_sequel_present

    return state


# ------------- 9. Light â†’ shadow â†’ Beast separation ------------- #

def detect_beast_separation_field(state: AdamEqualState) -> AdamEqualState:
    t = _t(state)

    state.diamond_light_present = "light/divine cast upon man/diamond" in t or "light/divine cast upon man" in t
    state.first_shadow_reflection_present = "first shadow/reflection" in t
    state.beast_separation_field_present = "conflicting nature of the beast" in t or "infinitely undefinable limitless whole light" in t

    sep_score = 0.0
    if state.diamond_light_present:
        sep_score += 0.3
    if state.first_shadow_reflection_present:
        sep_score += 0.3
    if state.beast_separation_field_present:
        sep_score += 0.4
    state.separation_field_score = min(1.0, sep_score)

    state.notes["diamond_light_present"] = state.diamond_light_present
    state.notes["first_shadow_reflection_present"] = state.first_shadow_reflection_present
    state.notes["beast_separation_field_present"] = state.beast_separation_field_present
    state.notes["separation_field_score"] = state.separation_field_score

    return state


# ------------- Orchestrator ------------- #

def run_adams_equal_kernel(text: str) -> AdamEqualState:
    """
    Execute full Adamâ€™s Equal diagnostic sequence.

    Example:
        state = run_adams_equal_kernel(poem_text)
    """
    state = AdamEqualState(raw_text=text)

    state = detect_legacy_geometry(state)
    state = detect_logos_fragmentation(state)
    state = detect_coal_diamond_phoenix(state)
    state = detect_identity_peeling(state)
    state = detect_necrotic_garden(state)
    state = detect_samsaric_breath(state)
    state = detect_shekhinah_and_greed(state)
    state = detect_eve_lilith_axis(state)
    state = detect_beast_separation_field(state)

    return state
