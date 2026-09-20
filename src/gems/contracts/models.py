from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping
from uuid import uuid4


class EpistemicStatus(str, Enum):
    """Epistemic status taxonomy for forensic artifact classification.

    EXPLICIT: User directly provided or declared this
    INFERRED: System derived this from other data
    UNKNOWN: Status cannot be determined
    CONFLICTED: Multiple conflicting sources of information

    Note: CONFLICTED is reserved for future use (currently only used in tests).
    """
    EXPLICIT = "explicit"
    INFERRED = "inferred"
    UNKNOWN = "unknown"
    CONFLICTED = "conflicted"


class Origin(str, Enum):
    """Origin taxonomy for forensic provenance tracking.

    HUMAN: Originated from human user
    AI: Originated from AI system
    JOINT: Originated from both human and AI collaboration
    UNCERTAIN: Origin cannot be determined

    Note: HUMAN and JOINT are reserved for potential future use (currently only used in tests).
    """
    HUMAN = "human"
    AI = "ai"
    JOINT = "joint"
    UNCERTAIN = "uncertain"


class Authority(str, Enum):
    """Authority level taxonomy for forensic decision tracking.

    OBSERVATION: Fact-level data (no decision authority)
    ANALYSIS: System analysis with supporting evidence
    PROPOSAL: Proposed solution pending human review
    HUMAN_AUTHORIZATION: Human-approved authorization level

    Note: PROPOSAL and HUMAN_AUTHORIZATION are reserved for potential future use
    (currently only used in tests). They represent higher authority levels in the
    forensic taxonomy but production code does not yet generate them.
    """
    OBSERVATION = "observation"
    ANALYSIS = "analysis"
    PROPOSAL = "proposal"
    HUMAN_AUTHORIZATION = "human_authorization"


class WorkflowStatus(str, Enum):
    """Workflow outcome status for forensic audit trail.

    COMPLETED: Workflow completed successfully
    FAILED: Workflow encountered an error or failed

    Note: FAILED is reserved for error tracking (currently only used in tests).
    Production code only creates COMPLETED status artifacts.
    """
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True)
class Provenance:
    source_id: str
    origin: Origin
    epistemic_status: EpistemicStatus
    authority: Authority = Authority.ANALYSIS
    parent_ids: tuple[str, ...] = ()
    note: str | None = None


@dataclass(frozen=True)
class Artifact:
    artifact_id: str = field(default_factory=lambda: str(uuid4()))
    kind: str = "artifact"
    content: Any = None
    provenance: Provenance | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Handoff:
    task_id: str = ""
    sender: str = ""
    recipient: str = ""
    artifacts: tuple[Artifact, ...] = ()


@dataclass(frozen=True)
class GemSpec:
    name: str
    purpose: str
    capabilities: tuple[str, ...]
