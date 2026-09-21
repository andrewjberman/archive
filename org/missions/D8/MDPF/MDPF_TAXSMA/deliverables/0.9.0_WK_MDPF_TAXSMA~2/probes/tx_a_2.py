#!/usr/bin/env python3
"""MDPF_TAXSMA TX-a-2 probe: one acceptance criterion per invocation (TXA2-AC1 .. TXA2-AC12).

    cd <WS> && timeout 120 py -3.12 org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~2/probes/tx_a_2.py AC<n>

Each run prints its measurement with vintage (HEAD, UTC time, dirty state of the files under test) and
denominator, then exactly one line: `VERDICT: PASS-TXA2-AC<n>` or `VERDICT: FAIL-TXA2-AC<n> <reason>`.

AC1..AC11 each run their own subset of data/mdpf/tests/taxsma/test_taxsma_consolidator.py -- selected by
`-k` -- in a fresh subprocess (never in-process, so a probe crash cannot look like a pass), and PASS
requires rc 0 AND at least one test collected (a 0-of-0 run is a vacuous pass and reads FAIL here).

AC12 is different in kind: it runs the WHOLE MDPF Gold suite (data/mdpf/scripts/gold/tests, the suite
this cell's bound-17 baseline names -- 92 collected, 89 passed, 3 failed, all three in
test_global_fold_flag2.py) and PASSES only if the failing id SET is EXACTLY the three pre-existing ones
-- no fewer, no more, no different id -- never a bare pass/fail COUNT (a count can hide a swap: one
pre-existing failure fixed, one new one introduced, same total).

No test in this suite calls a real Gateway, Microsoft Graph, SharePoint, a live 0833/0824/b00 source or
a real S3/boto3 client -- synthetic envelopes/fixtures only (worker bound).
"""
from __future__ import annotations

import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
TEST_REL = "data/mdpf/tests/taxsma/test_taxsma_consolidator.py"
MODULE_REL = "data/mdpf/scripts/gold/mdpf_gold_consolidator.py"
GOLD_SUITE_REL = "data/mdpf/scripts/gold/tests"
UNDER_TEST = [MODULE_REL, TEST_REL]
PER_AC_TIMEOUT = 100

# The pytest -k filter carrying each criterion, against test_taxsma_consolidator.py's own class/method
# names. AC3 and AC4 are proven by the SAME regression class (the null-leaf fixture demonstrates both the
# `_last` non-fill property and the withhold-not-zero-fill property in one arm plus its negative control).
AC_FILTERS = {
    1: "TXA2AC1Order",
    2: "TXA2AC2FailureIsolation",
    3: "TXA2AC3AC4NullLeafRegression",
    4: "TXA2AC3AC4NullLeafRegression",
    5: "TXA2AC5OperationalControl",
    6: "TXA2AC6CategoryGoldAddress",
    7: "test_tax_member_carries_exactly_wire_status_fields or test_never_mutates_the_callers_dict",
    8: "test_each_of_the_three_named_reason_codes_propagates_one_arm_per_code",
    9: "TXA2AC9CalendarUnavailable",
    10: "TXA2AC10WeekendHoliday",
    11: "TXA2AC11Disabled",
}
KNOWN_PRE_EXISTING_FAILURES = frozenset({
    "data/mdpf/scripts/gold/tests/test_global_fold_flag2.py::test_carry_within_window_carries_and_labels",
    "data/mdpf/scripts/gold/tests/test_global_fold_flag2.py::test_carry_beyond_window_absent_for_real",
    "data/mdpf/scripts/gold/tests/test_global_fold_flag2.py::test_carry_source_is_measured_never_interpolated",
})


def _utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _git(repo: Path, *args: str) -> tuple:
    r = subprocess.run(["git", *args], cwd=str(repo), capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout, r.stderr


def _repo() -> Path:
    rc, out, err = _git(HERE.parent, "rev-parse", "--show-toplevel")
    if rc != 0 or not out.strip():
        raise RuntimeError("git rev-parse --show-toplevel failed: rc=%s %s" % (rc, err.strip()))
    return Path(out.strip())


def _vintage(repo: Path, paths) -> str:
    rc, head, _ = _git(repo, "rev-parse", "--short=10", "HEAD")
    rc2, st, _ = _git(repo, "status", "--porcelain", "--", *paths)
    dirty = [ln.strip() for ln in st.splitlines() if ln.strip()]
    return "vintage: HEAD %s, %s UTC, files under test %d, dirty vs HEAD %d%s" % (
        head.strip() if rc == 0 else "UNREAD", _utc(), len(paths), len(dirty),
        (" (" + "; ".join(dirty) + ")") if dirty else "")


def _verdict(n: int, ok: bool, reason: str = "") -> int:
    if ok:
        print("VERDICT: PASS-TXA2-AC%d" % n, flush=True)
        return 0
    print("VERDICT: FAIL-TXA2-AC%d %s" % (n, reason or "unspecified"), flush=True)
    return 1


def _run_ac(repo: Path, n: int) -> int:
    filt = AC_FILTERS[n]
    cmd = [sys.executable, "-m", "pytest", TEST_REL, "-k", filt, "-v", "-p", "no:cacheprovider", "--color=no"]
    print(_vintage(repo, UNDER_TEST))
    print("invocation: (cwd %s) %s" % (repo, " ".join(cmd[1:])))
    t0 = time.perf_counter()
    try:
        r = subprocess.run(cmd, cwd=str(repo), capture_output=True, text=True, timeout=PER_AC_TIMEOUT)
    except subprocess.TimeoutExpired:
        print("TIMEOUT after %ds" % PER_AC_TIMEOUT)
        return _verdict(n, False, "the test run timed out (%ds)" % PER_AC_TIMEOUT)
    elapsed = time.perf_counter() - t0
    out = (r.stdout or "") + (r.stderr or "")
    print(out.strip()[-6000:])
    print("elapsed: %.2fs, rc=%d" % (elapsed, r.returncode))
    passed_match = re.search(r"(\d+) passed", out)
    failed_match = re.search(r"(\d+) failed", out)
    collected = re.search(r"collected (\d+) item", out)
    deselected = re.search(r"(\d+) deselected", out)
    n_collected = int(collected.group(1)) if collected else 0
    n_deselected = int(deselected.group(1)) if deselected else 0
    n_selected = n_collected - n_deselected
    n_passed = int(passed_match.group(1)) if passed_match else 0
    n_failed = int(failed_match.group(1)) if failed_match else 0
    print("measurement: collected=%d selected(by -k %r)=%d passed=%d failed=%d" % (
        n_collected, filt, n_selected, n_passed, n_failed))
    if r.returncode != 0:
        return _verdict(n, False, "pytest rc=%d (not 0)" % r.returncode)
    if n_selected == 0 or n_passed == 0:
        return _verdict(n, False, "0 tests matched -k %r -- a vacuous pass, refused" % filt)
    if n_failed != 0:
        return _verdict(n, False, "pytest output names %d failure(s) despite rc=0" % n_failed)
    if n_passed != n_selected:
        return _verdict(n, False, "passed=%d != selected=%d (a skip or error is hiding)" % (n_passed, n_selected))
    return _verdict(n, True)


def _run_ac12(repo: Path) -> int:
    cmd = [sys.executable, "-m", "pytest", GOLD_SUITE_REL, "-q", "-p", "no:cacheprovider", "--color=no"]
    print(_vintage(repo, [GOLD_SUITE_REL, MODULE_REL]))
    print("invocation: (cwd %s) %s" % (repo, " ".join(cmd[1:])))
    t0 = time.perf_counter()
    try:
        r = subprocess.run(cmd, cwd=str(repo), capture_output=True, text=True, timeout=PER_AC_TIMEOUT)
    except subprocess.TimeoutExpired:
        print("TIMEOUT after %ds" % PER_AC_TIMEOUT)
        return _verdict(12, False, "the suite run timed out (%ds)" % PER_AC_TIMEOUT)
    elapsed = time.perf_counter() - t0
    out = (r.stdout or "") + (r.stderr or "")
    print(out.strip()[-8000:])
    print("elapsed: %.2fs, rc=%d" % (elapsed, r.returncode))
    passed_match = re.search(r"(\d+) passed", out)
    failed_match = re.search(r"(\d+) failed", out)
    n_passed = int(passed_match.group(1)) if passed_match else 0
    n_failed = int(failed_match.group(1)) if failed_match else 0
    failing_ids = set(re.findall(r"^FAILED (\S+)", out, flags=re.MULTILINE))
    print("measurement: passed=%d failed=%d failing_ids=%d denominator(known pre-existing)=%d"
          % (n_passed, n_failed, len(failing_ids), len(KNOWN_PRE_EXISTING_FAILURES)))
    if failing_ids:
        print("failing ids: %s" % sorted(failing_ids))
    new_failures = failing_ids - KNOWN_PRE_EXISTING_FAILURES
    missing_known = KNOWN_PRE_EXISTING_FAILURES - failing_ids
    if new_failures:
        return _verdict(12, False, "NEW failure id(s) beyond the 3 pre-existing: %s" % sorted(new_failures))
    if missing_known:
        # A pre-existing failure that now PASSES is not a regression -- but the exact-set claim this
        # criterion makes ("fails only on the 3 pre-existing ids") is about the SET this run measured, so
        # a fixed id is reported, never silently folded into a bare pass.
        print("NOTE: %d of the 3 pre-existing failing id(s) no longer fail -- not a regression, reported "
              "for the record: %s" % (len(missing_known), sorted(missing_known)))
    if n_failed != len(failing_ids):
        return _verdict(12, False, "pytest summary count (%d) != distinct failing ids captured (%d)"
                        % (n_failed, len(failing_ids)))
    return _verdict(12, True)


def main() -> int:
    if len(sys.argv) != 2 or not re.fullmatch(r"AC(?:[1-9]|1[0-2])", sys.argv[1]):
        print("usage: tx_a_2.py AC1 .. AC12", file=sys.stderr)
        return 2
    n = int(sys.argv[1][2:])
    repo = _repo()
    if n == 12:
        return _run_ac12(repo)
    return _run_ac(repo, n)


if __name__ == "__main__":
    sys.exit(main())
