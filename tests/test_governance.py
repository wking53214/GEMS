import pytest

from gems.contracts import Artifact, Authority, EpistemicStatus, Origin, Provenance
from gems.governance import ConstitutionalViolation, HumanAuthorityGuard


def test_ai_artifact_cannot_claim_human_authorization():
    artifact = Artifact(provenance=Provenance("ai-1", Origin.AI, EpistemicStatus.INFERRED, Authority.HUMAN_AUTHORIZATION))
    with pytest.raises(ConstitutionalViolation):
        HumanAuthorityGuard().assert_not_human_authorization(artifact)


def test_explicit_human_authorization_is_allowed():
    artifact = Artifact(provenance=Provenance("draft-1", Origin.AI, EpistemicStatus.INFERRED))
    authorized = HumanAuthorityGuard().authorize(artifact, "human-action-1")
    assert authorized.provenance.authority is Authority.HUMAN_AUTHORIZATION
    assert authorized.provenance.origin is Origin.HUMAN
