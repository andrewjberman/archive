"""Shared read-only core for HVST-g-2 (S3 LIST/GET only). Reuses g-1's _common unchanged."""
import datetime  # noqa: F401  (re-exported for callers as G.datetime)
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

DELIV_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BEFORE_JSON = os.path.join(DELIV_DIR, "g2_before_state.json")
COO_HALF_DIR = os.path.join(C.DELIV, "2.0.0_SA_COO_H", "round18")
SIGNING_RERUN = os.path.join(COO_HALF_DIR, "g2_signing_ac2_rerun.txt")
TABLES = (pg.GOLD_TABLE, pg.GOLD_DAILY_TABLE, pg.GOLD_EVENT_TABLE)

# COO half section 3 (the BEFORE state at signing): table -> (parts, newest key, ETag, rows)
SECTION3 = {
    pg.GOLD_TABLE: (5, "amgt/harvest/gold/article_security_mention/date=2026-09-29/part-20260929T112204Z.parquet",
                    "b8118b05d3160c7c31b4955c22732afe", 275),
    pg.GOLD_DAILY_TABLE: (6, "amgt/harvest/gold/chatter_daily/date=2026-09-29/part-20260929T112222Z.parquet",
                          "06025a62eb771b336f33fe097d50c61c", 51952),
    pg.GOLD_EVENT_TABLE: (7, "amgt/harvest/gold/chatter_event/date=2026-09-29/part-20260929T092439Z.parquet",
                          "c146a325c98963f965b8b1bd69ca3393", 8),
}


def list_parts(client):
    """{table: [{key, etag, size}] sorted by the reader's own (date, key) rule}."""
    out = {}
    for t in TABLES:
        prefix = store.table_prefix("amgt", "gold", t)
        parts = []
        for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
            for o in page.get("Contents", []) or []:
                if o["Key"].endswith(".parquet"):
                    parts.append({"key": o["Key"], "etag": o["ETag"].strip('"'), "size": o["Size"]})
        parts.sort(key=lambda p: (pg._DATE_PARTITION_RE.search(p["key"]).group(1), p["key"]))
        out[t] = parts
    return out


def read_rows(client, key):
    resp = client.get_object(Bucket=store.HARVEST_BUCKET, Key=key)
    raw = resp["Body"].read()
    return pq.read_table(io.BytesIO(raw)).to_pylist()


def head_etag(client, key):
    return client.head_object(Bucket=store.HARVEST_BUCKET, Key=key)["ETag"].strip('"')


def partition_date(key):
    return pg._DATE_PARTITION_RE.search(key).group(1)
