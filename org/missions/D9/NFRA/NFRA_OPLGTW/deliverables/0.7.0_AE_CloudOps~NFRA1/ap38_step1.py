#!/usr/bin/env python
"""OG-ap-38 Phase A step 1: the host's BEFORE state, READ-ONLY, in ONE SSM run (Rule 12: local -> S3 -> the instance pulls -> execute).
The tools/list read executes gateway code, so it runs through the hard guard (W/ap38_guard.py: oom_score_adj 1000, RLIMIT_AS 1400 MB, wall limit 120 s).
Reads: the unit's limits and NRestarts, the marker, the cgroup version and controllers, host memory, the uvicorn process count, the .env key count and whether MUSE_CLIENT_ID is a key
(counts only, never a value), tools/list.
usage: python ap38_step1.py <out.json>   (repository root of the worktree that holds this file)"""
from __future__ import annotations

import io
import json
import os
import re
import time

import boto3

INSTANCE = "i-07dccb1615503ac99"
BUCKET = "opal-313476888478-lambda-artifacts"
HERE = os.path.dirname(os.path.abspath(__file__))
PY = "/opt/opal-gateway/.venv/bin/python"


def main(outp: str) -> None:
    s3 = boto3.client("s3")
    for name, key in (("ap38_guard.py", "ec2/opal-gateway/ap38_guard.py"), ("ap36_toolslist.py", "ec2/opal-gateway/ap36_toolslist.py")):
        s3.put_object(Bucket=BUCKET, Key=key, Body=io.open(os.path.join(HERE, name), "rb").read())
    cmd = (
        "cd /opt/opal-gateway && rm -f /tmp/ap38_guard.py /tmp/ap36_toolslist.py && "
        "aws s3 cp s3://%(b)s/ec2/opal-gateway/ap38_guard.py /tmp/ap38_guard.py --region us-east-1 >/dev/null && "
        "aws s3 cp s3://%(b)s/ec2/opal-gateway/ap36_toolslist.py /tmp/ap36_toolslist.py --region us-east-1 >/dev/null && "
        "echo ---UNIT && systemctl show opal-gateway -p MemoryMax -p MemoryHigh -p OOMScoreAdjust -p NRestarts -p MainPID -p ActiveState && "
        "echo ---MARKER && (test -e /opt/opal-gateway/.deployed_commit && echo PRESENT=$(cat /opt/opal-gateway/.deployed_commit) || echo ABSENT) && "
        "echo ---CGROUP && stat -fc %%T /sys/fs/cgroup && cat /sys/fs/cgroup/cgroup.controllers && "
        "echo ---MEM && free -m | sed -n 2p && nproc && "
        "echo ---PROCS && (ps -eo pid,rss,comm,args | grep -E 'uvicorn' | grep -v grep | awk '{print $1, $2, $3}') && "
        "echo ---ENV && grep -cE '^[A-Za-z_][A-Za-z0-9_]*=' /opt/opal-gateway/.env && (grep -c '^MUSE_CLIENT_ID=' /opt/opal-gateway/.env || true) && "
        "echo ---TOOLS && %(py)s /tmp/ap38_guard.py 120 /tmp/ap36_toolslist.py --host; echo ---END" % {"b": BUCKET, "py": PY})
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=300)["Command"]["CommandId"]
    inv = None
    for _ in range(80):
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except Exception:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    sec = {m.group(1): m.group(2).strip() for m in re.finditer(r"---([A-Z]+)\n(.*?)(?=\n---[A-Z]+\n|\Z)", so, re.S)}
    unit = dict(ln.split("=", 1) for ln in sec.get("UNIT", "").splitlines() if "=" in ln)
    cg = sec.get("CGROUP", "").splitlines()
    mem = sec.get("MEM", "").splitlines()
    procs = [ln for ln in sec.get("PROCS", "").splitlines() if ln.strip()]
    env = sec.get("ENV", "").splitlines()
    tools = {}
    if "AP28_JSON" in sec.get("TOOLS", ""):
        tools = json.loads(sec["TOOLS"].split("AP28_JSON", 1)[1].strip().splitlines()[0])
    doc = {"ssm_command_id": cid, "ssm_status": inv["Status"], "read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "guard_for_tools_list": "oom_score_adj_1000_rlimit_as_1400mb",
           "unit": unit, "marker": sec.get("MARKER", ""), "cgroup_fs": cg[0] if cg else None, "cgroup_controllers_has_memory": bool(cg[1:] and "memory" in cg[1].split()),
           "mem_line": mem[0] if mem else None, "nproc": mem[1] if len(mem) > 1 else None, "uvicorn_process_lines": len(procs),
           "env_key_count": int(env[0]) if env and env[0].isdigit() else None, "muse_client_id_is_a_key": bool(len(env) > 1 and env[1].strip() not in ("", "0")),
           "tools": tools}
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1))


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
