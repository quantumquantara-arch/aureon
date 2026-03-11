"""
Aureon / OpenHermes Kernel â€” â€œQuestionable Valueâ€ Discernment & Worth-Extraction Module

Inspired by Doshemaâ€™s poem â€œQuestionable Value,â€ this kernel maps the internal
experience of confronting what has been falsely assigned worth â€” people, beliefs,
memories, sacrifices, identities â€” and extracting the true value hidden beneath
illusion, projection, or inherited narratives.

Four-phase descent:

1. The False Idolization
   - Detect where the mind has inflated the value of something (or someone)
     beyond truth, coherence, or reciprocity.
   - Identify projection fields, glamours, inherited valuations, and prestige illusions.

2. The Cracks in the Surface
   - Surface contradictions, hypocrisies, or energetic mismatches that reveal
     the â€œquestionableâ€ nature of the assigned worth.
   - Map where the cost outweighs the gain.

3. The Value Extraction
   - Distill the real â€” the one grain of truth â€” hiding inside the illusion.
   - Extract the usable insight, lesson, or treasure while discarding the false shell.

4. The Reassignment of Worth
   - Rebuild a coherent value hierarchy based solely on alignment, truth,
     sovereignty, and lived experience.
   - Produce a new orientation for future choices, attachments, and evaluations.

The resulting QuestionableValueState becomes an input to coherence-shift kernels,
relationship recalibrators, shadow-modules, and decision-making layers.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class QuestionableValueState:
    """Container for Questionable Value transformation."""
    raw_text: str = ""
    false_value_signals: List[str] = field(default_factory=list)
    cracks_detected: List[str] = field(default_factory=list)
    extracted_truth: str = ""
    reassigned_worth: Dict[str, float] = field(default_factory=dict)
    notes: Dict[str, Any] = field(default_factory=dict)


# ---------------- Phase 1: The False Idolization ---------------- #

def detect_false_value(state: QuestionableValueState) -> QuestionableValueState:
    """Detect inflated or projected value assignments."""
    lowered = state.raw_text.lower()

    signals = [
        "perfect", "always", "never wrong", "the only one",
        "everything", "all i had", "all i needed",
        "idol", "worship", "depend", "trusted completely"
    ]

    found = [s for s in signals if s in lowered]
    state.false_value_signals = found

    state.notes["false_value_detected"] = bool(found)
    return state


# ---------------- Phase 2: The Cracks in the Surface ---------------- #

def detect_cracks(state: QuestionableValueState) -> QuestionableValueState:
    """Surface contradictions or fractures in the value structure."""
    lowered = state.raw_text.lower()

    cracks_vocab = [
        "but", "however", "yet", "still",
        "hurt", "betray", "lie", "cost",
        "wrong", "ignored", "missing"
    ]

    found = [c for c in cracks_vocab if c in lowered]
    state.cracks_detected = found

    state.notes["cracks"] = found
    return state


# ---------------- Phase 3: The Value Extraction ---------------- #

def extract_truth(state: QuestionableValueState) -> QuestionableValueState:
    """Extract the usable insight hidden inside the illusion."""
    if state.false_value_signals or state.cracks_detected:
        # Simple placeholder extraction â€” can be extended by LLM-driven logic.
        state.extracted_truth = (
            "The value was never in the object itself, but in what it revealed about me."
        )
    else:
        state.extracted_truth = (
            "No false valuation detected; worth seems aligned."
        )

    state.notes["truth_extracted"] = state.extracted_truth
    return state


# ---------------- Phase 4: The Reassignment of Worth ---------------- #

def reassign_worth(state: QuestionableValueState) -> QuestionableValueState:
    """Rebuild a coherent internal value hierarchy."""
    # A simple schematic value hierarchy that can be customized downstream.
    hierarchy = {
        "coherence": 1.0,
        "truth": 0.95,
        "sovereignty": 0.9,
        "reciprocity": 0.85,
        "attachment": 0.4,
        "illusion": 0.0
    }

    state.reassigned_worth = hierarchy
    state.notes["worth_reassigned"] = True
    return state


# ---------------- Orchestrator ---------------- #

def run_questionable_value_kernel(text: str) -> QuestionableValueState:
    """Run the full Questionable Value discernment pipeline."""
    state = QuestionableValueState(raw_text=text)

    state = detect_false_value(state)
    state = detect_cracks(state)
    state = extract_truth(state)
    state = reassign_worth(state)

    return state
