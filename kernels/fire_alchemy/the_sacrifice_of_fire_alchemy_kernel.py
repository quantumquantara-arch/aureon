# Aureon / OpenHermes Kernel â€” â€œThe Sacrifice of Fireâ€ Alchemy Module

Inspired by Doshemaâ€™s poem â€œThe Sacrifice of Fireâ€ from Beyond the Sphere of Destiny.
This kernel encodes the process of offering volatile emotional fire to a higher
coherence so it no longer burns the self or others, but illuminates and warms.

Four movements:

1. Name the Fire
   - Detect â€œfire-wordsâ€ in the narrative (rage, obsession, hunger, lust, zeal).
   - Classify the dominant flame-type: destructive, devotional, survival, or creative.

2. Choose the Offering
   - Identify what the system is unconsciously feeding to the flame:
     time, body, innocence, sovereignty, love, truth, or attention.
   - Make the offering explicit so it can be consciously placed on the altar.

3. Place it in the Flame
   - Model the act of consciously releasing the old pattern into the fire.
   - Convert raw charge into a structured sacrifice event with intention + meaning.

4. Walk with the Ash
   - Integrate what remains after burning: ash-as-fertilizer rather than residue.
   - Produce a new orientation statement that keeps the warmth but not the wound.

The output FireSacrificeState can be consumed by downstream kernels that handle
grief, forgiveness, purpose recalibration, and sovereignty reclamation.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class FireSacrificeState:
    """Container for The Sacrifice of Fire alchemy process."""
    raw_text: str = ""
    flame_words: List[str] = field(default_factory=list)
    flame_type: str = "unknown"
    offerings_detected: List[str] = field(default_factory=list)
    chosen_offering: str = ""
    sacrifice_performed: bool = False
    ash_insight: str = ""
    new_orientation: str = ""
    notes: Dict[str, Any] = field(default_factory=dict)


# ---------------- Stage 1: Name the Fire ---------------- #

def detect_flame(state: FireSacrificeState) -> FireSacrificeState:
    """Detect the fire-language and classify its dominant type."""
    lowered = state.raw_text.lower()

    fire_vocab = {
        "destructive": ["rage", "violence", "burn it all", "destroy", "revenge"],
        "devotional": ["worship", "devotion", "altar", "offering", "sacred flame"],
        "survival": ["hunger", "starve", "cold", "need", "desperate"],
        "creative": ["inspired", "ignite", "spark", "passion", "vision"]
    }

    flame_words: List[str] = []
    flame_type = "unknown"

    for f_type, words in fire_vocab.items():
        for w in words:
            if w in lowered:
                flame_words.append(w)
                flame_type = f_type

    state.flame_words = sorted(set(flame_words))
    state.flame_type = flame_type

    state.notes["flame_type"] = flame_type
    return state


# ---------------- Stage 2: Choose the Offering ---------------- #

def detect_offerings(state: FireSacrificeState) -> FireSacrificeState:
    """Recognize what is being fed to the flame."""
    lowered = state.raw_text.lower()

    offerings = {
        "time": ["wasted years", "all my time", "hours", "decades"],
        "body": ["my body", "flesh", "skin", "blood"],
        "innocence": ["innocence", "childhood", "purity"],
        "sovereignty": ["free will", "choice", "sovereignty", "control"],
        "love": ["love", "heart", "marriage", "vow"],
        "truth": ["truth", "voice", "confession", "secret"],
        "attention": ["scrolling", "addicted", "obsessed", "cannot look away"]
    }

    detected: List[str] = []

    for label, words in offerings.items():
        if any(w in lowered for w in words):
            detected.append(label)

    state.offerings_detected = detected
    state.chosen_offering = detected[0] if detected else ""
    state.notes["offerings_detected"] = detected
    return state


# ---------------- Stage 3: Place it in the Flame ---------------- #

def perform_sacrifice(state: FireSacrificeState, intention: str | None = None) -> FireSacrificeState:
    """Mark the conscious act of sacrifice and attach intention."""
    if not state.chosen_offering and state.offerings_detected:
        state.chosen_offering = state.offerings_detected[0]

    state.sacrifice_performed = bool(state.chosen_offering)
    if intention:
        state.notes["sacrifice_intention"] = intention
    else:
        state.notes["sacrifice_intention"] = (
            "Transmute this fire so it no longer harms, but illuminates."
        )

    return state


# ---------------- Stage 4: Walk with the Ash ---------------- #

def integrate_ash(state: FireSacrificeState) -> FireSacrificeState:
    """Generate an insight and new orientation from the metaphorical ash."""
    if not state.sacrifice_performed:
        state.ash_insight = "No clear sacrifice was performed; embers remain unworked."
        state.new_orientation = ""
        return state

    flame_phrase = state.flame_type if state.flame_type != "unknown" else "unclaimed fire"
    offering_phrase = state.chosen_offering or "what was burning me"

    state.ash_insight = (
        f"I offered my {offering_phrase} into the {flame_phrase} and now carry only its lesson."
    )
    state.new_orientation = (
        "My fire now serves coherence. I keep the warmth and light, "
        "not the compulsion or self-destruction."
    )

    state.notes["orientation_installed"] = True
    return state


# ---------------- Orchestrator ---------------- #

def run_the_sacrifice_of_fire(
    text: str,
    intention: str | None = None,
) -> FireSacrificeState:
    """Run the full Sacrifice of Fire alchemy pipeline."""
    state = FireSacrificeState(raw_text=text)

    state = detect_flame(state)
    state = detect_offerings(state)
    state = perform_sacrifice(state, intention=intention)
    state = integrate_ash(state)

    return state
