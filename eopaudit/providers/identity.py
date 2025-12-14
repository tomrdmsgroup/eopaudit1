from __future__ import annotations

from typing import Dict, Optional


class IdentityResolutionProvider:
    """Interface for mapping raw party identifiers to canonical identities."""

    def resolve(self, raw_identifier: str) -> Optional[Dict[str, str]]:
        raise NotImplementedError


class StubIdentityResolutionProvider(IdentityResolutionProvider):
    """Stub when no identity directory exists."""

    def resolve(self, raw_identifier: str) -> Optional[Dict[str, str]]:
        return None
