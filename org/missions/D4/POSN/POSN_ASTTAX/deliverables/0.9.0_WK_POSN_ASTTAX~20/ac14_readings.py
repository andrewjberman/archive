#!/usr/bin/env python3
"""POSN_ASTTAX.TO-V4-1 V4-AC14 -- THE JUDGMENT READINGS. NO VERDICT IS OFFERED HERE.

V4-AC14 is graded by 3.0.0_SA_CVO~Z at L9 and asks two questions:
  (1) is the null-share disclosure HONEST FOR A READER OF THE PAGE?
  (2) is the source precedence (Yang first, Bloomberg second) the right one for a ticker
      BOTH sources carry?

This script prints the measurements those questions need and stops there. It reads the
SERVED artifact (what a page would read) plus the two upstream inputs, and it computes the
counterfactuals -- the renormalised number the artifact does NOT publish, and the per-FIELD
precedence the producer does NOT implement -- so the grader can see the size of each choice
rather than argue it in the abstract.

ASCII only.
"""
from __future__ import annotations

import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    "..", "..", "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "data", "assets", "scripts", "gold"))
sys.path.insert(0, REPO)

import boto3  # noqa: E402
import build_satellites_characteristics as P  # noqa: E402

SERVED = os.path.join(REPO, ".scratch", "served_characteristics.json")


def main() -> int:
    with open(SERVED, encoding="utf-8") as fh:
        doc = json.load(fh)

    print("=" * 100)
    print("V4-AC14 READINGS -- recorded for L9. NO VERDICT IS OFFERED.")
    print("  subject: the SERVED artifact s3://opal-data-cot/platinum/satellites/characteristics.json")
    print("  as_of %s | inputs %s" % (doc["as_of"], json.dumps(doc["inputs"])))
    print("=" * 100)
    print()

    print("READING 1 -- WHAT A PAGE READER WOULD SEE: the published number, its covered")
    print("weight, and the number the SAME data would produce if it WERE renormalised.")
    print("(published = numerator/100; renormalised = numerator/weight_with_value. The")
    print("artifact publishes the first. Where coverage is high the two are close; where it")
    print("is low they are far apart, and THAT is the whole question.)")
    print()
    print("   %-20s %-9s %12s %12s %10s %10s" %
          ("satellite", "field", "published", "renormalised", "covered%", "null%"))
    for code in doc["satellites"]:
        sat = doc["satellites"][code]
        total = sat["total_weight"]
        for field in P.SCALAR_FIELDS:
            wv = sat["coverage"]["weight_with_value"][field]
            wn = sat["coverage"]["weight_null"][field]
            pub = sat[field]
            ren = (pub * 100.0 / wv) if (pub is not None and wv) else None
            print("   %-20s %-9s %12s %12s %9.2f%% %9.2f%%" %
                  (code, field,
                   "NULL" if pub is None else "%.6f" % pub,
                   "NULL" if ren is None else "%.6f" % ren,
                   100.0 * wv / total, 100.0 * wn / total))
    print()

    print("   THE SPREAD, worst first (published vs renormalised, scalar fields):")
    rows = []
    for code in doc["satellites"]:
        sat = doc["satellites"][code]
        total = sat["total_weight"]
        for field in P.SCALAR_FIELDS:
            wv = sat["coverage"]["weight_with_value"][field]
            pub = sat[field]
            if pub is None or not wv:
                continue
            ren = pub * 100.0 / wv
            rows.append((100.0 * wv / total, code, field, pub, ren))
    rows.sort()
    for cov, code, field, pub, ren in rows[:6]:
        print("     %-20s %-9s covered %6.2f%%   published %.6f   renormalised %.6f   ratio %.2fx"
              % (code, field, cov, pub, ren, (ren / pub) if pub else float("nan")))
    print()
    print("   THE RETURN WINDOWS' COVERAGE (one line per satellite, min across the 8 windows):")
    for code in doc["satellites"]:
        sat = doc["satellites"][code]
        total = sat["total_weight"]
        cov = {w: 100.0 * sat["coverage"]["weight_with_value"]["returns"][w] / total
               for w in sat["returns"]}
        lo = min(cov, key=lambda w: cov[w])
        print("     %-20s min %-4s %6.2f%% covered   (max %-4s %6.2f%%)"
              % (code, lo, cov[lo], max(cov, key=lambda w: cov[w]), max(cov.values())))
    print()
    print("   WHAT CARRIES THE NULL SHARE IN THE ARTIFACT: coverage.weight_null, per field,")
    print("   in the SAME object as the number, plus satellites.<code>.sources naming every")
    print("   ticker's resolved source and contributors naming the tickers that fed each")
    print("   aggregate. Nothing about the disclosure depends on a consumer computing it.")
    print()

    print("=" * 100)
    print("READING 2 -- THE TICKERS BOTH SOURCES CARRY, and what per-FIELD precedence")
    print("would have changed. The producer resolves precedence ONCE PER TICKER (the cell's")
    print("wording), so a ticker Yang carries takes Yang's nulls too.")
    print()
    s3 = boto3.client("s3")
    positioning = P.load_positioning(s3)
    frame, _ = P.load_bbg(s3, doc["inputs"]["bbg_as_of"])
    yang, _ = P.yang_index(positioning)
    bbg, _ = P.bbg_index(frame)
    holdings = P.load_holdings(s3)

    sat_tickers = {}
    for code in holdings["satellites"]:
        for row in holdings["satellites"][code]["holdings"]:
            sat_tickers.setdefault(row["ticker"].upper(), 0.0)
            sat_tickers[row["ticker"].upper()] += row["weight"]

    both = sorted(t for t in sat_tickers if t in yang and t in bbg)
    only_y = sorted(t for t in sat_tickers if t in yang and t not in bbg)
    only_b = sorted(t for t in sat_tickers if t not in yang and t in bbg)
    neither = sorted(t for t in sat_tickers if t not in yang and t not in bbg)
    print("   satellite tickers: %d total | BOTH sources %d | Yang only %d | Bloomberg only %d | NEITHER %d"
          % (len(sat_tickers), len(both), len(only_y), len(only_b), len(neither)))
    print("     BOTH:        %s" % both)
    print("     Bloomberg:   %s" % only_b)
    print("     NEITHER:     %s   (contributes its whole weight to weight_null on every field)"
          % neither)
    print()
    print("   FOR EVERY TICKER BOTH CARRY -- Yang's value (used) vs Bloomberg's (ignored):")
    would_fill = []
    for t in both:
        print("     %s" % t)
        for field in P.SCALAR_FIELDS:
            yv, bv = yang[t].get(field), bbg[t].get(field)
            note = ""
            if yv is None and bv is not None:
                note = "  <-- per-FIELD precedence WOULD FILL this null"
                would_fill.append((t, field, bv))
            elif yv is not None and bv is not None:
                note = "  (both present; delta %+.6g)" % (float(bv) - float(yv))
            print("       %-9s yang=%-22s bbg=%-22s%s"
                  % (field, "NULL" if yv is None else round(float(yv), 6),
                     "NULL" if bv is None else round(float(bv), 6), note))
        yr = yang[t].get("returns") or {}
        print("       returns   yang=%d window(s) populated   bbg=0 (the pull has no return columns)"
              % len([k for k, v in yr.items() if v is not None]))
    print()
    print("   (ticker, field) pairs a per-FIELD precedence would fill that are NULL today: %d"
          % len(would_fill))
    for t, field, bv in would_fill:
        weight = sat_tickers[t]
        print("     %-6s %-9s bbg=%s   total satellite weight carrying this ticker: %.2f"
              % (t, field, round(float(bv), 6), weight))
    print()
    print("   THE ONE MIXED-VENDOR CONSEQUENCE, stated as a measurement rather than a view:")
    print("   under per-FIELD precedence an aggregate could take some tickers' values from")
    print("   Yang and others' from Bloomberg IN THE SAME NUMBER. The artifact's sources map")
    print("   is per TICKER, so such a number could not be attributed field by field from the")
    print("   artifact alone.")
    print()
    print("NO VERDICT IS OFFERED. V4-AC14 is graded by 3.0.0_SA_CVO~Z at L9.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
