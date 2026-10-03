"""IRPT_DASHBD TO-DB-b-15 -- read every dim_balance partition ONCE (account_id, net_mv_plus_cash, margin_balance) and cache it locally,
so the inception scan under both value bases, the null counts and the sign check all read the same bytes. READS ONLY: S3 get/list;
nothing is written to S3; no vendor call.

Usage: python scan_balance_history_r8.py <repo_root> <cache_dir> [workers]
Writes <cache_dir>/<day>.parquet for each partition and <cache_dir>/_summary.json.
"""
import importlib.util
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
from botocore.config import Config

root = Path(sys.argv[1]).resolve()
cache = Path(sys.argv[2])
workers = int(sys.argv[3]) if len(sys.argv) > 3 else 12
cache.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(root))
spec = importlib.util.spec_from_file_location("ard", root / "data/assets/scripts/gold/irpt_reporting/account_return_daily.py")
ard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ard)
s3 = boto3.client("s3", config=Config(max_pool_connections=32, retries={"max_attempts": 6, "mode": "adaptive"}))
doc = ard.load_declaration()
src = ard.source_entry(doc, ard.declared_sources(doc)[0])
days = ard.partition_days(s3, src["bucket"], src["balance_prefix"])
print("partitions:", len(days), days[0], days[-1], flush=True)
t0 = time.time()


def one(day):
    f = cache / (day + ".parquet")
    if f.is_file():
        return day, "cached", None
    try:
        fr = ard.read_partition(s3, src["bucket"], src["balance_prefix"], day,
                                columns=["account_id", "net_mv_plus_cash", "margin_balance"])
    except SystemExit as exc:
        # a partition without margin_balance fails the projection; fall back to the two columns and say so
        fr2 = ard.read_partition(s3, src["bucket"], src["balance_prefix"], day, columns=["account_id", "net_mv_plus_cash"])
        fr2["margin_balance"] = float("nan")
        fr2.attrs["no_margin_column"] = True
        fr2.to_parquet(f)
        return day, "NO_MARGIN_COLUMN", str(exc)[:120]
    if fr is None:
        return day, "absent", None
    fr.to_parquet(f)
    return day, "ok", None


status = {}
with ThreadPoolExecutor(workers) as ex:
    for i, (day, st, note) in enumerate(ex.map(one, days), 1):
        status[day] = [st, note]
        if i % 25 == 0 or i == len(days):
            print("  %d/%d  %.0fs" % (i, len(days), time.time() - t0), flush=True)
(cache / "_summary.json").write_text(json.dumps({"days": days, "status": status}), encoding="utf-8")
print("done", round(time.time() - t0), "s", flush=True)
