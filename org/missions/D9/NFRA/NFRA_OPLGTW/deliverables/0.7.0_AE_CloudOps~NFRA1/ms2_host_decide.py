#!/usr/bin/env python
"""OG-ms-2 Phase B: the DEPLOYED tree's own answers (order amendment A1), READ-ONLY, one script that is both the host program (--host, on the gateway host under
/opt/opal-gateway/.venv/bin/python, always through the hard guard W/ap38_guard.py) and its runner (default: uploads itself, runs once over SSM, Rule 12).
Host side, modes:
  pre   the marker, whether the deployed `app.data_entitlement.MASTERS` lists the master, and whether the host role can read Alyssa's live profile and grant (revisions only)
  post  decide() and check_scope() of the DEPLOYED code on her LIVE grant (a strongly consistent read of the store from the host)
Counts, booleans, revisions and the marker only: no identifier is printed.
usage: python ms2_host_decide.py <pre|post> <out.json>   (repository root)"""
from __future__ import annotations

import io
import json
import os
import sys
import time
import traceback

ROOT = "/opt/opal-gateway"
NEW = "08403355"
TOOLS4 = ("schwab_get_access", "schwab_list_files", "schwab_describe_dataset", "schwab_query")
BUCKET, INSTANCE, PY = "opal-313476888478-lambda-artifacts", "i-07dccb1615503ac99", ROOT + "/.venv/bin/python"


def host(mode):
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    os.environ.setdefault("MOCK_GRAPH", "1")
    import boto3
    from boto3.dynamodb.types import TypeDeserializer
    from app import access_state as acs
    from app import data_entitlement as de
    marker = io.open(ROOT + "/.deployed_commit", encoding="utf-8").read().strip()
    out = {"tree": "deployed", "code_sha": marker, "master_in_deployed_MASTERS": NEW in de.MASTERS, "masters_count": len(de.MASTERS)}
    items, kw, td = [], {"TableName": "gateway-access-state-table", "ConsistentRead": True, "FilterExpression": "begins_with(pk,:p)", "ExpressionAttributeValues": {":p": {"S": "POLICY#"}}}, TypeDeserializer()
    client = boto3.client("dynamodb", region_name="us-east-1")
    resp = {"LastEvaluatedKey": True}
    while "LastEvaluatedKey" in resp:
        resp = client.scan(**kw)
        items += [{k: td.deserialize(v) for k, v in it.items()} for it in resp["Items"]]
        if "LastEvaluatedKey" in resp:
            kw["ExclusiveStartKey"] = resp["LastEvaluatedKey"]
    cands = [i for i in items if i.get("record_type") == "principal_profile" and i.get("status") == "active" and str(i.get("email", "")).lower().split("@")[0] == "alyssa"]
    out["policy_items_read"], out["alyssa_active_profiles"] = len(items), len(cands)
    if len(cands) != 1:
        out["fatal"] = "alyssa resolves to %d active profiles" % len(cands)
        return out
    p = cands[0]
    store = acs.AccessState(client=client)
    profile = de.parse_profile(store.get(de.profile_key(p["tid"], p["oid"])), p["tid"], p["oid"])
    grant = de.parse_grant(store.get(de.grant_key(p["tid"], p["oid"], profile.grant_revision)), p["tid"], p["oid"], profile.grant_revision)
    out.update({"profile_revision": int(profile.revision), "grant_revision": int(profile.grant_revision), "grant_status": grant.status, "masters_in_grant": len(grant.scope.masters), "new_master_in_grant": NEW in grant.scope.masters})
    if mode == "post":
        acc = de.Access(True, profile, grant, de.allowed_tools(profile, grant))
        admit = {t: de.decide(t, acc) is None for t in TOOLS4}
        refuse = {"schwab_prepare_download": de.decide("schwab_prepare_download", acc) is not None}
        ans = {o: [bool(de.check_scope(grant.scope, {"operation": o, "master": NEW, "dataset": d})) for d in sorted(grant.scope.datasets)] for o in ("list", "describe", "query", "download_filtered")}
        out["alyssa"] = {"admit": admit, "refuse": refuse, "master_in_scope": bool(NEW in grant.scope.masters and not any(ans["list"] + ans["describe"] + ans["query"]) and all(ans["download_filtered"])),
                         "download_refused_by_scope_on_new_master": all(ans["download_filtered"]), "tree": "deployed", "code_sha": marker}
    return out


def runner(mode, outp):
    import boto3
    s3 = boto3.client("s3")
    here = os.path.dirname(os.path.abspath(__file__))
    for name in ("ap38_guard.py", "ms2_host_decide.py"):
        s3.put_object(Bucket=BUCKET, Key="ec2/opal-gateway/" + name, Body=io.open(os.path.join(here, name), "rb").read())
    cmd = ("cd /opt/opal-gateway && rm -f /tmp/ap38_guard.py /tmp/ms2_host_decide.py && "
           "aws s3 cp s3://%(b)s/ec2/opal-gateway/ap38_guard.py /tmp/ap38_guard.py --region us-east-1 >/dev/null && "
           "aws s3 cp s3://%(b)s/ec2/opal-gateway/ms2_host_decide.py /tmp/ms2_host_decide.py --region us-east-1 >/dev/null && "
           "%(py)s /tmp/ap38_guard.py 120 /tmp/ms2_host_decide.py --host %(m)s" % {"b": BUCKET, "py": PY, "m": mode})
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
    if "MS2_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("MS2_JSON", 1)[1].strip().splitlines()[0])
    doc["ssm_command_id"], doc["guard"] = cid, "oom_score_adj_1000_rlimit_as_1400mb"
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1))


if __name__ == "__main__":
    if "--host" in sys.argv:
        print("MS2_JSON")
        try:
            print(json.dumps(host(sys.argv[sys.argv.index("--host") + 1]), separators=(",", ":")))
        except Exception:
            print(json.dumps({"fatal": traceback.format_exc()[-800:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1], sys.argv[2])
