"""PRF-a-4 + PRF-b-4 -- GAIN/LOSS (ADVI_PERFRP TO-R1-DS, AC5). DELIVERED LAST (s.11 #5).

AC5: the six-table census printed BEFORE the lots projection; the lots->positions
tie-out with its residual printed; Gain/Loss delivered LAST.

The ordering is the criterion, not decoration, and this run is why. The census is what
revealed that two of the four unrealized tables are the SAME HOLDINGS AT A COARSER
GRAIN -- a fact that turns a naive four-table sum into a 99.76% residual.

THE GRAIN FINDING, measured then VERIFIED rather than inferred from a naming pattern
-------------------------------------------------------------------------------------
  fact_uln  290,101 rows  sum(current_market_value)   760,207,285.09   LOT grain
  fact_upn   62,515 rows                              760,207,284.93   POSITION grain
  fact_ult  209,951 rows                            1,016,098,392.27   LOT grain
  fact_upt   40,218 rows                            1,016,098,392.07   POSITION grain
The pairs agree to $0.16 and $0.20, and share 62,512 / 40,209 (account, cusip) keys.

VERIFIED, not assumed: aggregating fact_uln's lots to (account, cusip) reproduces
fact_upn to within one cent on 62,511 OF 62,512 KEYS. So upn IS uln at position grain.
(One key differs by $158,434.85 -- a single outlier, reported and NOT chased; it is
one key in 62,512 and does not move the tie-out.)

SUMMING ALL FOUR DOUBLE-COUNTS THE ENTIRE BOOK. My first tie-out did exactly that and
produced a residual of 99.7640% -- a number that reads as a catastrophic data failure
and is entirely an artifact of adding two grains together. I caught it because the
residual was absurd and because I ran the overlap check, not because the sum looked
wrong: 3.55bn against a 1.78bn book is exactly 2x, and 2x is what a duplicated
universe looks like.

CORRECTED TIE-OUT, lot grain only:
  lots (uln + ult)     1,776,305,677.36   500,052 lot rows
  canonical_positions  1,778,404,303.12   102,905 position rows
  RESIDUAL                -2,098,625.76   -0.1180% of positions

EVIDENCE VINTAGE: live plane read 2026-08-25; citations resolve at
23271aac6480f2ebd65a37247ae64dde4d68c199.
"""
from __future__ import annotations

import datetime as dt
import io

import boto3
import pyarrow.parquet as pq

ASSETS = "opal-data-assets"
GOLD = "opal-data-49financial"
SILVER = "schwab/08335338/silver/"
ASOF = "2026-08-21"

SIX_TABLES = ("fact_uln", "fact_ult", "fact_upn", "fact_upt", "fact_rld", "fact_trn")
LOT_GRAIN = ("fact_uln", "fact_ult")          # the unrealized LOT tables
POSITION_GRAIN = ("fact_upn", "fact_upt")     # the SAME holdings, aggregated
REALIZED = "fact_rld"

s3 = boto3.client("s3")


def _read(bucket, prefix, date):
    r = s3.list_objects_v2(Bucket=bucket, Prefix="%sdate=%s/" % (prefix, date))
    keys = [o["Key"] for o in r.get("Contents", []) if o["Key"].endswith(".parquet")]
    o = s3.get_object(Bucket=bucket, Key=keys[0])
    return pq.read_table(io.BytesIO(o["Body"].read())).to_pandas(), keys[0]


def _partitions(bucket, prefix):
    p = s3.get_paginator("list_objects_v2")
    out = set()
    for pg in p.paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
        for c in pg.get("CommonPrefixes", []) or []:
            seg = c["Prefix"].rstrip("/").split("/")[-1]
            if seg.startswith("date="):
                out.add(seg.split("=", 1)[1])
    return sorted(out)


def main() -> int:
    print("PRF-a-4 + PRF-b-4 GAIN/LOSS -- ADVI_PERFRP TO-R1-DS (AC5)")
    print("as-of %s  |  DELIVERED LAST per s.11 #5, CENSUS FIRST" % ASOF)
    print("=" * 108)

    # ---------- 1. THE CENSUS, FIRST ----------
    print("\n1. SIX-TABLE CENSUS (printed BEFORE any projection -- this is the ordering AC5 requires)")
    print("   %-10s %10s  %-24s %10s %6s" % ("table", "partitions", "range", "rows@asof", "cols"))
    frames = {}
    for t in SIX_TABLES:
        ds = _partitions(ASSETS, SILVER + t + "/")
        df, key = _read(ASSETS, SILVER + t + "/", ASOF)
        frames[t] = df
        print("   %-10s %10d  %-24s %10d %6d"
              % (t, len(ds), "%s..%s" % (ds[0], ds[-1]), len(df), len(df.columns)))
    print("   NOTE: fact_rld runs DEEPER than the other five (floor 2023-07-12 vs 2024-07-08).")

    # ---------- 2. THE GRAIN FINDING ----------
    print("\n2. GRAIN -- the census's real output, and the reason the ordering matters")
    for t in LOT_GRAIN + POSITION_GRAIN:
        mv = float(frames[t]["current_market_value"].fillna(0).sum())
        grain = "LOT" if t in LOT_GRAIN else "POSITION (same holdings, aggregated)"
        print("   {:<10} rows={:<8} sum(current_market_value)={:>18,.2f}   {}".format(
            t, len(frames[t]), mv, grain))
    uln, upn = frames["fact_uln"], frames["fact_upn"]
    g = uln.groupby([uln["account_id"].astype(str), uln["cusip"].astype(str)])[
        "current_market_value"].sum()
    p = upn.set_index([upn["account_id"].astype(str), upn["cusip"].astype(str)])[
        "current_market_value"]
    common = g.index.intersection(p.index)
    d = (g.loc[common] - p.loc[common]).abs()
    print("   VERIFIED (not inferred from the naming): aggregating uln lots to (account,cusip)")
    print("   reproduces upn within one cent on {} of {} keys; max delta {:,.2f}".format(
        int((d < 0.01).sum()), len(common), float(d.max())))
    print("   -> SUMMING ALL FOUR DOUBLE-COUNTS THE BOOK. Lot grain only, below.")

    # ---------- 3. THE TIE-OUT ----------
    print("\n3. LOTS -> POSITIONS TIE-OUT, with the residual printed (AC5)")
    lots_mv = sum(float(frames[t]["current_market_value"].fillna(0).sum()) for t in LOT_GRAIN)
    lot_rows = sum(len(frames[t]) for t in LOT_GRAIN)
    pos, pos_key = _read(GOLD, "gold/advi/canonical/canonical_positions/", ASOF)
    pos_mv = float(pos["market_value_settled_unsettled"].fillna(0).sum())
    resid = lots_mv - pos_mv
    print("   lots (uln + ult)          {:>20,.2f}   rows={}".format(lots_mv, lot_rows))
    print("   canonical_positions       {:>20,.2f}   rows={}".format(pos_mv, len(pos)))
    print("   RESIDUAL                  {:>20,.2f}   {:.4f}% of positions"
          .format(resid, 100 * resid / pos_mv if pos_mv else 0.0))
    print("   The residual is REPORTED, not explained away. It is not chased here:")
    print("   attributing it needs the position-without-lots population, which is a")
    print("   different question from the one AC5 asks.")

    # ---------- 4. THE LOTS PROJECTION ----------
    print("\n4. LOTS PROJECTION -- unrealized ST/LT, realized, cost basis")
    asof_d = dt.date.fromisoformat(ASOF)
    tot = {"st_mv": 0.0, "lt_mv": 0.0, "st_gl": 0.0, "lt_gl": 0.0,
           "st_n": 0, "lt_n": 0, "undet_n": 0, "undet_mv": 0.0, "cost": 0.0}
    for t in LOT_GRAIN:
        df = frames[t]
        acq = df.get("acquired_date")
        for i in range(len(df)):
            mv = float(df["current_market_value"].iloc[i] or 0.0)
            gl = float(df["unrealized_gain_loss"].iloc[i] or 0.0)
            cb = float(df["cost_basis_unamortized"].iloc[i] or 0.0)
            tot["cost"] += cb
            a = acq.iloc[i] if acq is not None else None
            held_lt = None
            if a is not None and str(a) not in ("", "NaT", "None"):
                try:
                    ad = a.date() if hasattr(a, "date") else dt.date.fromisoformat(str(a)[:10])
                    held_lt = (asof_d - ad).days > 365
                except Exception:
                    held_lt = None
            if held_lt is True:
                tot["lt_mv"] += mv
                tot["lt_gl"] += gl
                tot["lt_n"] += 1
            elif held_lt is False:
                tot["st_mv"] += mv
                tot["st_gl"] += gl
                tot["st_n"] += 1
            else:
                tot["undet_mv"] += mv
                tot["undet_n"] += 1
    print("   UNREALIZED, split by holding period (acquired_date vs as-of, >365d = LT):")
    print("     LONG-TERM    lots={:<8} mv={:>18,.2f}  unrealized_gain_loss={:>16,.2f}"
          .format(tot["lt_n"], tot["lt_mv"], tot["lt_gl"]))
    print("     SHORT-TERM   lots={:<8} mv={:>18,.2f}  unrealized_gain_loss={:>16,.2f}"
          .format(tot["st_n"], tot["st_mv"], tot["st_gl"]))
    print("     UNDETERMINED lots={:<8} mv={:>18,.2f}  (no usable acquired_date -- NAMED,"
          " never folded into ST)".format(tot["undet_n"], tot["undet_mv"]))
    print("     cost basis (unamortized) {:>18,.2f}".format(tot["cost"]))
    chk = tot["lt_mv"] + tot["st_mv"] + tot["undet_mv"]
    print("     CHECK lt+st+undetermined == lots total: {} (delta {:,.2f})"
          .format("PASS" if abs(chk - lots_mv) < 0.01 else "FAIL", chk - lots_mv))

    # INDEPENDENT TIE: does the reported unrealized_gain_loss equal MV - cost basis?
    # Checked against the UNAMORTIZED column because that is the one summed above.
    implied = lots_mv - tot["cost"]
    reported = tot["lt_gl"] + tot["st_gl"]
    print("     TIE: reported unrealized_gain_loss {:>16,.2f}".format(reported))
    print("          MV - cost_basis_unamortized   {:>16,.2f}".format(implied))
    print("          delta                         {:>16,.2f}  ({:.4f}% of the gain)"
          .format(reported - implied,
                  100 * (reported - implied) / reported if reported else 0.0))
    print("          THEY DO NOT TIE EXACTLY, and that is REPORTED rather than rounded away:")
    print("          the lot tables carry FOUR basis columns (cost_basis_unamortized,")
    print("          adjusted_cost_basis_amortized, original_cost_basis,")
    print("          adjusted_cost_incldg_unpd_amort). The reported gain is evidently not")
    print("          computed against the unamortized one. WHICH basis the served Gain/Loss")
    print("          card must use is a METHOD question, not a lookup -- it is s.11 #13")
    print("          territory (DS-authored, CTO-ruled, CVO-certified) and is NOT decided here.")

    rld, _ = _read(ASSETS, SILVER + REALIZED + "/", ASOF)
    print("   REALIZED (fact_rld, as-of partition only -- NOT a period aggregation):")
    print("     rows={:<8} proceeds={:>18,.2f}  gain_loss_dollars={:>16,.2f}"
          .format(len(rld), float(rld["proceeds"].fillna(0).sum()),
                  float(rld["gain_loss_dollars"].fillna(0).sum())))
    print("     A windowed realized figure is a SUM OVER PARTITIONS IN THE WINDOW and is")
    print("     not computed here; this is the as-of day, stated so it is not misread.")

    print("\n" + "=" * 108)
    print("DENOMINATORS: 6 tables censused; %d lot rows; %d position rows; residual %.4f%%"
          % (lot_rows, len(pos), 100 * resid / pos_mv if pos_mv else 0.0))
    print("ST/LT undetermined: %d lots -- fact_upn/fact_upt carry NO acquired_date at all,"
          % tot["undet_n"])
    print("  so a projection built on the POSITION-grain tables could not split ST/LT at all.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
