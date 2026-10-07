"""AMGT_RESAPP round 77 -- AMGT-ba-19, the chatter phase-COVERAGE read (CTO round-76 analysis, ruling 4; row Z-S360).

  python r77_ba19.py --cell coverage|inputs [--file <PHASE_COVERAGE.json>]

Reads the worker's PHASE_COVERAGE.json (default: deliverables/0.9.0_WK_AMGT_RESAPP~285/PHASE_COVERAGE.json). Shape:
  {"function_code_sha256": "...",
   "cold_invokes": [{"request_id": "...", "init_ms": 0.0, "duration_ms": 0.0,
                     "phases": [{"label": "...", "ms": 0.0}], "outside_ms": 0.0}],
   "label_set": ["..."],
   "emit_sites": [{"file": "lib/...py", "line": 0, "label": "..."}],
   "free_cuts": [{"what": "...", "est_ms": 0.0}], "free_cuts_exhausted": false, "residual_ms": 0.0,
   "provisioned_concurrency_inputs": {"memory_mb": 1769, "instances": 1, "price_per_gb_second": 0.0,
                                      "price_source": "...", "hours_per_month": 730, "monthly_usd": 0.0}}

coverage: C1 at least 3 cold invokes, and for each one sum(phases) + outside_ms equals duration_ms within 1 ms; C2 every phase
    label is in label_set and every label_set member has an emit site whose file exists and whose line is inside the file;
    C3 either free_cuts is non-empty or free_cuts_exhausted is true with a residual_ms above 0.
inputs: C1 memory_mb is 1769 and instances is 1; C2 price_source is non-empty; C3 monthly_usd equals
    memory_mb/1024 * price_per_gb_second * 3600 * hours_per_month * instances within 0.01.
Verdict: R77 BA19 <CELL>: YES|NO (exit 0|1).
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

DEFAULT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~285/PHASE_COVERAGE.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", choices=("coverage", "inputs"), required=True)
    ap.add_argument("--file", default="")
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    path = a.file or os.path.join(root, DEFAULT)
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if not os.path.isfile(path):
        print(f"   no coverage file at {path}")
        clause("C0 the coverage file exists", False)
        return _verdict(a, ok)
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    if a.cell == "coverage":
        cold = doc.get("cold_invokes") or []
        gaps = []
        for inv in cold:
            total = sum(float(p.get("ms") or 0.0) for p in inv.get("phases") or []) + float(inv.get("outside_ms") or 0.0)
            if abs(total - float(inv.get("duration_ms") or 0.0)) > 1.0:
                gaps.append((inv.get("request_id"), round(total, 1), inv.get("duration_ms")))
        print(f"   cold invokes {len(cold)}; invokes whose attribution does not sum to the Duration {len(gaps)} e.g. {gaps[:3]}")
        clause("C1 every cold millisecond is attributed (sum equals Duration within 1 ms, 3 or more cold invokes)",
               len(cold) >= 3 and not gaps, f"{len(cold) - len(gaps)} of {len(cold)}")
        labels = set(doc.get("label_set") or [])
        used = {p.get("label") for inv in cold for p in inv.get("phases") or []}
        sites = doc.get("emit_sites") or []
        bad_sites = []
        for s in sites:
            f = os.path.join(root, s.get("file") or "")
            try:
                with open(f, encoding="utf-8") as fh:
                    n = sum(1 for _ in fh)
                if not 1 <= int(s.get("line") or 0) <= n:
                    bad_sites.append(s)
            except OSError:
                bad_sites.append(s)
        sited = {s.get("label") for s in sites}
        print(f"   labels {len(labels)}; used but unlisted {sorted(used - labels)}; listed with no emit site {sorted(labels - sited)}; "
              f"bad emit sites {len(bad_sites)}")
        clause("C2 the label set is closed and every label has a real emit site",
               labels and not (used - labels) and not (labels - sited) and not bad_sites, f"{len(sites)} sites")
        cuts = doc.get("free_cuts") or []
        exhausted = bool(doc.get("free_cuts_exhausted")) and float(doc.get("residual_ms") or 0.0) > 0.0
        clause("C3 the free cuts are listed, or stated exhausted with the residual", bool(cuts) or exhausted,
               f"cuts {len(cuts)}; exhausted {bool(doc.get('free_cuts_exhausted'))}; residual {doc.get('residual_ms')}")
    else:
        pc = doc.get("provisioned_concurrency_inputs") or {}
        clause("C1 memory 1769 MB and one instance", pc.get("memory_mb") == 1769 and pc.get("instances") == 1,
               f"{pc.get('memory_mb')} MB x {pc.get('instances')}")
        clause("C2 the price carries its source", bool(str(pc.get("price_source") or "").strip()), str(pc.get("price_source"))[:80])
        try:
            want = (1769 / 1024.0) * float(pc["price_per_gb_second"]) * 3600.0 * float(pc["hours_per_month"]) * 1
            got = float(pc["monthly_usd"])
            arith = abs(want - got) <= 0.01 and got > 0
        except (KeyError, TypeError, ValueError):
            want, got, arith = None, None, False
        clause("C3 the monthly figure is the stated arithmetic", arith, f"stated {got}; computed {want}")
    return _verdict(a, ok)


def _verdict(a, ok):
    verdict = "YES" if ok and all(ok) else "NO"
    print(f"R77 BA19 {a.cell.upper()}: {verdict}")
    return 0 if verdict == "YES" else 1


if __name__ == "__main__":
    sys.exit(main())
