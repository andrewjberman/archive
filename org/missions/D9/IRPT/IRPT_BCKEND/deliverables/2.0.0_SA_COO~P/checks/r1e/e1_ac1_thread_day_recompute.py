"""~E round 1 AC1 -- the thread account's gold daily return equals an independent recompute from the declared silver.

Usage: python e1_ac1_thread_day_recompute.py [day, default 2026-09-25]
PRD ADDENDUM v0.19 rulings 2-4 (Andrew-direct call 3): the day-t return of an account is
    sum over included holdings of v_i(t-1) * r_i(t)  /  (sum over included holdings of v_i(t-1) + cash(t-1))
where v_i is the holding's end-of-day market value (a cusip's lots summed), r_i = price(t) / price(t-1) - 1 on a
positive price both days, cash is the declared cash balance with a zero return, and a holding without a positive price
on both days is EXCLUDED (the account row carries excluded_count). No inflow/outflow term.
Sources: the declaration data/assets/scripts/gold/irpt_holdings_performance/sources.json (49financial entry: bucket,
positions prefix, balance prefix, cash columns); the gold at lib/opal_naming address("irpt", "49financial", "gold",
"holdings_performance_daily", "date=<day>") with columns account_id, business_date, daily_return, account_value,
excluded_count, excluded_weight.
Pass: the gold row for the thread account exists and its daily_return is within 1e-9 of the recompute, and its
excluded_count equals the recompute's.
"""
import io
import json
import sys
from pathlib import Path

import boto3
import pandas as pd

ROOT = Path(__file__).resolve().parents[9]
sys.path.insert(0, str(ROOT / "lib"))
import opal_naming  # noqa: E402
import trading_calendar  # noqa: E402

THREAD = "0010498003"
DAY = sys.argv[1] if len(sys.argv) > 1 else "2026-09-25"
DECL = ROOT / "data/assets/scripts/gold/irpt_holdings_performance/sources.json"
s3 = boto3.client("s3")
ok = True


def parquet(bucket, prefix):
    keys = [o["Key"] for o in s3.list_objects_v2(Bucket=bucket, Prefix=prefix).get("Contents", []) if o["Key"].endswith(".parquet")]
    if not keys:
        return None
    return pd.concat([pd.read_parquet(io.BytesIO(s3.get_object(Bucket=bucket, Key=k)["Body"].read())) for k in keys])


def split(uri):
    bucket, _, key = uri[len("s3://"):].partition("/")
    return bucket, key.rstrip("/") + "/"


if not DECL.is_file():
    print("FAIL: no source declaration at %s" % DECL.relative_to(ROOT))
    ok = False
else:
    src = json.loads(DECL.read_text(encoding="utf-8"))["49financial"]
    prev = str(trading_calendar.prev_trading_day(pd.Timestamp(DAY).date()))
    pos = {d: parquet(src["bucket"], "%sdate=%s/" % (src["positions_prefix"], d)) for d in (prev, DAY)}
    bal = parquet(src["bucket"], "%sdate=%s/" % (src["balance_prefix"], prev))
    p0 = pos[prev][pos[prev]["account_id"].astype(str) == THREAD].groupby("cusip").agg(
        v=("market_value_settled_unsettled", "sum"), p=("closing_price", "first"))
    p1 = pos[DAY][pos[DAY]["account_id"].astype(str) == THREAD].groupby("cusip")["closing_price"].first()
    b = bal[bal["account_id"].astype(str) == THREAD]
    cash = float(sum(float(b[c].fillna(0.0).sum()) for c in src["cash_columns"]))
    num, den, excluded = 0.0, cash, 0
    for cusip, row in p0.iterrows():
        pt = float(p1.get(cusip, 0.0) or 0.0)
        if float(row["p"] or 0.0) > 0 and pt > 0:
            num += float(row["v"]) * (pt / float(row["p"]) - 1.0)
            den += float(row["v"])
        else:
            excluded += 1
    expect = num / den if den > 0 else None
    bucket, key = split(opal_naming.address("irpt", "49financial", "gold", "holdings_performance_daily", "date=%s" % DAY))
    gold = parquet(bucket, key)
    row = None if gold is None else gold[gold["account_id"].astype(str) == THREAD]
    if row is None or len(row) != 1:
        print("FAIL: gold %s holds %s row(s) for the thread account" % (key, 0 if row is None else len(row)))
        ok = False
    else:
        got, gx = float(row["daily_return"].iloc[0]), int(row["excluded_count"].iloc[0])
        print("recompute %.12f (excluded %d) | gold %.12f (excluded %d)" % (expect, excluded, got, gx))
        ok = expect is not None and abs(got - expect) <= 1e-9 and gx == excluded
if ok:
    print("E1-AC1 PASS")
else:
    print("E1-AC1 FAIL")
sys.exit(0 if ok else 1)
