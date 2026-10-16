"""IRPT_DASHBD (workstream F-SHIP, ~F2): a READ-ONLY census of a firm's transaction silver that returns only COUNTS AND COLUMN NAMES --
the partitions read, the objects read, the row count from each object's parquet FOOTER, and the column list of the first non-empty
object. It reads no cell value of any column, so it never touches an account id, an amount or a client field.

  python <this file> <firm> <out.json>        firm: 49financial | cottonwood | inflection

The producing record's own `reads` field is this tool's output (CTO round-128 analysis, msg 9175: a ground-read or producer record carries
its own non-null reads; the issuer's census is corroboration, never the record). Run from the repository root; needs boto3 and pyarrow and
the box's AWS credentials; makes GET requests only (a ranged GET of each object's tail for the footer, and the head for the schema).
"""
import datetime as dt
import importlib.util
import io
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
import pyarrow.parquet as pq
from botocore.config import Config

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting/adapters"))
import account_return_daily as ard  # noqa: E402

s3 = boto3.client("s3", config=Config(max_pool_connections=16, retries={"max_attempts": 5}))


class RangeFile(io.RawIOBase):
    """A read-only file-like over one S3 object that fetches byte ranges, so a parquet footer costs one small GET."""

    def __init__(self, bucket, key):
        self.bucket, self.key = bucket, key
        self.size = s3.head_object(Bucket=bucket, Key=key)["ContentLength"]
        self.pos = 0

    def readable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, offset, whence=0):
        self.pos = offset if whence == 0 else (self.pos + offset if whence == 1 else self.size + offset)
        return self.pos

    def read(self, n=-1):
        if self.pos >= self.size:
            return b""
        end = self.size - 1 if n is None or n < 0 else min(self.size - 1, self.pos + n - 1)
        body = s3.get_object(Bucket=self.bucket, Key=self.key, Range="bytes=%d-%d" % (self.pos, end))["Body"].read()
        self.pos += len(body)
        return body

    def readinto(self, b):
        data = self.read(len(b))
        b[:len(data)] = data
        return len(data)


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def where(firm):
    if firm == "49financial":
        src = json.load(open(ROOT / "data/assets/scripts/gold/irpt_reporting/sources.json", encoding="utf-8"))["schwab_08335338"]
        return src["bucket"], src["transactions_prefix"], "fact_trn"
    if firm == "cottonwood":
        cbd = load("cbd", "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_bd_account_return_daily.py")
        return cbd.BUCKET, cbd.SILVER_ROOT + "fact_transactions/", "fact_transactions"
    iar = load("iar", "data/assets/scripts/gold/irpt_reporting/adapters/inflection_account_return_daily.py")
    bucket, _, rest = iar.ORION_SILVER[len("s3://"):].partition("/")
    return bucket, rest + "fact_transactions/", "fact_transactions"


def keys_of(bucket, prefix, day):
    out = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix="%sdate=%s/" % (prefix, day)):
        for o in page.get("Contents", []) or []:
            if o["Key"].endswith(".parquet"):
                out.append(o["Key"])
    return sorted(out)


def main(firm, out_path):
    bucket, prefix, table = where(firm)
    days = ard.partition_days(s3, bucket, prefix)

    def one(day):
        rows, objs, names = 0, 0, None
        for k in keys_of(bucket, prefix, day):
            md = pq.read_metadata(RangeFile(bucket, k))
            objs += 1
            rows += md.num_rows
            if names is None and md.num_rows:
                names = [md.schema.column(i).name for i in range(md.num_columns)]
        return rows, objs, names

    with ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(one, days))
    columns = next((n for _, _, n in results if n), [])
    out = {"firm": firm, "table": table, "read_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "partitions_read": len(days), "objects_read": sum(o for _, o, _ in results), "rows": sum(r for r, _, _ in results),
           "partitions_empty": sum(1 for r, _, _ in results if not r), "first_day": days[0] if days else None,
           "last_day": days[-1] if days else None, "columns": columns, "column_count": len(columns),
           "reader": "footer-only: ranged GET of each parquet object's tail; no cell value read"}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    print(firm, "partitions", out["partitions_read"], "objects", out["objects_read"], "rows", out["rows"], "columns", out["column_count"])


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("49financial", "cottonwood", "inflection"):
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
