"""AMGT_RESAPP round 62 analysis (@3d590fcb31): the one-off warm-up before Andrew's demo read. TWO SEQUENTIAL read-only invokes of
BA_US_Equity /timeline/day/2026-09-08. The first may hit the 18 s deadline and leave the silver read filling that sandbox's cache;
the second must carry headlines. An invoke, never a deploy; no scheduler.

Prints per call: UTC time, status, Duration / Init Duration (REPORT), article count, headlines present, headline_reason present.
Verdict: THE SECOND CALL CARRIES HEADLINES: YES|NO.
"""
from __future__ import annotations

import base64
import datetime
import json
import re
import sys

import boto3

FUNCTION = "opal-amgt-scoped-api"
PATH = "/api/scoped/amgt/security/BA_US_Equity/timeline/day/2026-09-08"


def call(lam):
    event = {"rawPath": PATH, "headers": {"x-firm-id": "opal"},
             "requestContext": {"http": {"method": "GET", "path": PATH}}, "queryStringParameters": None}
    r = lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(event).encode("utf-8"), LogType="Tail")
    raw = json.loads(r["Payload"].read())
    log = base64.b64decode(r.get("LogResult") or b"").decode("utf-8", "replace")
    rep = next((ln for ln in log.splitlines() if ln.startswith("REPORT")), "")
    dur = re.search(r"\tDuration: ([\d.]+) ms", rep)
    init = re.search(r"Init Duration: ([\d.]+) ms", rep)
    body = json.loads(raw.get("body") or "{}") if isinstance(raw, dict) else {}
    arts = body.get("articles") or []
    return {"at": datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%SZ"), "status": raw.get("statusCode"),
            "duration_ms": float(dur.group(1)) if dur else None, "init_ms": float(init.group(1)) if init else None,
            "articles": len(arts), "with_headline": sum(1 for a in arts if a.get("headline")),
            "headline_reason": bool(body.get("headline_reason"))}


def main():
    lam = boto3.client("lambda", region_name="us-east-1")
    first = call(lam)
    second = call(lam)
    for n, c in (("first", first), ("second", second)):
        print(f"{n}: {c}")
    ok = second["status"] == 200 and second["articles"] > 0 and second["with_headline"] == second["articles"] and not second["headline_reason"]
    print(f"THE SECOND CALL CARRIES HEADLINES: {'YES' if ok else 'NO'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
