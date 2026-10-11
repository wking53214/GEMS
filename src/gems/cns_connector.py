"""Optional connector to CNS (``cns.gate``) for the GEMS governance validator.

GEMS is independent. It has no CNS dependency, imports nothing from CNS when it
loads, and its whole suite passes with CNS absent. This module is the one place
in ``src/gems`` that knows CNS exists, and it asks for CNS only when one of its
functions is called. Without CNS installed those calls raise
:class:`CnsNotInstalled` with the install command; nothing else in GEMS is
affected. ``gems/__init__`` does not import this module.

What connecting means
---------------------
GEMS keeps its own verdict: :meth:`GovernanceValidator.validate_artifact`
returns ``None`` when an artifact's provenance is present and its epistemic
status is valid, and raises ``ValueError`` when it is not. CNS's shared gate
contract is ``cns.gate.GateResult`` (``gate``, ``position``, ``outcome``,
``reason``, ``subject``, ``subject_digest``). This module translates one into
the other without changing either, so a consumer that speaks CNS can resolve
GEMS's verdict alongside gates from other repositories.

The transport gateway under ``transport/`` is a separate, unreconciled package
with its own connector (``gems_transport.cns_connector``); this one covers only
``src/gems``.

The mapping, and why
--------------------
* **Position is ``OMEGA``, a judgment call that GEMS does not settle.** Nothing
  in ``src/gems`` calls the validator at all (only tests do), so the repo gives
  it no end. It judges the provenance record an artifact carries, which is a
  check on a result, and that is why it is placed at ``OMEGA``; an artifact
  handed to a Gem is equally something it could judge, so this is not the only
  reading. The connector does not claim a precondition end
  (``cns_chain(...).complete()`` is ``False`` by design), so the placement does
  not make a chain look complete.
* ``validate_artifact`` returns -> ``PASS``.
* ``validate_artifact`` raises ``ValueError`` -> ``TERMINAL_BREACH``. GEMS models
  no retry or repair: ``Artifact`` and ``Provenance`` are frozen, the validator
  reports one refusal and nothing resubmits. Nothing here invents a ``RETRY``.
* Any other exception (for example ``TypeError`` from an unhashable status) is
  not a verdict. It propagates unchanged and never becomes a ``PASS``.

Fail closed: ``PASS`` is produced only when the validator itself accepted, the
artifact also satisfies the GEMS governance rules the ``PASS`` reason names, and
the verdict could be bound to what it judged. A verdict whose content CNS cannot
digest is ``TERMINAL_BREACH``, unbound, with the reason saying so. A missing
verdict is not a ``PASS`` either: :func:`to_cns_result` has no default for
``refusal``, and when told the validator returned it re-checks the two
conditions on the artifact (a looser custom validator cannot make this
connector pass what the GEMS rules refuse).

What a ``PASS`` means
---------------------
Provenance is present, the epistemic status is a known value, and the artifact
does not come from a purely HUMAN origin while claiming ``HUMAN_AUTHORIZATION``. That is what
``GovernanceValidator`` checks. A ``PASS`` from this gate still does not prove
that a human authorized anything: it only shows the artifact did not claim
authority it cannot hold.

What a verdict is bound to
--------------------------
``subject`` is a label (default ``"artifact"``). ``subject_digest`` is
``cns.gate.subject_digest`` over the artifact's identity and its whole
provenance record::

    {"kind": "governed_artifact", "artifact_id": ..., "provenance": None | {
        "source_id", "origin", "epistemic_status", "authority",
        "parent_ids", "note"}}

``Artifact.content`` and ``Artifact.metadata`` are not judged by the validator
and are deliberately not bound: two artifacts that differ only in content share
a verdict and a digest. Enum members are reduced to their values first, because
CNS digests a ``str`` by formatting it and ``format()`` of a ``str`` enum
differs between Python 3.10 and 3.11+. The repo's own executor stamps plain
strings where the enums belong, and the validator accepts both, so both digest
alike.

Real inputs CNS cannot digest (a NaN ``note``, an object as ``source_id``) are
handled as above: the verdict is ``TERMINAL_BREACH`` and unbound, even when the
validator itself accepted the artifact.

Install with the extra: ``pip install 'gems-infrastructure[cns]'``.
"""

from __future__ import annotations

import importlib
from enum import Enum
from types import ModuleType
from typing import Any, Callable

from gems.contracts import Artifact
from gems.governance import GovernanceValidator

__all__ = [
    "CnsGovernanceGate",
    "CnsNotInstalled",
    "artifact_digest",
    "cns_available",
    "cns_chain",
    "to_cns_result",
    "validate_to_cns",
]

INSTALL_HINT = "pip install 'gems-infrastructure[cns]'"

#: The ``gate`` field of a verdict.
GATE_NAME = "governance"
#: What ``subject`` is set to when the caller does not name the judged content.
DEFAULT_SUBJECT = "artifact"


class CnsNotInstalled(ImportError):
    """Raised by this module's functions when ``cns`` cannot be imported."""


def _cns_gate() -> ModuleType:
    """Import ``cns.gate`` on demand, or say exactly what is missing."""
    try:
        return importlib.import_module("cns.gate")
    except ImportError as exc:
        raise CnsNotInstalled(
            "gems.cns_connector needs the CNS package (cns.gate), which is not "
            f"installed. Install it with: {INSTALL_HINT}. GEMS itself works "
            "without it."
        ) from exc


def cns_available() -> bool:
    """Whether the CNS gate contract can be imported in this environment."""
    try:
        _cns_gate()
    except CnsNotInstalled:
        return False
    return True


def _plain(value: Any) -> Any:
    """``value`` with enum members reduced to their values and tuples to lists."""
    if isinstance(value, Enum):
        return _plain(value.value)
    if isinstance(value, (tuple, list)):
        return [_plain(item) for item in value]
    return value


def _content(artifact: Artifact) -> dict[str, Any]:
    """The judged content: identity plus the whole provenance record."""
    provenance = artifact.provenance
    record = None
    if provenance is not None:
        record = {
            "source_id": _plain(provenance.source_id),
            "origin": _plain(provenance.origin),
            "epistemic_status": _plain(provenance.epistemic_status),
            "authority": _plain(provenance.authority),
            "parent_ids": _plain(provenance.parent_ids),
            "note": _plain(provenance.note),
        }
    return {
        "kind": "governed_artifact",
        "artifact_id": _plain(artifact.artifact_id),
        "provenance": record,
    }


def artifact_digest(artifact: Artifact) -> str:
    """The digest a bound verdict on ``artifact`` carries.

    Pass it, with the subject label, to ``GateResult.binds`` to check that a
    verdict was issued against exactly this artifact identity and provenance.
    Raises for an artifact CNS cannot digest (a verdict on one is unbound).
    """
    return _cns_gate().subject_digest(_content(artifact))


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


def _gems_refusal(artifact: Artifact) -> ValueError | None:
    """What the GEMS governance rules say about ``artifact``, as the validator says it.

    A ``TypeError`` from an unhashable status is not a verdict and propagates.
    """
    try:
        GovernanceValidator().validate_artifact(artifact)
    except ValueError as exc:
        return exc
    return None


def to_cns_result(
    artifact: Artifact,
    refusal: ValueError | None,
    *,
    subject: str = DEFAULT_SUBJECT,
) -> Any:
    """Translate the validator's verdict on ``artifact`` into a ``cns.gate.GateResult``.

    ``refusal`` is required: it is the ``ValueError`` ``validate_artifact``
    raised, or ``None`` to say it returned. Leaving it out is an error, never a
    ``PASS``. ``PASS`` exactly when there is no refusal, the GEMS governance
    rules agree that the artifact has provenance and a valid epistemic status
    (a ``None`` that the rules contradict is ``TERMINAL_BREACH``), and the
    verdict could be bound to the artifact; every other case is
    ``TERMINAL_BREACH``. The position is ``OMEGA``.
    """
    cns_gate = _cns_gate()
    _require_subject(subject)
    if not isinstance(artifact, Artifact):
        raise TypeError(
            f"the governance validator judges an Artifact; got {type(artifact).__name__}"
        )
    if refusal is not None and not isinstance(refusal, ValueError):
        raise TypeError(
            "refusal must be the ValueError validate_artifact raised, or None; "
            f"got {type(refusal).__name__}"
        )
    if refusal is None:
        contradiction = _gems_refusal(artifact)
        if contradiction is None:
            outcome = cns_gate.GateOutcome.PASS
            reason = "provenance present and epistemic status valid"
        else:
            outcome = cns_gate.GateOutcome.TERMINAL_BREACH
            reason = (
                "validate_artifact is reported to have returned, but the GEMS "
                f"governance rules refuse this artifact: {contradiction}"
            )
    else:
        outcome = cns_gate.GateOutcome.TERMINAL_BREACH
        reason = str(refusal) or "governance validation refused the artifact"
    digest, problem = _bind(cns_gate, lambda: _content(artifact))
    if not digest:
        outcome = cns_gate.GateOutcome.TERMINAL_BREACH
        reason = f"unbound, the judged content cannot be digested canonically ({problem}); {reason}"
    return cns_gate.GateResult(
        gate=GATE_NAME,
        position=cns_gate.GatePosition.OMEGA,
        outcome=outcome,
        reason=reason,
        subject=subject,
        subject_digest=digest,
    )


def validate_to_cns(
    artifact: Artifact,
    validator: GovernanceValidator | None = None,
    *,
    subject: str = DEFAULT_SUBJECT,
) -> Any:
    """Run ``GovernanceValidator.validate_artifact`` and return the verdict as a CNS verdict.

    Same validator, same verdict, same absence of side effects; only the
    representation differs. A ``ValueError`` is the validator's refusal and is
    translated. Any other exception is not a verdict and propagates unchanged.
    A custom ``validator`` may refuse more than GEMS does; it cannot make this
    return ``PASS`` for an artifact the GEMS rules refuse. CNS is checked
    first, so without it this raises ``CnsNotInstalled`` before the validator
    runs.
    """
    _cns_gate()
    _require_subject(subject)
    if not isinstance(artifact, Artifact):
        raise TypeError(
            f"the governance validator judges an Artifact; got {type(artifact).__name__}"
        )
    judge = validator if validator is not None else GovernanceValidator()
    try:
        judge.validate_artifact(artifact)
    except ValueError as exc:
        return to_cns_result(artifact, exc, subject=subject)
    return to_cns_result(artifact, None, subject=subject)


class CnsGovernanceGate:
    """GEMS's governance validator as a ``cns.gate.Gate`` at the OMEGA end.

    ``check`` runs the validator unchanged on an :class:`~gems.contracts.Artifact`
    and returns its verdict as a bound ``cns.gate.GateResult``.
    """

    name = GATE_NAME

    def __init__(
        self,
        validator: GovernanceValidator | None = None,
        *,
        subject: str = DEFAULT_SUBJECT,
    ) -> None:
        _cns_gate()  # fail here, at construction, not on first use
        _require_subject(subject)
        self._validator = validator if validator is not None else GovernanceValidator()
        self._subject = subject

    @property
    def position(self) -> Any:
        return _cns_gate().GatePosition.OMEGA

    def check(self, candidate: object) -> Any:
        if not isinstance(candidate, Artifact):
            raise TypeError(
                f"the governance gate judges an Artifact; got {type(candidate).__name__}"
            )
        return validate_to_cns(candidate, self._validator, subject=self._subject)


def cns_chain(
    validator: GovernanceValidator | None = None,
    *,
    subject: str = DEFAULT_SUBJECT,
) -> Any:
    """A ``cns.gate.GateChain`` holding the governance gate in ``omega``.

    ``alpha`` stays empty and ``complete()`` is ``False``: ``src/gems`` has no
    precondition end, and this connector does not invent one.
    """
    cns_gate = _cns_gate()
    return cns_gate.GateChain(omega=(CnsGovernanceGate(validator, subject=subject),))
