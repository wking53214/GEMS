"""Opt-in gate: with GEMS_REQUIRE_TRANSPORT=1, a skipped test fails the run.

The transport tests need conservation_kernel, TIE and CNS, and each skips
itself when one is missing (``pytest.importorskip``). A skip reports success
and verifies nothing, so CI sets GEMS_REQUIRE_TRANSPORT=1 after installing all
three, and any skip, at collection or at run time, then fails the run. Without
the variable nothing changes: a bare checkout still skips as before.
"""

import os

_REQUIRE = os.environ.get("GEMS_REQUIRE_TRANSPORT") == "1"
_SKIPPED = []


def _record(report):
    if report.skipped and not hasattr(report, "wasxfail"):
        _SKIPPED.append(report.nodeid)


def pytest_runtest_logreport(report):
    if _REQUIRE:
        _record(report)


def pytest_collectreport(report):
    if _REQUIRE:
        _record(report)


def pytest_terminal_summary(terminalreporter):
    if _SKIPPED:
        terminalreporter.section("GEMS_REQUIRE_TRANSPORT=1: skips are failures", red=True)
        for nodeid in _SKIPPED:
            terminalreporter.line(f"  SKIPPED  {nodeid}")


def pytest_sessionfinish(session, exitstatus):
    if _SKIPPED and exitstatus == 0:
        session.exitstatus = 1
