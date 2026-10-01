"""Shared reads for HVST-p-1's issuer checks (2.0.0_SA_COO~H). Read-only against S3.

`dry_build()` runs the producer's OWN `publication_gold.build_mention` against a stub client: every read passes through to
the real S3 client, and `put_object` / `head_object` on the one gold key are captured in memory. The captured parquet IS
the expected write (round-25 ruling 1: a stub put-count dry run of the command that reaches the put).
"""
import datetime
import io
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

UNIVERSE = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~46/securities.universe.json")
WK = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~66")
SIGNING = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round26/p1_signing_expected.json")


class CapturingClient:
    """Pass-through S3 client that captures puts instead of sending them."""

    def __init__(self, real):
        self._real = real
        self.puts = {}

    def put_object(self, Bucket, Key, Body, **kw):
        self.puts[Key] = {"body": Body, "kwargs": sorted(kw)}
        return {"ETag": '"captured"'}

    def head_object(self, Bucket, Key, **kw):
        if Key in self.puts:
            return {"ContentLength": len(self.puts[Key]["body"])}
        return self._real.head_object(Bucket=Bucket, Key=Key, **kw)

    def __getattr__(self, name):
        return getattr(self._real, name)


def securities():
    with open(UNIVERSE, encoding="utf-8") as fh:
        return json.load(fh)


def gold_prefix():
    return store.table_prefix("amgt", "gold", pg.GOLD_TABLE)


def list_parts(cl=None):
    cl = cl or store._default_client()
    out = {}
    for page in cl.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=gold_prefix()):
        for obj in page.get("Contents", []) or []:
            out[obj["Key"]] = [obj["ETag"].strip('"'), obj["Size"]]
    return out


def norm_rows(rows):
    """{(article_key, security_key): canonical JSON of the row} -- comparable across builds."""
    out = {}
    for r in rows:
        k = "%s|%s" % (r.get("article_key"), r.get("security_key"))
        out[k] = json.dumps(r, sort_keys=True, default=str)
    return out


def dry_build(as_of=None):
    as_of = as_of or datetime.datetime.now(datetime.timezone.utc).date()
    cl = CapturingClient(store._default_client())
    summary = pg.build_mention(securities(), as_of, client=cl)
    if len(cl.puts) != 1:
        raise SystemExit("dry build captured %d puts, expected exactly 1" % len(cl.puts))
    key, put = next(iter(cl.puts.items()))
    rows = pq.read_table(io.BytesIO(put["body"])).to_pylist()
    return summary, key, rows


def served_rows():
    return pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True, default=str)
