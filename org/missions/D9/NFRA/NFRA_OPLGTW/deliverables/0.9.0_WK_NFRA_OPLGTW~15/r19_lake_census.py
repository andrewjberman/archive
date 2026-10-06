"""OG-rl-7 PHASE A (the OA-e-10 admit-list precondition): census of the gateway audit lake s3://opal-mcp-audit/audit/dt=<day>/ over a day range.
Reads every object IN MEMORY (keys carry ':' and cannot be written on this device), parses each JSONL line, and prints COUNTS only:
objects, records, parse failures, the distinct record shapes (tool / event), every record whose raw text names the /login route or whose
tool names login, and the identities (redacted to a 8-hex digest + domain) on those records.  No secret is read: the lake carries
metadata-only records (audit._safe_args).  usage: python r19_lake_census.py <first day> <last day> <out json>"""
import collections
import concurrent.futures as cf
import datetime
import hashlib
import json
import re
import sys

import boto3

BUCKET = "opal-mcp-audit"
first, last, out = sys.argv[1], sys.argv[2], sys.argv[3]
s3 = boto3.Session(region_name="us-east-1").client("s3")
d0 = datetime.date.fromisoformat(first)
d1 = datetime.date.fromisoformat(last)
days = [(d0 + datetime.timedelta(n)).isoformat() for n in range((d1 - d0).days + 1)]
keys = []
per_day = {}
for d in days:
    n = 0
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="audit/dt=%s/" % d):
        for o in page.get("Contents", []):
            keys.append(o["Key"])
            n += 1
    per_day[d] = n
print("days", len(days), "objects listed", len(keys))

LOGIN_RE = re.compile(r"(?<![A-Za-z_/])/login(?![A-Za-z_/])")   # the bare /login route, not /schwab/download/login
shapes = collections.Counter()
login_recs = []
login_like = collections.Counter()
fail = []
n_rec = 0


def redact(u):
    if not isinstance(u, str) or not u:
        return "(none)"
    dom = u.split("@", 1)[1] if "@" in u else "-"
    return "%s@%s" % (hashlib.sha256(u.lower().encode()).hexdigest()[:8], dom)


def one(key):
    try:
        body = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read().decode("utf-8", errors="replace")
    except Exception as exc:   # noqa: BLE001
        return key, None, str(exc)[:100]
    return key, body, None


with cf.ThreadPoolExecutor(24) as ex:
    for key, body, err in ex.map(one, keys):
        if err:
            fail.append((key, err))
            continue
        for ln in body.splitlines():
            if not ln.strip():
                continue
            n_rec += 1
            try:
                rec = json.loads(ln)
            except ValueError:
                fail.append((key, "bad json"))
                continue
            shapes[(rec.get("event") or "") + "|" + (rec.get("tool") or "")] += 1
            raw = ln
            tool = str(rec.get("tool") or "")
            route = str(rec.get("route") or "")
            hit_route = bool(LOGIN_RE.search(raw))
            if "login" in tool.lower() or "login" in route.lower() or hit_route:
                login_like[(tool, route[:40], hit_route)] += 1
                if hit_route or tool.lower() == "login" or route == "/login":
                    login_recs.append({"day": key.split("/")[1], "tool": tool, "route": route[:40], "outcome": rec.get("outcome"),
                                       "who": redact(rec.get("user") or rec.get("caller") or rec.get("principal"))})
res = {"bucket": BUCKET, "first_day": first, "last_day": last, "days": len(days), "objects_per_day_min": min(per_day.values()),
       "objects_per_day_max": max(per_day.values()), "objects": len(keys), "records": n_rec, "read_failures": len(fail),
       "distinct_shapes": len(shapes), "shapes_top": shapes.most_common(60),
       "login_like_records": sum(login_like.values()), "login_like_breakdown": [[list(k), v] for k, v in login_like.items()],
       "bare_login_route_records": len(login_recs), "bare_login_route_records_sample": login_recs[:20],
       "per_day": per_day}
json.dump(res, open(out, "w", encoding="utf-8", newline="\n"), indent=1)
print("records", n_rec, "read_failures", len(fail), "distinct shapes", len(shapes))
print("login-like records", sum(login_like.values()), "bare /login route records", len(login_recs))
for k, v in login_like.items():
    print("  login-like", k, v)
