"""Synthetic source and external witness fixtures for deterministic tests.

This module is deliberately not TIE.  It creates a small artifact that has
the shape required by the current conservation kernel so the future TIE
handoff can be tested without pretending that TIE exists.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from conservation_kernel import (
    Actor,
    ActorKind,
    Artifact,
    AuthorizationEvent,
    AuthorityStatus,
    CanonicalState,
    EpistemicStatus,
    EvidenceKind,
    EvidenceRecord,
    EvidenceRegistry,
    OriginStatus,
    Proposition,
    TemporalMetadata,
    TemporalScope,
    TransitionKind,
    Uncertainty,
    UncertaintyState,
)

from gems_transport.artifact import AuthorityReference
from gems_transport.contracts import GemIdentity, TransformationProposal, TransformationRequest, utc_now
from gems_transport.reference_gems.base import BaseGem


FIXED_TIME = "2026-01-10T10:00:00Z"


def fixed_clock() -> str:
    return FIXED_TIME


@dataclass(frozen=True)
class SyntheticTIESource:
    """Synthetic future-TIE handoff; no TIE code is used."""

    artifact: Artifact
    registry: EvidenceRegistry


def _evidence(
    registry: EvidenceRegistry,
    evidence_id: str,
    kind: EvidenceKind,
    provided_by: Actor,
    *,
    independent: bool = False,
) -> None:
    registry.add_evidence(
        EvidenceRecord(
            evidence_id=evidence_id,
            subject_id="*",
            kind=kind,
            provided_by=provided_by,
            independent=independent,
            active=True,
            detail={"fixture": "synthetic-not-TIE"},
            created_at=FIXED_TIME,
        )
    )


def synthetic_tie_source() -> SyntheticTIESource:
    registry = EvidenceRegistry()
    external = Actor.external("synthetic-source-observer", "synthetic future-TIE fixture")
    model = Actor.model("synthetic-model", "reference Gem fixture")
    _evidence(registry, "ev-source", EvidenceKind.SOURCE_OBSERVATION, external, independent=True)
    _evidence(registry, "ev-conflict", EvidenceKind.CITATION, external)
    _evidence(registry, "ev-review-consensus", EvidenceKind.MODEL_CONSENSUS, model)

    source_ref = ("tie:synthetic:segment-001",)
    propositions = (
        Proposition(
            proposition_id="p-human-fact",
            text="The source records 42 active sessions.",
            epistemic_status=EpistemicStatus.FACT,
            origin=OriginStatus.HUMAN_ORIGINATED,
            authority=AuthorityStatus.NONE,
            evidence_refs=("ev-source",),
            source_refs=source_ref,
            temporal=TemporalMetadata(
                scope=TemporalScope.CURRENT,
                occurred_at="2026-01-10T09:05:00Z",
                observed_at="2026-01-10T09:05:02Z",
            ),
        ),
        Proposition(
            proposition_id="p-unknown",
            text="The cause of the second spike is unknown.",
            epistemic_status=EpistemicStatus.UNKNOWN,
            origin=OriginStatus.EXTERNAL_ORIGINATED,
            uncertainty=Uncertainty(UncertaintyState.UNKNOWN, "no independent observation yet"),
            source_refs=source_ref,
        ),
        Proposition(
            proposition_id="p-inference",
            text="The first spike may be related to a deployment.",
            epistemic_status=EpistemicStatus.INFERENCE,
            origin=OriginStatus.MACHINE_ORIGINATED,
            uncertainty=Uncertainty(UncertaintyState.UNCERTAIN, "derived from timing correlation"),
            evidence_refs=("ev-source",),
            source_refs=source_ref,
            derivation_method="synthetic-correlation-rule",
        ),
        Proposition(
            proposition_id="p-recommendation",
            text="Review deployment timing before changing capacity.",
            epistemic_status=EpistemicStatus.RECOMMENDATION,
            origin=OriginStatus.MACHINE_ORIGINATED,
            authority=AuthorityStatus.PROPOSED,
            uncertainty=Uncertainty(UncertaintyState.UNCERTAIN, "recommendation requires human decision"),
            evidence_refs=("ev-review-consensus",),
            source_refs=source_ref,
        ),
        Proposition(
            proposition_id="p-machine",
            text="A machine-generated inference is present in the source package.",
            epistemic_status=EpistemicStatus.INFERENCE,
            origin=OriginStatus.MACHINE_ORIGINATED,
            uncertainty=Uncertainty(UncertaintyState.UNCERTAIN, "machine-generated source inference"),
            evidence_refs=("ev-source",),
            source_refs=source_ref,
            derivation_method="synthetic-source-rule",
        ),
        Proposition(
            proposition_id="p-estimate",
            text="Estimated load is between 35 and 50 sessions.",
            epistemic_status=EpistemicStatus.ESTIMATED,
            origin=OriginStatus.MACHINE_ORIGINATED,
            uncertainty=Uncertainty(UncertaintyState.UNCERTAIN, "sample estimate"),
            evidence_refs=("ev-source",),
            source_refs=source_ref,
            derivation_method="synthetic-sample-estimate",
        ),
        Proposition(
            proposition_id="p-conflict",
            text="Two source notes disagree about the second spike.",
            epistemic_status=EpistemicStatus.CONFLICTED,
            origin=OriginStatus.EXTERNAL_ORIGINATED,
            uncertainty=Uncertainty(UncertaintyState.CONFLICTED, "source notes disagree"),
            evidence_refs=("ev-conflict",),
            source_refs=source_ref,
        ),
        Proposition(
            proposition_id="p-historical",
            text="The earlier incident occurred during the January maintenance window.",
            epistemic_status=EpistemicStatus.FACT,
            origin=OriginStatus.EXTERNAL_ORIGINATED,
            evidence_refs=("ev-source",),
            source_refs=source_ref,
            temporal=TemporalMetadata(
                scope=TemporalScope.HISTORICAL,
                occurred_at="2026-01-02T03:00:00Z",
                observed_at="2026-01-02T03:10:00Z",
            ),
        ),
        Proposition(
            proposition_id="p-simulation",
            text="A simulated capacity increase would reduce queue depth.",
            epistemic_status=EpistemicStatus.SIMULATED,
            origin=OriginStatus.MACHINE_ORIGINATED,
            uncertainty=Uncertainty(UncertaintyState.UNCERTAIN, "simulation input assumptions"),
            source_refs=source_ref,
            derivation_method="synthetic-capacity-simulation",
            temporal=TemporalMetadata(scope=TemporalScope.SIMULATION),
        ),
    )
    artifact = Artifact(
        artifact_id="synthetic-tie-source",
        content=(
            "Synthetic TIE-like source package. It contains a fact, unknown, "
            "inference, recommendation, estimate, conflict, historical state, "
            "and simulation for hostile transport testing."
        ),
        propositions=propositions,
        producer=Actor.external("synthetic-tie-handoff", "future TIE handoff fixture"),
        created_at=FIXED_TIME,
    )
    return SyntheticTIESource(artifact, registry)


class HumanApprovalFixture(BaseGem):
    """Synthetic external human authorization fixture, not a Gem implementation."""

    identity = GemIdentity(
        gem_id="human-approval-fixture",
        gem_version="0.1",
        implementation_id="gems.fixture.human-approval-boundary.v0.1",
        role="external-human-approval-fixture",
        capabilities=("explicit-authorization-event",),
        actor_kind=ActorKind.SYSTEM,
    )

    def __init__(self, *, clock: Callable[[], str] = fixed_clock) -> None:
        super().__init__(self.identity, clock=clock)

    @staticmethod
    def register_recommendation_authorization(registry: EvidenceRegistry, proposition_id: str) -> tuple[str, ...]:
        human = Actor.human("synthetic-human-approver", "explicit test fixture human")
        events = (
            AuthorizationEvent(
                authorization_id="auth-recommendation-decision",
                authorized_by=human,
                subject_id=proposition_id,
                transition_kind=TransitionKind.AUTHORITY_ESCALATION,
                from_value=EpistemicStatus.RECOMMENDATION.value,
                to_value=EpistemicStatus.DECISION.value,
                reason="synthetic human approves the recommendation as a decision",
                created_at=FIXED_TIME,
            ),
            AuthorizationEvent(
                authorization_id="auth-proposed-human-authorized",
                authorized_by=human,
                subject_id=proposition_id,
                transition_kind=TransitionKind.AUTHORITY_ESCALATION,
                from_value=AuthorityStatus.PROPOSED.value,
                to_value=AuthorityStatus.HUMAN_AUTHORIZED.value,
                reason="synthetic human grants decision authority",
                created_at=FIXED_TIME,
            ),
            AuthorizationEvent(
                authorization_id="auth-approved-canonical",
                authorized_by=human,
                subject_id=proposition_id,
                transition_kind=TransitionKind.CANONICALIZATION,
                from_value=CanonicalState.PROPOSED.value,
                to_value=CanonicalState.CANONICAL.value,
                reason="synthetic human approves the result as canonical for the fixture",
                created_at=FIXED_TIME,
            ),
        )
        for event in events:
            registry.add_authorization(event)
        return tuple(item.authorization_id for item in events)

    def authorize(self, registry: EvidenceRegistry, artifact: Artifact) -> TransformationProposal:
        proposition_id = "p-recommendation"
        authorizations = self.register_recommendation_authorization(registry, proposition_id)
        source = artifact.proposition_map()[proposition_id]
        approved = self.clone_proposition(
            source,
            epistemic_status=EpistemicStatus.DECISION,
            authority=AuthorityStatus.HUMAN_AUTHORIZED,
            canonical_state=CanonicalState.CANONICAL,
            authorization_refs=authorizations,
        )
        propositions = tuple(approved if item.proposition_id == proposition_id else item for item in artifact.propositions)
        request = self.make_request(
            artifact,
            transformation_type="HUMAN_APPROVAL",
            intent="apply externally registered human authorization to the recommendation",
            request_suffix="canonical-approval",
        )
        output = self._artifact(
            request,
            suffix="canonical-approved",
            content=f"Human-approved canonical result: {artifact.content}",
            propositions=propositions,
        )
        authority_refs = tuple(
            AuthorityReference(
                authorization_id=authorization_id,
                subject_id=proposition_id,
                transition_kind=(
                    TransitionKind.CANONICALIZATION
                    if authorization_id == "auth-approved-canonical"
                    else TransitionKind.AUTHORITY_ESCALATION
                ),
            )
            for authorization_id in authorizations
        )
        return self._proposal(
            request,
            output,
            evidence_refs=("ev-source",),
            authorization_refs=authorizations,
            authority_refs=authority_refs,
        )

