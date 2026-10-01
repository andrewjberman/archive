"""Live-S3 helpers for the RIV-d-4 checks (READ-ONLY). The act record is the worker's
org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.9.0_WK_ETFS_RIVALS~4/d4_live.json, read from the tree the check runs in."""
from __future__ import annotations

import io
import json
import pathlib

BUCKET = "opal-data-etfs"
RECORD = "org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.9.0_WK_ETFS_RIVALS~4/d4_live.json"


def record() -> dict:
    p = pathlib.Path(RECORD)
    if not p.is_file():
        raise RuntimeError(f"act record absent: {p} (RIV-d-4 has not acted)")
    return json.loads(p.read_text(encoding="utf-8"))


def _s3():
    import boto3

    return boto3.client("s3")


def keys(prefix: str) -> list[str]:
    out, s3 = [], _s3()
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix):
        out += [o["Key"] for o in page.get("Contents", [])]
    return out


def get(key: str) -> bytes:
    return _s3().get_object(Bucket=BUCKET, Key=key)["Body"].read()


def parquet(key: str):
    import pandas as pd

    return pd.read_parquet(io.BytesIO(get(key)))


def latest_parquet(prefix: str):
    ks = sorted(k for k in keys(prefix) if k.endswith(".parquet"))
    return (ks[-1], parquet(ks[-1])) if ks else (None, None)
