#!/usr/bin/env python
"""OG-rl-19 Phase B: one READ-ONLY look at where the service's memory sits (cat of /proc and cgroup files over SSM). Counts in MB, thread count, restarts. No request to the service, no write.
usage: python r3c_rss_read.py <out.json>"""
from __future__ import annotations

import io
import json
import sys
import time

import boto3

INSTANCE = "i-07dccb1615503ac99"
ssm = boto3.client("ssm", region_name="us-east-1")
SCRIPT = ("pid=$(systemctl show opal-gateway -p MainPID --value); f=/sys/fs/cgroup/system.slice/opal-gateway.service; "
          "echo PID=$pid; grep -E '^(VmRSS|RssAnon|RssFile|RssShmem|Threads):' /proc/$pid/status | tr -s ' \\t' ' ' | sed 's/^/S|/'; "
          "echo CG_CURRENT=$(cat $f/memory.current) CG_PEAK=$(cat $f/memory.peak 2>/dev/null || echo NA); grep -E '^(anon|file|kernel|slab|shmem) ' $f/memory.stat | sed 's/^/ST|/'; "
          "echo CHILDREN=$(pgrep -P $pid 2>/dev/null | wc -l); echo NRESTARTS=$(systemctl show opal-gateway -p NRestarts --value); date -u +NOW=%Y-%m-%dT%H:%M:%SZ")
cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [SCRIPT]}, TimeoutSeconds=60)["Command"]["CommandId"]
inv = None
for _ in range(40):
    time.sleep(2)
    try:
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
    except Exception:
        continue
    if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
        break
out = inv["StandardOutputContent"]
io.open(sys.argv[1], "w", encoding="utf-8", newline="\n").write(json.dumps({"ssm_status": inv["Status"], "ssm_command_id": cid, "raw": out.splitlines()}, indent=1) + "\n")
print(out)
