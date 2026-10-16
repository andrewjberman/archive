#!/usr/bin/env python3
"""AR-y-368 base checker (0.9.0_WK_IRPT_ANLREQ~165). Prints BASE-OK only when the three signed run 1 and 2 files
(the driver, the mint helper and the run 1 csv, all under 0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/) are byte-identical to
the base commit and hash to their pinned sha256. Hashes and git diff only: never executes the driver or the mint helper.
Exit 0 = BASE-OK, 1 = BASE-BAD <why>."""
import hashlib
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
BASE = "2ba399d785"
FOLDER = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/"
PINS = [
    (FOLDER + "fwd1_driver.mjs", "455f660940bf34dd0de126d81ec0667df95d3030c7eb40621e26c1cb8eee1247"),
    (FOLDER + "fwd1_mint.py", "04e4ba64ddb74895442a7b291e14862fc9b395b65cc814c75bb737b8445ec5d4"),
    (FOLDER + "fwd1_holdings_49financial.csv", "23cbe4eb0bdaf0a950b33f304b4d9e50830ab032ae154edb0d458bf5ec44c3be"),
]


def main():
    paths = [p for p, _ in PINS]
    diff = subprocess.run(["git", "-C", str(ROOT), "diff", "--quiet", BASE, "--"] + paths, timeout=120)
    if diff.returncode != 0:
        print("BASE-BAD git diff --quiet %s rc=%d: a signed file differs from the base commit" % (BASE, diff.returncode))
        return 1
    matched = 0
    for rel, pin in PINS:
        digest = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        if digest != pin:
            print("BASE-BAD sha256 mismatch on %s: %s" % (rel.rsplit("/", 1)[1], digest))
            return 1
        matched += 1
    print("BASE-OK driver sha256 455f660940bf34dd0de126d81ec0667df95d3030c7eb40621e26c1cb8eee1247, "
          "mint 04e4ba64..., run 1 csv 23cbe4eb... unchanged (git diff rc=0 on 3 of 3 paths at %s; "
          "%d of 3 sha256 pins matched)" % (BASE, matched))
    return 0


if __name__ == "__main__":
    sys.exit(main())
