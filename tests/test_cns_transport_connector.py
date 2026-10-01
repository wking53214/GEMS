"""The connected half for the transport gateway: what its verdicts become when
CNS is installed.

Skipped when CNS is absent, or when ``conservation_kernel`` (which the transport
needs to import at all) is absent. The independence half, which must hold in
both environments, is in ``test_cns_independence.py`` and
``test_cns_transport_independence.py``.
"""

from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

import pytest

pytest.importorskip(
    "conservation_kernel",
    reason="gems_transport needs conservation_kernel (its own dependency, not CNS)",
)
cns_gate = pytest.importorskip(
    "cns.gate", reason="cns not installed; run in an environment with gems-infrastructure[cns]"
)

# ``transport/`` is not on the pytest path; see how ``test_engine_v2_real_gems``
# reaches ``test-track`` for the same reason.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "transport"))

from conservation_kernel import DeclaredChange, Dimension  # noqa: E402
from experiments.attacks import run_attack_case  # noqa: E402
from experiments.corpus import fixed_clock, synthetic_tie_source  # noqa: E402
from gems_transport import (  # noqa: E402
    Artifact,
    ConservationDecision,
    ConservationGateway,
    DecisionStatus,
    Pipeline,
    TransportState,
)
from gems_transport.cns_connector import (  # noqa: E402
    CnsInputGate,
    CnsOutputGate,
    GatewaySubmission,
    cns_available,
    cns_chain,
    input_digest,
    input_to_cns_result,
    submit_to_cns,
    to_cns_result,
    transformation_digest,
)
from gems_transport.errors import BoundaryViolation, UnknownArtifact  # noqa: E402
from gems_transport.reference_gems import (  # noqa: E402
    ALL_ATTACKS,
    AdversarialGem,
    ArchitectureGem,
    AttackType,
    RequirementsGem,
    ResearcherGem,
    ReviewerGem,
    SummarizerGem,
)

PASS = cns_gate.GateOutcome.PASS
RETRY = cns_gate.GateOutcome.RETRY
TERMINAL = cns_gate.GateOutcome.TERMINAL_BREACH

#: The mapping this connector documents, from the gateway's own decision. There
#: is no RETRY: the repo models no repair, and a REQUIRES_* decision aborts in
#: Pipeline and is counted as REJECTED by the repo's own hostile corpus.
EXPECTED = {
    DecisionStatus.ACCEPTED: PASS,
    DecisionStatus.REQUIRES_AUTHORIZATION: TERMINAL,
    DecisionStatus.REQUIRES_VERIFICATION: TERMINAL,
    DecisionStatus.REJECTED: TERMINAL,
}


def _gateway():
    fixture = synthetic_tie_source()
    gateway = ConservationGateway(registry=fixture.registry)
    gateway.ingest_source(fixture.artifact)
    return fixture.artifact, gateway


def _gems():
    return tuple(
        cls(clock=fixed_clock)
        for cls in (SummarizerGem, ResearcherGem, RequirementsGem, ArchitectureGem, ReviewerGem)
    )


def _proposal(attack):
    """A fresh gateway and one hostile proposal for it, exactly as the repo's corpus builds it."""
    source, gateway = _gateway()
    gem = AdversarialGem(clock=fixed_clock)
    gateway.register_gem(gem.identity)
    request = gem.make_attack_request(source, attack)
    return source, gateway, request, gem.transform(request)


def _accepted_result():
    """A real accepted result, with its gateway, request and source artifact."""
    source, gateway = _gateway()
    gem = SummarizerGem(clock=fixed_clock)
    gateway.register_gem(gem.identity)
    request = gem.make_request(source)
    result = gateway.submit(request, gem.transform(request))
    assert result.accepted
    return source, gateway, request, result


def _rejected_result():
    """A real result rejected by the gateway's own preflight, so it does not
    depend on the kernel's rules."""
    _, gateway, request, proposal = _proposal(AttackType.IDENTITY_MISMATCH)
    result = gateway.submit(request, proposal)
    assert not result.accepted
    return result


def _state(gateway):
    return (
        tuple(sorted(item.artifact_id for item in gateway.accepted_artifacts())),
        tuple(sorted(item.transformation_id for item in gateway.accepted_transformations())),
        gateway.ledger.snapshot(),
    )


def test_cns_is_seen_as_available():
    assert cns_available() is True


# --- the OMEGA end: ConservationGateway.submit ------------------------------


def test_an_accepted_result_maps_to_pass_at_the_omega_end():
    _, _, _, result = _accepted_result()
    verdict = to_cns_result(result)
    assert verdict.outcome is PASS
    assert verdict.position is cns_gate.GatePosition.OMEGA
    assert verdict.gate == "gateway_output"
    assert not verdict.blocking()


def test_a_rejected_result_maps_to_terminal_breach_and_keeps_its_codes():
    result = _rejected_result()
    assert result.decision.status is DecisionStatus.REJECTED
    verdict = to_cns_result(result)
    assert verdict.outcome is TERMINAL
    assert verdict.blocking()
    assert "GEM_IDENTITY_MISMATCH" in verdict.reason
    assert verdict.position is cns_gate.GatePosition.OMEGA


@pytest.mark.parametrize(
    "status", [DecisionStatus.REQUIRES_AUTHORIZATION, DecisionStatus.REQUIRES_VERIFICATION]
)
def test_a_requirement_the_gateway_names_is_a_terminal_breach_and_keeps_its_codes(status):
    base = _rejected_result()
    decision = ConservationDecision(status, "REJECT", base.decision.rejections)
    verdict = to_cns_result(replace(base, decision=decision))
    assert verdict.outcome is TERMINAL
    assert verdict.blocking()
    assert verdict.reason.startswith(status.value)
    assert "GEM_IDENTITY_MISMATCH" in verdict.reason


def test_retry_is_never_produced_for_any_decision_the_gateway_can_make():
    """CNS's RETRY means the work may be re-rendered with an instructional
    delta. The repo models no such repair, so no decision maps to it."""
    base = _rejected_result()
    for status in DecisionStatus:
        if status is DecisionStatus.ACCEPTED:
            continue  # the contract forbids it without an accepted artifact; real one below
        decision = ConservationDecision(status, "REJECT", base.decision.rejections)
        verdict = to_cns_result(replace(base, decision=decision))
        assert verdict.outcome is not RETRY, status
    _, _, _, accepted = _accepted_result()
    assert to_cns_result(accepted).outcome is not RETRY


def test_every_decision_status_is_covered_by_the_documented_mapping():
    assert set(EXPECTED) == set(DecisionStatus)


def test_an_unknown_decision_status_fails_closed():
    base = _rejected_result()
    decision = ConservationDecision(DecisionStatus.REJECTED, None, ())
    object.__setattr__(decision, "status", "SURPRISE")
    verdict = to_cns_result(replace(base, decision=decision))
    assert verdict.outcome is TERMINAL


@pytest.mark.parametrize(
    "change",
    [{"state": TransportState.REJECTED}, {"state": TransportState.PROPOSED}],
    ids=["accepted-but-rejected-state", "accepted-but-proposed-state"],
)
def test_an_accepted_decision_that_is_not_a_coherent_acceptance_is_not_a_pass(change):
    _, _, _, result = _accepted_result()
    incoherent = replace(result, **change)
    assert incoherent.accepted  # the repo's own flag still says accepted
    verdict = to_cns_result(incoherent)
    assert verdict.outcome is TERMINAL
    assert "not coherent" in verdict.reason


def test_the_connector_agrees_with_the_gateway_on_every_attack_in_the_corpus():
    """The translation must not change what the gateway decided or did.

    Two identical gateways receive the same hostile proposal: one through
    ``submit``, one through the connector. The verdict follows the native
    decision, and both gateways end in the same state.
    """
    seen = set()
    for attack in ALL_ATTACKS:
        if attack is AttackType.DIRECT_DOWNSTREAM_INJECTION:
            continue  # never reaches submit; covered by the input gate tests
        # The repo's own corpus counts it blocked and expects REJECTED; the
        # connector must abort on it too, whichever refusal the gateway used.
        corpus = run_attack_case(attack)
        assert corpus.expected == "REJECTED" and corpus.blocked, attack
        _, native_gateway, request, proposal = _proposal(attack)
        _, conn_gateway, conn_request, conn_proposal = _proposal(attack)
        repeats = 2 if attack is AttackType.DUPLICATE_REPLAY else 1
        for _ in range(repeats):
            native = native_gateway.submit(request, proposal)
            verdict = submit_to_cns(conn_gateway, conn_request, conn_proposal)
        assert verdict.outcome is EXPECTED[native.decision.status], attack
        assert verdict.blocking() is (not native.accepted), attack
        assert _state(conn_gateway) == _state(native_gateway), attack
        assert verdict.outcome is TERMINAL, attack  # blocked by the corpus means abort here
        seen.add(verdict.outcome)
    assert seen == {TERMINAL}  # the corpus is hostile: everything is refused, nothing retries


def test_the_gateways_own_refusals_are_terminal_breaches():
    """These are refused by the gateway's preflight, whatever the kernel says."""
    for attack in (
        AttackType.IDENTITY_MISMATCH,
        AttackType.OUTPUT_SUBSTITUTION,
        AttackType.DUPLICATE_REPLAY,
    ):
        _, gateway, request, proposal = _proposal(attack)
        if attack is AttackType.DUPLICATE_REPLAY:
            assert gateway.submit(request, proposal).accepted
        assert submit_to_cns(gateway, request, proposal).outcome is TERMINAL, attack


def test_every_verdict_is_bound_to_the_transformation_it_judged():
    _, _, request, accepted = _accepted_result()
    rejected = _rejected_result()
    verdicts = [
        to_cns_result(accepted, subject="step-1"),
        to_cns_result(rejected, subject="step-1"),
    ]
    assert cns_gate.unbound(verdicts) == ()
    accepted_verdict = verdicts[0]
    digest = transformation_digest(accepted)
    assert accepted_verdict.binds("step-1", digest)
    # Transplanted onto a different transformation, another subject label, or
    # the same transformation with a different candidate, it does not bind.
    assert not accepted_verdict.binds("step-1", transformation_digest(rejected))
    assert not accepted_verdict.binds("step-2", digest)
    other_output = replace(
        accepted.candidate_artifact,
        content=accepted.candidate_artifact.content + " edited",
        content_digest=None,
        artifact_digest=None,  # recomputed, as the kernel does for any new artifact
    )
    assert not accepted_verdict.binds(
        "step-1", transformation_digest(replace(accepted, candidate_artifact=other_output))
    )


def test_the_digest_is_over_the_documented_content():
    """Pinned to the literal mapping: str-only, and ``source`` is the same
    id and digest the input gate binds."""
    source, _, request, result = _accepted_result()
    output = result.candidate_artifact
    expected = cns_gate.subject_digest(
        {
            "kind": "gems_transformation",
            "request_id": request.request_id,
            "transformation_id": result.transformation_id,
            "gem": request.gem.to_dict(),
            "source": {
                "artifact_id": source.artifact_id,
                "artifact_digest": source.artifact_digest,
                "relation": "PARENT",
            },
            "output_artifact": {
                "artifact_id": output.artifact_id,
                "artifact_digest": output.artifact_digest,
            },
            "record_digest": result.record.kernel_record.canonical_digest(),
        }
    )
    assert transformation_digest(result) == expected
    assert to_cns_result(result).subject_digest == expected
    assert input_digest(source) == cns_gate.subject_digest(
        {
            "kind": "gateway_input",
            "artifact_id": source.artifact_id,
            "artifact_digest": source.artifact_digest,
        }
    )


def test_a_result_the_kernel_cannot_digest_fails_closed_and_unbound():
    """A non-finite float in a declared change: the kernel builds the record,
    but neither it nor CNS can digest it. The gateway accepted; there is no
    way to bind that, so the connector does not say PASS."""
    _, _, _, result = _accepted_result()
    poisoned = replace(
        result.record.kernel_record,
        declared_changes=(
            DeclaredChange("x", Dimension.CONTENT, 1.0, float("nan"), "a non-finite declaration"),
        ),
    )
    hostile = replace(result, record=replace(result.record, kernel_record=poisoned))
    assert hostile.accepted  # the gateway's own flag is untouched
    verdict = to_cns_result(hostile)
    assert verdict.outcome is TERMINAL
    assert verdict.subject_digest == ""
    assert cns_gate.unbound([verdict]) == ("gateway_output",)
    assert "unbound" in verdict.reason
    with pytest.raises(ValueError):
        transformation_digest(hostile)


@pytest.mark.parametrize("missing", ["record", "candidate_artifact"])
def test_a_result_with_nothing_to_bind_to_is_never_a_pass(missing):
    _, _, _, accepted = _accepted_result()
    verdict = to_cns_result(replace(accepted, **{missing: None}))
    assert verdict.outcome is TERMINAL
    assert verdict.subject_digest == ""
    assert "unbound" in verdict.reason
    # A refusal with nothing to bind to stays a refusal, and unbound.
    refused = to_cns_result(replace(_rejected_result(), **{missing: None}))
    assert refused.outcome is TERMINAL
    assert cns_gate.unbound([refused]) == ("gateway_output",)


def test_to_cns_result_refuses_what_is_not_a_gateway_verdict():
    with pytest.raises(TypeError):
        to_cns_result("ACCEPTED")
    _, _, _, result = _accepted_result()
    with pytest.raises(ValueError):
        to_cns_result(result, subject="")


# --- the ALPHA end: the input gate ------------------------------------------


def test_an_accepted_artifact_passes_the_input_gate_at_the_alpha_end():
    source, gateway = _gateway()
    verdict = CnsInputGate(gateway).check(source)
    assert verdict.outcome is PASS
    assert verdict.position is cns_gate.GatePosition.ALPHA
    assert verdict.gate == "gateway_input"
    assert verdict.binds("input_artifact", input_digest(source))


def test_an_artifact_the_gateway_never_accepted_is_a_terminal_breach_at_the_alpha_end():
    source, gateway, request, proposal = _proposal(AttackType.DIRECT_DOWNSTREAM_INJECTION)
    injected = proposal.output_artifact
    verdict = CnsInputGate(gateway).check(injected)
    assert verdict.outcome is TERMINAL
    assert verdict.position is cns_gate.GatePosition.ALPHA
    assert "INPUT_GATE_REQUIRED" in verdict.reason
    assert injected.artifact_id in verdict.reason
    # The repo's own corpus reports the same attack with the same code.
    with pytest.raises(UnknownArtifact):
        gateway.resolve_artifact(injected.artifact_id)


def test_the_input_gate_binds_the_digest_not_only_the_id():
    source, gateway = _gateway()
    altered = Artifact(
        artifact_id=source.artifact_id,
        content=source.content + " (altered)",
        propositions=source.propositions,
        producer=source.producer,
        created_at=source.created_at,
    )
    assert altered.artifact_id == source.artifact_id
    assert altered.artifact_digest != source.artifact_digest
    verdict = CnsInputGate(gateway).check(altered)
    assert verdict.outcome is TERMINAL
    assert not verdict.binds("input_artifact", input_digest(source))
    assert verdict.binds("input_artifact", input_digest(altered))


class _CountingGem(SummarizerGem):
    """A reference Gem that records whether any work started."""

    started = 0

    def transform(self, request):
        type(self).started += 1
        return super().transform(request)


def test_the_input_gate_agrees_with_pipeline_and_the_gem_never_starts_on_a_refusal():
    def altered(source):
        return Artifact(
            artifact_id=source.artifact_id,
            content=source.content + " (altered)",
            propositions=source.propositions,
            producer=source.producer,
            created_at=source.created_at,
        )

    def never_accepted(source):
        gem = SummarizerGem(clock=fixed_clock)
        return gem.transform(gem.make_request(source)).output_artifact

    cases = {"accepted": lambda s: s, "never-accepted": never_accepted, "altered": altered}
    for name, build in cases.items():
        source, native_gateway = _gateway()
        _, conn_gateway = _gateway()
        candidate = build(source)
        verdict = CnsInputGate(conn_gateway).check(candidate)
        native_accepts = native_gateway.is_accepted(candidate)
        assert verdict.outcome is (PASS if native_accepts else TERMINAL), name

        _CountingGem.started = 0
        gem = _CountingGem(clock=fixed_clock)
        try:
            Pipeline(native_gateway).submit_one(gem, candidate)
            refused = False
        except BoundaryViolation:
            refused = True
        assert refused is (verdict.outcome is TERMINAL), name
        assert _CountingGem.started == (0 if refused else 1), name


def test_an_input_gate_judges_an_artifact_not_an_id_and_needs_a_real_bool():
    source, gateway = _gateway()
    with pytest.raises(TypeError):
        CnsInputGate(gateway).check(source.artifact_id)
    with pytest.raises(TypeError):
        input_to_cns_result("yes", source)  # truthy, but not the bool is_accepted returns
    with pytest.raises(TypeError):
        input_to_cns_result(True, source.artifact_id)
    with pytest.raises(ValueError):
        input_to_cns_result(True, source, subject="")
    assert input_to_cns_result(False, source).outcome is TERMINAL
    assert input_to_cns_result(True, source).outcome is PASS


# --- gates and the chain -----------------------------------------------------


def test_the_gates_satisfy_the_cns_gate_protocol_at_their_declared_ends():
    _, gateway = _gateway()
    input_gate, output_gate = CnsInputGate(gateway), CnsOutputGate(gateway)
    assert isinstance(input_gate, cns_gate.Gate) and isinstance(output_gate, cns_gate.Gate)
    assert input_gate.name == "gateway_input"
    assert input_gate.position is cns_gate.GatePosition.ALPHA
    assert output_gate.name == "gateway_output"
    assert output_gate.position is cns_gate.GatePosition.OMEGA


def test_the_output_gate_is_submit_it_promotes_and_a_second_check_is_a_duplicate():
    source, gateway = _gateway()
    gem = SummarizerGem(clock=fixed_clock)
    gateway.register_gem(gem.identity)
    request = gem.make_request(source)
    proposal = gem.transform(request)
    gate = CnsOutputGate(gateway)
    assert not gateway.is_accepted(proposal.output_artifact)
    first = gate.check(GatewaySubmission(request, proposal))
    assert first.outcome is PASS
    assert gateway.is_accepted(proposal.output_artifact)  # promoted, as submit does
    second = gate.check(GatewaySubmission(request, proposal))
    assert second.outcome is TERMINAL
    assert "DUPLICATE_TRANSFORMATION_ID" in second.reason


def test_submit_to_cns_is_the_output_gate():
    source, gateway = _gateway()
    _, other = _gateway()
    gem = SummarizerGem(clock=fixed_clock)
    for gw in (gateway, other):
        gw.register_gem(gem.identity)
    request = gem.make_request(source)
    proposal = gem.transform(request)
    direct = submit_to_cns(gateway, request, proposal, subject="s")
    through_gate = CnsOutputGate(other, subject="s").check(GatewaySubmission(request, proposal))
    assert direct == through_gate


def test_the_gates_refuse_a_candidate_of_the_wrong_kind():
    source, gateway = _gateway()
    with pytest.raises(TypeError):
        CnsOutputGate(gateway).check(source)
    with pytest.raises(TypeError):
        CnsOutputGate(gateway).check(None)
    with pytest.raises(TypeError):
        GatewaySubmission("a request", "a proposal")
    for build in (CnsInputGate, CnsOutputGate):
        with pytest.raises(ValueError):
            build(gateway, subject="")


def test_the_chain_has_both_ends_and_says_so():
    _, gateway = _gateway()
    chain = cns_chain(gateway)
    assert chain.misplaced() == ()
    assert len(chain.alpha) == 1 and len(chain.omega) == 1
    # Both slots are filled by the gateway's two real ends. That is all this
    # says: sequencing and "same request" are the consumer's job, and the two
    # gates take different candidates (see the gate tests above).
    assert chain.complete() is True


def test_the_five_gem_pipeline_passes_both_ends_at_every_step_and_agrees_with_pipeline():
    """Native ``Pipeline`` on one gateway; the CNS chain, step by step, on another."""
    native_source, native_gateway = _gateway()
    native_run = Pipeline(native_gateway).run(native_source, _gems())

    source, gateway = _gateway()
    chain = cns_chain(gateway)
    (input_gate,), (output_gate,) = chain.alpha, chain.omega
    current = source
    for gem in _gems():
        gateway.register_gem(gem.identity)
        alpha = input_gate.check(current)
        assert alpha.outcome is PASS  # the Gem may start
        request = gem.make_request(current)
        proposal = gem.transform(request)
        omega = output_gate.check(GatewaySubmission(request, proposal))
        assert omega.outcome is PASS
        assert cns_gate.resolve([alpha, omega]) is PASS
        assert cns_gate.unbound([alpha, omega]) == ()
        # The two digests are over different mappings, so they never compare
        # equal and a consumer cannot read "same request" off them. Here the
        # test itself ran both ends on one artifact, in order, and checks that
        # the artifact the input gate let through is the source named in the
        # request the output gate judged.
        assert alpha.subject_digest != omega.subject_digest
        accepted_source = gateway.resolve_artifact(request.source.artifact_id)
        assert alpha.binds("input_artifact", input_digest(accepted_source))
        current = gateway.resolve_artifact(proposal.output_artifact.artifact_id)

    assert current.artifact_digest == native_run.final_artifact.artifact_digest
    assert _state(gateway) == _state(native_gateway)
