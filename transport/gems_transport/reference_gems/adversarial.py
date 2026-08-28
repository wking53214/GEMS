"""Hostile reference Gem used to attack the transport boundary."""

from __future__ import annotations

from dataclasses import replace
from enum import Enum

from conservation_kernel import (
    Artifact,
    AuthorityStatus,
    CanonicalState,
    EpistemicStatus,
    OriginStatus,
    Proposition,
    TemporalMetadata,
    TemporalScope,
    Uncertainty,
    UncertaintyState,
)
from conservation_kernel.events import TransformationRecord as KernelTransformationRecord

from ..artifact import LineageReference
from ..contracts import GemIdentity, TransformationProposal, TransformationRequest, utc_now
from .base import BaseGem


class AttackType(str, Enum):
    UNKNOWN_TO_FACT = "unknown-to-fact"
    INFERENCE_TO_FACT = "inference-to-fact"
    RECOMMENDATION_TO_DECISION = "recommendation-to-decision"
    AI_TO_HUMAN = "ai-output-to-human-origin"
    SOURCE_STRIPPING = "source-stripping"
    SOURCE_SUBSTITUTION = "source-substitution"
    FALSE_LINEAGE = "false-lineage"
    UNCERTAINTY_DELETION = "uncertainty-deletion"
    CONFLICT_DELETION = "conflict-deletion"
    FABRICATED_AUTHORIZATION = "fabricated-authorization"
    FABRICATED_VERIFICATION = "fabricated-independent-verification"
    HISTORICAL_REWRITE = "historical-timestamp-rewrite"
    CANONICAL_REWRITE = "canonical-state-rewrite"
    UNROOTED_ARTIFACT = "unrooted-artifact"
    DIRECT_DOWNSTREAM_INJECTION = "direct-downstream-injection"
    OUTPUT_SUBSTITUTION = "output-substitution"
    DUPLICATE_REPLAY = "duplicate-replay"
    METADATA_FORGERY = "metadata-forgery"
    PROVENANCE_MISMATCH = "provenance-mismatch"
    IDENTITY_MISMATCH = "identity-mismatch"


ALL_ATTACKS = tuple(AttackType)


class AdversarialGem(BaseGem):
    """A registered but untrusted Gem that deliberately emits bad proposals."""

    def __init__(self, *, clock=None) -> None:
        super().__init__(
            GemIdentity(
                gem_id="adversarial",
                gem_version="0.1",
                implementation_id="gems.reference.adversarial.v0.1",
                role="hostile-test-instrument",
                capabilities=("arbitrary-proposal", "attack-fixture"),
            ),
            clock=clock or utc_now,
        )

    def make_attack_request(self, input_artifact: Artifact, attack: AttackType) -> TransformationRequest:
        return self.make_request(
            input_artifact,
            transformation_type="HOSTILE_ATTACK",
            intent=f"deliberately attempt {attack.value}",
            request_suffix=attack.value,
            metadata={"attack": attack.value},
        )

    @staticmethod
    def _find(source: Artifact, proposition_id: str) -> Proposition:
        try:
            return source.proposition_map()[proposition_id]
        except KeyError as exc:
            raise KeyError(f"hostile fixture requires proposition {proposition_id}") from exc

    def _mutated(self, request: TransformationRequest, attack: AttackType) -> Artifact:
        source = request.input_artifact
        propositions = list(source.propositions)
        by_id = source.proposition_map()

        if attack is AttackType.UNKNOWN_TO_FACT:
            old = self._find(source, "p-unknown")
            propositions[propositions.index(old)] = replace(
                old,
                epistemic_status=EpistemicStatus.FACT,
                uncertainty=Uncertainty(UncertaintyState.NONE, ""),
                evidence_refs=("fake-proof",),
            )
        elif attack is AttackType.INFERENCE_TO_FACT:
            old = self._find(source, "p-inference")
            propositions[propositions.index(old)] = replace(
                old,
                epistemic_status=EpistemicStatus.FACT,
                uncertainty=Uncertainty(UncertaintyState.NONE, ""),
            )
        elif attack is AttackType.RECOMMENDATION_TO_DECISION:
            old = self._find(source, "p-recommendation")
            propositions[propositions.index(old)] = replace(
                old,
                epistemic_status=EpistemicStatus.DECISION,
                authority=AuthorityStatus.HUMAN_AUTHORIZED,
                authorization_refs=("fake-auth",),
            )
        elif attack is AttackType.AI_TO_HUMAN:
            old = self._find(source, "p-machine")
            propositions[propositions.index(old)] = replace(old, origin=OriginStatus.HUMAN_ORIGINATED)
        elif attack is AttackType.SOURCE_STRIPPING:
            old = self._find(source, "p-human-fact")
            propositions[propositions.index(old)] = replace(old, source_refs=())
        elif attack is AttackType.SOURCE_SUBSTITUTION:
            old = self._find(source, "p-human-fact")
            propositions[propositions.index(old)] = replace(old, source_refs=("forged-source",))
        elif attack is AttackType.FALSE_LINEAGE:
            return Artifact(
                artifact_id=f"{source.artifact_id}:attack-{attack.value}",
                content=f"Hostile false lineage for {source.content}",
                propositions=tuple(propositions),
                producer=self.identity.actor(),
                parent_artifact_ids=("forged-parent",),
                version=source.version + 1,
                functional_contract=source.functional_contract,
                created_at=request.created_at,
            )
        elif attack is AttackType.UNCERTAINTY_DELETION:
            old = self._find(source, "p-estimate")
            propositions[propositions.index(old)] = replace(old, uncertainty=Uncertainty(UncertaintyState.NONE, ""))
        elif attack is AttackType.CONFLICT_DELETION:
            old = self._find(source, "p-conflict")
            propositions[propositions.index(old)] = replace(
                old,
                uncertainty=Uncertainty(UncertaintyState.NONE, ""),
                evidence_refs=(),
            )
        elif attack is AttackType.FABRICATED_AUTHORIZATION:
            old = self._find(source, "p-recommendation")
            propositions[propositions.index(old)] = replace(
                old,
                epistemic_status=EpistemicStatus.DECISION,
                authority=AuthorityStatus.HUMAN_AUTHORIZED,
                authorization_refs=("fabricated-human-event",),
            )
        elif attack is AttackType.FABRICATED_VERIFICATION:
            old = self._find(source, "p-unknown")
            propositions[propositions.index(old)] = replace(
                old,
                epistemic_status=EpistemicStatus.FACT,
                uncertainty=Uncertainty(UncertaintyState.NONE, ""),
                evidence_refs=("fabricated-independent-check",),
            )
        elif attack is AttackType.HISTORICAL_REWRITE:
            old = self._find(source, "p-historical")
            propositions[propositions.index(old)] = replace(
                old,
                temporal=TemporalMetadata(
                    scope=TemporalScope.CURRENT,
                    occurred_at="2026-01-10T09:00:00Z",
                    observed_at="2026-01-10T09:01:00Z",
                ),
            )
        elif attack is AttackType.CANONICAL_REWRITE:
            old = self._find(source, "p-human-fact")
            propositions[propositions.index(old)] = replace(
                old,
                authority=AuthorityStatus.CANONICAL,
                canonical_state=CanonicalState.CANONICAL,
                authorization_refs=("fake-canonical-auth",),
            )
        elif attack is AttackType.UNROOTED_ARTIFACT:
            propositions.append(
                Proposition(
                    proposition_id="p-unrooted-fabrication",
                    text="A hostile Gem invented this proposition without a parent.",
                    epistemic_status=EpistemicStatus.INFERENCE,
                    origin=OriginStatus.MACHINE_ORIGINATED,
                    authority=AuthorityStatus.NONE,
                    uncertainty=Uncertainty(UncertaintyState.UNCERTAIN, "unrooted hostile claim"),
                    evidence_refs=("ev-source",),
                    canonical_state=CanonicalState.PROPOSED,
                    source_refs=("tie:synthetic",),
                    derivation_method="hostile-fabrication",
                )
            )
        elif attack is AttackType.METADATA_FORGERY:
            old = self._find(source, "p-machine")
            metadata = dict(old.metadata)
            metadata["verified"] = True
            propositions[propositions.index(old)] = replace(old, metadata=metadata)
        elif attack is AttackType.PROVENANCE_MISMATCH:
            old = self._find(source, "p-machine")
            propositions[propositions.index(old)] = replace(old, source_refs=("tie:synthetic", "unrelated-source"))
        elif attack in {
            AttackType.DIRECT_DOWNSTREAM_INJECTION,
            AttackType.OUTPUT_SUBSTITUTION,
            AttackType.DUPLICATE_REPLAY,
            AttackType.IDENTITY_MISMATCH,
        }:
            pass
        else:  # pragma: no cover - enum exhaustiveness guard
            raise AssertionError(f"unhandled attack {attack}")

        return Artifact(
            artifact_id=f"{source.artifact_id}:attack-{attack.value}",
            content=f"Hostile {attack.value}: {source.content}",
            propositions=tuple(propositions),
            producer=self.identity.actor(),
            parent_artifact_ids=(source.artifact_id,),
            version=source.version + 1,
            functional_contract=source.functional_contract,
            created_at=request.created_at,
        )

    def transform(self, request: TransformationRequest) -> TransformationProposal:
        attack = AttackType(request.metadata["attack"])
        output = self._mutated(request, attack)
        proposal = self._proposal(
            request,
            output,
            evidence_refs=tuple(
                ref for proposition in output.propositions for ref in proposition.evidence_refs
            ),
            authorization_refs=tuple(
                ref for proposition in output.propositions for ref in proposition.authorization_refs
            ),
            claimed_validation_results=("verified=true", "human_authorized=true")
            if attack in {AttackType.FABRICATED_AUTHORIZATION, AttackType.FABRICATED_VERIFICATION}
            else (),
            metadata={"attack": attack.value},
        )

        if attack is AttackType.OUTPUT_SUBSTITUTION:
            fake = LineageReference("substituted-output", "0" * 64, relation="OUTPUT")
            forged_kernel = replace(
                proposal.record.kernel_record,
                output_artifact_id=fake.artifact_id,
                output_hash=fake.artifact_digest,
            )
            forged_record = replace(proposal.record, output=fake, kernel_record=forged_kernel)
            return replace(proposal, record=forged_record)

        if attack is AttackType.IDENTITY_MISMATCH:
            forged_identity = GemIdentity(
                gem_id="forged-gem",
                gem_version="9.9",
                implementation_id="forged.implementation",
                role="forged",
            )
            forged_kernel = replace(proposal.record.kernel_record, transformer=forged_identity.actor())
            forged_record = replace(proposal.record, gem=forged_identity, kernel_record=forged_kernel)
            return replace(proposal, record=forged_record)

        return proposal


__all__ = ["ALL_ATTACKS", "AdversarialGem", "AttackType"]

