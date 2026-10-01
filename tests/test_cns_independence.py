"""GEMS is independent of CNS, and these tests hold whether or not CNS is
installed. Each subprocess test runs in a fresh interpreter in which ``cns`` is
blocked outright (``sys.modules['cns'] = None`` makes any import of it fail), so
the result does not depend on what the test environment happens to contain.

The transport package has the same guarantee and needs ``conservation_kernel``
to import at all, so its subprocess tests live in
``test_cns_transport_independence.py``. The static checks here cover both
packages without importing either.
"""

from __future__ import annotations

import ast
import subprocess
import sys
import textwrap
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = str(ROOT / "src")
PACKAGE_DIRS = (ROOT / "src" / "gems", ROOT / "transport" / "gems_transport")
CONNECTORS = (
    ROOT / "src" / "gems" / "cns_connector.py",
    ROOT / "transport" / "gems_transport" / "cns_connector.py",
)
PINNED_SHA = "3b465dbcc1a6a4ab6f1040f93d44483196abd737"

BLOCK = "import sys; sys.modules['cns'] = None; sys.modules['cns.gate'] = None\n"


def _run(code: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-c", BLOCK + textwrap.dedent(code)],
        capture_output=True,
        text=True,
        env={"PYTHONPATH": SRC, "PATH": ""},
        timeout=60,
    )


def _run_open(code: str) -> subprocess.CompletedProcess[str]:
    """Like ``_run`` but with ``cns`` NOT blocked, so a soft import that a
    block would swallow is visible. Where CNS is installed this is the real
    guard; where it is not, it still runs and is simply trivially true."""
    return subprocess.run(
        [sys.executable, "-c", textwrap.dedent(code)],
        capture_output=True,
        text=True,
        env={"PYTHONPATH": SRC, "PATH": ""},
        timeout=60,
    )


def test_gems_and_its_connector_import_with_cns_blocked():
    done = _run(
        """
        import sys
        import gems, gems.cns_connector
        live = [n for n, m in sys.modules.items()
                if (n == 'cns' or n.startswith('cns.')) and m is not None]
        assert live == [], live
        print('ok')
        """
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "ok"


def test_gems_still_judges_and_routes_with_cns_blocked():
    done = _run(
        """
        from gems import (Artifact, GemRegistry, GemSpec, GovernanceValidator,
                          WorkflowCoordinator)
        from gems.contracts import EpistemicStatus, Origin, Provenance

        validator = GovernanceValidator()
        try:
            validator.validate_artifact(Artifact(content='x'))
        except ValueError:
            pass
        else:
            raise SystemExit('a missing provenance was accepted')
        good = Artifact(content='x', provenance=Provenance(
            'src', Origin.HUMAN, EpistemicStatus.EXPLICIT))
        validator.validate_artifact(good)

        registry = GemRegistry()
        registry.register(GemSpec('a', 'p', ('cap',)))
        handoff = WorkflowCoordinator(registry).execute_capability('cap', good)
        assert handoff.recipient == 'a'
        print('ok')
        """
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "ok"


def test_connector_says_what_is_missing_when_cns_is_blocked():
    done = _run(
        """
        from gems import Artifact
        from gems.cns_connector import (CnsNotInstalled, artifact_digest,
                                        cns_available, cns_chain, to_cns_result,
                                        validate_to_cns)
        assert cns_available() is False
        a = Artifact(content='x')
        for call in (lambda: validate_to_cns(a), lambda: to_cns_result(a, None),
                     lambda: artifact_digest(a), cns_chain):
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
        from gems.cns_connector import CnsGovernanceGate, CnsNotInstalled
        try:
            CnsGovernanceGate()
        except CnsNotInstalled:
            print('ok')
        """
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "ok"


def test_cns_is_checked_before_the_validator_runs():
    done = _run(
        """
        from gems import Artifact
        from gems.cns_connector import CnsNotInstalled, validate_to_cns

        class Tripwire:
            def validate_artifact(self, artifact):
                raise SystemExit('the validator ran without cns')

        try:
            validate_to_cns(Artifact(content='x'), Tripwire())
        except CnsNotInstalled:
            print('ok')
        """
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "ok"


def test_importing_every_gems_module_loads_no_cns_even_when_cns_is_installed():
    """A soft import (``try: importlib.import_module('cns.gate')``) is swallowed
    by the blocked-cns tests above, so this one lets CNS be found. After every
    ``gems`` module is imported, including the connector, no ``cns`` module may
    be loaded; only a connector call may load it."""
    done = _run_open(
        """
        import importlib, pkgutil, sys
        import gems

        names = ['gems']
        for info in pkgutil.walk_packages(gems.__path__, 'gems.'):
            importlib.import_module(info.name)
            names.append(info.name)
        assert 'gems.cns_connector' in names, names
        live = sorted(n for n in sys.modules if n == 'cns' or n.startswith('cns.'))
        assert live == [], live

        # The probe above can see CNS: once a connector asks for it, it is there.
        from gems.cns_connector import cns_available
        if cns_available():
            assert 'cns.gate' in sys.modules
        print('ok')
        """
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "ok"


def _cns_imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found += [a.name for a in node.names if a.name.split(".")[0] == "cns"]
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and (node.module or "").split(".")[0] == "cns":
                found.append(node.module)
    return found


def test_no_module_of_either_package_imports_cns_by_statement():
    """CNS is reached only through importlib inside a function, never by an
    ``import`` statement, so nothing can pull it in at import time."""
    offenders = {}
    for package in PACKAGE_DIRS:
        for path in sorted(package.rglob("*.py")):
            names = _cns_imports(path)
            if names:
                offenders[str(path.relative_to(ROOT))] = names
    assert offenders == {}


#: Ways to load a module by name at run time, which no ``import`` statement shows.
_LOADERS = {"__import__", "import_module"}


def _reaches_cns_dynamically(source: str) -> list[str]:
    """What in ``source`` can load a module by name or names CNS as a string.

    The statement-form check cannot see ``importlib.import_module('cns.gate')``
    or ``__import__('cns')``, and a ``try/except`` around either makes a soft
    import that every blocked-cns test swallows. Outside the two connectors
    nothing may import ``importlib``, call a loader, or hold a string that is
    ``cns`` or starts ``cns.``.
    """
    found = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            found += [f"import {a.name}" for a in node.names if a.name.split(".")[0] == "importlib"]
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and (node.module or "").split(".")[0] == "importlib":
                found.append(f"from {node.module} import ...")
        elif isinstance(node, ast.Call):
            func = node.func
            name = func.id if isinstance(func, ast.Name) else getattr(func, "attr", None)
            if name in _LOADERS:
                found.append(f"call to {name}")
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            if node.value in _LOADERS or node.value == "cns" or node.value.startswith("cns."):
                found.append(f"string {node.value!r}")
    return found


def test_no_module_outside_the_connectors_loads_by_name_or_names_cns():
    offenders = {}
    for package in PACKAGE_DIRS:
        for path in sorted(package.rglob("*.py")):
            if path in CONNECTORS:
                continue
            found = _reaches_cns_dynamically(path.read_text(encoding="utf-8"))
            if found:
                offenders[str(path.relative_to(ROOT))] = found
    assert offenders == {}


def test_the_dynamic_import_check_flags_the_soft_imports_it_exists_to_catch():
    soft = (
        "try:\n    __import__('cns.gate')\nexcept ImportError:\n    pass\n",
        "import importlib\ntry:\n    importlib.import_module('cns.gate')\nexcept ImportError:\n    pass\n",
        "from importlib import import_module as load\nload('c' + 'ns')\n",
        "def late():\n    return __import__('cns')\n",
        "x = getattr(__builtins__, '__import__')\n",
        "NAME = 'cns.gate'\n",
    )
    for source in soft:
        assert _reaches_cns_dynamically(source), source
    assert _reaches_cns_dynamically("import json\nlabel = 'cnsx'\nj = json.dumps({})\n") == []


def test_the_connectors_reach_cns_only_inside_a_function():
    for path in CONNECTORS:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        inside_function = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                inside_function.update(id(child) for child in ast.walk(node))
        calls = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and getattr(node.func, "attr", None) == "import_module"
        ]
        assert calls, f"{path.name} no longer loads CNS through importlib"
        assert all(id(node) in inside_function for node in calls), path.name
        # Exactly one load, of exactly the one module the connector needs, and
        # no other way to load anything by name.
        assert [[arg.value for arg in call.args] for call in calls] == [["cns.gate"]], path.name
        assert not [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "__import__"
        ], path.name
        named = {
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and (node.value == "cns" or node.value.startswith("cns."))
        }
        assert named == {"cns.gate"}, (path.name, named)


def test_neither_package_init_loads_its_connector():
    for init in (
        ROOT / "src" / "gems" / "__init__.py",
        ROOT / "transport" / "gems_transport" / "__init__.py",
    ):
        assert "cns_connector" not in init.read_text(encoding="utf-8"), init


def test_the_package_declares_no_cns_runtime_dependency():
    data = tomllib.loads((ROOT / "pyproject.toml").read_text())
    runtime = data["project"]["dependencies"]
    assert not any(dep.lower().replace("_", "-").startswith("cns") for dep in runtime)
    extra = data["project"]["optional-dependencies"]["cns"]
    assert len(extra) == 1
    assert extra[0].startswith("cns @ git+https://github.com/wking53214/cns.git@")
    assert extra[0].endswith(PINNED_SHA)
