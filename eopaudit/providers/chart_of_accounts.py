from __future__ import annotations

from typing import Dict, Optional


class ChartOfAccountsProvider:
    """Interface for resolving account metadata."""

    def account_details(self, account_id: str) -> Optional[Dict[str, str]]:
        raise NotImplementedError


class StubChartOfAccountsProvider(ChartOfAccountsProvider):
    """Stubbed provider when no COA is available."""

    def account_details(self, account_id: str) -> Optional[Dict[str, str]]:
        return None
