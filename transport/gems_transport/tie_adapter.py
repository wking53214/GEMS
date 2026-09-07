"""Future TIE integration boundary.

TIE is not currently a GitHub repository or an importable dependency.  This
module intentionally defines only the interface that a future adapter must
implement.  It contains no synthetic TIE behavior and no undocumented schema.
"""

from __future__ import annotations

from typing import Protocol

from conservation_kernel import Artifact


class TIEArtifactSource(Protocol):
    """Future integration point for a real TIE source handoff."""

    def load_artifact(self) -> Artifact:
        """Return a typed source artifact once a real TIE adapter exists."""
        ...


class TIEIntegrationMissing(RuntimeError):
    """Raised by callers that require TIE before the integration exists."""


def require_tie_adapter() -> TIEArtifactSource:
    raise TIEIntegrationMissing(
        "TIE is MISSING: no GitHub repository, package, or runtime adapter is available"
    )

