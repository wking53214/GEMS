"""Scoring rubric for GEMS and workflows."""

from typing import Dict, Any
from .metrics import GemMetrics, WorkflowMetrics


class ScoringRubric:
    """Evaluates and scores GEMS and workflow executions."""

    # Thresholds for quality ratings
    EXCELLENT_THRESHOLD = 0.95
    GOOD_THRESHOLD = 0.85
    ACCEPTABLE_THRESHOLD = 0.70

    @staticmethod
    def score_gem(metrics: GemMetrics) -> Dict[str, Any]:
        """Score an individual Gem execution (0-100)."""
        score = 0.0
        breakdown = {}

        # Routing correctness (25 points max)
        routing_score = 25.0 if metrics.routing_correct else 0.0
        breakdown["routing"] = routing_score
        score += routing_score

        # Context preservation (25 points max)
        context_score = 25.0 if metrics.context_preserved else 0.0
        breakdown["context"] = context_score
        score += context_score

        # Authority respect (25 points max)
        authority_score = 25.0 if metrics.authority_respected else 0.0
        breakdown["authority"] = authority_score
        score += authority_score

        # Output quality (25 points max)
        quality_score = metrics.output_quality_score * 25.0
        breakdown["quality"] = quality_score
        score += quality_score

        # Deductions for errors
        error_penalty = min(len(metrics.errors) * 5, 20)
        breakdown["errors"] = -error_penalty
        score -= error_penalty

        score = max(0, min(100, score))

        return {
            "total_score": score,
            "breakdown": breakdown,
            "rating": ScoringRubric._rating_from_score(score),
        }

    @staticmethod
    def score_workflow(metrics: WorkflowMetrics) -> Dict[str, Any]:
        """Score a complete workflow execution (0-100)."""
        score = 0.0
        breakdown = {}

        # Routing accuracy (30 points max)
        routing_score = metrics.routing_accuracy * 30.0
        breakdown["routing_accuracy"] = routing_score
        score += routing_score

        # Continuity preservation (30 points max)
        continuity_score = metrics.continuity_preservation * 30.0
        breakdown["continuity_preservation"] = continuity_score
        score += continuity_score

        # Authority respect (20 points max)
        # Deduct 5 points per violation, up to 20
        authority_score = 20.0 - min(metrics.authority_violations * 5, 20)
        breakdown["authority_respect"] = authority_score
        score += authority_score

        # Output quality (15 points max)
        quality_score = metrics.output_quality * 15.0
        breakdown["output_quality"] = quality_score
        score += quality_score

        # Efficiency (5 points max)
        efficiency_score = min(metrics.efficiency_rating * 5.0, 5.0)
        breakdown["efficiency"] = efficiency_score
        score += efficiency_score

        # Deductions for issues
        issue_penalty = min(len(metrics.issues) * 3, 15)
        breakdown["issues"] = -issue_penalty
        score -= issue_penalty

        score = max(0, min(100, score))

        return {
            "total_score": score,
            "breakdown": breakdown,
            "rating": ScoringRubric._rating_from_score(score),
            "success": metrics.success,
        }

    @staticmethod
    def score_system(all_workflows: Dict[str, WorkflowMetrics]) -> Dict[str, Any]:
        """Score the overall GEMS system based on all workflow executions."""
        if not all_workflows:
            return {
                "total_score": 0,
                "rating": "No Data",
                "message": "No workflows executed",
            }

        workflows = list(all_workflows.values())

        # Average workflow score
        workflow_scores = [
            ScoringRubric.score_workflow(w)["total_score"]
            for w in workflows
        ]
        avg_score = sum(workflow_scores) / len(workflow_scores)

        # Success rate bonus/penalty
        success_count = sum(1 for w in workflows if w.success)
        success_rate = success_count / len(workflows)

        # Consistency (all workflows score similarly)
        score_variance = (
            sum((s - avg_score) ** 2 for s in workflow_scores) / len(workflow_scores)
        )
        consistency_penalty = min(score_variance / 100, 10)

        total_score = avg_score - consistency_penalty
        total_score = max(0, min(100, total_score))

        return {
            "total_score": total_score,
            "rating": ScoringRubric._rating_from_score(total_score),
            "workflows_executed": len(workflows),
            "success_rate": success_rate,
            "average_workflow_score": avg_score,
            "consistency_score": 100 - consistency_penalty,
        }

    @staticmethod
    def _rating_from_score(score: float) -> str:
        """Convert numerical score to quality rating."""
        if score >= 95:
            return "Exceptional"
        elif score >= 85:
            return "Excellent"
        elif score >= 75:
            return "Good"
        elif score >= 60:
            return "Acceptable"
        elif score >= 40:
            return "Poor"
        else:
            return "Failed"
