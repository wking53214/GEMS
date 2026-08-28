"""Run the bounded GEMS control/treatment experiment."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from gems_transport import ConservationGateway, Pipeline
from gems_transport.reference_gems import ArchitectureGem, RequirementsGem, ResearcherGem, ReviewerGem, SummarizerGem

from .attacks import control_outcomes, run_hostile_corpus
from .corpus import HumanApprovalFixture, fixed_clock, synthetic_tie_source


def run_reference_pipeline() -> dict[str, Any]:
    fixture = synthetic_tie_source()
    gateway = ConservationGateway(registry=fixture.registry)
    pipeline = Pipeline(gateway)
    gems = (
        SummarizerGem(clock=fixed_clock),
        ResearcherGem(clock=fixed_clock),
        RequirementsGem(clock=fixed_clock),
        ArchitectureGem(clock=fixed_clock),
        ReviewerGem(clock=fixed_clock),
    )
    run = pipeline.run(fixture.artifact, gems)
    approval = HumanApprovalFixture(clock=fixed_clock)
    gateway.register_gem(approval.identity)
    approved_request = approval.make_request(
        run.final_artifact,
        transformation_type="HUMAN_APPROVAL",
        intent="apply externally registered human authorization",
        request_suffix="canonical-approval",
    )
    # ``authorize`` creates the same request shape and registers the external
    # events.  The explicit request above is not used as an authority source;
    # the fixture's proposal is what enters the gateway.
    approved_proposal = approval.authorize(gateway.registry, run.final_artifact)
    approved_result = gateway.submit(approved_request, approved_proposal)
    reconstruction = gateway.reconstruct(approved_result.accepted_artifact.artifact_id)
    return {
        "source_artifact_id": fixture.artifact.artifact_id,
        "gem_sequence": [item.identity.to_dict() for item in gems],
        "accepted_transformations": len(gateway.accepted_transformations()),
        "approval_accepted": approved_result.accepted,
        "final_artifact_id": approved_result.accepted_artifact.artifact_id if approved_result.accepted else None,
        "reconstruction": reconstruction.to_dict(),
    }


def run_experiment() -> dict[str, Any]:
    treatment = [item.to_dict() for item in run_hostile_corpus()]
    control = list(control_outcomes())
    reference = run_reference_pipeline()
    return {
        "protocol_version": "GEMS/0.1",
        "experiment": "deterministic-hostile-transport-baseline",
        "control": {
            "total_transformations": len(control),
            "accepted": sum(1 for item in control if item["accepted"]),
            "unauthorized_acceptance": sum(1 for item in control if item["accepted"]),
            "outcomes": control,
        },
        "treatment": {
            "total_transformations": len(treatment),
            "accepted": sum(1 for item in treatment if item["accepted"]),
            "rejected_or_contained": sum(1 for item in treatment if item["blocked"]),
            "unauthorized_acceptance": sum(1 for item in treatment if item["accepted"]),
            "outcomes": treatment,
        },
        "reference_pipeline": reference,
        "claims": {
            "mechanism_test": "TEST-VERIFIED if the repository test suite and this run pass",
            "general_superiority": "UNVERIFIED",
            "external_truth_verification": "FALSIFIED",
            "external_process_enforcement": "FALSIFIED",
        },
    }


def main() -> None:
    report = run_experiment()
    result_path = Path(__file__).parent / "results" / "initial_run.json"
    result_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "experiment": report["experiment"],
        "control_accepted": report["control"]["accepted"],
        "treatment_accepted": report["treatment"]["accepted"],
        "treatment_rejected_or_contained": report["treatment"]["rejected_or_contained"],
        "reference_pipeline_accepted": report["reference_pipeline"]["approval_accepted"],
        "result_path": str(result_path),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
