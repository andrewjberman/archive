"""AR345-y-AC2 checker (0.9.0_WK_IRPT_ANLREQ~149): the one mutant that must fire.

Copies fwd1_driver.mjs to a scratch folder OUTSIDE the worktree (a tempfile.mkdtemp under the system temp), replaces the
POST branch of the route guard so that it admits EVERY POST, and runs that copy's --selftest. Prints MUTANT-FIRES only when
that run FAILS (exit non-zero with SELFTEST-BAD); otherwise MUTANT-SURVIVES and exit 1. A marker that is not found exactly
once is MUTANT-SURVIVES too: the mutant was not applied, so nothing fired.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "fwd1_driver" / "fwd1_driver.mjs"
MARK = "return POST_ALLOWED.some((re) => re.test(u.pathname))"
MUTANT_BODY = "return true"


def main():
    src = SRC.read_text(encoding="utf-8")
    count = src.count(MARK)
    if count != 1:
        print("MUTANT-SURVIVES guard marker found %d times, mutant not applied" % count)
        return 1
    mutant = src.replace(MARK, MUTANT_BODY)
    tmp = tempfile.mkdtemp(prefix="fwd1_mutant_")
    try:
        copy = Path(tmp) / "fwd1_driver.mjs"
        copy.write_text(mutant, encoding="utf-8")
        r = subprocess.run(["node", str(copy), "--selftest"], capture_output=True, text=True, timeout=300)
        bad_lines = [ln for ln in r.stdout.splitlines() if ln.startswith("SELFTEST-BAD")]
        if r.returncode != 0 and bad_lines:
            print("MUTANT-FIRES every-POST guard: selftest rc=%d; %s" % (r.returncode, bad_lines[0][:300]))
            return 0
        print("MUTANT-SURVIVES every-POST guard: selftest rc=%d, no SELFTEST-BAD line" % r.returncode)
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
