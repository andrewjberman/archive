"""IRPT_DASHBD (workstream F-SHIP, ~F2): a READ-ONLY, VALUES-FREE format census of two Inflection `fact_transactions` columns that are STRINGS, for the
Inflection producer's reading rules (round 131): `transDate` (must read as an ISO calendar date) and `avgPrice` (must read as a number).

  python <this file> <out.json>

Over EVERY partition and over the rows whose status is Complete it counts the rows, the `transDate` values that match YYYY-MM-DD, the `avgPrice` values
that cast to a number, and the `avgPrice` values that are the literal text of a non-number. It writes counts only: no date, price, amount, account id
or identifier is kept or written. GET requests only. Run from the repository root with the box's AWS credentials; needs boto3 and pyarrow.
"""
import datetime as dt
import importlib.util
import io
import json
import sys
from pathlib import Path

import boto3
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
from botocore.config import Config

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting/adapters"))
import account_return_daily as ard  # noqa: E402

NUMBER = r"^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$"
ZERO = r"^[+-]?0*(\.0*)?([eE][+-]?\d+)?$"
s3 = boto3.client("s3", config=Config(max_pool_connections=8, retries={"max_attempts": 5}))


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(out_path):
    iar = load("iar", "data/assets/scripts/gold/irpt_reporting/adapters/inflection_account_return_daily.py")
    bucket, _, rest = iar.ORION_SILVER[len("s3://"):].partition("/")
    prefix = rest + "fact_transactions/"
    days = ard.partition_days(s3, bucket, prefix)
    c = {"rows_complete": 0, "transDate_iso": 0, "transDate_not_iso": 0, "avgPrice_numeric": 0, "avgPrice_not_numeric": 0, "avgPrice_zero": 0}
    for day in days:
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix="%sdate=%s/" % (prefix, day)):
            for o in page.get("Contents", []) or []:
                if not o["Key"].endswith(".parquet"):
                    continue
                raw = s3.get_object(Bucket=bucket, Key=o["Key"])["Body"].read()
                t = pq.read_table(io.BytesIO(raw), columns=["status", "transDate", "avgPrice"])
                t = t.filter(pc.equal(t.column("status"), "Complete"))
                n = t.num_rows
                c["rows_complete"] += n
                iso = pc.sum(pc.cast(pc.match_substring_regex(t.column("transDate"), r"^\d{4}-\d{2}-\d{2}$"), pa.int64())).as_py() or 0
                c["transDate_iso"] += int(iso)
                c["transDate_not_iso"] += n - int(iso)
                price = pc.utf8_trim_whitespace(t.column("avgPrice"))
                ok = int(pc.sum(pc.cast(pc.match_substring_regex(price, NUMBER), pa.int64())).as_py() or 0)
                both = pc.and_(pc.match_substring_regex(price, NUMBER), pc.match_substring_regex(price, ZERO))
                zero = int(pc.sum(pc.cast(both, pa.int64())).as_py() or 0)
                c["avgPrice_numeric"] += ok
                c["avgPrice_not_numeric"] += n - ok
                c["avgPrice_zero"] += zero
        print("read", day, flush=True)
    out = {"firm": "inflection", "read_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "table": "fact_transactions",
           "partitions_read": len(days), "counts_over_complete_rows": c,
           "reader": "values-free: counts of rows by whether transDate matches YYYY-MM-DD and avgPrice parses as a number; no value is kept or written"}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    print(c)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
