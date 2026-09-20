from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from gems.contracts import Artifact, Handoff, WorkflowStatus


@dataclass
class WorkflowState:
    """Minimal workflow state for forensic analysis and audit trail tracking."""

    task_id: str = field(default_factory=lambda: str(uuid4()))
    status: WorkflowStatus = WorkflowStatus.COMPLETED
    baseline: tuple[Artifact, ...] = ()
    history: list[Handoff] = field(default_factory=list)
