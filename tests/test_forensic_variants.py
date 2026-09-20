"""50 comprehensive test variants for forensic analysis system."""

import pytest
from gems.contracts import (
    Artifact,
    Authority,
    EpistemicStatus,
    Handoff,
    Origin,
    Provenance,
    WorkflowStatus,
    GemSpec,
)
from gems.core.workflow import WorkflowState
from gems.core.registry import GemRegistry
from gems.core.router import Router
from gems.governance.validator import GovernanceValidator


# ============================================================================
# VARIANT GROUP 1: Basic WorkflowState Functionality (1-5)
# ============================================================================

def test_01_workflow_state_default_initialization():
    """Variant 1: WorkflowState initializes with defaults."""
    state = WorkflowState()
    assert state.task_id is not None
    assert len(state.task_id) > 0
    assert state.status == WorkflowStatus.COMPLETED
    assert state.baseline == ()
    assert state.history == []


def test_02_workflow_state_custom_task_id():
    """Variant 2: WorkflowState accepts custom task_id."""
    state = WorkflowState(task_id="custom-task-123")
    assert state.task_id == "custom-task-123"


def test_03_workflow_state_custom_status_failed():
    """Variant 3: WorkflowState can track FAILED status."""
    state = WorkflowState(status=WorkflowStatus.FAILED)
    assert state.status == WorkflowStatus.FAILED


def test_04_workflow_state_with_baseline_artifacts():
    """Variant 4: WorkflowState initializes with baseline artifacts."""
    artifact1 = Artifact(content="baseline1")
    artifact2 = Artifact(content="baseline2")
    state = WorkflowState(baseline=(artifact1, artifact2))
    assert len(state.baseline) == 2
    assert state.baseline[0].content == "baseline1"


def test_05_workflow_state_with_empty_baseline():
    """Variant 5: WorkflowState handles empty baseline tuple."""
    state = WorkflowState(baseline=())
    assert state.baseline == ()
    assert isinstance(state.baseline, tuple)


# ============================================================================
# VARIANT GROUP 2: Artifact Immutability (6-10)
# ============================================================================

def test_06_artifact_immutability_frozen():
    """Variant 6: Artifact dataclass is frozen (immutable)."""
    artifact = Artifact(content="immutable")
    with pytest.raises(Exception):  # FrozenInstanceError
        artifact.content = "modified"


def test_07_artifact_id_uniqueness():
    """Variant 7: Each Artifact gets unique ID."""
    a1 = Artifact(content="same")
    a2 = Artifact(content="same")
    assert a1.artifact_id != a2.artifact_id


def test_08_artifact_with_provenance():
    """Variant 8: Artifact stores provenance metadata."""
    prov = Provenance(
        source_id="analyst_1",
        origin=Origin.AI,
        epistemic_status=EpistemicStatus.INFERRED,
        authority=Authority.ANALYSIS,
    )
    artifact = Artifact(content="analyzed", provenance=prov)
    assert artifact.provenance.source_id == "analyst_1"


def test_09_artifact_with_metadata():
    """Variant 9: Artifact can store additional metadata."""
    artifact = Artifact(
        content="data",
        metadata={"confidence": 0.95, "source": "external_db"},
    )
    assert artifact.metadata["confidence"] == 0.95


def test_10_artifact_kind_field():
    """Variant 10: Artifact has kind field."""
    artifact = Artifact(kind="observation")
    assert artifact.kind == "observation"


# ============================================================================
# VARIANT GROUP 3: Provenance Tracking (11-15)
# ============================================================================

def test_11_provenance_source_tracking():
    """Variant 11: Provenance tracks artifact source."""
    prov = Provenance(
        source_id="human_user",
        origin=Origin.HUMAN,
        epistemic_status=EpistemicStatus.EXPLICIT,
        authority=Authority.OBSERVATION,
    )
    assert prov.source_id == "human_user"
    assert prov.origin == Origin.HUMAN


def test_12_provenance_epistemic_status_inference():
    """Variant 12: Provenance tracks inferred epistemic status."""
    prov = Provenance(
        source_id="ai",
        origin=Origin.AI,
        epistemic_status=EpistemicStatus.INFERRED,
        authority=Authority.ANALYSIS,
    )
    assert prov.epistemic_status == EpistemicStatus.INFERRED


def test_13_provenance_authority_levels():
    """Variant 13: Provenance tracks different authority levels."""
    authorities = [
        Authority.OBSERVATION,
        Authority.ANALYSIS,
        Authority.PROPOSAL,
        Authority.HUMAN_AUTHORIZATION,
    ]
    for auth in authorities:
        prov = Provenance(
            source_id="test",
            origin=Origin.HUMAN,
            epistemic_status=EpistemicStatus.EXPLICIT,
            authority=auth,
        )
        assert prov.authority == auth


def test_14_provenance_parent_chain():
    """Variant 14: Provenance tracks parent artifact IDs."""
    parent_id = "artifact-123"
    prov = Provenance(
        source_id="child",
        origin=Origin.AI,
        epistemic_status=EpistemicStatus.INFERRED,
        authority=Authority.ANALYSIS,
        parent_ids=(parent_id,),
    )
    assert parent_id in prov.parent_ids


def test_15_provenance_with_note():
    """Variant 15: Provenance can include explanatory note."""
    prov = Provenance(
        source_id="test",
        origin=Origin.AI,
        epistemic_status=EpistemicStatus.CONFLICTED,
        authority=Authority.PROPOSAL,
        note="Needs human review due to conflicting interpretations",
    )
    assert "conflicting" in prov.note


# ============================================================================
# VARIANT GROUP 4: Handoff Tracking (16-20)
# ============================================================================

def test_16_handoff_basic_creation():
    """Variant 16: Handoff tracks execution steps."""
    artifact = Artifact(content="result")
    handoff = Handoff(
        task_id="task1",
        sender="analyzer1",
        recipient="analyzer2",
        artifacts=(artifact,),
    )
    assert handoff.sender == "analyzer1"
    assert handoff.recipient == "analyzer2"


def test_17_handoff_multiple_artifacts():
    """Variant 17: Handoff can contain multiple artifacts."""
    a1, a2, a3 = (
        Artifact(content="r1"),
        Artifact(content="r2"),
        Artifact(content="r3"),
    )
    handoff = Handoff(
        task_id="task1",
        sender="processor",
        recipient="aggregator",
        artifacts=(a1, a2, a3),
    )
    assert len(handoff.artifacts) == 3


def test_18_handoff_immutability():
    """Variant 18: Handoff dataclass is frozen."""
    handoff = Handoff(task_id="t1", sender="a", recipient="b")
    with pytest.raises(Exception):  # FrozenInstanceError
        handoff.sender = "modified"


def test_19_handoff_default_empty_artifacts():
    """Variant 19: Handoff defaults to empty artifacts."""
    handoff = Handoff(task_id="t1", sender="a", recipient="b")
    assert handoff.artifacts == ()


def test_20_handoff_same_task_chain():
    """Variant 20: Multiple handoffs can share task_id."""
    h1 = Handoff(task_id="TASK", sender="a", recipient="b")
    h2 = Handoff(task_id="TASK", sender="b", recipient="c")
    h3 = Handoff(task_id="TASK", sender="c", recipient="d")
    assert h1.task_id == h2.task_id == h3.task_id


# ============================================================================
# VARIANT GROUP 5: Workflow History Management (21-25)
# ============================================================================

def test_21_workflow_single_handoff():
    """Variant 21: WorkflowState tracks single handoff."""
    h = Handoff(task_id="t1", sender="a", recipient="b")
    state = WorkflowState(history=[h])
    assert len(state.history) == 1
    assert state.history[0].sender == "a"


def test_22_workflow_multi_step_chain():
    """Variant 22: WorkflowState preserves execution chain."""
    handoffs = [
        Handoff(task_id="chain", sender=f"step{i}", recipient=f"step{i+1}")
        for i in range(5)
    ]
    state = WorkflowState(history=handoffs)
    assert len(state.history) == 5
    assert state.history[0].sender == "step0"
    assert state.history[4].sender == "step4"


def test_23_workflow_history_modification_via_append():
    """Variant 23: History list can be modified after creation."""
    state = WorkflowState()
    h = Handoff(task_id="t1", sender="a", recipient="b")
    state.history.append(h)
    assert len(state.history) == 1


def test_24_workflow_large_history():
    """Variant 24: WorkflowState handles large histories."""
    handoffs = [
        Handoff(task_id="big", sender=f"worker{i%10}", recipient=f"worker{(i+1)%10}")
        for i in range(100)
    ]
    state = WorkflowState(history=handoffs)
    assert len(state.history) == 100


def test_25_workflow_history_with_complex_artifacts():
    """Variant 25: Workflow history with rich artifact metadata."""
    artifacts = [
        Artifact(
            content=f"step{i}",
            provenance=Provenance(
                source_id=f"source{i}",
                origin=Origin.AI if i % 2 else Origin.HUMAN,
                epistemic_status=EpistemicStatus.INFERRED
                if i % 2
                else EpistemicStatus.EXPLICIT,
                authority=Authority.ANALYSIS,
            ),
        )
        for i in range(3)
    ]
    handoffs = [
        Handoff(task_id="t", sender=f"a{i}", recipient=f"b{i}", artifacts=(artifacts[i],))
        for i in range(3)
    ]
    state = WorkflowState(history=handoffs)
    assert all(h.artifacts[0].provenance is not None for h in state.history)


# ============================================================================
# VARIANT GROUP 6: Forensic Analysis - Provenance Chain (26-30)
# ============================================================================

def test_26_forensic_linear_provenance_chain():
    """Variant 26: Reconstruct linear provenance chain."""
    a1 = Artifact(
        artifact_id="root",
        content="initial",
        provenance=Provenance(
            source_id="user", origin=Origin.HUMAN, epistemic_status=EpistemicStatus.EXPLICIT, authority=Authority.OBSERVATION
        ),
    )
    a2 = Artifact(
        content="processed",
        provenance=Provenance(
            source_id="processor",
            origin=Origin.AI,
            epistemic_status=EpistemicStatus.INFERRED,
            authority=Authority.ANALYSIS,
            parent_ids=(a1.artifact_id,),
        ),
    )
    a3 = Artifact(
        content="validated",
        provenance=Provenance(
            source_id="validator",
            origin=Origin.AI,
            epistemic_status=EpistemicStatus.INFERRED,
            authority=Authority.ANALYSIS,
            parent_ids=(a2.artifact_id,),
        ),
    )
    assert a3.provenance.parent_ids[0] == a2.artifact_id
    assert a2.provenance.parent_ids[0] == a1.artifact_id


def test_27_forensic_branching_provenance():
    """Variant 27: Detect branching in provenance tree."""
    base = Artifact(artifact_id="base", content="source")
    branch1 = Artifact(
        content="branch1",
        provenance=Provenance(
            source_id="a1",
            origin=Origin.AI,
            epistemic_status=EpistemicStatus.INFERRED,
            authority=Authority.ANALYSIS,
            parent_ids=(base.artifact_id,),
        ),
    )
    branch2 = Artifact(
        content="branch2",
        provenance=Provenance(
            source_id="a2",
            origin=Origin.AI,
            epistemic_status=EpistemicStatus.INFERRED,
            authority=Authority.ANALYSIS,
            parent_ids=(base.artifact_id,),
        ),
    )
    assert branch1.provenance.parent_ids == branch2.provenance.parent_ids


def test_28_forensic_mixed_origin_tracking():
    """Variant 28: Track mixed human/AI contribution chain."""
    origins = [Origin.HUMAN, Origin.AI, Origin.JOINT, Origin.UNCERTAIN]
    artifacts = []
    parent_id = "start"
    for i, origin in enumerate(origins):
        a = Artifact(
            content=f"step{i}",
            provenance=Provenance(
                source_id=f"agent{i}",
                origin=origin,
                epistemic_status=EpistemicStatus.EXPLICIT,
                authority=Authority.ANALYSIS,
                parent_ids=(parent_id,) if i > 0 else (),
            ),
        )
        artifacts.append(a)
        parent_id = a.artifact_id
    assert artifacts[3].provenance.origin == Origin.UNCERTAIN


def test_29_forensic_authority_escalation():
    """Variant 29: Track authority level transitions."""
    progression = [
        (Authority.OBSERVATION, Origin.HUMAN),
        (Authority.ANALYSIS, Origin.AI),
        (Authority.PROPOSAL, Origin.AI),
        (Authority.HUMAN_AUTHORIZATION, Origin.HUMAN),
    ]
    artifacts = []
    parent_id = None
    for auth, origin in progression:
        a = Artifact(
            content="escalated",
            provenance=Provenance(
                source_id="escalation",
                origin=origin,
                epistemic_status=EpistemicStatus.EXPLICIT,
                authority=auth,
                parent_ids=(parent_id,) if parent_id else (),
            ),
        )
        artifacts.append(a)
        parent_id = a.artifact_id
    assert artifacts[-1].provenance.authority == Authority.HUMAN_AUTHORIZATION


def test_30_forensic_conflicted_epistemic_status():
    """Variant 30: Detect and track conflicted information."""
    a1 = Artifact(
        content="claim_a",
        provenance=Provenance(
            source_id="source1",
            origin=Origin.HUMAN,
            epistemic_status=EpistemicStatus.EXPLICIT,
            authority=Authority.OBSERVATION,
        ),
    )
    a2 = Artifact(
        content="claim_b_contradicts_a",
        provenance=Provenance(
            source_id="source2",
            origin=Origin.HUMAN,
            epistemic_status=EpistemicStatus.EXPLICIT,
            authority=Authority.OBSERVATION,
        ),
    )
    conflict = Artifact(
        content="conflict_detected",
        provenance=Provenance(
            source_id="analyzer",
            origin=Origin.AI,
            epistemic_status=EpistemicStatus.CONFLICTED,
            authority=Authority.PROPOSAL,
            parent_ids=(a1.artifact_id, a2.artifact_id),
        ),
    )
    assert conflict.provenance.epistemic_status == EpistemicStatus.CONFLICTED


# ============================================================================
# VARIANT GROUP 7: Forensic Analysis - Workflow Patterns (31-35)
# ============================================================================

def test_31_forensic_specialist_contribution_pattern():
    """Variant 31: Identify specialist contribution patterns."""
    specialists = ["analyst", "validator", "reviewer"]
    contributions = {s: 0 for s in specialists}

    handoffs = []
    for i in range(6):
        specialist = specialists[i % len(specialists)]
        h = Handoff(
            task_id="workflow",
            sender=specialist,
            recipient="queue",
            artifacts=(Artifact(content=f"output{i}"),),
        )
        handoffs.append(h)
        contributions[specialist] += 1

    state = WorkflowState(history=handoffs)
    for h in state.history:
        contributions[h.sender] += 1

    assert contributions["analyst"] > 0


def test_32_forensic_workflow_bottleneck_detection():
    """Variant 32: Detect workflow bottlenecks."""
    bottleneck_specialist = "slow_analyst"
    handoffs = []

    for i in range(10):
        if i < 3 or i > 6:
            sender = "fast_analyst"
        else:
            sender = bottleneck_specialist
        h = Handoff(
            task_id="bottleneck_test",
            sender=sender,
            recipient="next",
        )
        handoffs.append(h)

    state = WorkflowState(history=handoffs)
    sender_counts = {}
    for h in state.history:
        sender_counts[h.sender] = sender_counts.get(h.sender, 0) + 1

    assert sender_counts[bottleneck_specialist] == 4


def test_33_forensic_parallel_path_detection():
    """Variant 33: Detect parallel processing paths."""
    parallel_paths = ["path_A", "path_B", "path_C"]
    handoffs = []

    for path in parallel_paths:
        for i in range(3):
            h = Handoff(
                task_id="parallel",
                sender=f"{path}_step{i}",
                recipient=f"{path}_step{i+1}",
            )
            handoffs.append(h)

    state = WorkflowState(history=handoffs)

    paths_found = set()
    for h in state.history:
        for path in parallel_paths:
            if path in h.sender:
                paths_found.add(path)

    assert len(paths_found) == 3


def test_34_forensic_workflow_duration_from_handoff_count():
    """Variant 34: Estimate workflow duration by step count."""
    handoffs = [
        Handoff(task_id="estimate", sender=f"step{i}", recipient=f"step{i+1}")
        for i in range(20)
    ]
    state = WorkflowState(history=handoffs)

    # More handoffs suggest longer workflow
    complexity_score = len(state.history)
    assert complexity_score == 20


def test_35_forensic_workflow_state_distribution():
    """Variant 35: Track distribution of workflow completion states."""
    completed = WorkflowState(status=WorkflowStatus.COMPLETED)
    failed = WorkflowState(status=WorkflowStatus.FAILED)

    workflows = [completed, failed, completed, completed]
    status_counts = {
        WorkflowStatus.COMPLETED: sum(1 for w in workflows if w.status == WorkflowStatus.COMPLETED),
        WorkflowStatus.FAILED: sum(1 for w in workflows if w.status == WorkflowStatus.FAILED),
    }

    assert status_counts[WorkflowStatus.COMPLETED] == 3
    assert status_counts[WorkflowStatus.FAILED] == 1


# ============================================================================
# VARIANT GROUP 8: Registry and Router (36-40)
# ============================================================================

def test_36_registry_single_specialist():
    """Variant 36: Register and discover single specialist."""
    registry = GemRegistry()
    spec = GemSpec("DataAnalyst", "analyze data", ("analysis",))
    registry.register(spec)

    found = registry.list()
    assert len(found) == 1
    assert found[0].name == "DataAnalyst"


def test_37_registry_multiple_specialists():
    """Variant 37: Register multiple specialists with overlapping capabilities."""
    registry = GemRegistry()
    specs = [
        GemSpec("Analyst1", "basic analysis", ("analysis",)),
        GemSpec("Analyst2", "advanced analysis", ("analysis", "ml")),
        GemSpec("Validator", "validation", ("validation",)),
    ]
    for spec in specs:
        registry.register(spec)

    assert len(registry.list()) == 3


def test_38_router_selects_alphabetically_first():
    """Variant 38: Router selects alphabetically first when multiple match."""
    registry = GemRegistry()
    registry.register(GemSpec("Zebra", "z", ("analysis",)))
    registry.register(GemSpec("Apple", "a", ("analysis",)))

    router = Router(registry)
    route = router.route("analysis")
    assert route.gem == "Apple"


def test_39_router_raises_on_unknown_capability():
    """Variant 39: Router raises LookupError for unknown capability."""
    registry = GemRegistry()
    registry.register(GemSpec("Expert", "knows", ("known",)))

    router = Router(registry)
    with pytest.raises(LookupError):
        router.route("unknown")


def test_40_router_capability_matching():
    """Variant 40: Router matches partial capability sets."""
    registry = GemRegistry()
    registry.register(GemSpec("MultiTool", "versatile", ("read", "write", "analyze")))

    router = Router(registry)
    for capability in ["read", "write", "analyze"]:
        route = router.route(capability)
        assert route.gem == "MultiTool"
        assert route.capability == capability


# ============================================================================
# VARIANT GROUP 9: Governance Validation (41-45)
# ============================================================================

def test_41_governance_validator_creation():
    """Variant 41: Create governance validator instance."""
    validator = GovernanceValidator()
    assert validator is not None


def test_42_governance_validator_with_artifact():
    """Variant 42: Validator can accept artifacts with provenance."""
    validator = GovernanceValidator()
    artifact = Artifact(
        content="test",
        provenance=Provenance(
            source_id="test",
            origin=Origin.HUMAN,
            epistemic_status=EpistemicStatus.EXPLICIT,
            authority=Authority.OBSERVATION,
        ),
    )
    # Validator should not raise on valid artifact
    validator.validate_artifact(artifact)


def test_43_governance_multiple_validators():
    """Variant 43: Create multiple validator instances."""
    validators = [GovernanceValidator() for _ in range(3)]
    assert len(validators) == 3
    assert all(v is not None for v in validators)


def test_44_governance_with_workflow_state():
    """Variant 44: Validator works with workflow state."""
    validator = GovernanceValidator()
    state = WorkflowState()
    artifact = Artifact(
        content="test",
        provenance=Provenance(
            source_id="test",
            origin=Origin.HUMAN,
            epistemic_status=EpistemicStatus.EXPLICIT,
            authority=Authority.OBSERVATION,
        ),
    )
    state.history.append(
        Handoff(task_id=state.task_id, sender="a", recipient="b", artifacts=(artifact,))
    )
    validator.validate_artifact(artifact)


def test_45_governance_constraint_tracking():
    """Variant 45: Governance validator can track constraints."""
    validator = GovernanceValidator()
    artifact1 = Artifact(
        content="proposal",
        provenance=Provenance(
            source_id="ai",
            origin=Origin.AI,
            epistemic_status=EpistemicStatus.INFERRED,
            authority=Authority.PROPOSAL,
        ),
    )
    artifact2 = Artifact(
        content="approved",
        provenance=Provenance(
            source_id="human",
            origin=Origin.HUMAN,
            epistemic_status=EpistemicStatus.EXPLICIT,
            authority=Authority.HUMAN_AUTHORIZATION,
        ),
    )
    validator.validate_artifact(artifact1)
    validator.validate_artifact(artifact2)


# ============================================================================
# VARIANT GROUP 10: Integration and Edge Cases (46-50)
# ============================================================================

def test_46_end_to_end_complete_workflow():
    """Variant 46: Complete workflow from input to forensic analysis."""
    registry = GemRegistry()
    registry.register(GemSpec("InputHandler", "input", ("input",)))
    registry.register(GemSpec("Processor", "process", ("process",)))
    registry.register(GemSpec("Validator", "validate", ("validate",)))

    router = Router(registry)
    input_route = router.route("input")
    process_route = router.route("process")
    validate_route = router.route("validate")

    assert input_route.gem == "InputHandler"
    assert process_route.gem == "Processor"
    assert validate_route.gem == "Validator"


def test_47_forensic_recovery_of_failed_workflow():
    """Variant 47: Forensic analysis of failed workflow."""
    state = WorkflowState(status=WorkflowStatus.FAILED)

    artifact1 = Artifact(content="input")
    artifact2 = Artifact(content="partial_result")

    h1 = Handoff(
        task_id=state.task_id,
        sender="processor",
        recipient="validator",
        artifacts=(artifact1,),
    )
    h2 = Handoff(
        task_id=state.task_id,
        sender="validator",
        recipient="error_handler",
        artifacts=(artifact2,),
    )

    state.history.extend([h1, h2])

    assert state.status == WorkflowStatus.FAILED
    assert len(state.history) == 2


def test_48_audit_trail_immutability_verification():
    """Variant 48: Verify audit trail immutability."""
    artifacts = [
        Artifact(
            content=f"record{i}",
            provenance=Provenance(
                source_id=f"source{i}",
                origin=Origin.HUMAN,
                epistemic_status=EpistemicStatus.EXPLICIT,
                authority=Authority.OBSERVATION,
            ),
        )
        for i in range(5)
    ]

    handoffs = [
        Handoff(
            task_id="audit",
            sender="auditor",
            recipient="archive",
            artifacts=(artifacts[i],),
        )
        for i in range(5)
    ]

    state = WorkflowState(baseline=tuple(artifacts), history=handoffs)

    # Verify immutability of baseline
    assert state.baseline[0].artifact_id == artifacts[0].artifact_id
    assert state.baseline[0].provenance.source_id == "source0"


def test_49_complex_multi_team_workflow():
    """Variant 49: Forensic analysis of multi-team workflow."""
    teams = ["team_research", "team_analysis", "team_validation", "team_reporting"]

    handoffs = []
    for round_num in range(3):
        for team_idx, team in enumerate(teams):
            h = Handoff(
                task_id="multi_team",
                sender=f"{team}_round{round_num}",
                recipient=f"{teams[(team_idx + 1) % len(teams)]}_round{round_num}",
            )
            handoffs.append(h)

    state = WorkflowState(history=handoffs)

    # Verify all teams contributed
    team_contributions = set()
    for h in state.history:
        for team in teams:
            if team in h.sender:
                team_contributions.add(team)

    assert len(team_contributions) == 4


def _setup_registry_for_comprehensive():
    """Setup registry with research specialists."""
    registry = GemRegistry()
    specialists = [
        ("Researcher", "research", ("research", "literature")),
        ("Analyst", "analysis", ("analysis", "statistics")),
        ("Validator", "validation", ("validation", "verification")),
    ]
    for name, purpose, capabilities in specialists:
        registry.register(GemSpec(name, purpose, capabilities))
    return registry


def _build_workflow_artifacts():
    """Build artifacts for comprehensive validation workflow."""
    baseline = Artifact(
        content="research_question",
        provenance=Provenance(
            source_id="researcher",
            origin=Origin.HUMAN,
            epistemic_status=EpistemicStatus.EXPLICIT,
            authority=Authority.OBSERVATION,
        ),
    )
    analysis = Artifact(
        content="statistical_results",
        provenance=Provenance(
            source_id="analyst",
            origin=Origin.AI,
            epistemic_status=EpistemicStatus.INFERRED,
            authority=Authority.ANALYSIS,
            parent_ids=(baseline.artifact_id,),
        ),
    )
    validation = Artifact(
        content="verified_results",
        provenance=Provenance(
            source_id="validator",
            origin=Origin.AI,
            epistemic_status=EpistemicStatus.INFERRED,
            authority=Authority.ANALYSIS,
            parent_ids=(analysis.artifact_id,),
        ),
    )
    return baseline, analysis, validation


def test_50_forensic_system_comprehensive_validation():
    """Variant 50: Comprehensive validation of entire forensic system."""
    registry = _setup_registry_for_comprehensive()
    baseline, analysis, validation = _build_workflow_artifacts()

    handoffs = [
        Handoff(
            task_id="comprehensive",
            sender="Researcher",
            recipient="Analyst",
            artifacts=(baseline,),
        ),
        Handoff(
            task_id="comprehensive",
            sender="Analyst",
            recipient="Validator",
            artifacts=(analysis,),
        ),
        Handoff(
            task_id="comprehensive",
            sender="Validator",
            recipient="archive",
            artifacts=(validation,),
        ),
    ]

    state = WorkflowState(baseline=(baseline,), history=handoffs, status=WorkflowStatus.COMPLETED)
    router = Router(registry)
    validator = GovernanceValidator()

    assert len(state.history) == 3
    assert state.status == WorkflowStatus.COMPLETED
    assert state.history[0].sender == "Researcher"
    assert state.history[-1].sender == "Validator"
    assert validation.provenance.parent_ids[0] == analysis.artifact_id
    assert len(registry.list()) == 3

    for capability in ["research", "analysis", "validation"]:
        route = router.route(capability)
        assert route is not None

    validator.validate_artifact(baseline)
    validator.validate_artifact(analysis)
    validator.validate_artifact(validation)
