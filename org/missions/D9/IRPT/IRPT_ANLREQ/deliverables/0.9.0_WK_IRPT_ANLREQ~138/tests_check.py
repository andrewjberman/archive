#!/usr/bin/env python3
"""AR330-y-AC1 (IRPT_ANLREQ.TO-AR-y-330): runs the new test file, then every test file in ycharts/research/tests whose
name contains commentary, packager, producer or layout. Prints TESTS-OK only when the new file passes cases (a) to (d)
with 0 failed and the other files have 0 failed; otherwise TESTS-BAD <why> and exit 1."""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[7]  # deliverables/<serial>/ -> deliverables -> IRPT_ANLREQ -> IRPT -> D9 -> missions -> org -> worktree
TESTS = ROOT / "infra" / "aws" / "lambda" / "investor-reporting" / "ycharts" / "research" / "tests"
NEW = "test_commentary_disclaimer_pending.py"
WORDS = ("commentary", "packager", "producer", "layout")
CASES = ("test_a_", "test_b_", "test_c_", "test_d_")
COUNT = re.compile(r"(\d+) (passed|failed|errors?|skipped|xfailed|xpassed)")
SUMMARY = re.compile(r"^=*\s*((?:\d+ \w+(?:, )?)+) in [\d.]+s", re.M)


def run(files):
    cmd = [sys.executable, "-m", "pytest", "-q", "-rA", "-p", "no:cacheprovider", "--color=no"] + files
    p = subprocess.run(cmd, cwd=str(TESTS), capture_output=True, text=True, timeout=300)
    out = p.stdout + p.stderr
    summaries = SUMMARY.findall(out)
    counts = {}
    if summaries:
        for n, kind in COUNT.findall(summaries[-1]):
            key = "error" if kind.startswith("error") else kind
            counts[key] = counts.get(key, 0) + int(n)
    return p.returncode, out, counts


def main():
    others = sorted(p.name for p in TESTS.glob("test_*.py") if p.name != NEW and any(w in p.name for w in WORDS))
    print("NEW-FILE: %s" % NEW)
    print("OTHER-FILES (%d): %s" % (len(others), ", ".join(others)))
    rc_new, out_new, c_new = run([NEW])
    print("NEW RUN rc=%d counts=%s" % (rc_new, c_new))
    passed_new = set(re.findall(r"^PASSED \S+::(\S+)", out_new, re.M))
    missing = [c for c in CASES if not any(name.startswith(c) for name in passed_new)]
    if rc_new != 0 or c_new.get("failed", 0) or c_new.get("error", 0):
        print("TESTS-BAD new file did not pass: rc=%d counts=%s" % (rc_new, c_new))
        return 1
    if missing:
        print("TESTS-BAD new file lacks a PASSED case for %s" % ", ".join(missing))
        return 1
    rc_o, out_o, c_o = run(others)
    print("OTHERS RUN rc=%d counts=%s" % (rc_o, c_o))
    n_others = c_o.get("passed", 0)
    failed_o = c_o.get("failed", 0) + c_o.get("error", 0)
    if rc_o != 0 or failed_o or n_others == 0:
        print("TESTS-BAD others: rc=%d failed+errors=%d passed=%d" % (rc_o, failed_o, n_others))
        return 1
    print("TESTS-OK %d new, %d others, 0 failed" % (c_new.get("passed", 0), n_others))
    return 0


if __name__ == "__main__":
    sys.exit(main())
