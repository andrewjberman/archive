"""IRPT_DASHBD (workstream F-SHIP, ~F2): the LATEST-SNAPSHOT price and null census of the Inflection transaction table (round 135). READ-ONLY, VALUES-FREE, counts only; GET
requests only. Each Orion silver `fact_transactions` partition is a cumulative snapshot of the whole history (see inflection_snapshot_census.py), so the proper domain of a
count is the LATEST snapshot.

  python <this file> <out.json>

Over the latest partition's Complete rows it counts: the rows; the rows with units and a positive navPrice; of those the rows with a non-blank fundFamilyName and the rows
without one; of the fund-family rows the rows whose navPrice * noUnits is within one percent of transAmount; the rows with zero units; the rows with units and a
non-positive navPrice; and the null or blank rows of avgPrice and of the other producer-facing columns.
"""
import datetime as dt
import importlib.util
import io
import json
import sys
from pathlib import Path

import boto3
import pyarrow as pa
import pyarrow.parquet as pq
from botocore.config import Config

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting/adapters"))
import account_return_daily as ard  # noqa: E402

COLS = ["status", "transDate", "accountId", "transactionDescription", "transAmount", "noUnits", "avgPrice", "navPrice", "fundFamilyName", "ticker", "productName",
        "custodianName", "id"]
s3 = boto3.client("s3", config=Config(max_pool_connections=8, retries={"max_attempts": 5}))


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def blank(series):
    return int((series.isna() | (series.astype(str).str.strip() == "")).sum())


def main(out_path):
    iar = load("iar", "data/assets/scripts/gold/irpt_reporting/adapters/inflection_account_return_daily.py")
    bucket, _, rest = iar.ORION_SILVER[len("s3://"):].partition("/")
    prefix = rest + "fact_transactions/"
    day = ard.partition_days(s3, bucket, prefix)[-1]
    tables = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix="%sdate=%s/" % (prefix, day)):
        for o in page.get("Contents", []) or []:
            if o["Key"].endswith(".parquet"):
                tables.append(pq.read_table(io.BytesIO(s3.get_object(Bucket=bucket, Key=o["Key"])["Body"].read()), columns=COLS))
    df = pa.concat_tables(tables, promote_options="default").to_pandas()
    c = df[df["status"] == "Complete"]
    units = c["noUnits"].astype(float)
    nav = c["navPrice"].astype(float)
    amt = c["transAmount"].astype(float)
    usable = (units != 0) & (nav > 0)
    fam = c["fundFamilyName"].notna() & (c["fundFamilyName"].astype(str).str.strip() != "")
    diff = (units * nav - amt).abs()
    tol = amt.abs() * 0.01 + 0.01
    out = {"firm": "inflection", "latest_snapshot": day, "read_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "rows_all_statuses": int(len(df)), "complete_rows": int(len(c)),
           "fund_family": {"unit_bearing_positive_nav_rows": int(usable.sum()), "with_fund_family": int((usable & fam).sum()), "without_fund_family": int((usable & ~fam).sum()),
                           "fund_rows_within_1pct": int((usable & fam & (diff <= tol)).sum())},
           "zero_units_rows": int((units == 0).sum()), "units_with_nonpositive_navPrice_rows": int(((units != 0) & (nav <= 0)).sum()),
           "null_or_blank_rows_complete": {col: blank(c[col]) for col in COLS},
           "reader": "values-free: counts only; no value is kept or written"}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    print(json.dumps(out)[:1500])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
