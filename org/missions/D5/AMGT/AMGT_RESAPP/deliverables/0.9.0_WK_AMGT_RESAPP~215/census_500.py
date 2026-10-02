"""AMGT-an-6 (round 64, analysis ruling 3, row Z-S238): the 500 census -- READ-ONLY attribution, never an alarm.

  python census_500.py --days N [--group /aws/lambda/opal-amgt-scoped-api] [--region us-east-1]
  python census_500.py --selftest

Reads the function's CloudWatch Logs (filter_log_events, a read-only logs call) over the last N days and groups the
window's 500s BY SIGNATURE, so N failures are not read as N causes:

  * an `AMGT_500 {json}` line (the post-fix period) -> "<exception_class> on <route>"
  * a Lambda `[ERROR] <Class>: ...` line or a `Task timed out after` line with no AMGT_500 line for the same request
    (the pre-fix period: the fault escaped the handler) -> "unattributed: <the log evidence>"
  * a REPORT line whose Status is error/timeout with neither of the above -> "unattributed: REPORT Status: <status>"

One request id is ONE 500, however many log lines it wrote. The denominator printed is the 500s over the invocations
(distinct REPORT request ids) in the window. No write, no alarm, no notification, no monitor.
"""
from __future__ import annotations

import argparse
import collections
import datetime
import json
import re
import sys

GROUP = "/aws/lambda/opal-amgt-scoped-api"
REGION = "us-east-1"
UUID = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
ERROR_LINE = re.compile(r"^\[ERROR\] ([A-Za-z_][\w.]*): ?(.*)")
TIMEOUT_LINE = re.compile(r"Task timed out after ([\d.]+) seconds")
REPORT_STATUS = re.compile(r"\bStatus: (\w+)")
REPORT_REQ = re.compile(r"^REPORT RequestId: (\S+)")
PATTERN = '?"AMGT_500" ?"[ERROR]" ?"Task timed out" ?"REPORT RequestId"'


def _head(text, n=90):
    return " ".join(str(text).split())[:n]


def classify(events):
    """events: iterable of (log stream name, message) in log order. A Lambda `[ERROR] ...` or timeout line names no
    request id: it belongs to the next REPORT line of the SAME stream (one invocation at a time per stream), which is
    how two lines of one failure stay one 500. Returns (invocations, found): the set of REPORT request ids, and a map
    request id -> (signature, evidence) of the 500s."""
    invocations = set()
    amgt = {}
    errors = {}
    timeouts = {}
    reports = {}
    anon = 0
    pending = collections.defaultdict(list)  # stream -> anonymous failure keys awaiting their REPORT line
    for stream, message in events:
        text = message.rstrip()
        rid_match = UUID.search(text)
        rid = rid_match.group(0) if rid_match else None
        report = REPORT_REQ.match(text)
        if report:
            rid = report.group(1)
            invocations.add(rid)
            for key in pending.pop(stream, []):
                for table in (errors, timeouts):
                    if key in table:
                        table.setdefault(rid, table.pop(key))
            status = REPORT_STATUS.search(text)
            if status and status.group(1).lower() in ("error", "timeout"):
                reports[rid] = status.group(1).lower()
            continue
        if "AMGT_500" in text:
            try:
                record = json.loads(text.split("AMGT_500", 1)[1].strip())
            except ValueError:
                record = {"exception_class": "unparsed", "route": None, "message": _head(text)}
            rid = record.get("request_id") or rid
            if rid is None:
                anon += 1
                rid = "anon-%d" % anon
            amgt[rid] = record
            continue
        error = ERROR_LINE.match(text)
        timeout = TIMEOUT_LINE.search(text)
        if error or timeout:
            if rid is None:
                anon += 1
                rid = "anon-%d" % anon
                pending[stream].append(rid)
            if error:
                errors.setdefault(rid, "[ERROR] %s: %s" % (error.group(1), _head(error.group(2))))
            else:
                timeouts.setdefault(rid, "Task timed out after %s seconds" % timeout.group(1))
    found = {}
    for rid in set(amgt) | set(errors) | set(timeouts) | set(reports):
        if rid in amgt:
            record = amgt[rid]
            found[rid] = ("%s on %s" % (record.get("exception_class") or "<no class>", record.get("route") or "<no route>"),
                          _head(record.get("message") or ""))
        elif rid in errors:
            found[rid] = ("unattributed: %s" % errors[rid].split(":", 1)[0], errors[rid])
        elif rid in timeouts:
            found[rid] = ("unattributed: %s" % re.sub(r"[\d.]+", "N", timeouts[rid]), timeouts[rid])
        else:
            found[rid] = ("unattributed: REPORT Status: %s" % reports[rid], "REPORT Status: %s" % reports[rid])
    return invocations, found


def read_events(days, group, region):
    import boto3

    client = boto3.client("logs", region_name=region)
    start = int((datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)).timestamp() * 1000)
    kwargs = {"logGroupName": group, "startTime": start, "filterPattern": PATTERN}
    messages = []  # (log stream, message), in the order the API returned them
    pages = 0
    while True:
        page = client.filter_log_events(**kwargs)
        pages += 1
        messages.extend((e.get("logStreamName"), e["message"]) for e in page.get("events", []))
        token = page.get("nextToken")
        if not token:
            break
        kwargs["nextToken"] = token
    return messages, pages


def report(days, invocations, found, extra=""):
    print("DENOMINATOR: %d 500s across %d invocations in %d days%s" % (len(found), len(invocations), days, extra))
    table = collections.Counter(sig for sig, _ in found.values())
    sample = {}
    for rid, (sig, ev) in sorted(found.items()):
        sample.setdefault(sig, "%s (request %s)" % (ev, rid))
    print("SIGNATURES: %d distinct signature(s) for %d 500s" % (len(table), len(found)))
    for sig, n in sorted(table.items(), key=lambda kv: (-kv[1], kv[0])):
        print("  %5d  %s  | e.g. %s" % (n, sig, sample[sig]))


def selftest():
    uid = ["11111111-1111-1111-1111-11111111111%d" % i for i in range(1, 6)]
    planted = {"request_id": uid[2], "route": "/security/{security_key}/overlay", "security_key": "BA_US_Equity",
               "exception_class": "RuntimeError", "message": "planted"}
    events = [
        "[ERROR] KeyError: 'x'\nTraceback (most recent call last):",
        "REPORT RequestId: %s\tDuration: 1.0 ms\tStatus: error" % uid[0],
        "2026-10-02T00:00:00Z %s Task timed out after 30.01 seconds" % uid[1],
        "REPORT RequestId: %s\tDuration: 30000 ms" % uid[1],
        "[ERROR]\t2026-10-02T00:00:01Z\t%s\tAMGT_500 %s" % (uid[2], json.dumps(planted)),
        "AMGT_500 %s" % json.dumps(planted),
        "REPORT RequestId: %s\tDuration: 5 ms" % uid[2],
        "REPORT RequestId: %s\tDuration: 5 ms" % uid[3],
    ]
    invocations, found = classify([("s1", m) for m in events])
    sigs = sorted(sig for sig, _ in found.values())
    assert len(invocations) == 4, invocations
    assert sigs == sorted(["RuntimeError on /security/{security_key}/overlay", "unattributed: [ERROR] KeyError",
                           "unattributed: Task timed out after N seconds"]), sigs
    report(1, invocations, found, " (SELFTEST on planted events)")
    print("SELFTEST OK: one request id is one 500; the planted AMGT_500 line groups by class and route")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int)
    ap.add_argument("--group", default=GROUP)
    ap.add_argument("--region", default=REGION)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.days or a.days < 1:
        ap.error("--days N (N >= 1) is required")
    messages, pages = read_events(a.days, a.group, a.region)
    invocations, found = classify(messages)
    print("READ: group %s region %s, %d matching log event(s) in %d page(s), read-only filter_log_events"
          % (a.group, a.region, len(messages), pages))
    report(a.days, invocations, found)
    return 0


if __name__ == "__main__":
    sys.exit(main())
