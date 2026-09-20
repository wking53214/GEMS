"""Integration tests for WorkflowCoordinator with real Router."""

import pytest

from gems.contracts import (
    Artifact,
    Authority,
    EpistemicStatus,
    GemSpec,
    Origin,
    Provenance,
)
from gems.core.coordinator import (
    ExecutionRecord,
    MockGemExecutor,
    WorkflowCoordinator,
)
from gems.core.registry import GemRegistry


@pytest.fixture
def registry_with_gems():
    """Create a registry with test Gems."""
    registry = GemRegistry()

    # Register test Gems
    registry.register(GemSpec(
        name="analyzer",
        purpose="Analyzes input",
        capabilities=("analyze", "investigate"),
    ))
    registry.register(GemSpec(
        name="reviewer",
        purpose="Reviews content",
        capabilities=("review", "audit"),
    ))
    registry.register(GemSpec(
        name="summarizer",
        purpose="Summarizes content",
        capabilities=("summarize", "condense"),
    ))

    return registry


@pytest.fixture
def provenance_base():
    """Create base provenance for test artifacts."""
    return Provenance(
        source_id="test_user",
        origin=Origin.HUMAN,
        epistemic_status=EpistemicStatus.EXPLICIT,
        authority=Authority.OBSERVATION,
    )


class TestWorkflowCoordinatorRouting:
    """Test WorkflowCoordinator routing to correct Gems."""

    def test_routes_to_capability_match(self, registry_with_gems, provenance_base):
        """Coordinator routes to Gem advertising the capability."""
        coordinator = WorkflowCoordinator(registry_with_gems)

        input_artifact = Artifact(
            content="test input",
            provenance=provenance_base,
        )

        handoff = coordinator.execute_capability("analyze", input_artifact)

        # Verify handoff was created with correct recipient
        assert handoff.recipient == "analyzer"
        assert len(handoff.artifacts) == 1
        assert handoff.artifacts[0].content  # Result was produced

    def test_routes_to_first_alphabetically(self, registry_with_gems, provenance_base):
        """When multiple Gems have same capability, routes alphabetically."""
        registry = registry_with_gems

        # Add another Gem with "analyze" capability
        registry.register(GemSpec(
            name="alpha_analyzer",
            purpose="Another analyzer",
            capabilities=("analyze",),
        ))

        coordinator = WorkflowCoordinator(registry)
        input_artifact = Artifact(content="test", provenance=provenance_base)

        handoff = coordinator.execute_capability("analyze", input_artifact)

        # Should route to "alpha_analyzer" (comes before "analyzer" alphabetically)
        assert handoff.recipient == "alpha_analyzer"

    def test_raises_lookup_error_for_unknown_capability(
        self, registry_with_gems, provenance_base
    ):
        """Coordinator raises LookupError when capability not found."""
        coordinator = WorkflowCoordinator(registry_with_gems)
        input_artifact = Artifact(content="test", provenance=provenance_base)

        with pytest.raises(LookupError, match="No Gem advertises"):
            coordinator.execute_capability("unknown_capability", input_artifact)


class TestWorkflowCoordinatorExecution:
    """Test WorkflowCoordinator execution and result handling."""

    def test_executes_and_returns_handoff(self, registry_with_gems, provenance_base):
        """Coordinator executes Gem and returns valid Handoff."""
        coordinator = WorkflowCoordinator(registry_with_gems)
        input_artifact = Artifact(content="test", provenance=provenance_base)

        handoff = coordinator.execute_capability("analyze", input_artifact)

        assert handoff.sender == "coordinator"
        assert handoff.recipient == "analyzer"
        assert handoff.artifacts
        assert handoff.task_id

    def test_preserves_provenance_through_handoff(
        self, registry_with_gems, provenance_base
    ):
        """Handoff preserves input provenance and creates output provenance."""
        coordinator = WorkflowCoordinator(registry_with_gems)
        input_artifact = Artifact(content="test input", provenance=provenance_base)

        handoff = coordinator.execute_capability("analyze", input_artifact)

        result_artifact = handoff.artifacts[0]

        # Result should have new provenance
        assert result_artifact.provenance is not None
        assert result_artifact.provenance.source_id == "analyzer"
        assert result_artifact.provenance.origin == "ai"
        assert result_artifact.provenance.authority == "analysis"

        # Parent should reference input artifact
        assert input_artifact.artifact_id in result_artifact.provenance.parent_ids

    def test_records_execution_history(self, registry_with_gems, provenance_base):
        """Coordinator records execution in history."""
        coordinator = WorkflowCoordinator(registry_with_gems)
        input_artifact = Artifact(content="test", provenance=provenance_base)

        handoff = coordinator.execute_capability("analyze", input_artifact)

        assert len(coordinator.execution_history) == 1

        record = coordinator.execution_history[0]
        assert isinstance(record, ExecutionRecord)
        assert record.capability == "analyze"
        assert record.route.gem == "analyzer"
        assert record.input_artifact == input_artifact
        assert record.output_artifact == handoff.artifacts[0]


class TestWorkflowCoordinatorCustomExecutor:
    """Test WorkflowCoordinator with custom Gem executors."""

    def test_uses_custom_executor_for_gem(self, registry_with_gems, provenance_base):
        """Coordinator uses custom executor when provided."""
        def custom_executor(artifact, context):
            return Artifact(
                content="custom result",
                provenance=Provenance(
                    source_id="custom",
                    origin=Origin.AI,
                    epistemic_status=EpistemicStatus.INFERRED,
                    authority=Authority.ANALYSIS,
                    parent_ids=(artifact.artifact_id,),
                ),
            )

        coordinator = WorkflowCoordinator(
            registry_with_gems,
            custom_executors={"analyzer": custom_executor},
        )

        input_artifact = Artifact(content="test", provenance=provenance_base)
        handoff = coordinator.execute_capability("analyze", input_artifact)

        result = handoff.artifacts[0]
        assert result.content == "custom result"
        assert result.provenance.source_id == "custom"

    def test_validates_custom_executor_return_type(
        self, registry_with_gems, provenance_base
    ):
        """Coordinator validates that custom executor returns Artifact."""
        def bad_executor(artifact, context):
            return {"not": "an artifact"}

        coordinator = WorkflowCoordinator(
            registry_with_gems,
            custom_executors={"analyzer": bad_executor},
        )

        input_artifact = Artifact(content="test", provenance=provenance_base)

        with pytest.raises(TypeError, match="must return Artifact"):
            coordinator.execute_capability("analyze", input_artifact)


class TestWorkflowCoordinatorMultiStep:
    """Test WorkflowCoordinator with multi-step workflows."""

    def test_executes_workflow_steps(self, registry_with_gems, provenance_base):
        """Coordinator executes multiple workflow steps in sequence."""
        coordinator = WorkflowCoordinator(registry_with_gems)

        step1_artifact = Artifact(content="step 1 input", provenance=provenance_base)
        step2_artifact = Artifact(content="step 2 input", provenance=provenance_base)

        workflow_steps = [
            ("analyze", step1_artifact),
            ("review", step2_artifact),
        ]

        handoff_history, final_artifact = coordinator.execute_workflow(workflow_steps)

        assert len(handoff_history) == 2
        assert handoff_history[0].recipient == "analyzer"
        assert handoff_history[1].recipient == "reviewer"
        assert final_artifact.content  # Result was produced

    def test_builds_context_through_workflow(
        self, registry_with_gems, provenance_base
    ):
        """Coordinator builds context across workflow steps."""
        coordinator = WorkflowCoordinator(registry_with_gems)

        artifact1 = Artifact(content="input 1", provenance=provenance_base)
        artifact2 = Artifact(content="input 2", provenance=provenance_base)

        workflow_steps = [
            ("analyze", artifact1),
            ("review", artifact2),
        ]

        handoff_history, _ = coordinator.execute_workflow(workflow_steps)

        # Verify both steps were executed
        assert len(handoff_history) == 2

    def test_chain_maintains_provenance(self, registry_with_gems, provenance_base):
        """Multi-step workflow maintains provenance chain."""
        coordinator = WorkflowCoordinator(registry_with_gems)

        artifact1 = Artifact(content="input", provenance=provenance_base)
        artifact2 = Artifact(content="next input", provenance=provenance_base)

        workflow_steps = [
            ("analyze", artifact1),
            ("review", artifact2),
        ]

        handoff_history, final_artifact = coordinator.execute_workflow(workflow_steps)

        # Final artifact should have provenance
        assert final_artifact.provenance is not None
        assert final_artifact.provenance.source_id == "reviewer"


class TestMockGemExecutor:
    """Test MockGemExecutor behavior."""

    def test_mock_executor_returns_artifact(self, provenance_base):
        """MockGemExecutor returns valid Artifact."""
        executor = MockGemExecutor()
        input_artifact = Artifact(content="test", provenance=provenance_base)

        result = executor.execute("test_gem", "test_capability", input_artifact)

        assert isinstance(result, Artifact)
        assert result.content
        assert result.provenance is not None

    def test_mock_executor_quality_score_configurable(self, provenance_base):
        """MockGemExecutor quality score is configurable."""
        executor_high = MockGemExecutor(quality_score=0.95)
        executor_low = MockGemExecutor(quality_score=0.60)

        input_artifact = Artifact(content="test", provenance=provenance_base)

        result_high = executor_high.execute("gem", "cap", input_artifact)
        result_low = executor_low.execute("gem", "cap", input_artifact)

        assert result_high.metadata["quality_score"] == 0.95
        assert result_low.metadata["quality_score"] == 0.60

    def test_mock_executor_tracks_parent_artifact(self, provenance_base):
        """MockGemExecutor tracks parent artifact in provenance."""
        executor = MockGemExecutor()
        input_artifact = Artifact(content="test", provenance=provenance_base)

        result = executor.execute("gem", "cap", input_artifact)

        assert input_artifact.artifact_id in result.provenance.parent_ids
