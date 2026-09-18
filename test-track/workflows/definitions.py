"""Workflow definitions for Phase 2 test track execution."""

import sys
from pathlib import Path

# Add test-track to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from harness.engine import WorkflowDefinition, WorkflowStep


# Workflow 1: Complex Feature Implementation (OAuth2 Authentication)
WORKFLOW_001 = WorkflowDefinition(
    workflow_id="workflow-001",
    classification="High complexity, multi-specialist",
    description="OAuth2 Authentication Implementation with MFA and audit logging",
    steps=[
        WorkflowStep(
            gem_name="Requirements Analyst",
            description="Clarify and specify OAuth2 + MFA + audit logging requirements",
            required_inputs=["feature_request"],
            provides_outputs=["requirements_spec", "acceptance_criteria"],
            expected_duration=0.8,
        ),
        WorkflowStep(
            gem_name="Research Analyst",
            description="Research OAuth2 approaches, precedents, and security considerations",
            required_inputs=["requirements_spec"],
            provides_outputs=["research_findings", "security_precedents"],
            expected_duration=1.1,
            dependencies=["Requirements Analyst"],
        ),
        WorkflowStep(
            gem_name="Systems Architect",
            description="Design strategic multi-provider OAuth2 architecture",
            required_inputs=["requirements_spec", "research_findings"],
            provides_outputs=["strategic_architecture", "governance_model"],
            expected_duration=1.3,
            dependencies=["Requirements Analyst", "Research Analyst"],
        ),
        WorkflowStep(
            gem_name="Engineering Architecture & Evolution",
            description="Design tactical API, deployment strategy, and database schema",
            required_inputs=["strategic_architecture"],
            provides_outputs=["api_design", "deployment_strategy", "db_schema"],
            expected_duration=1.0,
            dependencies=["Systems Architect"],
        ),
        WorkflowStep(
            gem_name="Code Review Sentinel",
            description="Review implementation quality and identify issues",
            required_inputs=["api_design"],
            provides_outputs=["code_review_findings"],
            expected_duration=0.9,
            dependencies=["Engineering Architecture & Evolution"],
        ),
        WorkflowStep(
            gem_name="Security & Governance Auditor",
            description="Audit for security and governance compliance",
            required_inputs=["api_design", "deployment_strategy"],
            provides_outputs=["security_findings"],
            expected_duration=1.1,
            dependencies=["Engineering Architecture & Evolution"],
        ),
        WorkflowStep(
            gem_name="Testing & Validation Engineer",
            description="Develop and validate test strategy",
            required_inputs=["api_design"],
            provides_outputs=["test_strategy", "validation_results"],
            expected_duration=0.8,
            dependencies=["Engineering Architecture & Evolution"],
        ),
        WorkflowStep(
            gem_name="Integration Guardian",
            description="Validate backward compatibility and integration",
            required_inputs=["api_design"],
            provides_outputs=["integration_validation"],
            expected_duration=0.6,
            dependencies=["Engineering Architecture & Evolution"],
        ),
        WorkflowStep(
            gem_name="Knowledge Architect",
            description="Document decisions, architecture, and migration guide",
            required_inputs=["strategic_architecture", "api_design", "security_findings"],
            provides_outputs=["decision_records", "documentation"],
            expected_duration=0.5,
            dependencies=["Systems Architect", "Engineering Architecture & Evolution"],
        ),
    ],
    expected_duration=5.2,
    expected_specialist_count=9,
)


# Workflow 2: Security-Critical Refactoring
WORKFLOW_002 = WorkflowDefinition(
    workflow_id="workflow-002",
    classification="Medium complexity, security-focused",
    description="Security-critical refactoring with structure preservation",
    steps=[
        WorkflowStep(
            gem_name="Refactoring Guardian",
            description="Analyze safe refactoring boundaries and structure preservation",
            required_inputs=["code_target"],
            provides_outputs=["refactoring_plan"],
            expected_duration=1.0,
        ),
        WorkflowStep(
            gem_name="Security & Governance Auditor",
            description="Confirm refactoring doesn't introduce vulnerabilities",
            required_inputs=["refactoring_plan"],
            provides_outputs=["security_assessment"],
            expected_duration=0.8,
            dependencies=["Refactoring Guardian"],
        ),
        WorkflowStep(
            gem_name="Code Review Sentinel",
            description="Review refactored code quality and maintainability",
            required_inputs=["refactoring_plan"],
            provides_outputs=["code_review"],
            expected_duration=0.6,
            dependencies=["Refactoring Guardian"],
        ),
        WorkflowStep(
            gem_name="Testing & Validation Engineer",
            description="Confirm regression tests passing",
            required_inputs=["code_review"],
            provides_outputs=["regression_results"],
            expected_duration=0.2,
            dependencies=["Code Review Sentinel"],
        ),
    ],
    expected_duration=2.7,
    expected_specialist_count=5,
)


# Workflow 3: Multi-Source Integration with Deletion
WORKFLOW_003 = WorkflowDefinition(
    workflow_id="workflow-003",
    classification="High complexity, integration + deletion",
    description="Multi-source code integration with authorized deletion",
    steps=[
        WorkflowStep(
            gem_name="Integration Guardian",
            description="Develop multi-source merge strategy and conflict detection",
            required_inputs=["source_a", "source_b", "source_c"],
            provides_outputs=["merge_strategy"],
            expected_duration=0.9,
        ),
        WorkflowStep(
            gem_name="Code Review Sentinel",
            description="Review merged code quality",
            required_inputs=["merge_strategy"],
            provides_outputs=["merge_review"],
            expected_duration=0.6,
            dependencies=["Integration Guardian"],
        ),
        WorkflowStep(
            gem_name="Testing & Validation Engineer",
            description="Validate integration and detect regressions",
            required_inputs=["merge_review"],
            provides_outputs=["integration_test_results"],
            expected_duration=0.7,
            dependencies=["Code Review Sentinel"],
        ),
        WorkflowStep(
            gem_name="Deletion Authority",
            description="Analyze deletion candidates and assess dependencies",
            required_inputs=["integration_test_results"],
            provides_outputs=["deletion_analysis"],
            expected_duration=0.8,
            dependencies=["Testing & Validation Engineer"],
        ),
        WorkflowStep(
            gem_name="Deletion Authority Omega",
            description="Execute authorized deletion with verified authorization",
            required_inputs=["deletion_analysis"],
            provides_outputs=["deletion_execution"],
            expected_duration=0.3,
            dependencies=["Deletion Authority"],
        ),
        WorkflowStep(
            gem_name="Knowledge Architect",
            description="Document deletion decision and recovery options",
            required_inputs=["deletion_execution"],
            provides_outputs=["deletion_documentation"],
            expected_duration=0.2,
            dependencies=["Deletion Authority Omega"],
        ),
    ],
    expected_duration=3.5,
    expected_specialist_count=6,
)


# Workflow 4: Architectural Evolution Decision
WORKFLOW_004 = WorkflowDefinition(
    workflow_id="workflow-004",
    classification="Medium-high complexity, strategic decision",
    description="Architectural evolution and strategic decision making",
    steps=[
        WorkflowStep(
            gem_name="Systems Architect",
            description="Set strategic direction and long-term vision",
            required_inputs=["architecture_options"],
            provides_outputs=["strategic_direction"],
            expected_duration=1.0,
        ),
        WorkflowStep(
            gem_name="Engineering Architecture & Evolution",
            description="Validate tactical implementation feasibility",
            required_inputs=["strategic_direction"],
            provides_outputs=["tactical_validation"],
            expected_duration=0.9,
            dependencies=["Systems Architect"],
        ),
        WorkflowStep(
            gem_name="Research Analyst",
            description="Provide evidence supporting architectural choice",
            required_inputs=["strategic_direction"],
            provides_outputs=["supporting_evidence"],
            expected_duration=0.7,
            dependencies=["Systems Architect"],
        ),
        WorkflowStep(
            gem_name="Code Review Sentinel",
            description="Review architectural implementation",
            required_inputs=["tactical_validation"],
            provides_outputs=["architecture_review"],
            expected_duration=0.5,
            dependencies=["Engineering Architecture & Evolution"],
        ),
        WorkflowStep(
            gem_name="Testing & Validation Engineer",
            description="Develop validation strategy for new architecture",
            required_inputs=["architecture_review"],
            provides_outputs=["validation_strategy"],
            expected_duration=0.4,
            dependencies=["Code Review Sentinel"],
        ),
        WorkflowStep(
            gem_name="Knowledge Architect",
            description="Document decision rationale and implications",
            required_inputs=["strategic_direction", "supporting_evidence"],
            provides_outputs=["decision_documentation"],
            expected_duration=0.3,
            dependencies=["Systems Architect", "Research Analyst"],
        ),
    ],
    expected_duration=3.8,
    expected_specialist_count=6,
)


# Workflow 5: Requirements Clarification to Implementation
WORKFLOW_005 = WorkflowDefinition(
    workflow_id="workflow-005",
    classification="High complexity, full lifecycle",
    description="Full lifecycle from requirements clarification to implementation validation",
    steps=[
        WorkflowStep(
            gem_name="Requirements Analyst",
            description="Clarify and specify requirements",
            required_inputs=["user_request"],
            provides_outputs=["clarified_requirements"],
            expected_duration=0.9,
        ),
        WorkflowStep(
            gem_name="Research Analyst",
            description="Gather evidence for proposed approach",
            required_inputs=["clarified_requirements"],
            provides_outputs=["research_data"],
            expected_duration=0.7,
            dependencies=["Requirements Analyst"],
        ),
        WorkflowStep(
            gem_name="Systems Architect",
            description="Design strategic architecture",
            required_inputs=["clarified_requirements", "research_data"],
            provides_outputs=["system_architecture"],
            expected_duration=0.8,
            dependencies=["Requirements Analyst", "Research Analyst"],
        ),
        WorkflowStep(
            gem_name="Engineering Architecture & Evolution",
            description="Design tactical implementation",
            required_inputs=["system_architecture"],
            provides_outputs=["implementation_design"],
            expected_duration=0.8,
            dependencies=["Systems Architect"],
        ),
        WorkflowStep(
            gem_name="Code Review Sentinel",
            description="Review implementation quality",
            required_inputs=["implementation_design"],
            provides_outputs=["quality_assessment"],
            expected_duration=0.6,
            dependencies=["Engineering Architecture & Evolution"],
        ),
        WorkflowStep(
            gem_name="Testing & Validation Engineer",
            description="Validate implementation",
            required_inputs=["implementation_design"],
            provides_outputs=["validation_results"],
            expected_duration=0.5,
            dependencies=["Engineering Architecture & Evolution"],
        ),
        WorkflowStep(
            gem_name="Knowledge Architect",
            description="Preserve decisions and documentation",
            required_inputs=["system_architecture", "implementation_design"],
            provides_outputs=["preserved_knowledge"],
            expected_duration=0.3,
            dependencies=["Systems Architect", "Engineering Architecture & Evolution"],
        ),
    ],
    expected_duration=4.6,
    expected_specialist_count=7,
)


# Collection of all workflows
ALL_WORKFLOWS = [
    WORKFLOW_001,
    WORKFLOW_002,
    WORKFLOW_003,
    WORKFLOW_004,
    WORKFLOW_005,
]
