#!/usr/bin/env python
"""OG-gm-1 Phase A: does the audit lake hold any record by a user of one role name over the last N days? READ ONLY (LIST and GET on s3://opal-mcp-audit). COUNTS ONLY: no principal key, e-mail or value is printed or kept.
usage: python gm1_signin_scan.py <days> <out.json>"""
from __future__ import annotations

import concurrent.futures
import datetime
import json
import sys

import boto3

BUCKET = "opal-mcp-audit"
ROLE = "menachem"
DAYS = int(sys.argv[1])
OUT = sys.argv[2]
s3 = boto3.client("s3", region_name="us-east-1")
today = datetime.datetime.now(datetime.timezone.utc).date()


def list_day(day):
    out, token = [], None
    while True:
        kw = {"Bucket": BUCKET, "Prefix": "audit/dt=%s/" % day}
        if token:
            kw["ContinuationToken"] = token
        page = s3.list_objects_v2(**kw)
        out += [o["Key"] for o in page.get("Contents", [])]
        if not page.get("IsTruncated"):
            return out
        token = page.get("NextContinuationToken")


keys = []
for d in range(DAYS):
    keys += list_day((today - datetime.timedelta(days=d)).isoformat())


def one(key):
    hits, total = 0, 0
    try:
        body = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read().decode("utf-8", "replace")
    except Exception:
        return None
    for line in body.splitlines():
        if line.strip():
            total += 1
            if str(json.loads(line).get("user", "")).lower().startswith(ROLE):
                hits += 1
    return hits, total


records = errors = hits = 0
with concurrent.futures.ThreadPoolExecutor(32) as ex:
    for res in ex.map(one, keys):
        if res is None:
            errors += 1
        else:
            hits += res[0]
            records += res[1]
out = {"days": DAYS, "objects": len(keys), "read_errors": errors, "records": records, "records_by_a_user_of_the_role": hits}
json.dump(out, open(OUT, "w"), indent=1)
print(json.dumps(out))
