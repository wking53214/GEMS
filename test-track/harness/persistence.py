"""Results persistence for GEMS workflow executions."""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from .metrics import WorkflowMetrics


class ResultsPersistence:
    """Saves and retrieves workflow execution results."""

    def __init__(self, results_dir: str = "test-track/results"):
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def save_run(
        self,
        workflows: Dict[str, WorkflowMetrics],
        run_name: str = None,
    ) -> str:
        """
        Save a complete test run with all workflow results.

        Returns the path where results were saved.
        """
        if run_name is None:
            run_name = datetime.now().strftime("%Y%m%d_%H%M%S")

        run_data = {
            "timestamp": datetime.now().isoformat(),
            "run_name": run_name,
            "workflows": {
                wid: metrics.as_dict()
                for wid, metrics in workflows.items()
            },
        }

        # Calculate aggregate stats
        stats = self._calculate_stats(workflows)
        run_data["aggregate_stats"] = stats

        # Save to JSON file
        output_file = self.results_dir / f"{run_name}_results.json"
        with open(output_file, "w") as f:
            json.dump(run_data, f, indent=2)

        return str(output_file)

    def get_trends(self, limit: int = None) -> List[Dict[str, Any]]:
        """Get trends from previous runs."""
        runs = sorted(self.results_dir.glob("*_results.json"), reverse=True)

        if limit:
            runs = runs[:limit]

        trends = []
        for run_file in runs:
            with open(run_file) as f:
                data = json.load(f)
                trends.append({
                    "timestamp": data["timestamp"],
                    "run_name": data["run_name"],
                    "stats": data.get("aggregate_stats", {}),
                })

        return trends

    @staticmethod
    def _calculate_stats(workflows: Dict[str, WorkflowMetrics]) -> Dict[str, Any]:
        """Calculate aggregate statistics from workflows."""
        if not workflows:
            return {}

        metrics_list = list(workflows.values())

        stats = {
            "total_workflows": len(metrics_list),
            "successful_workflows": sum(1 for m in metrics_list if m.success),
            "success_rate": sum(1 for m in metrics_list if m.success) / len(metrics_list),
            "avg_routing_accuracy": sum(m.routing_accuracy for m in metrics_list) / len(metrics_list),
            "avg_continuity_preservation": sum(m.continuity_preservation for m in metrics_list) / len(metrics_list),
            "total_authority_violations": sum(m.authority_violations for m in metrics_list),
            "avg_output_quality": sum(m.output_quality for m in metrics_list) / len(metrics_list),
            "avg_efficiency": sum(m.efficiency_rating for m in metrics_list) / len(metrics_list),
            "total_execution_time": sum(m.total_duration_seconds for m in metrics_list),
        }

        return stats
