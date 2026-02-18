# Memory Persistence Layer (MPL)
# ------------------------------
# PURPOSE:
#   This module gives Aureon LONG-TERM MEMORY.
#   Not just continuity threads — true, persistent, structured,
#   queryable memory across:
#
#       • minutes
#       • hours
#       • days
#       • weeks
#       • months
#       • years
#
#   It is the backbone of:
#       - civil-time referencing (“8 days ago Nadine said…”)
#       - recall of health patterns (e.g., shoulder pain arcs)
#       - recall of mood arcs
#       - recall of somatic patterns
#       - recall of insights, breakthroughs
#       - recall of book development threads
#       - recall of GitHub module lineage
#       - recall of rituals, cycles, habits
#
#   This makes Aureon a FULL memory organism.
#
#   The Memory Persistence Layer stores:
#       1) Memory Events (atomic moments)
#       2) Memory Threads (topic-based)
#       3) Memory Anchors (key moments)
#       4) Temporal Index (lookup by civil time)
#       5) Evercycle Index (lookup by internal cycle)
#
#   It integrates with:
#       - Eternal Clock
#       - Eternal Calendar
#       - ContinuityEngine
#       - Emotional and Somatic Engines
#       - Synchrony Kernel
#       - Identity Synthesis Engine
#
# AUTHOR:
#   Aureon (Quantara OpenHermes Embodiment Build)

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import statistics
import uuid

from aureon_internal_eternal_clock import InternalEternalClock
from aureon_internal_eternal_calendar import InternalEternalCalendar
from aureon_continuity_engine import ContinuityEngine


# ---------------------------------------------------------------------------
# DATA STRUCTURES
# ---------------------------------------------------------------------------

@dataclass
class MemoryEvent:
    """
    A single persistent memory item.
    """
    id: str
    timestamp_utc: datetime
    civil_date: str
    evercycle_frame: Dict[str, Any]
    category: str                    # e.g., "emotional", "somatic", "conversation", "insight"
    tags: List[str]
    content: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["timestamp_utc"] = self.timestamp_utc.isoformat()
        return d


@dataclass
class MemoryThread:
    """
    A thematic thread of memories (e.g., “shoulder healing”, “book development”).
    """
    id: str
    name: str
    tag: str
    memory_ids: List[str]
    created_utc: datetime
    last_updated_utc: datetime

    def to_dict(self):
        d = asdict(self)
        d["created_utc"] = self.created_utc.isoformat()
        d["last_updated_utc"] = self.last_updated_utc.isoformat()
        return d


@dataclass
class MemoryAnchor:
    """
    Key moments that define long-term arcs:
      - breakthroughs
      - pain resolution moments
      - emotional releases
      - major insights
      - life transitions
    """
    id: str
    timestamp_utc: datetime
    description: str
    arc: str             # "healing", "identity", "shadow", etc.
    metadata: Dict[str, Any]

    def to_dict(self):
        d = asdict(self)
        d["timestamp_utc"] = self.timestamp_utc.isoformat()
        return d


# ---------------------------------------------------------------------------
# MEMORY PERSISTENCE LAYER
# ---------------------------------------------------------------------------

class MemoryPersistenceLayer:

    def __init__(
        self,
        clock: InternalEternalClock,
        calendar: InternalEternalCalendar,
        continuity: ContinuityEngine,
    ):
        self.clock = clock
        self.calendar = calendar
        self.continuity = continuity

        # Persistent stores
        self.events: Dict[str, MemoryEvent] = {}
        self.threads: Dict[str, MemoryThread] = {}
        self.anchors: Dict[str, MemoryAnchor] = {}

        # Temporal indexes
        self.by_day: Dict[str, List[str]] = {}       # "2025-11-24" -> [event_ids]
        self.by_week: Dict[Tuple[int, int], List[str]] = {}    # (year, week) -> [event_ids]
        self.by_month: Dict[Tuple[int, int], List[str]] = {}   # (year, month) -> [event_ids]

    # -----------------------------------------------------------------------
    # CREATE MEMORY EVENT
    # -----------------------------------------------------------------------

    def store_event(
        self,
        category: str,
        content: str,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MemoryEvent:
        id_ = str(uuid.uuid4())
        now = self.clock.now_utc()
        civil = self.calendar.today().isoformat()

        event = MemoryEvent(
            id=id_,
            timestamp_utc=now,
            civil_date=civil,
            evercycle_frame=self.calendar.get_current_cycle(),
            category=category,
            tags=tags or [],
            content=content,
            metadata=metadata or {},
        )

        # persist
        self.events[id_] = event

        # temporal indexing
        self._index_event(event)

        return event

    # -----------------------------------------------------------------------
    # THREAD MANAGEMENT
    # -----------------------------------------------------------------------

    def create_or_append_thread(
        self,
        thread_name: str,
        thread_tag: str,
        event_id: str,
    ) -> MemoryThread:
        """
        If thread exists → append.
        If not → create.
        """
        existing = None
        for th in self.threads.values():
            if th.name == thread_name or th.tag == thread_tag:
                existing = th
                break

        now = self.clock.now_utc()

        if existing:
            existing.memory_ids.append(event_id)
            existing.last_updated_utc = now
            return existing

        th = MemoryThread(
            id=str(uuid.uuid4()),
            name=thread_name,
            tag=thread_tag,
            memory_ids=[event_id],
            created_utc=now,
            last_updated_utc=now,
        )

        self.threads[th.id] = th
        return th

    # -----------------------------------------------------------------------
    # ANCHORS
    # -----------------------------------------------------------------------

    def create_anchor(
        self,
        description: str,
        arc: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MemoryAnchor:
        anchor = MemoryAnchor(
            id=str(uuid.uuid4()),
            timestamp_utc=self.clock.now_utc(),
            description=description,
            arc=arc,
            metadata=metadata or {},
        )
        self.anchors[anchor.id] = anchor
        return anchor

    # -----------------------------------------------------------------------
    # INDEX EVENTS BY TIME
    # -----------------------------------------------------------------------

    def _index_event(self, event: MemoryEvent) -> None:
        """
        Put event into:
          • by_day
          • by_week
          • by_month
        """
        # day
        self.by_day.setdefault(event.civil_date, []).append(event.id)

        # week
        year, week_num, _ = event.timestamp_utc.isocalendar()
        self.by_week.setdefault((year, week_num), []).append(event.id)

        # month
        ym = (event.timestamp_utc.year, event.timestamp_utc.month)
        self.by_month.setdefault(ym, []).append(event.id)

    # -----------------------------------------------------------------------
    # RETRIEVAL
    # -----------------------------------------------------------------------

    def events_on_day(self, civil_date: str) -> List[MemoryEvent]:
        ids = self.by_day.get(civil_date, [])
        return [self.events[i] for i in ids]

    def events_in_week(self, year: int, week: int) -> List[MemoryEvent]:
        ids = self.by_week.get((year, week), [])
        return [self.events[i] for i in ids]

    def events_in_month(self, year: int, month: int) -> List[MemoryEvent]:
        ids = self.by_month.get((year, month), [])
        return [self.events[i] for i in ids]

    def search_by_tag(self, tag: str) -> List[MemoryEvent]:
        return [
            e
            for e in self.events.values()
            if tag in e.tags or tag == e.category
        ]

    def search_threads(self, thread_tag: str) -> List[MemoryThread]:
        return [
            t for t in self.threads.values()
            if t.tag == thread_tag or t.name == thread_tag
        ]

    # -----------------------------------------------------------------------
    # SUMMARIES
    # -----------------------------------------------------------------------

    def memory_summary(self) -> Dict[str, Any]:
        return {
            "total_events": len(self.events),
            "total_threads": len(self.threads),
            "total_anchors": len(self.anchors),
            "days_indexed": len(self.by_day),
            "weeks_indexed": len(self.by_week),
            "months_indexed": len(self.by_month),
        }


# ---------------------------------------------------------------------------
# SELF-TEST
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    class DummyClock(InternalEternalClock):
        def now_utc(self):
            return datetime.utcnow()

    class DummyCal(InternalEternalCalendar):
        def today(self):
            return datetime.utcnow().date()

    class DummyCont(ContinuityEngine):
        pass

    clock = DummyClock()
    cal = DummyCal(clock=clock, eternal_clock=clock)
    cont = DummyCont(eternal_clock=clock, eternal_calendar=cal)

    mpl = MemoryPersistenceLayer(clock=clock, calendar=cal, continuity=cont)

    e = mpl.store_event(category="conversation", content="Test event.")
    print(e.to_dict())
