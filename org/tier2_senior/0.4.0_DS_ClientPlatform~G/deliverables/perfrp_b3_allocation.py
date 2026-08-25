"""PRF-b-3 -- ALLOCATION SNAPSHOT + DRIFT (ADVI_PERFRP TO-R1-DS, AC9).

AC9: Sum(class MV) == level MV at every level; drift(as-of, as-of) == 0.

Current-state per the CTO PRD-author ruling (@67448): allocation is NOT period-keyed
in v1. The snapshot carries its as-of on its face; period-over-period comparison
arrives on an OBSERVED-HISTORY trigger, never a date.

LEVEL TREE (contract LEVELS): relationship -> account -> class.
  allocation_of_parent = class MV / its ACCOUNT's MV
  allocation_of_total  = class MV / its RELATIONSHIP's MV
Rollup is BY JOIN and the additivity is asserted at every level, not assumed.

JOIN RULE, inherited from a-3 (@74e69270ce) and NOT re-derived here: positions join
dim_asset_classification ON CUSIP, never on the same-named `security_key`, because
the two security_key columns are different key spaces. Joining on the name reports
~92% of holdings unclassified.

ON THE STRENGTH OF drift(as-of, as-of) == 0, stated rather than oversold: this is a
DETERMINISM check, not a data-correctness one. It catches an unstable sort, a
non-deterministic groupby, or a float-accumulation bug in the drift function. It
CANNOT catch wrong classification or wrong market value -- comparing a snapshot to
itself is silent about whether the snapshot is right. It earns its place as a cheap
implementation guard and is reported as exactly that. (The a-2 lesson: an assertion
that cannot fail on the axis you care about must say which axis it does cover.)

EVIDENCE VINTAGE: live plane read 2026-08-25; source citations resolve at
23271aac6480f2ebd65a37247ae64dde4d68c199.
"""
from __future__ import annotations

import io

import boto3
import pyarrow.parquet as pq

BUCKET = "opal-data-49financial"
ASOF = "2026-08-21"
MV = "market_value_settled_unsettled"
TOL = 0.01  # one cent

s3 = boto3.client("s3")


def read(table, date, tier="canonical"):
    key = f"gold/advi/{tier}/{table}/date={date}/data.parquet"
    o = s3.get_object(Bucket=BUCKET, Key=key)
    return pq.read_table(io.BytesIO(o["Body"].read())).to_pandas(), f"s3://{BUCKET}/{key}"


def build_snapshot(pos, a07, rel):
    """The allocation snapshot. Pure over its inputs so it can be called twice."""
    p = pos.copy()
    p["_cusip"] = p["cusip"].astype("string")
    cls = a07.drop_duplicates(subset=["cusip"])[["cusip", "asset_class"]].copy()
    cls["_cusip"] = cls["cusip"].astype("string")
    j = p.merge(cls[["_cusip", "asset_class"]], on="_cusip", how="left")
    # residue is NAMED, never folded into a class (a-3 / AC4)
    j["asset_class"] = j["asset_class"].fillna("NO-CLASSIFICATION-ROW")
    r = rel.drop_duplicates(subset=["account_id"])[["account_id", "relationship_id"]]
    j = j.merge(r, on="account_id", how="left")
    j["relationship_id"] = j["relationship_id"].fillna("UNMAPPED-RELATIONSHIP")
    return j


def main() -> int:
    pos, pos_src = read("canonical_positions", ASOF)
    a07, a07_src = read("dim_asset_classification", ASOF, "dimensions")
    rel, rel_src = read("dim_relationship", ASOF, "dimensions")

    print("PRF-b-3 ALLOCATION SNAPSHOT + DRIFT -- ADVI_PERFRP TO-R1-DS (AC9)")
    print("as-of %s  (current-state per CTO 67448; NOT period-keyed in v1)" % ASOF)
    print("=" * 104)
    print("SOURCES (named objects):")
    for s in (pos_src, a07_src, rel_src):
        print("  %s" % s)
    print("JOIN: positions x a07 ON CUSIP (a-3 @74e69270ce); accounts x relationship ON account_id")

    j = build_snapshot(pos, a07, rel)

    total_mv = float(j[MV].fillna(0).sum())
    acct = j.groupby("account_id")[MV].sum()
    relmv = j.groupby("relationship_id")[MV].sum()
    by_ac = j.groupby(["account_id", "asset_class"])[MV].sum()
    by_rc = j.groupby(["relationship_id", "asset_class"])[MV].sum()

    print("\nLEVEL TREE")
    print("  relationships ......... %d" % j["relationship_id"].nunique())
    print("  accounts .............. %d" % j["account_id"].nunique())
    print("  classes ............... %d  %s"
          % (j["asset_class"].nunique(), sorted(j["asset_class"].unique())))
    print("  total MV .............. {:>20,.2f}".format(total_mv))

    print("\nAC9 PART 1 -- ADDITIVITY, asserted at EVERY level (not assumed)")
    a_sum = float(by_ac.groupby(level=0).sum().sum())
    r_sum = float(by_rc.groupby(level=0).sum().sum())
    checks = [
        ("Sum(class MV per account) == Sum(account MV)", a_sum, float(acct.sum())),
        ("Sum(class MV per relationship) == Sum(rel MV)", r_sum, float(relmv.sum())),
        ("Sum(account MV) == total MV", float(acct.sum()), total_mv),
        ("Sum(relationship MV) == total MV", float(relmv.sum()), total_mv),
    ]
    worst = 0.0
    for label, got, want in checks:
        d = abs(got - want)
        worst = max(worst, d)
        print("  {:<48} delta={:>14,.6f}  {}".format(label, d, "PASS" if d < TOL else "*** FAIL ***"))

    # per-account additivity, the strict form: every account individually
    per = by_ac.groupby(level=0).sum().subtract(acct, fill_value=0.0).abs()
    print("  per-account additivity: %d of %d accounts within one cent (worst %,.6f)"
          .replace(",.6f", ".6f") % (int((per < TOL).sum()), len(per), float(per.max())))

    print("\nAC9 PART 2 -- drift(as-of, as-of) == 0")
    j2 = build_snapshot(pos, a07, rel)          # recomputed independently
    s1 = j.groupby(["relationship_id", "asset_class"])[MV].sum().sort_index()
    s2 = j2.groupby(["relationship_id", "asset_class"])[MV].sum().sort_index()
    aligned = s1.index.equals(s2.index)
    drift = float((s1 - s2).abs().max()) if aligned else float("nan")
    print("  index aligned: %s" % aligned)
    print("  max |drift| over %d (relationship, class) cells: %.10f" % (len(s1), drift))
    print("  %s" % ("PASS" if aligned and drift < TOL else "*** FAIL ***"))
    print("  SCOPE: this is a DETERMINISM check. It catches an unstable sort or a")
    print("         non-deterministic groupby. It is SILENT about whether the snapshot")
    print("         is correct -- comparing a snapshot to itself cannot test that.")

    print("\nALLOCATION SHARES -- top relationships by MV")
    print("  {:<28} {:>18} {:>10}".format("relationship_id", "MV", "of total"))
    for rid, v in relmv.sort_values(ascending=False).head(5).items():
        print("  {:<28} {:>18,.2f} {:>9.4f}%".format(str(rid)[:28], float(v),
                                                     100 * float(v) / total_mv if total_mv else 0))

    print("\n  allocation_of_parent = class MV / account MV ; allocation_of_total = class MV / relationship MV")
    print("  worked example, largest relationship:")
    top = relmv.sort_values(ascending=False).index[0]
    sub = by_rc.loc[top]
    for k, v in sub.sort_values(ascending=False).items():
        print("     {:<24} {:>18,.2f}  of_total={:.4f}%".format(
            str(k), float(v), 100 * float(v) / float(relmv.loc[top]) if float(relmv.loc[top]) else 0))
    print("     {:<24} {:>18,.2f}  {}".format(
        "SUM", float(sub.sum()),
        "== relationship MV" if abs(float(sub.sum()) - float(relmv.loc[top])) < TOL else "*** MISMATCH ***"))

    print("\nDENOMINATORS")
    print("  positions rows ........................ %d" % len(pos))
    print("  accounts with NO relationship mapping . %d"
          % int((j["relationship_id"] == "UNMAPPED-RELATIONSHIP").sum()))
    print("  MV in NO-CLASSIFICATION-ROW residue ... {:,.2f}".format(
        float(j.loc[j["asset_class"] == "NO-CLASSIFICATION-ROW", MV].fillna(0).sum())))
    return 0 if worst < TOL else 1


if __name__ == "__main__":
    raise SystemExit(main())
