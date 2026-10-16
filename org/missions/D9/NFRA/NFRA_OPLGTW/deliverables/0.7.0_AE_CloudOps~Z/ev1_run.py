#!/usr/bin/env python
"""OG-ap-23 Phase B step 5: upload the served harness to S3, run it on the instance, keep the JSON.

Rule 12 shape: LOCAL -> S3 -> the instance PULLS -> execute. No code is written on the box and no
python is inlined in the SSM command text.

TRUNCATION IS A LOUD FAILURE HERE, not a silent partial: get_command_invocation caps
StandardOutputContent, so the harness's JSON is parsed, and a cap that cut it makes json.loads raise
rather than hand back a half record that reads like a result.
"""
from __future__ import annotations

import io
import json
import sys
import time

import boto3

INSTANCE = "i-07dccb1615503ac99"
BUCKET = "opal-313476888478-lambda-artifacts"
KEY = "ec2/opal-gateway/ev1_discover.py"
LOCAL = r"C:\Users\Opal Bloomberg\Desktop\ajb_workspace\org\missions\D9\NFRA\NFRA_OPLGTW\deliverables\0.7.0_AE_CloudOps~Z\ev1_discover.py"
OUT = sys.argv[1]
ARGS = " ".join(sys.argv[2:])

body = io.open(LOCAL, "rb").read()
boto3.client("s3").put_object(Bucket=BUCKET, Key=KEY, Body=body)
print("uploaded s3://%s/%s (%d bytes)" % (BUCKET, KEY, len(body)))

cmd = ("cd /opt/opal-gateway && rm -f /tmp/ev1_discover.py && "
       "aws s3 cp s3://%s/%s /tmp/ev1_discover.py --region us-east-1 >/dev/null && "
       "md5sum /tmp/ev1_discover.py && "
       "/opt/opal-gateway/.venv/bin/python /tmp/ev1_discover.py %s" % (BUCKET, KEY, ARGS))

ssm = boto3.client("ssm")
cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript",
                       Parameters={"commands": [cmd]}, TimeoutSeconds=600)["Command"]["CommandId"]
print("ssm command %s" % cid)
inv = None
for _ in range(100):
    time.sleep(4)
    inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
    if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
        break
print("status=%s rc=%s" % (inv["Status"], inv.get("ResponseCode")))
so = inv.get("StandardOutputContent", "")
se = inv.get("StandardErrorContent", "")
if se.strip():
    print("--- stderr (first 1200):")
    print(se[:1200])

io.open(OUT + ".raw.txt", "w", encoding="utf-8", newline="\n").write(
    "status=%s rc=%s\ncommand_id=%s\n--- STDOUT ---\n%s\n--- STDERR ---\n%s\n"
    % (inv["Status"], inv.get("ResponseCode"), cid, so, se))

MARK = "EV1_DISCOVER_JSON"
if MARK not in so:
    print("NO %s marker in the host output -- see %s.raw.txt" % (MARK, OUT))
    sys.exit(2)
host_md5 = so.split(MARK)[0].strip().splitlines()
blob = so.split(MARK, 1)[1].strip()
doc = json.loads(blob)                      # raises if the output was capped
if isinstance(doc, list):
    doc = {"log": doc}
doc["_ssm"] = {"command_id": cid, "status": inv["Status"], "response_code": inv.get("ResponseCode"),
               "harness_md5_on_host": host_md5[-1] if host_md5 else None,
               "stdout_chars": len(so)}
io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1, default=str) + "\n")
print("WROTE %s (%d chars of host stdout, JSON parsed whole)" % (OUT, len(so)))
b = doc.get("body", doc)
for k in sorted(b):
    v = b[k]
    if isinstance(v, (bool, int, float, str)) or v is None:
        print("  %-52s %s" % (k, json.dumps(v, default=str)[:150]))
