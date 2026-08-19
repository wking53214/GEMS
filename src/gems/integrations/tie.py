from __future__ import annotations

from typing import Any, Mapping

from gems.contracts import Artifact, EpistemicStatus, Origin, Provenance


class TIEPackageAdapter:
    """Consumes a generic TIE_PACKAGE without assuming an unrecovered schema."""

    def to_artifact(self, package: Mapping[str, Any], source_id: str = "tie") -> Artifact:
        return Artifact(
            kind="tie_package",
            content=dict(package),
            metadata={"adapter": "reconstruction-baseline", "source": "TIE"},
            provenance=Provenance(
                source_id=source_id,
                origin=Origin.UNCERTAIN,
                epistemic_status=EpistemicStatus.UNKNOWN,
                note="TIE_PACKAGE schema not recovered; payload preserved opaquely",
            ),
        )
