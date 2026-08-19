import pytest

from gems.core.registry import GemRegistry
from gems.core.router import Router
from gems.contracts import GemSpec


def test_router_selects_exact_capability():
    r = GemRegistry()
    r.register(GemSpec("Research Analyst", "research", ("research",)))
    assert Router(r).route("research").gem == "Research Analyst"


def test_router_rejects_unknown_capability():
    with pytest.raises(LookupError):
        Router(GemRegistry()).route("unknown")
