from __future__ import annotations

from gems.contracts import GemSpec
from gems.core.registry import GemRegistry

CATALOG = (
    ("Requirements Analyst", "requirements analysis", ("requirements",)),
    ("Research Analyst", "research and analytical investigation", ("research",)),
    ("Engineering Architecture & Evolution", "engineering architecture and evolution", ("architecture",)),
    ("Code Review Sentinel", "code review", ("code-review",)),
    ("Integration Guardian", "integration oversight", ("integration",)),
    ("Security & Governance Auditor", "security and governance review", ("security", "governance")),
    ("Testing & Validation Engineer", "testing and validation", ("testing", "validation")),
    ("Documentation", "documentation production and maintenance", ("documentation",)),
    ("Knowledge Architect", "knowledge architecture", ("knowledge",)),
    ("Workflow Coordinator", "coordinate specialized Gem activity", ("coordination",)),
    ("Deletion Demon", "unspecified deletion/review concept", ("deletion-review",)),
)


def build_default_registry() -> GemRegistry:
    registry = GemRegistry()
    for name, purpose, capabilities in CATALOG:
        registry.register(GemSpec(name=name, purpose=purpose, capabilities=capabilities))
    return registry
