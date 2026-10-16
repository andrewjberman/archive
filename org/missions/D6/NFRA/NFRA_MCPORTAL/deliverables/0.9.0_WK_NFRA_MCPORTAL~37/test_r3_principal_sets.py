import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from r3_principal_sets import compare  # noqa: E402

SCRIPT = os.path.join(HERE, "r3_principal_sets.py")


def test_equal_sets_report_equal():
    r = compare(["a", "b"], ["b", "a"])
    assert r["equal"] is True
    assert r["only_page_n"] == 0
    assert r["only_raw_n"] == 0
    assert r["vacuous"] is False


def test_principal_only_in_raw_means_the_page_misses_it():
    r = compare(["a"], ["a", "b"])
    assert r["equal"] is False
    assert r["only_raw_n"] == 1


def test_principal_only_in_page_is_reported():
    r = compare(["a", "b"], ["a"])
    assert r["equal"] is False
    assert r["only_page_n"] == 1


def test_two_empty_sets_are_not_evidence():
    r = compare([], [])
    assert r["equal"] is False
    assert r["vacuous"] is True


def test_scan_denied_stops_without_a_run(tmp_path):
    read = tmp_path / "read.txt"
    read.write_text(
        "SIM identity=Andrew_Berman table_arn_ok=yes Scan=implicitDeny "
        "DescribeTable=allowed OperatorRoleScan=implicitDeny\n"
        "RESULT: STOP\n",
        encoding="utf-8",
    )
    out = tmp_path / "r3_run.json"
    proc = subprocess.run(
        [sys.executable, SCRIPT, "--from-read", str(read), "--out", str(out)],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 3
    assert not out.exists()
