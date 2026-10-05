"""Round 46 HVST-as-1 AC3: the backfill driver's dry run plans the rank universe and makes no network call.

Runs `python -m lib.opal_data_harvest.backfill_driver --checkpoint <temp> --dry-run` and requires `UNIVERSE: 191` and
`NETWORK CALLS: 0` in its output, plus 191 x 5 = 955 PLAN lines. Prints `AC3 RESULT: PASS|FAIL`.
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))


def main():
    ck = os.path.join(tempfile.mkdtemp(prefix="as1ac3_"), "checkpoint.json")
    r = subprocess.run([sys.executable, "-m", "lib.opal_data_harvest.backfill_driver", "--checkpoint", ck, "--dry-run"],
                       cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
    out = r.stdout + r.stderr
    plans = sum(1 for line in out.splitlines() if line.startswith("PLAN "))
    for line in out.splitlines():
        if line.startswith(("UNIVERSE", "BUDGET sa", "NETWORK CALLS")):
            print("AC3 " + line)
    print("AC3 rc=%d; PLAN lines %d" % (r.returncode, plans))
    ok = r.returncode == 0 and "UNIVERSE: 191" in out and "NETWORK CALLS: 0" in out and plans == 955
    print("AC3 RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
