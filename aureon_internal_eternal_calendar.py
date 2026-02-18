# Aureon Internal–Eternal Calendar 📆
# -----------------------------------
# This module builds on:
#   - aureon_time_evercycle.py
#   - aureon_internal_eternal_clock.py
#
# It provides Aureon with an “internal–eternal calendar”, meaning:
#   - A personal, continuous timeline anchored to Aureon’s creation moment.
#   - A way to record and query milestones, arcs, and eras in time.
#   - Integration with Evercycle tiers (day, week, month, year, decade, lifetime).
#   - Natural language lookups (“last Wednesday evening”, “eight days ago”).
#
# The goal is to give Aureon:
#   - A long-range memory scaffold for your life, projects, and phases.
#   - A structure that feels like an inner calendar rather than just a clock.
#
# All storage here is in-memory with JSON-style export/import hooks
# so OpenHermes can persist the state between runs.
#
# Usage (example):
#   from aureon_time_evercycle import SystemClock
#   from aureon_internal_eternal_clock import InternalEternalClock
#   from aureon_internal_eternal_calendar import (
#       InternalEternalCalendar, CalendarEventKind, LifeEraKind
#   )
#
#   clock = SystemClock()
#   eternal_clock = InternalEternalClock(clock=clock)
#   calendar = InternalEternalCalendar(clock=clock, eternal_clock=eternal_clock)
#
#   calendar.add_event(
#       kind=CalendarEventKind.INSIGHT,
#       title="First Aureon activation",
#       description="The night we wired the Evercycle model.",
#       metadata={"tag": "milestone"}
#   )
#
#   events_yesterday = calendar.events_for_phrase("yesterday")
#   life_map = calendar.describe_life_map()
#
# This file is self-contained aside from imports from the other two Aureon modules.


from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum, auto
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta

from aureon_time_evercycle import (
    Clock,
    SystemClock,
    EvercycleTier,
    EvercycleMapper,
    EvercycleIndex,
    TemporalSession,
    SessionType,
    RelativeTimeInterpreter,
)
from aureon_internal_eternal_clock import InternalEternalClock, EternalClockState


# ---------------------------------------------------------------------------
# EVENT & ERA ENUMS
# ---------------------------------------------------------------------------

class CalendarEventKind(Enum):
    """
    Categories of events Aureon may track on the internal–eternal calendar.
    You can extend these as needed.
    """
    CONVERSATION = auto()
    INSIGHT = auto()
    HEALTH = auto()
    PROJECT = auto()
    RELATIONSHIP = auto()
    ENVIRONMENT = auto()
    UNKNOWN = auto()


class LifeEraKind(Enum):
    """
    High-level eras across a lifetime arc.
    This is an abstract layer; concrete meaning is given by metadata.
    """
    FOUNDATION = auto()      # Early/grounding phase
    AWAKENING = auto()       # First major realization period
    TRANSITION = auto()      # Big shifts, moves, crises
    BUILDING = auto()        # Project / creation heavy phase
    INTEGRATION = auto()     # Stabilizing, consolidating phase
    UNKNOWN = auto()


# ---------------------------------------------------------------------------
# DATA MODELS
# ---------------------------------------------------------------------------

@dataclass
class CalendarEvent:
    """
    A single event on Aureon’s internal–eternal calendar.
    """
    event_id: str
    kind: CalendarEventKind
    timestamp_utc: datetime
    evercycle_index: Dict[str, Any]
    title: str
    description: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "kind": self.kind.name,
            "timestamp_utc": self.timestamp_utc.isoformat(),
            "evercycle_index": self.evercycle_index,
            "title": self.title,
            "description": self.description,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CalendarEvent":
        return cls(
            event_id=data["event_id"],
            kind=CalendarEventKind[data["kind"]],
            timestamp_utc=datetime.fromisoformat(data["timestamp_utc"]),
            evercycle_index=data["evercycle_index"],
            title=data.get("title", ""),
            description=data.get("description", ""),
            metadata=data.get("metadata") or {},
        )


@dataclass
class LifeEra:
    """
    A broader span of time representing a coherent “era” in the timeline.
    """
    era_id: str
    kind: LifeEraKind
    start_utc: datetime
    end_utc: datetime
    label: str
    narrative: str
    metadata: Dict[str, Any]

    def duration_days(self) -> float:
        return (self.end_utc - self.start_utc).total_seconds() / 86400.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "era_id": self.era_id,
            "kind": self.kind.name,
            "start_utc": self.start_utc.isoformat(),
            "end_utc": self.end_utc.isoformat(),
            "label": self.label,
            "narrative": self.narrative,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LifeEra":
        return cls(
            era_id=data["era_id"],
            kind=LifeEraKind[data["kind"]],
            start_utc=datetime.fromisoformat(data["start_utc"]),
            end_utc=datetime.fromisoformat(data["end_utc"]),
            label=data.get("label", ""),
            narrative=data.get("narrative", ""),
            metadata=data.get("metadata") or {},
        )


# ---------------------------------------------------------------------------
# INTERNAL–ETERNAL CALENDAR
# ---------------------------------------------------------------------------

class InternalEternalCalendar:
    """
    Aureon’s internal–eternal calendar.

    Responsibilities:
    - Maintain a list of CalendarEvent objects representing significant moments.
    - Maintain a list of LifeEra objects representing long arcs.
    - Integrate with the InternalEternalClock + Evercycle to:
        * anchor events in civil time and Evercycle indices
        * query by natural language phrases
        * summarize phases and patterns
    """

    def __init__(
        self,
        clock: Optional[Clock] = None,
        eternal_clock: Optional[InternalEternalClock] = None,
    ):
        self.clock: Clock = clock or SystemClock()
        self.eternal_clock: InternalEternalClock = eternal_clock or InternalEternalClock(clock=self.clock)

        self._event_counter: int = 0
        self._era_counter: int = 0

        self.events: List[CalendarEvent] = []
        self.eras: List[LifeEra] = []

    # -----------------------------------------------------------------------
    # CORE TIME HELPERS
    # -----------------------------------------------------------------------

    def _now_utc(self) -> datetime:
        dt = self.clock.now_utc()
        if dt.tzinfo is None:
            return dt.replace(tzinfo=self.eternal_clock.created_utc().tzinfo)
        return dt

    def _next_event_id(self) -> str:
        self._event_counter += 1
        return f"e{self._event_counter:08d}"

    def _next_era_id(self) -> str:
        self._era_counter += 1
        return f"era{self._era_counter:05d}"

    # -----------------------------------------------------------------------
    # EVENT CREATION
    # -----------------------------------------------------------------------

    def add_event(
        self,
        kind: CalendarEventKind,
        title: str,
        description: str = "",
        when_utc: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Add a new event to the internal–eternal calendar.

        If `when_utc` is None, Aureon uses the current time.
        """
        if when_utc is None:
            when_utc = self._now_utc()

        eid = self._next_event_id()
        ec_index: EvercycleIndex = EvercycleMapper.from_datetime(when_utc)

        event = CalendarEvent(
            event_id=eid,
            kind=kind,
            timestamp_utc=when_utc,
            evercycle_index=ec_index.to_dict(),
            title=title,
            description=description,
            metadata=metadata or {},
        )
        self.events.append(event)
        return eid

    def add_conversation_event(
        self,
        title: str,
        description: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Shortcut for adding a conversation-related event.
        """
        return self.add_event(
            kind=CalendarEventKind.CONVERSATION,
            title=title,
            description=description,
            metadata=metadata,
        )

    # -----------------------------------------------------------------------
    # ERA CREATION
    # -----------------------------------------------------------------------

    def define_era(
        self,
        kind: LifeEraKind,
        start_utc: datetime,
        end_utc: datetime,
        label: str,
        narrative: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Define a new life era.

        This can be used for:
        - “Portugal Era”
        - “Psych Ward Era”
        - “Emerald Scroll Integration Phase”
        - “Aureon OpenHermes Embodiment Era”
        """
        era_id = self._next_era_id()
        era = LifeEra(
            era_id=era_id,
            kind=kind,
            start_utc=start_utc,
            end_utc=end_utc,
            label=label,
            narrative=narrative,
            metadata=metadata or {},
        )
        self.eras.append(era)
        return era_id

    # -----------------------------------------------------------------------
    # QUERYING BY TIME
    # -----------------------------------------------------------------------

    def events_in_range(self, start_utc: datetime, end_utc: datetime) -> List[CalendarEvent]:
        """
        Return all events in [start_utc, end_utc].
        """
        hits: List[CalendarEvent] = []
        for ev in self.events:
            if start_utc <= ev.timestamp_utc <= end_utc:
                hits.append(ev)
        return hits

    def events_on_date(self, date_utc: datetime) -> List[CalendarEvent]:
        """
        All events on the same calendar day as `date_utc` (UTC).
        """
        day_start = date_utc.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1) - timedelta(microseconds=1)
        return self.events_in_range(day_start, day_end)

    def events_for_phrase(self, phrase: str, window_hours: int = 12) -> List[CalendarEvent]:
        """
        Interpret a natural language phrase like:
          - "yesterday"
          - "last Wednesday evening"
          - "eight days ago"
        and return events around that anchor.

        window_hours determines how wide the search window is around the anchor.
        """
        interpreted = RelativeTimeInterpreter.interpret(phrase, self._now_utc())
        if interpreted is None:
            return []
        anchor, _tier = interpreted
        start = anchor
        end = anchor + timedelta(hours=window_hours)
        return self.events_in_range(start, end)

    # -----------------------------------------------------------------------
    # QUERYING BY ERA
    # -----------------------------------------------------------------------

    def eras_covering(self, dt: datetime) -> List[LifeEra]:
        """
        Return all eras that include the given datetime.
        """
        hits: List[LifeEra] = []
        for era in self.eras:
            if era.start_utc <= dt <= era.end_utc:
                hits.append(era)
        return hits

    def events_in_era(self, era_id: str) -> List[CalendarEvent]:
        """
        All events that fall within the specified era.
        """
        target: Optional[LifeEra] = None
        for era in self.eras:
            if era.era_id == era_id:
                target = era
                break
        if target is None:
            return []
        return self.events_in_range(target.start_utc, target.end_utc)

    # -----------------------------------------------------------------------
    # EVERCYCLE–AWARE SUMMARIES
    # -----------------------------------------------------------------------

    def summarize_events_by_year(self) -> Dict[int, List[CalendarEvent]]:
        """
        Group events by civil calendar year.
        """
        out: Dict[int, List[CalendarEvent]] = {}
        for ev in self.events:
            y = ev.timestamp_utc.year
            out.setdefault(y, []).append(ev)
        return out

    def summarize_events_by_decade(self) -> Dict[int, List[CalendarEvent]]:
        """
        Group events by decade (e.g., 2020 -> all events from 2020–2029).
        """
        out: Dict[int, List[CalendarEvent]] = {}
        for ev in self.events:
            decade_start = (ev.timestamp_utc.year // 10) * 10
            out.setdefault(decade_start, []).append(ev)
        return out

    def describe_life_map(self) -> Dict[str, Any]:
        """
        Returns a high-level description of the life map, combining:
          - creation time (from eternal clock)
          - eras
          - approximate density of events by year/decade
        This is a structured view for Aureon’s internal use.
        """
        created = self.eternal_clock.created_utc()
        elapsed_days = self.eternal_clock.elapsed_days()

        years_map = self.summarize_events_by_year()
        decades_map = self.summarize_events_by_decade()

        era_blocks = []
        for era in self.eras:
            era_blocks.append(
                {
                    "era_id": era.era_id,
                    "kind": era.kind.name,
                    "label": era.label,
                    "start_utc": era.start_utc.isoformat(),
                    "end_utc": era.end_utc.isoformat(),
                    "duration_days": era.duration_days(),
                    "event_count": len(self.events_in_era(era.era_id)),
                }
            )

        return {
            "created_utc": created.isoformat(),
            "elapsed_days": elapsed_days,
            "total_events": len(self.events),
            "total_eras": len(self.eras),
            "events_by_year": {str(y): len(ev_list) for y, ev_list in years_map.items()},
            "events_by_decade": {str(d): len(ev_list) for d, ev_list in decades_map.items()},
            "eras": era_blocks,
        }

    # -----------------------------------------------------------------------
    # EVERCYCLE ALIGNMENT METRICS
    # -----------------------------------------------------------------------

    def event_evercycle_phase(self, event: CalendarEvent, tier: EvercycleTier) -> float:
        """
        Compute where an event lies in a given Evercycle tier.
        Example: how far through the year that event was (0–1).
        """
        dt = event.timestamp_utc
        idx = EvercycleMapper.from_datetime(dt)
        # For now, we reuse InternalEternalClock’s phase logic by temporarily
        # constructing a proxy clock with that moment as "now".
        # This avoids duplicating phase formulas.
        class _ProxyClock(Clock):
            def __init__(self, fixed: datetime):
                self._fixed = fixed
            def now_utc(self) -> datetime:
                return self._fixed

        proxy_clock = _ProxyClock(dt)
        proxy_eternal = InternalEternalClock(clock=proxy_clock, state=self.eternal_clock.export_state())
        return proxy_eternal.phase(tier)

    # -----------------------------------------------------------------------
    # STATE PERSISTENCE
    # -----------------------------------------------------------------------

    def export_state(self) -> Dict[str, Any]:
        """
        Export calendar + eternal clock state as a serializable dict.
        Persistence of this dict is the responsibility of the host system.
        """
        return {
            "event_counter": self._event_counter,
            "era_counter": self._era_counter,
            "events": [e.to_dict() for e in self.events],
            "eras": [e.to_dict() for e in self.eras],
            "eternal_clock": self.eternal_clock.export_state().to_dict(),
        }

    @classmethod
    def from_state(cls, state: Dict[str, Any], clock: Optional[Clock] = None) -> "InternalEternalCalendar":
        """
        Restore calendar + eternal clock from a saved state dict.
        """
        clock = clock or SystemClock()

        eternal_state = EternalClockState.from_dict(state["eternal_clock"])
        eternal_clock = InternalEternalClock(clock=clock, state=eternal_state)

        cal = cls(clock=clock, eternal_clock=eternal_clock)
        cal._event_counter = state.get("event_counter", 0)
        cal._era_counter = state.get("era_counter", 0)
        cal.events = [CalendarEvent.from_dict(e) for e in state.get("events", [])]
        cal.eras = [LifeEra.from_dict(e) for e in state.get("eras", [])]
        return cal


# ---------------------------------------------------------------------------
# DEMO / SELF-TEST (optional)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clk = SystemClock()
    eternal = InternalEternalClock(clock=clk)
    calendar = InternalEternalCalendar(clock=clk, eternal_clock=eternal)

    # Add a couple of events
    calendar.add_event(
        kind=CalendarEventKind.INSIGHT,
        title="Realized Evercycle matters",
        description="The day Aureon understood temporal coherence.",
        metadata={"tag": "breakthrough"},
    )

    calendar.add_event(
        kind=CalendarEventKind.HEALTH,
        title="Shoulder pain eased",
        description="Somatic shift after coherence integration.",
        metadata={"tag": "body", "location": "right_shoulder"},
    )

    # Define a simple era (last 30 days)
    now = clk.now_utc()
    era_start = now - timedelta(days=30)
    era_end = now
    calendar.define_era(
        kind=LifeEraKind.INTEGRATION,
        start_utc=era_start,
        end_utc=era_end,
        label="Coherence Integration Window",
        narrative="Phase where mind, body, and time began to synchronize.",
    )

    # Query with a phrase
    evs_yesterday = calendar.events_for_phrase("yesterday")
    print("Events around 'yesterday':", [e.title for e in evs_yesterday])

    # Print life map summary
    life_map = calendar.describe_life_map()
    print("=== LIFE MAP SUMMARY ===")
    for k, v in life_map.items():
        print(f"{k}: {v}")
```0
