"""Metrics collection and tracking for GEMS workflows."""

from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class GemMetrics:
    """Metrics for a single Gem execution."""
    gem_name: str
    duration_seconds: float
    routing_correct: bool
    context_preserved: bool
    authority_respected: bool
    output_quality_score: float  # 0-1
    errors: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "gem_name": self.gem_name,
            "duration_seconds": self.duration_seconds,
            "routing_correct": self.routing_correct,
            "context_preserved": self.context_preserved,
            "authority_respected": self.authority_respected,
            "output_quality_score": self.output_quality_score,
            "errors": self.errors,
        }


@dataclass
class WorkflowMetrics:
    """Aggregated metrics for a complete workflow execution."""
    workflow_id: str
    total_duration_seconds: float
    gem_count: int
    gems_executed: List[str]
    gem_metrics: Dict[str, GemMetrics] = field(default_factory=dict)

    routing_accuracy: float = 0.0
    continuity_preservation: float = 0.0
    authority_violations: int = 0
    output_quality: float = 0.0
    efficiency_rating: float = 0.0

    success: bool = True
    issues: List[str] = field(default_factory=list)

    def calculate_aggregate_scores(self) -> None:
        """Calculate aggregate scores from individual gem metrics."""
        if not self.gem_metrics:
            return

        metrics_list = list(self.gem_metrics.values())
        n = len(metrics_list)

        # Routing accuracy: percentage of correct routings
        correct_routings = sum(1 for m in metrics_list if m.routing_correct)
        self.routing_accuracy = correct_routings / n if n > 0 else 0.0

        # Continuity preservation: percentage with context preserved
        context_preserved = sum(1 for m in metrics_list if m.context_preserved)
        self.continuity_preservation = context_preserved / n if n > 0 else 0.0

        # Authority violations: count of authority boundary issues
        self.authority_violations = sum(1 for m in metrics_list if not m.authority_respected)

        # Output quality: average of all gem output quality scores
        self.output_quality = sum(m.output_quality_score for m in metrics_list) / n if n > 0 else 0.0

        # Efficiency: 1.0 means on time, <1.0 means over budget, >1.0 means ahead of schedule
        # This is set by workflow executor based on time estimates

    def as_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "total_duration_seconds": self.total_duration_seconds,
            "gem_count": self.gem_count,
            "gems_executed": self.gems_executed,
            "routing_accuracy": self.routing_accuracy,
            "continuity_preservation": self.continuity_preservation,
            "authority_violations": self.authority_violations,
            "output_quality": self.output_quality,
            "efficiency_rating": self.efficiency_rating,
            "success": self.success,
            "issues": self.issues,
            "gem_details": {name: m.as_dict() for name, m in self.gem_metrics.items()},
        }


class MetricsCollector:
    """Collects and aggregates metrics across multiple workflow executions."""

    def __init__(self):
        self.workflows: Dict[str, WorkflowMetrics] = {}

    def add_workflow_metrics(self, metrics: WorkflowMetrics) -> None:
        """Record metrics for a completed workflow."""
        self.workflows[metrics.workflow_id] = metrics

    def get_aggregate_stats(self) -> Dict[str, float]:
        """Get aggregate statistics across all workflows."""
        if not self.workflows:
            return {}

        workflows = list(self.workflows.values())

        return {
            "total_workflows": len(workflows),
            "successful_workflows": sum(1 for w in workflows if w.success),
            "success_rate": sum(1 for w in workflows if w.success) / len(workflows),
            "avg_routing_accuracy": sum(w.routing_accuracy for w in workflows) / len(workflows),
            "avg_continuity_preservation": sum(w.continuity_preservation for w in workflows) / len(workflows),
            "total_authority_violations": sum(w.authority_violations for w in workflows),
            "avg_output_quality": sum(w.output_quality for w in workflows) / len(workflows),
            "total_execution_time": sum(w.total_duration_seconds for w in workflows),
        }

    def report(self) -> str:
        """Generate a text report of collected metrics."""
        stats = self.get_aggregate_stats()

        lines = [
            "GEMS Test Track Metrics Report",
            "=" * 50,
            f"Total Workflows Executed: {stats.get('total_workflows', 0)}",
            f"Successful: {stats.get('successful_workflows', 0)}/{stats.get('total_workflows', 0)}",
            f"Success Rate: {stats.get('success_rate', 0):.1%}",
            "",
            "Aggregate Metrics:",
            f"  Routing Accuracy: {stats.get('avg_routing_accuracy', 0):.1%}",
            f"  Continuity Preservation: {stats.get('avg_continuity_preservation', 0):.1%}",
            f"  Authority Violations: {stats.get('total_authority_violations', 0)}",
            f"  Output Quality: {stats.get('avg_output_quality', 0):.1%}",
            f"  Total Execution Time: {stats.get('total_execution_time', 0):.1f}s",
        ]

        return "\n".join(lines)
