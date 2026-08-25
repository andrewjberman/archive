"""PRF-a-3 -- CLASSIFICATION COVERAGE (ADVI_PERFRP TO-R1-DS, AC4).

Prints positions MARKET VALUE total / classified / residue over
canonical_positions x dim_asset_classification, with THE RESIDUE NAMED and never
folded into a class.

Current-state per the CTO PRD-author ruling (@67448): the Allocation surface is
NOT period-keyed in v1, so coverage is measured at the newest partition with its
as-of carried, not over a window.

EVIDENCE VINTAGE: live plane read 2026-08-25; source citations resolve at
23271aac6480f2ebd65a37247ae64dde4d68c199 (verified clean vs HEAD before citing,
per the standing named-ref rule).

THE JOIN, AND WHY IT IS NOT THE OBVIOUS ONE
-------------------------------------------
Both tables carry a column called `security_key`. THEY ARE NOT THE SAME KEY SPACE,
and joining on the shared NAME is catastrophically wrong:

  a07  security_key = ticker.upper() if present, else cusip, else "NAME:"+normalized
       (a07_dim_asset_classification.py:248-252) -- TICKER-PREFERRING
  b01  security_key = A_03 dim_security's key, joined to positions ON CUSIP
       (b01_canonical_positions.py:11, :61)      -- a different derivation entirely

MEASURED both ways at date=2026-08-21:
  join on security_key ....  190 of 2,269 position keys matched  (8.4%)
  join on cusip ..........  2,269 of 2,270 matched               (99.96%)

The name-join would have reported ~92% of client holdings UNCLASSIFIED -- a
catastrophic false finding that reads as a data problem rather than a join bug, and
that a reviewer would plausibly believe. THE JOIN IS CUSIP, and it is grounded on the
producers' source above rather than chosen because it returns a nicer number.

NO EXISTING CONSUMER JOINS THESE TWO TABLES (comp-find over runners_49f: no
merge/join on dim_asset_classification). This join is established HERE, so the rule
is recorded here and carried into the b-1 contract rather than left as folklore.
"""
from __future__ import annotations

import io

import boto3
import pyarrow.parquet as pq

BUCKET = "opal-data-49financial"
ASOF = "2026-08-21"   # newest partition of BOTH inputs, measured

s3 = boto3.client("s3")


def read(table, date, tier="canonical"):
    key = f"gold/advi/{tier}/{table}/date={date}/data.parquet"
    o = s3.get_object(Bucket=BUCKET, Key=key)
    return pq.read_table(io.BytesIO(o["Body"].read())).to_pandas(), f"s3://{BUCKET}/{key}"


def main() -> int:
    pos, pos_key = read("canonical_positions", ASOF)
    a07, a07_key = read("dim_asset_classification", ASOF, "dimensions")

    print("PRF-a-3 CLASSIFICATION COVERAGE -- ADVI_PERFRP TO-R1-DS (AC4)")
    print("as-of %s  (current-state per CTO ruling 67448; NOT period-keyed in v1)" % ASOF)
    print("=" * 104)
    print("SOURCES (named objects, not 'the latest'):")
    print("  %s" % pos_key)
    print("  %s" % a07_key)
    print("JOIN: cusip  -- NOT security_key. See the module docstring; the two")
    print("      security_key columns are different key spaces built by different rules.")

    mv = "market_value_settled_unsettled"
    pos["_cusip"] = pos["cusip"].astype("string")
    a07["_cusip"] = a07["cusip"].astype("string")

    cls = a07.drop_duplicates(subset=["_cusip"])[["_cusip", "asset_class", "classification_source"]]
    j = pos.merge(cls, on="_cusip", how="left")

    total_rows = len(j)
    total_mv = float(j[mv].fillna(0).sum())

    # RESIDUE IS TWO DISTINCT THINGS and they must not be merged:
    #   NO-CLASSIFICATION-ROW : the cusip is absent from a07 entirely
    #   UNCLASSIFIED-LOUD     : a07 HAS the security and declares it unclassified
    # The first is a coverage gap; the second is a classification verdict. Folding
    # them would hide which one you are looking at, and they take different remedies.
    no_row = j["asset_class"].isna()
    loud = j["asset_class"].eq("UNCLASSIFIED-LOUD")
    classified = ~no_row & ~loud

    print("\nROW / VALUE COVERAGE")
    print("  %-34s %10s  %20s" % ("bucket", "rows", "market value"))
    print("  " + "-" * 68)
    for label, mask in (("CLASSIFIED", classified),
                        ("residue: UNCLASSIFIED-LOUD", loud),
                        ("residue: NO-CLASSIFICATION-ROW", no_row)):
        print("  {:<34} {:>10}  {:>20,.2f}".format(label, int(mask.sum()), float(j.loc[mask, mv].fillna(0).sum())))
    print("  " + "-" * 68)
    print("  {:<34} {:>10}  {:>20,.2f}".format("TOTAL", total_rows, total_mv))

    res_mv = float(j.loc[loud | no_row, mv].fillna(0).sum())
    cls_mv = float(j.loc[classified, mv].fillna(0).sum())
    print("\n  CHECK: classified + residue == total -> %s"
          % ("PASS" if abs((cls_mv + res_mv) - total_mv) < 0.01 else "FAIL"))
    if total_mv:
        print("  classified share of MV: %.4f%%" % (100 * cls_mv / total_mv))
        print("  residue    share of MV: %.4f%%" % (100 * res_mv / total_mv))

    print("\nCLASS MIX over CLASSIFIED rows (the Allocation card's content):")
    g = j[classified].groupby("asset_class")[mv].agg(["count", "sum"]).sort_values("sum", ascending=False)
    for k, r in g.iterrows():
        print("  {:<18} rows={:<8} mv={:>20,.2f}  ({:.4f}% of classified)".format(
            k, int(r["count"]), float(r["sum"]),
            100 * float(r["sum"]) / cls_mv if cls_mv else 0.0))

    print("\nRESIDUE IS NAMED, NEVER FOLDED (AC4):")
    print("  UNCLASSIFIED-LOUD ..... a07 HAS the security and declares it unclassified.")
    print("                          A classification verdict. Remedy: classify it.")
    print("  NO-CLASSIFICATION-ROW . the cusip is absent from a07 entirely.")
    print("                          A coverage gap. Remedy: extend the population.")
    print("  These are DIFFERENT STATES with DIFFERENT REMEDIES and are reported")
    print("  separately. Merging them into one 'unclassified' bucket would hide which.")

    print("\nDENOMINATORS")
    print("  canonical_positions rows ............ %d" % len(pos))
    print("  dim_asset_classification rows ....... %d" % len(a07))
    print("  distinct cusip in positions ......... %d" % pos["_cusip"].nunique(dropna=True))
    print("  distinct cusip in a07 ............... %d" % a07["_cusip"].nunique(dropna=True))
    print("  positions cusips absent from a07 .... %d"
          % len(set(pos["_cusip"].dropna()) - set(a07["_cusip"].dropna())))
    print("  positions rows with NULL cusip ...... %d" % int(pos["cusip"].isna().sum()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
