#!/usr/bin/env python
"""OG-rz-2 (CVO note, 'scheduled callers in the window'): who calls the gateway between 06:00Z and 06:45Z? READ ONLY. COUNTS ONLY: the audit lake's `user` field holds sign-in addresses, so a caller is
counted (a distinct-caller COUNT and a short hash prefix is never written) and no address, argument or row is written. Also lists the EventBridge schedules whose rule name names the gateway or MCP and that fire in the window.
usage: python rz2_callers.py <day> [<day> ...]    (days are the three previous UTC days, YYYY-MM-DD)"""
from __future__ import annotations

import hashlib
import io
import json
import re
import statistics
import sys

import boto3

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
BUCKET, START, END = "opal-mcp-audit", "06:00:00", "06:45:00"
s3 = boto3.client("s3", region_name="us-east-1")
days = sys.argv[1:]
tools = {}
objects = errors = 0
for day in days:
    token, keys = None, []
    first = True
    kw, page = {}, {}
    while first or token:
        first = False
        kw = {"Bucket": BUCKET, "Prefix": "audit/dt=%s/" % day}
        if token:
            kw["ContinuationToken"] = token
        else:
            kw["StartAfter"] = "audit/dt=%s/%sT%s" % (day, day, START[:5])
        page = s3.list_objects_v2(**kw)
        keys += [o["Key"] for o in page.get("Contents", [])]
        token = page.get("NextContinuationToken") if page.get("IsTruncated") else None
    inwin = [k for k in keys if (START <= k.split("/")[-1][11:19] <= END) and k.split("/")[-1][:10] == day]
    for k in inwin:
        objects += 1
        try:
            for ln in s3.get_object(Bucket=BUCKET, Key=k)["Body"].read().decode("utf-8", "replace").splitlines():
                if not ln.strip():
                    continue
                rec = json.loads(ln)
                t = tools.setdefault(str(rec.get("tool")), {"calls": 0, "per_day": {}, "callers": {}, "outcomes": {}})
                t["calls"] += 1
                t["per_day"][day] = t["per_day"].get(day, 0) + 1
                who = hashlib.sha256(str(rec.get("user", "")).encode()).hexdigest()[:8]
                ts = str(rec.get("ts") or k.split("/")[-1][:19])
                t["callers"].setdefault(who, []).append(ts)
                o = str(rec.get("outcome") or "unknown")[:16]
                t["outcomes"][o] = t["outcomes"].get(o, 0) + 1
        except Exception:
            errors += 1


def secs(ts):
    import datetime as dt
    try:
        return dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
    except Exception:
        return None


rows = []
for name, t in sorted(tools.items(), key=lambda kv: -kv[1]["calls"]):
    gaps = []
    for lst in t["callers"].values():
        v = sorted(x for x in (secs(s) for s in lst) if x is not None)
        gaps += [b - a for a, b in zip(v, v[1:]) if b - a > 0]
    rows.append({"tool": name, "calls_total": t["calls"], "calls_per_day": t["per_day"], "distinct_callers": len(t["callers"]), "median_gap_seconds_between_a_callers_calls": round(statistics.median(gaps), 1) if gaps else None,
                 "outcomes": t["outcomes"]})

# EventBridge schedules naming the gateway or MCP that fire inside the window
ev = boto3.client("events", region_name="us-east-1")
rules, token = [], None
first = True
r = {}
while first or token:
    first = False
    r = ev.list_rules(NextToken=token) if token else ev.list_rules()
    rules += r["Rules"]
    token = r.get("NextToken")


def field_matches(spec, value, lo, hi):
    if spec in ("*", "?"):
        return True
    for part in spec.split(","):
        step = 1
        if "/" in part:
            part, st = part.split("/")
            step = int(st)
        if part in ("*", "?"):
            rng = range(lo, hi + 1, step)
        elif "-" in part:
            a, b = part.split("-")
            rng = range(int(a), int(b) + 1, step)
        else:
            rng = range(int(part), (hi if step > 1 else int(part)) + 1, step) if step > 1 else [int(part)]
        if value in rng:
            return True
    return False


def fires_in_window(expr):
    m = re.match(r"cron\((\S+) (\S+) .*\)", expr or "")
    if not m:
        return None
    minute, hour = m.group(1), m.group(2)
    return any(field_matches(hour, 6, 0, 23) and field_matches(minute, mn, 0, 59) for mn in range(0, 46))


sched = [r for r in rules if r.get("ScheduleExpression")]
named = [r["Name"] for r in sched if re.search(r"gateway|mcp", r["Name"], re.I) and fires_in_window(r["ScheduleExpression"])]
rate_named = [r["Name"] for r in sched if re.search(r"gateway|mcp", r["Name"], re.I) and (r["ScheduleExpression"] or "").startswith("rate(")]
union = set()
for t in tools.values():
    union |= set(t["callers"])
out = {"distinct_callers_across_all_tools": len(union), "window_utc": "%s to %s" % (START, END), "days_read": days, "audit_objects_read": objects, "read_errors": errors, "records_in_window": sum(r["calls_total"] for r in rows), "tools": rows,
       "eventbridge": {"rules_with_a_schedule": len(sched), "gateway_or_mcp_named_cron_rules_firing_in_the_window": named, "gateway_or_mcp_named_rate_rules": rate_named,
                       "note": "an EventBridge rule is not proof of a gateway caller: the audit lake rows above are the record of who actually called"},
       "reading": "Calls in this window on the three days before are the scheduled and overnight callers; every distinct caller counts one sign-in identity (not named here); a tool with a steady gap is a poller."}
io.open(W + "RZ2_CALLERS.json", "w", encoding="utf-8", newline="\n").write(json.dumps(out, indent=1) + "\n")
print(json.dumps({"objects": objects, "errors": errors, "records": out["records_in_window"], "tools": [(r["tool"], r["calls_total"], r["distinct_callers"], r["median_gap_seconds_between_a_callers_calls"]) for r in rows], "eventbridge": out["eventbridge"]}, indent=1)[:3000])
