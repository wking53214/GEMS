from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from gems.contracts import Artifact


class VerificationStatus(str, Enum):
    VERIFIED = "verified"
    REJECTED = "rejected"
    NOT_VERIFIED = "not_verified"


@dataclass(frozen=True)
class VerifiedArtifactResult:
    """Result returned by an external artifact-integrity or lineage adapter."""

    source: Artifact
    output: Artifact | None
    status: VerificationStatus
    source_identity: str | None = None
    output_identity: str | None = None
    transformation_id: str | None = None
    transformation_version: str | None = None
    lineage_reference: str | None = None
    reason: str | None = None


class VerifiedArtifactAdapter(Protocol):
    """Boundary for external verification without duplicating its implementation."""

    def verify(self, artifact: Artifact) -> VerifiedArtifactResult:
        """Verify an artifact and return explicit external integrity state."""
        ...
