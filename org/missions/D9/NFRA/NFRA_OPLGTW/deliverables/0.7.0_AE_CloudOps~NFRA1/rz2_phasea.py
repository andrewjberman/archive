#!/usr/bin/env python
"""OG-rz-2 Phase A steps 3 and 4: the before-record and the plan facts. READ ONLY (describes, an SSM read, comp-find, a targeted terraform PLAN with -lock=false and no -out). NO apply, NO deploy, NO restart.
Counts, statuses and names only: no public IP address, ARN, account number or e-mail is written or printed.
  python rz2_phasea.py        (repository root)
Writes W/RZ2_BEFORE.json (and prints the facts the plan step needs)."""
from __future__ import annotations

import io
import json
import re
import subprocess
import time

import boto3

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
INSTANCE = "i-07dccb1615503ac99"
REGION = "us-east-1"
ec2 = boto3.client("ec2", region_name=REGION)
elb = boto3.client("elbv2", region_name=REGION)
ssm = boto3.client("ssm", region_name=REGION)

inst = ec2.describe_instances(InstanceIds=[INSTANCE])["Reservations"][0]["Instances"][0]
ip = inst.get("PublicIpAddress")
eips = ec2.describe_addresses(Filters=[{"Name": "instance-id", "Values": [INSTANCE]}])["Addresses"]
eip_attached = len(eips) > 0
subnet = ec2.describe_subnets(SubnetIds=[inst["SubnetId"]])["Subnets"][0]
rt = ec2.describe_route_tables(Filters=[{"Name": "association.subnet-id", "Values": [inst["SubnetId"]]}])["RouteTables"]
if not rt:
    rt = ec2.describe_route_tables(Filters=[{"Name": "vpc-id", "Values": [inst["VpcId"]]}, {"Name": "association.main", "Values": ["true"]}])["RouteTables"]
default_routes = [r for t in rt for r in t["Routes"] if r.get("DestinationCidrBlock") == "0.0.0.0/0"]
egress_via = "igw" if any(str(r.get("GatewayId", "")).startswith("igw-") for r in default_routes) else "nat" if any(r.get("NatGatewayId") for r in default_routes) else "other/none"
has_public_ip = ip is not None

# target group health
tg_rows = []
for tg in elb.describe_target_groups()["TargetGroups"]:
    for th in elb.describe_target_health(TargetGroupArn=tg["TargetGroupArn"])["TargetHealthDescriptions"]:
        if th["Target"]["Id"] == INSTANCE:
            tg_rows.append({"target_group": tg["TargetGroupName"], "state": th["TargetHealth"]["State"], "port": th["Target"].get("Port")})

# host reads over SSM
cmds = ["echo BEGIN", "date -u +%FT%TZ", "echo MARKER=$(cat /opt/opal-gateway/.deployed_commit)", "echo HEALTH=$(curl -s -o /dev/null -m 10 -w '%{http_code}' http://127.0.0.1:8080/health)",
        "systemctl show opal-gateway -p NRestarts -p MemoryHigh -p MemoryMax -p MemoryCurrent -p ActiveState -p MainPID", "echo MEMTOTAL_MB=$(awk '/MemTotal/ {printf \"%d\", $2/1024}' /proc/meminfo)",
        "echo CGMAX=$(cat /sys/fs/cgroup/system.slice/opal-gateway.service/memory.max)", "echo CGHIGH=$(cat /sys/fs/cgroup/system.slice/opal-gateway.service/memory.high)", "echo END"]
cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": cmds}, TimeoutSeconds=120)["Command"]["CommandId"]
for _ in range(40):
    time.sleep(3)
    try:
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
    except Exception:
        continue
    if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
        break
kv = dict(ln.split("=", 1) for ln in inv["StandardOutputContent"].splitlines() if "=" in ln)

# public-IP residual: what in Opal's own estate names the gateway's public egress address (counts and surface names only)
surfaces = {"aws_security_group_rules": [], "aws_waf_ip_sets": [], "repo_files": []}
if has_public_ip:
    cidr = ip + "/32"
    for sg in ec2.describe_security_groups(Filters=[{"Name": "ip-permission.cidr", "Values": [cidr]}])["SecurityGroups"] + ec2.describe_security_groups(Filters=[{"Name": "egress.ip-permission.cidr", "Values": [cidr]}])["SecurityGroups"]:
        if sg["GroupName"] not in surfaces["aws_security_group_rules"]:
            surfaces["aws_security_group_rules"].append(sg["GroupName"])
    for scope, rg in (("REGIONAL", REGION), ("CLOUDFRONT", "us-east-1")):
        try:
            w = boto3.client("wafv2", region_name=rg)
            for s in w.list_ip_sets(Scope=scope).get("IPSets", []):
                if cidr in w.get_ip_set(Name=s["Name"], Scope=scope, Id=s["Id"])["IPSet"]["Addresses"]:
                    surfaces["aws_waf_ip_sets"].append(s["Name"])
        except Exception as exc:  # noqa: BLE001
            surfaces.setdefault("waf_read_errors", []).append(type(exc).__name__)
    p = subprocess.run(["bash", "comp-find", "--files", "--all", re.escape(ip)], capture_output=True, text=True)
    out = p.stdout.replace("\r", "")
    files = sorted({ln.strip().split()[-1] for ln in out.splitlines() if ln.strip() and "/" in ln and ip not in ln and not ln.startswith(("comp-find", "DENOM", "WITHIN"))})
    files = [re.sub(r"\d{1,3}(?:\.\d{1,3}){3}", "<gateway public IPv4>", f) for f in files if ("/" in f or "." in f) and not f.isalpha()]
    surfaces["repo_files"] = sorted(set(files))
    surfaces["repo_search_tail"] = [ln for ln in out.splitlines() if "hit" in ln.lower() or "file(s)" in ln.lower() or "denominator" in ln.lower()][-3:]
    surfaces["repo_search_rc"] = p.returncode
names = surfaces["aws_security_group_rules"] + surfaces["aws_waf_ip_sets"] + surfaces["repo_files"]
before = {
    "read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "instance_id": INSTANCE, "instance_type": inst["InstanceType"], "state": inst["State"]["Name"], "az": inst["Placement"]["AvailabilityZone"],
    "eip_attached": eip_attached, "has_public_ipv4_now": has_public_ip, "subnet_auto_assigns_public_ip": bool(subnet.get("MapPublicIpOnLaunch")), "egress_route": egress_via,
    "public_ip_changes_on_stop_start": bool(has_public_ip and not eip_attached),
    "public_ip_basis": ("the instance holds an auto-assigned public IPv4 and no Elastic IP is attached: it is RELEASED on stop and a new one is assigned on start" if has_public_ip and not eip_attached
                        else "an Elastic IP is attached: the address survives stop/start" if eip_attached else "the instance has no public IPv4; egress goes via %s" % egress_via),
    "target_health": tg_rows, "nrestarts": int(kv.get("NRestarts", "-1")), "unit_memory_high": kv.get("MemoryHigh"), "unit_memory_max": kv.get("MemoryMax"), "unit_memory_current": kv.get("MemoryCurrent"),
    "cgroup_memory_max": kv.get("CGMAX"), "cgroup_memory_high": kv.get("CGHIGH"), "active_state": kv.get("ActiveState"), "memory_total_mb": int(kv.get("MEMTOTAL_MB", "0")), "live_ref": kv.get("MARKER"), "health_status": kv.get("HEALTH"),
    "public_ip_surfaces": {"count": len(names), "names": names, "aws_security_group_rules": surfaces["aws_security_group_rules"], "aws_waf_ip_sets": surfaces["aws_waf_ip_sets"], "repo_files": surfaces["repo_files"],
                           "repo_search": surfaces.get("repo_search_tail"), "vendor_side_allowlists": "NOT CLAIMED: a vendor that admits only a listed source address cannot be read from here"},
    "ssm_command_id": cid,
}
io.open(W + "RZ2_BEFORE.json", "w", encoding="utf-8", newline="\n").write(json.dumps(before, indent=1) + "\n")
print(json.dumps({k: v for k, v in before.items() if k not in ("ssm_command_id",)}, indent=1)[:3500])
