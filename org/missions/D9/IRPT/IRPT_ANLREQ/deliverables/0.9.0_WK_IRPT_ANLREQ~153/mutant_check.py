#!/usr/bin/env python3
"""AR352-y-AC3 checker (worker 0.9.0_WK_IRPT_ANLREQ~153, order IRPT_ANLREQ.TO-AR-y-352).

The one mutant: the new POST_ALLOWED entry for directory/resolve is loosened to
/^\\/api\\/scoped\\/investor-reporting\\/directory\\/.*$/ in a scratch copy OUTSIDE the product tree.
The copy's self-test must FAIL for the mutant to count as fired. Prints MUTANT-FIRES when the run
fails (exit 0); MUTANT-SURVIVES otherwise (exit 1).
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]  # <root>/org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/<serial>
DRIVER = ROOT / ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/"
                 "0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/fwd1_driver.mjs")

EXACT = r"  /^\/api\/scoped\/investor-reporting\/directory\/resolve$/,"
LOOSE = r"  /^\/api\/scoped\/investor-reporting\/directory\/.*$/,"


def main():
    text = DRIVER.read_text(encoding="utf-8")
    hits = text.count(EXACT)
    if hits != 1:
        print("MUTANT-SURVIVES target line is not unique in the amended driver (count %d)" % hits)
        return 1
    mutant = text.replace(EXACT, LOOSE)
    scratch = Path(tempfile.mkdtemp(prefix="ar352_mutant_"))
    try:
        copy = scratch / "fwd1_driver.mjs"
        copy.write_text(mutant, encoding="utf-8")
        run = subprocess.run(["node", str(copy), "--selftest"], capture_output=True, text=True, timeout=120)
        fails = [ln for ln in run.stdout.splitlines() if ln.startswith("case FAIL ")]
        summary = [ln for ln in run.stdout.splitlines() if ln.startswith("SELFTEST-")]
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    if run.returncode != 0:
        print("MUTANT-FIRES loosened entry %s" % LOOSE.strip())
        print("mutant selftest rc=%d; %s" % (run.returncode, summary[-1] if summary else "no summary line"))
        for f in fails:
            print(f)
        return 0
    print("MUTANT-SURVIVES the loosened entry passed the self-test (rc=%d)" % run.returncode)
    return 1


if __name__ == "__main__":
    sys.exit(main())
