from __future__ import annotations

from gems.contracts import GemSpec


class GemRegistry:
    """In-memory reconstruction of the referenced Gem catalog concept."""

    def __init__(self) -> None:
        self._gems: dict[str, GemSpec] = {}

    def register(self, spec: GemSpec) -> None:
        if spec.name in self._gems:
            raise ValueError(f"Gem already registered: {spec.name}")
        self._gems[spec.name] = spec

    def get(self, name: str) -> GemSpec:
        return self._gems[name]

    def list(self) -> tuple[GemSpec, ...]:
        return tuple(self._gems.values())
