"""Test engine_v2 with real GEMS execution path."""

import sys
from pathlib import Path

# Add test-track to path
sys.path.insert(0, str(Path(__file__).parent.parent / "test-track"))

import pytest

from gems import GemSpec
from harness.engine_v2 import RealGemsWorkflowEngine, WorkflowDefinition, WorkflowStep


@pytest.fixture
def gem_specs():
    """Create test Gem specifications."""
    return [
        GemSpec(
            name="Requirement Analyst",
            purpose="Clarifies requirements",
            capabilities=("requirements", "clarification"),
        ),
        GemSpec(
            name="Researcher",
            purpose="Researches evidence",
            capabilities=("research", "investigation"),
        ),
        GemSpec(
            name="Architect",
            purpose="Designs architecture",
            capabilities=("design", "architecture"),
        ),
        GemSpec(
            name="Reviewer",
            purpose="Reviews work",
            capabilities=("review", "audit"),
        ),
    ]


@pytest.fixture
def engine(gem_specs):
    """Create engine with test Gems."""
    return RealGemsWorkflowEngine(gem_specs)


class TestRealGemsWorkflowEngine:
    """Test engine using real GEMS execution."""

    def test_engine_executes_single_step(self, engine):
        """Engine executes single-step workflow with real Router."""
        workflow = WorkflowDefinition(
            workflow_id="test-1",
            classification="Simple",
            description="Single requirement analysis",
            steps=[
                WorkflowStep(
                    gem_name="Requirement Analyst",
                    description="Analyze requirements",
                    capability="requirements",
                    required_inputs=["req1"],
                    provides_outputs=["req_analysis"],
                    expected_duration=1.0,
                )
            ],
            expected_duration=1.0,
            expected_specialist_count=1,
        )

        execution = engine.execute_workflow(workflow)

        assert execution.workflow_id == "test-1"
        assert len(execution.steps_executed) == 1
        assert execution.steps_executed[0] == "Requirement Analyst"
        assert execution.metrics.success

    def test_engine_routes_correctly(self, engine):
        """Engine uses REAL Router for capability matching."""
        workflow = WorkflowDefinition(
            workflow_id="test-routing",
            classification="Simple",
            description="Test routing accuracy",
            steps=[
                WorkflowStep(
                    gem_name="Researcher",
                    description="Research the topic",
                    capability="research",  # This capability is advertised by Researcher
                    required_inputs=["topic"],
                    provides_outputs=["findings"],
                    expected_duration=1.0,
                )
            ],
            expected_duration=1.0,
            expected_specialist_count=1,
        )

        execution = engine.execute_workflow(workflow)

        # Verify routing was correct
        researcher_metrics = execution.metrics.gem_metrics.get("Researcher")
        assert researcher_metrics is not None
        assert researcher_metrics.routing_correct  # Real Router matched correctly

    def test_engine_routing_fails_for_unknown_capability(self, engine):
        """Engine properly fails when capability not found."""
        workflow = WorkflowDefinition(
            workflow_id="test-fail",
            classification="Bad",
            description="Unknown capability",
            steps=[
                WorkflowStep(
                    gem_name="Unknown",
                    description="Do something",
                    capability="unknown_capability",  # Not advertised by any Gem
                    required_inputs=[],
                    provides_outputs=[],
                    expected_duration=1.0,
                )
            ],
            expected_duration=1.0,
            expected_specialist_count=1,
        )

        execution = engine.execute_workflow(workflow)

        # Should fail
        assert not execution.metrics.success
        assert "routing failed" in " ".join(execution.metrics.issues).lower()

    def test_engine_preserves_provenance(self, engine):
        """Engine creates Handoffs with proper provenance."""
        workflow = WorkflowDefinition(
            workflow_id="test-provenance",
            classification="Provenance test",
            description="Verify provenance tracking",
            steps=[
                WorkflowStep(
                    gem_name="Architect",
                    description="Design",
                    capability="design",
                    required_inputs=[],
                    provides_outputs=["design"],
                    expected_duration=1.0,
                )
            ],
            expected_duration=1.0,
            expected_specialist_count=1,
        )

        execution = engine.execute_workflow(workflow)

        # Verify provenance was created
        architect_metrics = execution.metrics.gem_metrics.get("Architect")
        assert architect_metrics is not None
        assert architect_metrics.authority_respected  # Provenance was created with proper authority

    def test_engine_executes_multi_step_workflow(self, engine):
        """Engine executes multi-step workflow maintaining context."""
        workflow = WorkflowDefinition(
            workflow_id="test-multi",
            classification="Multi-step",
            description="Multiple steps",
            steps=[
                WorkflowStep(
                    gem_name="Requirement Analyst",
                    description="Analyze",
                    capability="requirements",
                    required_inputs=["req"],
                    provides_outputs=["req_analysis"],
                    expected_duration=1.0,
                ),
                WorkflowStep(
                    gem_name="Researcher",
                    description="Research",
                    capability="research",
                    required_inputs=["req_analysis"],
                    provides_outputs=["findings"],
                    expected_duration=1.0,
                ),
                WorkflowStep(
                    gem_name="Architect",
                    description="Design",
                    capability="design",
                    required_inputs=["findings"],
                    provides_outputs=["design"],
                    expected_duration=1.0,
                ),
            ],
            expected_duration=3.0,
            expected_specialist_count=3,
        )

        execution = engine.execute_workflow(workflow)

        # Verify all steps executed
        assert len(execution.steps_executed) == 3
        assert "Requirement Analyst" in execution.steps_executed
        assert "Researcher" in execution.steps_executed
        assert "Architect" in execution.steps_executed
        assert execution.metrics.success

    def test_engine_metrics_use_real_routing(self, engine):
        """Engine metrics reflect real Router behavior."""
        workflow = WorkflowDefinition(
            workflow_id="test-metrics",
            classification="Metrics test",
            description="Test metrics",
            steps=[
                WorkflowStep(
                    gem_name="Reviewer",
                    description="Review work",
                    capability="review",
                    required_inputs=[],
                    provides_outputs=[],
                    expected_duration=1.0,
                )
            ],
            expected_duration=1.0,
            expected_specialist_count=1,
        )

        execution = engine.execute_workflow(workflow)

        # Routing accuracy should be based on real Router, not dict lookup
        assert execution.metrics.routing_accuracy == 1.0  # Reviewer advertises "review"

    def test_engine_tracking_execution_history(self, engine):
        """Engine maintains execution history."""
        workflow1 = WorkflowDefinition(
            workflow_id="test-history-1",
            classification="First",
            description="First workflow",
            steps=[
                WorkflowStep(
                    gem_name="Architect",
                    description="Design",
                    capability="design",
                    required_inputs=[],
                    provides_outputs=[],
                    expected_duration=1.0,
                )
            ],
            expected_duration=1.0,
            expected_specialist_count=1,
        )

        workflow2 = WorkflowDefinition(
            workflow_id="test-history-2",
            classification="Second",
            description="Second workflow",
            steps=[
                WorkflowStep(
                    gem_name="Researcher",
                    description="Research",
                    capability="research",
                    required_inputs=[],
                    provides_outputs=[],
                    expected_duration=1.0,
                )
            ],
            expected_duration=1.0,
            expected_specialist_count=1,
        )

        engine.execute_workflow(workflow1)
        engine.execute_workflow(workflow2)

        assert len(engine.execution_history) == 2
        assert engine.execution_history[0].workflow_id == "test-history-1"
        assert engine.execution_history[1].workflow_id == "test-history-2"

    def test_engine_summary(self, engine):
        """Engine provides execution summary."""
        workflow = WorkflowDefinition(
            workflow_id="test-summary",
            classification="Summary test",
            description="Test summary",
            steps=[
                WorkflowStep(
                    gem_name="Architect",
                    description="Design",
                    capability="design",
                    required_inputs=[],
                    provides_outputs=[],
                    expected_duration=1.0,
                )
            ],
            expected_duration=1.0,
            expected_specialist_count=1,
        )

        engine.execute_workflow(workflow)

        summary = engine.get_execution_summary()

        assert summary["total_executions"] == 1
        assert summary["successful"] == 1
        assert summary["avg_routing_accuracy"] >= 0.0
