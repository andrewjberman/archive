"""HVST-m-1 shared read-only helpers: S3 GET/LIST/HEAD against s3://opal-data-harvest/ only.

No put, no delete, no vendor call. Publisher codes: barrons, bbg (store prefix bloomberg), ft,
sa (store prefix seeking-alpha), wsj.
"""

import collections
import hashlib
import io
import json
import os

import boto3
import pyarrow.parquet as pq

BUCKET = "opal-data-harvest"
VALIDATION_SECURITY = "992_HK_Equity"
PUBLISHERS = (
    ("barrons", "barrons"),
    ("bbg", "bloomberg"),
    ("ft", "ft"),
    ("sa", "seeking-alpha"),
    ("wsj", "wsj"),
)
OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_client = None


def client():
    global _client
    if _client is None:
        _client = boto3.client("s3", region_name="us-east-1")
    return _client


def list_keys(prefix):
    """Every object under prefix: [(key, size)], auto-paginated (denominator = len)."""
    out = []
    for page in client().get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            out.append((obj["Key"], obj["Size"]))
    return out


def get(key):
    """(bytes, metadata dict) or (None, error string) - a failed read is a VALUE, never silence."""
    try:
        resp = client().get_object(Bucket=BUCKET, Key=key)
        return resp["Body"].read(), dict(resp.get("Metadata", {}))
    except Exception as exc:  # noqa: BLE001 - the error text IS the recorded value
        return None, "%s: %s" % (type(exc).__name__, exc)


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def bronze_articles(store):
    """[(key, size)] of bronze article objects for a store prefix."""
    return list_keys("%s/harvest/bronze/article/" % store)


def silver_rows(store, table="article"):
    """[(part_key, arrow_table)] for every parquet under silver/<table>/; a failed read is
    returned with table=None and the error string, never dropped."""
    parts = []
    for key, _size in list_keys("%s/harvest/silver/%s/" % (store, table)):
        if not key.endswith(".parquet"):
            continue
        raw, meta = get(key)
        if raw is None:
            parts.append((key, None, meta))
            continue
        parts.append((key, pq.read_table(io.BytesIO(raw)), None))
    return parts


def silver_row_dicts(store, table="article"):
    """Flat list of (part_key, row dict, schema_column_names)."""
    out = []
    unreadable = []
    for key, tbl, err in silver_rows(store, table):
        if tbl is None:
            unreadable.append((key, err))
            continue
        cols = list(tbl.schema.names)
        for row in tbl.to_pylist():
            out.append((key, row, cols))
    return out, unreadable


def discovered_for_list(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [str(x) for x in value]
    return [str(value)]


def received_form(meta):
    if not isinstance(meta, dict):
        return "unreadable"
    return meta.get("received-form", "unlabelled")


def emit(name, text, result):
    """Print the text and write m1_<name>_output.txt + m1_<name>_result.json in the deliverables."""
    print(text)
    with open(os.path.join(OUT_DIR, "m1_%s_output.txt" % name), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text + "\n")
    with open(os.path.join(OUT_DIR, "m1_%s_result.json" % name), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, indent=1, sort_keys=True, default=str)
        fh.write("\n")


def counter_line(counter):
    return ", ".join("%s=%d" % (k, v) for k, v in sorted(counter.items())) or "(none)"


Counter = collections.Counter
