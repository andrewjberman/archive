#!/usr/bin/env python
"""OG-rl-17 Phase B step 6: the in-flight guard read from the DEPLOYED tree on the host (/opt/opal-gateway), not from the repo. READ ONLY; no gateway code is run (the files are READ as text and the constants parsed),
so no hard guard is needed. Records: whether app/inflight_guard.py exists, its MAX_INFLIGHT and QUEUE_WAIT_S, whether app/tools.py carries the `async with inflight_guard.guard.slot(` hook and the Busy handler, and the file md5 against the release blob.
usage: python rl17_inflight.py <out.json> <release_sha>   (repository root)"""
from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import sys
import time

import boto3

OUT, REL = sys.argv[1:3]
INSTANCE = "i-07dccb1615503ac99"
G = "infra/aws/ec2/opal-gateway/"
CMD = ("echo ---GUARD; cat /opt/opal-gateway/app/inflight_guard.py; echo ---TOOLS; grep -n 'inflight_guard' /opt/opal-gateway/app/tools.py; echo ---MD5; md5sum /opt/opal-gateway/app/inflight_guard.py /opt/opal-gateway/app/tools.py | cut -d' ' -f1; echo ---END")


def blob(path):
    return subprocess.run(["git", "show", "%s:%s" % (REL, G + path)], capture_output=True).stdout


ssm = boto3.client("ssm", region_name="us-east-1")
cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [CMD]}, TimeoutSeconds=120)["Command"]["CommandId"]
inv = None
for _ in range(40):
    time.sleep(3)
    try:
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
    except Exception:
        continue
    if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
        break
so = inv["StandardOutputContent"]
sec = {}
for blk in so.split("---")[1:]:
    name, _, rest = blk.partition("\n")
    sec[name.strip()] = rest
guard_txt, tools_txt, md5s = sec.get("GUARD", ""), sec.get("TOOLS", ""), [x.strip() for x in sec.get("MD5", "").split() if x.strip()]
mx = re.search(r"^MAX_INFLIGHT\s*=\s*(\d+)", guard_txt, re.M)
qw = re.search(r"^QUEUE_WAIT_S\s*=\s*([0-9.]+)", guard_txt, re.M)
rec = {"read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "ssm_command_id": cid, "ssm_status": inv["Status"],
       "guard_in_deployed_tree": "class InflightGuard" in guard_txt and "guard = InflightGuard()" in guard_txt, "limit": int(mx.group(1)) if mx else None, "wait_s": float(qw.group(1)) if qw else None,
       "deployed_call_tool_hook": "inflight_guard.guard.slot(" in tools_txt and "inflight_guard.Busy" in tools_txt,
       "inflight_guard_md5_equals_release_blob": bool(md5s) and md5s[0] == hashlib.md5(blob("app/inflight_guard.py")).hexdigest(),
       "tools_py_md5_equals_release_blob": len(md5s) > 1 and md5s[1] == hashlib.md5(blob("app/tools.py")).hexdigest(),
       "source": "ssm cat of /opt/opal-gateway/app/inflight_guard.py and grep of app/tools.py; nothing executed"}
io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1) + "\n")
print(json.dumps(rec))
