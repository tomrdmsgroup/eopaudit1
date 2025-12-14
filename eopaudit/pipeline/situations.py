from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import List

from ..models import PersistedStage, Situation, Signal


class SituationFramework:
    """Framework placeholder for Layer-2 situation construction."""

    def build_situations(self, signals: List[Signal]) -> List[Situation]:
        # Without Layer-2 logic from V7 docs, create stub groupings
        situation = Situation(
            id=str(uuid.uuid4()),
            signal_ids=[s.id for s in signals],
            status="pending_definition",
            classification="unclassified",
            notes=(
                "Layer-2 definitions required from V7. Without them, signals are grouped into"
                " a single placeholder situation."
            ),
        )
        return [situation]

    def persist(self, situations: List[Situation], output_dir: Path) -> PersistedStage:
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / "situations.json"
        serialized = [s.__dict__ for s in situations]
        path.write_text(json.dumps(serialized, indent=2))
        return PersistedStage(name="situations", output_path=path)
