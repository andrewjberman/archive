#!/usr/bin/env python
"""OG-rz-2 Phase B step 2 (COO H2, H3): after the apply, wait until the host reads `t4g.large` and `running`, the SSM agent is online, the service answers /health 200 locally, the marker is UNCHANGED, host memory total is
at least 7,000 MB, the target group is healthy and the Elastic IP is still associated. Polls every 10 s. READ ONLY. Exit 0 when every condition holds; exit 1 at the timeout (default 600 s = H3's 10 minutes), printing what held.
usage: python rz2_pb_wait.py <out.json> [timeout_s=600]      Writes the state timeline and the post-resize facts; no address, ARN or account number."""
from __future__ import annotations

import io
import json
import sys
import time

import boto3

OUT = sys.argv[1]
TIMEOUT = int(sys.argv[2]) if len(sys.argv) > 2 else 600
INSTANCE, LIVE = "i-07dccb1615503ac99", "6d1b5dcb64b945deb98664c6ae078d8f1e8a6c5c"
ec2, elb, ssm = (boto3.client(n, region_name="us-east-1") for n in ("ec2", "elbv2", "ssm"))
CMDS = ["echo BEGIN", "date -u +%FT%TZ", "echo MARKER=$(cat /opt/opal-gateway/.deployed_commit)", "echo HEALTH=$(curl -s -o /dev/null -m 10 -w '%{http_code}' http://127.0.0.1:8080/health)",
        "systemctl show opal-gateway -p NRestarts -p MemoryHigh -p MemoryMax -p MemoryCurrent -p ActiveState -p MainPID", "echo MEMTOTAL_MB=$(awk '/MemTotal/ {printf \"%d\", $2/1024}' /proc/meminfo)",
        "echo UPTIME_S=$(cut -d. -f1 /proc/uptime)", "echo END"]


def host_facts():
    cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": CMDS}, TimeoutSeconds=60)["Command"]["CommandId"]
    for _ in range(20):
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except Exception:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            return dict(ln.split("=", 1) for ln in inv["StandardOutputContent"].splitlines() if "=" in ln), inv["Status"]
    return {}, "Timeout"


def snapshot():
    inst = ec2.describe_instances(InstanceIds=[INSTANCE])["Reservations"][0]["Instances"][0]
    state, itype = inst["State"]["Name"], inst["InstanceType"]
    ping = None
    if state == "running":
        info = ssm.describe_instance_information(Filters=[{"Key": "InstanceIds", "Values": [INSTANCE]}])["InstanceInformationList"]
        ping = info[0]["PingStatus"] if info else None
    return state, itype, ping


def evaluate():
    kv, status = host_facts()
    eip = ec2.describe_addresses(Filters=[{"Name": "instance-id", "Values": [INSTANCE]}])["Addresses"]
    th = [d["TargetHealth"]["State"] for t in elb.describe_target_groups()["TargetGroups"] if "gateway" in t["TargetGroupName"]
          for d in elb.describe_target_health(TargetGroupArn=t["TargetGroupArn"])["TargetHealthDescriptions"] if d["Target"]["Id"] == INSTANCE]
    facts = {"ssm_status": status, "marker": kv.get("MARKER"), "health": kv.get("HEALTH"), "memory_total_mb": int(kv.get("MEMTOTAL_MB", "0") or 0), "nrestarts": kv.get("NRestarts"), "unit_memory_high": kv.get("MemoryHigh"),
             "unit_memory_max": kv.get("MemoryMax"), "memory_current": kv.get("MemoryCurrent"), "active_state": kv.get("ActiveState"), "uptime_s": kv.get("UPTIME_S"), "target_health": th, "eip_associated": len(eip) == 1}
    checks = {"marker unchanged": facts["marker"] == LIVE, "health 200": facts["health"] == "200", "memory total >= 7000 MB": facts["memory_total_mb"] >= 7000, "target healthy": th == ["healthy"], "EIP associated": facts["eip_associated"]}
    facts["checks"] = checks
    return facts


def main():
    start, timeline, last, ok = time.time(), [], {}, False
    while time.time() - start < TIMEOUT and not ok:
        state, itype, ping = snapshot()
        entry = {"t": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "state": state, "type": itype, "ssm": ping}
        timeline.append(entry)
        print(entry)
        if state == "running" and itype == "t4g.large" and ping == "Online":
            last = evaluate()
            print(last["checks"])
            ok = all(last["checks"].values())
        if not ok:
            time.sleep(10)
    rec = {"waited_s": round(time.time() - start), "timeout_s": TIMEOUT, "all_conditions_hold": ok, "timeline": timeline, "post_resize": last}
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1) + "\n")
    print("RESIZE WAIT:", "ALL HOLD after %d s" % rec["waited_s"] if ok else "TIMEOUT or a condition does not hold: STOP (COO H3)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
