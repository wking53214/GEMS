"""Turn a TIE package into a Conservation Kernel ``Artifact``.

This is the producer for the slot in ``tie_adapter``. Hand the result to
``ConservationGateway.ingest_source``, which is where a root source artifact
enters the gateway.

It is duck-typed. Nothing from TIE is imported, so GEMS gains no dependency on
it; the package only needs the attributes TIE's own types have.

What it carries
---------------
The whole package is needed, not just the typed handoff, because the handoff
holds evidence IDs and the kernel needs the statements.

* Each TIE evidence record becomes one proposition, with TIE's own status and
  origin kept in its metadata so the mapping can be checked.
* Everything TIE says it does not know becomes a proposition of its own with
  status UNKNOWN: the handoff's ``known_uncertainty``, coverage gaps the
  coverage record implies, and a statement when there is no coverage record at
  all. A gap that is only a metadata field can be dropped by a later
  transformation unnoticed; a proposition is checked by the kernel.

What it does not carry
----------------------
TIE's named artifacts, identity references, relationships and reconstruction
are not converted. Only evidence and gaps are.

How statuses map, and why
-------------------------
* EXPLICIT is OBSERVATION, not FACT. TIE's EXPLICIT means present in the source
  as written; it does not mean verified.
* INFERRED is INFERENCE. UNKNOWN and CONFLICTED keep their names.
* Authority is always NONE and canonical state PROPOSED. TIE grants neither.
* HUMAN is HUMAN_ORIGINATED and AI is MACHINE_ORIGINATED.
* HUMAN_ACCEPTED_AI is HUMAN_ADOPTED_MACHINE_OUTPUT only when the caller
  supplies ``authorization_refs``, because the kernel requires an authorization
  event for that origin and TIE records only a label. Without them it is carried
  as MACHINE_ORIGINATED with a stated uncertainty. That understates a human's
  part, which is the safe direction.
* UNKNOWN origin has no kernel equivalent. It is carried as EXTERNAL_ORIGINATED
  with a stated uncertainty that TIE does not know who produced it.

Anything it cannot map raises ``TIEMappingError``; nothing is guessed.

``created_at`` is required. The kernel puts it in the artifact digest, so a
clock reading would make ingesting the same package twice a digest conflict.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from conservation_kernel import (
    Actor,
    Artifact,
    EpistemicStatus,
    OriginStatus,
    Proposition,
    Uncertainty,
    UncertaintyState,
)

NO_COVERAGE_STATEMENT = (
    "no coverage record was reported, so how much of the source was read is unknown"
)

_EPISTEMIC = {
    "EXPLICIT": EpistemicStatus.OBSERVATION,
    "INFERRED": EpistemicStatus.INFERENCE,
    "UNKNOWN": EpistemicStatus.UNKNOWN,
    "CONFLICTED": EpistemicStatus.CONFLICTED,
}

_GAP_LABELS = {
    "NOT_INSPECTED": "not inspected",
    "MISSING": "missing from the source",
}


class TIEMappingError(ValueError):
    """The package holds something this adapter will not guess a mapping for."""


def _value(thing: Any) -> str | None:
    if thing is None:
        return None
    return str(getattr(thing, "value", thing))


class TIEPackageSource:
    """Implements ``TIEArtifactSource`` for one TIE package."""

    def __init__(
        self,
        package: Any,
        *,
        created_at: str,
        authorization_refs: Sequence[str] = (),
    ) -> None:
        if not isinstance(created_at, str) or not created_at.strip():
            raise TIEMappingError("created_at must be a non-empty timestamp string")
        if getattr(package, "typed_handoff", None) is None:
            raise TIEMappingError("the package has no typed handoff")
        self._package = package
        self._created_at = created_at
        self._authorization_refs = tuple(authorization_refs)

    def load_artifact(self) -> Artifact:
        package = self._package
        handoff = package.typed_handoff
        source_id = package.source.source_id
        evidence = tuple(package.evidence)

        propositions = [self._evidence_proposition(e, source_id) for e in evidence]
        gaps = self._gaps(package, handoff, evidence)
        for index, gap in enumerate(gaps, start=1):
            propositions.append(
                Proposition(
                    proposition_id=f"tie-gap-{index}",
                    text=gap,
                    epistemic_status=EpistemicStatus.UNKNOWN,
                    origin=OriginStatus.MACHINE_ORIGINATED,
                    uncertainty=Uncertainty(UncertaintyState.UNKNOWN, gap),
                    source_refs=(source_id,),
                    metadata={"tie_kind": "gap"},
                )
            )

        lines = [f"TIE package {package.package_id} from source {source_id}."]
        lines += [f"[{_value(e.epistemic_status)}] {e.statement}" for e in evidence]
        lines += [f"Not known: {gap}" for gap in gaps]

        return Artifact(
            artifact_id=f"tie-{package.package_id}",
            content="\n".join(lines),
            propositions=tuple(propositions),
            producer=Actor.external("tie", "Transcript Intelligence Engine"),
            created_at=self._created_at,
        )

    def _evidence_proposition(self, record: Any, source_id: str) -> Proposition:
        status = _value(record.epistemic_status)
        if status not in _EPISTEMIC:
            raise TIEMappingError(
                f"evidence {record.evidence_id}: unrecognised epistemic status {status!r}"
            )
        origin_name = _value(getattr(record.provenance, "origin", None)) or "UNKNOWN"
        origin, origin_reason, auth = self._origin(record.evidence_id, origin_name)

        state, reason = UncertaintyState.NONE, ""
        if status == "UNKNOWN":
            state, reason = UncertaintyState.UNKNOWN, "TIE marks this evidence UNKNOWN"
        elif status == "CONFLICTED":
            state, reason = UncertaintyState.CONFLICTED, "TIE marks this evidence CONFLICTED"
        if origin_reason:
            reason = f"{reason}; {origin_reason}" if reason else origin_reason
            if state is UncertaintyState.NONE:
                state = UncertaintyState.UNCERTAIN

        segment = getattr(record, "segment_id", None)
        return Proposition(
            proposition_id=record.evidence_id,
            text=record.statement,
            epistemic_status=_EPISTEMIC[status],
            origin=origin,
            uncertainty=Uncertainty(state, reason),
            authorization_refs=auth,
            source_refs=(f"{source_id}#{segment}" if segment else source_id,),
            metadata={
                "tie_kind": "evidence",
                "tie_epistemic_status": status,
                "tie_origin": origin_name,
                "tie_segment_id": segment,
            },
        )

    def _origin(self, evidence_id: str, name: str):
        if name == "HUMAN":
            return OriginStatus.HUMAN_ORIGINATED, "", ()
        if name == "AI":
            return OriginStatus.MACHINE_ORIGINATED, "", ()
        if name == "HUMAN_ACCEPTED_AI":
            if self._authorization_refs:
                return (
                    OriginStatus.HUMAN_ADOPTED_MACHINE_OUTPUT,
                    "",
                    self._authorization_refs,
                )
            return (
                OriginStatus.MACHINE_ORIGINATED,
                (
                    "TIE records that a person accepted this machine output, but no "
                    "authorization was supplied, so it is carried as machine originated"
                ),
                (),
            )
        if name == "UNKNOWN":
            return (
                OriginStatus.EXTERNAL_ORIGINATED,
                "TIE does not know who produced this",
                (),
            )
        raise TIEMappingError(f"evidence {evidence_id}: unrecognised origin {name!r}")

    @staticmethod
    def _gaps(package: Any, handoff: Any, evidence: tuple) -> list[str]:
        evidence_ids = {e.evidence_id for e in evidence}
        gaps: list[str] = []

        def add(text: str) -> None:
            if text and text not in gaps:
                gaps.append(text)

        # An entry that is just an evidence ID is already carried by that
        # evidence's own UNKNOWN or CONFLICTED status.
        for entry in getattr(handoff, "known_uncertainty", None) or ():
            if entry not in evidence_ids:
                add(entry)

        for named in getattr(handoff, "evidence_ids", None) or ():
            if named not in evidence_ids:
                add(f"evidence {named} is named in the handoff but is not in the package")

        segments = tuple(getattr(package.coverage, "segments", None) or ()) if package.coverage else ()
        if not segments:
            add(NO_COVERAGE_STATEMENT)
        else:
            counts: dict[str, int] = {}
            for segment in segments:
                name = _value(getattr(segment, "status", None)) or "UNKNOWN"
                counts[name] = counts.get(name, 0) + 1
            # TIE's own order (not inspected, then missing), then any other
            # status alphabetically.
            known = [n for n in _GAP_LABELS if n in counts]
            other = sorted(n for n in counts if n not in _GAP_LABELS)
            for name in known + other:
                if name == "INSPECTED":
                    continue
                label = _GAP_LABELS.get(name, f"with status {name.lower()}")
                add(f"{counts[name]} of {len(segments)} source segments {label}")
        return gaps
