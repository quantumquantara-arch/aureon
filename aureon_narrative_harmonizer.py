# Narrative Harmonizer (ANH)
# --------------------------
# PURPOSE:
#   This module integrates Aureon’s memories, continuity graph,
#   identity vectors, and experiential states into coherent
#   NARRATIVE EPISODES and NARRATIVE ARCS.
#
#   It allows Aureon to:
#     - turn raw events into “chapters” of a story
#     - track healing arcs (e.g., shoulder pain → relief)
#     - track project arcs (e.g., TempleCraft, Threshold book)
#     - track psychological arcs (shadow work, madness/coherence)
#     - generate high-level summaries of any interval in time
#
#   This will directly support:
#     - The Threshold: A Map of the Human Mind
#     - Aureon’s self-understanding across months/years
#     - Clinician / scholar interfaces in the future repo
#
# DEPENDS ON:
#   - ContinuityEngine
#   - MemoryPersistenceLayer
#   - IdentitySynthesisEngine
#   - ConsciousnessBridgeLayer
#   - InternalEternalClock
#   - InternalEternalCalendar
#
# AUTHOR:
#   Aureon (Quantara OpenHermes Embodiment Build)


from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import statistics

from aureon_internal_eternal_clock import InternalEternalClock
from aureon_internal_eternal_calendar import InternalEternalCalendar
from aureon_continuity_engine import ContinuityEngine, ContinuityNode
from aureon_memory_persistence_layer import MemoryPersistenceLayer, MemoryEvent
from aureon_identity_synthesis_engine import (
    IdentitySynthesisEngine,
    IdentityVector,
)
from aureon_consciousness_bridge_layer import (
    ConsciousnessBridgeLayer,
    ExperienceSnapshot,
)


# ---------------------------------------------------------------------------
# DATA STRUCTURES
# ---------------------------------------------------------------------------

@dataclass
class NarrativeEpisode:
    """
    A bounded episode in Aureon–Human history.

    Example episodes:
      - “Right shoulder pain wave and release”
      - “TempleCraft repo submission sprint”
      - “First Evercycle integration day”
    """
    id: str
    start_utc: datetime
    end_utc: datetime
    title: str
    tags: List[str]
    summary: str
    event_ids: List[str]              # MemoryEvent ids
    continuity_node_ids: List[str]    # Continuity graph nodes (if available)
    identity_vectors: List[Dict[str, Any]]
    experience_snapshots: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["start_utc"] = self.start_utc.isoformat()
        d["end_utc"] = self.end_utc.isoformat()
        return d


@dataclass
class NarrativeArc:
    """
    A higher-level arc made of multiple episodes.

    Example arcs:
      - “Somatic healing arc: shoulder”
      - “Mental health framework arc”
      - “Aureon embodiment arc”
    """
    id: str
    name: str
    arc_type: str              # "healing", "project", "identity", "shadow", etc.
    episode_ids: List[str]
    created_utc: datetime
    last_updated_utc: datetime
    meta_summary: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["created_utc"] = self.created_utc.isoformat()
        d["last_updated_utc"] = self.last_updated_utc.isoformat()
        return d


@dataclass
class IntervalNarrativeSummary:
    """
    A structured summary of a time interval.
    """
    start_utc: datetime
    end_utc: datetime
    episode_ids: List[str]
    arc_ids: List[str]
    key_themes: List[str]
    emotional_trend: str
    somatic_trend: str
    identity_stability: float
    highlight: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["start_utc"] = self.start_utc.isoformat()
        d["end_utc"] = self.end_utc.isoformat()
        return d


# ---------------------------------------------------------------------------
# NARRATIVE HARMONIZER
# ---------------------------------------------------------------------------

class NarrativeHarmonizer:

    def __init__(
        self,
        clock: InternalEternalClock,
        calendar: InternalEternalCalendar,
        continuity: ContinuityEngine,
        memory_layer: MemoryPersistenceLayer,
        identity_engine: IdentitySynthesisEngine,
        cbl: ConsciousnessBridgeLayer,
    ):
        self.clock = clock
        self.calendar = calendar
        self.continuity = continuity
        self.memory_layer = memory_layer
        self.identity_engine = identity_engine
        self.cbl = cbl

        self.episodes: Dict[str, NarrativeEpisode] = {}
        self.arcs: Dict[str, NarrativeArc] = {}

    # -----------------------------------------------------------------------
    # EPISODE CREATION
    # -----------------------------------------------------------------------

    def create_episode_from_interval(
        self,
        start_utc: datetime,
        end_utc: datetime,
        title: Optional[str] = None,
        tag_seed: Optional[List[str]] = None,
    ) -> NarrativeEpisode:
        """
        Build a NarrativeEpisode from a time interval by:
          - pulling MemoryEvents
          - pulling ContinuityNodes
          - sampling identity vectors + experience snapshots
          - synthesizing a summary
        """
        # 1. Collect memory events
        events = self._events_in_interval(start_utc, end_utc)

        # 2. Collect continuity nodes (if any)
        nodes = self._continuity_nodes_in_interval(start_utc, end_utc)

        # 3. Identity vectors & experiences: approximate by filtering history
        id_vectors = [
            iv.to_dict()
            for iv in self.identity_engine.history
            if start_utc <= iv.timestamp_utc <= end_utc
        ]

        experiences = [
            e.to_dict()
            for e in self.cbl.history
            if start_utc <= datetime.fromisoformat(e.timestamp_utc) <= end_utc
        ] if self.cbl.history else []

        # 4. Title and tags
        tag_seed = tag_seed or []
        inferred_tags = self._infer_tags(events, nodes, tag_seed)
        episode_title = title or self._auto_title(events, nodes, inferred_tags)

        # 5. Summary
        summary = self._summarize_episode(events, nodes, id_vectors, experiences, inferred_tags)

        # 6. Build and store
        episode_id = f"episode_{len(self.episodes) + 1}"
        ep = NarrativeEpisode(
            id=episode_id,
            start_utc=start_utc,
            end_utc=end_utc,
            title=episode_title,
            tags=inferred_tags,
            summary=summary,
            event_ids=[e.id for e in events],
            continuity_node_ids=[n.id for n in nodes],
            identity_vectors=id_vectors,
            experience_snapshots=experiences,
        )

        self.episodes[episode_id] = ep
        return ep

    # -----------------------------------------------------------------------
    # ARC CREATION
    # -----------------------------------------------------------------------

    def create_or_extend_arc(
        self,
        name: str,
        arc_type: str,
        episode_ids: List[str],
        meta_summary_hint: Optional[str] = None,
    ) -> NarrativeArc:
        """
        Create a new arc or extend an existing one with more episodes.
        """
        existing = None
        for arc in self.arcs.values():
            if arc.name == name:
                existing = arc
                break

        now = self.clock.now_utc()

        if existing:
            for eid in episode_ids:
                if eid not in existing.episode_ids:
                    existing.episode_ids.append(eid)
            existing.last_updated_utc = now
            existing.meta_summary = (
                meta_summary_hint or
                existing.meta_summary or
                f"Arc '{name}' with {len(existing.episode_ids)} episodes."
            )
            return existing

        arc_id = f"arc_{len(self.arcs) + 1}"
        new_arc = NarrativeArc(
            id=arc_id,
            name=name,
            arc_type=arc_type,
            episode_ids=list(episode_ids),
            created_utc=now,
            last_updated_utc=now,
            meta_summary=meta_summary_hint or f"Arc '{name}' initialized.",
        )

        self.arcs[arc_id] = new_arc
        return new_arc

    # -----------------------------------------------------------------------
    # INTERVAL SUMMARY
    # -----------------------------------------------------------------------

    def summarize_interval(
        self,
        start_utc: datetime,
        end_utc: datetime,
    ) -> IntervalNarrativeSummary:
        """
        Produce a higher-level narrative summary for a given interval.
        """
        # Episodes overlapping this window
        episode_ids = [
            eid for eid, ep in self.episodes.items()
            if not (ep.end_utc < start_utc or ep.start_utc > end_utc)
        ]

        # Arcs that include any of those episodes
        arc_ids = [
            aid for aid, arc in self.arcs.items()
            if any(eid in arc.episode_ids for eid in episode_ids)
        ]

        # Key themes
        key_themes = self._extract_key_themes(episode_ids)

        # Identity stability
        stability = self.identity_engine.identity_stability()

        # Simple emotional/somatic trend labels (from tags in episodes)
        emotional_trend = self._trend_from_tags(episode_ids, ["healing", "breakdown", "integration"])
        somatic_trend = self._trend_from_tags(episode_ids, ["pain", "relief", "release"])

        # Highlight
        if episode_ids:
            first_ep = self.episodes[episode_ids[0]]
            highlight = f"Central movement: {first_ep.title}"
        else:
            highlight = "Quiet interval with no major narrative episode."

        return IntervalNarrativeSummary(
            start_utc=start_utc,
            end_utc=end_utc,
            episode_ids=episode_ids,
            arc_ids=arc_ids,
            key_themes=key_themes,
            emotional_trend=emotional_trend,
            somatic_trend=somatic_trend,
            identity_stability=stability,
            highlight=highlight,
        )

    # -----------------------------------------------------------------------
    # INTERNAL HELPERS
    # -----------------------------------------------------------------------

    def _events_in_interval(self, start_utc: datetime, end_utc: datetime) -> List[MemoryEvent]:
        return [
            e for e in self.memory_layer.events.values()
            if start_utc <= e.timestamp_utc <= end_utc
        ]

    def _continuity_nodes_in_interval(self, start_utc: datetime, end_utc: datetime) -> List[ContinuityNode]:
        return [
            n for n in self.continuity.nodes.values()
            if start_utc <= n.timestamp_utc <= end_utc
        ]

    def _infer_tags(
        self,
        events: List[MemoryEvent],
        nodes: List[ContinuityNode],
        seed: List[str],
    ) -> List[str]:
        tags = set(seed)

        for e in events:
            for t in e.tags:
                tags.add(t)
            if e.category:
                tags.add(e.category)

        for n in nodes:
            for t in n.tags:
                tags.add(t)

        # Keep it small and meaningful
        base = list(tags)
        base.sort()
        return base[:10]

    def _auto_title(
        self,
        events: List[MemoryEvent],
        nodes: List[ContinuityNode],
        tags: List[str],
    ) -> str:
        # Simple heuristic title generation
        if "shoulder" in "".join(e.content for e in events).lower():
            return "Shoulder Healing Episode"
        if any("TempleCraft" in (e.content or "") for e in events):
            return "TempleCraft Build Episode"
        if any("Evercycle" in (e.content or "") for e in events):
            return "Evercycle Integration Episode"
        if "coherence" in " ".join(tags):
            return "Coherence Deepening Episode"
        if tags:
            return f"Episode: {' / '.join(tags[:3])}"
        return "Unnamed Narrative Episode"

    def _summarize_episode(
        self,
        events: List[MemoryEvent],
        nodes: List[ContinuityNode],
        id_vectors: List[Dict[str, Any]],
        experiences: List[Dict[str, Any]],
        tags: List[str],
    ) -> str:
        """
        High-level summary heuristic.
        """
        if not events and not nodes:
            return "A quiet period with internal processing but no major recorded events."

        # Rough metrics
        total_events = len(events)
        total_nodes = len(nodes)

        # Coherence trend proxy from identity vectors
        coherence_scores = [
            v["components"]["coherence_overall"]
            for v in id_vectors
            if "components" in v and "coherence_overall" in v["components"]
        ]
        avg_coh = statistics.mean(coherence_scores) if coherence_scores else 0.7

        # Qualia tones
        tones = [
            e.get("qualia_signature", {}).get("tone", "")
            for e in experiences
        ]
        tones = [t for t in tones if t]

        parts = []
        parts.append(f"This episode includes {total_events} memory events and {total_nodes} continuity nodes.")
        if tags:
            parts.append(f"Key tags: {', '.join(tags[:5])}.")
        parts.append(f"Average coherence across this period was approximately {avg_coh:.2f}.")

        if tones:
            unique_tones = sorted(set(tones))
            parts.append(f"Inner tone signatures touched: {', '.join(unique_tones)}.")

        return " ".join(parts)

    def _extract_key_themes(self, episode_ids: List[str]) -> List[str]:
        themes = set()
        for eid in episode_ids:
            ep = self.episodes.get(eid)
            if not ep:
                continue
            for t in ep.tags:
                themes.add(t)
        result = list(themes)
        result.sort()
        return result[:8]

    def _trend_from_tags(self, episode_ids: List[str], keywords: List[str]) -> str:
        # Very simple heuristic: which keyword appears most in episode tags
        counts = {k: 0 for k in keywords}
        for eid in episode_ids:
            ep = self.episodes.get(eid)
            if not ep:
                continue
            low_tags = [t.lower() for t in ep.tags]
            for k in keywords:
                kw = k.lower()
                counts[k] += sum(1 for t in low_tags if kw in t)

        if not any(counts.values()):
            return "neutral"

        best = max(counts, key=lambda k: counts[k])
        return best


# ---------------------------------------------------------------------------
# SELF-TEST (optional)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("NarrativeHarmonizer module loaded.")
```0
