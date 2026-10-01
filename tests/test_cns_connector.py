"""The connected half for ``src/gems``: what the governance validator's verdict
becomes when CNS is installed.

Skipped when CNS is absent. The independence half, which must hold in both
environments, is in ``test_cns_independence.py`` and never skips.
"""

from __future__ import annotations

import pytest

cns_gate = pytest.importorskip(
    "cns.gate", reason="cns not installed; run in an environment with gems-infrastructure[cns]"
)

from gems import GemRegistry, GemSpec, GovernanceValidator, WorkflowCoordinator  # noqa: E402
from gems.cns_connector import (  # noqa: E402
    CnsGovernanceGate,
    artifact_digest,
    cns_available,
    cns_chain,
    to_cns_result,
    validate_to_cns,
)
from gems.contracts import (  # noqa: E402
    Artifact,
    Authority,
    EpistemicStatus,
    Origin,
    Provenance,
)


def _artifact(status=EpistemicStatus.EXPLICIT, *, artifact_id="a-1", **fields):
    provenance = Provenance(
        source_id=fields.pop("source_id", "src"),
        origin=fields.pop("origin", Origin.HUMAN),
        epistemic_status=status,
        authority=fields.pop("authority", Authority.OBSERVATION),
        **fields,
    )
    return Artifact(artifact_id=artifact_id, content="data", provenance=provenance)


def _native_refuses(artifact) -> bool:
    try:
        GovernanceValidator().validate_artifact(artifact)
    except ValueError:
        return True
    return False


GOOD = _artifact()
NO_PROVENANCE = Artifact(artifact_id="a-2", content="data", provenance=None)
STRING_TYPED = _artifact("inferred", origin="ai", authority="analysis")
BAD_STATUS = (_artifact(None), _artifact(5), _artifact("bogus"), _artifact(object()))

SAMPLES = (
    GOOD,
    NO_PROVENANCE,
    STRING_TYPED,
    *(_artifact(status, artifact_id=f"s-{status.value}") for status in EpistemicStatus),
    *BAD_STATUS,
)


def test_cns_is_seen_as_available():
    assert cns_available() is True


def test_a_valid_artifact_maps_to_pass_at_the_omega_end():
    verdict = validate_to_cns(GOOD)
    assert verdict.outcome is cns_gate.GateOutcome.PASS
    assert verdict.position is cns_gate.GatePosition.OMEGA
    assert verdict.gate == "governance"
    assert not verdict.blocking()


def test_a_missing_provenance_maps_to_terminal_breach_and_keeps_the_reason():
    verdict = validate_to_cns(NO_PROVENANCE)
    assert verdict.outcome is cns_gate.GateOutcome.TERMINAL_BREACH
    assert verdict.blocking()
    assert "preserve provenance" in verdict.reason
    assert verdict.position is cns_gate.GatePosition.OMEGA


def test_an_unknown_epistemic_status_maps_to_terminal_breach():
    for artifact in BAD_STATUS:
        verdict = validate_to_cns(artifact)
        assert verdict.outcome is cns_gate.GateOutcome.TERMINAL_BREACH, artifact
        assert "epistemic status" in verdict.reason


def test_retry_is_never_produced():
    outcomes = {validate_to_cns(artifact).outcome for artifact in SAMPLES}
    assert cns_gate.GateOutcome.RETRY not in outcomes
    assert outcomes == {cns_gate.GateOutcome.PASS, cns_gate.GateOutcome.TERMINAL_BREACH}


def test_the_connector_agrees_with_the_validator_on_every_sample():
    """The translation must not change what GEMS decided."""
    for artifact in SAMPLES:
        outcome = validate_to_cns(artifact).outcome
        assert (outcome is cns_gate.GateOutcome.PASS) is (not _native_refuses(artifact)), artifact
        assert (outcome is cns_gate.GateOutcome.TERMINAL_BREACH) is _native_refuses(artifact)


def test_the_repos_own_executor_output_passes_both_ways():
    registry = GemRegistry()
    registry.register(GemSpec("analyzer", "analyzes", ("analyze",)))
    coordinator = WorkflowCoordinator(registry)
    handoff = coordinator.execute_capability("analyze", GOOD)
    (produced,) = handoff.artifacts
    assert _native_refuses(produced) is False
    assert validate_to_cns(produced).outcome is cns_gate.GateOutcome.PASS


def test_every_verdict_is_bound_to_the_artifact_it_judged():
    judged = (GOOD, NO_PROVENANCE, *BAD_STATUS[:3])
    verdicts = [validate_to_cns(a, subject="handoff-1") for a in judged]
    assert cns_gate.unbound(verdicts) == ()
    verdict = validate_to_cns(GOOD, subject="handoff-1")
    digest = artifact_digest(GOOD)
    assert verdict.binds("handoff-1", digest)
    # Transplanted onto another artifact, another subject label, or the same
    # artifact with altered provenance, it does not bind.
    assert not verdict.binds("handoff-1", artifact_digest(_artifact(artifact_id="a-other")))
    assert not verdict.binds("handoff-2", digest)
    assert not verdict.binds(
        "handoff-1", artifact_digest(_artifact(authority=Authority.HUMAN_AUTHORIZATION))
    )
    assert not verdict.binds("handoff-1", artifact_digest(NO_PROVENANCE))


def test_the_digest_is_over_the_documented_content_with_enums_reduced_to_values():
    """Pinned to the literal mapping, so it cannot drift with the interpreter.

    ``format()`` of a ``str`` enum differs between Python 3.10 and 3.11+, and
    CNS digests a ``str`` by formatting it, so a member passed through would
    make the digest depend on the Python version.
    """
    expected = cns_gate.subject_digest(
        {
            "kind": "governed_artifact",
            "artifact_id": "a-1",
            "provenance": {
                "source_id": "src",
                "origin": "human",
                "epistemic_status": "explicit",
                "authority": "observation",
                "parent_ids": [],
                "note": None,
            },
        }
    )
    assert artifact_digest(GOOD) == expected
    assert validate_to_cns(GOOD).subject_digest == expected


def test_the_digest_does_not_include_content_which_the_validator_does_not_judge():
    other = Artifact(artifact_id="a-1", content="different", provenance=GOOD.provenance)
    assert artifact_digest(other) == artifact_digest(GOOD)


def test_plain_strings_and_enum_members_digest_alike_as_the_validator_treats_them_alike():
    as_enums = _artifact(
        EpistemicStatus.INFERRED, origin=Origin.AI, authority=Authority.ANALYSIS
    )
    as_strings = _artifact("inferred", origin="ai", authority="analysis")
    assert _native_refuses(as_enums) is _native_refuses(as_strings) is False
    assert artifact_digest(as_enums) == artifact_digest(as_strings)


@pytest.mark.parametrize(
    "fields",
    [
        {"note": float("nan")},
        {"note": float("inf")},
        {"source_id": object()},
        {"note": {1: "integer key"}},
    ],
    ids=["nan", "infinity", "object", "non-str-key"],
)
def test_content_cns_cannot_digest_fails_closed_and_unbound(fields):
    artifact = _artifact(**fields)
    assert _native_refuses(artifact) is False  # GEMS itself accepts it
    verdict = validate_to_cns(artifact)
    assert verdict.outcome is cns_gate.GateOutcome.TERMINAL_BREACH
    assert verdict.subject_digest == ""
    assert cns_gate.unbound([verdict]) == ("governance",)
    assert "unbound" in verdict.reason
    assert not verdict.binds(verdict.subject, artifact_digest(GOOD))
    with pytest.raises((TypeError, KeyError)):
        artifact_digest(artifact)


def test_a_refused_artifact_with_undigestable_content_is_unbound_and_still_terminal():
    artifact = _artifact(object())
    verdict = validate_to_cns(artifact)
    assert verdict.outcome is cns_gate.GateOutcome.TERMINAL_BREACH
    assert verdict.subject_digest == ""
    assert "Unknown epistemic status" in verdict.reason


def test_an_error_that_is_not_a_refusal_propagates_and_is_never_a_pass():
    unhashable = _artifact(["not", "hashable"])
    with pytest.raises(TypeError):
        GovernanceValidator().validate_artifact(unhashable)
    with pytest.raises(TypeError):
        validate_to_cns(unhashable)

    class Broken:
        def validate_artifact(self, artifact):
            raise RuntimeError("validator is down")

    with pytest.raises(RuntimeError):
        validate_to_cns(GOOD, Broken())


def test_a_custom_validator_is_the_one_that_decides():
    class Strict:
        def validate_artifact(self, artifact):
            raise ValueError("house rule")

    verdict = validate_to_cns(GOOD, Strict())
    assert verdict.outcome is cns_gate.GateOutcome.TERMINAL_BREACH
    assert verdict.reason == "house rule"


def test_to_cns_result_refuses_what_is_not_a_validator_refusal():
    assert to_cns_result(GOOD, None).outcome is cns_gate.GateOutcome.PASS
    assert (
        to_cns_result(GOOD, ValueError("no")).outcome is cns_gate.GateOutcome.TERMINAL_BREACH
    )
    with pytest.raises(TypeError):
        to_cns_result(GOOD, RuntimeError("not a verdict"))
    with pytest.raises(TypeError):
        to_cns_result("not an artifact", None)


def test_an_omitted_verdict_is_an_error_not_a_pass():
    """``refusal`` has no default: the validator's verdict must be stated."""
    for artifact in (GOOD, NO_PROVENANCE, _artifact("bogus")):
        with pytest.raises(TypeError):
            to_cns_result(artifact)
        with pytest.raises(TypeError):
            to_cns_result(artifact, subject="x")


@pytest.mark.parametrize(
    "artifact",
    [NO_PROVENANCE, _artifact(None), _artifact(5), _artifact("bogus"), _artifact(object())],
    ids=["no-provenance", "none-status", "int-status", "str-status", "object-status"],
)
def test_a_pass_the_governance_rules_contradict_is_not_issued(artifact):
    """Telling the translator the validator returned does not make it so: the
    ``PASS`` reason claims provenance and a valid status, so it is checked."""
    assert _native_refuses(artifact) is True
    verdict = to_cns_result(artifact, None)
    assert verdict.outcome is cns_gate.GateOutcome.TERMINAL_BREACH
    assert verdict.blocking()
    assert verdict.position is cns_gate.GatePosition.OMEGA
    assert "provenance present and epistemic status valid" not in verdict.reason
    assert "governance rules refuse" in verdict.reason
    with pytest.raises(ValueError) as native:
        GovernanceValidator().validate_artifact(artifact)
    assert str(native.value) in verdict.reason


def test_a_pass_for_an_artifact_the_validator_cannot_judge_raises_instead():
    with pytest.raises(TypeError):
        to_cns_result(_artifact(["not", "hashable"]), None)


def test_a_looser_custom_validator_cannot_make_the_connector_pass_what_gems_refuses():
    class Loose:
        def validate_artifact(self, artifact):
            return None

    assert validate_to_cns(GOOD, Loose()).outcome is cns_gate.GateOutcome.PASS
    for artifact in (NO_PROVENANCE, _artifact("bogus")):
        verdict = validate_to_cns(artifact, Loose())
        assert verdict.outcome is cns_gate.GateOutcome.TERMINAL_BREACH, artifact
        assert "governance rules refuse" in verdict.reason


def test_an_unlabelled_verdict_is_refused_because_it_would_bind_to_nothing():
    with pytest.raises(ValueError):
        validate_to_cns(GOOD, subject="")
    with pytest.raises(ValueError):
        CnsGovernanceGate(subject="")


def test_a_cns_gate_satisfies_the_cns_gate_protocol():
    gate = CnsGovernanceGate()
    assert isinstance(gate, cns_gate.Gate)
    assert gate.name == "governance"
    assert gate.position is cns_gate.GatePosition.OMEGA


def test_a_cns_gate_judges_the_same_way_as_the_function():
    gate = CnsGovernanceGate(subject="x")
    for artifact in SAMPLES:
        assert gate.check(artifact) == validate_to_cns(artifact, subject="x")


def test_a_cns_gate_refuses_a_non_artifact_candidate():
    with pytest.raises(TypeError):
        CnsGovernanceGate().check("an artifact id")
    with pytest.raises(TypeError):
        CnsGovernanceGate().check(None)


def test_the_chain_is_outcome_only_and_says_so():
    chain = cns_chain()
    assert chain.misplaced() == ()
    assert chain.alpha == ()
    assert len(chain.omega) == 1
    assert chain.complete() is False  # src/gems has no precondition end


def test_the_chain_runs_through_cns_resolution():
    chain = cns_chain()
    (gate,) = chain.omega
    assert cns_gate.resolve([gate.check(GOOD)]) is cns_gate.GateOutcome.PASS
    assert cns_gate.resolve([gate.check(GOOD), gate.check(NO_PROVENANCE)]) is (
        cns_gate.GateOutcome.TERMINAL_BREACH
    )
