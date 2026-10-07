"""IRPT_CUSTDY -- read-only probe of the firm's returns gold for one day, written to a FILE.

Standing rule (1.0.0_SA_CTO~DELL2 msg 213): a firm-bucket read the dell2 user is denied goes to the laptop as a
committed read-only script whose result is a file. This is that script. It lists one partition of the
`account_return_daily` gold (IRPT_DASHBD's producer) and reads each parquet object's row count, columns and distinct
accounts. It writes nothing to S3.

Run (any box whose identity can read the firm bucket):
    python org/missions/D9/IRPT/IRPT_CUSTDY/deliverables/2.0.0_SA_COO~K2/read_returns_gold_partition.py \
        --master 08335338 --day 2026-09-30 --out <file.json>

The address is builder output: opal_naming.address("irpt", lookup(master)["firm"], "gold", "account_return_daily",
"date=<day>"). No bucket, prefix or firm token is typed here.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *([".."] * 7)))
sys.path.insert(0, os.path.join(ROOT, "lib"))

import opal_naming  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--master", required=True)
    ap.add_argument("--day", required=True)
    ap.add_argument("--table", default="account_return_daily")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)

    import boto3
    import pyarrow.parquet as pq

    firm = opal_naming.lookup(a.master)["firm"]
    uri = opal_naming.address("irpt", firm, "gold", a.table, "date=%s" % a.day)
    bucket, _, prefix = uri[len("s3://"):].partition("/")
    s3 = boto3.client("s3")
    result = {"uri": uri, "read_at": datetime.now(timezone.utc).isoformat(), "objects": [], "error": None}
    try:
        keys = []
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix.rstrip("/") + "/"):
            keys += [(o["Key"], o["Size"], o["LastModified"].isoformat()) for o in page.get("Contents", [])]
        accounts = set()
        for key, size, modified in keys:
            entry = {"key": key, "bytes": size, "last_modified": modified}
            if key.endswith(".parquet"):
                table = pq.read_table(io.BytesIO(s3.get_object(Bucket=bucket, Key=key)["Body"].read()))
                entry["rows"] = table.num_rows
                entry["columns"] = table.column_names
                for col in ("account_id", "account", "account_number"):
                    if col in table.column_names:
                        accounts.update(str(v) for v in table.column(col).to_pylist())
                        entry["account_column"] = col
                        break
            result["objects"].append(entry)
        result["object_count"] = len(keys)
        result["distinct_accounts"] = len(accounts)
    except Exception as exc:  # the failure is the result: written, never swallowed
        result["error"] = "%s: %s" % (type(exc).__name__, exc)
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print("RETURNS-GOLD-READ uri=%s objects=%s distinct_accounts=%s error=%s"
          % (uri, result.get("object_count"), result.get("distinct_accounts"), result["error"]))
    return 1 if result["error"] else 0


if __name__ == "__main__":
    sys.exit(main())
