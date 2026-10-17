#!/usr/bin/env python
"""OG-ap-35 Phase B host read-back: the entitlement decision, made by the INSTALLED gateway code on the host, for her principal.
READ-ONLY. No call is made as her; the decision functions are called in-process with a Principal built from the store.
Her principal is found by pk hash (first 10 hex of sha256 of the pk), so no identifier travels or prints.
Prints/writes names, booleans, counts and hashes only.
usage: python ag1_hostread.py <out.json>   (laptop side; ships the host script by SSM, in the shape of ap32_workers.py)"""
import base64
import json
import sys
import time

import boto3

INSTANCE = "i-07dccb1615503ac99"
PK_HASH = "2c61471b14"
HOST = r'''
import hashlib, json, sys
sys.path.insert(0, "/opt/opal-gateway")
import boto3
import app.access_state as acs
import app.data_entitlement as de
from app.context import Principal
PK_HASH = "%s"
ddb = boto3.client("dynamodb", region_name="us-east-1")
items, tok = [], None
while True:
    kw = {"TableName": "gateway-access-state-table", "ConsistentRead": True}
    if tok:
        kw["ExclusiveStartKey"] = tok
    r = ddb.scan(**kw)
    items += r["Items"]
    tok = r.get("LastEvaluatedKey")
    if not tok:
        break
hit = [i["pk"]["S"] for i in items if i.get("record_type", {}).get("S") == "principal_profile" and hashlib.sha256(i["pk"]["S"].encode()).hexdigest()[:10] == PK_HASH]
out = {"items_scanned": len(items), "profiles_matching_pk_hash": len(hit)}
if len(hit) == 1:
    _, tid, oid = hit[0].split("#")
    acc = de.current_access(Principal(tid, oid), acs.AccessState())
    ops = sorted(acc.grant.scope.operations) if acc.grant is not None else None
    dl = de.decide("schwab_prepare_download", acc, None)
    out.update({"profile_revision": acc.profile.revision, "grant_revision": acc.profile.grant_revision, "operations": ops,
                "allowed_tools_count": len(acc.tools),
                "schwab_prepare_download_in_allowed_tools": "schwab_prepare_download" in acc.tools,
                "download_refused": dl is not None, "download_denial_code": (dl or {}).get("error") or (dl or {}).get("code") or (dl or {}).get("reason"),
                "list_answers": {t: de.decide(t, acc, None) is None for t in ("schwab_list_files", "schwab_describe_dataset", "schwab_query")}})
print("BEGIN"); print(json.dumps(out, default=str)); print("END")
''' % PK_HASH

b64 = base64.b64encode(HOST.encode()).decode()
cmd = "echo %s | base64 -d > /tmp/ag1_hostread.py && /opt/opal-gateway/.venv/bin/python /tmp/ag1_hostread.py; rm -f /tmp/ag1_hostread.py" % b64
ssm = boto3.client("ssm")
cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]})["Command"]["CommandId"]
for _ in range(40):
    time.sleep(3)
    try:
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
    except ssm.exceptions.InvocationDoesNotExist:
        continue
    if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
        break
text = inv["StandardOutputContent"]
body = text.split("BEGIN", 1)[1].split("END", 1)[0].strip() if "BEGIN" in text else ""
res = {"ssm_command_id": cid, "status": inv["Status"], "host": json.loads(body) if body else None}
if not body:
    res["stderr_tail"] = inv["StandardErrorContent"][-400:]
json.dump(res, open(sys.argv[1], "w"), indent=1)
print(json.dumps(res, indent=1))
