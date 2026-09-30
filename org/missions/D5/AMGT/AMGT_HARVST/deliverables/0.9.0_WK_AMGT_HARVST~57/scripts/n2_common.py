"""HVST-n-2 shared read-only helpers: S3 GET/LIST only against s3://opal-data-harvest/. No put, no
delete, no vendor call. The builder under test is imported from the worktree
(lib/opal_data_harvest/silver_from_bronze.py); nothing here writes to S3.
"""

import datetime
import io
import json
import os
import sys

import boto3
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(HERE, *([".."] * 8)))
sys.path.insert(0, REPO)

BUCKET = "opal-data-harvest"
SECURITY = "992_HK_Equity"
PUBLISHERS = (("barrons", "barrons"), ("bbg", "bloomberg"), ("ft", "ft"), ("sa", "seeking-alpha"), ("wsj", "wsj"))

_client = None


def client():
    global _client
    if _client is None:
        _client = boto3.client("s3", region_name="us-east-1")
    return _client


def list_keys(prefix):
    out = []
    for page in client().get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            out.append(obj["Key"])
    return out


def get(key):
    resp = client().get_object(Bucket=BUCKET, Key=key)
    return resp["Body"].read(), dict(resp.get("Metadata", {}))


def silver_parts(store, table="article"):
    """[(part_key, [row dicts])] for every parquet under silver/<table>/ (a failed read raises)."""
    parts = []
    for key in list_keys("%s/harvest/silver/%s/" % (store, table)):
        if key.endswith(".parquet"):
            raw, _meta = get(key)
            parts.append((key, pq.read_table(io.BytesIO(raw)).to_pylist()))
    return parts


def received_form(meta):
    return meta.get("received-form", "unlabelled")


def emit(name, text, result):
    print(text)
    with open(os.path.join(OUT_DIR, "n2_%s_output.txt" % name), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text + "\n")
    with open(os.path.join(OUT_DIR, "n2_%s_result.json" % name), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, indent=1, sort_keys=True, default=str)
        fh.write("\n")


def norm(v):
    """Comparable form: datetimes as UTC instants, containers as sorted JSON, scalars as str."""
    if isinstance(v, datetime.datetime):
        if v.tzinfo is None:
            v = v.replace(tzinfo=datetime.timezone.utc)
        return v.astimezone(datetime.timezone.utc).isoformat()
    if isinstance(v, (list, dict)):
        return json.dumps(v, sort_keys=True, default=str)
    return None if v is None else str(v)
