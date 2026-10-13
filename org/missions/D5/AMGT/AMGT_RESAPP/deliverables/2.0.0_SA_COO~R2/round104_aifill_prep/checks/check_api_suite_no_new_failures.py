"""check_api_suite_no_new_failures.py -- the lib/research/api suite has no failure the base did not already have.

  PYTHONPATH=<repo root> python check_api_suite_no_new_failures.py
The base carries 4 failing tests (date-dependent feed and coverage tests, recorded in baseline_api_failures.txt). A cell that touches
scoped_amgt.py must not add one. Prints `AIFILL API SUITE: YES (base F failing, now G failing, new 0, passed P)` or `NO (...)`.
Bounded: the suite runs in about a minute.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASELINE = os.path.join(os.path.dirname(HERE), "baseline_api_failures.txt")


def main():
    with open(BASELINE, "r", encoding="utf-8") as handle:
        base = {ln.strip() for ln in handle if ln.strip().startswith("FAILED ")}
    proc = subprocess.run([sys.executable, "-m", "pytest", "lib/research/api/tests", "-q", "-p", "no:cacheprovider", "--color=no", "-rf"],
                          capture_output=True, text=True, timeout=500)
    now = {re.sub(r" - .*$", "", ln.strip()) for ln in proc.stdout.splitlines() if ln.startswith("FAILED ")}
    passed = re.findall(r"(\d+) passed", proc.stdout)
    new = sorted(now - base)
    ok = bool(passed) and not new and "error" not in proc.stdout.splitlines()[-1].lower()
    print("AIFILL API SUITE: %s (base %d failing, now %d failing, new %d, passed %s)" % ("YES" if ok else "NO", len(base), len(now), len(new), passed[-1] if passed else "?"))
    for name in new:
        print("NEW FAILURE: " + name)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
