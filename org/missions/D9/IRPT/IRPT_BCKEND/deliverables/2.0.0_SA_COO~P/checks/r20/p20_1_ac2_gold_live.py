"""IB-pr-201 AC2 -- the seam probe against the REAL holdings gold (read-only): the thread account's YTD answer equals
the chain of its landed daily returns.

Usage: python p20_1_ac2_gold_live.py <worktree root>
Source: lib/opal_naming address("irpt", "49financial", "gold", "holdings_performance_daily", ...) -- the 184 partitions
~E round 1 landed (TO-IB-er-201; chained YTD 0.058285). The check chains the thread account's OK daily_return rows over
2026-01-01..2026-09-25 independently, then asks holdings_gold.calculate through HoldingsGoldSource on the live bucket.
Pass: the two agree within 1e-12, and the answer's provider is OPAL_HOLDINGS.
"""
import io
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _pkg import install  # noqa: E402

root, package = install(sys.argv[1] if len(sys.argv) > 1 else ".")
import opal_naming  # noqa: E402
import tenants  # noqa: E402
from ids import opaque_account  # noqa: E402

T = "0010498003"
uri = opal_naming.address("irpt", "49financial", "gold", "holdings_performance_daily", "date=2026-01-02")
bucket, _, key = uri[len("s3://"):].partition("/")
prefix = key[:key.index("date=")]
s3 = boto3.client("s3")
pages = s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix, Delimiter="/")
days = sorted(p["Prefix"][len(prefix) + 5:-1] for page in pages for p in page.get("CommonPrefixes", []))
days = [d for d in days if "2026-01-01" <= d <= "2026-09-25"]


def row(day):
    f = pd.read_parquet(io.BytesIO(s3.get_object(Bucket=bucket, Key="%sdate=%s/data.parquet" % (prefix, day))["Body"].read()))
    r = f[(f["account_id"].astype(str) == T) & (f["status"] == "OK")]
    return float(r["daily_return"].iloc[0]) if len(r) == 1 else None


with ThreadPoolExecutor(16) as pool:
    rets = [r for r in pool.map(row, days) if r is not None]
chain = 1.0
for r in rets:
    chain *= 1.0 + r
want = chain - 1.0
ok = True
try:
    import holdings_gold as hg
    acct = opaque_account(tenants._CANONICAL_49F, T)
    scope = {"verified_request_firm_id": tenants._LEGACY_SHORT_ID["49F"], "permitted_account_set": [acct],
             "resolved_scope": {"scope_ids": [acct]}}
    rep = hg.calculate(scope, "2026-01-01", "2026-09-25", hg.HoldingsGoldSource(s3, bucket=bucket, prefix=prefix))["report"]
    got = rep["returns"]["account_detail"][0]["value"]
    print("gold days %d | independent chain %.12f | holdings_gold %.12f | provider %s" % (len(rets), want, got,
          rep["lineage"].get("provider")))
    ok = abs(got - want) < 1e-12 and rep["lineage"].get("provider") == "OPAL_HOLDINGS"
except Exception as exc:
    print("FAIL: holdings_gold could not answer (%s); independent chain over %d days %.12f" % (type(exc).__name__, len(rets), want))
    ok = False
if ok:
    print("P20-1-AC2 PASS")
else:
    print("P20-1-AC2 FAIL")
sys.exit(0 if ok else 1)
