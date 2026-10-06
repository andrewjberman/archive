#!/usr/bin/env python3
"""OG-pm-2 -- read-only fetch + parse of the gateway ALB access logs for UTC days into a local scratch cache.
Usage: pm2_fetch.py <cache.json> <YYYY-MM-DD> [<YYYY-MM-DD> ...]
Reads only (s3:ListObjectsV2 / GetObject on opal-data-security waf-logs/alb-opal-gateway/). Writes ONLY <cache.json>.
Each ALB log line is split by the documented field order; the query string is DROPPED from the request URL at parse time
(it can carry an OAuth code); no header, cookie or bearer is in an ALB access log line.
"""
import concurrent.futures as cf
import datetime as dt
import gzip
import json
import re
import sys

import boto3

BUCKET = "opal-data-security"
PFX = "waf-logs/alb-opal-gateway/AWSLogs/313476888478/elasticloadbalancing/us-east-1/"
S3 = boto3.client("s3", region_name="us-east-1")
TOK = re.compile(r'"[^"]*"|\S+')


def keys_for(day):
    d = dt.date.fromisoformat(day)
    out = []
    for off in (0, 1):
        x = d + dt.timedelta(days=off)
        pfx = PFX + x.strftime("%Y/%m/%d/")
        for pg in S3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=pfx):
            out += [o["Key"] for o in pg.get("Contents", [])]
    return out


def parse(line):
    f = TOK.findall(line)
    if len(f) < 20:
        return None
    req = f[12].strip('"').split(" ")
    method, url = req[0], (req[1] if len(req) > 1 else "")
    path = re.sub(r"^https?://[^/]+", "", url).split("?")[0]
    return {
        "type": f[0], "time": f[1], "client": f[3].rsplit(":", 1)[0], "target": f[4],
        "req_t": float(f[5]), "tgt_t": float(f[6]), "resp_t": float(f[7]),
        "elb_status": f[8], "tgt_status": f[9], "method": method, "path": path,
        "ua": f[13].strip('"')[:80], "rule": f[22] if len(f) > 22 else None,
        "created": f[23] if len(f) > 23 else None,
        "actions": f[24].strip('"') if len(f) > 24 else None,
    }


def fetch(key):
    body = S3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
    rows = []
    for ln in gzip.decompress(body).decode("utf-8", "replace").splitlines():
        r = parse(ln)
        if r:
            rows.append(r)
    return rows


def main():
    out, days = sys.argv[1], sys.argv[2:]
    cache = {}
    for day in days:
        ks = keys_for(day)
        rows = []
        with cf.ThreadPoolExecutor(12) as ex:
            for part in ex.map(fetch, ks):
                rows += part
        rows = [r for r in rows if r["time"].startswith(day)]
        cache[day] = {"files_read": len(ks), "rows": rows}
        print(day, "files", len(ks), "rows_in_day", len(rows))
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(cache, fh)


main()
