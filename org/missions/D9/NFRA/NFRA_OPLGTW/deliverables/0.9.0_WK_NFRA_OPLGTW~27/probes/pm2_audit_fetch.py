#!/usr/bin/env python3
"""OG-pm-2 -- read-only fetch of the gateway audit-lake records (bucket opal-mcp-audit, audit/dt=<day>/) for UTC days into
a local scratch cache. Usage: pm2_audit_fetch.py <cache.json> <YYYY-MM-DD> [...]
Keeps ONLY ts, tool, event, route, outcome, tier, credential_class, caller, the `label=` and `route=` tokens of `detail`,
and a short digest of user/principal (the raw email is never kept). `args` is never read into the cache. Reads: s3:ListObjectsV2 / GetObject only. Writes only <cache.json>.
"""
import concurrent.futures as cf
import hashlib
import json
import re
import sys

import boto3

BUCKET = "opal-mcp-audit"
S3 = boto3.client("s3", region_name="us-east-1")


def dg(x):
    return "u#" + hashlib.sha256(str(x).encode()).hexdigest()[:8] if x else None


def one(key):
    try:
        r = json.loads(S3.get_object(Bucket=BUCKET, Key=key)["Body"].read().decode("utf-8", "replace").splitlines()[0])
    except Exception as e:  # a failed read is counted, not hidden
        return {"_err": type(e).__name__}
    det = str(r.get("detail") or "")
    lab = re.search(r"\blabel=([A-Za-z0-9_.-]{1,40})", det)
    rte = re.search(r"\broute=(/\S{1,80})", det)
    return {"dlabel": lab.group(1) if lab else None, "droute": rte.group(1) if rte else None, "ts": r.get("ts"), "tool": r.get("tool"), "event": r.get("event"), "route": r.get("route"),
            "outcome": r.get("outcome"), "tier": r.get("tier"), "cred": r.get("credential_class"),
            "caller": r.get("caller"), "user": dg(r.get("user")), "principal": dg(r.get("principal")),
            "has_bytes": "bytes" in r}


def main():
    out, days = sys.argv[1], sys.argv[2:]
    cache = {}
    for day in days:
        keys = []
        for pg in S3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="audit/dt=%s/" % day):
            keys += [o["Key"] for o in pg.get("Contents", [])]
        with cf.ThreadPoolExecutor(16) as ex:
            recs = list(ex.map(one, keys))
        errs = sum(1 for r in recs if "_err" in r)
        cache[day] = {"objects": len(keys), "read_errors": errs, "records": [r for r in recs if "_err" not in r]}
        print(day, "objects", len(keys), "read_errors", errs)
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(cache, fh)


main()
