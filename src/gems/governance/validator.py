from __future__ import annotations

from gems.contracts import Artifact, EpistemicStatus


class GovernanceValidator:
    def validate_artifact(self, artifact: Artifact) -> None:
        if artifact.provenance is None:
            raise ValueError("Governed artifact must preserve provenance")
        if artifact.provenance.epistemic_status not in set(EpistemicStatus):
            raise ValueError("Unknown epistemic status")
