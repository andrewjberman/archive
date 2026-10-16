"""IRPT_DASHBD (workstream F-SHIP, ~F2): a READ-ONLY, VALUES-FREE SHAPE census of one Inflection `fact_transactions` string column, for the Inflection
producer's reading rules (round 131).

  python <this file> <column> <out.json> [n_partitions]        default column avgPrice, default 8 partitions (0 = every partition)

For a seeded draw of partitions (or every partition) and over the rows whose status is Complete it counts the rows per SHAPE: the value with every
digit replaced by the character 9 (so `12.5` reads `99.9` and the text `None` reads `None`). No digit of any value is kept. Counts only. GET requests
only. Run from the repository root with the box's AWS credentials; needs boto3 and pyarrow.
"""
import datetime as dt
import importlib.util
import io
import json
import random
import sys
from pathlib import Path

import boto3
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


def main(column, out_path, n_partitions):
    iar = load("iar", "data/assets/scripts/gold/irpt_reporting/adapters/inflection_account_return_daily.py")
    bucket, _, rest = iar.ORION_SILVER[len("s3://"):].partition("/")
    prefix = rest + "fact_transactions/"
    days = ard.partition_days(s3, bucket, prefix)
    picked = days if not n_partitions or n_partitions >= len(days) else sorted(random.Random(131).sample(days, n_partitions))
    shapes = {}
    rows = 0
    for day in picked:
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix="%sdate=%s/" % (prefix, day)):
            for o in page.get("Contents", []) or []:
                if not o["Key"].endswith(".parquet"):
                    continue
                raw = s3.get_object(Bucket=bucket, Key=o["Key"])["Body"].read()
                t = pq.read_table(io.BytesIO(raw), columns=["status", column])
                t = t.filter(pc.equal(t.column("status"), "Complete"))
                rows += t.num_rows
                shaped = pc.replace_substring_regex(t.column(column), r"[0-9]", "9")
                for v in pc.value_counts(shaped).to_pylist():
                    key = "(null)" if v["values"] is None else str(v["values"])
                    shapes[key] = shapes.get(key, 0) + int(v["counts"])
    top = dict(sorted(shapes.items(), key=lambda kv: -kv[1])[:40])
    out = {"firm": "inflection", "column": column, "read_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "partitions_read": len(picked), "partitions_in_table": len(days), "rows_complete": rows, "distinct_shapes": len(shapes),
           "top_shapes_by_rows": top, "reader": "values-free: every digit replaced by 9; counts of rows per shape; no value is kept or written"}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    print("rows", rows, "distinct_shapes", len(shapes), list(top.items())[:12])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 8)
