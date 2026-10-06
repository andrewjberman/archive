"""AMGT_RESAPP round 73 AMGT-aw-7 -- the /freshness WARM latency, AMENDMENT 1's "also report".

AMENDMENT 1: "Also report the warm latency of /api/scoped/amgt/freshness (3 calls): it now reads
~105 ledgers per request (aw-3)."  The COO half's outcome table adds: "a warm read over 2,000 ms is
a row, not a rollback".

Invoked exactly as round 73's own check does it -- boto3 lambda.invoke with the same HTTP-shaped
event -- so the number is comparable to the checks' own reads rather than to a different transport.
The function must already be WARM; this does not try to measure a cold start.

Prints the per-call duration, the status, the covered row count (the denominator the latency is per),
and how many of the three calls sit over the 2,000 ms bar.
"""

from __future__ import annotations

import json
import time

import boto3

FN = "opal-amgt-scoped-api"
PATH = "/api/scoped/amgt/freshness"
CALLS = 3
BAR_MS = 2000


def _event(path, query=None):
    return {
        "rawPath": path,
        "requestContext": {"http": {"method": "GET"}},
        "headers": {"x-firm-id": "opal"},
        "queryStringParameters": query,
    }


def main():
    lam = boto3.client("lambda", region_name="us-east-1")

    # One discarded warm-up invoke: the bar is a WARM bar, and the first call after an idle can
    # carry an init. Naming it here so the three reported calls are unambiguously warm.
    lam.invoke(FunctionName=FN, Payload=json.dumps(_event(PATH)).encode())

    durations = []
    statuses = []
    rows_seen = []
    for _ in range(CALLS):
        t0 = time.perf_counter()
        r = lam.invoke(FunctionName=FN, Payload=json.dumps(_event(PATH)).encode())
        payload = json.loads(r["Payload"].read())
        ms = (time.perf_counter() - t0) * 1000.0
        durations.append(ms)
        statuses.append(payload.get("statusCode"))
        try:
            body = json.loads(payload.get("body") or "null")
        except ValueError:
            body = None
        rows = body.get("rows") if isinstance(body, dict) else None
        rows_seen.append(len(rows) if isinstance(rows, list) else None)

    over = [d for d in durations if d > BAR_MS]
    print("AW7 /freshness WARM latency -- %d calls, bar %d ms" % (CALLS, BAR_MS))
    for i, (ms, st, n) in enumerate(zip(durations, statuses, rows_seen), 1):
        print("   call %d: %8.1f ms  status %s  rows %s" % (i, ms, st, n))
    print("   min %.1f ms  max %.1f ms  over-bar %d of %d" % (min(durations), max(durations), len(over), CALLS))
    print("   statuses %s | row counts %s" % (statuses, rows_seen))
    # The verdict line is deliberately NOT an exit code: AMENDMENT 1 makes this REPORT-ONLY, and an
    # over-bar read is a surprise row rather than a rollback. Printing a verdict that a caller could
    # mistake for a gate would misrepresent what the halves asked for.
    print("AW7 FRESHNESS LATENCY: %s (report-only; over-bar is a row, never a rollback)"
          % ("ALL UNDER BAR" if not over else "%d OVER BAR" % len(over)))


if __name__ == "__main__":
    main()
