"""IRPT_DASHBD (workstream F-SHIP, ~F2): a READ-ONLY, VALUES-FREE census of the SIGN of Inflection's `transAmount` per `transactionDescription` (a
vendor enum of 48 words, not client data), over the rows whose status is Complete and over EVERY partition, for the Inflection producer's amount rule
(round 131).

  python <this file> <out.json>

Per description it counts the Complete rows with a positive, a negative and a zero transAmount. No amount, account id, symbol or identifier is kept
or written. GET requests only. Run from the repository root with the box's AWS credentials; needs boto3 and pyarrow.
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
    per = {}
    rows = complete = 0
    for day in days:
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix="%sdate=%s/" % (prefix, day)):
            for o in page.get("Contents", []) or []:
                if not o["Key"].endswith(".parquet"):
                    continue
                raw = s3.get_object(Bucket=bucket, Key=o["Key"])["Body"].read()
                t = pq.read_table(io.BytesIO(raw), columns=["status", "transactionDescription", "transAmount"])
                rows += t.num_rows
                t = t.filter(pc.equal(t.column("status"), "Complete"))
                complete += t.num_rows
                amt = pc.cast(t.column("transAmount"), pa.float64())
                sign = pc.sign(amt)
                for d in pc.unique(t.column("transactionDescription")).to_pylist():
                    m = pc.equal(t.column("transactionDescription"), d)
                    sg = pc.filter(sign, m)
                    cell = per.setdefault(str(d), {"positive": 0, "negative": 0, "zero": 0, "null": 0})
                    cell["positive"] += int(pc.sum(pc.cast(pc.equal(sg, 1.0), pa.int64())).as_py() or 0)
                    cell["negative"] += int(pc.sum(pc.cast(pc.equal(sg, -1.0), pa.int64())).as_py() or 0)
                    cell["zero"] += int(pc.sum(pc.cast(pc.equal(sg, 0.0), pa.int64())).as_py() or 0)
                    cell["null"] += int(sg.null_count)
        print("read", day, flush=True)
    out = {"firm": "inflection", "read_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "table": "fact_transactions",
           "partitions_read": len(days), "rows": rows, "rows_complete": complete, "sign_by_description": dict(sorted(per.items())),
           "reader": "values-free: counts of Complete rows by the sign of transAmount per description; no amount is kept or written"}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    print("rows", rows, "complete", complete, "descriptions", len(per))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
