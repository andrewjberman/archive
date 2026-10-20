#!/usr/bin/env python
"""OG-rl-17 condition C1: how many tool calls ran at once over the 24 h before the measurement, from the audit lake. READ ONLY (s3:ListBucket and GetObject on s3://opal-mcp-audit). COUNTS ONLY: no principal, e-mail, argument or value is printed or kept.
The audit record carries ONE timestamp (`ts`, written when the call is LOGGED, at its end or at its denial) and no start, no duration (app/audit.py log_call; no 'elapsed', 'duration' or latency field exists in audit.py, tools.py or server.py),
so a call's start-to-end overlap cannot be computed from the lake. What the lake CAN give is how many calls were logged in the same second and in the same 2, 5 and 10 s windows: a call logged at t ran no later than t, and k calls logged
in one second all ended inside that second, so "peak completions per second" is a lower-bound PROXY for the busiest moment, not the overlap. Both variants are recorded: every record that carries a `tool` key, and those with outcome ok or error (a denied call takes no slot).
usage: python rl17_c1_peak.py <window_end_utc, e.g. 2026-10-20T12:05:00Z> <out.json> [scratch.json]"""
from __future__ import annotations

import collections
import concurrent.futures
import datetime
import io
import json
import sys
import time

import boto3

BUCKET = "opal-mcp-audit"
END = sys.argv[1]
OUT = sys.argv[2]
end_dt = datetime.datetime.strptime(END, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
start_dt = end_dt - datetime.timedelta(hours=24)
START = start_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
s3 = boto3.client("s3", region_name="us-east-1")


def list_keys(prefix):
    keys, token = [], None
    while True:
        kw = {"Bucket": BUCKET, "Prefix": prefix}
        if token:
            kw["ContinuationToken"] = token
        page = s3.list_objects_v2(**kw)
        keys += [o["Key"] for o in page.get("Contents", [])]
        if not page.get("IsTruncated"):
            return keys
        token = page.get("NextContinuationToken")


days = sorted({start_dt.strftime("%Y-%m-%d"), end_dt.strftime("%Y-%m-%d")})
keys = []
for d in days:
    keys += list_keys("audit/dt=%s/" % d)
# the key time is the object's time; records inside may differ by a few seconds, so read the keys in [start-1min, end+1min] and filter on the record's own ts
lo, hi = (start_dt - datetime.timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%S"), (end_dt + datetime.timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%S")
keys = [k for k in keys if lo <= k.split("/")[-1][:19] <= hi]


def one(k):
    for attempt in range(3):
        try:
            body = s3.get_object(Bucket=BUCKET, Key=k)["Body"].read().decode("utf-8", "replace")
            out = []
            for ln in body.splitlines():
                if ln.strip():
                    r = json.loads(ln)
                    if "tool" in r and r.get("ts"):
                        out.append((r["ts"], str(r.get("outcome")), str(r.get("tool"))))
            return out
        except Exception:
            time.sleep(1 + attempt)
    return None


rec_all, errors, objects_read = [], 0, 0
with concurrent.futures.ThreadPoolExecutor(16) as ex:
    for res in ex.map(one, keys):
        if res is None:
            errors += 1
        else:
            objects_read += 1
            rec_all += res
s_iso, e_iso = START[:19], END[:19]
inwin = [(ts, oc, tl) for ts, oc, tl in rec_all if s_iso <= ts[:19] <= e_iso]


def epoch(ts):
    return datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()


def peaks(rows):
    times = sorted(epoch(r[0]) for r in rows)
    out = {}
    for w in (1, 2, 5, 10):
        best, j = 0, 0
        for i, t in enumerate(times):
            while times[j] <= t - w:
                j += 1
            best = max(best, i - j + 1)
        out["max_logged_in_any_%ds_window" % w] = best
    per_sec = collections.Counter(int(t) for t in times)
    out["seconds_with_2_or_more"], out["seconds_with_3_or_more"], out["seconds_with_4_or_more"] = (sum(1 for v in per_sec.values() if v >= n) for n in (2, 3, 4))
    out["records"] = len(times)
    return out


slot_taking = [r for r in inwin if r[1] in ("ok", "error")]
# which tools make up the busy seconds (counts only): for every second with 4 or more records, the tool names present; and the same peaks without the internal job tool(s) that log in bursts
per_sec_tools = collections.defaultdict(collections.Counter)
for ts, oc, tl in slot_taking:
    per_sec_tools[int(epoch(ts))][tl] += 1
busy = [c for c in per_sec_tools.values() if sum(c.values()) >= 4]
tool_in_busy = collections.Counter()
for c in busy:
    tool_in_busy.update(c)
per_tool_peak = collections.defaultdict(int)
for c in per_sec_tools.values():
    for tl, n in c.items():
        per_tool_peak[tl] = max(per_tool_peak[tl], n)
without_internal = [r for r in slot_taking if r[2] != "ms_site_children"]
doc = {"window_start": START, "window_end": END, "peak": None, "peak_status": "NOT COMPUTABLE FROM THE LAKE: the audit record has one timestamp (logging time) and no start or duration, so the overlap of each call's start and end cannot be formed",
       "method": "audit lake s3://opal-mcp-audit, LIST + GET of the objects whose key time lies within one minute of the window (%d objects, %d read, %d read errors), records with a tool key whose own ts lies in the window; "
                 "completions logged in the same 1, 2, 5 and 10 s windows (counts only). A call logged at t ended at t; k calls logged in one second ended in that second. This is a lower-bound proxy for the busiest moment, not the overlap." % (len(keys), objects_read, errors),
       "all_tool_records": peaks(inwin), "ok_or_error_records": peaks(slot_taking), "ok_or_error_without_ms_site_children": peaks(without_internal),
       "records_in_busy_seconds_by_tool": dict(tool_in_busy.most_common(12)), "max_per_second_by_tool": dict(sorted(per_tool_peak.items(), key=lambda kv: -kv[1])[:12]),
       "read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
print(json.dumps({k: doc[k] for k in ("window_start", "window_end", "ok_or_error_records", "ok_or_error_without_ms_site_children", "records_in_busy_seconds_by_tool", "max_per_second_by_tool")}))
