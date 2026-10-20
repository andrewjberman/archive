#!/usr/bin/env python
"""OG-rz-2 Phase B step 1 / COO H5: re-read the host BEFORE the stop. READ ONLY. Prints one verdict line per condition and exits 0 only if every one holds:
  the live ref is 6d1b5dcb64, the unit limits are 1200M and 1400M, the target group is healthy, the .env has 65 keys, the host md5 walk equals the live ref (0 differ), the Elastic IP is associated,
  the instance is t4g.small and running.
usage: python rz2_pb_pre.py <out dir>      (repository root)   Writes <out dir>/pre.json plus step1_before.json and host_md5_before.json. No address, ARN or account number is written."""
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
INSTANCE, LIVE = "i-07dccb1615503ac99", "6d1b5dcb64b945deb98664c6ae078d8f1e8a6c5c"
TRUNK = "9095ce68f399f8fc6406ed1d9db674319fdb3f76"
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
    "live ref is 6d1b5dcb64": marker == LIVE,
    "unit limits 1200M and 1400M": unit.get("MemoryHigh") == "1258291200" and unit.get("MemoryMax") == "1468006400",
    "target group healthy": th == ["healthy"],
    ".env 65 keys": s1.get("env_key_count") == 65,
    "host md5 differ 0, missing 0": not md5.get("differ") and not md5.get("missing_on_host"),
    "Elastic IP associated": len(eip) == 1,
    "instance t4g.small and running": inst["InstanceType"] == "t4g.small" and inst["State"]["Name"] == "running",
    "NRestarts 0": unit.get("NRestarts") == "0",
}
rec = {"read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "marker": marker, "instance_type": inst["InstanceType"], "state": inst["State"]["Name"], "target_health": th, "eip_associated": len(eip) == 1,
       "unit": unit, "env_key_count": s1.get("env_key_count"), "host_md5_differ": len(md5.get("differ", [])), "nrestarts": unit.get("NRestarts"), "checks": checks}
io.open(OUT + "pre.json", "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1) + "\n")
for k, v in checks.items():
    print("%-34s %s" % (k, "yes" if v else "NO"))
print("PRE-WINDOW READ: %s" % ("ALL HOLD" if all(checks.values()) else "STOP: a condition does not hold"))
sys.exit(0 if all(checks.values()) else 1)
