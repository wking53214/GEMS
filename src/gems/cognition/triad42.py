from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Challenge:
    reviewer: str
    findings: tuple[str, ...]


class Red:
    name = "Red / Assumption Breaker"

    def review(self, proposal: str) -> Challenge:
        return Challenge(self.name, ("Check hidden assumptions", "Check authority overreach", "Check unsupported verification claims"))


class Gray:
    name = "Gray / Grey"

    def review(self, proposal: str) -> Challenge:
        return Challenge(self.name, ("Check structure", "Check abstraction", "Check pattern consistency"))


class Green:
    name = "Green"

    def review(self, proposal: str) -> Challenge:
        return Challenge(self.name, ("Check natural-world/ecological parallels",))


class DeepThought42:
    name = "42 / Deep Thought"

    def review(self, proposal: str) -> Challenge:
        return Challenge(self.name, ("Generate a compass idea without treating it as evidence",))


class Triad42:
    def __init__(self) -> None:
        self.reviewers = (Red(), Gray(), Green(), DeepThought42())

    def review(self, proposal: str) -> tuple[Challenge, ...]:
        return tuple(r.review(proposal) for r in self.reviewers)
