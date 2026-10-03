"""IRPT_DASHBD TO-DB-b-11 -- MEASURE the publisher (reporting-publish/handler.py run()) at the 49 Financial population.

Reads only. The real 6-account gold history (562 partitions, 2024-07-08..) is read from S3 once, then REPLICATED under synthetic
account ids to the population size, held as parquet bytes IN MEMORY behind a fake S3 client (nothing is written to S3 or disk;
puts are counted and optionally delayed by PUT_LATENCY seconds to stand in for the network). The handler's own run() is then
executed over it, shard by shard, so the read -> build -> bounded-parallel-put path that the Lambda runs is what is timed.

Usage: python p2_publisher_measure_r5.py <repo_root> <population> <shards|0> <put_latency_s> [<history_cache.parquet>]
Prints one JSON line.
"""
import importlib.util
import io
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

root = Path(sys.argv[1]).resolve()
POP = int(sys.argv[2])
SHARDS = int(sys.argv[3])
LAT = float(sys.argv[4])
cache = Path(sys.argv[5]) if len(sys.argv) > 5 else None

spec = importlib.util.spec_from_file_location("rp_handler", root / "infra/aws/lambda/investor-reporting/reporting-publish/handler.py")
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
firm = h.resolve_firm(None)[1]
cols = list(h.publisher.GOLD_COLUMNS)

# ---- the real 6-account history
if cache is not None and cache.is_file():
    real = pq.read_table(cache)
else:
    import boto3
    from botocore.config import Config
    s3r = boto3.client("s3", region_name="us-east-1", config=Config(max_pool_connections=32))
    bucket, by_date = h._gold_objects(s3r, firm)
    keys = [k for d in sorted(by_date) for k in by_date[d]]

    def one(k):
        return pq.read_table(io.BytesIO(s3r.get_object(Bucket=bucket, Key=k)["Body"].read()), columns=cols)

    with ThreadPoolExecutor(12) as ex:
        real = pa.concat_tables(list(ex.map(one, keys)))
    if cache is not None:
        pq.write_table(real, cache)
accts = sorted(set(real["account_id"].to_pylist()))
print("real history: %d rows, %d accounts, %d days" % (real.num_rows, len(accts), len(set(real["business_date"].to_pylist()))), flush=True)

# ---- replicate to the population, one parquet object per day, in memory
ids = ["9%09d" % j for j in range(POP)]
by_src = {a: [ids[j] for j in range(POP) if j % len(accts) == i] for i, a in enumerate(accts)}
days = sorted(set(real["business_date"].to_pylist()))
bd = np.array(real["business_date"].to_pylist())
ac = np.array(real["account_id"].to_pylist())
objects = {}
prefix_probe = h.opal_naming.address("irpt", firm, h.TIER_GOLD, h.TABLE_GOLD, "date=0000-00-00")
bucket, key0 = h._split(prefix_probe)
base = key0.rsplit("/date=", 1)[0]
t0 = time.time()
for d in days:
    parts = []
    for a in accts:
        idx = np.nonzero((bd == d) & (ac == a))[0]
        if not len(idx):
            continue
        reps = by_src[a]
        t = real.take(pa.array(np.repeat(idx, len(reps))))
        t = t.set_column(t.schema.get_field_index("account_id"), "account_id", pa.array(reps, type=t.schema.field("account_id").type))
        parts.append(t)
    buf = io.BytesIO()
    pq.write_table(pa.concat_tables(parts), buf)
    objects["%s/date=%s/data.parquet" % (base, d)] = buf.getvalue()
gold_bytes = sum(len(v) for v in objects.values())
print("synthetic gold: %d partitions, %d accounts on the last day, %.1f MB (built in %.1fs)" % (
    len(objects), sum(len(v) for v in by_src.values()), gold_bytes / 1e6, time.time() - t0), flush=True)


class Body:
    def __init__(self, b):
        self.b = b

    def read(self):
        return self.b


class FakeS3:
    def __init__(self):
        self.puts = 0
        self.heads = 0

    def get_paginator(self, name):
        class P:
            def paginate(self, Bucket, Prefix):
                yield {"Contents": [{"Key": k} for k in sorted(objects) if k.startswith(Prefix)]}
        return P()

    def get_object(self, Bucket, Key):
        return {"Body": Body(objects[Key])}

    def put_object(self, **kw):
        time.sleep(LAT)
        self.puts += 1

    def head_object(self, **kw):
        time.sleep(LAT)
        self.heads += 1
        return {"ContentLength": 1}


def peak_mb():
    try:
        import psutil
        return psutil.Process().memory_info().peak_wset / 1e6
    except Exception:  # noqa: BLE001
        return None


out = {"population": POP, "history_days": len(days), "gold_history_mb": round(gold_bytes / 1e6, 1), "shards": SHARDS,
       "put_latency_s": LAT, "put_workers": h.PUT_WORKERS, "read_workers": h.READ_WORKERS, "runs": []}
for i in (range(SHARDS) if SHARDS else [None]):
    fs = FakeS3()
    t = time.time()
    res = h.run(s3=fs, upload=True, shard=i, shards=SHARDS or None)
    sec = time.time() - t
    out["runs"].append({"shard": i, "accounts": len(res), "ok": sum(1 for r in res if r["ok"]), "seconds": round(sec, 1),
                        "puts": fs.puts, "heads": fs.heads, "peak_working_set_mb": peak_mb()})
    if SHARDS and i >= 1:  # two shards time the per-shard cost; the rest are the same by the hash split
        break
print(json.dumps(out))
