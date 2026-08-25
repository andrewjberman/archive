"""PRF-a-1 ADDENDUM -- SOURCE HISTORY COVERAGE (ADVI_PERFRP TO-R1-DS).

WHY THIS EXISTS: A CORRECTION TO MY OWN a-1 AUDIT
--------------------------------------------------
a-1 (@068ca0bebf) classified every plan column MAPPED or ABSENT and printed
N = M + K. That arithmetic is correct and unchanged. But "MAPPED" collapsed two
materially different situations, and the audit had no way to say which:

  MAPPED, FULL history  -- the source spans the whole SI window, so the column is
                           computable for QTD / YTD / 1Y / 3Y / SI alike.
  MAPPED, SHALLOW history-- the source exists and carries the column, but spans only
                           a handful of recent dates, so the column is computable for
                           a few days and for NO contract period.

Both read "MAPPED". A consumer reading a-1 alone would conclude a shallow-sourced
column is available for a 3Y window; it is not, and nothing in the audit said so.
That is the same defect shape this round keeps finding -- a statement that is TRUE
and does not carry what a consumer needs to act on it -- and here it was mine.

The remedy is not to reclassify anything as ABSENT. The columns ARE mapped; what was
missing is the COVERAGE dimension, which is what this addendum supplies. a-1's N/M/K
stands; this narrows what M entitles a consumer to claim.

MEASURED 2026-08-24, full partition listings, NOT sampled.
"""
from __future__ import annotations

import boto3

GOLD = "opal-data-49financial"
ASSETS = "opal-data-assets"

# (label, bucket, prefix, which a-1 mappings rest on it)
SOURCES = [
    ("canonical_valuation", GOLD, "gold/advi/canonical/canonical_valuation/",
     "bmv, emv, bmv_cash, emv_cash, bmv_accrual, emv_accrual, account_id, date"),
    ("flow_ledger", GOLD, "gold/advi/canonical/flow_ledger/",
     "all 8 external-flow columns, advisory_fee_billed, transaction_fee"),
    ("nna_canonical", GOLD, "gold/advi/canonical/nna_canonical/",
     "flow_classification_complete, nna headline"),
    ("twr_daily", GOLD, "gold/advi/canonical/twr_daily/",
     "daily_return_net/gross, daily_factor_*, return_eligible, flow_timing_basis"),
    ("dim_transaction", ASSETS, "schwab/08335338/silver/dim_transaction/",
     "income_total (via the imported core's resolver)"),
    ("canonical_positions", GOLD, "gold/advi/canonical/canonical_positions/",
     "PRF-a-3 classification coverage; PRF-b-3 allocation snapshot + drift"),
    ("dim_asset_classification", GOLD, "gold/advi/dimensions/dim_asset_classification/",
     "PRF-a-3 the classification axis itself"),
    ("valuation_integrity", GOLD, "gold/advi/canonical/valuation_integrity/",
     "recon_residual, recon_residual_pct_bmv, known_component_total, valuation_complete"),
    ("accrual_materiality", GOLD, "gold/advi/canonical/accrual_materiality/",
     "accrual diagnostics"),
    ("nna_atomic", GOLD, "gold/advi/canonical/nna_atomic/",
     "dormant-superseded by c01 (determination); not a live dependency"),
    ("dim_account", GOLD, "gold/advi/dimensions/dim_account/",
     "PRF-a-6 roster (a00 side); account identity"),
    ("dim_relationship", GOLD, "gold/advi/dimensions/dim_relationship/",
     "the relationship level of the level tree"),
    ("dim_account_xref", ASSETS, "blackdiamond/49f/silver/dim_account_xref/",
     "PRF-a-6 roster (xref side), known-not-held"),
]

# The contract's SI floor. A source must reach back to here to serve an SI window.
SI_FLOOR = "2024-07-08"
AS_OF = "2026-08-21"  # the measured frontier; periods are computed against it

# A source serves a period iff its FLOOR DATE reaches back to the period's START DATE.
# Counting partitions is the WRONG test and I shipped it once: a source can hold 250
# partitions all inside one month and serve no annual period at all. The comparison is
# floor-vs-start, never span-vs-threshold.
PERIOD_START = {
    "QTD": "2026-07-01",
    "YTD": "2026-01-01",
    "1Y": "2025-08-21",
    "3Y": "2023-08-21",
    "SI": SI_FLOOR,
}

s3 = boto3.client("s3")


def partitions(bucket, prefix):
    p = s3.get_paginator("list_objects_v2")
    out = set()
    for pg in p.paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
        for c in pg.get("CommonPrefixes", []) or []:
            seg = c["Prefix"].rstrip("/").split("/")[-1]
            if seg.startswith("date="):
                out.add(seg.split("=", 1)[1])
    return sorted(out)


def main() -> int:
    print("PRF-a-1 ADDENDUM -- SOURCE HISTORY COVERAGE")
    print("a-1's N=56 = M=46 + K=10 is UNCHANGED. This narrows what M entitles you to claim.")
    print("=" * 112)

    rows = []
    for label, bucket, prefix, used_by in SOURCES:
        ds = partitions(bucket, prefix)
        rows.append((label, ds, used_by))

    full, shallow = [], []
    print("%-26s %7s  %-12s %-12s  %s" % ("source", "parts", "floor", "frontier", "verdict"))
    print("-" * 112)
    for label, ds, _ in rows:
        if not ds:
            print("%-26s %7d  %-12s %-12s  %s" % (label, 0, "-", "-", "NO PARTITIONS"))
            continue
        reaches_si = ds[0] <= SI_FLOOR
        # twr_daily floors one trading day after the SI floor BY CONSTRUCTION: a first
        # return needs a prior-day BMV. That is not shallowness and must not read as it.
        by_construction = (label == "twr_daily" and ds[0] <= "2024-07-09")
        if reaches_si or by_construction:
            verdict = ("FULL (floors 1 trading day after SI BY CONSTRUCTION)"
                       if by_construction and not reaches_si else "FULL (reaches the SI floor)")
            reaches_si = True
        else:
            verdict = "*** SHALLOW ***"
        (full if reaches_si else shallow).append(label)
        print("%-26s %7d  %-12s %-12s  %s" % (label, len(ds), ds[0], ds[-1], verdict))

    print("\nDENOMINATOR: %d sources measured, ALL partitions listed (not sampled)." % len(rows))
    print("  FULL    %d -- %s" % (len(full), ", ".join(full)))
    print("  SHALLOW %d -- %s" % (len(shallow), ", ".join(shallow)))

    print("\n" + "=" * 112)
    print("WHAT THE SHALLOW SOURCES CARRY, i.e. what a consumer must NOT assume from a-1's 'MAPPED':")
    for label, ds, used_by in rows:
        if not ds or ds[0] <= SI_FLOOR or label == "twr_daily":
            continue
        span = len(ds)
        servable = [p for p, start in PERIOD_START.items() if ds[0] <= start]
        print("  %-26s %d partition(s) %s..%s" % (label, span, ds[0], ds[-1]))
        print("      feeds : %s" % used_by)
        print("      serves: %s" % (", ".join(servable) if servable else
                                    "NO contract period -- recent dates only"))

    print("\n" + "=" * 112)
    print("CONSEQUENCE FOR THE CONTRACT, stated as a fact and not a proposal:")
    print("  The contract offers PERIODS = QTD, YTD, 1Y, 3Y, SI, custom.")
    print("  Figures resting on a SHALLOW source are computable for NONE of them.")
    print("  This is NOT the declared-absent list (those columns have no source at all).")
    print("  It is a THIRD state: the column is sourced, and its HISTORY is not.")
    print("  Whether that is a defect or the expected state of a young table is NOT this")
    print("  audit's call -- it is measured here and routed to the issuer.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
