"""Deterministic architecture proposal reference Gem."""

from __future__ import annotations

from conservation_kernel import AuthorityStatus, CanonicalState, EpistemicStatus, OriginStatus, Uncertainty, UncertaintyState

from ..contracts import GemIdentity, TransformationProposal, TransformationRequest, utc_now
from .base import BaseGem


class ArchitectureGem(BaseGem):
    def __init__(self, *, evidence_ref: str = "ev-source", gem_id: str = "architecture", version: str = "0.1", clock=None) -> None:
        super().__init__(
            GemIdentity(
                gem_id=gem_id,
                gem_version=version,
                implementation_id="gems.reference.architecture.v0.1",
                role="architecture",
                capabilities=("architecture-mapping", "functional-proposal"),
            ),
            clock=clock or utc_now,
        )
        self.evidence_ref = evidence_ref

    def transform(self, request: TransformationRequest) -> TransformationProposal:
        source = request.input_artifact
        parent = next(
            (item for item in reversed(source.propositions) if "requirement" in item.proposition_id),
            source.propositions[-1],
        )
        architecture = self.clone_proposition(
            parent,
            proposition_id=f"{source.artifact_id}:architecture",
            text=f"Architecture proposal for {parent.proposition_id}: retain explicit lineage.",
            epistemic_status=EpistemicStatus.INFERENCE,
            origin=OriginStatus.MACHINE_ORIGINATED,
            authority=AuthorityStatus.NONE,
            uncertainty=Uncertainty(UncertaintyState.UNCERTAIN, "architecture proposal requires review"),
            evidence_refs=(self.evidence_ref,),
            authorization_refs=(),
            canonical_state=CanonicalState.PROPOSED,
            parent_proposition_ids=(parent.proposition_id,),
            derivation_method="deterministic-architecture-mapping",
        )
        output = self._artifact(
            request,
            suffix="architecture",
            content=f"Architecture proposal derived from: {source.content}",
            propositions=(*source.propositions, architecture),
        )
        return self._proposal(request, output, evidence_refs=(self.evidence_ref,))
