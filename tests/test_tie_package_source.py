"""The TIE package source: what a TIE package becomes at the GEMS boundary.

Skipped without ``conservation_kernel``, like the other transport tests. TIE is
not imported by the adapter; these tests use plain stand-ins with the
attributes TIE's types have, and one test uses the real TIE when it is
installed.
"""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

pytest.importorskip(
    "conservation_kernel",
    reason="gems_transport needs conservation_kernel (its own dependency)",
)
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "transport"))

from conservation_kernel import (
    AuthorityStatus,
    CanonicalState,
    EpistemicStatus,
    OriginStatus,
    UncertaintyState,
)
from conservation_kernel.errors import RootAdmissionError
from gems_transport import (
    ConservationGateway,
    TIEMappingError,
    TIEPackageSource,
)
from gems_transport.tie_package_source import NO_COVERAGE_STATEMENT

NOW = "2026-10-10T12:00:00Z"


def val(name):
    return NS(value=name)


def seg(status, n=0):
    return NS(segment_id=f"s{n}", status=val(status))


def ev(eid, status="EXPLICIT", origin="HUMAN", segment="s0", text=None):
    return NS(
        evidence_id=eid,
        statement=text or f"statement for {eid}",
        epistemic_status=val(status),
        provenance=NS(origin=val(origin)),
        segment_id=segment,
    )


def package(evidence=(), known=(), segments=None, evidence_ids=None, handoff=True):
    evidence = tuple(evidence)
    if segments is None:
        segments = (seg("INSPECTED"),)
    coverage = None if segments is False else NS(segments=tuple(segments))
    typed = NS(
        known_uncertainty=tuple(known),
        evidence_ids=tuple(e.evidence_id for e in evidence) if evidence_ids is None else evidence_ids,
    )
    return NS(
        package_id="p1",
        source=NS(source_id="src-1"),
        coverage=coverage,
        evidence=evidence,
        typed_handoff=typed if handoff else None,
    )


def load(pkg, **kwargs):
    return TIEPackageSource(pkg, created_at=NOW, **kwargs).load_artifact()


def by_id(artifact):
    return artifact.proposition_map()


# Statuses ----------------------------------------------------------------


def test_each_tie_status_maps_without_being_strengthened():
    artifact = load(
        package(
            [
                ev("e1", "EXPLICIT"),
                ev("e2", "INFERRED"),
                ev("e3", "UNKNOWN"),
                ev("e4", "CONFLICTED"),
            ]
        )
    )
    props = by_id(artifact)
    assert props["e1"].epistemic_status is EpistemicStatus.OBSERVATION
    assert props["e1"].epistemic_status is not EpistemicStatus.FACT
    assert props["e2"].epistemic_status is EpistemicStatus.INFERENCE
    assert props["e3"].epistemic_status is EpistemicStatus.UNKNOWN
    assert props["e4"].epistemic_status is EpistemicStatus.CONFLICTED
    assert props["e3"].uncertainty.state is UncertaintyState.UNKNOWN
    assert props["e4"].uncertainty.state is UncertaintyState.CONFLICTED


def test_tie_never_grants_authority_or_canonical_state():
    artifact = load(package([ev("e1", origin="HUMAN"), ev("e2", origin="AI")]))
    for prop in artifact.propositions:
        assert prop.authority is AuthorityStatus.NONE
        assert prop.canonical_state is CanonicalState.PROPOSED


def test_tie_own_vocabulary_is_kept_in_metadata():
    prop = by_id(load(package([ev("e1", "INFERRED", "AI", segment="s7")])))["e1"]
    assert prop.metadata["tie_epistemic_status"] == "INFERRED"
    assert prop.metadata["tie_origin"] == "AI"
    assert prop.metadata["tie_segment_id"] == "s7"
    assert prop.source_refs == ("src-1#s7",)


def test_an_unrecognised_status_or_origin_is_refused_not_guessed():
    with pytest.raises(TIEMappingError):
        load(package([ev("e1", status="PROBABLY")]))
    with pytest.raises(TIEMappingError):
        load(package([ev("e1", origin="ROBOT")]))


# Origin ------------------------------------------------------------------


def test_human_and_ai_origins_map_plainly():
    props = by_id(load(package([ev("h", origin="HUMAN"), ev("a", origin="AI")])))
    assert props["h"].origin is OriginStatus.HUMAN_ORIGINATED
    assert props["a"].origin is OriginStatus.MACHINE_ORIGINATED
    assert props["h"].uncertainty.state is UncertaintyState.NONE


def test_human_accepted_ai_is_not_upgraded_without_authorization():
    prop = by_id(load(package([ev("e1", origin="HUMAN_ACCEPTED_AI")])))["e1"]
    assert prop.origin is OriginStatus.MACHINE_ORIGINATED
    assert prop.uncertainty.state is UncertaintyState.UNCERTAIN
    assert "no authorization was supplied" in prop.uncertainty.reason
    assert prop.metadata["tie_origin"] == "HUMAN_ACCEPTED_AI"


def test_human_accepted_ai_with_authorization_is_carried_as_adopted():
    artifact = load(package([ev("e1", origin="HUMAN_ACCEPTED_AI")]), authorization_refs=("auth-1",))
    prop = by_id(artifact)["e1"]
    assert prop.origin is OriginStatus.HUMAN_ADOPTED_MACHINE_OUTPUT
    assert prop.authorization_refs == ("auth-1",)


def test_an_authorization_the_gateway_does_not_hold_is_refused_at_ingest():
    artifact = load(package([ev("e1", origin="HUMAN_ACCEPTED_AI")]), authorization_refs=("nope",))
    with pytest.raises(RootAdmissionError):
        ConservationGateway().ingest_source(artifact)


def test_unknown_origin_is_stated_not_hidden():
    prop = by_id(load(package([ev("e1", origin="UNKNOWN")])))["e1"]
    assert prop.origin is OriginStatus.EXTERNAL_ORIGINATED
    assert prop.uncertainty.state is UncertaintyState.UNCERTAIN
    assert "does not know who produced" in prop.uncertainty.reason


# Gaps --------------------------------------------------------------------


def gap_texts(artifact):
    return [p.text for p in artifact.propositions if p.metadata.get("tie_kind") == "gap"]


def test_known_uncertainty_is_carried_verbatim_as_unknown_claims():
    artifact = load(package([ev("e1")], known=("the speaker is not identified",)))
    assert gap_texts(artifact) == ["the speaker is not identified"]
    gap = next(p for p in artifact.propositions if p.metadata.get("tie_kind") == "gap")
    assert gap.epistemic_status is EpistemicStatus.UNKNOWN
    assert gap.uncertainty.state is UncertaintyState.UNKNOWN


def test_an_evidence_id_in_known_uncertainty_is_not_duplicated():
    artifact = load(package([ev("e1", "UNKNOWN")], known=("e1",)))
    assert gap_texts(artifact) == []
    assert by_id(artifact)["e1"].epistemic_status is EpistemicStatus.UNKNOWN


def test_uninspected_and_missing_segments_become_gaps():
    segments = [seg("INSPECTED", 0), seg("NOT_INSPECTED", 1), seg("MISSING", 2), seg("MISSING", 3)]
    artifact = load(package([ev("e1")], segments=segments))
    assert gap_texts(artifact) == [
        "1 of 4 source segments not inspected",
        "2 of 4 source segments missing from the source",
    ]


def test_a_gap_tie_already_stated_is_not_stated_twice():
    segments = [seg("INSPECTED", 0), seg("NOT_INSPECTED", 1)]
    stated = "1 of 2 source segments not inspected"
    artifact = load(package([ev("e1")], known=(stated,), segments=segments))
    assert gap_texts(artifact) == [stated]


def test_no_coverage_record_is_stated_not_read_as_full_coverage():
    for segments in (False, ()):
        artifact = load(package([ev("e1")], segments=segments))
        assert gap_texts(artifact) == [NO_COVERAGE_STATEMENT]


def test_fully_inspected_with_nothing_unknown_has_no_gap_claims():
    assert gap_texts(load(package([ev("e1"), ev("e2")]))) == []


def test_evidence_named_by_the_handoff_but_absent_is_a_gap():
    artifact = load(package([ev("e1")], evidence_ids=("e1", "e9")))
    assert gap_texts(artifact) == ["evidence e9 is named in the handoff but is not in the package"]


def test_every_gap_is_also_in_the_content_text():
    artifact = load(package([ev("e1")], known=("something unread",)))
    assert "Not known: something unread" in artifact.content


# Determinism and inputs --------------------------------------------------


def test_loading_twice_gives_the_same_digest_so_reingest_is_idempotent():
    pkg = package([ev("e1"), ev("e2", "INFERRED")], known=("x",))
    assert load(pkg).artifact_digest == load(pkg).artifact_digest
    gateway = ConservationGateway()
    first = gateway.ingest_source(load(pkg))
    assert gateway.ingest_source(load(pkg)) is first


def test_created_at_is_required_and_must_be_real():
    pkg = package([ev("e1")])
    for bad in ("", "   ", None):
        with pytest.raises(TIEMappingError):
            TIEPackageSource(pkg, created_at=bad)


def test_a_package_without_a_typed_handoff_is_refused():
    with pytest.raises(TIEMappingError):
        TIEPackageSource(package([ev("e1")], handoff=False), created_at=NOW)


def test_a_package_with_no_evidence_still_loads_and_says_what_it_lacks():
    artifact = load(package([], segments=False))
    assert gap_texts(artifact) == [NO_COVERAGE_STATEMENT]
    assert artifact.content.strip()


# The gateway and CNS -----------------------------------------------------


def test_the_artifact_enters_the_gateway_as_a_root_source():
    artifact = load(
        package(
            [ev("e1"), ev("e2", "INFERRED", "AI"), ev("e3", "CONFLICTED", "UNKNOWN")],
            known=("one thing TIE did not read",),
            segments=[seg("INSPECTED", 0), seg("NOT_INSPECTED", 1)],
        )
    )
    gateway = ConservationGateway()
    gateway.ingest_source(artifact)
    assert gateway.is_accepted(artifact)


def test_the_cns_input_gate_passes_an_ingested_tie_artifact_and_refuses_one_that_was_not():
    cns_gate = pytest.importorskip("cns.gate", reason="cns not installed")
    from gems_transport.cns_connector import CnsInputGate

    artifact = load(package([ev("e1")]))
    gateway = ConservationGateway()
    gate = CnsInputGate(gateway)
    assert gate.check(artifact).outcome is cns_gate.GateOutcome.TERMINAL_BREACH
    gateway.ingest_source(artifact)
    assert gate.check(artifact).outcome is cns_gate.GateOutcome.PASS


# Real TIE ----------------------------------------------------------------


def test_a_real_tie_package_with_a_declared_gap_arrives_with_the_gap():
    pytest.importorskip("tie", reason="TIE not installed")
    from tie.coverage.segmenter import segment_source
    from tie.evidence.extract import evidence_from_statement
    from tie.models import EpistemicStatus as TieStatus
    from tie.models import OriginKind, Provenance, SourceRecord
    from tie.package.builder import build_package

    source = SourceRecord(
        source_id="real-1",
        content="A" * 300,
        provenance=Provenance(origin=OriginKind.HUMAN_ACCEPTED_AI),
    )
    coverage = segment_source(source, max_chars=100, not_inspected=[(100, 200)])
    evidence = [
        evidence_from_statement(
            source,
            evidence_id="ev-1",
            statement="the call was escalated",
            epistemic_status=TieStatus.EXPLICIT,
            segment_id=coverage.segments[0].segment_id,
        )
    ]
    pkg = build_package(package_id="real-pkg", source=source, coverage=coverage, evidence=evidence)

    artifact = load(pkg)
    props = by_id(artifact)
    assert props["ev-1"].epistemic_status is EpistemicStatus.OBSERVATION
    assert props["ev-1"].origin is OriginStatus.MACHINE_ORIGINATED
    assert any("not inspected" in text for text in gap_texts(artifact))
    ConservationGateway().ingest_source(artifact)
