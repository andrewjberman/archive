"""AMGT_RESAPP round-87 PREP -- ONE disposition pass over the project's open remediation rows (CTO~DELL1 round-86 analysis R3).

  python r87_rows.py --ledger <json> [--census <comp-surprise json>]

The DOMAIN is every remediation row of AMGT_RESAPP that reads `closed: false` in `comp-surprise --project AMGT_RESAPP --json`
(re-read live unless --census names a saved read); its size is printed first. The ledger is a JSON list of
    {"id": <row id>, "disposition": "CLOSED", "commit": <hash that resolved it>, "basis": <one line>}
    {"id": <row id>, "disposition": "CARRIED", "owner": <seat serial>, "condition": <what clears it>}
    {"id": <row id>, "disposition": "DISMISSED", "reason": <why it is not a defect any more>}
    L1 every open row id appears in the ledger exactly once (missing and duplicated ids printed);
    L2 no ledger id lies outside the open set;
    L3 every CLOSED commit resolves in this repository (git cat-file -e <hash>^{commit});
    L4 every CARRIED row names a seat serial (`<n>.<n>.<n>_<XX>_...`) and a non-empty condition;
    L5 every DISMISSED row carries a reason of at least 20 characters.
The count after the pass is printed: CLOSED / CARRIED / DISMISSED of the open denominator, and carried-without-owner (must be 0).
Verdict: R87 ROWS: YES|NO (exit 0|1). At the base (2026-10-09 ~18:4xZ): NO -- no ledger; 125 open of 505 remediation rows.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
import sys

SERIAL_RE = re.compile(r"^\d+\.\d+\.\d+_[A-Z]{2}_\S+$")


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def _census(path):
    if path:
        return json.load(open(path, encoding="utf-8"))
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    out = subprocess.run([sys.executable, root + "/.tools/comp-surprise.py", "--project", "AMGT_RESAPP", "--json"],
                         capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0 or not out.stdout.strip():
        print("ERROR: comp-surprise read failed rc=%s: %s" % (out.returncode, out.stderr.strip()[:300]))
        sys.exit(2)
    return json.loads(out.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--census")
    a = ap.parse_args()
    rows = _census(a.census)["remediation_rows"]
    open_ids = [r["id"] for r in rows if not r.get("closed")]
    print("   domain: %d remediation rows, %d read closed:false" % (len(rows), len(open_ids)))
    try:
        ledger = json.load(open(a.ledger, encoding="utf-8"))
    except (OSError, ValueError) as e:
        say(False, "L1 ledger readable: %s" % e)
        print("R87 ROWS: NO")
        return 1
    counts = collections.Counter(e.get("id") for e in ledger)
    missing = [i for i in open_ids if counts[i] == 0]
    dup = [i for i, n in counts.items() if n > 1]
    outside = [i for i in counts if i not in set(open_ids)]
    l1 = say(not missing and not dup, "L1 every open row disposed exactly once: %d of %d (missing %d %s; duplicated %s)" % (
        len(open_ids) - len(missing), len(open_ids), len(missing), missing[:5], dup[:5]))
    l2 = say(not outside, "L2 no ledger id outside the open set: %d outside %s" % (len(outside), outside[:5]))
    bad3, bad4, bad5 = [], [], []
    kinds = collections.Counter()
    for e in ledger:
        d = e.get("disposition")
        kinds[d] += 1
        if d == "CLOSED":
            c = str(e.get("commit") or "")
            ok = bool(c) and subprocess.run(["git", "cat-file", "-e", c + "^{commit}"], capture_output=True).returncode == 0
            if not ok:
                bad3.append(e.get("id"))
        elif d == "CARRIED":
            if not SERIAL_RE.match(str(e.get("owner") or "")) or not str(e.get("condition") or "").strip():
                bad4.append(e.get("id"))
        elif d == "DISMISSED":
            if len(str(e.get("reason") or "").strip()) < 20:
                bad5.append(e.get("id"))
        else:
            bad5.append(e.get("id"))
    l3 = say(not bad3, "L3 every CLOSED commit resolves: %d bad %s" % (len(bad3), bad3[:5]))
    l4 = say(not bad4, "L4 every CARRIED row names a seat serial and a condition: %d bad %s" % (len(bad4), bad4[:5]))
    l5 = say(not bad5, "L5 every DISMISSED row carries a reason (and no unknown disposition): %d bad %s" % (len(bad5), bad5[:5]))
    print("   count after the pass: CLOSED %d, CARRIED %d, DISMISSED %d of %d open; carried without an owner %d" % (
        kinds["CLOSED"], kinds["CARRIED"], kinds["DISMISSED"], len(open_ids), len(bad4)))
    ok = l1 and l2 and l3 and l4 and l5
    print("R87 ROWS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
