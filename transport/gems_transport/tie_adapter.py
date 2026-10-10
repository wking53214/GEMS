"""TIE integration boundary.

TIE (Transcript Intelligence Engine) exists as its own repository,
github.com/wking53214/TIE. What does not exist yet is the adapter that turns
one of its typed handoffs into a Conservation Kernel ``Artifact``. This module
defines only the interface that adapter must implement. It contains no
synthetic TIE behavior and no undocumented schema.

Things an adapter should carry, which TIE records and a plain ``Artifact``
does not: the handoff's ``known_uncertainty`` verbatim, and the coverage
record (which source segments were inspected, not inspected or missing).
Dropping either lets a partial reading arrive looking complete.
"""

from __future__ import annotations

from typing import Protocol

from conservation_kernel import Artifact


class TIEArtifactSource(Protocol):
    """Integration point for a real TIE source handoff."""

    def load_artifact(self) -> Artifact:
        """Return a typed source artifact from a TIE handoff."""
        ...


class TIEIntegrationMissing(RuntimeError):
    """Raised by callers that require a TIE adapter before one exists."""


def require_tie_adapter() -> TIEArtifactSource:
    raise TIEIntegrationMissing(
        "No TIE adapter is available in GEMS: TIE exists as its own repository "
        "(github.com/wking53214/TIE), but nothing here converts its typed "
        "handoff into a Conservation Kernel Artifact yet"
    )
