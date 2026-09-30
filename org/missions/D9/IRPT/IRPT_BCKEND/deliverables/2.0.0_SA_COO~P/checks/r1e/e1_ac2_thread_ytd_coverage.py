"""~E round 1 AC2 -- the thread account's gold covers every YTD trading day and chains to a finite YTD above -1.

Usage: python e1_ac2_thread_ytd_coverage.py [end day, default 2026-09-25]
For every trading day 2026-01-02..<end> (lib/trading_calendar), the gold partition at lib/opal_naming
address("irpt", "49financial", "gold", "holdings_performance_daily", "date=<day>") carries one row for the thread
account. The chained YTD, prod(1 + daily_return) - 1, is finite and above -1. PRD ADDENDUM v0.19 rulings 5 (day axis)
and 11 (thread first).
"""
import io
import math
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
import pandas as pd

ROOT = Path(__file__).resolve().parents[9]
sys.path.insert(0, str(ROOT / "lib"))
import opal_naming  # noqa: E402
import trading_calendar  # noqa: E402

THREAD = "0010498003"
END = sys.argv[1] if len(sys.argv) > 1 else "2026-09-25"
s3 = boto3.client("s3")


def day_row(day):
    uri = opal_naming.address("irpt", "49financial", "gold", "holdings_performance_daily", "date=%s" % day)
    bucket, _, key = uri[len("s3://"):].partition("/")
    keys = [o["Key"] for o in s3.list_objects_v2(Bucket=bucket, Prefix=key.rstrip("/") + "/").get("Contents", []) if o["Key"].endswith(".parquet")]
    if not keys:
        return day, None
    f = pd.concat([pd.read_parquet(io.BytesIO(s3.get_object(Bucket=bucket, Key=k)["Body"].read())) for k in keys])
    r = f[f["account_id"].astype(str) == THREAD]
    return day, (float(r["daily_return"].iloc[0]) if len(r) == 1 else None)


days = [str(d) for d in trading_calendar.trading_days_between(pd.Timestamp("2026-01-02").date(), pd.Timestamp(END).date())]
with ThreadPoolExecutor(16) as pool:
    rows = dict(pool.map(day_row, days))
missing = [d for d, r in rows.items() if r is None]
running = 1.0
for d in days:
    if rows[d] is not None:
        running *= 1.0 + rows[d]
ytd = running - 1.0
print("trading days %d (%s..%s) | missing thread rows %d | chained YTD %s" % (len(days), days[0], days[-1], len(missing),
      "%.6f" % ytd if not missing else "n/a"))
ok = not missing and math.isfinite(ytd) and ytd > -1.0
if ok:
    print("E1-AC2 PASS")
else:
    print("E1-AC2 FAIL")
sys.exit(0 if ok else 1)
