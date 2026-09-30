"""The transport package is independent of CNS, and these tests hold whether or
not CNS is installed. Each one runs in a fresh interpreter in which ``cns`` is
blocked outright (``sys.modules['cns'] = None`` makes any import of it fail).

``gems_transport`` imports ``conservation_kernel`` (a declared dependency of
this project) whenever it is imported, so these tests need it. They are skipped
only when *that* is missing, as the transport itself is unusable then; they
never skip because CNS is absent or present. The static guarantees that need no
kernel are in ``test_cns_independence.py``.
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

conservation_kernel = pytest.importorskip(
    "conservation_kernel",
    reason="gems_transport needs conservation_kernel (its own dependency, not CNS)",
)

ROOT = Path(__file__).resolve().parents[1]
KERNEL_PARENT = str(Path(conservation_kernel.__file__).resolve().parents[1])
PYTHONPATH = ":".join([str(ROOT / "src"), str(ROOT / "transport"), KERNEL_PARENT])

BLOCK = "import sys; sys.modules['cns'] = None; sys.modules['cns.gate'] = None\n"


def _run(code: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-c", BLOCK + textwrap.dedent(code)],
        capture_output=True,
        text=True,
        env={"PYTHONPATH": PYTHONPATH, "PATH": ""},
        timeout=120,
    )


def _run_open(code: str) -> subprocess.CompletedProcess[str]:
    """Like ``_run`` but with ``cns`` NOT blocked, so a soft import that a
    block would swallow is visible. Where CNS is installed this is the real
    guard; where it is not, it still runs and is simply trivially true."""
    return subprocess.run(
        [sys.executable, "-c", textwrap.dedent(code)],
        capture_output=True,
        text=True,
        env={"PYTHONPATH": PYTHONPATH, "PATH": ""},
        timeout=120,
    )


def test_importing_every_transport_module_loads_no_cns_even_when_cns_is_installed():
    """A soft import (``try: importlib.import_module('cns.gate')``) is swallowed
    by the blocked-cns tests, so this one lets CNS be found. After every
    ``gems_transport`` module and the experiment modules are imported,
    including the connector, no ``cns`` module may be loaded; only a connector
    call may load it."""
    done = _run_open(
        """
        import importlib, pkgutil, sys
        import gems_transport

        names = ['gems_transport']
        for info in pkgutil.walk_packages(gems_transport.__path__, 'gems_transport.'):
            importlib.import_module(info.name)
            names.append(info.name)
        assert 'gems_transport.cns_connector' in names, names
        import experiments.attacks, experiments.corpus
        live = sorted(n for n in sys.modules if n == 'cns' or n.startswith('cns.'))
        assert live == [], live

        # The probe above can see CNS: once a connector asks for it, it is there.
        from gems_transport.cns_connector import cns_available
        if cns_available():
            assert 'cns.gate' in sys.modules
        print('ok')
        """
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "ok"


def test_transport_and_its_connector_import_with_cns_blocked():
    done = _run(
        """
        import sys
        import gems_transport, gems_transport.cns_connector
        live = [n for n, m in sys.modules.items()
                if (n == 'cns' or n.startswith('cns.')) and m is not None]
        assert live == [], live
        print('ok')
        """
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "ok"


def test_the_gateway_still_judges_with_cns_blocked():
    done = _run(
        """
        from gems_transport import ConservationGateway, Pipeline
        from gems_transport.reference_gems import SummarizerGem
        from experiments.attacks import run_hostile_corpus
        from experiments.corpus import fixed_clock, synthetic_tie_source

        fixture = synthetic_tie_source()
        gateway = ConservationGateway(registry=fixture.registry)
        run = Pipeline(gateway).run(fixture.artifact, [SummarizerGem(clock=fixed_clock)])
        assert run.accepted
        outcomes = run_hostile_corpus()
        assert len(outcomes) == 20
        assert not any(item.accepted for item in outcomes)
        print('ok')
        """
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "ok"


def test_connector_says_what_is_missing_when_cns_is_blocked():
    done = _run(
        """
        from gems_transport import ConservationGateway
        from gems_transport.cns_connector import (CnsNotInstalled, cns_available,
                                                  cns_chain, input_digest,
                                                  input_to_cns_result, submit_to_cns,
                                                  to_cns_result, transformation_digest)
        from experiments.corpus import synthetic_tie_source

        assert cns_available() is False
        fixture = synthetic_tie_source()
        gateway = ConservationGateway(registry=fixture.registry)
        calls = (
            lambda: cns_chain(gateway),
            lambda: input_digest(fixture.artifact),
            lambda: input_to_cns_result(True, fixture.artifact),
            lambda: to_cns_result(None),
            lambda: transformation_digest(None),
            lambda: submit_to_cns(gateway, None, None),
        )
        for call in calls:
            try:
                call()
            except CnsNotInstalled as exc:
                assert "pip install 'gems-infrastructure[cns]'" in str(exc)
                assert isinstance(exc, ImportError)
            else:
                raise SystemExit('a connector call worked without cns')
        print('ok')
        """
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "ok"


def test_constructing_a_cns_gate_fails_at_construction_not_first_use():
    done = _run(
        """
        from gems_transport import ConservationGateway
        from gems_transport.cns_connector import CnsInputGate, CnsNotInstalled, CnsOutputGate
        gateway = ConservationGateway()
        for build in (CnsInputGate, CnsOutputGate):
            try:
                build(gateway)
            except CnsNotInstalled:
                pass
            else:
                raise SystemExit('built a gate without cns')
        print('ok')
        """
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "ok"


def test_cns_is_checked_before_the_gateway_is_touched():
    """``submit_to_cns`` must not submit anything when CNS is missing."""
    done = _run(
        """
        from gems_transport import ConservationGateway
        from gems_transport.cns_connector import CnsNotInstalled, submit_to_cns
        from gems_transport.reference_gems import SummarizerGem
        from experiments.corpus import fixed_clock, synthetic_tie_source

        fixture = synthetic_tie_source()
        gateway = ConservationGateway(registry=fixture.registry)
        gateway.ingest_source(fixture.artifact)
        gem = SummarizerGem(clock=fixed_clock)
        gateway.register_gem(gem.identity)
        request = gem.make_request(fixture.artifact)
        proposal = gem.transform(request)
        before = (len(gateway.accepted_artifacts()), len(gateway.ledger.entries()))
        try:
            submit_to_cns(gateway, request, proposal)
        except CnsNotInstalled:
            pass
        else:
            raise SystemExit('submitted without cns')
        after = (len(gateway.accepted_artifacts()), len(gateway.ledger.entries()))
        assert before == after, (before, after)
        print('ok')
        """
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "ok"
