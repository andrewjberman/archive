"""TCKT_VNEXT TV-r-1 trace -- READ-ONLY. Reads what Alyssa's own filing left behind (CTO ruling msg 1648).

Usage: python tv_r1_trace.py --since 2026-10-08T21:00:00Z [--ticket <ticket_id>] [--out <path.json>]

Reads, in order:
  1. opal-tickets: every analysis_request ticket created at/after --since (full scan, paginated, denominator printed).
     Kept: ticket_id, status, created_at, created_by, firm answer, attachment ids, report_ref, claimed_by, assignee,
     event names + times. Answer VALUES other than the firm are not copied (client names stay out of the record).
  2. opal-ticket-api and irpt-ycharts-generate CloudWatch logs over [since, now] filtered by the ticket id and the
     attachment's upload_id / input_id (event counts printed per filter; a zero is printed as a zero, not omitted).
Writes nothing to AWS. No credential is read.
"""
import argparse
import datetime as dt
import json
import sys

import boto3

REGION = "us-east-1"
TABLE = "opal-tickets"
FUNCTIONS = ("opal-ticket-api", "irpt-ycharts-generate")


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def scan_tickets(since):
    tbl = boto3.resource("dynamodb", region_name=REGION).Table(TABLE)
    items, kwargs, pages = [], {}, 0
    while True:
        r = tbl.scan(**kwargs)
        pages += 1
        items.extend(r.get("Items", []))
        if "LastEvaluatedKey" not in r:
            break
        kwargs["ExclusiveStartKey"] = r["LastEvaluatedKey"]
    hits = [i for i in items if i.get("ticket_type") == "analysis_request" and str(i.get("created_at", "")) >= since]
    print(f"OK: scanned {TABLE}: {len(items)} item(s) over {pages} page(s); analysis_request since {since}: {len(hits)}")
    return hits


def keep(t):
    answers = t.get("answers") or {}
    events = [{"action": e.get("action"), "ts": e.get("ts"), "actor": e.get("actor")} for e in (t.get("events") or [])]
    return {
        "ticket_id": t.get("ticket_id"), "status": t.get("status"), "created_at": t.get("created_at"),
        "created_by": t.get("created_by"), "firm": answers.get("firm"), "answer_keys": sorted(answers),
        "attachment": t.get("attachment"), "report_ref": t.get("report_ref"),
        "claimed_by": t.get("claimed_by"), "assignee": t.get("assignee"), "events": events,
    }


def log_hits(fn, start_ms, end_ms, term):
    logs = boto3.client("logs", region_name=REGION)
    n, kwargs, samples = 0, {}, []
    while True:
        r = logs.filter_log_events(logGroupName=f"/aws/lambda/{fn}", startTime=start_ms, endTime=end_ms,
                                   filterPattern=f'"{term}"', **kwargs)
        for e in r.get("events", []):
            n += 1
            if len(samples) < 5:
                samples.append({"ts": iso(dt.datetime.fromtimestamp(e["timestamp"] / 1000, dt.timezone.utc)),
                                "msg": e["message"][:300]})
        if not r.get("nextToken") or r.get("nextToken") == kwargs.get("nextToken"):
            break
        kwargs["nextToken"] = r["nextToken"]
    return n, samples


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", required=True)
    ap.add_argument("--ticket")
    ap.add_argument("--out")
    ap.add_argument("--exclude-created-by", nargs="*", default=[])
    a = ap.parse_args(argv)
    since_dt = dt.datetime.fromisoformat(a.since.replace("Z", "+00:00"))
    now = dt.datetime.now(dt.timezone.utc)
    tickets = [keep(t) for t in scan_tickets(a.since)]
    if a.exclude_created_by:
        tickets = [t for t in tickets if t["created_by"] not in a.exclude_created_by]
        print(f"OK: excluded created_by {a.exclude_created_by}: {len(tickets)} left")
    if a.ticket:
        tickets = [t for t in tickets if t["ticket_id"] == a.ticket]
        print(f"OK: filtered to --ticket {a.ticket}: {len(tickets)}")
    result = {"since": a.since, "read_at": iso(now), "tickets": tickets, "logs": []}
    start_ms, end_ms = int(since_dt.timestamp() * 1000), int(now.timestamp() * 1000)
    for t in tickets:
        att = t.get("attachment") or {}
        ref = t.get("report_ref") or {}
        terms = [x for x in (t["ticket_id"], att.get("upload_id"), att.get("input_id"),
                             ref.get("request_id") if isinstance(ref, dict) else None) if x]
        for fn in FUNCTIONS:
            for term in terms:
                n, samples = log_hits(fn, start_ms, end_ms, term)
                print(f"{'OK' if n else 'WARN'}: {fn} log events matching {term}: {n}")
                result["logs"].append({"function": fn, "term": term, "count": n, "samples": samples})
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, default=str)
        print(f"OK: wrote {a.out}")
    else:
        print(json.dumps(result, indent=2, default=str))
    return 0 if tickets else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
