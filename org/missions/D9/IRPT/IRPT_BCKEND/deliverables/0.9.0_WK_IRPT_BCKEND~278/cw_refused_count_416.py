"""IB-pr-416 AMENDMENT 1 (2.0.0_SA_COO~P2): count the performance-report requests irpt-performance-adapter refused since a start instant.
    python cw_refused_count_416.py <start_iso_utc> <out_json>
Reads /aws/lambda/irpt-performance-adapter with boto3 `filter_log_events` through its paginator (every page, counted CLIENT-SIDE; the
window and the page count are printed). Counts only: no message text, account id, balance, fee or flow is written. A request is one
`irpt_error` line whose operation is performance-report (served._record prints exactly one per refused request); the TypeError subset
is the `irpt_internal` lines whose exception_type is TypeError for that operation (the Enforcer(load_report_owner=) failure). AWS read only.
ASCII only.
"""
import datetime
import json
import sys

import boto3

start_iso, out_path = sys.argv[1], sys.argv[2]
GROUP = "/aws/lambda/irpt-performance-adapter"
OP = "performance-report"
start = datetime.datetime.strptime(start_iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
end = datetime.datetime.now(datetime.timezone.utc)
logs = boto3.client("logs", region_name="us-east-1")
pages = events = 0
errors, internal, internal_typeerror, codes = 0, 0, 0, {}
first = last = None
for page in logs.get_paginator("filter_log_events").paginate(
        logGroupName=GROUP, startTime=int(start.timestamp() * 1000), endTime=int(end.timestamp() * 1000), filterPattern='"%s"' % OP):
    pages += 1
    for ev in page.get("events", []):
        events += 1
        msg = ev.get("message", "").strip()
        if not msg.startswith("{"):
            continue
        try:
            doc = json.loads(msg)
        except ValueError:
            continue
        if doc.get("operation") != OP:
            continue
        ts = ev["timestamp"]
        first = ts if first is None else min(first, ts)
        last = ts if last is None else max(last, ts)
        if doc.get("event") == "irpt_error":
            errors += 1
            code = str(doc.get("public_reason_code"))
            codes[code] = codes.get(code, 0) + 1
        elif doc.get("event") == "irpt_internal":
            internal += 1
            if doc.get("exception_type") == "TypeError":
                internal_typeerror += 1


def iso(ms):
    return datetime.datetime.fromtimestamp(ms / 1000.0, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if ms else None


doc = {"log_group": GROUP, "operation": OP, "window_start": start_iso, "window_end": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
       "pages_read": pages, "events_matched_by_filter": events,
       "refused_requests_irpt_error": errors, "refusals_by_public_reason_code": codes,
       "irpt_internal_events": internal, "irpt_internal_typeerror_events": internal_typeerror,
       "first_event": iso(first), "last_event": iso(last), "counted": "client-side over every page; counts only"}
with open(out_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(doc, indent=1, sort_keys=True) + "\n")
print(json.dumps(doc, sort_keys=True))
