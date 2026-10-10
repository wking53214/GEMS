"""The TIE adapter slot says what is true.

It used to say "TIE is MISSING: no GitHub repository, package, or runtime
adapter is available". TIE is a repository, and the source adapter now exists as
TIEPackageSource; the older require_tie_adapter slot still raises and says so.

The wording is checked from the source text, so it holds in an environment
without conservation_kernel (CI installs only pytest). The behavioral check
needs the kernel, like the other transport tests, and skips without it.
"""

import sys
from pathlib import Path

import pytest

TRANSPORT = Path(__file__).resolve().parents[1] / "transport"
SOURCE = (TRANSPORT / "gems_transport" / "tie_adapter.py").read_text()


def test_the_wording_names_the_missing_adapter_not_a_missing_repository():
    assert "No TIE adapter is configured" in SOURCE
    assert "TIEPackageSource" in SOURCE
    assert "github.com/wking53214/TIE" in SOURCE
    assert "TIE is MISSING" not in SOURCE
    assert "no GitHub repository" not in SOURCE


def test_the_readmes_no_longer_say_tie_is_absent():
    root = TRANSPORT.parent
    for name in ("README.md", "transport/README.md"):
        text = (root / name).read_text()
        assert "TIE is its own repo" in text and "TIE is MISSING" not in text, name
        assert "TIEPackageSource" in text, name


def test_requiring_an_adapter_still_fails_closed_with_that_message():
    pytest.importorskip(
        "conservation_kernel",
        reason="gems_transport needs conservation_kernel (its own dependency)",
    )
    sys.path.insert(0, str(TRANSPORT))
    from gems_transport import TIEIntegrationMissing, require_tie_adapter

    with pytest.raises(TIEIntegrationMissing) as info:
        require_tie_adapter()
    assert "No TIE adapter" in str(info.value)
    assert "TIEPackageSource" in str(info.value)
