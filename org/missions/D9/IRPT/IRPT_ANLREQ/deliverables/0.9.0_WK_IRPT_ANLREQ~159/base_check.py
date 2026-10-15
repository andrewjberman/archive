"""AR362-y-AC2: the run 1 and 2 holdings csv, the signed driver and the signed mint helper are untouched.

Prints BASE-OK sha256 23cbe4eb0bdaf0a950b33f304b4d9e50830ab032ae154edb0d458bf5ec44c3be unchanged only when the three
paths are byte-identical to base commit 35193dba68 (git diff --quiet) and their sha256 values match the pins. Otherwise
prints BASE-BAD <why> and exits 1. Nothing is run: the driver and the mint helper are hashed, never executed.
"""
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WT = os.path.normpath(os.path.join(HERE, *([os.pardir] * 7)))
BASE_COMMIT = "35193dba68"
FOLDER = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver"
PINS = (
    (FOLDER + "/fwd1_holdings_49financial.csv",
     "23cbe4eb0bdaf0a950b33f304b4d9e50830ab032ae154edb0d458bf5ec44c3be"),
    (FOLDER + "/fwd1_driver.mjs",
     "ae008182f9ee3ad120ad9a9e7686dbb9e6cccaba360d8359253d3965e6329496"),
    (FOLDER + "/fwd1_mint.py",
     "04e4ba64ddb74895442a7b291e14862fc9b395b65cc814c75bb737b8445ec5d4"),
)


def sha256_of(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    paths = [rel for rel, _ in PINS]
    rc = subprocess.call(["git", "-C", WT, "diff", "--quiet", BASE_COMMIT, "--"] + paths)
    if rc != 0:
        print("BASE-BAD git diff --quiet %s rc=%d over the three signed paths (differs from base, or git failed)"
              % (BASE_COMMIT, rc))
        return 1
    for rel, want in PINS:
        got = sha256_of(os.path.join(WT, *rel.split("/")))
        if got != want:
            print("BASE-BAD %s sha256 %s differs from pinned %s" % (rel, got, want))
            return 1
    print("BASE-OK sha256 23cbe4eb0bdaf0a950b33f304b4d9e50830ab032ae154edb0d458bf5ec44c3be unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
