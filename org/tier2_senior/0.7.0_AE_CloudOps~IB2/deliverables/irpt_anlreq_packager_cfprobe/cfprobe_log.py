"""IRPT_ANLREQ TO-READ-PACKAGER-CFPROBE step 2 (applier 0.7.0_AE_CloudOps~IB2), READ ONLY: the authorizer Lambda's log lines around the probe's second.

  python cfprobe_log.py     prints the R2 lines and writes r2_lines.txt beside this file

Only the time and a closed decision word are printed; a log line's content (which may carry an e-mail of a synthetic or real login) is never printed.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
GROUP = "/aws/lambda/opal-portal-authorizer"
CALL = datetime(2026, 10, 20, 10, 24, 35, tzinfo=timezone.utc)
lines = []


def ms(dt):
    return int(dt.timestamp() * 1000)


def word(message):
    if "Origin verification FAILED" in message:
        return "ORIGIN_VERIFICATION_FAILED"
    if "Origin verification unavailable" in message:
        return "ORIGIN_VERIFICATION_UNAVAILABLE"
    if "Token verified successfully" in message:
        return "ADMITTED"
    if "No token provided" in message:
        return "NO_TOKEN"
    return None


logs = boto3.client("logs", region_name="us-east-1")
total, hits = 0, []
for pg in logs.get_paginator("filter_log_events").paginate(logGroupName=GROUP, startTime=ms(CALL) - 30000, endTime=ms(CALL) + 30000):
    for ev in pg["events"]:
        total += 1
        w = word(ev["message"])
        if w:
            t = datetime.fromtimestamp(ev["timestamp"] / 1000.0, timezone.utc).strftime("%H:%M:%S")
            hits.append((t, w))
lines.append("NOTE-R2 window 10:24:05..10:25:05 log group %s holds %d events; %d carry a decision word" % (GROUP, total, len(hits)))
for t, w in hits:
    lines.append("R2 %sZ reason=%s" % (t, w))
if not hits:
    lines.append("R2 NOT-FOUND no decision line in %s between 10:24:05Z and 10:25:05Z" % GROUP)
text = "\n".join(lines) + "\n"
(HERE / "r2_lines.txt").write_text(text, encoding="ascii", errors="replace", newline="\n")
print(text)
