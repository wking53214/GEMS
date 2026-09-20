"""Deterministic requirements extraction reference Gem."""

from __future__ import annotations

from conservation_kernel import AuthorityStatus, CanonicalState, EpistemicStatus, OriginStatus, Uncertainty, UncertaintyState

from ..contracts import TransformationProposal, TransformationRequest, utc_now
from .base import BaseGem, create_gem_identity


class RequirementsGem(BaseGem):
    def __init__(self, *, evidence_ref: str = "ev-source", gem_id: str = "requirements", version: str = "0.1", clock=None) -> None:
        identity = create_gem_identity(
            gem_id=gem_id,
            version=version,
            role="requirements",
            capabilities=("requirement-extraction", "source-lineage"),
        )
        super().__init__(identity, clock=clock or utc_now)
        self.evidence_ref = evidence_ref

    def transform(self, request: TransformationRequest) -> TransformationProposal:
        source = request.input_artifact
        parent = next(iter(source.propositions))
        requirement = self.clone_proposition(
            parent,
            proposition_id=f"{source.artifact_id}:requirement",
            text=f"Requirement candidate: preserve {parent.proposition_id} without changing its epistemic status.",
            epistemic_status=EpistemicStatus.INFERENCE,
            origin=OriginStatus.MACHINE_ORIGINATED,
            authority=AuthorityStatus.NONE,
            uncertainty=Uncertainty(UncertaintyState.UNCERTAIN, "candidate requirement requires human review"),
            evidence_refs=(self.evidence_ref,),
            authorization_refs=(),
            canonical_state=CanonicalState.PROPOSED,
            parent_proposition_ids=(parent.proposition_id,),
            derivation_method="deterministic-requirement-mapping",
        )
        output = self._artifact(
            request,
            suffix="requirements",
            content=f"Requirements candidates derived from: {source.content}",
            propositions=(*source.propositions, requirement),
        )
        return self._proposal(request, output, evidence_refs=(self.evidence_ref,))
