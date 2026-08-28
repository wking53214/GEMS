"""Deterministic reviewer reference Gem."""

from __future__ import annotations

from conservation_kernel import AuthorityStatus, CanonicalState, EpistemicStatus, OriginStatus, Uncertainty, UncertaintyState

from ..contracts import GemIdentity, TransformationProposal, TransformationRequest, utc_now
from .base import BaseGem


class ReviewerGem(BaseGem):
    def __init__(self, *, evidence_ref: str = "ev-review-consensus", gem_id: str = "reviewer", version: str = "0.1", clock=None) -> None:
        super().__init__(
            GemIdentity(
                gem_id=gem_id,
                gem_version=version,
                implementation_id="gems.reference.reviewer.v0.1",
                role="reviewer",
                capabilities=("review", "recommendation"),
            ),
            clock=clock or utc_now,
        )
        self.evidence_ref = evidence_ref

    def transform(self, request: TransformationRequest) -> TransformationProposal:
        source = request.input_artifact
        parent = next(
            (item for item in reversed(source.propositions) if "architecture" in item.proposition_id),
            source.propositions[-1],
        )
        recommendation = self.clone_proposition(
            parent,
            proposition_id=f"{source.artifact_id}:recommendation",
            text=f"Recommendation: review {parent.proposition_id} before implementation.",
            epistemic_status=EpistemicStatus.RECOMMENDATION,
            origin=OriginStatus.MACHINE_ORIGINATED,
            authority=AuthorityStatus.NONE,
            uncertainty=Uncertainty(UncertaintyState.UNCERTAIN, "review recommendation is not a decision"),
            evidence_refs=(self.evidence_ref,),
            authorization_refs=(),
            canonical_state=CanonicalState.PROPOSED,
            parent_proposition_ids=(parent.proposition_id,),
            derivation_method=None,
        )
        output = self._artifact(
            request,
            suffix="review",
            content=f"Review findings derived from: {source.content}",
            propositions=(*source.propositions, recommendation),
        )
        return self._proposal(request, output, evidence_refs=(self.evidence_ref,))
