"""AMGT_RESAPP round 77 -- cell AMGT-ba-5 (CTO round-76 ruling 6; rows Z-W266-S2 and Z-W266-S3): the page repairs
on the security page's driver chart and segment breakdown.

  AC1  one press opens the filing passage ONCE, also where several points share one passage id
  AC2  a served table passage is drawn as a table with its column labels; the y axis formats its ticks
  AC3  the segment breakdown shows one heading per segment

Each criterion runs `r77_ba5_harness.cjs` (beside this file) with node against the portal checkout under the
repository root: the ACTUAL `ThesisDriverChart.tsx` / `SegmentBreakdown.tsx`, transpiled and walked, fed the
DEPLOYED /thesis bytes in `r77_groupB_fixture.json`. No browser, no network, no write.

  python r77_ba5.py --crit AC1|AC2|AC3 [--where local]
Prints the harness's PASS / FAIL clause lines and `R77 BA5 <crit> SERVED: YES|NO`; exit 0 on YES.
"""
import argparse
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    node = shutil.which("node")
    if not node:
        print("FAIL the instrument could not run: node is not on PATH")
        print("R77 BA5 %s SERVED: NO" % a.crit)
        return 1
    try:
        done = subprocess.run([node, os.path.join(HERE, "r77_ba5_harness.cjs"), "--crit", a.crit], timeout=100)
    except subprocess.TimeoutExpired:
        print("FAIL the instrument did not finish in 100 s")
        print("R77 BA5 %s SERVED: NO" % a.crit)
        return 1
    return done.returncode


if __name__ == "__main__":
    sys.exit(main())
