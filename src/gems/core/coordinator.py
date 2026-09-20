"""Workflow coordinator for executing GEMS capabilities."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable
from uuid import uuid4

from gems.contracts import Artifact, Handoff, Provenance
from gems.core.registry import GemRegistry
from gems.core.router import Router, Route


class GemExecutor(ABC):
    """Abstract interface for executing a Gem capability."""

    @abstractmethod
    def execute(
        self,
        gem_name: str,
        capability: str,
        input_artifact: Artifact,
        context: dict[str, Any] | None = None,
    ) -> Artifact:
        """Execute a Gem and return result artifact.

        Args:
            gem_name: Name of the Gem to execute
            capability: The capability being requested
            input_artifact: Input artifact with provenance
            context: Optional workflow context

        Returns:
            Result Artifact with provenance tracking the execution
        """
        pass


class MockGemExecutor(GemExecutor):
    """Mock executor for testing - simulates Gem behavior without actual execution."""

    def __init__(self, quality_score: float = 0.85):
        self.quality_score = quality_score

    def execute(
        self,
        gem_name: str,
        capability: str,
        input_artifact: Artifact,
        context: dict[str, Any] | None = None,
    ) -> Artifact:
        """Return a simulated result."""
        result_content = f"{gem_name} processed: {input_artifact.content}"

        # Create provenance for the result
        parent_ids = (input_artifact.artifact_id,) if input_artifact.artifact_id else ()
        result_provenance = Provenance(
            source_id=gem_name,
            origin="ai",
            epistemic_status="inferred",
            authority="analysis",
            parent_ids=parent_ids,
            note=f"Result from {gem_name} executing {capability}",
        )

        return Artifact(
            content=result_content,
            provenance=result_provenance,
            metadata={
                "gem": gem_name,
                "capability": capability,
                "quality_score": self.quality_score,
            },
        )


class WorkflowCoordinator:
    """Coordinates execution of workflows by routing to and executing Gems."""

    def __init__(
        self,
        registry: GemRegistry,
        executor: GemExecutor | None = None,
        custom_executors: dict[str, Callable] | None = None,
    ):
        """Initialize coordinator.

        Args:
            registry: GemRegistry with available Gems
            executor: GemExecutor implementation (defaults to MockGemExecutor)
            custom_executors: Dict mapping gem_name to custom executor functions
        """
        self.registry = registry
        self.router = Router(registry)
        self.executor = executor or MockGemExecutor()
        self.custom_executors = custom_executors or {}
        self.execution_history: list[ExecutionRecord] = []

    def execute_capability(
        self,
        capability: str,
        input_artifact: Artifact,
        context: dict[str, Any] | None = None,
    ) -> Handoff:
        """Execute a capability by routing to appropriate Gem.

        Args:
            capability: The capability to execute
            input_artifact: Input artifact with provenance
            context: Optional workflow context

        Returns:
            Handoff with the result

        Raises:
            LookupError: If no Gem advertises the capability
        """
        context = context or {}

        # Route to appropriate Gem
        route = self.router.route(capability)

        # Execute the Gem
        if route.gem in self.custom_executors:
            result = self.custom_executors[route.gem](
                input_artifact, context
            )
            if not isinstance(result, Artifact):
                raise TypeError(
                    f"Custom executor for {route.gem} must return Artifact, got {type(result)}"
                )
        else:
            result = self.executor.execute(
                route.gem, capability, input_artifact, context
            )

        # Create handoff
        task_id = str(uuid4())
        handoff = Handoff(
            task_id=task_id,
            sender="coordinator",
            recipient=route.gem,
            artifacts=(result,),
        )

        # Record execution
        record = ExecutionRecord(
            task_id=task_id,
            capability=capability,
            route=route,
            input_artifact=input_artifact,
            output_artifact=result,
            handoff=handoff,
        )
        self.execution_history.append(record)

        return handoff

    def execute_workflow(
        self,
        workflow_steps: list[tuple[str, Artifact]],
        context: dict[str, Any] | None = None,
    ) -> tuple[list[Handoff], Artifact]:
        """Execute a multi-step workflow.

        Args:
            workflow_steps: List of (capability, initial_artifact) tuples
            context: Optional workflow context

        Returns:
            Tuple of (handoff_history, final_artifact)
        """
        context = context or {}
        handoff_history = []
        current_artifact = None

        for capability, artifact in workflow_steps:
            handoff = self.execute_capability(capability, artifact, context)
            handoff_history.append(handoff)
            current_artifact = handoff.artifacts[-1] if handoff.artifacts else artifact
            context[f"{capability}_result"] = current_artifact

        return handoff_history, current_artifact or workflow_steps[-1][1]


@dataclass(frozen=True)
class ExecutionRecord:
    """Record of a single Gem execution."""

    task_id: str
    capability: str
    route: Route
    input_artifact: Artifact
    output_artifact: Artifact
    handoff: Handoff
