from r2_principal_sets import compare


def test_equal_sets_report_equal():
    r = compare(["a", "b"], ["b", "a"])
    assert r["equal"] is True
    assert r["only_scan_n"] == 0
    assert r["only_history_n"] == 0
    assert r["vacuous"] is False


def test_principal_only_in_scan_fails():
    r = compare(["a", "b"], ["a"])
    assert r["equal"] is False
    assert r["only_scan_n"] == 1


def test_principal_only_in_history_fails():
    r = compare(["a"], ["a", "b"])
    assert r["equal"] is False
    assert r["only_history_n"] == 1


def test_two_empty_sets_are_not_evidence():
    r = compare([], [])
    assert r["equal"] is False
    assert r["vacuous"] is True
