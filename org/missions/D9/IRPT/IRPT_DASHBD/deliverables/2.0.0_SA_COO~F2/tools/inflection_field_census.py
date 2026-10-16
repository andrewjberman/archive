"""IRPT_DASHBD (workstream F-SHIP, ~F2): a READ-ONLY, VALUES-FREE census of the Inflection transaction table's producer-facing fields, for the
Inflection producer's rules (round 131).

  python <this file> <out.json>

Over EVERY partition of the Orion silver `fact_transactions` table it counts: the rows; the rows per `status` value (a vendor enum, not client
data); for each producer-facing column the null (or blank) rows, over ALL rows and over the Complete rows; and, over the Complete rows and per
`transactionDescription` (a vendor enum), whether `navPrice * noUnits` agrees with `transAmount` within one percent (a price-source test: counts
of agree, disagree, zero units and a non-positive navPrice). It writes counts only: no account id, no amount, no price, no identifier, no symbol,
no row. GET requests only. Run from the repository root with the box's AWS credentials; needs boto3 and pyarrow.

Round-131 correction: the first version counted a null string as zero null rows (pc.or_ propagates a null; this one uses or_kleene).
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

COLUMNS = ["status", "transDate", "accountId", "transactionDescription", "transAmount", "noUnits", "avgPrice", "navPrice", "ticker", "productName",
           "custodianName", "id"]
s3 = boto3.client("s3", config=Config(max_pool_connections=8, retries={"max_attempts": 5}))


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def null_or_blank(col):
    """The number of null (or, for text, blank) cells. or_kleene, because is_null is never null and the trimmed comparison is null on a null."""
    if pa.types.is_string(col.type) or pa.types.is_large_string(col.type):
        bad = pc.or_kleene(pc.is_null(col), pc.equal(pc.utf8_trim_whitespace(col), ""))
        return int(pc.sum(pc.cast(bad, pa.int64())).as_py() or 0)
    return int(col.null_count)


def count_true(mask):
    return int(pc.sum(pc.cast(pc.fill_null(mask, False), pa.int64())).as_py() or 0)


def main(out_path):
    iar = load("iar", "data/assets/scripts/gold/irpt_reporting/adapters/inflection_account_return_daily.py")
    bucket, _, rest = iar.ORION_SILVER[len("s3://"):].partition("/")
    prefix = rest + "fact_transactions/"
    days = ard.partition_days(s3, bucket, prefix)
    rows = 0
    status = {}
    nulls_all = {c: 0 for c in COLUMNS}
    nulls_complete = {c: 0 for c in COLUMNS}
    types = {}
    price = {}
    for day in days:
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix="%sdate=%s/" % (prefix, day)):
            for o in page.get("Contents", []) or []:
                if not o["Key"].endswith(".parquet"):
                    continue
                raw = s3.get_object(Bucket=bucket, Key=o["Key"])["Body"].read()
                names = pq.read_schema(io.BytesIO(raw)).names
                t = pq.read_table(io.BytesIO(raw), columns=[c for c in COLUMNS if c in names])
                rows += t.num_rows
                for c in t.column_names:
                    types[c] = str(t.schema.field(c).type)
                    nulls_all[c] += null_or_blank(t.column(c))
                for v in pc.value_counts(t.column("status")).to_pylist():
                    key = "(null)" if v["values"] is None else str(v["values"])
                    status[key] = status.get(key, 0) + int(v["counts"])
                t = t.filter(pc.equal(t.column("status"), "Complete"))
                for c in t.column_names:
                    nulls_complete[c] += null_or_blank(t.column(c))
                amt = pc.cast(t.column("transAmount"), pa.float64())
                units = pc.cast(t.column("noUnits"), pa.float64())
                nav = pc.cast(t.column("navPrice"), pa.float64())
                diff = pc.abs(pc.subtract(pc.multiply(units, nav), amt))
                tol = pc.add(pc.multiply(pc.abs(amt), 0.01), 0.01)
                usable = pc.and_(pc.not_equal(units, 0.0), pc.greater(nav, 0.0))
                agree = pc.and_(usable, pc.less_equal(diff, tol))
                disagree = pc.and_(usable, pc.greater(diff, tol))
                zero_units = pc.equal(units, 0.0)
                bad_nav = pc.and_(pc.not_equal(units, 0.0), pc.less_equal(nav, 0.0))
                desc = t.column("transactionDescription")
                for d in pc.unique(desc).to_pylist():
                    m = pc.equal(desc, d)
                    cell = price.setdefault(str(d), {"agree": 0, "disagree": 0, "zero_units": 0, "units_with_nonpositive_navPrice": 0})
                    cell["agree"] += count_true(pc.and_(agree, m))
                    cell["disagree"] += count_true(pc.and_(disagree, m))
                    cell["zero_units"] += count_true(pc.and_(zero_units, m))
                    cell["units_with_nonpositive_navPrice"] += count_true(pc.and_(bad_nav, m))
        print("read", day, flush=True)
    out = {"firm": "inflection", "read_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "table": "fact_transactions",
           "partitions_in_table": len(days), "partitions_read": len(days), "rows": rows, "rows_per_status": dict(sorted(status.items())),
           "null_or_blank_rows_all": nulls_all, "null_or_blank_rows_complete": nulls_complete, "column_types": types,
           "navprice_times_units_vs_amount_by_description": dict(sorted(price.items())),
           "reader": "values-free: counts of rows per status, of null or blank rows per column, and of price-agreement per description; no value is kept or written"}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    print("rows", rows, "status", out["rows_per_status"])
    print("nulls_all", nulls_all)
    print("nulls_complete", nulls_complete)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
