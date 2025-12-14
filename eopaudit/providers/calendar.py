from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CalendarPeriod:
    fiscal_year: str
    fiscal_period: str


class CalendarProvider:
    """Interface for mapping dates to fiscal periods."""

    def period_for(self, occurred_at: datetime) -> Optional[CalendarPeriod]:
        raise NotImplementedError


class StubCalendarProvider(CalendarProvider):
    """Fallback calendar provider when no real fiscal calendar is available."""

    def period_for(self, occurred_at: datetime) -> Optional[CalendarPeriod]:
        # Placeholder: assumes fiscal year equals calendar year and monthly periods
        return CalendarPeriod(fiscal_year=str(occurred_at.year), fiscal_period=f"{occurred_at.year}-{occurred_at.month:02d}")
