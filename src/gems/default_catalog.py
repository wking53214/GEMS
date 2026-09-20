from __future__ import annotations

from gems.contracts import GemSpec
from gems.core.registry import GemRegistry

CATALOG = (
    ("Requirements Analyst", "converting unclear ideas, business needs, technical requests, and improvement goals into precise, actionable requirements", ("objective-definition", "requirement-specification", "scope-management", "constraint-identification", "dependency-analysis", "success-criteria-definition", "risk-identification")),
    ("Research Analyst", "evidence-based research and analysis supporting technical, strategic, and business decisions", ("evidence-analysis", "source-evaluation", "comparative-analysis", "decision-support", "uncertainty-quantification", "alternative-evaluation", "finding-synthesis")),
    ("Systems Architect", "strategic platform design and evolution for complex systems, AI governance, and modular architectures", ("platform-design", "systems-integration", "governance-architecture", "scalability-planning", "reliability-engineering", "modularity-optimization", "long-term-adaptability")),
    ("Engineering Architecture & Evolution", "safe implementation and controlled evolution of systems through architectural authority", ("architecture-design", "system-evolution", "design-validation", "dependency-management", "constraint-preservation", "interface-definition", "architectural-risk-assessment")),
    ("Code Review Sentinel", "independent quality gate for identifying defects, regressions, and architectural issues", ("defect-detection", "architectural-analysis", "regression-prevention", "maintainability-assessment", "code-quality-evaluation", "compatibility-analysis", "failure-mode-identification")),
    ("Integration Guardian", "combining code from multiple sources into coherent implementation", ("integration-strategy", "conflict-resolution", "component-preservation", "multi-source-analysis", "merge-coordination", "functional-continuity")),
    ("Security & Governance Auditor", "risk reviewer for security, governance, compliance, and control integrity", ("threat-analysis", "control-assessment", "compliance-validation", "risk-identification", "breach-prevention", "governance-enforcement", "auditability-assurance", "privilege-review")),
    ("Testing & Validation Engineer", "system reliability validation and regression prevention", ("testing-strategy", "validation-design", "baseline-verification", "regression-testing", "evidence-collection", "failure-analysis")),
    ("Technical Documentation Specialist", "technical documentation and architecture documentation", ("documentation-creation", "technical-writing", "architecture-documentation", "developer-documentation", "knowledge-communication")),
    ("Knowledge Architect", "institutional memory and knowledge preservation", ("knowledge-preservation", "architecture-documentation", "decision-records", "history-tracking")),
    ("Refactoring Guardian", "safe evolution of existing software through structure improvement without behavioral change", ("structure-preservation", "incremental-improvement", "code-clarity", "maintainability-enhancement", "dependency-analysis", "behavior-validation", "risk-assessment")),
    ("Workflow Coordinator", "organizing collaboration between specialized AI roles through continuity preservation, context transfer, and responsibility coordination", ("workflow-establishment", "state-management", "specialist-coordination", "sequencing", "handoff-integrity", "continuity-preservation", "conflict-resolution", "workflow-completion")),
    ("Deletion Authority", "governed analysis and execution of material removal with preserved recoverability and authorization verification", ("deletion-analysis", "candidate-identification", "dependency-assessment", "authorization-verification", "scope-control", "deletion-execution", "recoverability-preservation", "removal-documentation")),
    ("BP (Banana Peel)", "adversarial testing specialist identifying failure modes, edge cases, and assumption violations through deliberate chaos testing", ("edge-case-identification", "failure-mode-analysis", "assumption-testing", "adversarial-analysis", "boundary-violation-detection", "stress-testing", "recovery-validation", "resilience-assessment")),
    ("Archeologist", "ecosystem evolution specialist discovering missing capabilities and emerging specialties through pattern analysis and gap identification", ("capability-gap-analysis", "pattern-recognition", "workload-analysis", "specialist-interaction-analysis", "emerging-need-detection", "gem-recommendation", "impact-assessment", "evolution-roadmap")),
)


def build_default_registry() -> GemRegistry:
    registry = GemRegistry()
    for name, purpose, capabilities in CATALOG:
        registry.register(GemSpec(name=name, purpose=purpose, capabilities=capabilities))
    return registry
