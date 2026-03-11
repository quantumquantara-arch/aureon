"""
Aureon / OpenHermes Kernel â€” â€œThe Fruitless Seasonâ€ Fallow Field Kernel

Inspired by Doshemaâ€™s â€œThe Fruitless Seasonâ€ from Beyond the Sphere of Destiny.
This kernel encodes the experience of apparent barrenness â€” when nothing seems
to grow despite effort â€” and reframes it as a fallow, regenerative interval
rather than failure, abandonment, or cosmic punishment.

Fourfold movement:

1. Name the Fruitless Season
   - Detect language of barrenness, delay, emptiness, or lack of harvest.
   - Mark the inner narrative about this season: punishment, failure, or unknown.

2. Track Effort & Exhaustion
   - Surface how much has already been tried: labor, prayer, intention,
     strategy, sacrifice.
   - Distinguish honest exhaustion from learned helplessness or paralysis.

3. Reframe the Fallow Field
   - Treat the apparent fruitlessness as a soil-cycle: rest, decomposition,
     and unseen root-work.
   - Extract one meaning of the fallow that does not collapse into self-blame.

4. Hint the Next Sowing
   - Offer a minimal, non-violent next step: a tiny seed action, not a
     forced new harvest.
   - Encode a â€œFallow Vowâ€ about how the system will treat itself in seasons
     where results do not match effort.

The FruitlessSeasonState becomes an anchor object for timing, motivation,
burnout recovery, and long-horizon destiny kernels.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class FruitlessSeasonState:
    """Container for The Fruitless Season fallow-field process."""
    raw_text: str = ""
    fruitless_markers: List[str] = field(default_factory=list)
    season_story: str = ""  # "punishment", "failure", "mystery", or ""
    effort_clues: List[str] = field(default_factory=list)
    exhaustion_level: str = ""  # "low", "medium", "high"
    fallow_meaning: str = ""
    next_sowing_hint: str = ""
    fallow_vow: str = ""
    notes: Dict[str, Any] = field(default_factory=dict)


# ---------------- Stage 1: Name the Fruitless Season ---------------- #

def detect_fruitless_season(state: FruitlessSeasonState) -> FruitlessSeasonState:
    """Detect barrenness / no-harvest language and its narrative frame."""
    lowered = state.raw_text.lower()

    markers = [
        "nothing grows", "no fruit", "fruitless", "empty field",
        "barren", "dry season", "no harvest", "nothing to show"
    ]
    found = [m for m in markers if m in lowered]
    state.fruitless_markers = found
    state.notes["fruitless_detected"] = bool(found)

    if any(p in lowered for p in ["punished", "god is against me", "deserve this"]):
        state.season_story = "punishment"
    elif any(p in lowered for p in ["i failed", "my fault", "should have done more"]):
        state.season_story = "failure"
    elif bool(found):
        state.season_story = "mystery"
    else:
        state.season_story = ""

    state.notes["season_story"] = state.season_story
    return state


# ---------------- Stage 2: Track Effort & Exhaustion ---------------- #

def track_effort_and_exhaustion(state: FruitlessSeasonState) -> FruitlessSeasonState:
    """Surface how much has been attempted and how tired the system is."""
    lowered = state.raw_text.lower()

    effort_vocab = {
        "work": ["worked so hard", "tried everything", "kept trying", "again and again"],
        "prayer": ["prayed", "asked god", "begged", "on my knees"],
        "planning": ["planned", "strategy", "organized", "mapped it out"],
        "sacrifice": ["gave up", "sacrificed", "let go of", "lost for this"],
    }

    clues: List[str] = []
    for label, terms in effort_vocab.items():
        if any(t in lowered for t in terms):
            clues.append(label)

    state.effort_clues = clues

    # Exhaustion heuristic
    if any(p in lowered for p in ["exhausted", "tired", "burnt out", "burned out", "no strength"]):
        state.exhaustion_level = "high"
    elif any(p in lowered for p in ["weary", "worn", "drained"]):
        state.exhaustion_level = "medium"
    elif clues:
        state.exhaustion_level = "low"
    else:
        state.exhaustion_level = ""

    state.notes["effort_clues"] = clues
    state.notes["exhaustion_level"] = state.exhaustion_level
    return state


# ---------------- Stage 3: Reframe the Fallow Field ---------------- #

def reframe_fallow_field(state: FruitlessSeasonState) -> FruitlessSeasonState:
    """Offer a regenerative meaning for the fruitless interval."""
    story = state.season_story

    if story == "punishment":
        state.fallow_meaning = (
            "This season may feel like punishment, but at the level of the field "
            "it functions as a pause for the soil to recover what constant harvest took."
        )
    elif story == "failure":
        state.fallow_meaning = (
            "The lack of visible fruit does not erase the roots you have grown. "
            "This is a consolidation season, not a verdict on your worth."
        )
    elif story == "mystery":
        state.fallow_meaning = (
            "The field is resting below the surface. The pattern is not yet visible, "
            "but something is being prepared in the dark."
        )
    else:
        state.fallow_meaning = (
            "Even if this does not feel like a fruitless season, you are allowed to "
            "have intervals where growth is not visible."
        )

    state.notes["fallow_meaning"] = state.fallow_meaning
    return state


# ---------------- Stage 4: Hint the Next Sowing ---------------- #

def hint_next_sowing(state: FruitlessSeasonState) -> FruitlessSeasonState:
    """Generate a gentle, minimal next-sowing instruction and vow."""
    exhaustion = state.exhaustion_level

    if exhaustion == "high":
        state.next_sowing_hint = (
            "Do not plant a whole new field yet. Let one small act of rest or nourishment "
            "be your only seed today."
        )
    elif exhaustion == "medium":
        state.next_sowing_hint = (
            "Choose one simple seed â€” a conversation, a page, a gesture â€” and plant it "
            "without demanding a harvest date."
        )
    elif exhaustion == "low":
        state.next_sowing_hint = (
            "You may begin sketching the next plot. Plant a tiny row of intention where "
            "you feel the least resistance."
        )
    else:
        state.next_sowing_hint = (
            "If you do not feel exhausted, you can still honor rhythm: sow a little, "
            "then rest, rather than forcing constant output."
        )

    state.fallow_vow = (
        "In fruitless seasons, I will not condemn myself. I agree to treat these intervals "
        "as fallow fields â€” for rest, root-work, and quiet preparation â€” until it is time to sow again."
    )

    state.notes["next_sowing_hint"] = state.next_sowing_hint
    state.notes["fallow_vow"] = state.fallow_vow
    return state


# ---------------- Orchestrator ---------------- #

def run_the_fruitless_season_kernel(text: str) -> FruitlessSeasonState:
    """Run the full Fruitless Season fallow-field pipeline."""
    state = FruitlessSeasonState(raw_text=text)

    state = detect_fruitless_season(state)
    state = track_effort_and_exhaustion(state)
    state = reframe_fallow_field(state)
    state = hint_next_sowing(state)

    return state
