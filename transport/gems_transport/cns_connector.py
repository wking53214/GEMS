"""Optional connector to CNS (``cns.gate``) for the GEMS transport gateway.

The transport package is independent of CNS. It has no CNS dependency, imports
nothing from CNS when it loads, and everything in it works with CNS absent.
This module is the one place in ``gems_transport`` that knows CNS exists, and
it asks for CNS only when one of its functions is called. Without CNS installed
those calls raise :class:`CnsNotInstalled` with the install command; nothing
else is affected. ``gems_transport/__init__`` does not import this module.

What connecting means
---------------------
The gateway keeps its own verdicts. Its output end is
:meth:`ConservationGateway.submit`, which returns a
:class:`~gems_transport.contracts.TransformationResult` whose ``decision`` is
``ACCEPTED``, ``REJECTED``, ``REQUIRES_AUTHORIZATION`` or
``REQUIRES_VERIFICATION``. Its input end is
:meth:`ConservationGateway.is_accepted`, which ``Pipeline`` turns into a
``BoundaryViolation`` ("input gate refused artifact") before any Gem runs.
CNS's shared gate contract is ``cns.gate.GateResult`` (``gate``, ``position``,
``outcome``, ``reason``, ``subject``, ``subject_digest``). This module
translates the gateway's verdicts into it without changing them, so a consumer
that speaks CNS can resolve them alongside gates from other repositories.

The two ends and where they sit
-------------------------------
* **The input gate is the ALPHA end.** ``Pipeline.execute`` and
  ``Pipeline.submit_one`` check ``is_accepted`` before ``gem.make_request`` and
  ``gem.transform``. A refusal means the Gem never runs
  (``experiments.attacks`` names it ``INPUT_GATE_REQUIRED``).
* **``submit`` is the OMEGA end.** The Gem's output is an untrusted proposal;
  ``submit`` judges the produced candidate and only an accepted one is promoted
  to the accepted-artifact map. A refusal means the result does not leave.

``Pipeline`` runs both on the same artifact in that order, so the transport has
both ends and ``cns_chain(gateway).complete()`` is ``True``. That says the two
slots are filled by the gateway's two real ends, and nothing more. The connector
is not wired into ``Pipeline``, and nothing here enforces the order or that both
verdicts concern one request. Their content overlaps: the ALPHA digest is over
the artifact's id and digest, and the OMEGA digest is over a different mapping
that holds the same pair as ``source``. The two digests are not comparable with
each other, so a consumer holding the two results cannot read "same request"
off them without recomputing. Running the ends in order, on the same artifact,
is the consumer's responsibility. The gates also take different candidates, an
``Artifact`` for the input gate and a ``GatewaySubmission`` for the output
gate, so a consumer calls each with its own.

The mapping, and why
--------------------
=====================================  =====================================
gateway                                CNS
=====================================  =====================================
``is_accepted`` true                   ``PASS`` at ``ALPHA``
``is_accepted`` false                  ``TERMINAL_BREACH`` at ``ALPHA``
decision ``ACCEPTED``                  ``PASS`` at ``OMEGA``
decision ``REQUIRES_AUTHORIZATION``    ``TERMINAL_BREACH``
decision ``REQUIRES_VERIFICATION``     ``TERMINAL_BREACH``
decision ``REJECTED``                  ``TERMINAL_BREACH``
=====================================  =====================================

``RETRY`` is never produced. In CNS a retry means the work may be re-rendered
with an instructional delta, and this repo models no repair of a refused
submission: ``Pipeline.execute`` stops at the first non-accepted result,
``Pipeline.run`` raises ``PipelineRejected``, and the repo's own hostile corpus
expects ``REJECTED`` for every attack that reaches ``submit`` (including the
ones the gateway reports as ``REQUIRES_AUTHORIZATION`` or
``REQUIRES_VERIFICATION``). The gateway cannot tell an honest missing
authorization from a forged one and reports both the same way, and ``reason``
carries the refusal codes and details, which is what a retry loop would feed
straight back to the Gem that made the proposal. So the two ``REQUIRES_*``
decisions are ``TERMINAL_BREACH`` like ``REJECTED``, with the decision's own
name and the refusal codes first in ``reason``. A human or evidence event
registered afterwards (``register_authorization``, ``register_evidence``) is a
new request for the consumer to make; this connector offers no retry for it.

Fail closed: ``PASS`` needs the gateway's own acceptance and a coherent result
(state ``ACCEPTED`` and an accepted artifact present) and a verdict that could
be bound to what it judged. Anything else, including an unknown decision status
and content CNS cannot digest, is ``TERMINAL_BREACH``.

What a verdict is bound to
--------------------------
``subject`` is a label (default ``"input_artifact"`` or ``"transformation"``).
``subject_digest`` is ``cns.gate.subject_digest`` over a mapping made only of
strings and lists of strings:

* input gate: ``{"kind": "gateway_input", "artifact_id", "artifact_digest"}``;
* output gate: ``{"kind": "gems_transformation", "request_id",
  "transformation_id", "gem" (the registered identity), "source" (id, digest,
  relation), "output_artifact" (id, digest of the candidate judged),
  "record_digest"}``, where ``record_digest`` is the kernel's own
  ``TransformationRecord.canonical_digest()``.

The kernel already digests everything it judges, so this binds the verdict to
that content and keeps the CNS-side input to str only. The evidence registry is
the witness the verdict was judged *against*, not the thing judged, and is not
in the digest.

One real input cannot be expressed: a non-finite float in a declared change.
The kernel builds such a record but ``canonical_digest()`` refuses it, and so
does CNS. The verdict is then ``TERMINAL_BREACH`` and unbound (empty
``subject_digest``, so ``cns.gate.unbound`` names it) with the reason saying
why; it is never ``PASS``. A result with no record or no candidate artifact is
handled the same way.

``CnsOutputGate.check`` *is* ``ConservationGateway.submit``: in this repo judging
and promotion are one step, by design, so an accepted candidate is promoted and
a second ``check`` of it is refused as a duplicate. The state changes are
exactly the ones a direct ``submit`` makes.

Install with the extra: ``pip install 'gems-infrastructure[cns]'`` (the
transport also needs ``conservation-kernel``, which the package already
requires).
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from types import ModuleType
from typing import Any, Callable

from conservation_kernel import Artifact

from .contracts import (
    DecisionStatus,
    TransformationProposal,
    TransformationRequest,
    TransformationResult,
    TransportState,
)
from .transport import ConservationGateway

__all__ = [
    "CnsInputGate",
    "CnsNotInstalled",
    "CnsOutputGate",
    "GatewaySubmission",
    "cns_available",
    "cns_chain",
    "input_digest",
    "input_to_cns_result",
    "submit_to_cns",
    "to_cns_result",
    "transformation_digest",
]

INSTALL_HINT = "pip install 'gems-infrastructure[cns]'"

#: The ``gate`` field of an input gate verdict.
INPUT_GATE_NAME = "gateway_input"
#: The ``gate`` field of an output gate verdict.
OUTPUT_GATE_NAME = "gateway_output"
#: What ``subject`` is set to when the caller does not name the judged content.
DEFAULT_INPUT_SUBJECT = "input_artifact"
DEFAULT_OUTPUT_SUBJECT = "transformation"


class CnsNotInstalled(ImportError):
    """Raised by this module's functions when ``cns`` cannot be imported."""


def _cns_gate() -> ModuleType:
    """Import ``cns.gate`` on demand, or say exactly what is missing."""
    try:
        return importlib.import_module("cns.gate")
    except ImportError as exc:
        raise CnsNotInstalled(
            "gems_transport.cns_connector needs the CNS package (cns.gate), which "
            f"is not installed. Install it with: {INSTALL_HINT}. The GEMS "
            "transport itself works without it."
        ) from exc


def cns_available() -> bool:
    """Whether the CNS gate contract can be imported in this environment."""
    try:
        _cns_gate()
    except CnsNotInstalled:
        return False
    return True


@dataclass(frozen=True)
class GatewaySubmission:
    """One proposal as the gateway judges it: the request and the Gem's proposal."""

    request: TransformationRequest
    proposal: TransformationProposal

    def __post_init__(self) -> None:
        if not isinstance(self.request, TransformationRequest):
            raise TypeError(
                f"request must be a TransformationRequest; got {type(self.request).__name__}"
            )
        if not isinstance(self.proposal, TransformationProposal):
            raise TypeError(
                f"proposal must be a TransformationProposal; got {type(self.proposal).__name__}"
            )


def _artifact_ref(artifact: Artifact) -> dict[str, str]:
    return {
        "artifact_id": artifact.artifact_id,
        "artifact_digest": str(artifact.artifact_digest),
    }


def _input_content(artifact: Artifact) -> dict[str, Any]:
    return {"kind": "gateway_input", **_artifact_ref(artifact)}


def _transformation_content(result: TransformationResult) -> dict[str, Any]:
    """The judged content of a result, as str-only canonical input.

    ``canonical_digest()`` raises ``ValueError`` for a non-finite float in a
    declared change; callers that must not raise go through ``_bind``.
    """
    record = result.record
    candidate = result.candidate_artifact
    if record is None or candidate is None:
        raise ValueError("the result carries no record or no candidate artifact to bind to")
    return {
        "kind": "gems_transformation",
        "request_id": result.request_id,
        "transformation_id": result.transformation_id,
        "gem": record.gem.to_dict(),
        "source": record.source.to_dict(),
        "output_artifact": _artifact_ref(candidate),
        "record_digest": record.kernel_record.canonical_digest(),
    }


def input_digest(artifact: Artifact) -> str:
    """The digest a bound input gate verdict on ``artifact`` carries."""
    return _cns_gate().subject_digest(_input_content(artifact))


def transformation_digest(result: TransformationResult) -> str:
    """The digest a bound output gate verdict on ``result`` carries.

    Pass it, with the subject label, to ``GateResult.binds`` to check that a
    verdict was issued against exactly this transformation. Raises for a result
    the kernel cannot digest (a verdict on one is unbound).
    """
    return _cns_gate().subject_digest(_transformation_content(result))


def _bind(cns_gate: ModuleType, content: Callable[[], dict[str, Any]]) -> tuple[str, str]:
    """``(digest, problem)``; ``digest`` is empty when the content cannot be digested.

    Any failure to build or digest the content means the verdict cannot be
    bound. That is reported, never raised, so it can fail the verdict closed.
    """
    try:
        return cns_gate.subject_digest(content()), ""
    except Exception as exc:  # noqa: BLE001 - every cause fails closed the same way
        return "", f"{type(exc).__name__}: {exc}"


def _require_subject(subject: str) -> None:
    if not isinstance(subject, str) or not subject:
        raise ValueError(
            "subject must be a non-empty label; an unlabelled verdict binds to nothing"
        )


def _verdict(
    cns_gate: ModuleType,
    *,
    gate_name: str,
    position: Any,
    outcome: Any,
    reason: str,
    subject: str,
    content: Callable[[], dict[str, Any]],
) -> Any:
    """Build the verdict, refusing to issue a PASS that is not bound."""
    digest, problem = _bind(cns_gate, content)
    if not digest:
        outcome = cns_gate.GateOutcome.TERMINAL_BREACH
        reason = f"unbound, the judged content cannot be digested canonically ({problem}); {reason}"
    return cns_gate.GateResult(
        gate=gate_name,
        position=position,
        outcome=outcome,
        reason=reason,
        subject=subject,
        subject_digest=digest,
    )


def _label(value: Any) -> str:
    """An enum's value, not its ``str()``, which differs across Python versions."""
    return str(getattr(value, "value", value))


def _output_outcome(cns_gate: ModuleType, result: TransformationResult) -> tuple[Any, str]:
    """``(outcome, reason)`` for the gateway's decision, failing closed."""
    decision = result.decision
    status = decision.status
    detail = "; ".join(f"{item.code}: {item.detail}" for item in decision.rejections)
    if status is DecisionStatus.ACCEPTED:
        if result.state is TransportState.ACCEPTED and result.accepted_artifact is not None:
            return cns_gate.GateOutcome.PASS, f"ACCEPTED (kernel status {decision.kernel_status})"
        present = "present" if result.accepted_artifact is not None else "absent"
        return (
            cns_gate.GateOutcome.TERMINAL_BREACH,
            "decision is ACCEPTED but the result is not coherent "
            f"(state {_label(result.state)}, accepted artifact {present})",
        )
    # REJECTED, REQUIRES_AUTHORIZATION, REQUIRES_VERIFICATION and any status this
    # code does not know are all refusals: the repo models no repair, so there
    # is no RETRY here (see the module docstring).
    return cns_gate.GateOutcome.TERMINAL_BREACH, f"{_label(status)}: {detail}"


def to_cns_result(
    result: TransformationResult,
    *,
    subject: str = DEFAULT_OUTPUT_SUBJECT,
) -> Any:
    """Translate the gateway's verdict in ``result`` into a ``cns.gate.GateResult``.

    The position is ``OMEGA``. ``PASS`` exactly when the gateway accepted and
    promoted the candidate and the verdict could be bound to it; every other
    case, the two ``REQUIRES_*`` decisions included, is ``TERMINAL_BREACH``.
    ``RETRY`` is never produced.
    """
    cns_gate = _cns_gate()
    _require_subject(subject)
    if not isinstance(result, TransformationResult):
        raise TypeError(
            f"the gateway's verdict is a TransformationResult; got {type(result).__name__}"
        )
    outcome, reason = _output_outcome(cns_gate, result)
    return _verdict(
        cns_gate,
        gate_name=OUTPUT_GATE_NAME,
        position=cns_gate.GatePosition.OMEGA,
        outcome=outcome,
        reason=reason,
        subject=subject,
        content=lambda: _transformation_content(result),
    )


def input_to_cns_result(
    accepted: bool,
    artifact: Artifact,
    *,
    subject: str = DEFAULT_INPUT_SUBJECT,
) -> Any:
    """Translate ``ConservationGateway.is_accepted(artifact)`` into a ``GateResult``.

    The position is ``ALPHA``: the artifact is judged before any Gem runs on
    it. ``True`` is ``PASS`` and ``False`` is ``TERMINAL_BREACH``; nothing
    repairs a non-accepted artifact at this end, ``Pipeline`` just refuses.
    """
    cns_gate = _cns_gate()
    _require_subject(subject)
    if not isinstance(accepted, bool):
        # A truthy non-bool (a non-empty string) must not read as acceptance.
        raise TypeError(
            f"accepted must be the bool is_accepted returned; got {type(accepted).__name__}"
        )
    if not isinstance(artifact, Artifact):
        raise TypeError(f"the input gate judges an Artifact; got {type(artifact).__name__}")
    if accepted:
        outcome = cns_gate.GateOutcome.PASS
        reason = "artifact is accepted by this gateway"
    else:
        outcome = cns_gate.GateOutcome.TERMINAL_BREACH
        reason = (
            f"INPUT_GATE_REQUIRED: artifact {artifact.artifact_id} is not accepted "
            "by this GEMS gateway"
        )
    return _verdict(
        cns_gate,
        gate_name=INPUT_GATE_NAME,
        position=cns_gate.GatePosition.ALPHA,
        outcome=outcome,
        reason=reason,
        subject=subject,
        content=lambda: _input_content(artifact),
    )


class CnsInputGate:
    """The gateway's input gate as a ``cns.gate.Gate`` at the ALPHA end.

    ``check`` calls ``gateway.is_accepted`` unchanged, which reads the
    accepted-artifact map and writes nothing, and returns the result as a bound
    ``GateResult``. It is the check ``Pipeline`` runs before a Gem does.
    """

    name = INPUT_GATE_NAME

    def __init__(
        self, gateway: ConservationGateway, *, subject: str = DEFAULT_INPUT_SUBJECT
    ) -> None:
        _cns_gate()  # fail here, at construction, not on first use
        _require_subject(subject)
        self._gateway = gateway
        self._subject = subject

    @property
    def position(self) -> Any:
        return _cns_gate().GatePosition.ALPHA

    def check(self, candidate: object) -> Any:
        if not isinstance(candidate, Artifact):
            raise TypeError(
                f"the input gate judges an Artifact; got {type(candidate).__name__}"
            )
        return input_to_cns_result(
            self._gateway.is_accepted(candidate), candidate, subject=self._subject
        )


class CnsOutputGate:
    """The gateway's ``submit`` as a ``cns.gate.Gate`` at the OMEGA end.

    ``check`` runs ``gateway.submit`` unchanged on a :class:`GatewaySubmission`
    and returns its decision as a bound ``GateResult``. Judging and promotion
    are one step in this repo, so ``check`` promotes an accepted candidate
    exactly as a direct ``submit`` does. The caller can then read it with
    ``gateway.resolve_artifact``.
    """

    name = OUTPUT_GATE_NAME

    def __init__(
        self, gateway: ConservationGateway, *, subject: str = DEFAULT_OUTPUT_SUBJECT
    ) -> None:
        _cns_gate()  # fail here, at construction, not on first use
        _require_subject(subject)
        self._gateway = gateway
        self._subject = subject

    @property
    def position(self) -> Any:
        return _cns_gate().GatePosition.OMEGA

    def check(self, candidate: object) -> Any:
        if not isinstance(candidate, GatewaySubmission):
            raise TypeError(
                f"the output gate judges a GatewaySubmission; got {type(candidate).__name__}"
            )
        result = self._gateway.submit(candidate.request, candidate.proposal)
        return to_cns_result(result, subject=self._subject)


def cns_chain(gateway: ConservationGateway) -> Any:
    """A ``cns.gate.GateChain`` with the input gate in ``alpha``, ``submit`` in ``omega``.

    ``complete()`` is ``True`` because both slots are filled by the gateway's
    two real ends, which ``Pipeline`` runs on one artifact (input gate before
    the Gem, ``submit`` after). Nothing here enforces that order or that both
    verdicts concern one request; that is the consumer's responsibility. The
    two gates take different candidates (an ``Artifact`` and a
    ``GatewaySubmission``). See the module docstring.
    """
    cns_gate = _cns_gate()
    return cns_gate.GateChain(
        alpha=(CnsInputGate(gateway),),
        omega=(CnsOutputGate(gateway),),
    )


def submit_to_cns(
    gateway: ConservationGateway,
    request: TransformationRequest,
    proposal: TransformationProposal,
    *,
    subject: str = DEFAULT_OUTPUT_SUBJECT,
) -> Any:
    """Run ``ConservationGateway.submit`` and return its decision as a CNS verdict.

    The gateway does exactly what it does for a direct ``submit``, including
    promoting an accepted candidate and recording a refusal in its ledger. CNS
    is checked first, so without it this raises ``CnsNotInstalled`` before the
    gateway is touched.
    """
    return CnsOutputGate(gateway, subject=subject).check(GatewaySubmission(request, proposal))
