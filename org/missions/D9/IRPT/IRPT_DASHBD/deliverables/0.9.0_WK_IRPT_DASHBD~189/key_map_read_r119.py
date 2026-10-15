"""IRPT_DASHBD round 119, workstream B-49F, cell DB-b-235 (worker 0.9.0_WK_IRPT_DASHBD~189).

The Commonwealth-to-Black-Diamond KEY-MAP READ: does the Cottonwood Black Diamond silver hold a map from the
Commonwealth custodian number (the account_id key of the Cottonwood account_return_daily gold) to the Black
Diamond account key (AccountID)?

READ ONLY. S3 LIST and GET of the silver prefix blackdiamond/cottonwood/silver/ (bucket opal-data-assets) and of
the gold prefix derived by lib/opal_naming.py address() for the Cottonwood account_return_daily table. No write
call of any kind. Writes one private file under the client evidence folder. Prints counts, table and column
names, dates and words only. No account number or key is printed.
"""
import io
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(ROOT / "lib"))
import opal_naming  # noqa: E402

BUCKET = "opal-data-assets"
SILVER = "blackdiamond/cottonwood/silver/"
FIRM = "cottonwood"
GOLD_TABLE = "account_return_daily"
PROBE_DATE = "date=2026-06-22"
PRIVATE = Path("C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~189")
PRIVATE_FILE = "key_map_read_r119_private.json"
NORMS = ("exact", "strip_leading_zeros", "zero_pad_10")
CUSTODIAN_SUBSTRINGS = ("Account Number", "Account Display Number", "Original Account Number")
MAP_PARTITIONS = 10
WORKERS = 8
CALLS = {"list": 0, "get": 0}


def norm(x, how):
    s = str(x).strip()
    if how == "strip_leading_zeros":
        return s.lstrip("0")
    if how == "zero_pad_10":
        return s.zfill(10)
    return s


def mapped_count(frontier_ids, custodian_values, how):
    vals = {norm(v, how) for v in custodian_values if v is not None}
    return sum(1 for a in frontier_ids if norm(a, how) in vals)


def list_names(s3, bucket, prefix):
    names = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
        CALLS["list"] += 1
        names += [c["Prefix"][len(prefix):].strip("/") for c in page.get("CommonPrefixes", [])]
    return sorted(names)


def list_dates(s3, bucket, prefix):
    return sorted(n[len("date="):] for n in list_names(s3, bucket, prefix) if n.startswith("date="))


def fetch(s3, bucket, key):
    return s3.get_object(Bucket=bucket, Key=key)["Body"].read()


def silver_key(table, day):
    return "%s%s/date=%s/data.parquet" % (SILVER, table, day)


def pick_partitions(parts):
    n = len(parts)
    if n <= MAP_PARTITIONS:
        return list(parts)
    idx = {0, n // 2, n - 1}
    for i in range(MAP_PARTITIONS):
        if len(idx) >= MAP_PARTITIONS:
            break
        idx.add(round(i * (n - 1) / (MAP_PARTITIONS - 1)))
    return [parts[i] for i in sorted(idx)]


def scan_pair(s3, table, dates, key_col, cust_col, frontier_set):
    chosen = pick_partitions(dates)
    read, missing = [], []
    rows_both = 0
    pairs = {}
    vals = set()
    for d in chosen:
        blob = fetch(s3, BUCKET, silver_key(table, d))
        CALLS["get"] += 1
        names = pq.read_schema(io.BytesIO(blob)).names
        if key_col not in names or cust_col not in names:
            missing.append(d)
            continue
        read.append(d)
        cols = pq.read_table(io.BytesIO(blob), columns=[key_col, cust_col]).to_pydict()
        for k, v in zip(cols[key_col], cols[cust_col]):
            if k is None or v is None:
                continue
            rows_both += 1
            pairs.setdefault(str(k).strip(), set()).add(str(v).strip())
            vals.add(v)
    mapped = {how: mapped_count(frontier_set, vals, how) for how in NORMS}
    return {
        "table": table,
        "key_column": key_col,
        "custodian_column": cust_col,
        "partitions_read": read,
        "partitions_missing": missing,
        "rows_both": rows_both,
        "distinct_keys": len(pairs),
        "distinct_custodian_values": len({x for s in pairs.values() for x in s}),
        "keys_with_multiple_custodian_values": sum(1 for s in pairs.values() if len(s) > 1),
        "mapped": mapped,
        "vals": vals,
    }


def main():
    s3 = boto3.client("s3")
    tables = list_names(s3, BUCKET, SILVER)
    dates = {t: list_dates(s3, BUCKET, SILVER + t + "/") for t in tables}
    with_parts = [t for t in tables if dates[t]]
    schemas = {}
    for t in with_parts:
        blob = fetch(s3, BUCKET, silver_key(t, dates[t][-1]))
        CALLS["get"] += 1
        schemas[t] = pq.read_schema(io.BytesIO(blob)).names
    cands = {}
    for t in with_parts:
        keys = [c for c in schemas[t] if c == "AccountID"]
        custs = [c for c in schemas[t] if any(s in c for s in CUSTODIAN_SUBSTRINGS)]
        if keys or custs:
            cands[t] = {"account_key_columns": keys, "custodian_number_columns": custs, "partition_date": dates[t][-1]}

    probe = opal_naming.address("irpt", FIRM, "gold", GOLD_TABLE, PROBE_DATE)
    gbucket, gkey = probe[len("s3://"):].split("/", 1)
    gprefix = gkey.rsplit("date=", 1)[0]
    gdates = list_dates(s3, gbucket, gprefix)
    frontier = gdates[-1]
    gaddr = opal_naming.address("irpt", FIRM, "gold", GOLD_TABLE, "date=%s" % frontier)
    gb, gk = gaddr[len("s3://"):].split("/", 1)
    fr_ids = pq.read_table(io.BytesIO(fetch(s3, gb, gk.rstrip("/") + "/data.parquet")), columns=["account_id"]).to_pydict()["account_id"]
    CALLS["get"] += 1
    fset = set(fr_ids)

    scans = []
    for t in sorted(cands):
        if not cands[t]["account_key_columns"]:
            continue
        for cc in cands[t]["custodian_number_columns"]:
            scans.append(scan_pair(s3, t, dates[t], "AccountID", cc, fset))

    best = None
    for s in scans:
        if s["rows_both"] == 0:
            continue
        top = max(s["mapped"].values())
        if best is None or top > best["top"]:
            pick = [h for h in NORMS if s["mapped"][h] == top][0]
            best = dict(s, top=top, normalization=pick)

    def hist_one(d):
        return pq.read_table(io.BytesIO(fetch(s3, gbucket, "%sdate=%s/data.parquet" % (gprefix, d))), columns=["account_id"]).to_pydict()["account_id"]

    hist = set()
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for ids in ex.map(hist_one, gdates):
            hist.update(ids)
    CALLS["get"] += len(gdates)
    hist_nonnull = {x for x in hist if x is not None}

    out = {
        "tables_listed": len(tables),
        "tables_with_partitions": len(with_parts),
        "tables": {t: {"partitions": len(dates[t]), "newest": dates[t][-1] if dates[t] else None, "columns": schemas.get(t, [])} for t in tables},
        "candidates": cands,
        "frontier": {"date": frontier, "account_ids": len(fset), "null_ids": sum(1 for x in fr_ids if x is None)},
        "scans": [{k: v for k, v in s.items() if k != "vals"} for s in scans],
        "history": {"partitions": len(gdates), "distinct_commonwealth_ids": len(hist_nonnull), "null_ids": sum(1 for x in hist if x is None)},
    }
    if best is not None:
        bn = best["normalization"]
        mh = mapped_count(hist_nonnull, best["vals"], bn)
        out["best"] = {k: v for k, v in best.items() if k != "vals"}
        out["best"]["unmapped"] = len(fset) - best["mapped"][bn]
        out["history"]["mapped_history_ids"] = mh
    out["calls"] = {"list": CALLS["list"], "get": CALLS["get"], "total": CALLS["list"] + CALLS["get"]}

    PRIVATE.mkdir(parents=True, exist_ok=True)
    (PRIVATE / PRIVATE_FILE).write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")

    print("tables_listed %d" % len(tables))
    print("tables_with_partitions %d" % len(with_parts))
    for t in with_parts:
        print("table %s partitions %d newest %s columns %d" % (t, len(dates[t]), dates[t][-1], len(schemas[t])))
    for t in sorted(cands):
        c = cands[t]
        print("candidate %s partition_date %s account_key_columns %s custodian_number_columns %s" % (t, c["partition_date"], c["account_key_columns"], c["custodian_number_columns"]))
    print("frontier date %s account_ids %d null_ids %d" % (frontier, len(fset), out["frontier"]["null_ids"]))
    for s in scans:
        print("scan %s %s %s partitions_read %d missing %d rows_both %d distinct_keys %d multi %d mapped %s" % (
            s["table"], s["key_column"], s["custodian_column"], len(s["partitions_read"]), len(s["partitions_missing"]),
            s["rows_both"], s["distinct_keys"], s["keys_with_multiple_custodian_values"], s["mapped"]))
    if best is not None:
        print("best %s %s %s normalization %s partitions %s" % (best["table"], best["key_column"], best["custodian_column"], best["normalization"], best["partitions_read"]))
        print("best coverage frontier_ids %d mapped %d unmapped %d" % (len(fset), best["top"], out["best"]["unmapped"]))
        print("history mapped_history_ids %d of distinct %d" % (out["history"]["mapped_history_ids"], len(hist_nonnull)))
    else:
        print("best none: no scanned pair holds rows with both columns")
    print("history partitions %d distinct_commonwealth_ids %d null_ids %d" % (len(gdates), len(hist_nonnull), out["history"]["null_ids"]))
    print("calls list %d get %d total %d" % (CALLS["list"], CALLS["get"], CALLS["list"] + CALLS["get"]))


if __name__ == "__main__":
    main()
