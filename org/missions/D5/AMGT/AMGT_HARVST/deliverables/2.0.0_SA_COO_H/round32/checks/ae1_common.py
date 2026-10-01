"""HVST-ae-1 shared reads (issuer, read-only): the sa wrong-object classifier, independent of the worker's code.

A sa silver article row is WRONG-OBJECT when ALL hold:
- it was discovered through a symbol news listing (`discovered_for` is non-empty);
- its row carries the raw article capture's own `id` (the body came from `/api/v3/articles/{news_id}`, a different id
  space from the listing's news ids);
- its title is not the title of the stored listing hit for the same id (no stored listing hit counts as not equal).
Measured at the cut (2026-10-01 ~05:0xZ, 85 rows): 38 rows (32 with a differing listing title, all dated 2023; 6 with no
stored listing hit, dated 2021). Listing-shaped rows (no `id`) and analysis-feed rows (no `discovered_for`) are never
WRONG-OBJECT. A date is NOT the signature: low-volume names list genuine pre-2026 items in live mode.
"""
import io
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)

import boto3  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import store  # noqa: E402

B = store.HARVEST_BUCKET
SILVER = "seeking-alpha/harvest/silver/article/"
LISTING = "seeking-alpha/harvest/silver/listing_hit/"
MENTION = "amgt/harvest/gold/article_security_mention/"
FLOOR = "2026-01-01"
WK = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~90")
MANIFEST = os.path.join(WK, "ae1_quarantine.json")


def client():
    return boto3.client("s3", region_name="us-east-1")


def keys(prefix, cl=None):
    cl = cl or client()
    out = []
    for page in cl.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix=prefix):
        out += [(o["Key"], o["LastModified"].isoformat()) for o in page.get("Contents", [])]
    return out


def rows(prefix, cl=None):
    cl = cl or client()
    out = []
    for k, _ in keys(prefix, cl):
        if k.endswith(".parquet"):
            for r in pq.read_table(io.BytesIO(cl.get_object(Bucket=B, Key=k)["Body"].read())).to_pylist():
                r["_part"] = k
                out.append(r)
    return out


def listed(value):
    if value is None:
        return False
    if isinstance(value, (list, tuple)):
        return len(value) > 0
    text = str(value).strip()
    return text not in ("", "None", "[]", "null")


def classify(silver, listing):
    titles = {}
    for r in listing:
        ident = str(r.get("article_id") or r.get("id") or "")
        if ident and r.get("title"):
            titles[ident] = r["title"]
    wrong = []
    for r in silver:
        if not listed(r.get("discovered_for")) or not listed(r.get("id")):
            continue
        if titles.get(str(r.get("article_id") or "")) != r.get("title"):
            wrong.append(r)
    return wrong


def article_key(r):
    return "sa:" + str(r.get("article_id"))
