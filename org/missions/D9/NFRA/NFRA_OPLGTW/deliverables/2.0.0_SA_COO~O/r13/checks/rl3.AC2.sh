#!/usr/bin/env bash
# OPLGTW OG-rl-3 AC2 (row Z-W15-S23 on the SERVED gateway): the newest read_meeting_transcript audit record written
# AFTER the manifest's deployed_at carries an integer `bytes` > 0 and a `principal` of the form <tid>/<oid>, beside the
# email `user`. The live read is the ISSUER's (signed in as Andrew). Prints booleans and counts only.
# Reads S3 IN MEMORY via boto3 listing keys from the deployed_at hour: the audit keys carry ':' and a Windows
# `aws s3 cp --recursive` silently drops every such key (2769 objects -> 16 copied, measured at the cut).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
at=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']['deployed_at'])" | tr -d '\r')
python - "$at" <<'EOF'
import json, re, sys
from datetime import datetime, timedelta, timezone
import boto3
at = sys.argv[1]
t0 = datetime.strptime(at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
s3 = boto3.client("s3", region_name="us-east-1")
pg = s3.get_paginator("list_objects_v2")
keys, d = [], t0.date()
while d <= datetime.now(timezone.utc).date():
    pre = "audit/dt=%s/" % d.isoformat()
    for page in pg.paginate(Bucket="opal-mcp-audit", Prefix=pre):
        for o in page.get("Contents", []):
            k = o["Key"]; stamp = k[len(pre):len(pre) + 19]
            if stamp >= t0.strftime("%Y-%m-%dT%H:%M:%S"):
                keys.append(k)
    d += timedelta(days=1)
recs = []
for k in keys:
    for line in s3.get_object(Bucket="opal-mcp-audit", Key=k)["Body"].read().decode("utf-8").splitlines():
        try: recs.append(json.loads(line))
        except ValueError: pass
pick = sorted([r for r in recs if isinstance(r, dict) and r.get("tool") == "read_meeting_transcript"
               and r.get("outcome") == "ok"], key=lambda r: str(r.get("ts", "")))
print("audit keys after deployed_at %s: %d; records %d; read_meeting_transcript ok: %d" % (at, len(keys), len(recs), len(pick)))
if not pick:
    print("RESULT: FAIL"); sys.exit(1)
r = pick[-1]
b = r.get("bytes"); p = str(r.get("principal", ""))
ok_b = isinstance(b, int) and not isinstance(b, bool) and b > 0
ok_p = re.fullmatch(r"[0-9a-f-]{36}/[0-9a-f-]{36}", p) is not None
print("newest record: bytes integer > 0 %s; principal is a <tid>/<oid> pair %s; user present %s" % (ok_b, ok_p, bool(r.get("user"))))
print("RESULT: PASS" if ok_b and ok_p else "RESULT: FAIL"); sys.exit(0 if ok_b and ok_p else 1)
EOF
