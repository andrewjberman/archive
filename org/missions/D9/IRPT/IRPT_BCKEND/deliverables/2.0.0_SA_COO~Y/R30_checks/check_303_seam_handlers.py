#!/usr/bin/env python3
"""IB-yr-303 AC3 -- the paired seam suite reaches a handler for every consumer operation (row IRPT_BCKEND-W91-S2).

CTO analysis ROUND_ANALYSIS.sweep5.md section 2 item 5: "A pass count is not a handler count." This check reads
the suite's own PRINTS, never its pass count. It runs
  python -m pytest -s -q -p no:cacheprovider --color=no _contracts/tests/test_seam_paired.py
from infra/aws/lambda/investor-reporting (bounded at 100 s) and reads two things off the output:
  (a) the number of lines carrying ROUTE_NO_HANDLER            -> must be 0
  (b) the operation table: one line per consumer operation, `<operation>  <OUTCOME>  <detail>` with OUTCOME one
      of the suite's own four values; an operation REACHED A HANDLER when its line does not carry
      ROUTE_NO_HANDLER                                          -> must be 12 of 12
PASS iff pytest exits 0, (a) is 0 and (b) is 12 of 12.
Base run (before the cut): FAIL -- 4 ROUTE_NO_HANDLER lines; 8 of 12 operations reached a handler
(analysis-requests, analysis-report, status-summary, status-job do not: declared_entry_point looks for
generate_installed.py / status_installed.py in source_dir, and the source map stages both from reports/).
Issuer 2.0.0_SA_COO~Y, round 30. ASCII only.
"""
import os
import re
import subprocess
import sys

ROOT = str(__import__("pathlib").Path(__file__).resolve().parents[8])  # parents[0] is R30_checks; the repo root is parents[8]
BASE = os.path.join(ROOT, "infra", "aws", "lambda", "investor-reporting")
OUTCOMES = ("CONFORMS", "BLOCKED-BY-W2-S16", "DEPLOYED-ONLY", "NOT-A-ROUTE")
ROW = re.compile(r"^([a-z][a-z0-9-]+)\s+(%s)\s" % "|".join(re.escape(o) for o in OUTCOMES))


def main():
    try:
        run = subprocess.run([sys.executable, "-m", "pytest", "-s", "-q", "-p", "no:cacheprovider", "--color=no",
                              "_contracts/tests/test_seam_paired.py"], cwd=BASE, capture_output=True, text=True,
                             timeout=100)
    except subprocess.TimeoutExpired:
        print("FAIL: the seam suite timed out at 100 s")
        return 1
    lines = run.stdout.splitlines()
    no_handler = sum(1 for line in lines if "ROUTE_NO_HANDLER" in line)
    rows = {}
    for line in lines:
        hit = ROW.match(line)
        if hit:
            rows[hit.group(1)] = "ROUTE_NO_HANDLER" not in line
    reached = sum(1 for ok in rows.values() if ok)
    if run.returncode == 0 and no_handler == 0 and len(rows) == 12 and reached == 12:
        print("PASS: 0 ROUTE_NO_HANDLER lines and 12 of 12 operations reached a handler")
        return 0
    print("FAIL: %d ROUTE_NO_HANDLER lines; %d of %d operations reached a handler; pytest rc %d"
          % (no_handler, reached, len(rows), run.returncode))
    return 1


if __name__ == "__main__":
    sys.exit(main())
