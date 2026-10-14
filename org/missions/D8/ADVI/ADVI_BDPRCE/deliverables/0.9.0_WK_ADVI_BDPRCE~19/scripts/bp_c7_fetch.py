#!/usr/bin/env python3
"""BP-c-7 fetch, ADVI_BDPRCE round 3. Worker 0.9.0_WK_ADVI_BDPRCE~19. READ-ONLY.

Reads (get-object and list-object-versions only):
  s3://opal-data-bd/silver/prices/canonical_prices.parquet   every version (listing, then one get per version)
  s3://opal-data-bd/silver/prices/<date>.parquet             every version of every daily file (listing, then get)
Writes (outside the checkout):
  C:/dev/wk-bdprce-r3-19-data/proj/*.parquet                 per-version PROJECTION: only rows whose asset_name is one
                                                             of the off-canonical assets, or whose ticker is one of
                                                             their tickers. Full object copies are deleted after projection.
  C:/dev/wk-bdprce-r3-19-data/fetch_log.json                 one line per object version: key, version id, ok/fail.
Inputs (outside the checkout): the round-2 extract and ticker lookup, sha256-checked by the caller.
Run from the worktree root:  python -I <this file>
"""
import concurrent.futures as cf
import csv
import json
import os
import sys
import time

import boto3
import botocore.config
import pyarrow as pa
import pyarrow.parquet as pq

DATA = "C:/dev/wk-bdprce-r3-19-data"
R2 = "C:/dev/wk-bdprce-r2-7-data"
BUCKET = "opal-data-bd"
PREFIX = "silver/prices/"
CANON = "silver/prices/canonical_prices.parquet"
THREADS = 6
COLS = ["date", "asset_name", "ticker", "price", "source"]


def log(msg):
    print(msg, flush=True)


def off_sets():
    """Off-canonical asset names and their tickers, from the round-2 extract and ticker lookup."""
    assets = set()
    with open(f"{R2}/lot_extract.csv", newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["price_class"] == "PRICED_OFF_NO_CANONICAL":
                assets.add(row["asset_name"])
    lookup = json.load(open(f"{R2}/ticker_lookup.json", encoding="utf-8"))
    tickers = set()
    for e in lookup:
        t = (e.get("ticker") or "").strip().upper()
        if e.get("asset_name") in assets and t not in ("", "UNKNOWN"):
            tickers.add(t)
    return assets, tickers


def list_versions(client):
    out = []
    pag = client.get_paginator("list_object_versions")
    for page in pag.paginate(Bucket=BUCKET, Prefix=PREFIX):
        for v in page.get("Versions", []):
            out.append({"Key": v["Key"], "VersionId": v["VersionId"], "LastModified": v["LastModified"].isoformat(),
                        "Size": v["Size"], "IsLatest": v["IsLatest"]})
    return out


def project_one(client, item, assets, tickers, idx):
    key, vid = item["Key"], item["VersionId"]
    safe = vid.replace("/", "_").replace("+", "-")
    tag = "canon" if key == CANON else "daily"
    stem = key.split("/")[-1].replace(".parquet", "")
    outp = f"{DATA}/proj/{tag}_{stem}_{idx:05d}_{safe}.parquet"
    if os.path.exists(outp):
        return {"key": key, "version_id": vid, "status": "cached", "rows_kept": None}
    full = f"{DATA}/versions/{idx:05d}_{safe}.parquet"
    try:
        client.download_file(BUCKET, key, full, ExtraArgs={"VersionId": vid})
        t = pq.read_table(full, columns=COLS)
        names = t.column("asset_name").to_pylist()
        tks = t.column("ticker").to_pylist()
        keep = [
            i for i, (n, tk) in enumerate(zip(names, tks))
            if (n is not None and n in assets) or (tk is not None and str(tk).strip().upper() in tickers)
        ]
        sub = t.take(pa.array(keep, type=pa.int64())) if keep else t.slice(0, 0)
        sub = sub.append_column("version_id", pa.array([vid] * sub.num_rows, type=pa.string()))
        sub = sub.append_column("object_key", pa.array([key] * sub.num_rows, type=pa.string()))
        sub = sub.append_column("last_modified", pa.array([item["LastModified"]] * sub.num_rows, type=pa.string()))
        pq.write_table(sub, outp)
        return {"key": key, "version_id": vid, "status": "ok", "rows_total": t.num_rows, "rows_kept": sub.num_rows}
    except Exception as e:  # recorded, never swallowed
        return {"key": key, "version_id": vid, "status": "fail", "error": f"{type(e).__name__}: {str(e)[:200]}"}
    finally:
        if os.path.exists(full):
            os.remove(full)


def main():
    os.makedirs(f"{DATA}/proj", exist_ok=True)
    os.makedirs(f"{DATA}/versions", exist_ok=True)
    assets, tickers = off_sets()
    log(f"OK: off-canonical assets={len(assets)} tickers={len(tickers)}")
    cfg = botocore.config.Config(retries={"max_attempts": 4, "mode": "standard"}, max_pool_connections=THREADS + 2)
    client = boto3.client("s3", config=cfg)
    versions = list_versions(client)
    # Only parquet objects (canonical and daily files); newest first, so the widening order is by time.
    items = [v for v in versions if v["Key"].endswith(".parquet") and not v["Key"].endswith("backfill_telemetry.json")]
    items.sort(key=lambda v: v["LastModified"], reverse=True)
    canon_n = sum(1 for v in items if v["Key"] == CANON)
    log(f"OK: listed parquet versions={len(items)} canonical={canon_n} daily={len(items) - canon_n}")
    results = []
    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=THREADS) as pool:
        futs = {pool.submit(project_one, client, it, assets, tickers, i): i for i, it in enumerate(items)}
        done = 0
        for f in cf.as_completed(futs):
            results.append(f.result())
            done += 1
            if done % 25 == 0 or done == len(items):
                log(f"PROGRESS {done}/{len(items)} elapsed={int(time.time() - t0)}s")
    results.sort(key=lambda r: (r["key"], r["version_id"]))
    json.dump({"listed": len(items), "results": results}, open(f"{DATA}/fetch_log.json", "w"), indent=1)
    ok = sum(1 for r in results if r["status"] in ("ok", "cached"))
    fail = [r for r in results if r["status"] == "fail"]
    log(f"DONE ok_or_cached={ok} fail={len(fail)} of listed={len(items)}")


if __name__ == "__main__":
    sys.exit(main())
