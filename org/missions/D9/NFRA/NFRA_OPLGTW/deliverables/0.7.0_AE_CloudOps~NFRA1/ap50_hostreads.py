#!/usr/bin/env python
"""OG-ap-50 Phase B: the host clock + failed units (clock.txt), the live unit limits + marker + named-file md5 (limits.txt), and the lease parameter (lease_final.json), read in the formats ap50_served_build.py parses.
READ ONLY (chronyc tracking, systemctl, md5sum, cat, an SSM describe-parameters); NO SSM write, nothing armed.
usage: python ap50_hostreads.py <out dir>      (repository root)"""
from __future__ import annotations

import io
import json
import sys
import time

import boto3

INSTANCE = "i-07dccb1615503ac99"
NAMED = ["harvest_research", "harvest_figures", "harvest_identity", "harvest_keys", "graph", "probe_listener", "audit", "admin_api", "family_depth"]
OUT = sys.argv[1].rstrip("/") + "/"
ssm = boto3.client("ssm", region_name="us-east-1")


def run(cmds):
    cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": cmds}, TimeoutSeconds=120)["Command"]["CommandId"]
    for _ in range(40):
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except Exception:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            return inv["Status"], inv["StandardOutputContent"], cid
    raise SystemExit("ssm did not finish")


st, out, cid1 = run(["echo BEGIN", "date -u +%FT%TZ", "chronyc tracking", "echo FAILED_COUNT=$(systemctl --failed --no-legend --plain | grep -c .)", "systemctl --failed --no-pager", "echo END"])
io.open(OUT + "clock.txt", "w", encoding="utf-8", newline="\n").write(out.replace("\r", ""))
cmds = ["echo BEGIN", "date -u +%FT%TZ", "echo CGMAX=$(cat /sys/fs/cgroup/system.slice/opal-gateway.service/memory.max)", "echo CGHIGH=$(cat /sys/fs/cgroup/system.slice/opal-gateway.service/memory.high)",
        "echo MARKER=$(cat /opt/opal-gateway/.deployed_commit)"]
cmds += ["echo MD5_%s=$(md5sum /opt/opal-gateway/app/%s.py | cut -d' ' -f1)" % (n, n) for n in NAMED]
cmds += ["systemctl show opal-gateway -p MainPID -p NRestarts -p MemoryHigh -p MemoryMax -p OOMScoreAdjust", "echo END"]
st2, out2, cid2 = run(cmds)
io.open(OUT + "limits.txt", "w", encoding="utf-8", newline="\n").write(out2.replace("\r", ""))
ps = ssm.describe_parameters(ParameterFilters=[{"Key": "Name", "Option": "BeginsWith", "Values": ["/opal-gateway/probe/"]}])["Parameters"]
lease = {"parameters_under_probe_prefix": len(ps), "get_parameter_found": any(p["Name"] == "/opal-gateway/probe/lease" for p in ps), "absent": not any(p["Name"] == "/opal-gateway/probe/lease" for p in ps),
         "read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "puts_made_by_this_seat": 0}
io.open(OUT + "lease_final.json", "w", encoding="utf-8", newline="\n").write(json.dumps(lease, indent=1) + "\n")
print("clock ssm", st, cid1, "| limits ssm", st2, cid2)
print(out.replace("\r", ""))
print(out2.replace("\r", ""))
print(lease)
