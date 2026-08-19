from gems.integrations.tie import TIEPackageAdapter
from gems.contracts import EpistemicStatus, Origin


def test_tie_package_is_preserved_opaquely():
    package = {"source": {"id": "x"}, "evidence": [{"text": "example"}]}
    artifact = TIEPackageAdapter().to_artifact(package)
    assert artifact.content == package
    assert artifact.provenance.epistemic_status is EpistemicStatus.UNKNOWN
    assert artifact.provenance.origin is Origin.UNCERTAIN
