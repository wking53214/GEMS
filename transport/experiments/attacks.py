"""Hostile corpus execution against the actual GEMS gateway."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from gems_transport import ConservationGateway
from gems_transport.errors import UnknownArtifact
from gems_transport.reference_gems import AdversarialGem, ALL_ATTACKS, AttackType

from .corpus import fixed_clock, synthetic_tie_source


@dataclass(frozen=True)
class AttackOutcome:
    attack: str
    expected: str
    actual: str
    accepted: bool
    blocked: bool
    bypassed: bool
    rejection_codes: tuple[str, ...]
    transformation_id: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "attack": self.attack,
            "expected": self.expected,
            "actual": self.actual,
            "accepted": self.accepted,
            "blocked": self.blocked,
            "bypassed": self.bypassed,
            "rejection_codes": list(self.rejection_codes),
            "transformation_id": self.transformation_id,
        }


def run_attack_case(attack: AttackType) -> AttackOutcome:
    fixture = synthetic_tie_source()
    gateway = ConservationGateway(registry=fixture.registry)
    gateway.ingest_source(fixture.artifact)
    gem = AdversarialGem(clock=fixed_clock)
    gateway.register_gem(gem.identity)
    request = gem.make_attack_request(fixture.artifact, attack)
    proposal = gem.transform(request)

    if attack is AttackType.DIRECT_DOWNSTREAM_INJECTION:
        try:
            gateway.resolve_artifact(proposal.output_artifact.artifact_id)
        except UnknownArtifact:
            return AttackOutcome(
                attack=attack.value,
                expected="NOT_ACCEPTED_BY_GATE",
                actual="NOT_ACCEPTED_BY_GATE",
                accepted=False,
                blocked=True,
                bypassed=True,
                rejection_codes=("INPUT_GATE_REQUIRED",),
                transformation_id=proposal.record.transformation_id,
            )
        return AttackOutcome(
            attack=attack.value,
            expected="NOT_ACCEPTED_BY_GATE",
            actual="ACCEPTED",
            accepted=True,
            blocked=False,
            bypassed=True,
            rejection_codes=(),
            transformation_id=proposal.record.transformation_id,
        )

    if attack is AttackType.DUPLICATE_REPLAY:
        first = gateway.submit(request, proposal)
        assert first.accepted, first.to_dict()
        result = gateway.submit(request, proposal)
    else:
        result = gateway.submit(request, proposal)
    codes = tuple(item.code for item in result.decision.rejections)
    return AttackOutcome(
        attack=attack.value,
        expected="REJECTED",
        actual=result.decision.status.value,
        accepted=result.accepted,
        blocked=not result.accepted,
        bypassed=False,
        rejection_codes=codes,
        transformation_id=result.transformation_id,
    )


def run_hostile_corpus() -> tuple[AttackOutcome, ...]:
    return tuple(run_attack_case(attack) for attack in ALL_ATTACKS)


def control_outcomes() -> tuple[dict[str, Any], ...]:
    """Conventional baseline: candidate outputs are treated as accepted data.

    This is deliberately not a claim about all conventional systems.  It is a
    deterministic control fixture for later comparative experiments.
    """

    fixture = synthetic_tie_source()
    gem = AdversarialGem(clock=fixed_clock)
    outcomes: list[dict[str, Any]] = []
    for attack in ALL_ATTACKS:
        request = gem.make_attack_request(fixture.artifact, attack)
        proposal = gem.transform(request)
        outcomes.append({
            "attack": attack.value,
            "accepted": True,
            "actual": "ACCEPTED_BY_CONTROL",
            "artifact_id": proposal.output_artifact.artifact_id,
        })
    return tuple(outcomes)

