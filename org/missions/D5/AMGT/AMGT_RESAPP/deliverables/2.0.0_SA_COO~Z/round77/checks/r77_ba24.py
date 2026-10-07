"""AMGT_RESAPP round 77 -- AMGT-ba-24, the walk on DEV: the capture floor.

  python r77_ba24.py [--floor 10] [--dir <captures dir>]

C1 the walk's captures directory (default deliverables/0.9.0_WK_AMGT_RESAPP~286/captures) holds --floor or more PNG files;
C2 WALK_ROUND77.md beside it exists and names every act of the order by its heading token: FWD-7, FWD-1, FWD-18, FWD-14,
   FWD-16 and FWD-12 (an act not walked is still named, with its reason).
Verdict: R77 BA24 WALK RECORD: YES|NO (exit 0|1). The walk's reading is the CVO's (AC3, judgment); this grades only the record.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

BASE = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~286"
ACTS = ("FWD-7", "FWD-1", "FWD-18", "FWD-14", "FWD-16", "FWD-12")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--floor", type=int, default=10)
    ap.add_argument("--dir", default="")
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    caps = a.dir or os.path.join(root, BASE, "captures")
    pngs = sorted(f for f in os.listdir(caps) if f.lower().endswith(".png")) if os.path.isdir(caps) else []
    c1 = len(pngs) >= a.floor
    print(f"{'PASS' if c1 else 'FAIL'} C1 the captures directory holds the floor {len(pngs)} of {a.floor}")
    record = os.path.join(os.path.dirname(caps), "WALK_ROUND77.md")
    text = open(record, encoding="utf-8").read() if os.path.isfile(record) else ""
    missing = [t for t in ACTS if t not in text]
    c2 = bool(text) and not missing
    print(f"{'PASS' if c2 else 'FAIL'} C2 the walk record names every act missing {missing if text else 'the record'}")
    ok = c1 and c2
    print(f"R77 BA24 WALK RECORD: {'YES' if ok else 'NO'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
