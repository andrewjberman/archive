#!/usr/bin/env python
"""OG-ev-1: upload ev1_answer_bodies.py to S3 (Rule 12), run it ONCE on the instance, decode the compressed block and write
W/ANSWER_BODIES.json plus W/ev1_meta.json. usage: python ev1_final_run.py   (from the repository root)"""
from __future__ import annotations

import base64
import datetime as dt
import io
import json
import sys
import time
import zlib

import boto3

INSTANCE = "i-07dccb1615503ac99"
BUCKET = "opal-313476888478-lambda-artifacts"
KEY = "ec2/opal-gateway/ev1_answer_bodies.py"
W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/"

body = io.open(W + "ev1_answer_bodies.py", "rb").read()
boto3.client("s3").put_object(Bucket=BUCKET, Key=KEY, Body=body)
print("uploaded s3://%s/%s (%d bytes)" % (BUCKET, KEY, len(body)))
cmd = ("cd /opt/opal-gateway && rm -f /tmp/ev1_answer_bodies.py && aws s3 cp s3://%s/%s /tmp/ev1_answer_bodies.py --region us-east-1 >/dev/null && "
       "/opt/opal-gateway/.venv/bin/python /tmp/ev1_answer_bodies.py" % (BUCKET, KEY))
ssm = boto3.client("ssm")
cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]},
                       TimeoutSeconds=900)["Command"]["CommandId"]
print("ssm command %s" % cid)
inv = None
for _ in range(150):
    time.sleep(4)
    inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
    if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
        break
so, se = inv.get("StandardOutputContent", ""), inv.get("StandardErrorContent", "")
print("status=%s rc=%s stdout_chars=%d" % (inv["Status"], inv.get("ResponseCode"), len(so)))
io.open(W + "ev1_run.raw.txt", "w", encoding="utf-8", newline="\n").write("status=%s\ncommand_id=%s\n--- STDOUT (sizes only kept below) ---\nchars=%d\n--- STDERR (head) ---\n%s\n"
                                                                              % (inv["Status"], cid, len(so), se[:600]))
if "EV1_BODIES_B64" not in so or "EV1_META_JSON" not in so:
    print("NO markers; stdout head:", so[:400])
    sys.exit(2)
b64 = so.split("EV1_BODIES_B64", 1)[1].split("EV1_META_JSON", 1)[0].strip()
meta = json.loads(so.split("EV1_META_JSON", 1)[1].strip())
if "fatal" in meta or not b64:
    print("host harness failed:", json.dumps(meta)[:1500])
    sys.exit(3)
releases = json.loads(zlib.decompress(base64.b64decode(b64)).decode("utf-8"))
try:
    live = boto3.client("s3").head_object(Bucket=BUCKET, Key="ec2/opal-gateway/opal-gateway-latest.tar.gz")["Metadata"].get("git-ref", "")
except Exception as exc:
    live = "unread: %s" % type(exc).__name__
doc = {"read_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "live_commit": live, "releases": releases}
io.open(W + "ANSWER_BODIES.json", "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
io.open(W + "ev1_meta.json", "w", encoding="utf-8", newline="\n").write(json.dumps(meta, indent=1) + "\n")
print("WROTE ANSWER_BODIES.json: %s" % {k: len(v) for k, v in releases.items()})
print("limit_bytes_used=%s b64_chars=%s blocked=%s" % (meta.get("limit_bytes_used"), meta.get("b64_chars"), meta.get("blocked")))
