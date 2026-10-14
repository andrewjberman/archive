"""Read-only dry run of the Cottonwood account_dim adapter over Cottonwood's REAL silver (round 103, DB-b-196).

Reads ONLY: S3 LIST and GET under blackdiamond/cottonwood/silver/fact_holdings/ and
blackdiamond/cottonwood/silver/fact_allocations/ in opal-data-assets. Writes NOTHING to S3.
The table is written ONLY to the private evidence folder; this script prints COUNTS only.

Usage: python -I dry_run_account_dim.py <repo_root> <private_out_dir> <as_of>
"""
import importlib.util
import io
import json
import sys
from pathlib import Path

import boto3
import pyarrow.parquet as pq

BUCKET = "opal-data-assets"
SILVER = "blackdiamond/cottonwood/silver/"
TABLES = ("fact_holdings", "fact_allocations")


def load_adapter(root):
    path = root / "data" / "assets" / "scripts" / "gold" / "irpt_reporting" / "adapters" / "cottonwood_account_dim.py"
    spec = importlib.util.spec_from_file_location("cottonwood_account_dim", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def latest_partition(s3, table, as_of):
    """LIST the table's date partitions (delimiter listing) and return the latest one <= as_of."""
    prefix = "%s%s/" % (SILVER, table)
    dates = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix, Delimiter="/"):
        for cp in page.get("CommonPrefixes", []):
            seg = cp["Prefix"][len(prefix):].rstrip("/")
            if seg.startswith("date=") and seg[5:] <= as_of:
                dates.append(seg[5:])
    if not dates:
        raise SystemExit("REFUSE: no %s partition <= %s" % (table, as_of))
    return sorted(dates)[-1]


def main():
    root = Path(sys.argv[1]).resolve()
    out_dir = Path(sys.argv[2])
    as_of = sys.argv[3]
    out_dir.mkdir(parents=True, exist_ok=True)
    ad = load_adapter(root)
    s3 = boto3.client("s3", region_name="us-east-1")
    frames, parts, reads = {}, {}, []
    for table in TABLES:
        day = latest_partition(s3, table, as_of)
        key = "%s%s/date=%s/data.parquet" % (SILVER, table, day)
        body = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
        frames[table] = pq.read_table(io.BytesIO(body)).to_pandas()
        parts[table] = day
        reads.append({"bucket": BUCKET, "prefix": "%s%s/" % (SILVER, table)})
    table = ad.build_account_dim(frames["fact_holdings"], frames["fact_allocations"])
    rows = table.to_pylist()
    names = table.column_names
    nulls = {n: sum(1 for r in rows if r[n] is None) for n in names}
    hh = {r["household_id"] for r in rows if r["household_id"] is not None}
    cov = {}
    for r in rows:
        cov[r["coverage"]] = cov.get(r["coverage"], 0) + 1
    multi = sum(1 for r in rows if r["household_relationship_count"] > 1)
    target = ad.emit_account_dim(table, parts["fact_holdings"])
    pq.write_table(table, str(out_dir / "account_dim_dry_run.parquet"))
    result = {
        "partitions_used": parts,
        "prefixes_read": reads,
        "accounts": len(rows),
        "relationship_ids": len(hh),
        "null_counts": nulls,
        "coverage_counts": cov,
        "multi_relationship_accounts": multi,
        "target_address": target["address"],
        "landed": target["landed"],
    }
    (out_dir / "dry_run_counts.json").write_text(json.dumps(result, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
