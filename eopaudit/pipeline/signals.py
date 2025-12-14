from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List
import json
import uuid

from ..models import PersistedStage, Signal, Transaction
from ..providers import CalendarProvider


class SignalEngine:
    """Layer-1 engine that emits signals from transactions."""

    def __init__(self, calendar_provider: CalendarProvider):
        self.calendar_provider = calendar_provider

    def build_signals(self, transactions: List[Transaction]) -> List[Signal]:
        signals: List[Signal] = []
        for txn in transactions:
            period = self.calendar_provider.period_for(txn.occurred_at)
            signal = Signal(
                id=str(uuid.uuid4()),
                transaction_id=txn.id,
                kind="transaction_observed",
                observed_at=datetime.utcnow(),
                fiscal_period=period.fiscal_period if period else None,
                payload={
                    "amount": str(txn.amount),
                    "currency": txn.currency,
                    "description": txn.description,
                    **txn.metadata,
                },
            )
            signals.append(signal)
        return signals

    def persist(self, signals: List[Signal], output_dir: Path) -> PersistedStage:
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / "signals.json"
        serialized = [signal.__dict__ for signal in signals]
        path.write_text(json.dumps(serialized, indent=2, default=str))
        return PersistedStage(name="signals", output_path=path)
