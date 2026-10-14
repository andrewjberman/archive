# -*- coding: utf-8 -*-
"""Shared live-probe helpers for the round-37 G1-TYPED AC2 checks (issuer's). Read only; box credentials."""
import io
import os
import sys
from types import SimpleNamespace

GW = os.path.join(os.getcwd(), "infra", "aws", "ec2", "opal-gateway")
BUCKET = "opal-data-harvest"


def setup():
    """Put the gateway on the path, patch the ONE principal point to an Opal stand-in, and return a boto3 s3 client."""
    sys.path.insert(0, GW)
    os.chdir(GW)
    os.environ.setdefault("AUDIT_PATH", os.path.join(os.environ.get("TEMP", "/tmp"), "gt_probe_audit.jsonl"))
    os.environ.pop("INTERNAL_READER_ROLE_ARN", None)     # the box reads with its own credentials
    import app.harvest_read as hr
    hr.get_current_principal = lambda: SimpleNamespace(email="live.probe@opalinvest.com", tid="probe-tid", oid="probe-oid")
    import boto3
    return boto3.client("s3")


def asml_key(c):
    """The packs/ key of ASML, found independently of every tool under test."""
    pg = c.get_paginator("list_objects_v2")
    for page in pg.paginate(Bucket=BUCKET, Prefix="packs/", Delimiter="/"):
        for p in page.get("CommonPrefixes", []):
            seg = p["Prefix"].split("/")[1]
            if "ASML" in seg.upper():
                return seg
    return None


def newest_part(c, prefix):
    keys = []
    for page in c.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix):
        keys += [o["Key"] for o in page.get("Contents", []) if o["Key"].endswith(".parquet")]
    if not keys:
        return None
    return max(keys, key=lambda k: (k.split("/")[-2], k.split("/")[-1]))


def read_table(c, key, columns=None):
    import pyarrow.parquet as pq
    body = c.get_object(Bucket=BUCKET, Key=key)["Body"].read()
    return pq.read_table(io.BytesIO(body), columns=columns)


def envelope_ok(d):
    return isinstance(d, dict) and all(k in d for k in ("as_of", "source_keys", "denominator", "absent_reason"))
