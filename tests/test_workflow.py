import pytest

from gems.contracts import Artifact, EpistemicStatus, Origin, Provenance, WorkflowStatus
from gems.core.handoff import HandoffValidator
from gems.core.registry import GemRegistry
from gems.core.router import Router
from gems.core.workflow import WorkflowCoordinator, WorkflowState
from gems.contracts import GemSpec


def test_workflow_preserves_baseline_and_completes():
    registry = GemRegistry()
    registry.register(GemSpec("Research Analyst", "research", ("research",)))
    coordinator = WorkflowCoordinator(Router(registry), HandoffValidator())
    artifact = Artifact(content="input", provenance=Provenance("src", Origin.HUMAN, EpistemicStatus.EXPLICIT))

    state, result = coordinator.execute("research", artifact, lambda gem, a: a)

    assert state.status is WorkflowStatus.COMPLETED
    assert state.baseline == (artifact,)
    assert result == artifact
    assert len(state.history) == 1


def test_workflow_envelope_contains_execution_identity_and_provenance():
    registry = GemRegistry()
    registry.register(GemSpec("Research Analyst", "research", ("research",)))
    coordinator = WorkflowCoordinator(Router(registry), HandoffValidator())
    artifact = Artifact(content="input", provenance=Provenance("src", Origin.HUMAN, EpistemicStatus.EXPLICIT))

    state, result = coordinator.execute_enveloped("research", artifact, lambda gem, a: a)

    assert result.status is WorkflowStatus.COMPLETED
    assert result.execution_state is state.status
    assert result.task_id == state.task_id
    assert result.artifact_id == artifact.artifact_id
    assert result.provenance == artifact.provenance
    assert result.verification_status == "not_performed"
    assert result.integrity == {}
    assert result.telemetry == {}


def test_workflow_marks_failed_before_reraising_worker_error():
    registry = GemRegistry()
    registry.register(GemSpec("Research Analyst", "research", ("research",)))
    coordinator = WorkflowCoordinator(Router(registry), HandoffValidator())
    state = WorkflowState()
    artifact = Artifact(content="input", provenance=Provenance("src", Origin.HUMAN, EpistemicStatus.EXPLICIT))

    def failing_worker(gem, value):
        raise RuntimeError("worker failed")

    with pytest.raises(RuntimeError, match="worker failed"):
        coordinator.execute("research", artifact, failing_worker, state)

    assert state.status is WorkflowStatus.FAILED
    assert state.history == []
