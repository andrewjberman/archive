#!/usr/bin/env python
"""OG-ap-28 Phase A step 1: tools_list_before. ONE script that is both the host program (when run with --host, on the gateway host under /opt/opal-gateway/.venv/bin/python)
and its runner (default: uploads itself to S3, runs once over SSM, writes the record; Rule 12).

Host side, READ-ONLY (audit sink stubbed): the registered tool count (app.tools.mcp._tool_manager.list_tools()) and the count the registry's own async list_tools() returns to a
master_admin stand-in (built in-process from the host's roster key, a synthetic Opal-domain address), i.e. what tools/list returns to such a principal; plus the health status.
Counts only: no identifier is printed.
usage: python ap28_toolslist.py <out.json>   (repository root)"""
from __future__ import annotations

import io
import json
import os
import sys
import time
import traceback

ROOT = "/opt/opal-gateway"


def host() -> dict:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    import asyncio
    import urllib.request
    from app import audit, context, identity_scope, tools
    from app.config import get_config
    audit.log_call = lambda *a, **k: None
    out = {}
    out["registry_count"] = len(tools.mcp._tool_manager.list_tools())
    try:
        with urllib.request.urlopen("http://127.0.0.1:8080/health", timeout=10) as r:
            out["health_status"] = r.status
    except Exception as exc:
        out["health_status"] = None
        out["health_error"] = type(exc).__name__
    roster = list(getattr(get_config(), "MASTER_ADMIN_PRINCIPALS", ()) or ())
    out["master_roster_entries"] = len(roster)
    if not roster:
        out["fatal"] = "no master_admin roster entry"
        return out
    tid, oid = str(roster[0]).strip().split("/")
    master = context.make_principal(tid, oid, "ap28.master@%s" % identity_scope.OPAL_USERS_DOMAIN)
    context.set_current_principal(master)
    listed = asyncio.run(tools.mcp.list_tools())
    out["tools_list_master_admin"] = len(listed)
    out["tools_list_equals_registry"] = len(listed) == out["registry_count"]
    return out


def runner(outp: str) -> None:
    import boto3
    instance = "i-07dccb1615503ac99"
    bucket = "opal-313476888478-lambda-artifacts"
    key = "ec2/opal-gateway/ap28_toolslist.py"
    me = os.path.abspath(__file__)
    boto3.client("s3").put_object(Bucket=bucket, Key=key, Body=io.open(me, "rb").read())
    cmd = ("cd /opt/opal-gateway && rm -f /tmp/ap28_toolslist.py && aws s3 cp s3://%s/%s /tmp/ap28_toolslist.py --region us-east-1 >/dev/null && "
           "/opt/opal-gateway/.venv/bin/python /tmp/ap28_toolslist.py --host" % (bucket, key))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[instance], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=300)["Command"]["CommandId"]
    inv = None
    for _ in range(80):
        time.sleep(3)
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=instance)
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    if "AP28_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("AP28_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1))


if __name__ == "__main__":
    if "--host" in sys.argv:
        print("AP28_JSON")
        try:
            print(json.dumps(host(), separators=(",", ":")))
        except Exception:
            print(json.dumps({"fatal": traceback.format_exc()[-800:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1])
