"""AMGT_RESAPP round 81 -- AMGT-ee-5, the walk on DEV of FWD-18 on ASML NA: the capture floor.

  python r80_dd3.py [--floor 6] [--dir <captures dir>]

C1 the walk's captures directory (default deliverables/0.9.0_WK_AMGT_RESAPP~322/captures) holds --floor or more PNG files;
C2 WALK_ROUND81.md beside it exists, names the portal commit it walked on a line starting 'PORTAL_REF:', and heads every act
   of the order by its token: FWD-18 (an act not walked is still headed, with its reason).
Verdict: R81 EE5 WALK RECORD: YES|NO (exit 0|1). The walk's reading is the CVO's (AC3, judgment); this grades only the record.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

BASE = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~322"
ACTS = ("FWD-18",)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--floor", type=int, default=6)
    ap.add_argument("--dir", default="")
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    caps = a.dir or os.path.join(root, BASE, "captures")
    pngs = sorted(f for f in os.listdir(caps) if f.lower().endswith(".png")) if os.path.isdir(caps) else []
    c1 = len(pngs) >= a.floor
    print(f"{'PASS' if c1 else 'FAIL'} C1 the captures directory holds the floor {len(pngs)} of {a.floor}")
    record = os.path.join(os.path.dirname(caps), "WALK_ROUND81.md")
    text = open(record, encoding="utf-8").read() if os.path.isfile(record) else ""
    missing = [t for t in ACTS if not re.search(r"^#+ .*\b%s\b(?!\d)" % re.escape(t), text, re.M)]
    ref = re.search(r"^PORTAL_REF:\s*([0-9a-f]{7,40})\b", text, re.M)
    c2 = bool(text) and not missing and bool(ref)
    print(f"{'PASS' if c2 else 'FAIL'} C2 the walk record heads every act and names its portal ref: "
          f"missing heads {missing if text else 'the record'}; PORTAL_REF {ref.group(1) if ref else 'absent'}")
    ok = c1 and c2
    print(f"R81 EE5 WALK RECORD: {'YES' if ok else 'NO'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
