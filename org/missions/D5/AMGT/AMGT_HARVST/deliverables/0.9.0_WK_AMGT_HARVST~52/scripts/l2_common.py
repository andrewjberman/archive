"""Shared read-only core for HVST-l-2 (S3 LIST/GET/HEAD and Lambda GetFunctionConfiguration only).
Reuses i1_common (deliverables/0.9.0_WK_AMGT_HARVST~46/scripts) unchanged for its helpers. The values of the halves are
typed here ONCE, from NEVER_WIDEN_HALF_COO_L2.md sections 2-4 (@4febdff4fb) and NEVER_WIDEN_ROUND22_L2_CTO_HALF.md
section 1 (@19f0954580)."""
import datetime  # noqa: F401
import io
import os
import sys

sys.dont_write_bytecode = True
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, *[".."] * 8))
sys.path.insert(0, os.path.join(_REPO, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
                                "0.9.0_WK_AMGT_HARVST~46", "scripts"))
import i1_common as C  # noqa: E402

import pyarrow.parquet as pq  # noqa: E402

pg, store = C.pg, C.store

DELIV_DIR = os.path.abspath(os.path.join(_HERE, ".."))
BEFORE_JSON = os.path.join(DELIV_DIR, "l2_before_state.json")
ACT_OUTPUT = os.path.join(DELIV_DIR, "l2_act_build_event_output.txt")
TABLES = (pg.GOLD_TABLE, pg.GOLD_DAILY_TABLE, pg.GOLD_EVENT_TABLE)
LAMBDA_NAME = "opal-amgt-scoped-api"
LAMBDA_SHA = "Um3BOJ+jcVc3B79VuFCn4RyD5VYu+IzCpe3BQOP/p7A="

# COO half section 3 (== CTO half section 1): table -> (parts, newest key, ETag, rows)
SECTION3 = {
    pg.GOLD_TABLE: (6, "amgt/harvest/gold/article_security_mention/date=2026-09-29/part-20260929T192610Z.parquet",
                    "831c5669591b247c5ebf2d081a91b249", 304),
    pg.GOLD_DAILY_TABLE: (8, "amgt/harvest/gold/chatter_daily/date=2026-09-29/part-20260929T212132Z.parquet",
                          "4743eb602f1d88b92017bae0022b66e1", 51952),
    pg.GOLD_EVENT_TABLE: (8, "amgt/harvest/gold/chatter_event/date=2026-09-29/part-20260929T192706Z.parquet",
                          "c146a325c98963f965b8b1bd69ca3393", 8),
}

# COO half section 4: the served event -> what it becomes.
# key: (security_key, served first_day, served last_day) -> None for KEPT (row-equal), else the CHANGED expectation
#   (new first_day, new last_day, new articles_total, old event_id prefix, new event_id prefix, new lead startswith)
EXPECTED = {
    ("992_HK_Equity", "2026-02-12", "2026-02-12"): None,
    ("992_HK_Equity", "2026-05-22", "2026-05-22"): None,
    ("BA_US_Equity", "2026-09-08", "2026-09-08"): None,
    ("COST_US_Equity", "2026-09-14", "2026-09-14"): None,
    ("NVDA_US_Equity", "2026-06-01", "2026-06-01"): None,
    ("992_HK_Equity", "2026-08-13", "2026-08-13"): ("2026-08-13", "2026-08-14", 3, "a95c2232e1a8", "8be45608d81b",
                                                    "Lenovo Posts Record Revenue"),
    ("AMZN_US_Equity", "2026-09-07", "2026-09-07"): ("2026-09-06", "2026-09-07", 5, "c9e34b38e4ba", "db2286aabb9f",
                                                      "Amazon Cargo Plane Overshoots Runway in Miami, Killing Five"),
    ("HD_US_Equity", "2026-08-18", "2026-08-18"): ("2026-08-17", "2026-08-18", 4, "a4be84824eec", "3edd30795cb9",
                                                    "Home Depot Stock Rises as Earnings Defy Housing Slump"),
}


def lambda_sha(region="us-east-1"):
    import boto3
    cfg = boto3.client("lambda", region_name=region).get_function_configuration(FunctionName=LAMBDA_NAME)
    return cfg["CodeSha256"], cfg.get("LastModified")


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
    raw = client.get_object(Bucket=store.HARVEST_BUCKET, Key=key)["Body"].read()
    return pq.read_table(io.BytesIO(raw)).to_pylist()


def head_etag(client, key):
    return client.head_object(Bucket=store.HARVEST_BUCKET, Key=key)["ETag"].strip('"')


def partition_date(key):
    return pg._DATE_PARTITION_RE.search(key).group(1)


def ekey(r):
    return (r["security_key"], C.canon(r["first_day"]), C.canon(r["last_day"]))


def map_events(served, new):
    """Map every served event to what it became, by article-key membership within the same security.
    Returns (rows, new_unclaimed) where rows = [(served_event, verdict, [target events])]; verdict is KEPT (one target,
    every field equal), CHANGED (one target, some field differs, target claimed by that served event only), MERGED (the
    target also holds members of another served event), GONE (no target). new_unclaimed = new events no served event maps
    to (NEW)."""
    by_member = {}
    for e in new:
        for k in e.get("article_keys") or []:
            by_member.setdefault((e["security_key"], k), e)
    claims = {}
    tmp = []
    for s in sorted(served, key=lambda r: (r["security_key"], str(r["first_day"]))):
        hits = {}
        for k in (s.get("article_keys") or []):
            e = by_member.get((s["security_key"], k))
            if e is not None:
                hits[id(e)] = e
        tmp.append((s, list(hits.values())))
        for h in hits:
            claims.setdefault(h, []).append(ekey(s))
    rows = []
    for s, tg in tmp:
        if not tg:
            verdict = "GONE"
        elif len(tg) > 1:
            verdict = "SPLIT"
        elif len(claims[id(tg[0])]) > 1:
            verdict = "MERGED"
        else:
            same = all(str(C.canon(s.get(f))) == str(C.canon(tg[0].get(f))) for f in set(s) | set(tg[0]))
            verdict = "KEPT" if same else "CHANGED"
        rows.append((s, verdict, tg))
    claimed = set(claims)
    unclaimed = [e for e in new if id(e) not in claimed]
    return rows, unclaimed
