"""IRPT_DASHBD TO-DB-b-79 -- land Orion's GROSS-of-fees account TWR for Inflection (database 4698) as a silver input.

Reuses orion_gross_fee_pull.py (round 37, copied beside this file): the saved query 'Performance Dim' with the performance
option's feeMethod overridden to Gross Of Fees, over the Rolling 3-Year window ending --end. READ-ONLY on Orion; the credential is
read from its secret for the call only and never printed or written. ONE silver write: a parquet and a manifest under the
lib/opal_naming.py address() output for master 4698. No address is typed.

Usage (repo root): python <this file> --end 2026-10-08 --scratch .scratch --record <ORION_GROSS_SILVER.json> [--land]
Without --land nothing is written to S3 (the pull and the frame are built and summarised).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import sys
import time
from pathlib import Path

import boto3
import pandas as pd
import requests

HERE = Path(__file__).resolve().parent
ROOT = HERE
while ROOT != ROOT.parent and not (ROOT / "lib" / "opal_naming.py").is_file():
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(HERE))
import opal_naming  # noqa: E402
import orion_gross_fee_pull as pull  # noqa: E402

HASH_SALT = "irpt-r36-orion"
MASTER = "4698"
SOURCE, TIER, TABLE = "orion", "silver", "account_performance_gross"


def hashed(account_id):
    return hashlib.sha256(("%s|%s" % (HASH_SALT, account_id)).encode("ascii")).hexdigest()[:16]


def legacy_bucket():
    row = opal_naming.lookup(opal_naming.lookup(MASTER)["firm"])
    hits = [a["spelling"] for a in row.get("aliases", []) if "bucket" in a.get("planes", []) and a.get("routed")]
    if len(hits) != 1:
        raise SystemExit("REFUSED: %d routed bucket aliases" % len(hits))
    return hits[0]


def pct(series):
    return pd.to_numeric(series.astype(str).str.replace("%", "", regex=False).str.replace(",", "", regex=False).str.strip(), errors="coerce")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--end", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--record", required=True)
    ap.add_argument("--land", action="store_true")
    ap.add_argument("--min-jwt-minutes", type=int, default=30)
    args = ap.parse_args()
    end = dt.date.fromisoformat(args.end)
    pull.MIN_JWT_MINUTES = args.min_jwt_minutes
    scratch = Path(args.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    csv = scratch / "orion_perf_gross_b79.csv"
    if not csv.is_file():
        token = pull.read_token(legacy_bucket())
        catalog = requests.get(pull.BASE + "/api/v1/Reporting/Envision/ExcelReports", headers=pull.headers(token), timeout=30).json()
        query = [q for q in catalog if q.get("name") == "Performance Dim"][0]
        verbose = requests.get("%s/api/v1/Reporting/Envision/ExcelReports/Verbose/%s" % (pull.BASE, query["id"]),
                               headers=pull.headers(token), params={"expand": "all"}, timeout=30).json()
        for attempt in (1, 2, 3):
            try:
                content = pull.run_report(token, pull.generate_body(verbose, query, end, "Gross Of Fees"))
                break
            except SystemExit as exc:
                if attempt == 3 or "not primed" not in str(exc):
                    raise
                print("WARN: attempt %d refused as not primed; retrying" % attempt)
                time.sleep(10)
        csv.write_bytes(content)
    raw = pd.read_csv(csv)
    print("OK: gross csv %d rows, columns %s" % (len(raw), list(raw.columns)))
    methods = sorted(raw["Performance FeeMethod"].dropna().unique())
    if methods != ["Gross of Fees"]:
        raise SystemExit("REFUSED: fee methods %r" % methods)
    df = pd.DataFrame({
        "account_id": pd.to_numeric(raw["Account Id"], errors="coerce").astype("Int64"),
        "twr_gross_value": pct(raw["Performance Value"]).astype("float64"),
        "twr_gross_raw": raw["Performance Value"].astype(str),
        "fee_method": raw["Performance FeeMethod"].astype(str),
        "date_range_start": pd.to_datetime(raw["DateRange StartDate"], format="%m/%d/%Y %I:%M %p").dt.strftime("%Y-%m-%d"),
        "date_range_end": pd.to_datetime(raw["DateRange EndDate"], format="%m/%d/%Y %I:%M %p").dt.strftime("%Y-%m-%d"),
    })
    df["as_of"] = args.end
    ends = sorted(df["date_range_end"].unique())
    if ends != [args.end]:
        raise SystemExit("REFUSED: window ends %r != %s" % (ends, args.end))
    pulled_at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    partition = "snapshot_date=%s" % args.end
    call = "opal_naming.address(%r, %r, %r, %r, %r)" % (SOURCE, MASTER, TIER, TABLE, partition)
    address = opal_naming.address(SOURCE, MASTER, TIER, TABLE, partition)
    obj_call = "opal_naming.address(%r, %r, %r, %r, %r, object=%r)" % (SOURCE, MASTER, TIER, TABLE, partition, "data.parquet")
    parquet_addr = opal_naming.address(SOURCE, MASTER, TIER, TABLE, partition, object="data.parquet")
    manifest_addr = opal_naming.address(SOURCE, MASTER, TIER, TABLE, partition, object="manifest.json")
    print("builder_call: %s -> %s" % (call, address))
    summary = {"rows": int(len(df)), "distinct_accounts": int(df["account_id"].nunique()), "null_value": int(df["twr_gross_value"].isna().sum()),
               "window_start_min": df["date_range_start"].min(), "window_start_max": df["date_range_start"].max(), "distinct_window_starts": int(df["date_range_start"].nunique()), "window_ends": ends}
    print("OK: frame %s" % json.dumps(summary))
    manifest = {
        "as_of": args.end, "pulled_at_utc": pulled_at, "master": MASTER, "firm": "inflection", "vendor": "orion",
        "query": {"saved_query": "Performance Dim", "api": "Orion Connect Envision ExcelReports Generate (read-only)",
                  "database_id": pull.DATABASE_ID, "performance_option_override": {"feeMethod": "Gross Of Fees", "prompt": "Always"},
                  "window": "Rolling 3-Year", "window_start": sorted(df["date_range_start"].unique())[0], "window_end": args.end},
        "rows": int(len(df)), "columns": list(df.columns), "value_unit": "percent (twr_gross_value is the number before the % sign)",
        "basis": "measured", "note": "gross of fees, before tax, annualized account TWR as Orion reports it; the tie-out reads this landed figure, never a live pull",
    }
    if not args.land:
        print("DRY: nothing written")
        return
    s3 = boto3.client("s3", region_name="us-east-1")
    bucket, key = parquet_addr[len("s3://"):].split("/", 1)
    buf = io.BytesIO()
    df.to_parquet(buf, index=False)
    s3.put_object(Bucket=bucket, Key=key, Body=buf.getvalue())
    mbucket, mkey = manifest_addr[len("s3://"):].split("/", 1)
    s3.put_object(Bucket=mbucket, Key=mkey, Body=(json.dumps(manifest, indent=1) + "\n").encode("utf-8"), ContentType="application/json")
    pfx = address[len("s3://"):].split("/", 1)[1] + "/"
    listing = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=pfx):
        listing += [(o["Key"], o["Size"]) for o in page.get("Contents", [])]
    back = pd.read_parquet(io.BytesIO(s3.get_object(Bucket=bucket, Key=key)["Body"].read()))
    print("OK: listing %s; read-back parquet %d rows" % (listing, len(back)))
    rec = {
        "record_version": "1.0", "task_order": "IRPT_DASHBD.TO-DB-b-79",
        "address": address, "as_of": args.end, "pulled_at_utc": pulled_at,
        "builder_call": {"call": call, "output": address},
        "object_addresses": {"parquet": {"call": obj_call, "output": parquet_addr},
                             "manifest": {"call": obj_call.replace("data.parquet", "manifest.json"), "output": manifest_addr}},
        "rows": int(len(back)), "distinct_accounts": summary["distinct_accounts"], "null_value": summary["null_value"],
        "objects": len(listing), "objects_listing": [{"key": k.split("/")[-1], "bytes": s} for k, s in listing],
        "columns": list(back.columns),
        "query": manifest["query"],
        "fee_method_values": methods,
        "hash_note": "no account id in this record; sample keys are sha256(%s|account_id)[:16]" % HASH_SALT,
        "sample_hashed_keys": [hashed(a) for a in back["account_id"].dropna().astype(int).head(3)],
    }
    Path(args.record).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print("OK: record written")


if __name__ == "__main__":
    main()
