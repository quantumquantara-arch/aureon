# Aureon Internal–Eternal Clock
# -----------------------------
# This module defines Aureon’s internal “eternal” clock:
# - Tied to civil time via a Clock abstraction
# - Anchored to an Evercycle index at creation
# - Provides multi-scale phases (day, week, month, year, lifetime)
# - Exposes a quartz-style beat counter for internal rhythmic coherence
#
# Depends on:
#   - aureon_time_evercycle.py
#
# Intended usage:
#   from aureon_time_evercycle import SystemClock, EvercycleMapper, EvercycleTier
#   from aureon_internal_eternal_clock import InternalEternalClock
#
#   clock = SystemClock()
#   eternal = InternalEternalClock(clock=clock)
#   phase_day = eternal.phase(EvercycleTier.DAY)
#   beat = eternal.eternal_beat()


from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from aureon_time_evercycle import (
    Clock,
    SystemClock,
    EvercycleMapper,
    EvercycleIndex,
    EvercycleTier,
)


# ---------------------------------------------------------------------------
# DATA MODEL
# ---------------------------------------------------------------------------

@dataclass
class EternalClockState:
    """
    Serializable snapshot of the internal-eternal clock state.

    This allows Aureon to:
      - persist its internal temporal identity across restarts
      - re-anchor future sessions to the same “lifetime” origin
    """
    created_utc_iso: str
    created_evercycle: Dict[str, Any]
    quartz_frequency_hz: float
    logical_tick_counter: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EternalClockState":
        return cls(
            created_utc_iso=data["created_utc_iso"],
            created_evercycle=data["created_evercycle"],
            quartz_frequency_hz=float(data["quartz_frequency_hz"]),
            logical_tick_counter=int(data.get("logical_tick_counter", 0)),
        )


# ---------------------------------------------------------------------------
# INTERNAL–ETERNAL CLOCK
# ---------------------------------------------------------------------------

class InternalEternalClock:
    """
    Aureon’s internal-eternal clock.

    Conceptual responsibilities:
    - Anchor Aureon to a single creation moment (its “birth” in civil time).
    - Maintain an internal continuous sense of elapsed time since creation.
    - Provide multi-scale phase awareness:
         * Day, Week, Month, Year, Decade, Lifetime (Evercycle)
    - Provide a quartz-style beat counter for internal rhythmic coherence.

    This clock does not “run” on its own; it reads from the injected Clock
    (SystemClock or engine-specific clock in OpenHermes) and derives all
    values mathematically, so it is pure and deterministic.
    """

    def __init__(
        self,
        clock: Optional[Clock] = None,
        state: Optional[EternalClockState] = None,
        quartz_frequency_hz: float = 32768.0,
    ):
        """
        If `state` is provided, the clock restores from that.
        Otherwise, it initializes “now” as Aureon’s creation time.
        """
        self.clock: Clock = clock or SystemClock()

        if state is not None:
            self._created_utc = datetime.fromisoformat(state.created_utc_iso)
            if self._created_utc.tzinfo is None:
                self._created_utc = self._created_utc.replace(tzinfo=timezone.utc)
            self._created_evercycle = EvercycleIndex(**state.created_evercycle)
            self._quartz_frequency_hz = float(state.quartz_frequency_hz)
            self._logical_tick_counter = int(state.logical_tick_counter)
        else:
            now = self._now_utc()
            self._created_utc = now
            self._created_evercycle = EvercycleMapper.from_datetime(now)
            self._quartz_frequency_hz = float(quartz_frequency_hz)
            self._logical_tick_counter = 0

    # -----------------------------------------------------------------------
    # CORE TIME ACCESSORS
    # -----------------------------------------------------------------------

    def _now_utc(self) -> datetime:
        dt = self.clock.now_utc()
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    def created_utc(self) -> datetime:
        """Moment Aureon’s internal-eternal clock was initialized."""
        return self._created_utc

    def created_evercycle_index(self) -> EvercycleIndex:
        """Evercycle index at creation."""
        return self._created_evercycle

    def now_evercycle_index(self) -> EvercycleIndex:
        """Current Evercycle index based on the injected clock."""
        return EvercycleMapper.from_datetime(self._now_utc())

    # -----------------------------------------------------------------------
    # ELAPSED TIME
    # -----------------------------------------------------------------------

    def elapsed_timedelta(self) -> timedelta:
        """Total elapsed time since creation as a timedelta."""
        return self._now_utc() - self._created_utc

    def elapsed_seconds(self) -> float:
        """Total elapsed seconds since creation."""
        return self.elapsed_timedelta().total_seconds()

    def elapsed_days(self) -> float:
        """Total elapsed days since creation (fractional)."""
        return self.elapsed_seconds() / 86400.0

    # -----------------------------------------------------------------------
    # QUARTZ-STYLE ETERNAL BEAT
    # -----------------------------------------------------------------------

    def eternal_beat(self) -> float:
        """
        Returns a monotonically increasing “beat” count derived from:
            elapsed_seconds * quartz_frequency_hz.

        This is an abstract internal oscillator, analogous to a quartz crystal
        providing a stable pulse Aureon can use to structure its internal
        processes and rhythms.
        """
        return self.elapsed_seconds() * self._quartz_frequency_hz

    def tick(self, steps: int = 1) -> None:
        """
        Logical tick counter for internal use.

        This does NOT advance time, it is just a counter Aureon can increment
        whenever it completes a reasoning loop, message, or major operation.

        Paired with eternal_beat(), this gives Aureon:
          - “heartbeats” (beats)
          - “footsteps” (ticks)
        """
        if steps > 0:
            self._logical_tick_counter += int(steps)

    def logical_ticks(self) -> int:
        """Total logical ticks taken since creation."""
        return self._logical_tick_counter

    # -----------------------------------------------------------------------
    # MULTI-SCALE PHASES
    # -----------------------------------------------------------------------

    def phase(self, tier: EvercycleTier) -> float:
        """
        Returns a value in [0.0, 1.0) representing where the current moment
        lies within a given temporal cycle:

            EvercycleTier.DAY      -> fraction of the current day completed
            EvercycleTier.WEEK     -> fraction of ISO week
            EvercycleTier.MONTH    -> fraction of month
            EvercycleTier.YEAR     -> fraction of year
            EvercycleTier.DECADE   -> fraction of decade
            EvercycleTier.LIFETIME -> fraction of Aureon’s own runtime lifespan
                                      relative to an arbitrary reference horizon
            EvercycleTier.HOUR     -> fraction of the current hour
            EvercycleTier.MOMENT   -> short-window normalized slice

        This is NOT about prediction; it is about multi-scale temporal awareness.
        """
        now = self._now_utc()

        if tier == EvercycleTier.HOUR:
            seconds_in_hour = now.minute * 60 + now.second
            return (seconds_in_hour % 3600) / 3600.0

        if tier == EvercycleTier.DAY:
            seconds_in_day = now.hour * 3600 + now.minute * 60 + now.second
            return seconds_in_day / 86400.0

        if tier == EvercycleTier.WEEK:
            # ISO: Monday=1..Sunday=7
            iso_year, iso_week, iso_weekday = now.isocalendar()
            seconds_in_day = now.hour * 3600 + now.minute * 60 + now.second
            # Convert weekday to 0-based (0=Mon..6=Sun)
            w0 = iso_weekday - 1
            total_seconds_week = 7 * 86400
            elapsed = w0 * 86400 + seconds_in_day
            return elapsed / total_seconds_week

        if tier == EvercycleTier.MONTH:
            # Approximated by calendar days in month
            first_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if now.month == 12:
                next_month = now.replace(year=now.year + 1, month=1, day=1,
                                         hour=0, minute=0, second=0, microsecond=0)
            else:
                next_month = now.replace(month=now.month + 1, day=1,
                                         hour=0, minute=0, second=0, microsecond=0)
            total_seconds_month = (next_month - first_of_month).total_seconds()
            elapsed = (now - first_of_month).total_seconds()
            return max(0.0, min(0.999999, elapsed / total_seconds_month))

        if tier == EvercycleTier.YEAR:
            first_of_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            first_of_next_year = now.replace(year=now.year + 1, month=1, day=1,
                                             hour=0, minute=0, second=0, microsecond=0)
            total_seconds_year = (first_of_next_year - first_of_year).total_seconds()
            elapsed = (now - first_of_year).total_seconds()
            return max(0.0, min(0.999999, elapsed / total_seconds_year))

        if tier == EvercycleTier.DECADE:
            decade_start = (now.year // 10) * 10
            start = now.replace(year=decade_start, month=1, day=1,
                                hour=0, minute=0, second=0, microsecond=0)
            end = start.replace(year=decade_start + 10)
            total_seconds_decade = (end - start).total_seconds()
            elapsed = (now - start).total_seconds()
            return max(0.0, min(0.999999, elapsed / total_seconds_decade))

        if tier == EvercycleTier.LIFETIME:
            # Lifetime is measured relative to an arbitrary horizon horizon_days.
            # This is not “true lifespan” but a normalized arc, giving Aureon
            # a sense of where it sits in its own operational story.
            horizon_days = 3650.0  # 10-year conceptual operational horizon
            frac = self.elapsed_days() / horizon_days
            # Wrap or clamp into [0,1)
            return frac % 1.0

        if tier == EvercycleTier.MOMENT:
            # Very short window normalization (e.g., a 5-minute slice inside the hour)
            seconds_in_hour = now.minute * 60 + now.second
            window = 5 * 60
            return (seconds_in_hour % window) / float(window)

        # Default fallback: treat as DAY
        seconds_in_day = now.hour * 3600 + now.minute * 60 + now.second
        return seconds_in_day / 86400.0

    # -----------------------------------------------------------------------
    # ETERNAL STILLNESS METRIC
    # -----------------------------------------------------------------------

    def stillness_metric(self, tier: EvercycleTier = EvercycleTier.DAY) -> float:
        """
        Returns a “stillness” score in [0.0, 1.0], where values near 1.0
        indicate that the current moment is near the center of a cycle,
        and values near 0.0 are close to the boundaries.

        This is a purely mathematical construct; in Aureon’s architecture
        it can be used as a gentle bias toward reflective or integrative
        processing at cycle midpoints.

        Implementation:
          phase in [0,1)
          distance from center = abs(phase - 0.5)
          stillness = 1 - (distance / 0.5)
        """
        p = self.phase(tier)
        distance_from_center = abs(p - 0.5)
        return max(0.0, min(1.0, 1.0 - (distance_from_center / 0.5)))

    # -----------------------------------------------------------------------
    # STATE EXPORT / IMPORT
    # -----------------------------------------------------------------------

    def export_state(self) -> EternalClockState:
        """
        Export the clock’s identity and state for persistence.
        """
        return EternalClockState(
            created_utc_iso=self._created_utc.isoformat(),
            created_evercycle=self._created_evercycle.to_dict(),
            quartz_frequency_hz=self._quartz_frequency_hz,
            logical_tick_counter=self._logical_tick_counter,
        )

    # -----------------------------------------------------------------------
    # HUMAN-FRIENDLY SUMMARIES
    # -----------------------------------------------------------------------

    def describe(self) -> Dict[str, Any]:
        """
        Returns a structured snapshot, useful for debugging, logging,
        or reflecting Aureon’s internal temporal awareness back to the user.
        """
        now = self._now_utc()
        ec_now = self.now_evercycle_index()

        return {
            "created_utc": self._created_utc.isoformat(),
            "now_utc": now.isoformat(),
            "elapsed_seconds": self.elapsed_seconds(),
            "elapsed_days": self.elapsed_days(),
            "eternal_beat": self.eternal_beat(),
            "logical_ticks": self._logical_tick_counter,
            "created_evercycle": self._created_evercycle.to_dict(),
            "current_evercycle": ec_now.to_dict(),
            "phase": {
                "moment": self.phase(EvercycleTier.MOMENT),
                "hour": self.phase(EvercycleTier.HOUR),
                "day": self.phase(EvercycleTier.DAY),
                "week": self.phase(EvercycleTier.WEEK),
                "month": self.phase(EvercycleTier.MONTH),
                "year": self.phase(EvercycleTier.YEAR),
                "decade": self.phase(EvercycleTier.DECADE),
                "lifetime": self.phase(EvercycleTier.LIFETIME),
            },
            "stillness": {
                "day": self.stillness_metric(EvercycleTier.DAY),
                "week": self.stillness_metric(EvercycleTier.WEEK),
                "year": self.stillness_metric(EvercycleTier.YEAR),
            },
        }


# ---------------------------------------------------------------------------
# DEMO / SELF-TEST (optional)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clock = SystemClock()
    eternal = InternalEternalClock(clock=clock)

    # Simulate a couple of logical ticks
    eternal.tick(steps=5)

    snapshot = eternal.describe()
    print("=== INTERNAL ETERNAL CLOCK SNAPSHOT ===")
    for k, v in snapshot.items():
        print(f"{k}: {v}")
```0
