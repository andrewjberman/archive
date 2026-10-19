#!/usr/bin/env python
"""OG-ap-50 Phase B steps 5 and 6: the route on the RUNNING service, read with a LOCAL request (the service port on 127.0.0.1, no load balancer, NO identity header), plus the two controls. READ ONLY: three GETs and a
lease-parameter DESCRIBE; no SSM parameter is written, nothing is armed. Status words and codes only (no body is kept).
  python ap50_route.py <before|after> <out.json>      (repository root)
Requests (service port 8080 on the host, as the uvicorn startup line prints): GET /api/admin/gateway/families, GET /api/admin/whoami (the control that is always mounted), GET /api/admin/gateway/no-such-route."""
from __future__ import annotations

import io
import json
import sys
import time

import boto3

INSTANCE = "i-07dccb1615503ac99"
PORT = 8080
PATHS = [("families", "/api/admin/gateway/families"), ("whoami", "/api/admin/whoami"), ("missing", "/api/admin/gateway/no-such-route")]


def main(when, outp):
    ssm = boto3.client("ssm", region_name="us-east-1")
    cmds = ["echo BEGIN", "date -u +%FT%TZ", "systemctl show opal-gateway -p MainPID -p NRestarts"]
    for name, path in PATHS:
        cmds.append("echo %s=$(curl -s -o /dev/null -m 10 -w '%%{http_code}' http://127.0.0.1:%d%s)" % (name.upper(), PORT, path))
    cmds.append("echo END")
    cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": cmds}, TimeoutSeconds=120)["Command"]["CommandId"]
    inv = None
    for _ in range(40):
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except Exception:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    kv = dict(ln.split("=", 1) for ln in so.splitlines() if "=" in ln)
    lease = ssm.describe_parameters(ParameterFilters=[{"Key": "Name", "Option": "BeginsWith", "Values": ["/opal-gateway/probe/"]}])["Parameters"]
    out = {"when": when, "ssm_command_id": cid, "ssm_status": inv["Status"], "read_at": [ln for ln in so.splitlines() if ln[:2] == "20"][:1],
           "probe": "a local request from the host itself to 127.0.0.1:%d (the service port, not the load balancer), no identity header, curl -s -w http_code; no body kept" % PORT,
           "families_status": int(kv.get("FAMILIES", "0") or 0), "whoami_status": int(kv.get("WHOAMI", "0") or 0), "missing_status": int(kv.get("MISSING", "0") or 0),
           "service_pid": kv.get("MainPID"), "nrestarts": kv.get("NRestarts"), "lease_parameters_under_probe_prefix": len(lease), "lease_parameter_absent": "/opal-gateway/probe/lease" not in [x["Name"] for x in lease]}
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
