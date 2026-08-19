from __future__ import annotations

from gems.contracts import Artifact, Authority, Origin


class ConstitutionalViolation(ValueError):
    pass


class HumanAuthorityGuard:
    """Enforces the recovered no-silent-AI-to-human-authority rule."""

    def assert_not_human_authorization(self, artifact: Artifact) -> None:
        provenance = artifact.provenance
        if provenance is None:
            raise ConstitutionalViolation("Authority-bearing artifact requires provenance")
        if provenance.authority is Authority.HUMAN_AUTHORIZATION and provenance.origin is not Origin.HUMAN:
            raise ConstitutionalViolation("AI/joint/uncertain material cannot silently become human authorization")

    def authorize(self, artifact: Artifact, human_source_id: str) -> Artifact:
        if artifact.provenance is None:
            raise ConstitutionalViolation("Cannot authorize artifact without provenance")
        from gems.contracts import Provenance
        return Artifact(
            artifact_id=artifact.artifact_id,
            kind=artifact.kind,
            content=artifact.content,
            metadata=artifact.metadata,
            provenance=Provenance(
                source_id=human_source_id,
                origin=Origin.HUMAN,
                epistemic_status=artifact.provenance.epistemic_status,
                authority=Authority.HUMAN_AUTHORIZATION,
                parent_ids=(artifact.provenance.source_id,),
                note="Explicit human authorization boundary crossing",
            ),
        )
