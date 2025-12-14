from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

from ..models import Transaction


class IngestionService:
    """Responsible for loading transaction data from disk."""

    def __init__(self, calendar_provider, identity_provider, chart_provider):
        self.calendar_provider = calendar_provider
        self.identity_provider = identity_provider
        self.chart_provider = chart_provider

    def load_transactions(self, path: Path) -> List[Transaction]:
        with path.open() as f:
            raw = json.load(f)

        transactions: List[Transaction] = []
        for entry in raw:
            occurred_at = datetime.fromisoformat(entry["occurred_at"])
            metadata = entry.get("metadata", {})
            if account_id := entry.get("account_id"):
                metadata["account"] = account_id
                account_details = self.chart_provider.account_details(account_id)
                if account_details:
                    metadata.update({f"account_{k}": v for k, v in account_details.items()})
            if party := entry.get("counterparty"):
                metadata["counterparty"] = party
                resolved = self.identity_provider.resolve(party)
                if resolved:
                    metadata.update({f"counterparty_{k}": v for k, v in resolved.items()})

            transactions.append(
                Transaction(
                    id=str(entry.get("id")),
                    occurred_at=occurred_at,
                    amount=float(entry["amount"]),
                    currency=entry.get("currency", ""),
                    description=entry.get("description", ""),
                    metadata=metadata,
                )
            )
        return transactions
