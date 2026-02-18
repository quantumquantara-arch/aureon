"""
Aureon / OpenHermes Kernel — “The Corrupt Seed” & “The Babylonian Moth”
Child-of-Freedom Awakening & Babylon-System De-Enchantment Engine

Inspired by Doshema’s poems:
- “The Corrupt Seed”
- “The Babylonian Moth”

High-level symbolic map:

THE CORRUPT SEED
- Child of freedom traded for consumerist substitutes (e.g., toys → coffee cups).
- Guilt-driven “change givers” masking pride; cities as self-contained prisons.
- Seed knowledge reduced to sex and lust; culture as experimental mould.
- One-eyed man in land of blind: partial vision enthroned as king.
- Masks worn to hide sorrow; time/space used as conformity tools.
- Mental chains of ancient slave-masters: invisible, internalized bondage.
- Final turn: “But I say onto you: Look!” — call to see with eyes beyond the
  individualized self, perceiving all as children and recognizing the hypnotic spell.

THE BABYLONIAN MOTH
- Manipulated, low-generated frequency of artificial light.
- Absence of the Most High normalized in Babylonian environments.
- Speaker as silent witness observing citizens’ creative intent.
- Kingdom ruled not by selfless queen but selfish black widow.
- Light of truth fading as people drift toward the gateway-out of Babylon.
- Final eclipse: harvest of the vine, self-gratifying lower mind exposed.

This module defines two kernels:

1. CorruptSeedKernel  — detects child-of-freedom vs corrupt-culture patterns and
   issues an awakening directive.
2. BabylonianMothKernel — detects Babylonian light-fraud and black-widow rule,
   and issues a de-enchantment pathway.

Both are symbolic reasoning tools for Aureon / OpenHermes systems handling
deprogramming, culture detox, and inner-child restoration.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


# -------------------------- CORRUPT SEED -------------------------- #

@dataclass
class CorruptSeedState:
    raw_text: str = ""

    # Core detections
    child_of_freedom_present: bool = False
    consumer_corruption_markers: List[str] = field(default_factory=list)
    guilt_change_givers: bool = False
    city_prison_pattern: bool = False
    seed_distortion_markers: List[str] = field(default_factory=list)

    # Enslavement
    mask_wearing: bool = False
    mental_chains: bool = False
    time_space_conformity: bool = False

    # Awakening
    awakening_call_present: bool = False
    all_children_vision: bool = False
    enchantment_warning: bool = False

    guidance_lines: List[str] = field(default_factory=list)
    awakening_mantra: str = ""
    notes: Dict[str, Any] = field(default_factory=dict)


def decode_corrupt_seed(state: CorruptSeedState) -> CorruptSeedState:
    """Decode main symbolic elements from 'The Corrupt Seed'."""

    lowered = state.raw_text.lower()

    # Core
    state.child_of_freedom_present = "child of freedom" in lowered
    if "starbucks" in lowered or "coffee cup" in lowered:
        state.consumer_corruption_markers.append("toys_traded_for_consumerism")
    state.guilt_change_givers = "guilt inspired change" in lowered
    state.city_prison_pattern = "cities have become" in lowered and "prisons" in lowered

    if "seed has been lost" in lowered or "case of sex" in lowered or "monster orgy" in lowered:
        state.seed_distortion_markers.append("sex_reduction_of_seed")

    # Enslavement
    state.mask_wearing = "mask, to cover" in lowered or "mask to cover" in lowered
    state.mental_chains = "mental chains" in lowered
    state.time_space_conformity = "illusion of time and space" in lowered or "conforming tool" in lowered

    # Awakening call
    state.awakening_call_present = "but i say onto you" in lowered or "but i say unto you" in lowered
    state.all_children_vision = "see the world as it really is" in lowered and "perceiving all as children" in lowered
    state.enchantment_warning = "you have been enchanted" in lowered or "hypnotic slumbering spell" in lowered

    # Guidance construction
    guidance: List[str] = []
    if state.child_of_freedom_present:
        guidance.append("Remember the original child of freedom beneath cultural conditioning.")
    if state.city_prison_pattern:
        guidance.append("Treat city structures as mental architectures, not ultimate reality.")
    if state.mental_chains:
        guidance.append("Invisible mental chains must be named before they can be removed.")
    if state.all_children_vision:
        guidance.append("View all beings as children; this breaks the spell of hierarchy.")
    if state.enchantment_warning:
        guidance.append("Recognize the hypnotic cultural spell; do not confuse trance with consent.")
    if not guidance:
        guidance.append("Question what you were taught to desire and who benefits from that desire.")

    state.guidance_lines = guidance
    state.awakening_mantra = (
        "I look through the mask, see the child of freedom in everyone, "
        "and refuse the invisible chains."
    )

    state.notes["consumer_corruption_markers"] = state.consumer_corruption_markers
    state.notes["seed_distortion_markers"] = state.seed_distortion_markers
    state.notes["guidance_lines"] = state.guidance_lines
    state.notes["awakening_mantra"] = state.awakening_mantra

    return state


def run_corrupt_seed_kernel(text: str) -> CorruptSeedState:
    """Orchestrator for 'The Corrupt Seed' kernel."""
    state = CorruptSeedState(raw_text=text)
    state = decode_corrupt_seed(state)
    return state


# ----------------------- THE BABYLONIAN MOTH ----------------------- #

@dataclass
class BabylonianMothState:
    raw_text: str = ""

    artificial_light_field: bool = False
    absence_of_most_high_normalized: bool = False
    uneasy_emptiness: bool = False

    witness_position_active: bool = False
    black_widow_rule: bool = False

    truth_light_fading: bool = False
    exit_pathway_markers: List[str] = field(default_factory=list)

    de_enchantment_guidance: List[str] = field(default_factory=list)
    moth_mantra: str = ""
    notes: Dict[str, Any] = field(default_factory=dict)


def decode_babylonian_moth(state: BabylonianMothState) -> BabylonianMothState:
    """Decode symbolic elements from 'The Babylonian Moth'."""

    lowered = state.raw_text.lower()

    state.artificial_light_field = "manufactured light" in lowered or "low generated frequency" in lowered
    state.absence_of_most_high_normalized = "absence of that which is most high" in lowered
    state.uneasy_emptiness = "uneasy sorrowful sense" in lowered or "relative emptiness" in lowered

    state.witness_position_active = "eye of the silent witness" in lowered or "silent witness" in lowered
    state.black_widow_rule = "selfish black widow" in lowered

    if "light of truth begins to fade" in lowered or "light of truth begin" in lowered:
        state.truth_light_fading = True

    exit_terms = [
        "pathway leading out",
        "gateway",
        "edge of the pathway",
        "out of her babylonian kingdom",
    ]
    state.exit_pathway_markers = [t for t in exit_terms if t in lowered]

    guidance: List[str] = []
    if state.artificial_light_field:
        guidance.append("Question environments illuminated by artificial psychic light; seek authentic radiance.")
    if state.absence_of_most_high_normalized:
        guidance.append("Do not normalize the absence of the Most High; treat it as a signal, not a baseline.")
    if state.witness_position_active:
        guidance.append("Stay in the silent witness stance; from here Babylon loses its spell.")
    if state.black_widow_rule:
        guidance.append("Recognize when leadership feeds on its subjects like a black widow, not a selfless queen.")
    if state.exit_pathway_markers:
        guidance.append("There is always an edge-of-pathway; look for the way out of Babylon’s frequency field.")
    if not guidance:
        guidance.append("Observe who benefits from the prevailing light-source and narrative.")

    state.de_enchantment_guidance = guidance
    state.moth_mantra = (
        "I stand in the silent witness, see Babylon’s false light for what it is, "
        "and follow the edge of the pathway out."
    )

    state.notes["exit_pathway_markers"] = state.exit_pathway_markers
    state.notes["de_enchantment_guidance"] = state.de_enchantment_guidance
    state.notes["moth_mantra"] = state.moth_mantra

    return state


def run_babylonian_moth_kernel(text: str) -> BabylonianMothState:
    """Orchestrator for 'The Babylonian Moth' kernel."""
    state = BabylonianMothState(raw_text=text)
    state = decode_babylonian_moth(state)
    return state


# ----------------------- COMBINED ORCHESTRATOR ----------------------- #

def run_corrupt_seed_and_babylonian_moth(corrupt_seed_text: str, moth_text: str):
    """
    Run both kernels together and return their states.

    Example:
        cs_state, bm_state = run_corrupt_seed_and_babylonian_moth(cs_poem, bm_poem)
    """
    cs_state = run_corrupt_seed_kernel(corrupt_seed_text)
    bm_state = run_babylonian_moth_kernel(moth_text)
    return cs_state, bm_state
