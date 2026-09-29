"""~E round 3 AC4 -- the 49F gold re-emitted under PRD v0.20 rulings 13-17 (row S195; 4.0.0_SA_CRO half @eca8083ad2
section 6): no implausible day is served and every day's manifest is complete.

Usage: python e3_ac4_49f_reemit_v020.py [end day, default 2026-09-25]
Over EVERY 49F gold partition 2024-07-09..<end> (address("irpt", "49financial", "gold", "holdings_performance_daily" |
"holdings_performance_manifest", "date=<d>")): (1) 0 rows with status OK and daily_return <= -1 or >= 1 (ruling 16);
(2) the daily table carries a `leveraged` column (ruling 15); (3) every day's manifest carries
accounts_with_prior_holdings, computable_count, not_computable_count and complete, and complete is true (ruling 17).
The census of OK rows with |daily_return| > 0.5 is printed beside the result (the CRO's before/after census).
"""
import io
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
import pandas as pd

ROOT = Path(__file__).resolve().parents[9]
sys.path.insert(0, str(ROOT / "lib"))
import opal_naming  # noqa: E402
import trading_calendar  # noqa: E402

END = sys.argv[1] if len(sys.argv) > 1 else "2026-09-25"
days = [str(d) for d in trading_calendar.trading_days_between(pd.Timestamp("2024-07-09").date(), pd.Timestamp(END).date())]
s3 = boto3.client("s3")
KEYS = ("accounts_with_prior_holdings", "computable_count", "not_computable_count", "complete")


def read(table, day):
    uri = opal_naming.address("irpt", "49financial", "gold", table, "date=%s" % day)
    bucket, _, key = uri[len("s3://"):].partition("/")
    objs = [o["Key"] for o in s3.list_objects_v2(Bucket=bucket, Prefix=key.rstrip("/") + "/").get("Contents", []) if o["Key"].endswith(".parquet")]
    if not objs:
        return None
    return pd.concat([pd.read_parquet(io.BytesIO(s3.get_object(Bucket=bucket, Key=k)["Body"].read())) for k in objs])


def one(day):
    g, m = read("holdings_performance_daily", day), read("holdings_performance_manifest", day)
    if g is None:
        return day, None, 0, 0, False, False
    ok = g[g["status"].astype(str) == "OK"]
    r = pd.to_numeric(ok["daily_return"], errors="coerce")
    bad = int(((r <= -1) | (r >= 1)).sum())
    big = int((r.abs() > 0.5).sum())
    row = m.iloc[0].to_dict() if m is not None and len(m) else {}
    complete = all(k in row for k in KEYS) and bool(row.get("complete")) is True
    return day, len(g), bad, big, "leveraged" in g.columns, complete


with ThreadPoolExecutor(32) as pool:
    res = list(pool.map(one, days))
absent = [d for d, n, *_ in res if n is None]
bad = sum(r[2] for r in res)
big = sum(r[3] for r in res)
nolev = [r[0] for r in res if r[1] is not None and not r[4]]
incomplete = [r[0] for r in res if not r[5]]
print("days %d | partitions absent %d | OK rows |r|>=1: %d | OK rows |r|>0.5: %d | days without `leveraged`: %d | manifests complete %d of %d%s" % (
    len(days), len(absent), bad, big, len(nolev), len(days) - len(incomplete), len(days),
    (" (first incomplete %s)" % incomplete[:3]) if incomplete else ""))
ok = not absent and bad == 0 and not nolev and not incomplete
print("E3-AC4 PASS" if ok else "E3-AC4 FAIL")
sys.exit(0 if ok else 1)
