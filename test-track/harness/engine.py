"""Workflow execution engine for GEMS."""

import time
from typing import Dict, List, Any, Callable
from dataclasses import dataclass
from .metrics import GemMetrics, WorkflowMetrics


@dataclass
class WorkflowStep:
    """A single step in a workflow."""
    gem_name: str
    description: str
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
    context_trail: Dict[str, Any]  # Track context through steps
    metrics: WorkflowMetrics


class WorkflowEngine:
    """Executes workflows and collects metrics."""

    def __init__(self, gems_catalog: Dict[str, str]):
        """
        Initialize with a catalog of available gems.

        Args:
            gems_catalog: Dict of {gem_name: gem_description}
        """
        self.gems_catalog = gems_catalog
        self.execution_history: List[WorkflowExecution] = []

    def execute_workflow(
        self,
        workflow: WorkflowDefinition,
        gem_executors: Dict[str, Callable] = None,
    ) -> WorkflowExecution:
        """
        Execute a complete workflow.

        Args:
            workflow: WorkflowDefinition to execute
            gem_executors: Dict of {gem_name: executor_function}
                          Executor should return a dict with execution results

        Returns:
            WorkflowExecution with results and metrics
        """
        if gem_executors is None:
            gem_executors = {}

        start_time = time.time()
        context = {}
        steps_executed = []
        metrics = WorkflowMetrics(
            workflow_id=workflow.workflow_id,
            total_duration_seconds=0,
            gem_count=len(workflow.steps),
            gems_executed=[],
        )

        # Execute each step
        for step in workflow.steps:
            step_start = time.time()

            # Check if gem is in catalog (routing correctness)
            routing_correct = step.gem_name in self.gems_catalog

            # Check if dependencies are met (context preservation)
            context_preserved = all(
                dep in context or dep in [s.gem_name for s in workflow.steps[:workflow.steps.index(step)]]
                for dep in step.dependencies
            )

            # Get or create executor for this gem
            if step.gem_name in gem_executors:
                executor = gem_executors[step.gem_name]
            else:
                # Default executor: simulate gem execution
                executor = self._default_executor

            # Execute the gem
            try:
                result = executor(
                    gem_name=step.gem_name,
                    description=step.description,
                    context=context,
                    inputs=step.required_inputs,
                )

                # Update context with outputs
                for output in step.provides_outputs:
                    context[output] = result.get(output, f"output_{output}")

                step_duration = time.time() - step_start

                # Check authority respect (all gems stayed in their role)
                authority_respected = result.get("authority_respected", True)

                # Get output quality score
                quality_score = result.get("quality_score", 0.8)

                # Record gem metrics
                gem_metric = GemMetrics(
                    gem_name=step.gem_name,
                    duration_seconds=step_duration,
                    routing_correct=routing_correct,
                    context_preserved=context_preserved,
                    authority_respected=authority_respected,
                    output_quality_score=quality_score,
                    errors=result.get("errors", []),
                )

                metrics.gem_metrics[step.gem_name] = gem_metric
                metrics.gems_executed.append(step.gem_name)
                steps_executed.append(step.gem_name)

            except Exception as e:
                # Record failure
                gem_metric = GemMetrics(
                    gem_name=step.gem_name,
                    duration_seconds=time.time() - step_start,
                    routing_correct=routing_correct,
                    context_preserved=context_preserved,
                    authority_respected=False,
                    output_quality_score=0.0,
                    errors=[str(e)],
                )
                metrics.gem_metrics[step.gem_name] = gem_metric
                metrics.success = False
                metrics.issues.append(f"Step {step.gem_name} failed: {str(e)}")

        # Calculate aggregate metrics
        total_time = time.time() - start_time
        metrics.total_duration_seconds = total_time
        metrics.calculate_aggregate_scores()

        # Calculate efficiency (actual time vs expected time)
        if workflow.expected_duration > 0:
            metrics.efficiency_rating = workflow.expected_duration / total_time

        # Create and record execution
        execution = WorkflowExecution(
            workflow_id=workflow.workflow_id,
            steps_executed=steps_executed,
            context_trail=context,
            metrics=metrics,
        )

        self.execution_history.append(execution)
        return execution

    @staticmethod
    def _default_executor(
        gem_name: str,
        description: str,
        context: Dict[str, Any],
        inputs: List[str],
    ) -> Dict[str, Any]:
        """
        Default executor for gems. Simulates execution.

        Returns a dict with:
        - All inputs as outputs (passed through)
        - authority_respected: bool
        - quality_score: float (0-1)
        - errors: list
        """
        return {
            "authority_respected": True,
            "quality_score": 0.85,
            "errors": [],
            **{f"output_{inp}": f"{gem_name}_{inp}" for inp in inputs},
        }

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
