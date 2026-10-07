"""OG-rl-7 PHASE A (OA-e-10 admit-list precondition), second lake read: WHO could have needed /login in the window.  The lake has no /login record
(r19_lake_census.json), but /login is the only recovery for a lapsed email-keyed Graph cache, and a lapse surfaces as outcome "needs_login" on a tool call.
This reads every record of the window and tallies, per identity (labelled: configured / alyssa / opalbloomberg / other = 8-hex digest + domain): records,
distinct days, and the records with outcome needs_login / denied / error, plus the first and last day seen.  Counts only; no args, no detail text.
usage: python r19_lake_users.py <first day> <last day> <out json>"""
import collections
import concurrent.futures as cf
import datetime
import hashlib
import json
import sys

import boto3

BUCKET = "opal-mcp-audit"
first, last, out = sys.argv[1], sys.argv[2], sys.argv[3]
s3 = boto3.Session(region_name="us-east-1").client("s3")
d0, d1 = datetime.date.fromisoformat(first), datetime.date.fromisoformat(last)
days = [(d0 + datetime.timedelta(n)).isoformat() for n in range((d1 - d0).days + 1)]
keys = []
for d in days:
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="audit/dt=%s/" % d):
        keys += [o["Key"] for o in page.get("Contents", [])]
LAB = {"andrew@opalinvest.com": "configured(andrew)", "alyssa@opalinvest.com": "alyssa", "opalbloomberg@opalinvest.com": "opalbloomberg"}


def label(u):
    if not isinstance(u, str) or not u:
        return "(none)"
    if u.lower() in LAB:
        return LAB[u.lower()]
    return "other:%s@%s" % (hashlib.sha256(u.lower().encode()).hexdigest()[:8], u.split("@", 1)[1] if "@" in u else "-")


per = collections.defaultdict(lambda: {"records": 0, "days": set(), "outcomes": collections.Counter(), "tools_needs_login": collections.Counter(), "needs_login_days": set()})


def one(k):
    return k, s3.get_object(Bucket=BUCKET, Key=k)["Body"].read().decode("utf-8", "replace")


bad = 0
with cf.ThreadPoolExecutor(24) as ex:
    for k, body in ex.map(one, keys):
        day = k.split("/")[1][3:]
        for ln in body.splitlines():
            if not ln.strip():
                continue
            try:
                r = json.loads(ln)
            except ValueError:
                bad += 1
                continue
            if "user" not in r:
                continue
            p = per[label(r.get("user"))]
            p["records"] += 1
            p["days"].add(day)
            oc = r.get("outcome") or ""
            p["outcomes"][oc] += 1
            if oc == "needs_login":
                p["tools_needs_login"][r.get("tool") or ""] += 1
                p["needs_login_days"].add(day)
res = {"first_day": first, "last_day": last, "objects": len(keys), "unparseable": bad, "identities": {}}
for who, p in sorted(per.items()):
    res["identities"][who] = {"records": p["records"], "distinct_days": len(p["days"]), "first_day": min(p["days"]), "last_day": max(p["days"]),
                              "outcomes": dict(p["outcomes"]), "needs_login_records": p["outcomes"].get("needs_login", 0),
                              "needs_login_tools": dict(p["tools_needs_login"]), "needs_login_days": sorted(p["needs_login_days"])}
json.dump(res, open(out, "w", encoding="utf-8", newline="\n"), indent=1)
print("objects", len(keys), "unparseable", bad, "identities", len(per))
for who, v in res["identities"].items():
    print(who, "records", v["records"], "days", v["distinct_days"], v["first_day"], v["last_day"], "needs_login", v["needs_login_records"], v["needs_login_days"][:5])
