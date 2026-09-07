"""Sequential Gem orchestration through the conservation gateway."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from conservation_kernel import Artifact

from .contracts import GemTransformer, TransformationResult
from .errors import BoundaryViolation, PipelineRejected
from .transport import ConservationGateway


@dataclass(frozen=True)
class PipelineRun:
    source_artifact: Artifact
    final_artifact: Artifact
    results: tuple[TransformationResult, ...]

    @property
    def accepted(self) -> bool:
        return all(item.accepted for item in self.results)

    @property
    def rejected_results(self) -> tuple[TransformationResult, ...]:
        return tuple(item for item in self.results if not item.accepted)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_artifact_id": self.source_artifact.artifact_id,
            "final_artifact_id": self.final_artifact.artifact_id,
            "accepted": self.accepted,
            "results": [item.to_dict() for item in self.results],
        }


class Pipeline:
    """Only passes accepted gateway outputs to the next Gem."""

    def __init__(self, gateway: ConservationGateway) -> None:
        self.gateway = gateway

    def execute(self, source_artifact: Artifact, gems: list[GemTransformer] | tuple[GemTransformer, ...]) -> PipelineRun:
        current = self.gateway.ingest_source(source_artifact)
        results: list[TransformationResult] = []
        for gem in gems:
            self.gateway.register_gem(gem.identity)
            if not self.gateway.is_accepted(current):
                raise BoundaryViolation(
                    f"pipeline refused to pass non-accepted artifact {current.artifact_id} to {gem.identity.key}"
                )
            request = gem.make_request(current)
            proposal = gem.transform(request)
            result = self.gateway.submit(request, proposal)
            results.append(result)
            if not result.accepted:
                return PipelineRun(source_artifact, current, tuple(results))
            current = result.accepted_artifact
        return PipelineRun(source_artifact, current, tuple(results))

    def run(self, source_artifact: Artifact, gems: list[GemTransformer] | tuple[GemTransformer, ...]) -> PipelineRun:
        result = self.execute(source_artifact, gems)
        if not result.accepted:
            raise PipelineRejected(result.rejected_results[-1])
        return result

    def submit_one(self, gem: GemTransformer, artifact: Artifact, *, request_kwargs: dict[str, Any] | None = None) -> TransformationResult:
        """Apply one Gem only when the supplied artifact is gateway-accepted."""

        if not self.gateway.is_accepted(artifact):
            raise BoundaryViolation(f"input gate refused artifact {artifact.artifact_id}")
        self.gateway.register_gem(gem.identity)
        request = gem.make_request(artifact, **(request_kwargs or {}))
        return self.gateway.submit(request, gem.transform(request))

