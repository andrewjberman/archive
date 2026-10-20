#!/usr/bin/env python3
"""BF-r-3 check: the two hand-parsing readers and their test file equal their pre-round bytes.

Under PRD v0.7 the two readers read master 08335338 (0833), which stays on today's key, so they need no change; the
round-2 edit comes back out. Compares `git rev-parse HEAD:<file>` with the blob at the round-1 base commit 5f1ad506a4.
Prints `RESTORE-OK files=3` or `RESTORE-DIFF file=<f> head=<blob> base=<blob>` per differing file, then exits 1.
"""
import subprocess
import sys

BASE = "5f1ad506a4"
FILES = [
    "data/canonical/schwab/build_canonical_daily.py",
    "data/canonical/schwab/silver/build_fact_tax_1099div.py",
    "data/canonical/schwab/tests/test_canonical_daily_date_axis.py",
]


def blob(rev, path):
    r = subprocess.run(["git", "rev-parse", f"{rev}:{path}"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else "MISSING"


def main():
    bad = 0
    for f in FILES:
        h, b = blob("HEAD", f), blob(BASE, f)
        if h != b:
            bad += 1
            print(f"RESTORE-DIFF file={f} head={h} base={b}")
    if bad:
        print(f"RESTORE-FAIL differing={bad} of {len(FILES)}")
        return 1
    print(f"RESTORE-OK files={len(FILES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
