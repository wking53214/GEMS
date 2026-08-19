from gems.cognition import Triad42


def test_triad42_has_four_reviewers():
    findings = Triad42().review("proposal")
    assert [f.reviewer for f in findings] == [
        "Red / Assumption Breaker", "Gray / Grey", "Green", "42 / Deep Thought"
    ]
