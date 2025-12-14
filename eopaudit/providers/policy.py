from __future__ import annotations

from typing import Dict, Optional


class Layer3PolicyProvider:
    """Interface for policy constraints applied during visibility gating."""

    def policy_for(self, situation_classification: str) -> Optional[Dict[str, str]]:
        raise NotImplementedError


class StubLayer3PolicyProvider(Layer3PolicyProvider):
    """Stub when policy configuration is absent."""

    def policy_for(self, situation_classification: str) -> Optional[Dict[str, str]]:
        return None
