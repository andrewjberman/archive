"""Round 47 HVST-at-1 AC2: the timing control (CTO ruling @7cd62976f1, round-46 analysis item 1).

Runs the worker's control `deliverables/0.9.0_WK_AMGT_HARVST~95/at-1.timing_control.py`. It drives
`HarvestUploader._run_listings` over the SAME 100 planted listing pages through the OLD per-group path and the NEW batched path,
against a stub S3 client whose silver `listing_hit` prefix already holds many parts. It must print:
`silver prefix reads: old <N> new <M>`, `wall seconds: old <a> new <b>`, `rows identical: True`, and `AC2 RESULT: PASS|FAIL`.
PASS requires: new prefix reads == 1 per source per pass, old > new, and rows identical. No network. Prints
`AC2 RESULT: PASS|FAIL`.
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
CONTROL = os.path.join(ROOT, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables", "0.9.0_WK_AMGT_HARVST~95",
                       "at-1.timing_control.py")


def main():
    if not os.path.isfile(CONTROL):
        print("AC2: timing control absent: %s" % CONTROL)
        print("AC2 RESULT: FAIL")
        return 1
    r = subprocess.run([sys.executable, CONTROL], cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=900)
    out = r.stdout + r.stderr
    for line in out.splitlines():
        if line.startswith(("silver prefix reads", "wall seconds", "rows identical", "AC2 RESULT")):
            print(line)
    ok = r.returncode == 0 and "AC2 RESULT: PASS" in out and "rows identical: True" in out
    if "AC2 RESULT" not in out:
        print("AC2 RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
