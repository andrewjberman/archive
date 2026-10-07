"""AMGT_RESAPP round 78 -- AMGT-bb-20, the line-ending cell (round-77 ruling 12 as amended by the CTO, C1 option (a) narrowed).

  python r78_bb20.py --crit AC1|AC2|AC3

The landable list is HYGIENE_LANDABLE_FILES_20261007.txt beside the round's notes: the files that carry CR in their index blob
under an `eol=lf` attribute, pass the commit gate as they stand, and are NOT under infra/aws/lambda/.

AC1 (build) every listed file reads `i/lf` in `git ls-files --eol` (at the base every one reads `i/crlf`).
AC2 (bound) for every listed file the committed bytes at HEAD, with CR removed, equal the bytes at the base commit with CR
    removed: a line-ending change and nothing else.
AC3 (bound) between the base commit and HEAD no file under data/smartx/ or infra/aws/ changed other than the listed ones, so
    no Lambda source and no gate-failing file moved.
Verdict: R78 BB20 <crit> SERVED: YES|NO (exit 0|1). Reads git only.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

LIST = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/HYGIENE_LANDABLE_FILES_20261007.txt"
BASE = "6989a232db"  # the shared tree's HEAD when the list was measured (2026-10-07 ~15:1xZ)


def _git(root, *args, text=True):
    return subprocess.run(["git", "-C", root] + list(args), capture_output=True, text=text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    with open(os.path.join(root, LIST), encoding="utf-8") as fh:
        files = [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]
    results = []

    def clause(name, cond, detail=""):
        results.append(bool(cond))
        print("%s %s %s" % ("PASS" if cond else "FAIL", name, detail))

    clause("C0 the list holds the files and none is a Lambda source", len(files) == 9
           and not any(f.startswith("infra/aws/lambda/") for f in files), "%d file(s)" % len(files))
    if a.crit == "AC1":
        eol = {}
        for line in _git(root, "ls-files", "--eol", "--", *files).stdout.splitlines():
            parts = line.split()
            eol[parts[-1]] = parts[0]
        lf = [f for f in files if eol.get(f) == "i/lf"]
        clause("C1 every listed file reads i/lf in the index", len(lf) == len(files),
               "%d of %d; not lf: %s" % (len(lf), len(files), [f for f in files if eol.get(f) != "i/lf"][:4]))
    elif a.crit == "AC2":
        same = []
        for f in files:
            old = _git(root, "show", "%s:%s" % (BASE, f), text=False).stdout.replace(b"\r", b"")
            new = _git(root, "show", "HEAD:%s" % f, text=False).stdout.replace(b"\r", b"")
            if old and old == new:
                same.append(f)
        clause("C1 with CR removed, every listed file equals its bytes at the base", len(same) == len(files),
               "%d of %d against %s" % (len(same), len(files), BASE))
    else:
        # AMENDMENT 1 (issuer): BASE..HEAD on the shared tree also holds other projects' commits under infra/aws, so the
        # diff graded a peer's work. The bound is THIS cell's own change: the commits authored by the cell's worker.
        changed = sorted(set(p for p in _git(root, "log", "--author=0.9.0_WK_AMGT_RESAPP~304 <", "--name-only", "--format=", "--",
                                             "data/smartx", "infra/aws").stdout.splitlines() if p.strip()))
        other = [p for p in changed if p not in files]
        clause("C1 the cell's own commits changed nothing else under data/smartx or infra/aws", bool(changed) and not other,
               "changed %d, outside the list %d %s" % (len(changed), len(other), other[:4]))
    ok = all(results)
    print("R78 BB20 %s SERVED: %s" % (a.crit, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
