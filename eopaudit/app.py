from __future__ import annotations

import argparse
from pathlib import Path

from .models import PersistedStage
from .pipeline.ingestion import IngestionService
from .pipeline.narrative import NarrativeBuilder
from .pipeline.signals import SignalEngine
from .pipeline.situations import SituationFramework
from .pipeline.visibility import VisibilityGate
from .providers import (
    StubCalendarProvider,
    StubChartOfAccountsProvider,
    StubIdentityResolutionProvider,
    StubLayer3PolicyProvider,
)


class EOPAuditApp:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.calendar_provider = StubCalendarProvider()
        self.chart_provider = StubChartOfAccountsProvider()
        self.identity_provider = StubIdentityResolutionProvider()
        self.policy_provider = StubLayer3PolicyProvider()

        self.ingestion = IngestionService(
            calendar_provider=self.calendar_provider,
            identity_provider=self.identity_provider,
            chart_provider=self.chart_provider,
        )
        self.signal_engine = SignalEngine(calendar_provider=self.calendar_provider)
        self.situation_framework = SituationFramework()
        self.visibility_gate = VisibilityGate(policy_provider=self.policy_provider)
        self.narrative_builder = NarrativeBuilder()

    def run(self, transactions_path: Path, output_dir: Path) -> None:
        transactions = self.ingestion.load_transactions(transactions_path)
        signals = self.signal_engine.build_signals(transactions)
        signal_stage = self.signal_engine.persist(signals, output_dir)

        situations = self.situation_framework.build_situations(signals)
        situation_stage = self.situation_framework.persist(situations, output_dir)

        visibility_records = self.visibility_gate.build_visibility(situations)
        visibility_stage = self.visibility_gate.persist(visibility_records, output_dir)

        narrative = self.narrative_builder.build(visibility_records)
        narrative_stage = self.narrative_builder.persist(narrative, output_dir)

        stages = [signal_stage, situation_stage, visibility_stage, narrative_stage]
        self._report_outputs(stages)

    def _report_outputs(self, stages: list[PersistedStage]) -> None:
        print("Pipeline complete. Outputs:")
        for stage in stages:
            print(f"- {stage.name}: {stage.output_path}")


def main():
    parser = argparse.ArgumentParser(description="EOP Audit pipeline")
    parser.add_argument(
        "transactions",
        type=Path,
        help="Path to a JSON file containing transactions",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Directory for pipeline outputs",
    )
    args = parser.parse_args()

    app = EOPAuditApp(base_dir=Path.cwd())
    app.run(args.transactions, args.output_dir)


if __name__ == "__main__":
    main()
