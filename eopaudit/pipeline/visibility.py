from __future__ import annotations

import json
from pathlib import Path
from typing import List
import uuid

from ..models import PersistedStage, Situation, VisibilityRecord
from ..providers import Layer3PolicyProvider


class VisibilityGate:
    """Applies policy to decide what becomes visible."""

    def __init__(self, policy_provider: Layer3PolicyProvider):
        self.policy_provider = policy_provider

    def build_visibility(self, situations: List[Situation]) -> List[VisibilityRecord]:
        visibility_records: List[VisibilityRecord] = []
        for situation in situations:
            policy = self.policy_provider.policy_for(situation.classification)
            if policy is None:
                visibility = "withheld"
                reason = "Layer-3 policy missing"
            else:
                visibility = policy.get("visibility", "withheld")
                reason = policy.get("reason", "policy applied")
            visibility_records.append(
                VisibilityRecord(
                    id=str(uuid.uuid4()),
                    situation_id=situation.id,
                    visibility=visibility,
                    gating_reason=reason,
                )
            )
        return visibility_records

    def persist(self, records: List[VisibilityRecord], output_dir: Path) -> PersistedStage:
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / "visibility.json"
        serialized = [r.__dict__ for r in records]
        path.write_text(json.dumps(serialized, indent=2))
        return PersistedStage(name="visibility", output_path=path)
