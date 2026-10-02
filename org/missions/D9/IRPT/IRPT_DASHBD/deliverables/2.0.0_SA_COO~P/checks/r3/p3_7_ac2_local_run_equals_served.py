"""DB-7-AC2 -- the packaged handler, run locally for 2026-09-28, reproduces the SERVED gold partition (the seam with
the real neighbour).

Reads the worker's local output
  org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/reporting_gold_local_20260928.parquet
and the served partition s3://opal-data-49financial/irpt/49financial/gold/account_return_daily/date=2026-09-28/data.parquet,
then compares them row for row on (account_id, business_date, market_value_eod, external_flow, total_return_daily,
return_basis, day_quality): same row count, same keys, numeric columns equal within 1e-9 (nulls equal to nulls).
Usage: python <this file> <repo_root>
"""
import io
import sys
from pathlib import Path

COLS = ["account_id", "business_date", "market_value_eod", "external_flow", "total_return_daily", "return_basis", "day_quality"]
NUM = ["market_value_eod", "external_flow", "total_return_daily"]


def fail(msg):
    print("FAIL: " + msg)
    print("DB-7-AC2 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    local = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/reporting_gold_local_20260928.parquet"
    if not local.is_file():
        fail("no local output at %s" % local)
    try:
        import boto3
        import pandas as pd
    except Exception as exc:  # noqa: BLE001
        fail("pandas/boto3 unavailable: %s" % exc)
    body = boto3.client("s3").get_object(
        Bucket="opal-data-49financial",
        Key="irpt/49financial/gold/account_return_daily/date=2026-09-28/data.parquet")["Body"].read()
    served = pd.read_parquet(io.BytesIO(body))
    mine = pd.read_parquet(local)
    for name, df in (("served", served), ("local", mine)):
        missing = [c for c in COLS if c not in df.columns]
        if missing:
            fail("%s lacks columns %s" % (name, missing))
    s = served[COLS].astype({"account_id": str, "business_date": str}).sort_values(["account_id"]).reset_index(drop=True)
    m = mine[COLS].astype({"account_id": str, "business_date": str}).sort_values(["account_id"]).reset_index(drop=True)
    if len(s) != len(m):
        fail("row count local %d != served %d" % (len(m), len(s)))
    if list(s["account_id"]) != list(m["account_id"]):
        fail("account sets differ")
    for c in ("business_date", "return_basis", "day_quality"):
        if list(s[c].astype(str)) != list(m[c].astype(str)):
            fail("column %s differs" % c)
    for c in NUM:
        a, b = s[c].astype(float), m[c].astype(float)
        both_null = a.isna() & b.isna()
        diff = (a - b).abs()
        bad = (~both_null) & ((a.isna() != b.isna()) | (diff > 1e-9))
        if bool(bad.any()):
            fail("column %s differs on %d row(s)" % (c, int(bad.sum())))
    print("OK: %d of %d served rows reproduced on %d columns" % (len(m), len(s), len(COLS)))
    print("DB-7-AC2 PASS")


if __name__ == "__main__":
    main()
