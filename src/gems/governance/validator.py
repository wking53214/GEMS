from __future__ import annotations

from gems.contracts import Artifact, Authority, EpistemicStatus, Origin


class GovernanceValidator:
    def validate_artifact(self, artifact: Artifact) -> None:
        if artifact.provenance is None:
            raise ValueError("Governed artifact must preserve provenance")
        if artifact.provenance.epistemic_status not in set(EpistemicStatus):
            raise ValueError("Unknown epistemic status")
        # Only a purely human-origin artifact may claim HUMAN_AUTHORIZATION.
        # This is an allowlist, not a block on Origin.AI: JOINT (human plus AI)
        # and UNCERTAIN (origin unknown) could hide AI authorship, and a
        # misspelled or unexpected origin must fail closed too.
        if (
            artifact.provenance.authority == Authority.HUMAN_AUTHORIZATION
            and artifact.provenance.origin != Origin.HUMAN
        ):
            raise ValueError(
                "only HUMAN-origin artifacts may claim HUMAN_AUTHORIZATION"
            )
