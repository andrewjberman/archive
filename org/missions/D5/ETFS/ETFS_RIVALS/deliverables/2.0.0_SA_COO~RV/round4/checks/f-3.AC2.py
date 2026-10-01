"""RIV-f-3 AC2 (reopen, row ETFS_RIVALS-Z-W4-S8) -- the package suite does not depend on the committed floor values.

RIV-d-5 committed the measured per-source floors (issuer 0.23, bloomberg 0.99, home_producer 0.0; b366ed9d7e) and 19 page tests
went red (test_p1_page_and_guardrails 12, test_p2_page_grouped_by_fund 6, test_r3_repairs 1): their fixtures carry unresolved
lines and read the live config. A test that is not ABOUT the floor pins the floor it needs; a floor test sets its own.
The suite runs with RIVALFUNDS_GUARDRAILS_OVERRIDE holding exactly the committed values, so it grades the same bytes on CLOUD
before and after d-5's drain.
  - the whole rivalfunds suite reads 0 failed under the committed floors;
  - control: it reads 0 failed under the all-zero floors too (nothing passes only because a floor was raised)."""
import json
import os
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

COMMITTED = {"min_resolved_fraction": {"issuer": 0.23, "bloomberg": 0.99, "home_producer": 0.0}}
ZERO = {"min_resolved_fraction": {"issuer": 0.0, "bloomberg": 0.0, "home_producer": 0.0}}


def suite(override):
    scripts = pathlib.Path(__file__).resolve().parents[9] / "data" / "etfs" / "scripts"
    env = dict(os.environ, RIVALFUNDS_GUARDRAILS_OVERRIDE=json.dumps(override))
    p = subprocess.run([sys.executable, "-m", "pytest", "rivalfunds/tests", "-q", "-p", "no:cacheprovider", "--color=no"],
                       cwd=str(scripts), env=env, capture_output=True, text=True, timeout=900)
    tail = [ln for ln in p.stdout.splitlines() if re.search(r"\d+ (passed|failed)", ln)]
    line = tail[-1] if tail else p.stdout[-300:]
    m = re.search(r"(\d+) failed", line)
    return (int(m.group(1)) if m else 0), line, p.returncode


def run(v):
    c.setup_path()
    n, line, rc = suite(COMMITTED)
    print(f"committed floors: {line} (rc={rc})")
    v.check(n == 0 and rc == 0, "suite 0 failed under the committed floors")
    n0, line0, rc0 = suite(ZERO)
    print(f"zero floors: {line0} (rc={rc0})")
    v.check(n0 == 0 and rc0 == 0, "control: suite 0 failed under the zero floors")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
