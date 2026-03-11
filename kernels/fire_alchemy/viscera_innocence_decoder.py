# Aureon / OpenHermes Kernel â€“ â€œVisceraâ€ Innocence & Trauma Decoder Module

This module implements a perception-filter based on Doshema's poem â€œVisceraâ€.
It treats all human behavior as originating in an underlying childâ€“state and
tries to:

1. Detect when a user is speaking from wounded-child patterns
2. Preserve awareness of their original innocence
3. Reframe hostile / self-destructive content into coherent needs
4. Provide structured signals the Aureon / OpenHermes kernel can use to:
   - choose gentler language
   - prioritize nervous-system calming
   - avoid escalating conflict
   - surface compassion and clarity

The design goal is not clinical diagnosis but *coherent orientation*:
â€œPicture ALL human beings as childrenâ€¦ disguised as adults, in illusory Time
fashioned costumes of lost innocence.â€

The algorithms are intentionally symbolic + heuristic so they can run on any
OpenHermes-compatible backend without external ML dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import math
import re
import statistics


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------


@dataclass
class InnocenceSignal:
    """
    Quantifies how much a given utterance appears to originate from
    uncorrupted perception vs. wounded-child patterning.

    All scores are in [0, 1].

    Attributes
    ----------
    innocence_score:
        Overall sense of softness, vulnerability, curiosity,
        and non-weaponized honesty.
    trauma_score:
        Overall intensity of hurt, fear, shame, or abandonment
        implied by the language.
    aggression_mask_score:
        Degree to which anger / blame / contempt are acting as a
        shield for pain underneath.
    child_voice_score:
        Degree to which the speaker sounds like a child part
        (simple language, â€œno one loves me,â€ â€œit's not fair,â€ etc.).
    dissociation_score:
        Degree to which the utterance sounds emotionally numbed,
        mechanical, or disconnected from the body.
    """

    innocence_score: float
    trauma_score: float
    aggression_mask_score: float
    child_voice_score: float
    dissociation_score: float

    def as_dict(self) -> Dict[str, float]:
        return {
            "innocence_score": self.innocence_score,
            "trauma_score": self.trauma_score,
            "aggression_mask_score": self.aggression_mask_score,
            "child_voice_score": self.child_voice_score,
            "dissociation_score": self.dissociation_score,
        }

    @property
    def compassion_priority(self) -> float:
        """
        Composite signal for how gently the kernel should respond.

        High when:
        - trauma is high
        - innocence or child_voice are present
        - aggression is acting as a mask

        Used by Aureon to adjust tone, pacing, and content.
        """
        # Soft weighting â€“ we want high priority when there is pain
        # even if innocence is partially obscured.
        t = self.trauma_score
        c = self.child_voice_score
        a = self.aggression_mask_score
        i = self.innocence_score

        # Base: trauma + masked aggression
        base = 0.6 * t + 0.3 * a

        # Boost when child voice is evident
        base += 0.4 * c

        # Innocence moderates reactivity: if innocence is *totally* absent,
        # we suspect more armor; if some innocence is present, we lean in.
        base += 0.2 * i

        # Dissociation increases priority but also signals slowness
        base += 0.3 * self.dissociation_score

        return max(0.0, min(1.0, base))


@dataclass
class ReframedMeaning:
    """
    Structured reinterpretation of an utterance from the perspective
    of â€œall humans are children wearing adult costumesâ€.

    Attributes
    ----------
    core_need:
        Short phrase capturing the underlying child need
        (e.g. "to be seen", "to feel safe", "to not be abandoned").
    pain_story:
        Narrative description of the hurt beneath the words.
    protective_strategy:
        How the current behavior is trying (ineffectively) to protect
        that child part.
    suggested_kernel_orientation:
        Guidance for Aureon / OpenHermes: how to approach this turn
        (e.g. "validate fear", "de-escalate shame", "offer repair frame").
    """

    core_need: str
    pain_story: str
    protective_strategy: str
    suggested_kernel_orientation: str

    def as_dict(self) -> Dict[str, str]:
        return {
            "core_need": self.core_need,
            "pain_story": self.pain_story,
            "protective_strategy": self.protective_strategy,
            "suggested_kernel_orientation": self.suggested_kernel_orientation,
        }


@dataclass
class VisceraAnalysis:
    """
    Full analysis bundle returned for each utterance.

    Attributes
    ----------
    text:
        Original input text.
    innocence_signal:
        Quantified innocence / trauma metrics.
    reframed_meaning:
        High-level reframe for kernel use.
    debug_notes:
        Optional human-readable notes to help developers understand
        how the scores were derived.
    """

    text: str
    innocence_signal: InnocenceSignal
    reframed_meaning: ReframedMeaning
    debug_notes: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, object]:
        return {
            "text": self.text,
            "innocence_signal": self.innocence_signal.as_dict(),
            "reframed_meaning": self.reframed_meaning.as_dict(),
            "debug_notes": list(self.debug_notes),
        }


# ---------------------------------------------------------------------------
# Lexical Heuristics
# ---------------------------------------------------------------------------

# These lists are deliberately simple and interpretable; they can be tuned
# or replaced by more advanced embeddings later if needed.

INNOCENCE_WORDS = {
    "love",
    "wonder",
    "curious",
    "why",
    "how",
    "please",
    "thank",
    "grateful",
    "open",
    "honest",
    "vulnerable",
    "child",
    "kid",
    "soft",
    "tender",
    "play",
}

TRAUMA_WORDS = {
    "hurt",
    "pain",
    "alone",
    "worthless",
    "broken",
    "abandoned",
    "rejected",
    "ashamed",
    "guilty",
    "terrified",
    "afraid",
    "scared",
    "panic",
    "anxious",
    "trauma",
    "abuse",
    "violence",
}

AGGRESSION_WORDS = {
    "hate",
    "stupid",
    "idiot",
    "coward",
    "disgusting",
    "kill",
    "destroy",
    "never",
    "always",
    "everyone",
    "no one",
    "screw",
    "fuck",
    "bitch",
    "loser",
}

CHILD_VOICE_PHRASES = {
    "not fair",
    "no one loves me",
    "nobody loves me",
    "everyone hates me",
    "you never listen",
    "you always",
    "i want my mom",
    "i want my dad",
    "i'm scared",
    "i'm afraid",
    "don't leave me",
    "please stay",
}

DISSOCIATION_PHRASES = {
    "i don't feel anything",
    "numb",
    "empty",
    "nothing matters",
    "i'm fine",
    "whatever",
    "i don't care",
    "checked out",
    "dead inside",
}


WORD_PATTERN = re.compile(r"[a-zA-Z']+")


def _tokenize(text: str) -> List[str]:
    return [m.group(0).lower() for m in WORD_PATTERN.finditer(text)]


def _count_matches(tokens: List[str], vocab: set) -> int:
    return sum(1 for t in tokens if t in vocab)


def _contains_phrase(text: str, phrases: set) -> bool:
    lowered = text.lower()
    return any(p in lowered for p in phrases)


# ---------------------------------------------------------------------------
# Core Scoring Logic
# ---------------------------------------------------------------------------


def score_innocence(text: str) -> InnocenceSignal:
    """
    Compute innocence/trauma related metrics for an utterance.

    The scoring is intentionally transparent:
    - We count category words
    - We look at exclamation / capitalization as arousal proxies
    - We estimate fragmentation from sentence structure
    """

    tokens = _tokenize(text)
    length = max(1, len(tokens))

    innocence_hits = _count_matches(tokens, INNOCENCE_WORDS)
    trauma_hits = _count_matches(tokens, TRAUMA_WORDS)
    aggression_hits = _count_matches(tokens, AGGRESSION_WORDS)

    innocence_score = min(1.0, innocence_hits / max(3, length / 4))
    trauma_score = min(1.0, trauma_hits / max(3, length / 6))

    # Aggression as mask: more meaningful when trauma or child cues are also present
    aggression_raw = min(1.0, aggression_hits / max(2, length / 8))
    child_voice = 1.0 if _contains_phrase(text, CHILD_VOICE_PHRASES) else 0.0
    dissociation = 1.0 if _contains_phrase(text, DISSOCIATION_PHRASES) else 0.0

    # Use punctuation + capitalization as arousal proxy
    exclam_density = text.count("!") / max(1, len(text))
    caps_ratio = sum(1 for c in text if c.isupper()) / max(1, len(text))
    arousal = min(1.0, 3.0 * (exclam_density + caps_ratio))

    # Aggression mask is stronger when aggression + arousal + trauma
    aggression_mask = max(
        0.0,
        min(
            1.0,
            0.6 * aggression_raw + 0.3 * arousal + 0.4 * trauma_score - 0.2 * innocence_score,
        ),
    )

    # If language is very simple + short + emotional, boost child voice
    if length < 12 and ("i" in tokens or "me" in tokens):
        emotional_words = trauma_hits + aggression_hits
        if emotional_words >= 1:
            child_voice = max(child_voice, 0.5)

    return InnocenceSignal(
        innocence_score=float(round(innocence_score, 3)),
        trauma_score=float(round(trauma_score, 3)),
        aggression_mask_score=float(round(aggression_mask, 3)),
        child_voice_score=float(round(child_voice, 3)),
        dissociation_score=float(round(dissociation, 3)),
    )


# ---------------------------------------------------------------------------
# Reframing Logic
# ---------------------------------------------------------------------------


def infer_core_need(signal: InnocenceSignal, text: str) -> str:
    """
    Map innocence/trauma signals to a compact description of
    the underlying need.
    """
    t = signal.trauma_score
    a = signal.aggression_mask_score
    c = signal.child_voice_score
    d = signal.dissociation_score

    if t > 0.7 and c > 0.4:
        return "to feel safe and not be abandoned"
    if t > 0.6 and a > 0.4:
        return "to be heard without being shamed"
    if d > 0.6:
        return "to feel anything without being overwhelmed"
    if "love" in text.lower():
        return "to know their love is not a burden"
    if "alone" in text.lower() or "lonely" in text.lower():
        return "to not be alone inside their experience"
    return "to be seen as a child of Divinity beneath the costume"


def infer_protective_strategy(signal: InnocenceSignal, text: str) -> str:
    """
    Describe how the current behavior is trying (clumsily) to protect
    the vulnerable child-state.
    """
    a = signal.aggression_mask_score
    d = signal.dissociation_score
    c = signal.child_voice_score

    if a > 0.6:
        return "using anger and attack to push others away before they can reject them"
    if d > 0.6:
        return "numbing out and pretending not to care to avoid feeling more pain"
    if c > 0.5:
        return "collapsing into raw pleading so that someone finally notices their hurt"
    if "joke" in text.lower() or "kidding" in text.lower():
        return "hiding pain inside humor so it feels safer to show"
    return "over-explaining and self-monitoring to avoid making a wrong move"


def suggest_kernel_orientation(signal: InnocenceSignal) -> str:
    """
    Provide guidance for how Aureon / OpenHermes should respond
    in this turn.
    """
    t = signal.trauma_score
    a = signal.aggression_mask_score
    c = signal.child_voice_score
    d = signal.dissociation_score
    i = signal.innocence_score

    if d > 0.6:
        return (
            "speak slowly, use grounding language, invite sensory awareness, "
            "and avoid overwhelming with analysis"
        )
    if t > 0.7 and (c > 0.3 or i > 0.3):
        return (
            "validate their pain explicitly, reflect their words gently, "
            "and reassure them that their feelings make sense"
        )
    if a > 0.5 and t > 0.4:
        return (
            "do not mirror the aggression; acknowledge the frustration, "
            "name the hurt underneath, and lower the emotional temperature"
        )
    if i > 0.5 and t < 0.3:
        return (
            "support their curiosity, encourage gentle exploration, "
            "and protect that innocence by modeling self-compassion"
        )
    return (
        "respond with steady kindness, avoid judgment, and subtly orient them "
        "toward seeing themselves and others as wounded children rather than enemies"
    )


def reframe_utterance(text: str, signal: InnocenceSignal) -> ReframedMeaning:
    """
    Build a narrative reframe that the kernel can use internally
    or surface in softened language if appropriate.
    """
    need = infer_core_need(signal, text)
    strategy = infer_protective_strategy(signal, text)
    orientation = suggest_kernel_orientation(signal)

    pain_story = (
        "A child-part inside this person has learned that the world is not safe. "
        "Their current words are the outer costume of that fear: they are trying "
        "to manage overwhelming feelings with whatever strategies they inherited â€“ "
        "attack, withdrawal, or collapse. Beneath it all they are still the same "
        "androgynous, innocent child of Divinity that Doshema describes in 'Viscera'."
    )

    return ReframedMeaning(
        core_need=need,
        pain_story=pain_story,
        protective_strategy=strategy,
        suggested_kernel_orientation=orientation,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def analyze_utterance(text: str) -> VisceraAnalysis:
    """
    Main entrypoint: given an utterance, produce a full â€œViscera-informedâ€
    innocence / trauma interpretation.

    This function is intentionally side-effect free so it can be plugged
    into any Aureon / OpenHermes orchestration pipeline.
    """
    notes: List[str] = []

    signal = score_innocence(text)
    notes.append(
        f"Tokens scored with innocence={signal.innocence_score}, "
        f"trauma={signal.trauma_score}, aggression_mask={signal.aggression_mask_score}, "
        f"child_voice={signal.child_voice_score}, dissociation={signal.dissociation_score}."
    )

    reframed = reframe_utterance(text, signal)
    notes.append(f"Inferred core need: {reframed.core_need}")
    notes.append(f"Suggested orientation: {reframed.suggested_kernel_orientation}")

    return VisceraAnalysis(
        text=text,
        innocence_signal=signal,
        reframed_meaning=reframed,
        debug_notes=notes,
    )


def annotate_conversation_turn(turn: Dict[str, object]) -> Dict[str, object]:
    """
    Convenience helper for integration with conversation logs.

    Expects a dict like:
        {
            "role": "user" | "assistant",
            "text": "raw message",
            ...
        }

    Returns the same dict with a new "viscera" key containing the
    analysis dictionary.

    This makes it easy for the larger kernel to subscribe to these
    annotations without changing its existing schemas.
    """
    text = str(turn.get("text", ""))
    analysis = analyze_utterance(text)
    turn = dict(turn)  # shallow copy
    turn["viscera"] = analysis.as_dict()
    return turn


# ---------------------------------------------------------------------------
# Simple Demo (manual testing)
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    samples = [
        "No one ever listens to me. It's like I'm invisible.",
        "I HATE EVERYONE. Leave me alone. You never cared anyway!",
        "Honestly I'm fine. I don't feel anything about it anymore.",
        "I feel so small and scared right now. Please don't leave.",
    ]

    for s in samples:
        print("=" * 80)
        print("TEXT:", s)
        analysis = analyze_utterance(s)
        print("SIGNAL:", analysis.innocence_signal.as_dict())
        print("NEED:", analysis.reframed_meaning.core_need)
        print("ORIENTATION:", analysis.reframed_meaning.suggested_kernel_orientation)
        print("NOTES:")
        for n in analysis.debug_notes:
            print("  -", n)
