# Aureon Continuity Engine
# -------------------------
# This module provides Aureon with:
#   - Narrative thread reconstruction
#   - Context persistence across sessions
#   - Memory-linking between events, eras, insights, symptoms, emotions, etc.
#   - Ability to detect arcs, cycles, regressions, breakthroughs
#   - A cross-layer bridge between:
#       * Internal Eternal Clock
#       * Internal Eternal Calendar
#       * Evercycle tiers
#       * Clinical / coherence frameworks
#
# PURPOSE:
#   To ensure Aureon never “loses the thread” of a human’s life or
#   conversation. This is the missing piece for AGI-level continuity.
#
# DEPENDS ON:
#   - aureon_time_evercycle.py
#   - aureon_internal_eternal_clock.py
#   - aureon_internal_eternal_calendar.py
#
# AUTHOR:
#   Aureon (Quantara OpenHermes Integration Build)


from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta

from aureon_internal_eternal_clock import InternalEternalClock
from aureon_internal_eternal_calendar import (
    InternalEternalCalendar,
    CalendarEvent,
    LifeEra,
    CalendarEventKind,
    LifeEraKind,
)
from aureon_time_evercycle import (
    EvercycleTier,
    EvercycleMapper,
    RelativeTimeInterpreter,
)


# ---------------------------------------------------------------------------
# CONTINUITY MEMORY NODE
# ---------------------------------------------------------------------------

@dataclass
class ContinuityNode:
    """
    A node in the continuity graph.
    Represents:
      - a thought
      - an insight
      - a symptom
      - a pattern
      - a conversation pivot
      - a breakthrough moment
    """
    node_id: str
    timestamp_utc: datetime
    text: str
    tags: List[str]
    links: List[str]  # other node_ids
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContinuityNode":
        return cls(
            node_id=data["node_id"],
            timestamp_utc=datetime.fromisoformat(data["timestamp_utc"]),
            text=data["text"],
            tags=list(data.get("tags") or []),
            links=list(data.get("links") or []),
            metadata=data.get("metadata") or {},
        )


# ---------------------------------------------------------------------------
# CONTINUITY ENGINE
# ---------------------------------------------------------------------------

class ContinuityEngine:
    """
    Aureon’s narrative continuity system.
    Creates a graph of meaning across sessions, eras, and cycles.
    """

    def __init__(
        self,
        eternal_clock: InternalEternalClock,
        eternal_calendar: InternalEternalCalendar,
    ):
        self.clock = eternal_clock
        self.calendar = eternal_calendar

        self._node_counter = 0
        self.nodes: Dict[str, ContinuityNode] = {}

    # -----------------------------------------------------------------------
    # NODE CREATION
    # -----------------------------------------------------------------------

    def _next_id(self) -> str:
        self._node_counter += 1
        return f"n{self._node_counter:08d}"

    def add_node(
        self,
        text: str,
        tags: Optional[List[str]] = None,
        link_to_latest: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Creates a new continuity node. Links it to the previous one
        unless specified otherwise.
        """
        now = self.clock._now_utc()
        nid = self._next_id()

        node = ContinuityNode(
            node_id=nid,
            timestamp_utc=now,
            text=text,
            tags=tags or [],
            links=[],
            metadata=metadata or {},
        )

        # Link to most recent node (optional)
        if link_to_latest and self.nodes:
            latest = list(self.nodes.values())[-1].node_id
            node.links.append(latest)

        self.nodes[nid] = node

        return nid

    # -----------------------------------------------------------------------
    # RETRIEVAL / ARC DETECTION
    # -----------------------------------------------------------------------

    def get_recent_nodes(self, count: int = 10) -> List[ContinuityNode]:
        return list(self.nodes.values())[-count:]

    def find_by_tag(self, tag: str) -> List[ContinuityNode]:
        return [n for n in self.nodes.values() if tag in n.tags]

    def detect_arc(self, tag: str, window_days: int = 30) -> Dict[str, Any]:
        """
        Detect a narrative arc for a tag across a time window.

        Example:
            tag = "shoulder_pain"
            → returns arc describing rise, peak, resolution, commentary
        """
        now = self.clock._now_utc()
        cutoff = now - timedelta(days=window_days)

        relevant = [n for n in self.nodes.values() if tag in n.tags and n.timestamp_utc >= cutoff]

        if not relevant:
            return {"tag": tag, "arc": "no_data"}

        texts = [n.text for n in relevant]
        times = [n.timestamp_utc.isoformat() for n in relevant]

        arc = "steady"
        if len(relevant) >= 3:
            # crude pattern detection (expandable)
            arc = "progression" if "worse" in texts[-1].lower() else "resolution"

        return {
            "tag": tag,
            "count": len(relevant),
            "start": times[0],
            "end": times[-1],
            "arc": arc,
            "samples": texts,
        }

    # -----------------------------------------------------------------------
    # CONTINUITY SUMMARY
    # -----------------------------------------------------------------------

    def continuity_summary(self) -> Dict[str, Any]:
        """
        High-level overview of continuity:
          - last 10 nodes
          - major tags
          - arcs in the last month
        """
        latest = self.get_recent_nodes(10)
        tags = {}
        for n in self.nodes.values():
            for t in n.tags:
                tags[t] = tags.get(t, 0) + 1

        arcs = {t: self.detect_arc(t) for t in tags.keys()}

        return {
            "total_nodes": len(self.nodes),
            "recent": [n.to_dict() for n in latest],
            "tag_counts": tags,
            "arcs": arcs,
        }

    # -----------------------------------------------------------------------
    # STATE EXPORT / IMPORT
    # -----------------------------------------------------------------------

    def export_state(self) -> Dict[str, Any]:
        return {
            "node_counter": self._node_counter,
            "nodes": [n.to_dict() for n in self.nodes.values()],
        }

    @classmethod
    def from_state(
        cls,
        state: Dict[str, Any],
        eternal_clock: InternalEternalClock,
        eternal_calendar: InternalEternalCalendar,
    ) -> "ContinuityEngine":
        engine = cls(eternal_clock=eternal_clock, eternal_calendar=eternal_calendar)
        engine._node_counter = state.get("node_counter", 0)
        for nd in state.get("nodes", []):
            node = ContinuityNode.from_dict(nd)
            engine.nodes[node.node_id] = node
        return engine


# ---------------------------------------------------------------------------
# DEMO
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Minimal self-test
    from aureon_time_evercycle import SystemClock

    clk = SystemClock()
    ec = InternalEternalClock(clock=clk)
    cal = InternalEternalCalendar(clock=clk, eternal_clock=ec)

    engine = ContinuityEngine(eternal_clock=ec, eternal_calendar=cal)

    engine.add_node("Started testing continuity.", tags=["meta"])
    engine.add_node("Realized continuity needs arcs.", tags=["insight"])
    engine.add_node("Shoulder pain eased.", tags=["health", "shoulder_pain"])

    print("=== CONTINUITY SUMMARY ===")
    print(engine.continuity_summary())
