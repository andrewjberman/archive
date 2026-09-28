"""IB-pr-192 AC2 -- the seam probe against the REAL neighbour: live twr_daily, read-only, one invested account.

Usage: python p19_2_ac2_live_seam.py <worktree root>
A Since-inception request (start 1970-01-01, end = the latest partition) for the control account answers period
"SI" with dates.actual_start equal to that account's first OK business_date in the live table (read here
independently from the partitions), and a finite value above -1. No write, no vendor call.
"""
import io
import math
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _engine_path import install  # noqa: E402

install(sys.argv[1] if len(sys.argv) > 1 else ".")
import f49_engine as f49  # noqa: E402
import tenants  # noqa: E402
from ids import opaque_account  # noqa: E402
from opal_naming import lookup  # noqa: E402

GOOD = "0010498003"
firm = lookup("49financial")
bucket, root = firm["bucket"], firm["trees"]["advi"]["gold_root"]
s3 = boto3.client("s3")
source = f49.EngineSource(s3, bucket=bucket, root=root)
days = source.partition_dates()
latest = days[-1]
prefix = root.rstrip("/") + "/" + f49.TABLE_DAILY + "/"


def status(day):
    raw = s3.get_object(Bucket=bucket, Key="%sdate=%s/data.parquet" % (prefix, day))["Body"].read()
    frame = pd.read_parquet(io.BytesIO(raw), columns=["account_id", "status"])
    hit = frame[frame["account_id"] == GOOD]
    return day, (len(hit) and hit["status"].iloc[0] == "OK")


with ThreadPoolExecutor(16) as pool:
    first_ok = next((d for d, is_ok in sorted(pool.map(status, days)) if is_ok), None)

account = opaque_account(tenants._CANONICAL_49F, GOOD)
scope = {"verified_request_firm_id": tenants._LEGACY_SHORT_ID["49F"], "permitted_account_set": [account],
         "resolved_scope": {"scope_ids": [account]}}
ok = True
try:
    report = f49.calculate(scope, "1970-01-01", latest, f49.EngineSource(s3, bucket=bucket, root=root))["report"]
    periods = [p.get("period") for p in report["returns"]["period_returns"]]
    actual, value = report["dates"]["actual_start"], report["returns"]["account_detail"][0]["value"]
    if "SI" in periods and actual == first_ok and math.isfinite(value) and value > -1.0:
        print("PASS: SI %s..%s value %.6f (first OK day read independently: %s)" % (actual, latest, value, first_ok))
    else:
        print("FAIL: periods %r actual_start %r (first OK %s) value %r" % (periods, actual, first_ok, value))
        ok = False
except Exception as exc:
    print("FAIL: Since-inception refused as %s (first OK %s)" % (type(exc).__name__, first_ok))
    ok = False

if ok:
    print("P19-2-AC2 PASS")
else:
    print("P19-2-AC2 FAIL")
sys.exit(0 if ok else 1)
