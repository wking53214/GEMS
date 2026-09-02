from gems.integrations.tie import TIEPackageAdapter
from gems.integrations.verified_artifact import (
    VerificationStatus,
    VerifiedArtifactAdapter,
    VerifiedArtifactResult,
)
from gems.contracts import EpistemicStatus, Origin


def test_tie_package_is_preserved_opaquely():
    package = {"source": {"id": "x"}, "evidence": [{"text": "example"}]}
    artifact = TIEPackageAdapter().to_artifact(package)
    assert artifact.content == package
    assert artifact.provenance.epistemic_status is EpistemicStatus.UNKNOWN
    assert artifact.provenance.origin is Origin.UNCERTAIN


def test_verified_artifact_adapter_is_dependency_free_boundary():
    package = {"source": {"id": "x"}}
    artifact = TIEPackageAdapter().to_artifact(package)
    result = VerifiedArtifactResult(
        source=artifact,
        output=artifact,
        status=VerificationStatus.NOT_VERIFIED,
    )

    class ExternalVerifier:
        def verify(self, value):
            return result

    adapter: VerifiedArtifactAdapter = ExternalVerifier()
    assert adapter.verify(artifact) is result
    assert result.status is VerificationStatus.NOT_VERIFIED
    assert result.source is artifact
    assert result.output is artifact
