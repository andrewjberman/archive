#!/usr/bin/env python
"""OG-rz-2 Phase B read-back: the memory of the SERVICE's cgroup around ONE large reply. READ ONLY (cat of cgroup files over SSM).
  python rz2_mem.py start <name> [seconds=75]   -> starts an SSM command that samples memory.current every 0.5 s for <seconds> and returns at once (the command id is kept in the scratch folder)
  python rz2_mem.py collect <name> <out.json>   -> waits for it, writes before / max / after (MB), the cgroup's memory.peak and the limits (MB) as counts
The call under test is made BETWEEN the two commands, ONE at a time, never concurrent. Counts only."""
from __future__ import annotations

import io
import json
import sys
import time

import boto3

INSTANCE = "i-07dccb1615503ac99"
SCR = "C:/tmp/ap50_scratch/"
ssm = boto3.client("ssm", region_name="us-east-1")
mode, name = sys.argv[1:3]
SCRIPT = ("f=/sys/fs/cgroup/system.slice/opal-gateway.service; b=$(cat $f/memory.current); m=$b; end=$(( $(date +%%s) + %d )); "
          "while [ $(date +%%s) -lt $end ]; do v=$(cat $f/memory.current); [ $v -gt $m ] && m=$v; sleep 0.5; done; a=$(cat $f/memory.current); "
          "echo SAMPLE BEFORE=$b MAX=$m AFTER=$a PEAK=$(cat $f/memory.peak 2>/dev/null || echo NA) HIGH=$(cat $f/memory.high) LIMIT=$(cat $f/memory.max)")
if mode == "start":
    secs = int(sys.argv[3]) if len(sys.argv) > 3 else 75
    cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [SCRIPT % secs]}, TimeoutSeconds=secs + 60)["Command"]["CommandId"]
    open(SCR + "rz2mem_%s.id" % name, "w").write(cid)
    print("sampler started for %s (%d s); command %s" % (name, secs, cid[:8]))
else:
    cid = open(SCR + "rz2mem_%s.id" % name).read().strip()
    inv = None
    for _ in range(80):
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except Exception:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    line = [ln for ln in inv["StandardOutputContent"].splitlines() if ln.startswith("SAMPLE")][-1]
    kv = dict(p.split("=", 1) for p in line.split()[1:])
    mb = lambda x: round(int(x) / 1048576.0, 1) if x.isdigit() else None  # noqa: E731
    rec = {"name": name, "before_mb": mb(kv["BEFORE"]), "max_mb": mb(kv["MAX"]), "after_mb": mb(kv["AFTER"]), "cgroup_peak_mb": mb(kv["PEAK"]), "memory_high_mb": mb(kv["HIGH"]), "memory_max_mb": mb(kv["LIMIT"]),
           "ssm_status": inv["Status"], "ssm_command_id": cid}
    io.open(sys.argv[3], "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1) + "\n")
    print(json.dumps(rec))
