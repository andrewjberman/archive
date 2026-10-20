#!/usr/bin/env python
"""OG-rl-17 Phase B step 1: re-read the host BEFORE the deploy (the base must still be the live ref). READ ONLY. Prints one verdict line per condition and exits 0 only if every one holds:
  the live ref is 13917ef993, the unit limits are 5600M and 6400M, the target group is healthy, the .env has 65 keys, the host md5 walk equals the live ref (0 differ), the Elastic IP is associated,
  the instance is t4g.large and running, tools/list is 103, the host memory total is at least 7000 MB.
usage: python rl17_pb_pre.py <out dir>      (repository root)   Writes <out dir>/pre.json plus step1_before.json and host_md5_before.json. No address, ARN or account number is written."""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import time

import boto3

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
OUT = sys.argv[1].rstrip("/") + "/"
os.makedirs(OUT, exist_ok=True)
INSTANCE, LIVE = "i-07dccb1615503ac99", "13917ef993207bee6b8df0124eec5444da4d62cd"
TRUNK = "c0a0ee2e9c21c4b9d4d0080b095240038be09354"
subprocess.run([sys.executable, W + "ap38_step1.py", OUT + "step1_before.json"], capture_output=True, text=True)
subprocess.run([sys.executable, W + "ap36_host_md5.py", LIVE, OUT + "host_md5_before.json", TRUNK], capture_output=True, text=True)
s1 = json.load(io.open(OUT + "step1_before.json", encoding="utf-8"))
md5 = json.load(io.open(OUT + "host_md5_before.json", encoding="utf-8"))
ec2, elb = boto3.client("ec2", region_name="us-east-1"), boto3.client("elbv2", region_name="us-east-1")
inst = ec2.describe_instances(InstanceIds=[INSTANCE])["Reservations"][0]["Instances"][0]
eip = ec2.describe_addresses(Filters=[{"Name": "instance-id", "Values": [INSTANCE]}])["Addresses"]
th = []
for tg in elb.describe_target_groups()["TargetGroups"]:
    for d in elb.describe_target_health(TargetGroupArn=tg["TargetGroupArn"])["TargetHealthDescriptions"]:
        if d["Target"]["Id"] == INSTANCE:
            th.append(d["TargetHealth"]["State"])
marker = (s1.get("marker") or "").split("=", 1)[-1]
unit = s1.get("unit", {})
checks = {
    "live ref is 13917ef993": marker == LIVE,
    "unit limits 5600M and 6400M": unit.get("MemoryHigh") == "5872025600" and unit.get("MemoryMax") == "6710886400",
    "target group healthy": th == ["healthy"],
    ".env 65 keys": s1.get("env_key_count") == 65,
    "host md5 differ 0, missing 0": not md5.get("differ") and not md5.get("missing_on_host"),
    "Elastic IP associated": len(eip) == 1,
    "instance t4g.large and running": inst["InstanceType"] == "t4g.large" and inst["State"]["Name"] == "running",
    "tools/list 103": (s1.get("tools") or {}).get("tools_list_master_admin") == 103,
    "host memory total >= 7000 MB": int((s1.get("mem_line") or "0 0").split()[1]) >= 7000,
    "NRestarts 0": unit.get("NRestarts") == "0",
}
rec = {"read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "marker": marker, "instance_type": inst["InstanceType"], "state": inst["State"]["Name"], "target_health": th, "eip_associated": len(eip) == 1,
       "unit": unit, "env_key_count": s1.get("env_key_count"), "host_md5_differ": len(md5.get("differ", [])), "nrestarts": unit.get("NRestarts"), "checks": checks}
io.open(OUT + "pre.json", "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1) + "\n")
for k, v in checks.items():
    print("%-34s %s" % (k, "yes" if v else "NO"))
print("PRE-WINDOW READ: %s" % ("ALL HOLD" if all(checks.values()) else "STOP: a condition does not hold"))
sys.exit(0 if all(checks.values()) else 1)
