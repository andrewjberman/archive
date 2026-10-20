#!/usr/bin/env python3
"""BF-z-2 check: the five round-1 master-form files equal their pre-round bytes.

Compares `git rev-parse HEAD:<file>` with the blob at the round-1 base commit 5f1ad506a4 (the issuance commit; its
first-parent-of-the-merge twin 293346aff1^1 holds the same blobs for these five files, measured 2026-10-20).
Prints `RESTORE-OK files=5` or `RESTORE-DIFF file=<f> head=<blob> base=<blob>` per differing file, then exits 1.
"""
import subprocess
import sys

BASE = "5f1ad506a4"
FILES = [
    "data/black_diamond/scripts/bronze/_monolith_bronze.py",
    "data/canonical/schwab/silver/_canonical_silver_lib.py",
    "data/canonical/schwab/build_canonical_daily.py",
    "data/canonical/schwab/silver/build_fact_tax_1099div.py",
    "data/canonical/schwab/tests/test_canonical_daily_date_axis.py",
]


def blob(rev, path):
    r = subprocess.run(["git", "rev-parse", f"{rev}:{path}"], capture_output=True, text=True)
    if r.returncode != 0:
        return "MISSING"
    return r.stdout.strip()


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
