#!/usr/bin/env python
"""OG-ap-42 Phase B: the served read, UNARMED ONLY. NO ARMING and NO SSM WRITE of any kind: this script only DESCRIBES and GETS the lease parameter (to show it absent before and after) and asks the host client
(ap40_probe_host.py, uploaded here) for the service's state and for calls to the listener of the RUNNING service, each of which must answer 403 probe_not_armed. Counts, status words and booleans only.
  python ap42_unarmed_run.py <out.json>      (repository root)"""
from __future__ import annotations

import io
import json
import os
import sys
import time

import boto3

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ap38_measure as m  # noqa: E402

LEASE_PARAM = "/opal-gateway/probe/lease"
OUT = sys.argv[1]
ssm = boto3.client("ssm", region_name="us-east-1")
s3 = boto3.client("s3", region_name="us-east-1")


def stamp():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def run_ssm(cmd, timeout=600):
    cid = ssm.send_command(InstanceIds=[m.INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=timeout)["Command"]["CommandId"]
    inv = None
    for _ in range(timeout // 3):
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=m.INSTANCE)
        except Exception:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    return inv


def host(args):
    inv = run_ssm("cd /opt/opal-gateway && %s /tmp/ap40_probe_host.py %s" % (m.PY, args))
    so = inv.get("StandardOutputContent", "")
    if "AP40_PROBE_JSON" not in so:
        raise RuntimeError("no marker from the host (%s): %s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    return json.loads(so.split("AP40_PROBE_JSON", 1)[1].strip())


def param_state():
    names = [p["Name"] for p in ssm.describe_parameters(ParameterFilters=[{"Key": "Name", "Option": "BeginsWith", "Values": ["/opal-gateway/probe/"]}])["Parameters"]]
    try:
        ssm.get_parameter(Name=LEASE_PARAM)
        got = True
    except ssm.exceptions.ParameterNotFound:
        got = False
    return {"parameters_under_probe_prefix": len(names), "get_parameter_found": got, "absent": (not names) and (not got), "read_at": stamp()}


def main():
    raw = {"started": stamp(), "puts_made_by_this_script": 0}
    here = os.path.dirname(os.path.abspath(__file__))
    for n in ("ap40_probe_host.py", "ap38_measure.py", "ap38_guard.py"):
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/" + n, Body=io.open(os.path.join(here, n), "rb").read())
    pulls = " && ".join("aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (m.BUCKET, n, n) for n in ("ap40_probe_host.py", "ap38_measure.py", "ap38_guard.py"))
    if "PULLED" not in run_ssm("cd /opt/opal-gateway && rm -f /tmp/ap40_probe_host.py && %s && echo PULLED" % pulls, 300).get("StandardOutputContent", ""):
        raise RuntimeError("the host scripts were not pulled")
    raw["lease_before"] = param_state()
    raw["state_before"] = host("state")
    pid0 = raw["state_before"]["pid"]
    calls = []
    for tool in ("etfs_compare_peers", "client_get_transactions", "client_get_fees"):
        r = host("call %s" % tool)
        calls.append({"tool": tool, "status": r["status"], "error": r["error"], "pid": r["pid"], "nrestarts": r["nrestarts"], "at": stamp()})
    raw["calls"] = calls
    raw["lease_after"] = param_state()
    raw["state_after"] = host("state")
    raw["pid_stable"] = raw["state_after"]["pid"] == pid0
    raw["finished"] = stamp()
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(raw, indent=1) + "\n")
    print("DONE", json.dumps({"calls": [(c["tool"], c["status"], c["error"]) for c in calls], "lease_absent_before": raw["lease_before"]["absent"], "lease_absent_after": raw["lease_after"]["absent"], "pid_stable": raw["pid_stable"]}))


if __name__ == "__main__":
    main()
