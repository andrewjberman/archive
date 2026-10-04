"""Round 45 HVST-ar-1 AC3 (ISSUER-graded after the served re-derivation): the same field census over the
SERVED silver tables (no --in-memory), graded by ar1_grade.py. Read-only. Prints `AC3 RESULT: PASS|FAIL`."""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
CENSUS = os.path.join(ROOT, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
                      "0.9.0_WK_AMGT_HARVST~93", "ar-1.field_census.py")
OUT = os.path.join(os.path.dirname(HERE), "ar-1.field_census.served.json")


def main():
    if not os.path.isfile(CENSUS):
        print("AC3: census script absent: %s" % CENSUS)
        print("AC3 RESULT: FAIL")
        return 1
    rc = subprocess.call([sys.executable, CENSUS, "--out", OUT], cwd=ROOT)
    if rc != 0 or not os.path.isfile(OUT):
        print("AC3: census rc=%s, output present=%s" % (rc, os.path.isfile(OUT)))
        print("AC3 RESULT: FAIL")
        return 1
    sys.path.insert(0, HERE)
    import ar1_grade
    return ar1_grade.main(OUT, "AC3")


if __name__ == "__main__":
    sys.exit(main())
