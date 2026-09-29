"""Round 22 AC2 (IB-pr-221) -- the seam probe against the REAL Inflection gold, read-only: account 998's YTD through
holdings_gold.calculate equals the independent chain of its OK days 2026-01-01..2026-09-25 within 1e-12.

Usage: python p22_1_ac2_inf_gold_live.py <worktree root>
"""
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _pkg import install  # noqa: E402

root, package = install(sys.argv[1] if len(sys.argv) > 1 else ".")
import boto3  # noqa: E402
import pandas as pd  # noqa: E402
import holdings_gold as hg  # noqa: E402
import opal_naming  # noqa: E402
import tenants  # noqa: E402
from ids import opaque_account  # noqa: E402

RAW, START, END = "998", "2026-01-01", "2026-09-25"
uri = opal_naming.address("irpt", "inflection", "gold", "holdings_performance_daily", "date=1970-01-01")
bucket, _, key = uri[len("s3://"):].partition("/")
prefix = key[:key.index("date=")]
s3 = boto3.client("s3")
chain, n = 1.0, 0
src = hg.HoldingsGoldSource(s3, bucket=bucket, prefix=prefix)
for day in src.partition_dates():
    d = str(day)
    if not (START <= d <= END):
        continue
    for o in s3.list_objects_v2(Bucket=bucket, Prefix="%sdate=%s/" % (prefix, d)).get("Contents", []):
        if o["Key"].endswith(".parquet"):
            f = pd.read_parquet(io.BytesIO(s3.get_object(Bucket=bucket, Key=o["Key"])["Body"].read()))
            f = f[(f["account_id"].astype(str) == RAW) & (f["status"].astype(str) == "OK")]
            for r in f["daily_return"]:
                chain *= 1.0 + float(r)
                n += 1
acct = opaque_account(tenants._CANONICAL_INF, RAW)
scope = {"verified_request_firm_id": tenants._LEGACY_SHORT_ID["INF"], "permitted_account_set": [acct],
         "resolved_scope": {"scope_ids": [acct]}}
try:
    rep = hg.calculate(scope, START, END, src)["report"]
    got = rep["returns"]["account_detail"][0]["value"]
    ok = abs(got - (chain - 1.0)) < 1e-12 and rep["lineage"]["provider"] == "OPAL_HOLDINGS"
    print("gold OK days %d | independent chain %.12f | holdings_gold %.12f | provider %s" % (n, chain - 1.0, got, rep["lineage"]["provider"]))
except Exception as exc:
    print("FAIL: holdings_gold could not answer (%s); independent chain over %d days %.12f" % (type(exc).__name__, n, chain - 1.0))
    ok = False
print("P22-1-AC2 PASS" if ok else "P22-1-AC2 FAIL")
sys.exit(0 if ok else 1)
