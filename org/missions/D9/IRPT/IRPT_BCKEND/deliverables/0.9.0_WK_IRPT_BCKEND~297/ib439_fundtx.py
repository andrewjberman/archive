#!/usr/bin/env python3
"""IB-pr-439 item 4: COUNTS of fund-dates carrying a priced custodian purchase or redemption.  Read only (S3 list + get); no account column is read;
no transaction price is compared with any bar.  Writes one counts-only json.

    python -I ib439_fundtx.py <out.json> <graded_days.json>

Table: the silver transactions table beside the holdings table (prefix = the holdings prefix's parent + 'fact_transactions/'); every date partition is read and
rows are de-duplicated on TransactionID.  A 'fund' = one of the nine funds of IB-pr-436 (no instrument-type field exists in the holdings source), by CUSIP.
A transaction counts as a PURCHASE or REDEMPTION when Transaction Type is Buy or Sale (Sub Type Buy / Sale / Redemption), with Price > 0.
"""
import io
import json
import sys
from collections import Counter
import boto3
import pyarrow.parquet as pq
from botocore.config import Config

BUCKET = "opal-data-assets"
HOLD_PARENT = sys.argv[3]            # '<source>/<scope>/silver/' (from the instrument's resolver, passed in so no scope literal is typed here)
PREFIX = HOLD_PARENT + "fact_transactions/"
FUNDS = {"31635V679": "FLCOX", "552985863": "MFEIX", "149498107": "CEMIX", "316146315": "FSGGX", "315911743": "FSMAX", "316146356": "FXNAX",
         "31635V729": "FSPGX", "13161T401": "CDSIX", "30254T643": "FPNIX"}
COLS = ["TransactionID", "Transaction Type", "Transaction Sub Type", "Trade Date", "Price", "CUSIP", "Ticker", "Units", "Share Class Type", "SEC Asset Type"]


def main():
    out, graded = sys.argv[1], set(json.load(open(sys.argv[2])))
    s3 = boto3.client("s3", region_name="us-east-1", config=Config(retries={"max_attempts": 8, "mode": "standard"}, read_timeout=120))
    parts = []
    tok = None
    while True:
        kw = dict(Bucket=BUCKET, Prefix=PREFIX, Delimiter="/")
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        parts += [p["Prefix"] for p in r.get("CommonPrefixes", [])]
        tok = r.get("NextContinuationToken")
        if not tok:
            break
    seen, rows_total, dup = {}, 0, 0
    absent_cols = Counter()
    ncols_objs = 0
    for p in parts:
        r = s3.list_objects_v2(Bucket=BUCKET, Prefix=p)
        for o in r.get("Contents", []):
            if not o["Key"].endswith(".parquet"):
                continue
            buf = io.BytesIO(s3.get_object(Bucket=BUCKET, Key=o["Key"])["Body"].read())
            have = set(pq.read_schema(buf).names)
            for c in COLS:
                if c not in have:
                    absent_cols[c] += 1
            ncols_objs += 1
            t = pq.read_table(buf, columns=[c for c in COLS if c in have]).to_pydict()
            n = len(t["TransactionID"])
            rows_total += n
            for i in range(n):
                k = t["TransactionID"][i]
                if k in seen:
                    dup += 1
                    continue
                seen[k] = {c: (t[c][i] if c in t else None) for c in COLS}
    import datetime as dt

    def iso(s):
        try:
            return dt.datetime.strptime(str(s).strip(), "%m/%d/%Y").date().isoformat()
        except Exception:
            return None
    parts_dates = sorted(p.rstrip("/").split("date=")[1] for p in parts)
    tdates = [iso(v["Trade Date"]) for v in seen.values()]
    tdates_ok = [d for d in tdates if d]
    pair, pair_in, fundset, fundset_in = set(), set(), set(), set()
    kinds = Counter()
    ticker_only = set()
    wide_pairs, wide_pairs_in = set(), set()
    reinv_pairs = set()
    for v in seen.values():
        d = iso(v["Trade Date"])
        cu = (v["CUSIP"] or "").strip()
        ty, sub = v["Transaction Type"], v["Transaction Sub Type"]
        pr = v["Price"]
        priced = pr is not None and pr == pr and pr > 0
        if cu in FUNDS:
            kinds[(ty, sub, "priced" if priced else "no_price")] += 1
            if ty in ("Buy", "Sale") and priced and d:
                pair.add((cu, d))
                fundset.add(cu)
                if d in graded:
                    pair_in.add((cu, d))
                    fundset_in.add(cu)
            if ty == "Dividend Reinvestment" and priced and d:
                reinv_pairs.add((cu, d))
        elif (v["Ticker"] or "").strip() in FUNDS.values():
            ticker_only.add((v["Ticker"], cu))
        # REFERENCE ONLY, not a type used in this cell: any security the table's own 'Share Class Type' marks other than ETF/Not Available,
        # under the table's 'SEC Asset Type' of registered investment companies
        if (v["SEC Asset Type"] or "").startswith("Securities Issued by Registered Investment") and (v["Share Class Type"] or "") not in ("ETF", "Not Available") \
                and ty in ("Buy", "Sale") and priced and d and cu:
            wide_pairs.add((cu, d))
            if d in graded:
                wide_pairs_in.add((cu, d))
    res = {
        "table": PREFIX.replace(HOLD_PARENT, "<holdings prefix parent>"),
        "date_partitions": len(parts_dates), "first_partition_date": parts_dates[0], "last_partition_date": parts_dates[-1], "objects_read": ncols_objs,
        "rows_read": rows_total, "distinct_transaction_ids": len(seen), "duplicate_rows_dropped": dup,
        "first_trade_date": min(tdates_ok), "last_trade_date": max(tdates_ok), "rows_with_unparseable_trade_date": len(tdates) - len(tdates_ok),
        "columns_absent_in_objects": dict(absent_cols),
        "fund_dates_with_a_priced_purchase_or_redemption": len(pair), "funds": len(fundset), "of_which_inside_the_85_days": len(pair_in),
        "funds_inside_the_85_days": len(fundset_in),
        "nine_funds_rows_by_type_subtype_price": {"%s|%s|%s" % k: v for k, v in sorted(kinds.items())},
        "dividend_reinvestment_fund_dates_priced_not_counted": len(reinv_pairs),
        "ticker_matches_with_other_cusip": sorted("%s/%s" % x for x in ticker_only)[:20],
        "reference_only_wider_basis": {"basis": "any security whose SEC Asset Type is registered-investment-company and whose Share Class Type is neither ETF nor Not Available; Buy or Sale with Price > 0; NOT a type used in this cell",
                                       "fund_dates": len(wide_pairs), "funds": len({c for c, _ in wide_pairs}), "fund_dates_inside_the_85_days": len(wide_pairs_in),
                                       "funds_inside_the_85_days": len({c for c, _ in wide_pairs_in})},
    }
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
