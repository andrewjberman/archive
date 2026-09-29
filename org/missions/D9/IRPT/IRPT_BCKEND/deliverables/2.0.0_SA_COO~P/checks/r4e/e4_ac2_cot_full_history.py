"""~E round 4 AC2 -- the Cottonwood gold reaches back to the first day a holdings return can exist (PRD v0.19 rulings
5, 6).

Usage: python e4_ac2_cot_full_history.py [end day, default 2026-09-25]
Cottonwood's positions silver (s3://opal-data-assets/blackdiamond/cottonwood/silver/fact_holdings/) lands a partition per
CALENDAR day from 2026-06-09. A trading day d is COMPUTABLE when the silver holds a partition for d and for its prior
trading day (ruling 5: a missing trading-day partition is ABSENT). Pass: for every computable trading day from the
first through <end>, a non-empty gold partition exists at
address("irpt", "cottonwood", "gold", "holdings_performance_daily", "date=<d>"). The count of non-computable trading
days is printed beside the result.
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
SILVER_BUCKET, SILVER_PREFIX = "opal-data-assets", "blackdiamond/cottonwood/silver/fact_holdings/"
s3 = boto3.client("s3")
landed = set()
for page in s3.get_paginator("list_objects_v2").paginate(Bucket=SILVER_BUCKET, Prefix=SILVER_PREFIX, Delimiter="/"):
    for cp in page.get("CommonPrefixes", []):
        tok = cp["Prefix"][len(SILVER_PREFIX):].rstrip("/")
        if tok.startswith("date="):
            landed.add(tok[5:])
first = min(landed)
tdays = [str(d) for d in trading_calendar.trading_days_between(pd.Timestamp(first).date(), pd.Timestamp(END).date())]
computable = [d for i, d in enumerate(tdays) if i > 0 and d in landed and tdays[i - 1] in landed]


def has(day):
    uri = opal_naming.address("irpt", "cottonwood", "gold", "holdings_performance_daily", "date=%s" % day)
    bucket, _, key = uri[len("s3://"):].partition("/")
    objs = [o for o in s3.list_objects_v2(Bucket=bucket, Prefix=key.rstrip("/") + "/").get("Contents", [])
            if o["Key"].endswith(".parquet") and o["Size"] > 0]
    return day, bool(objs)


with ThreadPoolExecutor(16) as pool:
    missing = [d for d, present in pool.map(has, computable) if not present]
print("silver partitions %d from %s | trading days %d | computable %d (%s..%s) | not computable %d | missing gold %d%s" % (
    len(landed), first, len(tdays) - 1, len(computable), computable[0], computable[-1], len(tdays) - 1 - len(computable),
    len(missing), (" (first %s)" % missing[:3]) if missing else ""))
ok = bool(computable) and not missing
if ok:
    print("E4-AC2 PASS")
else:
    print("E4-AC2 FAIL")
sys.exit(0 if ok else 1)
