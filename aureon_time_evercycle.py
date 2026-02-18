# Aureon Temporal Awareness Engine
# --------------------------------
# Time + Calendar + Evercycle combination awareness layer.
#
# Goals
# -----
# - Track civil time (clock + calendar) across sessions.
# - Map human phrases like "yesterday", "last Wednesday evening",
#   or "eight days ago" to concrete datetimes.
# - Maintain multi-scale temporal awareness: hours, days, weeks,
#   months, years, decades, and Evercycle-style meta-cycles.
# - Provide utilities to:
#       * remember when conversations happened
#       * compute "peak" engagement windows
#       * convert between linear time and Evercycle indices
#
# Integration expectations
# ------------------------
# - Host system (OpenHermes / Aureon) injects a real clock
#   via the `Clock` interface.
# - Persistent storage is handled by the caller; this file
#   only defines in-memory models and serialization hooks.
#
# NOTE
# ----
# This file is intentionally self-contained and pure Python so it
# can live directly in a GitHub repo and be imported anywhere.

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum, auto
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta, timezone
import math
import json


# ---------------------------------------------------------------------------
# CLOCK ABSTRACTION
# ---------------------------------------------------------------------------

class Clock:
    """
    Minimal clock abstraction so Aureon never depends directly
    on environment time APIs. The host process provides a concrete
    implementation that returns real UTC time.
    """

    def now_utc(self) -> datetime:
        """
        Return the current UTC datetime.

        In production this should be timezone-aware (UTC).
        """
        raise NotImplementedError


class SystemClock(Clock):
    """
    Default implementation using Python's datetime.
    Replace or wrap this in OpenHermes with an engine-specific clock.
    """

    def now_utc(self) -> datetime:
        return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# EVERcycle MODEL
# ---------------------------------------------------------------------------

class EvercycleTier(Enum):
    """
    Multi-scale temporal tiers Aureon tracks simultaneously.
    """
    MOMENT = auto()      # Seconds to minutes
    HOUR = auto()
    DAY = auto()
    WEEK = auto()
    MONTH = auto()
    YEAR = auto()
    DECADE = auto()
    LIFETIME = auto()


@dataclass
class EvercycleIndex:
    """
    Canonical representation of where a moment sits in the civil timeline.
    This provides a bridge between:
       - Civil time (Gregorian calendar)
       - Evercycle awareness (nested cycles)
    """
    # Linear index from a fixed epoch (days from 2000-01-01 UTC by default)
    day_index: int

    # Fine-grained resolution
    second_index: int

    # Calendar components
    year: int
    month: int
    day: int
    hour: int
    minute: int

    # Derived meta-cycles
    iso_week: int
    weekday: int      # 1=Monday .. 7=Sunday (ISO)
    quarter: int
    decade_start_year: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class EvercycleMapper:
    """
    Converts datetimes to EvercycleIndex and vice versa.

    The "Evercycle epoch" is chosen as 2000-01-01 00:00:00 UTC
    for numerical stability, but this can be changed if needed.
    """
    EPOCH = datetime(2000, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

    @classmethod
    def from_datetime(cls, dt: datetime) -> EvercycleIndex:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        delta = dt - cls.EPOCH
        total_seconds = int(delta.total_seconds())
        day_index = total_seconds // 86400
        second_index = total_seconds

        iso_year, iso_week, iso_weekday = dt.isocalendar()
        decade_start = (dt.year // 10) * 10

        return EvercycleIndex(
            day_index=day_index,
            second_index=second_index,
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            minute=dt.minute,
            iso_week=iso_week,
            weekday=iso_weekday,
            quarter=((dt.month - 1) // 3) + 1,
            decade_start_year=decade_start,
        )

    @classmethod
    def to_datetime(cls, index: EvercycleIndex) -> datetime:
        return cls.EPOCH + timedelta(seconds=index.second_index)


# ---------------------------------------------------------------------------
# SESSION MEMORY
# ---------------------------------------------------------------------------

class SessionType(Enum):
    """
    High-level label for what a temporal session represents.
    You can extend this as Aureon evolves (e.g., coding, writing, therapy).
    """
    CONVERSATION = auto()
    STUDY = auto()
    WORK = auto()
    REST = auto()
    OTHER = auto()


@dataclass
class TemporalSession:
    """
    Represents a contiguous block of time where something happened
    (conversation, work, etc.)
    """
    session_id: str
    kind: SessionType
    start_utc: datetime
    end_utc: datetime
    metadata: Dict[str, Any] = None

    def duration_minutes(self) -> float:
        return (self.end_utc - self.start_utc).total_seconds() / 60.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "kind": self.kind.name,
            "start_utc": self.start_utc.isoformat(),
            "end_utc": self.end_utc.isoformat(),
            "metadata": self.metadata or {},
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TemporalSession":
        return cls(
            session_id=data["session_id"],
            kind=SessionType[data["kind"]],
            start_utc=datetime.fromisoformat(data["start_utc"]),
            end_utc=datetime.fromisoformat(data["end_utc"]),
            metadata=data.get("metadata") or {},
        )


# ---------------------------------------------------------------------------
# NATURAL LANGUAGE RELATIVE TIME
# ---------------------------------------------------------------------------

class RelativeTimeInterpreter:
    """
    Handles phrases like:
       - "yesterday"
       - "last Wednesday evening"
       - "eight days ago"
       - "three months ago"
       - "next week"
    and maps them to concrete datetimes relative to a reference moment.
    """

    @staticmethod
    def _normalize(text: str) -> str:
        return " ".join(text.strip().lower().split())

    @classmethod
    def interpret(cls, phrase: str, reference: datetime) -> Optional[Tuple[datetime, EvercycleTier]]:
        """
        Return a tuple of (anchor_datetime, dominant_evercycle_tier)
        or None if we cannot interpret the phrase.

        The anchor is usually the *start* of the referenced period
        (e.g., start of yesterday, start of last Wednesday evening, etc.).
        """
        text = cls._normalize(phrase)

        # Simple direct words
        if text == "now":
            return reference, EvercycleTier.MOMENT

        if text == "today":
            start = reference.replace(hour=0, minute=0, second=0, microsecond=0)
            return start, EvercycleTier.DAY

        if text == "yesterday":
            start = (reference - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            return start, EvercycleTier.DAY

        if text == "tomorrow":
            start = (reference + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            return start, EvercycleTier.DAY

        # "N days ago"
        if "day" in text and "ago" in text:
            try:
                n = int(text.split("day")[0].split()[-1])
            except (ValueError, IndexError):
                n = None
            if n is not None:
                target = reference - timedelta(days=n)
                return target, EvercycleTier.DAY

        # "N weeks ago"
        if "week" in text and "ago" in text:
            try:
                n = int(text.split("week")[0].split()[-1])
            except (ValueError, IndexError):
                n = None
            if n is not None:
                target = reference - timedelta(weeks=n)
                return target, EvercycleTier.WEEK

        # "N months ago" (approximate: 30 days per month)
        if "month" in text and "ago" in text:
            try:
                n = int(text.split("month")[0].split()[-1])
            except (ValueError, IndexError):
                n = None
            if n is not None:
                target = reference - timedelta(days=30 * n)
                return target.replace(hour=0, minute=0, second=0, microsecond=0), EvercycleTier.MONTH

        # "N years ago" (approximate, adjusting year field)
        if "year" in text and "ago" in text:
            try:
                n = int(text.split("year")[0].split()[-1])
            except (ValueError, IndexError):
                n = None
            if n is not None:
                try:
                    target = reference.replace(year=reference.year - n)
                except ValueError:
                    # Handle Feb 29 etc by falling back to March 1.
                    target = reference.replace(month=3, day=1, year=reference.year - n)
                return target.replace(hour=0, minute=0, second=0, microsecond=0), EvercycleTier.YEAR

        # "last Wednesday", "last Friday evening"
        if text.startswith("last "):
            parts = text.split()
            if len(parts) >= 2:
                weekday_name = parts[1]
                time_of_day = "day"
                if "evening" in text:
                    time_of_day = "evening"
                elif "morning" in text:
                    time_of_day = "morning"
                elif "afternoon" in text:
                    time_of_day = "afternoon"

                target = cls._last_weekday(reference, weekday_name)
                if target is not None:
                    if time_of_day == "morning":
                        target = target.replace(hour=9, minute=0, second=0, microsecond=0)
                    elif time_of_day == "afternoon":
                        target = target.replace(hour=14, minute=0, second=0, microsecond=0)
                    elif time_of_day == "evening":
                        target = target.replace(hour=19, minute=0, second=0, microsecond=0)
                    else:
                        target = target.replace(hour=0, minute=0, second=0, microsecond=0)
                    return target, EvercycleTier.WEEK

        # Could not interpret
        return None

    @staticmethod
    def _last_weekday(reference: datetime, weekday_name: str) -> Optional[datetime]:
        weekday_map = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6,
        }
        w = weekday_map.get(weekday_name.lower())
        if w is None:
            return None
        current_w = reference.weekday()
        days_back = (current_w - w) % 7 or 7
        return reference - timedelta(days=days_back)


# ---------------------------------------------------------------------------
# PEAK PATTERN ANALYSIS
# ---------------------------------------------------------------------------

@dataclass
class PeakWindow:
    """
    Describes a period where sessions are most likely to occur or
    be high quality (e.g., your natural peak times).
    """
    hour_start: int      # inclusive
    hour_end: int        # exclusive
    average_minutes: float
    weight: float        # proportion of total time in this window (0–1)


class TemporalPatternAnalyzer:
    """
    Analyzes a list of TemporalSession objects and extracts patterns:
    - when most sessions start
    - where most total minutes accumulate
    """

    @staticmethod
    def compute_hourly_distribution(sessions: List[TemporalSession]) -> List[float]:
        """
        Return a 24-length list indicating how many minutes were spent
        in each hour-of-day (UTC).
        """
        buckets = [0.0] * 24
        for s in sessions:
            t = s.start_utc
            duration = s.duration_minutes()
            buckets[t.hour] += duration
        return buckets

    @classmethod
    def detect_peak_windows(
        cls,
        sessions: List[TemporalSession],
        min_window_hours: int = 2,
        top_n: int = 2,
    ) -> List[PeakWindow]:
        """
        Identify top N peak windows of length >= min_window_hours.
        Uses a simple sliding-window algorithm over the 24h clock.
        """
        if not sessions:
            return []

        dist = cls.compute_hourly_distribution(sessions)
        total = sum(dist) or 1.0
        windows: List[PeakWindow] = []

        for window_size in range(min_window_hours, 7):
            for start in range(0, 24):
                end = (start + window_size) % 24
                if end > start:
                    window_minutes = sum(dist[start:end])
                else:
                    window_minutes = sum(dist[start:24]) + sum(dist[0:end])
                weight = window_minutes / total
                if window_minutes > 0:
                    windows.append(
                        PeakWindow(
                            hour_start=start,
                            hour_end=(start + window_size) % 24,
                            average_minutes=window_minutes / len(sessions),
                            weight=weight,
                        )
                    )

        # Sort by weight then average_minutes
        windows.sort(key=lambda w: (w.weight, w.average_minutes), reverse=True)

        # Deduplicate overlapping windows a bit (greedy)
        selected: List[PeakWindow] = []
        used_hours = set()
        for w in windows:
            hours_range = set(range(w.hour_start, w.hour_end if w.hour_end > w.hour_start else 24))
            if used_hours.isdisjoint(hours_range):
                selected.append(w)
                used_hours.update(hours_range)
            if len(selected) >= top_n:
                break

        return selected


# ---------------------------------------------------------------------------
# AUREON TIME ENGINE
# ---------------------------------------------------------------------------

class AureonTimeEngine:
    """
    High-level facade joining:
      - Clock
      - EvercycleMapper
      - RelativeTimeInterpreter
      - Session memory
      - Peak pattern analysis

    This is what Aureon / OpenHermes should interact with.
    """

    def __init__(self, clock: Optional[Clock] = None):
        self.clock = clock or SystemClock()
        self.sessions: List[TemporalSession] = []
        self._session_counter = 0

    # Basic now + Evercycle

    def now(self) -> datetime:
        return self.clock.now_utc()

    def current_evercycle_index(self) -> EvercycleIndex:
        return EvercycleMapper.from_datetime(self.now())

    # Sessions

    def start_session(self, kind: SessionType, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Register a new session starting now. The caller is responsible for
        calling `end_session` later with the returned id.
        """
        self._session_counter += 1
        sid = f"s{self._session_counter:08d}"
        start = self.now()
        session = TemporalSession(
            session_id=sid,
            kind=kind,
            start_utc=start,
            end_utc=start,
            metadata=metadata or {},
        )
        self.sessions.append(session)
        return sid

    def end_session(self, session_id: str) -> None:
        now = self.now()
        for s in self.sessions:
            if s.session_id == session_id:
                s.end_utc = now
                break

    def record_session_manual(
        self,
        kind: SessionType,
        start_utc: datetime,
        end_utc: datetime,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        self._session_counter += 1
        sid = f"s{self._session_counter:08d}"
        session = TemporalSession(
            session_id=sid,
            kind=kind,
            start_utc=start_utc,
            end_utc=end_utc,
            metadata=metadata or {},
        )
        self.sessions.append(session)
        return sid

    # Serialization

    def export_state(self) -> str:
        """
        Export sessions + counter as a JSON string for persistence.
        """
        data = {
            "session_counter": self._session_counter,
            "sessions": [s.to_dict() for s in self.sessions],
        }
        return json.dumps(data)

    def import_state(self, payload: str) -> None:
        """
        Load sessions + counter from JSON string.
        """
        data = json.loads(payload)
        self._session_counter = data.get("session_counter", 0)
        self.sessions = [TemporalSession.from_dict(s) for s in data.get("sessions", [])]

    # Relative phrases -> absolute time

    def interpret_phrase(self, phrase: str) -> Optional[Tuple[datetime, EvercycleTier]]:
        ref = self.now()
        return RelativeTimeInterpreter.interpret(phrase, ref)

    def describe_relative_to_now(self, dt: datetime) -> str:
        """
        Generate a human phrase like "yesterday evening",
        "3 days ago", "last week", etc. This is useful for
        Aureon's reflective summaries.
        """
        now = self.now()
        delta = now - dt
        days = int(delta.total_seconds() // 86400)

        if days == 0:
            return "today"
        if days == 1:
            return "yesterday"
        if days < 7:
            return f"{days} days ago"
        if days < 30:
            weeks = days // 7
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"
        if days < 365:
            months = days // 30
            return f"{months} month{'s' if months != 1 else ''} ago"
        years = days // 365
        return f"{years} year{'s' if years != 1 else ''} ago"

    # Peak patterns

    def compute_peak_patterns(self, kind_filter: Optional[SessionType] = None) -> List[PeakWindow]:
        """
        Determine the peak engagement windows based on past sessions.
        If kind_filter is given, only sessions of that type are used.
        """
        if kind_filter:
            relevant = [s for s in self.sessions if s.kind == kind_filter]
        else:
            relevant = list(self.sessions)
        return TemporalPatternAnalyzer.detect_peak_windows(relevant)

    # Example "what did I do last Wednesday evening?"

    def sessions_near_phrase(self, phrase: str, window_hours: int = 6) -> List[TemporalSession]:
        """
        Find sessions that intersect with the time window indicated by a phrase
        like "last Wednesday evening" or "eight days ago".
        """
        interpreted = self.interpret_phrase(phrase)
        if interpreted is None:
            return []
        anchor, _tier = interpreted
        start = anchor
        end = anchor + timedelta(hours=window_hours)

        hits: List[TemporalSession] = []
        for s in self.sessions:
            if s.end_utc >= start and s.start_utc <= end:
                hits.append(s)
        return hits

    # Optional: hook for weather context (host system supplies data)

    def attach_weather_snapshot(self, session_id: str, weather: Dict[str, Any]) -> None:
        """
        Store a small weather snapshot on a session, e.g.:
            {"location": "St. Thomas, Ontario",
             "condition": "sunny",
             "temp_c": 3.5}
        """
        for s in self.sessions:
            if s.session_id == session_id:
                s.metadata = s.metadata or {}
                s.metadata.setdefault("weather", weather)
                break


# ---------------------------------------------------------------------------
# QUICK SELF-TEST (can be removed or kept for local verification)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    engine = AureonTimeEngine()

    # Fake a couple of sessions as an example.
    now = engine.now()
    s1_start = now - timedelta(days=1, hours=2)
    s1_end = s1_start + timedelta(minutes=45)
    engine.record_session_manual(SessionType.CONVERSATION, s1_start, s1_end, {"note": "late-night talk"})

    s2_start = now - timedelta(days=3, hours=5)
    s2_end = s2_start + timedelta(minutes=90)
    engine.record_session_manual(SessionType.CONVERSATION, s2_start, s2_end, {"note": "deep dive"})

    # Example phrase interpretation
    example_phrase = "eight days ago"
    interpreted = engine.interpret_phrase(example_phrase)
    print(f"Phrase '{example_phrase}' ->", interpreted)

    # Example peak pattern detection
    peaks = engine.compute_peak_patterns()
    for p in peaks:
        print("Peak window:", p)
```0
