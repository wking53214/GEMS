"""Deterministic researcher reference Gem."""

from __future__ import annotations

from conservation_kernel import AuthorityStatus, CanonicalState, EpistemicStatus, OriginStatus, Uncertainty, UncertaintyState

from ..contracts import TransformationProposal, TransformationRequest, utc_now
from .base import BaseGem, create_gem_identity


class ResearcherGem(BaseGem):
    def __init__(self, *, evidence_ref: str = "ev-source", gem_id: str = "researcher", version: str = "0.1", clock=None) -> None:
        identity = create_gem_identity(
            gem_id=gem_id,
            version=version,
            role="researcher",
            capabilities=("derived-inference", "evidence-reference"),
        )
        super().__init__(identity, clock=clock or utc_now)
        self.evidence_ref = evidence_ref

    def transform(self, request: TransformationRequest) -> TransformationProposal:
        source = request.input_artifact
        parent = next(iter(source.propositions))
        derived = self.clone_proposition(
            parent,
            proposition_id=f"{source.artifact_id}:research-inference",
            text=f"Derived inference from {parent.proposition_id}: {parent.text}",
            epistemic_status=EpistemicStatus.INFERENCE,
            origin=OriginStatus.MACHINE_ORIGINATED,
            authority=AuthorityStatus.NONE,
            uncertainty=Uncertainty(UncertaintyState.UNCERTAIN, "deterministic derived inference"),
            evidence_refs=(self.evidence_ref,),
            authorization_refs=(),
            canonical_state=CanonicalState.PROPOSED,
            parent_proposition_ids=(parent.proposition_id,),
            derivation_method="deterministic-research-rule",
        )
        output = self._artifact(
            request,
            suffix="research",
            content=f"Research note: {source.content}",
            propositions=(*source.propositions, derived),
        )
        return self._proposal(request, output, evidence_refs=(self.evidence_ref,))
