#!/usr/bin/env python3
"""BP-b-3 premise check: how tax.open_lots is present across the 3,510 detail.json objects (read-only, counts only).
Classes: field missing, empty list, non-empty list, not a list. No client field is read or printed.
Run from the worktree root:  python -I <this file>
"""
import concurrent.futures as cf
import json
from collections import Counter

import boto3
import botocore.config

CL_BUCKET = "opal-data-49financial"
CL_PREFIX = "advi/49financial/platinum/entities/clients/"


def main():
    s3 = boto3.session.Session().client(
        "s3", config=botocore.config.Config(max_pool_connections=32, retries={"max_attempts": 5, "mode": "standard"}))
    keys = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=CL_BUCKET, Prefix=CL_PREFIX):
        for o in page.get("Contents", []):
            k = o["Key"]
            if k.endswith("/detail.json") and k[len(CL_PREFIX):].count("/") == 1:
                keys.append(k)
    print(f"OBJECTS listed={len(keys)}")

    def classify(key):
        body = s3.get_object(Bucket=CL_BUCKET, Key=key)["Body"].read()
        o = json.loads(body)
        tax = o.get("tax")
        if not isinstance(tax, dict) or "open_lots" not in tax:
            return "tax_or_open_lots_missing"
        v = tax["open_lots"]
        if v is None:
            return "null"
        if not isinstance(v, list):
            return "not_a_list"
        return "empty_list" if len(v) == 0 else "non_empty_list"

    def safe(key):
        try:
            return classify(key)
        except Exception as e:  # noqa: BLE001 -- counted, never silent
            return "READ_FAILED:" + type(e).__name__

    cnt = Counter()
    with cf.ThreadPoolExecutor(max_workers=16) as ex:
        for res in ex.map(safe, keys):
            cnt[res] += 1
    print("OPEN_LOTS presence", dict(cnt), "total", sum(cnt.values()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
