"""The POSITIVE arm for NFRA_TRNSPT (laptop order 103564): one admitted message's PDF bytes land through the public
/hx/mail route with a hash. Prints status, byte count, the route's sha256 and the sha256 recomputed from the bytes;
never the bytes, the bearer or any body. Writes the bytes nowhere.

usage: python _pos_arm.py <route_names.json> <message_id> <attachment_id>
"""
import base64
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request

import boto3

BASE = "https://mcp.opalinvest.dev"
doc = json.load(open(sys.argv[1], encoding="utf-8"))
mid, aid = sys.argv[2], sys.argv[3]
sm = boto3.client("secretsmanager", region_name=os.environ.get("AWS_REGION", "us-east-1"))
bearer = sm.get_secret_value(SecretId=doc["mail"]["secret_name"])["SecretString"].strip()
path = doc["mail"]["probes"]["attachment"].format(prefix=doc["mail"]["prefix"], message_id=mid, attachment_id=aid)
req = urllib.request.Request(BASE + path, headers={"Authorization": "Bearer " + bearer})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        st, body = r.status, json.loads(r.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    st, body = e.code, {}
raw = base64.b64decode(body.get("content_base64", "") or b"")
own = hashlib.sha256(raw).hexdigest() if raw else None
print("status %s; content_returned %s; content_type %s; byte_count %s; decoded bytes %d" % (
    st, body.get("content_returned"), body.get("contentType") or body.get("content_type"), body.get("byte_count"),
    len(raw)))
print("route sha256 %s" % body.get("sha256"))
print("recomputed sha256 %s" % own)
print("magic %s" % (raw[:5] == b"%PDF-"))
ok = st == 200 and body.get("content_returned") is True and own == body.get("sha256") and raw[:5] == b"%PDF-" and \
    len(raw) == body.get("byte_count")
print("POSITIVE ARM %s" % ("PASS" if ok else "FAIL"))
