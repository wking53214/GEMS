from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable
from uuid import uuid4

from gems.contracts import Artifact, Handoff, Provenance, WorkflowStatus
from gems.core.handoff import HandoffValidator
from gems.core.router import Router


@dataclass
class WorkflowState:
    task_id: str = field(default_factory=lambda: str(uuid4()))
    status: WorkflowStatus = WorkflowStatus.CREATED
    baseline: tuple[Artifact, ...] = ()
    history: list[Handoff] = field(default_factory=list)


@dataclass(frozen=True)
class ExecutionResult:
    """Structured result for callers that need execution metadata."""

    task_id: str
    status: WorkflowStatus
    artifact_id: str
    artifact: Artifact
    provenance: Provenance | None
    execution_state: WorkflowStatus
    integrity: dict[str, object] = field(default_factory=dict)
    telemetry: dict[str, object] = field(default_factory=dict)
    verification_status: str = "not_performed"


class WorkflowCoordinator:
    """Minimal coordinator implementing recovered baseline/state/role coordination."""

    def __init__(self, router: Router, validator: HandoffValidator | None = None) -> None:
        self.router = router
        self.validator = validator or HandoffValidator()

    def execute(
        self,
        capability: str,
        artifact: Artifact,
        worker: Callable[[str, Artifact], Artifact],
        state: WorkflowState | None = None,
    ) -> tuple[WorkflowState, Artifact]:
        state, result = self.execute_enveloped(capability, artifact, worker, state)
        return state, result.artifact

    def execute_enveloped(
        self,
        capability: str,
        artifact: Artifact,
        worker: Callable[[str, Artifact], Artifact],
        state: WorkflowState | None = None,
    ) -> tuple[WorkflowState, ExecutionResult]:
        state = state or WorkflowState(baseline=(artifact,))
        route = self.router.route(capability)
        state.status = WorkflowStatus.RUNNING
        try:
            result = worker(route.gem, artifact)
            handoff = Handoff(
                task_id=state.task_id,
                sender=route.gem,
                recipient="workflow",
                artifacts=(result,),
                routing_signal=capability,
                workflow_state=state.status,
            )
            self.validator.validate(handoff)
        except Exception:
            state.status = WorkflowStatus.FAILED
            raise
        state.history.append(handoff)
        state.status = WorkflowStatus.COMPLETED
        return state, ExecutionResult(
            task_id=state.task_id,
            status=state.status,
            artifact_id=result.artifact_id,
            artifact=result,
            provenance=result.provenance,
            execution_state=state.status,
        )
