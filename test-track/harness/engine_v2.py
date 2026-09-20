"""Workflow execution engine using REAL GEMS routing and coordination.

This engine exercises the actual GEMS execution path:
  WorkflowDefinition
    → Real Router
    → Real WorkflowCoordinator
    → MockGemExecutor (simulated Gem behavior)
    → Real Handoff
    → Metrics

Note: Gem outputs are simulated (MockGemExecutor), but routing,
coordination, and handoff tracking are REAL GEMS.
"""

import time
from typing import Dict, List, Any, Callable
from dataclasses import dataclass

from gems import (
    GemRegistry,
    GemSpec,
    WorkflowCoordinator,
    MockGemExecutor,
    Artifact,
    Provenance,
    Origin,
    EpistemicStatus,
    Authority,
)
from .metrics import GemMetrics, WorkflowMetrics


@dataclass
class WorkflowStep:
    """A single step in a workflow."""

    gem_name: str
    description: str
    capability: str
    required_inputs: List[str]
    provides_outputs: List[str]
    expected_duration: float  # seconds
    dependencies: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class WorkflowDefinition:
    """Definition of a complete workflow."""

    workflow_id: str
    classification: str  # e.g., "High complexity, multi-specialist"
    description: str
    steps: List[WorkflowStep]
    expected_duration: float  # seconds
    expected_specialist_count: int


@dataclass
class WorkflowExecution:
    """Results of a workflow execution."""

    workflow_id: str
    steps_executed: List[str]
    context_trail: Dict[str, Any]
    metrics: WorkflowMetrics


class RealGemsWorkflowEngine:
    """Executes workflows using REAL GEMS Router and Coordinator.

    Gem outputs are mocked, but routing and coordination are real.
    """

    def __init__(self, gem_specs: List[GemSpec]):
        """
        Initialize with a list of GemSpec definitions.

        Args:
            gem_specs: List of GemSpec objects defining available Gems
        """
        # Build registry from specs
        self.registry = GemRegistry()
        for spec in gem_specs:
            self.registry.register(spec)

        # Build real coordinator
        self.coordinator = WorkflowCoordinator(
            self.registry, executor=MockGemExecutor(quality_score=0.85)
        )
        self.execution_history: List[WorkflowExecution] = []

    def _execute_step(
        self, step: WorkflowStep, context: Dict[str, Any], metrics: WorkflowMetrics
    ) -> tuple[bool, str | None]:
        """Execute a single workflow step. Returns (success, error_msg)."""
        step_start = time.time()
        try:
            input_artifact = Artifact(
                content=f"Input for {step.capability}",
                provenance=Provenance(
                    source_id="workflow",
                    origin=Origin.AI,
                    epistemic_status=EpistemicStatus.INFERRED,
                    authority=Authority.ANALYSIS,
                ),
            )
            handoff = self.coordinator.execute_capability(
                step.capability, input_artifact, context
            )
            step_duration = time.time() - step_start

            result = handoff.artifacts[0]
            gem_metric = GemMetrics(
                gem_name=step.gem_name,
                duration_seconds=step_duration,
                routing_correct=handoff.recipient == step.gem_name,
                context_preserved=True,
                authority_respected=result.provenance is not None
                    and result.provenance.authority in (Authority.ANALYSIS, Authority.PROPOSAL),
                output_quality_score=result.metadata.get("quality_score", 0.85),
                errors=[],
            )
            metrics.gem_metrics[step.gem_name] = gem_metric
            metrics.gems_executed.append(step.gem_name)

            context[f"{step.capability}_result"] = result
            for output in step.provides_outputs:
                context[output] = result.content
            return True, None
        except LookupError as e:
            metrics.gem_metrics[step.gem_name] = GemMetrics(
                gem_name=step.gem_name,
                duration_seconds=time.time() - step_start,
                routing_correct=False,
                context_preserved=False,
                authority_respected=False,
                output_quality_score=0.0,
                errors=[str(e)],
            )
            return False, f"routing failed: {str(e)}"
        except Exception as e:
            metrics.gem_metrics[step.gem_name] = GemMetrics(
                gem_name=step.gem_name,
                duration_seconds=time.time() - step_start,
                routing_correct=False,
                context_preserved=False,
                authority_respected=False,
                output_quality_score=0.0,
                errors=[str(e)],
            )
            return False, f"failed: {str(e)}"

    def execute_workflow(
        self,
        workflow: WorkflowDefinition,
        custom_gem_executors: Dict[str, Callable] = None,
    ) -> WorkflowExecution:
        """Execute workflow using real GEMS execution path."""
        if custom_gem_executors is None:
            custom_gem_executors = {}

        start_time = time.time()
        context = {}
        steps_executed = []
        metrics = WorkflowMetrics(
            workflow_id=workflow.workflow_id,
            total_duration_seconds=0,
            gem_count=len(workflow.steps),
            gems_executed=[],
        )

        for step in workflow.steps:
            success, error = self._execute_step(step, context, metrics)
            if success:
                steps_executed.append(step.gem_name)
            else:
                metrics.success = False
                metrics.issues.append(f"Step {step.gem_name} {error}")

        total_time = time.time() - start_time
        metrics.total_duration_seconds = total_time
        metrics.calculate_aggregate_scores()
        if workflow.expected_duration > 0:
            metrics.efficiency_rating = workflow.expected_duration / total_time

        execution = WorkflowExecution(
            workflow_id=workflow.workflow_id,
            steps_executed=steps_executed,
            context_trail=context,
            metrics=metrics,
        )
        self.execution_history.append(execution)
        return execution

    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of all executions."""
        if not self.execution_history:
            return {"total_executions": 0}

        executions = self.execution_history

        return {
            "total_executions": len(executions),
            "successful": sum(1 for e in executions if e.metrics.success),
            "failed": sum(1 for e in executions if not e.metrics.success),
            "avg_routing_accuracy": sum(
                e.metrics.routing_accuracy for e in executions
            ) / len(executions),
            "avg_continuity": sum(
                e.metrics.continuity_preservation for e in executions
            ) / len(executions),
            "total_authority_violations": sum(
                e.metrics.authority_violations for e in executions
            ),
            "total_execution_time": sum(e.metrics.total_duration_seconds for e in executions),
        }
