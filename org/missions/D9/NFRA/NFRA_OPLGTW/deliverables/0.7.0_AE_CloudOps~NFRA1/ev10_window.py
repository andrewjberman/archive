#!/usr/bin/env python
"""OG-ev-10 (COO msg 35890, read-only): count the gw_ratelimit rows in the audit lake over one UTC window and say whether any lies near a given minute span. Counts and the rows' object-key timestamps only (the key
names carry the record's own UTC time); no principal, address or row content is printed.
  python ev10_window.py <out.json> <start_utc> <end_utc> <near_start_utc> <near_end_utc>"""
from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor

import boto3

BUCKET = "opal-mcp-audit"
OUT, START, END, NEAR0, NEAR1 = sys.argv[1:6]
s3 = boto3.client("s3", region_name="us-east-1")


def keys():
    out, token, first = [], None, True
    day = START[:10]
    while first or token:
        first = False
        kw = {"Bucket": BUCKET, "Prefix": "audit/dt=%s/" % day}
        kw.update({"ContinuationToken": token} if token else {"StartAfter": "audit/dt=%s/%s" % (day, START[:-1])})
        page = s3.list_objects_v2(**kw)
        out += [o["Key"] for o in page.get("Contents", [])]
        token = page.get("NextContinuationToken") if page.get("IsTruncated") else None
    return [k for k in out if k.split("/")[-1][:19] <= END[:-1]]


def read(key):
    try:
        for ln in s3.get_object(Bucket=BUCKET, Key=key)["Body"].read().decode("utf-8", "replace").splitlines():
            if ln.strip() and json.loads(ln).get("event") == "gw_ratelimit":
                return key, True, None
        return key, False, None
    except Exception as exc:
        return key, False, type(exc).__name__


ks = keys()
with ThreadPoolExecutor(max_workers=16) as ex:
    res = list(ex.map(read, ks))
hits = [k.split("/")[-1][:19] + "Z" for k, h, _e in res if h]
near = [t for t in hits if NEAR0[:-1] <= t[:-1] <= NEAR1[:-1]]
rec = {"window_start": START, "window_end": END, "objects_listed": len(ks), "read_errors": sum(1 for _k, _h, e in res if e), "gw_ratelimit_rows": len(hits), "row_times_utc": hits,
       "near_span": [NEAR0, NEAR1], "rows_in_near_span": len(near), "source": "s3://%s audit/dt=<day>/ listed (StartAfter the window start) and every object read; event gw_ratelimit counted" % BUCKET}
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rec, indent=1) + "\n")
print(json.dumps({k: rec[k] for k in ("objects_listed", "read_errors", "gw_ratelimit_rows", "row_times_utc", "rows_in_near_span")}))
