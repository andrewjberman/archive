#!/usr/bin/env python3
"""POSN_ASTTAX.TO-V4-1 V4-AC4 -- THE DIFFERENCE CONTROL: what changes when GLD is absent.

TWO ARMS, ONE RUN, ONE DIFFERENCE. Both arms call the SAME build() in the SAME process over
the SAME holdings.json and the SAME positioning_data.json. The only thing that differs is
the Bloomberg frame:

    ARM A  the REAL bbg/<asof>/characteristics.parquet, as V4-AC3 read it
    ARM B  a SCRATCH COPY of that parquet with GLD's ROW REMOVED, written to .scratch/ and
           read back through the same pd.read_parquet + P.bbg_index path, so arm B differs
           from arm A in its INPUT and in nothing else -- not in its code path, not in its
           clock, not in its other two inputs.

WHY A CONTROL AT ALL: the AC3 numbers are consistent with a producer that reads Bloomberg
AND with one that ignores it entirely, because 23 of the 25 satellite tickers resolve from
Yang. Removing GLD is the one input change that must MOVE something if the Bloomberg leg is
real, and must move NOTHING if it is not. If the two arms do not differ, this control is not
discriminating and that -- not the result -- is what gets reported.

THE LIVE BUCKET IS NEVER WRITTEN: neither arm calls publish(); the scratch parquet is a
LOCAL file under .scratch/ and nothing is put to s3://opal-data-etfs or anywhere else.

ASCII only.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    "..", "..", "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "data", "assets", "scripts", "gold"))
sys.path.insert(0, REPO)

import boto3  # noqa: E402
import pandas as pd  # noqa: E402
import build_satellites_characteristics as P  # noqa: E402

SUBJECT = "Opal Satellite 15"
TICKER = "GLD"


def coverage_rows(doc, code):
    """(field, aggregate, weight_with_value, weight_null) for every field of one satellite."""
    sat = doc["satellites"][code]
    cov_v, cov_n = sat["coverage"]["weight_with_value"], sat["coverage"]["weight_null"]
    rows = [(f, sat[f], cov_v[f], cov_n[f]) for f in P.SCALAR_FIELDS]
    rows += [("returns.%s" % w, sat["returns"][w], cov_v["returns"][w], cov_n["returns"][w])
             for w in sat["returns"]]
    return rows


def main() -> int:
    as_of = dt.datetime.now(dt.timezone.utc).date().isoformat()
    bbg_as_of = P.resolve_bbg_as_of()
    print("=" * 100)
    print("V4-AC4 DIFFERENCE CONTROL -- %s REMOVED from a SCRATCH copy of bbg/%s"
          % (TICKER, bbg_as_of))
    print("=" * 100)

    s3 = boto3.client("s3")
    holdings_doc = P.load_holdings(s3)
    positioning_doc = P.load_positioning(s3)
    frame, manifest = P.load_bbg(s3, bbg_as_of)

    # ---- ARM A: the real partition ---------------------------------------
    rows_a, collisions = P.bbg_index(frame)
    doc_a = P.build(holdings_doc, positioning_doc, rows_a, manifest, as_of, bbg_as_of,
                    bbg_collisions=collisions)

    # ---- ARM B: the scratch copy, GLD removed ----------------------------
    mask = frame["security"].astype(str).str.split().str[0].str.upper() == TICKER
    print("  real partition rows: %d   rows matching %s: %d"
          % (len(frame), TICKER, int(mask.sum())))
    if int(mask.sum()) == 0:
        print("  REFUSING: %s is not in the real partition, so removing it cannot discriminate."
              % TICKER)
        return 1
    scratch_dir = os.path.join(REPO, ".scratch")
    os.makedirs(scratch_dir, exist_ok=True)
    scratch_path = os.path.join(scratch_dir, "bbg_characteristics_no_%s.parquet" % TICKER)
    frame[~mask].reset_index(drop=True).to_parquet(scratch_path, index=False)
    frame_b = pd.read_parquet(scratch_path)
    print("  scratch copy:        %s   rows: %d (one row fewer, %s gone)"
          % (scratch_path, len(frame_b), TICKER))
    rows_b, collisions_b = P.bbg_index(frame_b)
    print("  %s in arm A index: %s   in arm B index: %s"
          % (TICKER, TICKER in rows_a, TICKER in rows_b))
    doc_b = P.build(holdings_doc, positioning_doc, rows_b, manifest, as_of, bbg_as_of,
                    bbg_collisions=collisions_b)

    # ---- the comparison ---------------------------------------------------
    gld_row = rows_a[TICKER]
    carried = [f for f in P.SCALAR_FIELDS if gld_row.get(f) is not None]
    not_carried = [f for f in P.SCALAR_FIELDS if gld_row.get(f) is None]
    print()
    print("WHAT THE REAL %s ROW CARRIES (measured, not assumed): %s" % (TICKER, carried or "NOTHING"))
    print("WHAT IT DOES NOT CARRY:                               %s"
          % (not_carried + ["returns.* (the pull has no return columns)"]))
    weight = None
    for holding in holdings_doc["satellites"][SUBJECT]["holdings"]:
        if holding["ticker"].upper() == TICKER:
            weight = holding["weight"]
    print("%s's %s weight in holdings.json: %s" % (SUBJECT, TICKER, weight))
    print()

    print("%s -- ARM A (real) vs ARM B (%s removed):" % (SUBJECT, TICKER))
    print("   %-14s %-26s %-26s %s" % ("field", "aggregate A -> B", "weight_null A -> B", "verdict"))
    moved_agg, moved_null, unchanged = [], [], []
    a_rows = {r[0]: r for r in coverage_rows(doc_a, SUBJECT)}
    b_rows = {r[0]: r for r in coverage_rows(doc_b, SUBJECT)}
    for field in a_rows:
        _, agg_a, wv_a, wn_a = a_rows[field]
        _, agg_b, wv_b, wn_b = b_rows[field]
        d_null = round(wn_b - wn_a, 4)
        agg_changed = (agg_a != agg_b)
        if agg_changed:
            moved_agg.append(field)
        if abs(d_null) > 1e-9:
            moved_null.append((field, d_null))
        if not agg_changed and abs(d_null) <= 1e-9:
            unchanged.append(field)
        print("   %-14s %-26s %-26s %s"
              % (field,
                 "%s -> %s" % (("NULL" if agg_a is None else "%.6f" % agg_a),
                               ("NULL" if agg_b is None else "%.6f" % agg_b)),
                 "%.4f -> %.4f (%+.4f)" % (wn_a, wn_b, d_null),
                 "MOVED" if (agg_changed or abs(d_null) > 1e-9) else "unchanged"))

    print()
    print("READINGS:")
    print("  fields whose AGGREGATE moved      : %s" % (moved_agg or "NONE"))
    print("  fields whose weight_null ROSE     : %s"
          % ([("%s %+0.2f" % (f, d)) for f, d in moved_null] or "NONE"))
    print("  fields that did NOT move          : %s" % unchanged)
    print("  the rise equals %s's weight (%.2f) on every field it carried: %s"
          % (TICKER, weight or 0.0,
             all(abs(d - (weight or 0.0)) < 0.005 for f, d in moved_null
                 if f in carried) and sorted(f for f, _ in moved_null) == sorted(carried)))
    print()

    # The OTHER satellites that hold GLD must move too; the ones that do not hold it must not.
    print("EVERY SATELLITE -- does the arm B fee aggregate move, and does it hold %s?" % TICKER)
    for code in doc_a["satellites"]:
        holds = TICKER in [h["ticker"].upper()
                           for h in holdings_doc["satellites"][code]["holdings"]]
        fee_a = doc_a["satellites"][code]["fee"]
        fee_b = doc_b["satellites"][code]["fee"]
        print("   %-20s holds %s: %-5s   fee %.6f -> %.6f   %s"
              % (code, TICKER, holds, fee_a, fee_b,
                 "MOVED" if fee_a != fee_b else "unchanged"))
    print()

    differ = (doc_a["satellites"] != doc_b["satellites"])
    print("THE TWO ARMS DIFFER: %s" % differ)
    if not differ:
        print("  THE CONTROL IS NOT DISCRIMINATING -- reporting that, not the result.")
        return 1

    # Arm A must still be where V4-AC3 left it.
    ac3_path = os.path.join(REPO, ".scratch", "characteristics_dry_run.json")
    if os.path.exists(ac3_path):
        with open(ac3_path, encoding="utf-8") as fh:
            ac3 = json.load(fh)
        same = all(ac3["satellites"][c]["coverage"] == doc_a["satellites"][c]["coverage"]
                   and ac3["satellites"][c]["fee"] == doc_a["satellites"][c]["fee"]
                   for c in ac3["satellites"])
        print("ARM A still equals the V4-AC3 run (coverage + fee, all 9 satellites): %s" % same)
    print("THE LIVE BUCKET WAS NEVER WRITTEN: no publish() call in either arm; the only file")
    print("this script created is %s" % scratch_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
