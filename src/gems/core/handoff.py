from __future__ import annotations

from gems.contracts import Artifact, Handoff


class HandoffValidator:
    """Minimal validation for recovered typed-handoff/provenance invariants."""

    def validate(self, handoff: Handoff) -> None:
        if not handoff.sender or not handoff.recipient:
            raise ValueError("Handoff requires sender and recipient")
        for artifact in handoff.artifacts:
            self._validate_artifact(artifact)

    @staticmethod
    def _validate_artifact(artifact: Artifact) -> None:
        if artifact.provenance is None:
            raise ValueError(f"Artifact {artifact.artifact_id} is missing provenance")
