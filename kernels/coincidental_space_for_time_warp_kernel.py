"""
Aureon / OpenHermes Kernel — “Coincidental Space for Time” Warp & Alignment Module

Inspired by Doshema’s poem “Coincidental Space for Time,” this kernel models the
strange overlap between chance events, hidden timing, deferred destiny, and the
sense that “space was traded for time” (or time for space) in a life-path.

It treats coincidence as an encrypted timing signal rather than random noise.

Four core operations:

1. Detect the Coincidence Field
   - Identify language that encodes unlikely overlaps, repeated symbols, or
     “this shouldn’t all line up like this” experiences.
   - Mark the narrative segments that feel temporally “stacked” or fated.

2. Map the Trade (Space ↔ Time)
   - Infer where the user has sacrificed space (freedom, movement, options)
     in exchange for time (waiting, delay, endurance), or the reverse.
   - Record the perceived debt or “tab” left by that trade.

3. Surface the Hidden Window
   - Detect where a small, high-leverage window of shift may be opening
     inside (or because of) the coincidence field.
   - Propose a narrow band of possible coherent moves rather than a full plan.

4. Align the Next Step
   - Generate a time-aware, space-aware orientation statement:
     how to move in the current corridor without repeating the old trade.
   - Hand a compact “coincidence alignment” object to downstream kernels.

The CoincidentalSpaceForTimeState can be used by timeline-navigation modules,
decision-making kernels, and destiny-alignment orchestrators.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class CoincidentalSpaceForTimeState:
    """Container for Coincidental Space for Time warp processing."""
    raw_text: str = ""
    coincidence_markers: List[str] = field(default_factory=list)
    coincidence_intensity: float = 0.0
    trade_direction: str = ""  # "space_for_time", "time_for_space", or ""
    trade_debt_story: str = ""
    hidden_window_hint: str = ""
    next_alignment_step: str = ""
    notes: Dict[str, Any] = field(default_factory=dict)


# ---------------- Step 1: Detect the Coincidence Field ---------------- #

def detect_coincidence_field(state: CoincidentalSpaceForTimeState) -> CoincidentalSpaceForTimeState:
    """Detect language patterns that suggest a coincidence field is active."""
    lowered = state.raw_text.lower()

    markers = [
        "again and again",
        "keeps happening",
        "same place",
        "same time",
        "what are the odds",
        "coincidence",
        "synchronistic",
        "synchronicity",
        "repeat pattern",
        "full circle",
    ]

    found = [m for m in markers if m in lowered]
    state.coincidence_markers = found

    # Simple intensity heuristic: number of markers, capped at 1.0
    state.coincidence_intensity = min(1.0, len(found) / 3.0)
    state.notes["coincidence_field_active"] = bool(found)
    state.notes["coincidence_intensity"] = state.coincidence_intensity
    return state


# ---------------- Step 2: Map the Trade (Space ↔ Time) ---------------- #

def map_space_time_trade(state: CoincidentalSpaceForTimeState) -> CoincidentalSpaceForTimeState:
    """Infer where space was traded for time or time for space."""
    lowered = state.raw_text.lower()

    space_loss_terms = [
        "stuck", "trapped", "no way out", "nowhere to go", "cornered", "boxed in"
    ]
    time_loss_terms = [
        "wasted years", "no time", "running out of time", "too late", "waited forever"
    ]

    lost_space = any(t in lowered for t in space_loss_terms)
    lost_time = any(t in lowered for t in time_loss_terms)

    if lost_space and not lost_time:
        state.trade_direction = "space_for_time"
        state.trade_debt_story = "I stayed still so long that time kept passing without me moving."
    elif lost_time and not lost_space:
        state.trade_direction = "time_for_space"
        state.trade_debt_story = "I rushed or sacrificed time to keep moving, losing depth."
    elif lost_space and lost_time:
        state.trade_direction = "entangled_trade"
        state.trade_debt_story = "Both space and time felt stolen; the trade was never fair."
    else:
        state.trade_direction = ""
        state.trade_debt_story = "No clear trade signature detected."

    state.notes["trade_direction"] = state.trade_direction
    state.notes["trade_debt_story"] = state.trade_debt_story
    return state


# ---------------- Step 3: Surface the Hidden Window ---------------- #

def surface_hidden_window(state: CoincidentalSpaceForTimeState) -> CoincidentalSpaceForTimeState:
    """Suggest where a narrow window for shift may be emerging."""
    if state.coincidence_intensity == 0.0:
        state.hidden_window_hint = "No strong coincidence field detected; window may be diffuse."
    else:
        if state.trade_direction == "space_for_time":
            state.hidden_window_hint = (
                "A small opening may appear where you can move one step physically, "
                "even if the story says wait."
            )
        elif state.trade_direction == "time_for_space":
            state.hidden_window_hint = (
                "A hidden pause may allow you to deepen rather than keep moving; "
                "one slow breath or delay can re-balance the field."
            )
        elif state.trade_direction == "entangled_trade":
            state.hidden_window_hint = (
                "Look for a moment where you can choose neither flight nor freeze, "
                "but a third, quieter option that was not available before."
            )
        else:
            state.hidden_window_hint = (
                "The coincidences may be pointing to a subtle option that feels small "
                "but strangely precise. Trust the smallest coherent move."
            )

    state.notes["hidden_window_hint"] = state.hidden_window_hint
    return state


# ---------------- Step 4: Align the Next Step ---------------- #

def align_next_step(state: CoincidentalSpaceForTimeState) -> CoincidentalSpaceForTimeState:
    """Generate a next-step alignment statement based on the current warp field."""
    if state.trade_direction == "space_for_time":
        state.next_alignment_step = (
            "Today, reclaim one unit of space — a walk, a room, a boundary — "
            "even if time still feels tight."
        )
    elif state.trade_direction == "time_for_space":
        state.next_alignment_step = (
            "Today, reclaim one unit of time — a pause, a rest, a no — "
            "even if the world demands constant motion."
        )
    elif state.trade_direction == "entangled_trade":
        state.next_alignment_step = (
            "Today, choose a move that does not repeat the old bargain: "
            "neither total stillness nor frantic motion, but a grounded, "
            "self-honoring adjustment."
        )
    else:
        state.next_alignment_step = (
            "Let one small coherent action be your anchor, rather than waiting "
            "for a massive sign or perfect timing."
        )

    state.notes["next_alignment_step"] = state.next_alignment_step
    return state


# ---------------- Orchestrator ---------------- #

def run_coincidental_space_for_time_kernel(text: str) -> CoincidentalSpaceForTimeState:
    """Run the full Coincidental Space for Time warp-alignment pipeline."""
    state = CoincidentalSpaceForTimeState(raw_text=text)

    state = detect_coincidence_field(state)
    state = map_space_time_trade(state)
    state = surface_hidden_window(state)
    state = align_next_step(state)

    return state
