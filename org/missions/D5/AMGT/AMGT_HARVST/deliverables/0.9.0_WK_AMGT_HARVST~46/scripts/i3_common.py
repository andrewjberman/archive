"""Shared read-only core for HVST-i-3 (S3 LIST/GET/HEAD and Lambda GetFunctionConfiguration only).
Reuses i1_common (same folder) unchanged. The values of the halves are typed here ONCE, from
NEVER_WIDEN_HALF_COO_I3.md sections 2-3 (@1eda314890) and NEVER_WIDEN_ROUND19_I3_CTO_HALF.md section 1 (@4f34061729)."""
import datetime  # noqa: F401
import io
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i1_common as C  # noqa: E402

import pyarrow.parquet as pq  # noqa: E402

pg, store = C.pg, C.store

DELIV_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BEFORE_JSON = os.path.join(DELIV_DIR, "i3_before_state.json")
ACT_OUTPUT = os.path.join(DELIV_DIR, "i3_act_build_daily_output.txt")
SIGNING_RERUN = os.path.join(C.DELIV, "2.0.0_SA_COO_H", "round19", "i3_signing_i2_ac2_rerun.txt")
TABLES = (pg.GOLD_TABLE, pg.GOLD_DAILY_TABLE, pg.GOLD_EVENT_TABLE)
LAMBDA_NAME = "opal-amgt-scoped-api"
LAMBDA_SHA = "lg6NJ2JLYbTc9ZtlDaA9nckuNSOaZZmsYKzDjRPbB3s="
NEW_COL = "publishers_covered_codes"

# COO half section 3 (== CTO half section 1): table -> (parts, newest key, ETag, rows)
SECTION3 = {
    pg.GOLD_TABLE: (6, "amgt/harvest/gold/article_security_mention/date=2026-09-29/part-20260929T192610Z.parquet",
                    "831c5669591b247c5ebf2d081a91b249", 304),
    pg.GOLD_DAILY_TABLE: (7, "amgt/harvest/gold/chatter_daily/date=2026-09-29/part-20260929T192649Z.parquet",
                          "7bce5e68cf4fad06d227d4e41ff36dbd", 51952),
    pg.GOLD_EVENT_TABLE: (8, "amgt/harvest/gold/chatter_event/date=2026-09-29/part-20260929T192706Z.parquet",
                          "c146a325c98963f965b8b1bd69ca3393", 8),
}
# COO half section 4.1: the 149 PARTIAL rows and their codes
PAIR_PARTIAL = {"ASML_NA_Equity": (74, ["sa"]), "ASML_US_Equity": (74, ["sa"]), "992_HK_Equity": (1, ["wsj"])}
PAIR_CLASSES = {"DENIED": 51803, "PARTIAL": 149}


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


def dkey(r):
    return (r["security_key"], r["day"].isoformat() if hasattr(r["day"], "isoformat") else r["day"])
