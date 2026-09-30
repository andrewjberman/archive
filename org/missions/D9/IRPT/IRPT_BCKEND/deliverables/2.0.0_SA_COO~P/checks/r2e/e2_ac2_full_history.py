"""~E round 2 AC2 -- the 49F gold reaches back to the first day a holdings return can exist (PRD v0.19 ruling 6;
1.0.0_SA_CTO ruling 102520: since inception needs the history).

Usage: python e2_ac2_full_history.py [end day, default 2026-09-25]
The declared positions silver's first partition is 2024-07-08 (559 partitions to 2026-09-25, measured at the cut), so
the first computable day is the next trading day. Pass: a gold partition exists at
address("irpt", "49financial", "gold", "holdings_performance_daily", "date=<d>") for EVERY trading day d
(lib/trading_calendar) from that day through <end>, and none is empty.
"""
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
FIRST_SILVER = "2024-07-08"
s3 = boto3.client("s3")
start = trading_calendar.trading_days_between(pd.Timestamp(FIRST_SILVER).date(), pd.Timestamp(END).date())[1]
days = [str(d) for d in trading_calendar.trading_days_between(start, pd.Timestamp(END).date())]


def has(day):
    uri = opal_naming.address("irpt", "49financial", "gold", "holdings_performance_daily", "date=%s" % day)
    bucket, _, key = uri[len("s3://"):].partition("/")
    objs = [o for o in s3.list_objects_v2(Bucket=bucket, Prefix=key.rstrip("/") + "/").get("Contents", [])
            if o["Key"].endswith(".parquet") and o["Size"] > 0]
    return day, bool(objs)


with ThreadPoolExecutor(16) as pool:
    missing = [d for d, present in pool.map(has, days) if not present]
print("trading days %d (%s..%s) | missing gold partitions %d%s" % (len(days), days[0], days[-1], len(missing),
      (" (first %s)" % missing[:3]) if missing else ""))
ok = not missing
if ok:
    print("E2-AC2 PASS")
else:
    print("E2-AC2 FAIL")
sys.exit(0 if ok else 1)
