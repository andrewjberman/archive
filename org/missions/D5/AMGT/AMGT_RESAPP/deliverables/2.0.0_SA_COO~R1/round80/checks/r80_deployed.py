"""AMGT_RESAPP round 80 -- AMGT-dd-4, the redeploy's round-80 arm: every build cell's deployed check, in one run.

  python r80_deployed.py [--list <file>]

Reads r80_deployed_cells.txt beside this file: one shell command per line (a `#` line is a comment), each a round-80 build cell's
own check against the DEPLOYED function. The issuer fills that list at the GO, from the cells that drained. Runs each command from
the repository root with PYTHONPATH set to it; a command passes on exit 0.
Verdict: R80 DEPLOYED: YES n of n (exit 0); NO k of n (exit 1); an EMPTY list is NO CELLS LISTED (exit 2), never a pass.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", default="")
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    path = a.list or os.path.join(here, "r80_deployed_cells.txt")
    lines = []
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as fh:
            lines = [ln.strip() for ln in fh if ln.strip() and not ln.strip().startswith("#")]
    if not lines:
        print(f"R80 DEPLOYED: NO CELLS LISTED ({path})")
        return 2
    env = dict(os.environ, PYTHONPATH=root)
    passed = 0
    for cmd in lines:
        p = subprocess.run(cmd, shell=True, cwd=root, env=env, capture_output=True, text=True, timeout=1500)
        tail = [ln for ln in (p.stdout or "").strip().splitlines()[-2:]]
        print(f"{'PASS' if p.returncode == 0 else 'FAIL'} exit={p.returncode} :: {cmd} :: {' | '.join(tail)[:200]}")
        passed += p.returncode == 0
    ok = passed == len(lines)
    print(f"R80 DEPLOYED: {'YES' if ok else 'NO'} {passed} of {len(lines)}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
