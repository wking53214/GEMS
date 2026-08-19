from gems.contracts import Artifact, EpistemicStatus, Origin, Provenance
from gems.core.handoff import HandoffValidator
from gems.core.registry import GemRegistry
from gems.core.router import Router
from gems.core.workflow import WorkflowCoordinator
from gems.contracts import GemSpec


def test_workflow_preserves_baseline_and_completes():
    registry = GemRegistry()
    registry.register(GemSpec("Research Analyst", "research", ("research",)))
    coordinator = WorkflowCoordinator(Router(registry), HandoffValidator())
    artifact = Artifact(content="input", provenance=Provenance("src", Origin.HUMAN, EpistemicStatus.EXPLICIT))

    state, result = coordinator.execute("research", artifact, lambda gem, a: a)

    assert state.status == "completed"
    assert state.baseline == (artifact,)
    assert result == artifact
    assert len(state.history) == 1
