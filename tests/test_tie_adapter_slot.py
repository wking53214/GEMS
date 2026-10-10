"""The TIE adapter slot says what is true.

It used to say "TIE is MISSING: no GitHub repository, package, or runtime
adapter is available". TIE is a repository; the adapter is what is missing.
"""

import pytest

from gems_transport import TIEIntegrationMissing, require_tie_adapter


def test_requiring_an_adapter_still_fails_closed():
    with pytest.raises(TIEIntegrationMissing):
        require_tie_adapter()


def test_the_message_names_the_missing_adapter_not_a_missing_repository():
    with pytest.raises(TIEIntegrationMissing) as info:
        require_tie_adapter()
    text = str(info.value)
    assert "No TIE adapter" in text
    assert "github.com/wking53214/TIE" in text
    assert "TIE is MISSING" not in text and "no GitHub repository" not in text
