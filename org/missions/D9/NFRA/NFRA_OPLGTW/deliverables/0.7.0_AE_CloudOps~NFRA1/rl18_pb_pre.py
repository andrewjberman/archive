#!/usr/bin/env python
"""OG-rl-18 Phase B step 1: re-read the host BEFORE the deploy (the base must still be the live ref). READ ONLY. Prints one verdict line per condition and exits 0 only if every one holds:
  the live ref is 2923d1ee99, the unit limits are 5600M and 6400M, the target group is healthy, the .env has 65 keys, the host md5 walk equals the live ref (0 differ), the Elastic IP is associated,
  the instance is t4g.large and running, tools/list is 103, the host memory total is at least 7000 MB.
usage: python rl18_pb_pre.py <out dir>      (repository root)   Writes <out dir>/pre.json plus step1_before.json and host_md5_before.json. No address, ARN or account number is written."""
from __future__ import annotations

import hashlib
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
INSTANCE, LIVE = "i-07dccb1615503ac99", "2923d1ee99a014dab841b181af08ca67c643705e"
TRUNK = "daff5d69d7ce17adc5e751812f811e9d6a863572"
REL = "7863a9d65b11170a30d663d76834104eadd6ce6a"
ASK_SHA = "b8c6641a6e728de3e49b1c8facf9bde92118c2f7967037836bf008a8a19fdf38"
ASK = W + "NEVER_WIDEN_ASK_OG-rl-18.md"
HALVES = ["org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/%s/NEVER_WIDEN_HALF_%s_OG-rl-18_20261021.md" % (d, h) for d, h in (("1.0.0_SA_CTO~Z", "CTO"), ("2.0.0_SA_COO~O", "COO"), ("3.0.0_SA_CVO~Z", "CVO"))]
INBOX = "org/mcp/inbox/0.7.0_AE_CloudOps/~NFRA1/"
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
    "live ref is 2923d1ee99 (equals base_sha)": marker == LIVE,
    "unit limits 5600M and 6400M": unit.get("MemoryHigh") == "5872025600" and unit.get("MemoryMax") == "6710886400",
    "target group healthy": th == ["healthy"],
    ".env 65 keys": s1.get("env_key_count") == 65,
    "host md5 differ 0, missing 0": not md5.get("differ") and not md5.get("missing_on_host"),
    "Elastic IP associated": len(eip) == 1,
    "instance t4g.large and running": inst["InstanceType"] == "t4g.large" and inst["State"]["Name"] == "running",
    "tools/list 103": (s1.get("tools") or {}).get("tools_list_master_admin") == 103,
    "host memory total >= 7000 MB": int((s1.get("mem_line") or "0 0").split()[1]) >= 7000,
    "NRestarts 0": unit.get("NRestarts") == "0",
    "inside the window 2026-10-22 06:45Z-07:45Z": "2026-10-22T06:45:00Z" <= time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) < "2026-10-22T07:45:00Z",
    "ask sha256 equals the signed one": hashlib.sha256(io.open(ASK, "rb").read()).hexdigest() == ASK_SHA,
    "release branch head equals release_sha": subprocess.run(["git", "-C", "C:/tmp/og-rel-batch17", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip() == REL,
    "the three halves are SIGNED at the ask and the release": all(("SIGNED" in t and ASK_SHA[:12] in t and REL[:10] in t) for t in (subprocess.run(["git", "show", "HEAD:" + h], capture_output=True, text=True).stdout for h in HALVES)),
    "pending inbox is zero (recount)": sum(1 for f in os.listdir(INBOX) if os.path.isfile(INBOX + f) and not f.startswith(".")) == 0,
}
rec = {"read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "marker": marker, "instance_type": inst["InstanceType"], "state": inst["State"]["Name"], "target_health": th, "eip_associated": len(eip) == 1,
       "unit": unit, "env_key_count": s1.get("env_key_count"), "host_md5_differ": len(md5.get("differ", [])), "nrestarts": unit.get("NRestarts"), "checks": checks}
io.open(OUT + "pre.json", "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1) + "\n")
for k, v in checks.items():
    print("%-34s %s" % (k, "yes" if v else "NO"))
print("PRE-WINDOW READ: %s" % ("ALL HOLD" if all(checks.values()) else "STOP: a condition does not hold"))
sys.exit(0 if all(checks.values()) else 1)
