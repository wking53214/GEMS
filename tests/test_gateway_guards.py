"""The gateway is only a boundary when its kernel and registry are guarded, and the guards come from the deployer.

``ConservationGateway`` builds a kernel and a registry unless it is given them. A kernel with no root guard
registers any root it admits, a registry with no evidence guard takes any evidence, and a registry with no trusted
humans takes an authorization from any actor that labels itself human. So the gateway needs the deployer's guards, or
a statement that going without them is on purpose. These tests hold that, and that the guards it is given are the
ones asked.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

pytest.importorskip(
    "conservation_kernel",
    reason="gems_transport needs conservation_kernel (its own dependency, not CNS)",
)

# ``transport/`` is not on the pytest path; see test_cns_transport_connector.py for the same reason.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "transport"))

from conservation_kernel import (  # noqa: E402
    Actor,
    AuthorizationEvent,
    ConservationKernel,
    EvidenceRecord,
    EvidenceRegistry,
)
from conservation_kernel.enums import EvidenceKind, TransitionKind  # noqa: E402
from conservation_kernel.errors import InvalidEvent, RootAdmissionError, UnguardedKernelError  # noqa: E402
from experiments.corpus import FIXED_TIME, fixed_clock, synthetic_tie_source  # noqa: E402
from gems_transport import ConservationGateway  # noqa: E402
from gems_transport.errors import InvalidContract  # noqa: E402

OPT_OUT = {"allow_unguarded_roots": True, "allow_unguarded_evidence": True}


def _approve(authorization_id: str, human: Actor) -> AuthorizationEvent:
    return AuthorizationEvent(
        authorization_id=authorization_id,
        authorized_by=human,
        subject_id="p-human-fact",
        transition_kind=TransitionKind.AUTHORITY_ESCALATION,
        from_value="NONE",
        to_value="HUMAN_AUTHORIZED",
        reason="a guard test",
        created_at=FIXED_TIME,
    )


def _evidence(evidence_id: str) -> EvidenceRecord:
    return EvidenceRecord(
        evidence_id=evidence_id,
        subject_id="p-human-fact",
        kind=EvidenceKind.SOURCE_OBSERVATION,
        provided_by=Actor.external("guard-test", "a guard test"),
        independent=True,
        active=True,
        detail={"fixture": "guard-test"},
        created_at=FIXED_TIME,
    )


def test_a_gateway_with_no_guards_and_no_statement_is_refused_at_construction():
    with pytest.raises(UnguardedKernelError):
        ConservationGateway()


def test_a_root_guard_alone_is_not_enough_because_the_registry_would_take_any_evidence():
    with pytest.raises(UnguardedKernelError):
        ConservationGateway(root_guard=lambda artifact: True)


def test_an_evidence_guard_alone_is_not_enough_because_the_kernel_would_register_any_root():
    with pytest.raises(UnguardedKernelError):
        ConservationGateway(evidence_guard=lambda record: True)


def test_a_gateway_with_both_guards_is_built_and_asks_the_root_guard_before_a_root():
    asked = []
    fixture = synthetic_tie_source()

    def root_guard(artifact):
        asked.append(artifact.artifact_id)
        return False

    # The fixture's registry holds the evidence the root cites, so admission passes and the guard is reached.
    gateway = ConservationGateway(registry=fixture.registry, root_guard=root_guard, allow_unguarded_evidence=True)
    with pytest.raises(RootAdmissionError):
        gateway.ingest_source(fixture.artifact)
    assert asked == [fixture.artifact.artifact_id]
    assert not gateway.is_accepted(fixture.artifact)


def test_a_root_guard_that_says_yes_lets_the_root_in():
    fixture = synthetic_tie_source()
    gateway = ConservationGateway(registry=fixture.registry, root_guard=lambda a: True, allow_unguarded_evidence=True)
    gateway.ingest_source(fixture.artifact)
    assert gateway.is_accepted(fixture.artifact)


def test_the_evidence_guard_it_is_given_is_the_one_asked_before_evidence_is_taken():
    asked = []

    def evidence_guard(record):
        asked.append(record.evidence_id)
        return record.evidence_id == "ev-allowed"

    gateway = ConservationGateway(evidence_guard=evidence_guard, allow_unguarded_roots=True)
    gateway.register_evidence(_evidence("ev-allowed"))
    with pytest.raises(Exception):  # noqa: B017 - the registry's own refusal; its type is the kernel's to name
        gateway.register_evidence(_evidence("ev-refused"))
    assert asked == ["ev-allowed", "ev-refused"]
    assert gateway.registry.evidence("ev-allowed") is not None
    assert gateway.registry.evidence("ev-refused") is None


def test_authorizations_are_refused_without_trusted_humans_unless_that_is_said_to_be_deliberate():
    gateway = ConservationGateway(**OPT_OUT)
    with pytest.raises(InvalidEvent):
        gateway.register_authorization(_approve("auth-1", Actor.human("someone")))

    deliberate = ConservationGateway(**OPT_OUT, allow_untrusted_humans=True)
    deliberate.register_authorization(_approve("auth-1", Actor.human("someone")))


def test_trusted_humans_it_is_given_decide_whose_authorization_counts():
    gateway = ConservationGateway(**OPT_OUT, trusted_humans={"alice"})
    gateway.register_authorization(_approve("auth-alice", Actor.human("alice")))
    with pytest.raises(InvalidEvent):
        gateway.register_authorization(_approve("auth-mallory", Actor.human("mallory")))


def test_guards_given_to_the_gateway_as_well_as_to_a_kernel_or_registry_it_is_given_are_refused():
    kernel = ConservationKernel(**OPT_OUT)
    with pytest.raises(InvalidContract):
        ConservationGateway(kernel=kernel, root_guard=lambda a: True)
    with pytest.raises(InvalidContract):
        ConservationGateway(kernel=kernel, allow_unguarded_roots=True)
    with pytest.raises(InvalidContract):
        ConservationGateway(kernel=kernel, evidence_guard=lambda r: True)
    with pytest.raises(InvalidContract):
        ConservationGateway(kernel=kernel, trusted_humans={"alice"})
    with pytest.raises(InvalidContract):
        ConservationGateway(kernel=kernel, allow_unguarded_evidence=True)
    with pytest.raises(InvalidContract):
        ConservationGateway(kernel=kernel, clock=fixed_clock)
    with pytest.raises(InvalidContract):
        ConservationGateway(registry=EvidenceRegistry(), evidence_guard=lambda r: True, **OPT_OUT)
    with pytest.raises(InvalidContract):
        ConservationGateway(registry=EvidenceRegistry(), allow_untrusted_humans=True, **OPT_OUT)


def test_a_kernel_the_caller_built_is_used_as_it_is():
    kernel = ConservationKernel(**OPT_OUT)
    gateway = ConservationGateway(kernel=kernel)
    assert gateway.kernel is kernel
    assert gateway.registry is kernel.registry


def test_the_clock_it_is_given_is_the_one_the_kernel_decides_at():
    gateway = ConservationGateway(**OPT_OUT, clock=fixed_clock)
    assert gateway.kernel.clock is fixed_clock
