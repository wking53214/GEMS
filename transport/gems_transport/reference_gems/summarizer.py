"""Deterministic summarizer reference Gem."""

from __future__ import annotations

from ..contracts import GemIdentity, TransformationProposal, TransformationRequest, utc_now
from .base import BaseGem


class SummarizerGem(BaseGem):
    def __init__(self, *, gem_id: str = "summarizer", version: str = "0.1", clock=None) -> None:
        super().__init__(
            GemIdentity(
                gem_id=gem_id,
                gem_version=version,
                implementation_id="gems.reference.summarizer.v0.1",
                role="summarizer",
                capabilities=("content-compression", "provenance-preservation"),
            ),
            clock=clock or utc_now,
        )

    def transform(self, request: TransformationRequest) -> TransformationProposal:
        source = request.input_artifact
        summary = " ".join(source.content.split())[:240]
        output = self._artifact(
            request,
            suffix="summary",
            content=f"Summary: {summary}",
        )
        return self._proposal(request, output)
