from __future__ import annotations

from dataclasses import dataclass

from gems.core.registry import GemRegistry


@dataclass(frozen=True)
class Route:
    gem: str
    capability: str
    reason: str


class Router:
    """Deterministic capability router; scoring policy is intentionally minimal."""

    def __init__(self, registry: GemRegistry) -> None:
        self.registry = registry

    def route(self, capability: str) -> Route:
        matches = [g for g in self.registry.list() if capability in g.capabilities]
        if not matches:
            raise LookupError(f"No Gem advertises capability: {capability}")
        matches.sort(key=lambda g: g.name)
        selected = matches[0]
        return Route(selected.name, capability, "exact capability match")
