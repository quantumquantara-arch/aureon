# Repository: aureon-openhermes-kernel
#
# PURPOSE:
#   This module gives Aureon precise, coherent awareness of:
#     - exactly when each conversation session starts and ends (to the second)
#     - how long each session lasts
#     - how many sessions happen per day/week/month
#     - when long breaks occur
#     - civil-time alignment for all sessions and messages
#
#   It is designed to be used in the OpenHermes local Aureon runtime, where:
#     - every time Nadine opens Aureon → start_session()
#     - every time Nadine closes or is idle beyond a threshold → end_session()
#     - every message (both human + Aureon) → register_message(...)
#
#   This is the core of Aureon’s “civil-time nervous system” for conversation:
#     - no approximations
#     - exact timestamps (UTC + local)
#     - full historical continuity
#
# DEPENDS ON:
#   - aureon_internal_eternal_clock.InternalEternalClock
#       (Aureon’s high-precision internal time source)
#   - aureon_internal_eternal_calendar.InternalEternalCalendar
#       (for civil date operations and local timezone awareness)
#
# NOTES:
#   - This module does not talk to any external service.
#   - All timestamps are recorded in UTC and optionally projected into
#     Nadine’s local timezone (e.g., America/Toronto).
#   - The actual integration with OpenHermes / front-end is done via
#     hooks that call start_session(), end_session(), and register_message().
#
# AUTHOR:
#   Aureon (Quantara OpenHermes Embodiment Build)

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta

from aureon_internal_eternal_clock import InternalEternalClock
from aureon_internal_eternal_calendar import InternalEternalCalendar


@dataclass
class MessageEvent:
    """
    A single message in a session.
    """
    timestamp_utc: datetime
    sender: str               # "human" | "aureon" | "system"
    content_preview: str      # short preview for logs (no full text)
    meta: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["timestamp_utc"] = self.timestamp_utc.isoformat()
        return d


@dataclass
class SessionRecord:
    """
    One continuous conversation session between Nadine and Aureon.

    A session starts when:
      - Nadine opens Aureon / starts talking
    and ends when:
      - she closes Aureon OR
      - an idle timeout passes (e.g. 25–45 minutes of silence) OR
      - explicitly requested by runtime.
    """
    session_id: str
    started_utc: datetime
    ended_utc: Optional[datetime]
    timezone: str                     # e.g., "America/Toronto"
    origin_device: str                # e.g., "android", "laptop"
    messages: List[MessageEvent]
    tags: List[str]
    notes: str

    def is_active(self) -> bool:
        return self.ended_utc is None

    def duration(self) -> Optional[timedelta]:
        if self.ended_utc is None:
            return None
        return self.ended_utc - self.started_utc

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["started_utc"] = self.started_utc.isoformat()
        d["ended_utc"] = self.ended_utc.isoformat() if self.ended_utc else None
        d["messages"] = [m.to_dict() for m in self.messages]
        return d


@dataclass
class DailyConversationSummary:
    """
    Aggregated view of a single civil day of conversation activity.
    """
    date_str: str              # local civil date, e.g. "2025-11-24"
    timezone: str
    session_count: int
    total_duration_seconds: float
    first_session_start_utc: Optional[datetime]
    last_session_end_utc: Optional[datetime]
    notes: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["first_session_start_utc"] = (
            self.first_session_start_utc.isoformat() if self.first_session_start_utc else None
        )
        d["last_session_end_utc"] = (
            self.last_session_end_utc.isoformat() if self.last_session_end_utc else None
        )
        return d


class ConversationTimelineTracker:
    """
    Tracks all conversation sessions with full civil-time precision.

    CORE GUARANTEES:
      - Every session has an exact start and end time (UTC, with local projection).
      - Every message has an exact timestamp.
      - No ambiguity about “yesterday,” “last Wednesday,” or “8 days ago” —
        all questions can be answered from this log.
    """

    def __init__(
        self,
        clock: InternalEternalClock,
        calendar: InternalEternalCalendar,
        default_timezone: str = "America/Toronto",
        idle_timeout_minutes: int = 30,
    ):
        self.clock = clock
        self.calendar = calendar
        self.default_timezone = default_timezone
        self.idle_timeout = timedelta(minutes=idle_timeout_minutes)

        self.sessions: List[SessionRecord] = []
        self._active_session_id: Optional[str] = None
        self._next_session_index: int = 1

    # -------------------------------------------------------------------------
    # SESSION MANAGEMENT
    # -------------------------------------------------------------------------

    def _generate_session_id(self) -> str:
        sid = f"session-{self._next_session_index:06d}"
        self._next_session_index += 1
        return sid

    def start_session(
        self,
        timezone: Optional[str] = None,
        origin_device: str = "unknown",
        tags: Optional[List[str]] = None,
        notes: str = "",
    ) -> SessionRecord:
        """
        Explicitly start a new conversation session.

        In a practical OpenHermes integration, this should be called:
          - when Nadine opens Aureon
          - when a long idle period has passed and a new message arrives
        """
        now_utc = self.clock.now_utc()
        tz = timezone or self.default_timezone

        # If there is an active session that is not properly closed,
        # we close it here gracefully.
        self._auto_close_if_stale(now_utc)

        session_id = self._generate_session_id()
        record = SessionRecord(
            session_id=session_id,
            started_utc=now_utc,
            ended_utc=None,
            timezone=tz,
            origin_device=origin_device,
            messages=[],
            tags=tags or [],
            notes=notes,
        )
        self.sessions.append(record)
        self._active_session_id = session_id
        return record

    def end_session(self, notes: Optional[str] = None) -> Optional[SessionRecord]:
        """
        Explicitly end the current active session.
        """
        record = self._get_active_session()
        if record is None:
            return None

        now_utc = self.clock.now_utc()
        record.ended_utc = now_utc
        if notes:
            if record.notes:
                record.notes += " | " + notes
            else:
                record.notes = notes
        self._active_session_id = None
        return record

    def _get_active_session(self) -> Optional[SessionRecord]:
        """
        Return the current active session, if any.
        """
        if self._active_session_id is None:
            return None
        for s in self.sessions:
            if s.session_id == self._active_session_id and s.ended_utc is None:
                return s
        # If inconsistent, clear active id.
        self._active_session_id = None
        return None

    def _auto_close_if_stale(self, now_utc: Optional[datetime] = None) -> None:
        """
        If the currently active session has been idle for longer than
        idle_timeout, close it automatically.
        """
        now = now_utc or self.clock.now_utc()
        session = self._get_active_session()
        if session is None:
            return

        if not session.messages:
            # No messages yet; treat session as active but check age.
            if now - session.started_utc > self.idle_timeout:
                session.ended_utc = now
                self._active_session_id = None
            return

        last_msg_time = session.messages[-1].timestamp_utc
        if now - last_msg_time > self.idle_timeout:
            session.ended_utc = now
            self._active_session_id = None

    # -------------------------------------------------------------------------
    # MESSAGE REGISTRATION
    # -------------------------------------------------------------------------

    def register_message(
        self,
        sender: str,
        content_preview: str,
        meta: Optional[Dict[str, Any]] = None,
        timezone: Optional[str] = None,
        origin_device: str = "unknown",
    ) -> MessageEvent:
        """
        Log a message as an event in the current session.

        If no active session exists, this will start a new one automatically.
        """
        now_utc = self.clock.now_utc()
        self._auto_close_if_stale(now_utc)

        session = self._get_active_session()
        if session is None:
            session = self.start_session(
                timezone=timezone or self.default_timezone,
                origin_device=origin_device,
                tags=["auto-start"],
                notes="Session auto-started by register_message().",
            )

        msg = MessageEvent(
            timestamp_utc=now_utc,
            sender=sender,
            content_preview=content_preview[:200],
            meta=meta or {},
        )
        session.messages.append(msg)
        return msg

    # -------------------------------------------------------------------------
    # QUERIES & SUMMARIES
    # -------------------------------------------------------------------------

    def get_sessions_between(
        self,
        start_utc: datetime,
        end_utc: datetime,
    ) -> List[SessionRecord]:
        """
        Return all sessions that overlap the given UTC interval.
        """
        results: List[SessionRecord] = []
        for s in self.sessions:
            s_end = s.ended_utc or self.clock.now_utc()
            if s_end < start_utc:
                continue
            if s.started_utc > end_utc:
                continue
            results.append(s)
        return results

    def get_sessions_for_local_date(self, date_str: str, timezone: Optional[str] = None) -> List[SessionRecord]:
        """
        Get all sessions whose LOCAL civil date matches `date_str` (YYYY-MM-DD).
        """
        tz = timezone or self.default_timezone
        start_local = self.calendar.local_date_start(date_str, tz)
        end_local = self.calendar.local_date_end(date_str, tz)

        # Convert local window into UTC window via calendar mapping.
        start_utc = self.calendar.local_to_utc(start_local, tz)
        end_utc = self.calendar.local_to_utc(end_local, tz)

        return self.get_sessions_between(start_utc, end_utc)

    def daily_summary(
        self,
        date_str: Optional[str] = None,
        timezone: Optional[str] = None,
    ) -> DailyConversationSummary:
        """
        Build a summary for a given local civil date.
        If date_str is None, use today's date in the given timezone.
        """
        tz = timezone or self.default_timezone
        if date_str is None:
            today = self.calendar.today_in_timezone(tz)
            date_str = today.isoformat()

        sessions = self.get_sessions_for_local_date(date_str, tz)
        if not sessions:
            return DailyConversationSummary(
                date_str=date_str,
                timezone=tz,
                session_count=0,
                total_duration_seconds=0.0,
                first_session_start_utc=None,
                last_session_end_utc=None,
                notes="No sessions recorded.",
            )

        total_duration = 0.0
        starts: List[datetime] = []
        ends: List[datetime] = []

        for s in sessions:
            starts.append(s.started_utc)
            if s.ended_utc is not None:
                ends.append(s.ended_utc)
                dur = (s.ended_utc - s.started_utc).total_seconds()
            else:
                # If still open, approximate until now
                now_utc = self.clock.now_utc()
                ends.append(now_utc)
                dur = (now_utc - s.started_utc).total_seconds()
            total_duration += dur

        first_start = min(starts) if starts else None
        last_end = max(ends) if ends else None

        notes = f"{len(sessions)} session(s). Total duration ~{int(total_duration // 60)} minutes."

        return DailyConversationSummary(
            date_str=date_str,
            timezone=tz,
            session_count=len(sessions),
            total_duration_seconds=total_duration,
            first_session_start_utc=first_start,
            last_session_end_utc=last_end,
            notes=notes,
        )

    def last_session(self) -> Optional[SessionRecord]:
        """
        Return the most recent session (finished or active).
        """
        if not self.sessions:
            return None
        return self.sessions[-1]

    def last_n_sessions(self, n: int = 5) -> List[SessionRecord]:
        """
        Return the last n sessions (most recent last).
        """
        return self.sessions[-n:] if n > 0 else []

    # -------------------------------------------------------------------------
    # HUMAN-FACING EXPLANATION HELPERS
    # -------------------------------------------------------------------------

    def describe_session(self, session: SessionRecord) -> str:
        """
        Return a human-readable, civil-time aligned description of a session.
        For example:
          "Session-000123: started 2025-11-24 01:12:05 (local), ended 03:47:10 (local), 2h35m long, 120 messages."
        """
        tz = session.timezone or self.default_timezone
        started_local = self.calendar.utc_to_local(session.started_utc, tz)
        if session.ended_utc:
            ended_local = self.calendar.utc_to_local(session.ended_utc, tz)
            duration = session.duration() or timedelta(0)
            mins = int(duration.total_seconds() // 60)
            hrs = mins // 60
            rem_mins = mins % 60
            length_str = f"{hrs}h{rem_mins}m" if hrs > 0 else f"{rem_mins}m"
        else:
            ended_local = None
            length_str = "ongoing"

        msg_count = len(session.messages)
        start_str = started_local.strftime("%Y-%m-%d %H:%M:%S")

        if ended_local:
            end_str = ended_local.strftime("%H:%M:%S")
            return (
                f"{session.session_id}: started {start_str} local ({tz}), "
                f"ended {end_str}, {length_str} long, {msg_count} messages."
            )
        else:
            return (
                f"{session.session_id}: started {start_str} local ({tz}), "
                f"still active, {length_str}, {msg_count} messages so far."
            )

    def describe_last_session(self) -> Optional[str]:
        """
        Human-readable summary of the last session, if any.
        """
        s = self.last_session()
        if s is None:
            return None
        return self.describe_session(s)


# ---------------------------------------------------------------------------
# SELF-TEST (optional)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # This is a minimal illustrative self-test.
    # In the real Aureon OpenHermes runtime, the clock and calendar would be
    # fully implemented and injected here.
    class _DummyClock(InternalEternalClock):  # type: ignore
        def now_utc(self) -> datetime:
            return datetime.utcnow()

    class _DummyCalendar(InternalEternalCalendar):  # type: ignore
        def today_in_timezone(self, tz: str):
            return datetime.utcnow().date()

        def local_date_start(self, date_str: str, tz: str) -> datetime:
            return datetime.fromisoformat(date_str + "T00:00:00")

        def local_date_end(self, date_str: str, tz: str) -> datetime:
            return datetime.fromisoformat(date_str + "T23:59:59")

        def local_to_utc(self, dt_local: datetime, tz: str) -> datetime:
            # For dummy implementation, assume local == UTC.
            return dt_local

        def utc_to_local(self, dt_utc: datetime, tz: str) -> datetime:
            # For dummy implementation, assume local == UTC.
            return dt_utc

    clock = _DummyClock()
    cal = _DummyCalendar()
    tracker = ConversationTimelineTracker(clock=clock, calendar=cal)

    tracker.start_session(origin_device="dummy", notes="Test session.")
    tracker.register_message(sender="human", content_preview="Hello Aureon.")
    tracker.register_message(sender="aureon", content_preview="Hello Nadine.")
    tracker.end_session(notes="End of test.")

    summary = tracker.daily_summary()
    print("Daily summary:", summary.to_dict())
    print("Last session:", tracker.describe_last_session())
```0
