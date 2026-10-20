#!/usr/bin/env python
"""OG-rl-17 Phase B read-back record (COO ferry 20261020T181500Z, the CTO's advisor-tables ruling, item 1): the files of app/ (and app/refs/DATA_CATALOG.yaml, which lies under app/refs/) under /opt/opal-gateway that DIFFER from trunk HEAD at the read time,
by path and short sha only. READ ONLY (an md5 walk over SSM and git blobs). Counts, paths and hashes: no content. A record, not a trigger.
HEAD is the repository checkout's current HEAD (the branch box/sitez at the read time); the files outside batch16's take list that trunk carries ahead of the host are the ones named here.
usage: python rl17_deployed_vs_head.py <out.json>   (repository root)"""
from __future__ import annotations

import hashlib
import io
import json
import subprocess
import sys
import time

import boto3

OUT = sys.argv[1]
INSTANCE = "i-07dccb1615503ac99"
G = "infra/aws/ec2/opal-gateway/"
CMD = "cd /opt/opal-gateway && find app -type f ! -name '*.pyc' ! -path '*/__pycache__/*' -print0 | sort -z | xargs -0 md5sum"


def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True)


head = git("rev-parse", "HEAD").stdout.decode().strip()
ssm = boto3.client("ssm", region_name="us-east-1")
cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [CMD]}, TimeoutSeconds=180)["Command"]["CommandId"]
inv = None
for _ in range(60):
    time.sleep(3)
    try:
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
    except Exception:
        continue
    if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
        break
host = {}
for line in inv["StandardOutputContent"].splitlines():
    if "  " in line:
        h, p = line.split("  ", 1)
        host[p.strip()] = h.strip()
tree = git("ls-tree", "-r", "--name-only", head, "--", G + "app/").stdout.decode().split("\n")
head_paths = {p[len(G):] for p in tree if p.strip() and "/__pycache__/" not in p and not p.endswith(".pyc")}
differ, equal, crlf_only, host_only = [], 0, 0, []
for p, h in sorted(host.items()):
    if p not in head_paths:
        host_only.append({"path": p, "host_md5_16": h[:16]})
        continue
    blob = git("show", "%s:%s%s" % (head, G, p)).stdout
    if hashlib.md5(blob).hexdigest() == h:
        equal += 1
    elif hashlib.md5(blob.replace(b"\r\n", b"\n")).hexdigest() == h or hashlib.md5(blob.replace(b"\n", b"\r\n")).hexdigest() == h:
        crlf_only += 1
    else:
        differ.append({"path": p, "host_md5_16": h[:16], "head_md5_16": hashlib.md5(blob).hexdigest()[:16]})
head_only = sorted(head_paths - set(host))
rec = {"read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "head": head, "ssm_command_id": cid, "ssm_status": inv["Status"],
       "denominator": {"host_files_under_app": len(host), "head_files_under_app": len(head_paths)}, "equal": equal, "equal_after_line_ending_only": crlf_only, "differ_count": len(differ), "differ": differ,
       "host_only_count": len(host_only), "host_only": host_only, "head_only_count": len(head_only), "head_only_paths": head_only[:60],
       "reading": "A file that differs is a trunk change the host has not been given (outside batch16's take list) or a host file edited in place; this is a record, not a trigger."}
io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1) + "\n")
print(json.dumps({k: rec[k] for k in ("head", "denominator", "equal", "equal_after_line_ending_only", "differ_count", "host_only_count", "head_only_count")}))
