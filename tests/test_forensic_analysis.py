"""Test forensic analysis capabilities with restored WorkflowState."""

from gems.contracts import (
    Artifact,
    Authority,
    EpistemicStatus,
    Handoff,
    Origin,
    Provenance,
    WorkflowStatus,
)
from gems.core.workflow import WorkflowState


def test_workflow_state_immutability():
    """WorkflowState can be instantiated and tracks workflow history."""
    state = WorkflowState()
    assert state.status == WorkflowStatus.COMPLETED
    assert state.baseline == ()
    assert state.history == []


def test_workflow_state_with_baseline():
    """WorkflowState tracks initial artifacts."""
    artifact = Artifact(
        content="baseline data",
        provenance=Provenance(
            source_id="source1",
            origin=Origin.HUMAN,
            epistemic_status=EpistemicStatus.EXPLICIT,
            authority=Authority.OBSERVATION,
        ),
    )
    state = WorkflowState(baseline=(artifact,))
    assert len(state.baseline) == 1
    assert state.baseline[0].content == "baseline data"


def test_workflow_state_tracks_handoff_history():
    """WorkflowState can track handoff history for forensic analysis."""
    artifact1 = Artifact(content="step1")
    artifact2 = Artifact(content="step2")

    handoff1 = Handoff(
        task_id="task1",
        sender="analyzer1",
        recipient="analyzer2",
        artifacts=(artifact1,),
    )
    handoff2 = Handoff(
        task_id="task1",
        sender="analyzer2",
        recipient="system",
        artifacts=(artifact2,),
    )

    state = WorkflowState(baseline=(artifact1,), history=[handoff1, handoff2])
    assert len(state.history) == 2
    assert state.history[0].sender == "analyzer1"
    assert state.history[1].sender == "analyzer2"


def test_forensic_analysis_execution_chain():
    """Can reconstruct full execution chain from WorkflowState."""
    # Create baseline
    baseline = Artifact(
        content="initial query",
        provenance=Provenance(
            source_id="user",
            origin=Origin.HUMAN,
            epistemic_status=EpistemicStatus.EXPLICIT,
            authority=Authority.OBSERVATION,
        ),
    )

    # Create analysis step 1
    result1 = Artifact(
        content="preliminary analysis",
        provenance=Provenance(
            source_id="analyzer1",
            origin=Origin.AI,
            epistemic_status=EpistemicStatus.INFERRED,
            authority=Authority.ANALYSIS,
            parent_ids=(baseline.artifact_id,),
        ),
    )

    # Create analysis step 2
    result2 = Artifact(
        content="refined analysis",
        provenance=Provenance(
            source_id="analyzer2",
            origin=Origin.AI,
            epistemic_status=EpistemicStatus.INFERRED,
            authority=Authority.ANALYSIS,
            parent_ids=(result1.artifact_id,),
        ),
    )

    # Build workflow history
    handoff1 = Handoff(
        task_id="analysis_task",
        sender="analyzer1",
        recipient="analyzer2",
        artifacts=(result1,),
    )
    handoff2 = Handoff(
        task_id="analysis_task",
        sender="analyzer2",
        recipient="archive",
        artifacts=(result2,),
    )

    state = WorkflowState(baseline=(baseline,), history=[handoff1, handoff2])

    # Verify forensic analysis capabilities
    assert state.task_id  # Can identify task
    assert len(state.history) == 2  # Can see all steps
    assert state.history[0].sender == "analyzer1"  # Can identify participants
    assert state.history[1].sender == "analyzer2"
    assert result2.provenance.parent_ids == (result1.artifact_id,)  # Can trace lineage
    assert state.status == WorkflowStatus.COMPLETED  # Can verify completion


def test_forensic_use_case_workflow_complexity_analysis():
    """Support workflow complexity analysis by tracking step count."""
    artifacts = [Artifact(content=f"step{i}") for i in range(5)]
    handoffs = [
        Handoff(
            task_id="complex_task",
            sender=f"analyzer{i}",
            recipient=f"analyzer{i+1}",
            artifacts=(artifacts[i],),
        )
        for i in range(4)
    ]

    state = WorkflowState(baseline=(artifacts[0],), history=handoffs)

    # Complexity analysis: total steps = baseline + handoffs
    total_steps = len(state.baseline) + len(state.history)
    assert total_steps == 5

    # Can identify longest chain
    max_depth = max(len(h.artifacts) for h in state.history) if state.history else 0
    assert max_depth == 1


def test_forensic_use_case_specialist_performance():
    """Support specialist performance analysis by tracking handoffs per specialist."""
    task_id = "performance_task"
    artifacts = [Artifact(content=f"result{i}") for i in range(3)]

    handoffs = [
        Handoff(
            task_id=task_id,
            sender="specialist_A",
            recipient="specialist_B",
            artifacts=(artifacts[0],),
        ),
        Handoff(
            task_id=task_id,
            sender="specialist_B",
            recipient="specialist_A",
            artifacts=(artifacts[1],),
        ),
        Handoff(
            task_id=task_id,
            sender="specialist_A",
            recipient="archive",
            artifacts=(artifacts[2],),
        ),
    ]

    state = WorkflowState(history=handoffs)

    # Count handoffs by specialist
    specialist_work = {}
    for handoff in state.history:
        specialist_work[handoff.sender] = specialist_work.get(handoff.sender, 0) + 1

    assert specialist_work["specialist_A"] == 2
    assert specialist_work["specialist_B"] == 1
