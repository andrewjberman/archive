"""Shared read-only core for HVST-m-3 (S3 LIST/GET only; the desktop SQLite opened mode=ro).

No S3 write, no delete, no vendor call. Store keys come from lib/research/harvest/store.py and
lib/opal_data_harvest/harvest_grammar.py (article_hash rule); nothing is typed twice.
"""
import datetime
import io
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 8))
sys.path.insert(0, REPO)

import pyarrow.parquet as pq  # noqa: E402

from lib.opal_data_harvest import harvest_grammar as hg  # noqa: E402
from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

DELIV = os.path.join(REPO, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables")
UNIVERSE = os.path.join(DELIV, "0.9.0_WK_AMGT_HARVST~46", "securities.universe.json")
FLOOR = pg.BACKFILL_FLOOR
SOURCES = dict(hg.SOURCE_FOR_PUBLISHER)  # publisher code -> S3 source prefix


def a(text, n=None):
    s = ("" if text is None else str(text)).encode("ascii", "backslashreplace").decode("ascii")
    return s[:n] if n else s


def client():
    return store._default_client()


def list_keys(c, prefix):
    out = []
    for page in c.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        for o in page.get("Contents", []) or []:
            out.append({"key": o["Key"], "size": o["Size"], "etag": o["ETag"].strip('"'),
                        "modified": o["LastModified"]})
    return out


def read_parquet_rows(c, key):
    raw = c.get_object(Bucket=store.HARVEST_BUCKET, Key=key)["Body"].read()
    return pq.read_table(io.BytesIO(raw)).to_pylist()


def silver_all_rows(c, publisher_code, table="article"):
    """EVERY row of EVERY part (no collapse to latest): [(part_key, row)] for one publisher."""
    source = SOURCES[publisher_code]
    prefix = store.table_prefix(source, "silver", table)
    out = []
    for o in list_keys(c, prefix):
        if o["key"].endswith(".parquet"):
            for row in read_parquet_rows(c, o["key"]):
                out.append((o["key"], row))
    return out


def bronze_objects(c, publisher_code):
    """{article_hash: [key,...]} for one publisher's bronze article table."""
    source = SOURCES[publisher_code]
    prefix = store.table_prefix(source, "bronze", "article")
    out = {}
    for o in list_keys(c, prefix):
        seg = [p for p in o["key"].split("/") if p.startswith("article_hash=")]
        if seg:
            out.setdefault(seg[0].split("=", 1)[1], []).append(o["key"])
    return out


def main_root():
    """The main workspace root, derived (never typed): the first entry of git worktree list."""
    res = subprocess.run(["git", "worktree", "list", "--porcelain"], cwd=REPO, capture_output=True,
                         text=True, encoding="utf-8")
    first = res.stdout.splitlines()[0] if res.stdout else ""
    return first[len("worktree "):] if first.startswith("worktree ") else None


def runtime_root():
    root = main_root()
    return os.path.join(root, ".runtime", "opal-data-harvest") if root else None


def load_universe():
    with open(UNIVERSE, "r", encoding="utf-8") as fh:
        secs = json.load(fh)
    # Lenovo first, then the file's own order.
    secs = sorted(secs, key=lambda s: (s["security_key"] != "992_HK_Equity",))
    return secs


def to_date(v):
    if v is None:
        return None
    if isinstance(v, datetime.datetime):
        return v.astimezone(datetime.timezone.utc).date()
    return v
