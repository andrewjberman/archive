#!/usr/bin/env python3
"""MDPF_TAXSMA TX-a-1 probe: one acceptance criterion per invocation (TXA1-AC1 .. TXA1-AC10).

    cd <WS> && timeout 120 py -3.12 org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~2/probes/tx_a_1.py AC<n>

Each run prints its measurement with vintage (HEAD, UTC time, dirty state of the files under test) and
denominator, then exactly one line: `VERDICT: PASS-TXA1-AC<n>` or `VERDICT: FAIL-TXA1-AC<n> <reason>`.

Every criterion runs its own subset of data/mdpf/tests/taxsma/test_taxsma_aggregate.py -- the tests named
`test_ac<n>_*` -- in a fresh subprocess (never in-process, so a probe crash cannot look like a pass), and
PASS requires rc 0 AND at least one test collected (a 0-of-0 run is a vacuous pass and reads FAIL here).
AC6 and AC7 are the "(difference)" criteria: each one test asserts both arms (missing/declared;
overlap/no-overlap) inside one test body and prints what differed. No test in this suite reads a real
account, calls the Gateway, Microsoft Graph, SharePoint, the BD roster, b00 or a real S3/boto3 client --
synthetic dates/dollar fixtures only.
"""
from __future__ import annotations

import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
TEST_REL = "data/mdpf/tests/taxsma/test_taxsma_aggregate.py"
MODULE_REL = "data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py"
UNDER_TEST = [MODULE_REL, TEST_REL]
PER_AC_TIMEOUT = 100

# The pytest -k filter (a prefix on the test function name) that carries each criterion. "test_acN_" never
# collides with "test_acN0_".. within this suite's range (AC1..AC10 -- verified: no two-digit collision).
AC_FILTERS = {n: "test_ac%d_" % n for n in range(1, 11)}


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


def _vintage(repo: Path) -> str:
    rc, head, _ = _git(repo, "rev-parse", "--short=10", "HEAD")
    rc2, st, _ = _git(repo, "status", "--porcelain", "--", *UNDER_TEST)
    dirty = [ln.strip() for ln in st.splitlines() if ln.strip()]
    return "vintage: HEAD %s, %s UTC, files under test %d, dirty vs HEAD %d%s" % (
        head.strip() if rc == 0 else "UNREAD", _utc(), len(UNDER_TEST), len(dirty),
        (" (" + "; ".join(dirty) + ")") if dirty else "")


def _verdict(n: int, ok: bool, reason: str = "") -> int:
    if ok:
        print("VERDICT: PASS-TXA1-AC%d" % n, flush=True)
        return 0
    print("VERDICT: FAIL-TXA1-AC%d %s" % (n, reason or "unspecified"), flush=True)
    return 1


def _run_ac(repo: Path, n: int) -> int:
    filt = AC_FILTERS[n]
    cmd = [sys.executable, "-m", "pytest", TEST_REL, "-k", filt, "-v", "-p", "no:cacheprovider", "--color=no"]
    print(_vintage(repo))
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


def main() -> int:
    if len(sys.argv) != 2 or not re.fullmatch(r"AC(?:[1-9]|10)", sys.argv[1]):
        print("usage: tx_a_1.py AC1 .. AC10", file=sys.stderr)
        return 2
    n = int(sys.argv[1][2:])
    repo = _repo()
    return _run_ac(repo, n)


if __name__ == "__main__":
    sys.exit(main())
