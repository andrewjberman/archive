#!/usr/bin/env python3
"""IB-yr-303 AC2 -- the two generate test files that are red at the base when run ALONE collect and pass alone.

Each file runs in its OWN pytest process (a shared process would let the first file's sys.path edit carry the
second), from infra/aws/lambda/investor-reporting, bounded at 100 s each:
  ycharts/generate/tests/test_read_back_poll.py
  ycharts/generate/tests/test_resolve_upload.py
PASS iff both exit 0 with at least one test passed and none failed or errored.
Base run (before the cut): FAIL, 0 of 2 -- both stop at collection on
`ModuleNotFoundError: No module named 'extract'` (resident_worker.py imports it; the file's own sys.path setup does
not name ycharts/extract).
Issuer 2.0.0_SA_COO~Y, round 30. ASCII only.
"""
import os
import re
import subprocess
import sys

ROOT = str(__import__("pathlib").Path(__file__).resolve().parents[8])  # parents[0] is R30_checks; the repo root is parents[8]
BASE = os.path.join(ROOT, "infra", "aws", "lambda", "investor-reporting")
FILES = ("ycharts/generate/tests/test_read_back_poll.py", "ycharts/generate/tests/test_resolve_upload.py")


def main():
    good, notes = 0, []
    for rel in FILES:
        try:
            run = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", rel],
                                 cwd=BASE, capture_output=True, text=True, timeout=100)
        except subprocess.TimeoutExpired:
            notes.append("%s: timeout at 100 s" % os.path.basename(rel))
            continue
        tail = (run.stdout.strip().splitlines() or ["<no output>"])[-1]
        passed = re.search(r"(\d+) passed", tail)
        bad = re.search(r"(\d+) (failed|error)", tail)
        if run.returncode == 0 and passed and int(passed.group(1)) >= 1 and not bad:
            good += 1
        else:
            notes.append("%s: rc %d, %s" % (os.path.basename(rel), run.returncode, tail))
    if good == len(FILES):
        print("PASS: 2 of 2 files collect and pass alone")
        return 0
    print("FAIL: %d of 2 files collect and pass alone -- %s" % (good, " | ".join(notes)))
    return 1


if __name__ == "__main__":
    sys.exit(main())
