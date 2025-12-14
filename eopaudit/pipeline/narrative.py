from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List

from ..models import Narrative, PersistedStage, VisibilityRecord


class NarrativeBuilder:
    """Builds a narrative view from visibility records."""

    def build(self, records: List[VisibilityRecord]) -> Narrative:
        lines = [
            "EOP Audit Narrative",
            "Pipeline: Transactions -> Signals -> Situations -> Visibility -> Narrative",
            "Execution scope: visibility/reporting only",
            "",
        ]
        for record in records:
            lines.append(
                f"Situation {record.situation_id}: visibility={record.visibility}; reason={record.gating_reason}"
            )
        return Narrative(
            generated_at=datetime.utcnow(),
            content="\n".join(lines),
            visibility_ids=[r.id for r in records],
            execution_scope="visibility-only",
        )

    def persist(self, narrative: Narrative, output_dir: Path) -> PersistedStage:
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / "narrative.txt"
        path.write_text(narrative.content, encoding="utf-8")
        return PersistedStage(name="narrative", output_path=path)
