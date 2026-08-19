from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping
from uuid import uuid4


class EpistemicStatus(str, Enum):
    EXPLICIT = "explicit"
    INFERRED = "inferred"
    UNKNOWN = "unknown"
    CONFLICTED = "conflicted"


class Origin(str, Enum):
    HUMAN = "human"
    AI = "ai"
    JOINT = "joint"
    UNCERTAIN = "uncertain"


class Authority(str, Enum):
    OBSERVATION = "observation"
    ANALYSIS = "analysis"
    PROPOSAL = "proposal"
    HUMAN_AUTHORIZATION = "human_authorization"


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
    handoff_id: str = field(default_factory=lambda: str(uuid4()))
    task_id: str = ""
    sender: str = ""
    recipient: str = ""
    artifacts: tuple[Artifact, ...] = ()
    routing_signal: str | None = None
    workflow_state: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GemSpec:
    name: str
    purpose: str
    capabilities: tuple[str, ...]
    status: str = "conceptual"
    authority: tuple[Authority, ...] = (Authority.ANALYSIS, Authority.PROPOSAL)
    provenance: Provenance | None = None
    implementation_status: str = "reconstructed-baseline"
