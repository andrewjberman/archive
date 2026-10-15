"""IRPT_DASHBD round 120, workstream B-49F, cell DB-b-239 (worker 0.9.0_WK_IRPT_DASHBD~193).

The Black Diamond BRONZE read for the empty silver days, and the Commonwealth-to-Black-Diamond KEY-MAP count over ALL
non-empty fact_allocations partitions (CTO analysis ruling 3, round 120).

READ ONLY. S3 LIST and GET of the Cottonwood Black Diamond silver prefix (the NFS custodian column and the row count of
every fact_allocations partition), the LIST of the bronze allocations prefix (object keys and sizes only; no workbook is
read), and the Cottonwood account_return_daily gold prefix derived by lib/opal_naming.py address() (the account_id
column of every partition). No write call of any kind. The one file written is the history ids file, under the private
client evidence folder. Prints counts, dates, sizes and words only; no account id or key is printed.
"""
import hashlib
import io
import json
import re
import sys
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(ROOT))
from lib import opal_naming  # noqa: E402

BUCKET = "opal-data-assets"
SILVER = "blackdiamond/cottonwood/silver/"
BRONZE_ALLOC = "blackdiamond/cottonwood/bronze/allocations/"
TABLE = "fact_allocations"
CUSTODIAN = "NFS Account Number"
FIRM = "cottonwood"
GOLD_TABLE = "account_return_daily"
FRONTIER = "2026-06-22"
NORMS = ("exact", "strip_leading_zeros", "zero_pad_10")
PRIVATE = Path("C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~193")
IDS_FILE = PRIVATE / "history_ids.txt"
WORKERS = 8
CALLS = {"list": 0, "get": 0}
LOCK = threading.Lock()


def bump(kind):
    with LOCK:
        CALLS[kind] += 1


def norm(x, how):
    s = str(x).strip()
    if how == "strip_leading_zeros":
        return s.lstrip("0")
    if how == "zero_pad_10":
        return s.zfill(10)
    return s


def mapped_count(ids, custodian_values, how):
    vals = {norm(v, how) for v in custodian_values if v is not None}
    return sum(1 for i in ids if norm(i, how) in vals)


def verdict_of(empty_days, sizes, nonempty_min):
    present = [d for d in empty_days if d in sizes]
    if not present:
        return "BRONZE_ABSENT"
    if len(present) == len(empty_days) and all(sizes[d] < nonempty_min for d in present):
        return "SOURCE_EMPTY"
    if any(sizes[d] >= nonempty_min for d in present):
        return "SILVER_BUILD_GAP"
    return "MIXED"


def partition_dates(s3, bucket, prefix):
    dates = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
        bump("list")
        for c in page.get("CommonPrefixes", []):
            if "date=" in c["Prefix"]:
                dates.append(c["Prefix"].rstrip("/").rsplit("date=", 1)[1])
    return sorted(dates)


def object_rows(s3, bucket, prefix):
    rows = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
        bump("list")
        rows += page.get("Contents", [])
    return rows


def get_bytes(s3, bucket, key):
    bump("get")
    return s3.get_object(Bucket=bucket, Key=key)["Body"].read()


def read_silver(args):
    s3, day = args
    body = get_bytes(s3, BUCKET, "%sfact_allocations/date=%s/data.parquet" % (SILVER, day))
    t = pq.read_table(io.BytesIO(body), columns=[CUSTODIAN])
    return day, t.num_rows, t.column(CUSTODIAN).to_pylist()


def read_history(args):
    s3, gbucket, gprefix, day = args
    body = get_bytes(s3, gbucket, "%sdate=%s/data.parquet" % (gprefix, day))
    return day, pq.read_table(io.BytesIO(body), columns=["account_id"]).to_pydict()["account_id"]


def main():
    s3 = boto3.client("s3")

    # silver: every fact_allocations partition, row count and custodian column
    dates = partition_dates(s3, BUCKET, SILVER + TABLE + "/")
    with ThreadPoolExecutor(WORKERS) as ex:
        got = list(ex.map(read_silver, [(s3, d) for d in dates]))
    empty = [d for d, n, _ in got if n == 0]
    nonempty = [d for d, n, _ in got if n > 0]
    custodian = [v for _, n, vals in got if n > 0 for v in vals]
    nonempty_rows = sum(n for _, n, _ in got if n > 0)

    # bronze: one LIST of the allocations prefix, keys and sizes only
    rows = object_rows(s3, BUCKET, BRONZE_ALLOC)
    sizes = {}
    for o in rows:
        m = re.search(r"ALLOCATIONS_DAILY_(\d{4}-\d{2}-\d{2})\.xlsx$", o["Key"])
        if m:
            sizes[m.group(1)] = o["Size"]
    nonempty_sizes = [sizes[d] for d in nonempty if d in sizes]
    nonempty_min = min(nonempty_sizes)
    empty_objects = [{"date": d, "present": d in sizes, "bytes": sizes.get(d)} for d in empty]
    gap = [d for d in empty if d in sizes and sizes[d] >= nonempty_min]
    verdict = verdict_of(empty, sizes, nonempty_min)

    # gold: the Cottonwood account_return_daily history, every partition, account_id column
    probe = opal_naming.address("irpt", FIRM, "gold", GOLD_TABLE, "date=%s" % FRONTIER)
    gbucket, gkey = probe[len("s3://"):].split("/", 1)
    gprefix = gkey.rsplit("date=", 1)[0]
    gdates = partition_dates(s3, gbucket, gprefix)
    with ThreadPoolExecutor(WORKERS) as ex:
        hist = list(ex.map(read_history, [(s3, gbucket, gprefix, d) for d in gdates]))
    frontier_ids = dict(hist)[FRONTIER]
    fr_set = set(frontier_ids)
    all_ids = set()
    null_hist = 0
    types = Counter()
    for _, ids in hist:
        for x in ids:
            types[type(x).__name__] += 1
            if x is None:
                null_hist += 1
            else:
                all_ids.add(str(x))

    # the history ids file: private, never in the repo
    lines = sorted(all_ids)
    data = ("\n".join(lines) + "\n").encode("utf-8")
    PRIVATE.mkdir(parents=True, exist_ok=True)
    IDS_FILE.write_bytes(data)
    sha = hashlib.sha256(data).hexdigest()

    # the map over ALL non-empty partitions, under each normalisation; exact unless another is strictly better
    custodian_vals = set(norm(v, "exact") for v in custodian if v is not None)
    mh = {how: mapped_count(all_ids, custodian, how) for how in NORMS}
    mf = {how: mapped_count(fr_set, custodian, how) for how in NORMS}
    pick = max(NORMS, key=lambda h: (mh[h], -NORMS.index(h)))

    summary = {
        "silver": {
            "partitions": len(dates),
            "empty_days": empty,
            "empty_days_count": len(empty),
            "first_empty": empty[0] if empty else None,
            "last_empty": empty[-1] if empty else None,
            "nonempty_days": len(nonempty),
            "nonempty_rows": nonempty_rows,
            "custodian_distinct_nonnull": len(custodian_vals),
            "custodian_nulls": sum(1 for v in custodian if v is None),
        },
        "bronze": {
            "object_pattern": "allocations/ALLOCATIONS_DAILY_<date>.xlsx",
            "keys_listed": len(rows),
            "daily_objects": len(sizes),
            "empty_day_objects": empty_objects,
            "empty_day_present": sum(1 for o in empty_objects if o["present"]),
            "empty_day_size_counts": {str(k): v for k, v in sorted(Counter(o["bytes"] for o in empty_objects if o["present"]).items())},
            "nonempty_day_bytes_min": nonempty_min,
            "nonempty_day_bytes_max": max(nonempty_sizes),
            "gap_days": gap,
            "verdict": verdict,
        },
        "key_map": {
            "table": TABLE,
            "custodian_column": CUSTODIAN,
            "partitions_read": len(nonempty),
            "normalization_chosen": pick,
            "mapped_history_by_normalization": mh,
            "mapped_frontier_by_normalization": mf,
            "history_partitions": len(gdates),
            "frontier_partition": gdates[-1],
            "history_ids_distinct": len(all_ids),
            "history_null_ids": null_hist,
            "frontier_ids": len(fr_set),
            "frontier_null_ids": sum(1 for x in frontier_ids if x is None),
            "id_types": dict(types),
        },
        "history_ids_file": {"bytes": len(data), "sha256": sha, "lines": len(lines)},
        "calls": {"list": CALLS["list"], "get": CALLS["get"], "total": CALLS["list"] + CALLS["get"]},
    }
    print(json.dumps(summary, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
