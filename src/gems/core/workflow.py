from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable
from uuid import uuid4

from gems.contracts import Artifact, Handoff
from gems.core.handoff import HandoffValidator
from gems.core.router import Router


@dataclass
class WorkflowState:
    task_id: str = field(default_factory=lambda: str(uuid4()))
    status: str = "created"
    baseline: tuple[Artifact, ...] = ()
    history: list[Handoff] = field(default_factory=list)


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
        state = state or WorkflowState(baseline=(artifact,))
        route = self.router.route(capability)
        state.status = "running"
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
        state.history.append(handoff)
        state.status = "completed"
        return state, result
