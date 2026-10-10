"""TIE integration boundary.

TIE (Transcript Intelligence Engine) exists as its own repository,
github.com/wking53214/TIE. ``TIEPackageSource`` in ``tie_package_source``
turns one of its packages into a Conservation Kernel ``Artifact`` and
implements the interface below. This module defines only that interface. It
contains no synthetic TIE behavior and no undocumented schema.

``require_tie_adapter`` still raises: it takes no arguments, so it has no
package to build a source from. A caller builds ``TIEPackageSource`` itself.

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
        "No TIE adapter is configured: build a TIEPackageSource from a TIE package "
        "(github.com/wking53214/TIE) and pass its artifact to the gateway's "
        "ingest_source"
    )
