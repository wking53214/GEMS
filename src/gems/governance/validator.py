from __future__ import annotations

from gems.contracts import Artifact, Authority, EpistemicStatus, Origin


class GovernanceValidator:
    def validate_artifact(self, artifact: Artifact) -> None:
        if artifact.provenance is None:
            raise ValueError("Governed artifact must preserve provenance")
        if artifact.provenance.epistemic_status not in set(EpistemicStatus):
            raise ValueError("Unknown epistemic status")
        # An AI-origin artifact cannot authorize itself. Origin.AI == "ai", so
        # this also catches provenance records that carry plain strings.
        if (
            artifact.provenance.origin == Origin.AI
            and artifact.provenance.authority == Authority.HUMAN_AUTHORIZATION
        ):
            raise ValueError(
                "AI-origin artifact cannot claim HUMAN_AUTHORIZATION"
            )
