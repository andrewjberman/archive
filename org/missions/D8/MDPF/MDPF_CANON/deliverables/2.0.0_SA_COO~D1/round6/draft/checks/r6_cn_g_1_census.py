#!/usr/bin/env python3
"""MDPF_CANON round 6 -- issuer census check for cell CN-g-1 (the READER_CENSUS rows of dim_mdpf_non_model_assets.py).

Prints one `ARM <name>: PASS|FAIL <detail>` line per arm, then `ROUND 6 CENSUS: k of n arms`; exit 0 only when every arm passes.
ASCII only. Offline, reads two files. Terminates in well under a second.

  C1 GOLD-ROW      a READER_CENSUS row names `dim_mdpf_non_model_assets.py`, names the gold tier at the builder address, carries no
                   `gold/mdpf_revamp/` text, and every line it cites exists in the file and holds `partition_uri` or `def load_`
  C2 STAGING-ROW   the staging row that remains for this file (it still WRITES STAGING_KEY and READS the frozen pre-cutover snapshot)
                   cites only lines holding `STAGING_KEY` or `FROZEN_PRECUTOVER_KEY`, and no line of the old default URIs
  C3 NO-OTHER-READ no other row of the census cites this file at a line whose text names a staged aggregate
  C4 CONTROL       the `build_portal_gold_accrual.py` row is still present and still names the staging tree (a control that must pass
                   at the base, so the arms above are shown able to read the table)

  --script <path>  the file under test (default: data/mdpf/scripts/gold/dim_mdpf_non_model_assets.py)
  --census <path>  the census file (default: the CN-d-4 / CN-e-1 deliverable)
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or os.getcwd()
DEFAULT_SCRIPT = os.path.join(ROOT, "data", "mdpf", "scripts", "gold", "dim_mdpf_non_model_assets.py")
DEFAULT_CENSUS = os.path.join(ROOT, "org", "missions", "D8", "MDPF", "MDPF_CANON", "deliverables", "0.9.0_WK_MDPF_CANON~4", "READER_CENSUS.md")
FILE = "dim_mdpf_non_model_assets.py"
REL = "data/mdpf/scripts/gold/" + FILE
CITE = re.compile(re.escape(REL) + r":(\d+)")


def _rows(census: str):
    return [ln for ln in open(census, encoding="utf-8").read().splitlines() if ln.startswith("|")]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--script", default=DEFAULT_SCRIPT)
    ap.add_argument("--census", default=DEFAULT_CENSUS)
    args = ap.parse_args(argv)
    src = open(args.script, encoding="utf-8").read().splitlines()
    rows = [r for r in _rows(args.census) if FILE in r]
    first_cell = lambda r: r.split("|")[1].strip()  # noqa: E731
    gold_rows = [r for r in rows if "gold/mdpf_revamp/" not in first_cell(r) and "gold tier" in first_cell(r).lower()]
    stage_rows = [r for r in rows if first_cell(r).startswith("gold/mdpf_revamp/")]
    arms = []

    ok = False
    detail = "no row names the gold tier for %s" % FILE
    if gold_rows:
        r = gold_rows[0]
        lines = [int(x) for x in CITE.findall(r)]
        good = bool(lines) and all(0 < n <= len(src) and ("partition_uri" in src[n - 1] or "def load_" in src[n - 1]
                                                       or "def _gold_partition" in src[n - 1]) for n in lines)
        ok = good and "gold/mdpf_revamp/" not in r
        detail = "row cites lines %s; texts %s; staging text in row: %s" % (
            lines, [src[n - 1].strip()[:40] for n in lines if 0 < n <= len(src)], "gold/mdpf_revamp/" in r)
    arms.append(("C1 GOLD-ROW", ok, detail))

    ok = False
    detail = "no staging row remains for %s (it still writes STAGING_KEY and reads the frozen snapshot)" % FILE
    if stage_rows:
        lines = [int(x) for r in stage_rows for x in CITE.findall(r)]
        bad = [n for n in lines if not (0 < n <= len(src) and ("STAGING_KEY" in src[n - 1] or "FROZEN_PRECUTOVER_KEY" in src[n - 1]))]
        old_defaults = [n for n in lines if 0 < n <= len(src) and "DEFAULT_" in src[n - 1] and "_URI" in src[n - 1]]
        ok = bool(lines) and not bad and not old_defaults
        detail = "staging row cites lines %s; lines that are not a key definition: %s; old default URIs cited: %s" % (lines, bad, old_defaults)
    arms.append(("C2 STAGING-ROW", ok, detail))

    stray = []
    for r in rows:
        for n in (int(x) for x in CITE.findall(r)):
            if 0 < n <= len(src) and "aggregate_aua_timeseries.json" in src[n - 1]:
                stray.append(n)
    arms.append(("C3 NO-OTHER-READ", not stray, "census citations of a line holding a staged aggregate path: %s" % (stray or "none")))

    ctl = [r for r in _rows(args.census) if "build_portal_gold_accrual.py" in r and "gold/mdpf_revamp/" in r]
    arms.append(("C4 CONTROL", bool(ctl), "accrual-bridge rows naming the staging tree: %d (must be >= 1)" % len(ctl)))

    passed = 0
    for name, ok, detail in arms:
        print("ARM %s: %s %s" % (name, "PASS" if ok else "FAIL", detail))
        passed += 1 if ok else 0
    print("ROUND 6 CENSUS: %d of %d arms" % (passed, len(arms)))
    return 0 if passed == len(arms) else 1


if __name__ == "__main__":
    sys.exit(main())
