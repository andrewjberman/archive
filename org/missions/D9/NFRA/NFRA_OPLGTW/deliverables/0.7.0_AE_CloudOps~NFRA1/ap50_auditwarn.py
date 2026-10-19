#!/usr/bin/env python
"""OG-ap-50 Phase B: the audit_failure_counter record (OG-ap-48 AMENDMENT A1 governs a WARN): the number of `audit-lake WARN` lines in the service journal over the read-back window and the counter value (the last count= those lines print,
0 when there is no line). READ ONLY (journalctl over SSM). Counts and exception CLASS names only.
usage: python ap50_auditwarn.py <start_utc> <end_utc> <out.json>"""
from __future__ import annotations

import io
import json
import sys
import time

import boto3

START, END, OUT = sys.argv[1:4]
INSTANCE = "i-07dccb1615503ac99"
ssm = boto3.client("ssm", region_name="us-east-1")
cmd = ("journalctl -u opal-gateway --since '%s' --until '%s' --no-pager -o cat | grep 'audit-lake WARN' > /tmp/ap50_warn.txt; echo LINES=$(grep -c . /tmp/ap50_warn.txt); "
       "echo LASTCOUNT=$(grep -o 'count=[0-9]*' /tmp/ap50_warn.txt | tail -1 | cut -d= -f2); echo CLASSES=$(grep -oE '[A-Za-z]+(Error|Exception|Timeout)[A-Za-z]*' /tmp/ap50_warn.txt | sort -u | tr '\n' ' '); rm -f /tmp/ap50_warn.txt") % (START.replace("T", " ").rstrip("Z"), END.replace("T", " ").rstrip("Z"))
cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": ["TZ=UTC " + cmd]}, TimeoutSeconds=120)["Command"]["CommandId"]
for _ in range(40):
    time.sleep(3)
    try:
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
    except Exception:
        continue
    if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
        break
kv = dict(ln.split("=", 1) for ln in inv["StandardOutputContent"].splitlines() if "=" in ln)
out = {"journal_lines_readback": int(kv.get("LINES", "0") or 0), "counter_value": int(kv.get("LASTCOUNT", "0") or 0), "classes_seen": kv.get("CLASSES", "").split(),
       "method": "journalctl -u opal-gateway between %s and %s (the access-log window), grep -c 'audit-lake WARN'; the counter value is the last count= those lines print, 0 when there is no line; the counter is read by no route, so the journal line is its only observation" % (START, END),
       "read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "ssm_command_id": cid, "ssm_status": inv["Status"]}
io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(out, indent=1) + "\n")
print(json.dumps(out, indent=1))
