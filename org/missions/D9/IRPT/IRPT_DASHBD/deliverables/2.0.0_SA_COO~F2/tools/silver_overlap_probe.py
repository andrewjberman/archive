"""IRPT_DASHBD (workstream F-SHIP, ~F2): the READ-ONLY overlap probe of a firm's fact_transactions silver (CTO msg 10592, item 5).

  python <this file> <firm_key> <source> <scope> [<n_partitions>] [<table>]        e.g.  cottonwood blackdiamond cottonwood 6 fact_transactions      run from the repository root; GET requests only; counts only

Reads the transaction-id column of the newest <n_partitions> fact_transactions partitions under <source>/<scope>/silver/ in the registry's silver bucket for the scope's tenancy and prints:
the partitions listed, the id column found, per partition the rows and the distinct ids, the union of distinct ids over the partitions read against the sum of their rows, and the share of
ids present in two or more of the partitions read. A table whose partitions repeat the same transaction reads sum(rows) far above the union. No id value, account or figure is printed.
"""
import io
import sys
from collections import Counter
from pathlib import Path

import boto3
import pyarrow as pa
import pyarrow.parquet as pq
from botocore.config import Config

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "lib"))
import opal_naming  # noqa: E402

ID_CANDIDATES = ("TransactionID", "id", "transaction_id", "transactionId")
s3 = boto3.client("s3", config=Config(max_pool_connections=8, retries={"max_attempts": 5}))


def main(firm, source, scope, n, table="fact_transactions"):
    reg = opal_naming.load_registry()
    row = opal_naming.lookup(firm)
    bucket = reg["tiers"]["homes"][row["tenancy"]]["silver"]["bucket"]
    prefix = "%s/%s/silver/%s/" % (source, scope, table)
    days = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
        for c in page.get("CommonPrefixes", []) or []:
            name = c["Prefix"][len(prefix):].strip("/")
            if name.startswith("date="):
                days.append(name[len("date="):])
    days.sort()
    print("%s/%s: bucket tenancy %s, partitions listed %d (newest %s)" % (source, scope, row["tenancy"], len(days), days[-1] if days else None))
    union = Counter()
    total = 0
    used = 0
    id_col = None
    for day in days[-n:]:
        tables = []
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix="%sdate=%s/" % (prefix, day)):
            for o in page.get("Contents", []) or []:
                if o["Key"].endswith(".parquet"):
                    f = pq.ParquetFile(io.BytesIO(s3.get_object(Bucket=bucket, Key=o["Key"])["Body"].read()))
                    col = next((c for c in ID_CANDIDATES if c in f.schema_arrow.names), None)
                    if col is None:
                        print("  %s: no id column among %s; column names: %s" % (day, ID_CANDIDATES, f.schema_arrow.names))
                        continue
                    id_col = col
                    tables.append(f.read(columns=[col]))
        if not tables:
            continue
        ids = [str(v) for v in pa.concat_tables(tables, promote_options="default").column(0).to_pylist() if v is not None]
        d = set(ids)
        total += len(ids)
        used += 1
        for i in d:
            union[i] += 1
        print("  date=%s: rows %d, distinct ids %d" % (day, len(ids), len(d)))
    multi = sum(1 for v in union.values() if v >= 2)
    print("id column %s; partitions read %d; sum of rows %d; union of distinct ids %d; ids present in 2 or more partitions: %d (%.1f%%)"
          % (id_col, used, total, len(union), multi, 100.0 * multi / len(union) if union else 0.0))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 6, sys.argv[5] if len(sys.argv) > 5 else "fact_transactions")
