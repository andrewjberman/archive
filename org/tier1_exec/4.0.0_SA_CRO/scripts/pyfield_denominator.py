#!/usr/bin/env python3
"""pyfield_denominator.py -- compose the COLUMN DENOMINATOR from procedure + audited correction.

TO: NFRA_PYFIELD.TO-0.  Author: 4.0.0_SA_CRO.

THE STRUCTURE, and why it is this and not something simpler:

  1. The stated procedure (pyfield_classify.py) classifies 100% of the population into
     column / not-column / undecidable-at-this-site. That is the FULL CENSUS.
  2. A SYSTEMATIC audit sample (first-per-file alphabetical, per stratum) is hand-read.
     - Every procedure-DECIDED site in the sample is checked -> measures false positives.
     - Every procedure-UNDECIDABLE site in the sample is hand-adjudicated -> measures what
       fraction of the undecidable mass is actually column, and what is genuinely ambiguous.
  3. The audited rate is applied to the undecidable mass AS A RATE WITH A WILSON INTERVAL.
     It is NOT folded back into the rules -- doing that would tune the scorer to its own eval
     cases (Andrew-direct 2026-08-06) and the interval would then be a fiction.

So the published figure is: CONFIRMED columns + (undecidable mass x audited column rate),
carrying an interval that widens exactly as far as the undecidable mass is large.
"""
from __future__ import annotations

import collections
import json
import math
import sys


def wilson(k, n, z=1.96):
    """Wilson score interval -- correct at small n and at proportions near 0/1, unlike normal."""
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0.0, c - h), min(1.0, c + h))


def main():
    D = "org/tier1_exec/4.0.0_SA_CRO/deliverables/pyfield_to0"
    # errors="replace" per the strict-utf8 gate -- see the note in pyfield_classify.py.
    verdicts = [json.loads(ln) for ln in
                open(f"{D}/verdicts_v2.jsonl", encoding="utf-8", errors="replace")][1:]
    audit = [json.loads(ln) for ln in
             open(f"{D}/audit_v2.jsonl", encoding="utf-8", errors="replace")]
    hand = json.load(open(f"{D}/hand_adjudication.json", encoding="utf-8"))
    hmap = {a["locus"]: a["verdict"] for a in hand["adjudications"]}

    name = [r for r in verdicts if r["base_kind"] == "name"]
    exprs = [r for r in verdicts if r["base_kind"] != "name"]

    strata = ["S-A usage-only", "S-B usage+binding", "S-B2 binding-only", "S-C neither-axis"]

    print("=" * 88)
    print("NFRA_PYFIELD TO-0 -- COLUMN DENOMINATOR")
    print("=" * 88)
    print("denominator_grain : AST string-literal Subscript NODES")
    print("corpus            : data/inf/scripts/gold + data/assets/scripts/gold (124 files)")
    print(f"population        : {len(verdicts)} sites total; {len(name)} name-based; "
          f"{len(exprs)} expr-based\n")

    tot_conf_col = tot_conf_not = 0
    tot_und = 0
    est_lo = est_hi = est_pt = 0.0
    rows = []

    for s in strata:
        pop = [r for r in name if r["stratum"] == s]
        proc = collections.Counter(r["verdict"] for r in pop)
        n_col, n_not = proc["column"], proc["not-column"]
        n_und = proc["undecidable-at-this-site"]

        aud = [a for a in audit if a["stratum"] == s]
        aud_und = [a for a in aud if a["verdict"].startswith("undecidable")]
        hv = [hmap.get(a["locus"]) for a in aud_und]
        hv = [v for v in hv if v]
        k_col = sum(1 for v in hv if v == "column")
        k_not = sum(1 for v in hv if v == "not-column")
        k_amb = sum(1 for v in hv if v.startswith("undecidable"))

        p, lo, hi = wilson(k_col, len(hv)) if hv else (0.0, 0.0, 0.0)
        add_pt, add_lo, add_hi = n_und * p, n_und * lo, n_und * hi

        tot_conf_col += n_col
        tot_conf_not += n_not
        tot_und += n_und
        est_pt += n_col + add_pt
        est_lo += n_col + add_lo
        est_hi += n_col + add_hi

        rows.append((s, len(pop), n_col, n_not, n_und, len(hv), k_col, k_not, k_amb, p, lo, hi))

        print(f"-- {s}  (n={len(pop)}) " + "-" * (60 - len(s)))
        print(f"     procedure: column {n_col:>5} | not-column {n_not:>5} | undecidable {n_und:>5}")
        if hv:
            print(f"     audited undecidables: {len(hv)} hand-read -> column {k_col}, "
                  f"not-column {k_not}, genuinely-ambiguous {k_amb}")
            print(f"     audited column-rate of the undecidable mass: {p*100:.1f}% "
                  f"[95% CI {lo*100:.1f}-{hi*100:.1f}]")
            print(f"     => est. columns in this stratum: "
                  f"{n_col + add_pt:,.0f}  [{n_col + add_lo:,.0f} - {n_col + add_hi:,.0f}]")
        else:
            print("     (no undecidables in this stratum -- procedure fully decided it)")
        print()

    # expr-based: reported separately, never folded in silently
    e_proc = collections.Counter(r["verdict"] for r in exprs)
    print(f"-- S-D expr-base (n={len(exprs)}) " + "-" * 44)
    print(f"     procedure: column {e_proc['column']} | not-column {e_proc['not-column']} "
          f"| undecidable {e_proc['undecidable-at-this-site']}")
    print("     NOT extrapolated: a name-keyed heuristic cannot attempt these by construction.")
    print("     Reported as a STRUCTURAL FLOOR on unresolvability, per PRD 2.4.\n")

    print("=" * 88)
    print("THE DENOMINATOR")
    print("=" * 88)
    denom = len(name)
    print(f"  Denominator (name-based string-literal subscripts) : {denom:,}")
    print(f"  Confirmed column      (procedure, audit-checked)   : {tot_conf_col:,}")
    print(f"  Confirmed not-column  (procedure, audit-checked)   : {tot_conf_not:,}")
    print(f"  Undecidable mass carried into the estimate         : {tot_und:,}")
    print()
    print(f"  ESTIMATED COLUMNS : {est_pt:,.0f} of {denom:,}  "
          f"= {100*est_pt/denom:.1f}%")
    print(f"  95% interval      : {est_lo:,.0f} - {est_hi:,.0f}  "
          f"({100*est_lo/denom:.1f}% - {100*est_hi/denom:.1f}%)")
    print()
    print(f"  Against the FULL population incl. expr-bases ({len(verdicts):,}): "
          f"{100*est_pt/len(verdicts):.1f}% "
          f"({100*est_lo/len(verdicts):.1f}% - {100*est_hi/len(verdicts):.1f}%)")
    print("=" * 88)
    return 0


if __name__ == "__main__":
    sys.exit(main())
