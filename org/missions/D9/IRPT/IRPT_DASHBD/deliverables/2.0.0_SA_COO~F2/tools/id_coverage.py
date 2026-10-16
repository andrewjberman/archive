"""IRPT_DASHBD (workstream F-SHIP, ~F2): a READ-ONLY, VALUES-FREE coverage count of a firm's per-transaction identifier columns, for the
transaction contract's `source_txn_id` statement (CTO msg 9192: the contract gives `source_txn_id` a per-row claim and states the coverage per
firm WITH ITS DENOMINATOR; it is never presented as a universal key).

  python <this file> <firm> <out.json> [seed] [n_partitions]      firm: 49financial | cottonwood | inflection
                                                                     defaults: seed 130, n_partitions 12 (0 = every partition)

For a seeded draw of `n_partitions` partitions (or every partition when 0), and for each id-like column the firm's table has, it counts the
rows, the non-null (and non-blank) rows, and, WITHIN EACH PARTITION (the grain of the CTO's uniqueness rule, msg 9192), the rows whose value
occurs more than once and the partitions that hold any such value. It writes counts only: no identifier value, no account id, no amount. GET
requests only. A sample is a sample: coverage varies by period, so a statement about the table is made over every partition. Run from the repository root with the box's AWS credentials; needs boto3 and pyarrow.
"""
import datetime as dt
import importlib.util
import io
import json
import random
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

ID_COLUMNS = {
    "49financial": ["cashiering_transaction_identifier", "schwab_cashiering_unique_id", "order_number"],
    "cottonwood": ["TransactionID"],
    "inflection": ["id", "orderId", "tradeOrderId"],
}
s3 = boto3.client("s3", config=Config(max_pool_connections=8, retries={"max_attempts": 5}))


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def where(firm):
    if firm == "49financial":
        src = json.load(open(ROOT / "data/assets/scripts/gold/irpt_reporting/sources.json", encoding="utf-8"))["schwab_08335338"]
        return src["bucket"], src["transactions_prefix"]
    if firm == "cottonwood":
        cbd = load("cbd", "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_bd_account_return_daily.py")
        return cbd.BUCKET, cbd.SILVER_ROOT + "fact_transactions/"
    iar = load("iar", "data/assets/scripts/gold/irpt_reporting/adapters/inflection_account_return_daily.py")
    bucket, _, rest = iar.ORION_SILVER[len("s3://"):].partition("/")
    return bucket, rest + "fact_transactions/"


def keys_of(bucket, prefix, day):
    out = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix="%sdate=%s/" % (prefix, day)):
        for o in page.get("Contents", []) or []:
            if o["Key"].endswith(".parquet"):
                out.append(o["Key"])
    return sorted(out)


def main(firm, out_path, seed=130, n_partitions=12):
    bucket, prefix = where(firm)
    days = ard.partition_days(s3, bucket, prefix)
    picked = days if not n_partitions or n_partitions >= len(days) else sorted(random.Random(seed).sample(days, n_partitions))
    cols = ID_COLUMNS[firm]
    present = None
    rows = 0
    non_null = {c: 0 for c in cols}
    dup_rows = {c: 0 for c in cols}
    dup_partitions = {c: set() for c in cols}
    for day in picked:
        part_tables = []
        for k in keys_of(bucket, prefix, day):
            raw = s3.get_object(Bucket=bucket, Key=k)["Body"].read()
            names = pq.read_schema(io.BytesIO(raw)).names
            use = [c for c in cols if c in names]
            if present is None:
                present = use
            rows += pq.read_metadata(io.BytesIO(raw)).num_rows
            if use:
                part_tables.append(pq.read_table(io.BytesIO(raw), columns=use))
        if not part_tables:
            continue
        t = pa.concat_tables(part_tables, promote_options="default")
        for c in cols:
            if c not in t.column_names:
                continue
            col = pc.cast(t.column(c), pa.string())
            col = pc.filter(col, pc.and_(pc.is_valid(col), pc.not_equal(pc.utf8_trim_whitespace(col), "")))
            non_null[c] += len(col)
            if len(col):
                vc = pc.value_counts(col)
                counts = vc.field("counts")
                dups = pc.filter(counts, pc.greater(counts, 1))
                if len(dups):
                    dup_rows[c] += int(pc.sum(dups).as_py())
                    dup_partitions[c].add(day)
    out = {"firm": firm, "read_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "seed": seed,
           "partitions_in_table": len(days), "partitions_read": len(picked), "all_partitions": len(picked) == len(days), "rows": rows,
           "columns": {c: {"present_in_schema": c in (present or []), "non_null": non_null[c],
                           "share_non_null": round(non_null[c] / rows, 6) if rows else None,
                           "rows_in_values_repeated_within_a_partition": dup_rows[c],
                           "partitions_with_a_repeated_value": len(dup_partitions[c]),
                           "unique_within_every_partition": not dup_partitions[c]} for c in cols},
           "reader": "values-free: counts of non-null rows and of rows whose value repeats within a partition; no identifier value is kept or written"}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    print(firm, "partitions", len(picked), "of", len(days), "rows", rows,
          {c: (v["non_null"], v["rows_in_values_repeated_within_a_partition"]) for c, v in out["columns"].items()})


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ID_COLUMNS:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 130, int(sys.argv[4]) if len(sys.argv) > 4 else 12)
