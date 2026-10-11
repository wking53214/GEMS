"""AI-origin artifacts may not claim HUMAN_AUTHORIZATION.

Regression tests for the gap where GovernanceValidator passed such artifacts.
"""

import pytest

from gems.contracts import Artifact, Authority, EpistemicStatus, Origin, Provenance
from gems.cns_connector import validate_to_cns
from gems.governance import GovernanceValidator


def _artifact(origin, authority, status=EpistemicStatus.INFERRED):
    return Artifact(
        artifact_id="auth-test",
        content="x",
        provenance=Provenance(
            source_id="src",
            origin=origin,
            epistemic_status=status,
            authority=authority,
        ),
    )


def test_ai_origin_claiming_human_authorization_is_refused():
    with pytest.raises(ValueError, match="may claim HUMAN_AUTHORIZATION"):
        GovernanceValidator().validate_artifact(
            _artifact(Origin.AI, Authority.HUMAN_AUTHORIZATION)
        )


@pytest.mark.parametrize(
    "origin",
    [Origin.AI, Origin.JOINT, Origin.UNCERTAIN, "ai", "joint", "uncertain", "HUMAN", "human "],
)
def test_only_pure_human_origin_may_claim_human_authorization(origin):
    # Anything but exactly HUMAN is refused, including the misspelled "HUMAN".
    with pytest.raises(ValueError, match="may claim HUMAN_AUTHORIZATION"):
        GovernanceValidator().validate_artifact(_artifact(origin, Authority.HUMAN_AUTHORIZATION))


def test_plain_string_values_are_refused_too():
    with pytest.raises(ValueError, match="may claim HUMAN_AUTHORIZATION"):
        GovernanceValidator().validate_artifact(
            _artifact("ai", "human_authorization")
        )


@pytest.mark.parametrize(
    "origin, authority",
    [
        (Origin.HUMAN, Authority.HUMAN_AUTHORIZATION),
        (Origin.AI, Authority.ANALYSIS),
        (Origin.AI, Authority.PROPOSAL),
        (Origin.AI, Authority.OBSERVATION),
    ],
)
def test_other_combinations_still_pass(origin, authority):
    assert GovernanceValidator().validate_artifact(_artifact(origin, authority)) is None


def test_cns_verdict_is_breach_not_pass_for_ai_authorization_claim():
    verdict = validate_to_cns(_artifact(Origin.AI, Authority.HUMAN_AUTHORIZATION))
    assert verdict.outcome.value == "terminal_breach"
    assert "may claim HUMAN_AUTHORIZATION" in verdict.reason
