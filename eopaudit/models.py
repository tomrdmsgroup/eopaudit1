from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Transaction:
    """Raw transaction record from ingestion."""

    id: str
    occurred_at: datetime
    amount: float
    currency: str
    description: str
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class Signal:
    """Layer-1 signal produced from a transaction."""

    id: str
    transaction_id: str
    kind: str
    observed_at: datetime
    fiscal_period: Optional[str]
    payload: Dict[str, str]


@dataclass
class Situation:
    """Layer-2 situation derived from signals."""

    id: str
    signal_ids: List[str]
    status: str
    classification: str
    notes: str = ""


@dataclass
class VisibilityRecord:
    """Visibility layer view of a situation after gating."""

    id: str
    situation_id: str
    visibility: str
    gating_reason: str


@dataclass
class Narrative:
    """Narrative built from visibility records."""

    generated_at: datetime
    content: str
    visibility_ids: List[str]
    execution_scope: str


@dataclass
class PersistedStage:
    """Utility for capturing paths written by a pipeline stage."""

    name: str
    output_path: Path
