#!/usr/bin/env python
"""OG-rl-17 Phase B proof (index_pairs): in ONE fresh process from the DEPLOYED tree (/opt/opal-gateway) under the hard guard (W/ap38_guard.py: oom_score_adj 1000, RLIMIT_AS 1400 MB, wall limit 120 s),
`admin_gateway_breakdown._compute` with fakes for the grant store (no principal, no store read, no network write) as tests/test_admin_gateway_breakdown.py::test_real_server_tool_inventory does: every tool placed in the two
segmented buckets (opal-data-assets and opal-data-bd) carries `index_pairs`. READ ONLY. Counts only.
One file, two roles: python rl17_indexpairs.py <out.json> (RUNNER, repository root) / python rl17_indexpairs.py --host (HOST child, run under the guard)."""
from __future__ import annotations

import io
import json
import os
import sys
import time
import traceback

ROOT = "/opt/opal-gateway"
INSTANCE, BUCKET, PY = "i-07dccb1615503ac99", "opal-313476888478-lambda-artifacts", ROOT + "/.venv/bin/python"


def host():
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    os.environ.setdefault("MOCK_GRAPH", "1")
    with open(os.path.join(ROOT, ".env"), encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v)
    from app import admin_gateway_breakdown as bd
    from app import tools

    class FakeDdb:
        def scan(self, **kw):
            return {"Items": []}

    class FakeStore:
        def get(self, key):
            return None

        def query(self, *a, **k):
            return []

    body = bd._compute(scan_client=FakeDdb(), store=FakeStore())
    seg = [c for c in body["channels"] if c["id"] in bd.SEGMENTED_BUCKETS]
    tools_in_seg = [t for c in seg for t in c["tools"]]
    live = sorted(t.name for t in tools.mcp._tool_manager.list_tools())
    seen = [t["name"] for c in body["channels"] for t in c["tools"]]
    return {"segmented_buckets": sorted(c["id"] for c in seg), "segmented_tools": len(tools_in_seg), "with_index_pairs": sum(1 for t in tools_in_seg if isinstance(t.get("index_pairs"), list) and t["index_pairs"]),
            "with_index_pairs_key": sum(1 for t in tools_in_seg if "index_pairs" in t), "channels": len(body["channels"]), "tools_seen_once_each": sorted(seen) == live and len(seen) == len(set(seen)), "registry_count": len(live)}


def runner(outp):
    import boto3
    here = os.path.dirname(os.path.abspath(__file__))
    s3 = boto3.client("s3")
    for name in ("ap38_guard.py", "rl17_indexpairs.py"):
        s3.put_object(Bucket=BUCKET, Key="ec2/opal-gateway/" + name, Body=io.open(os.path.join(here, name), "rb").read())
    cmd = ("cd /opt/opal-gateway && rm -f /tmp/ap38_guard.py /tmp/rl17_indexpairs.py && "
           "aws s3 cp s3://%(b)s/ec2/opal-gateway/ap38_guard.py /tmp/ap38_guard.py --region us-east-1 >/dev/null && "
           "aws s3 cp s3://%(b)s/ec2/opal-gateway/rl17_indexpairs.py /tmp/rl17_indexpairs.py --region us-east-1 >/dev/null && "
           "%(py)s /tmp/ap38_guard.py 120 /tmp/rl17_indexpairs.py --host" % {"b": BUCKET, "py": PY})
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
    if "RL17_IP_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-400:]))
    doc = json.loads(so.split("RL17_IP_JSON", 1)[1].strip().splitlines()[0])
    doc["ssm_command_id"], doc["guard"], doc["read_at"] = cid, "oom_score_adj_1000_rlimit_as_1400mb", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc))


if __name__ == "__main__":
    if "--host" in sys.argv:
        print("RL17_IP_JSON")
        try:
            print(json.dumps(host(), separators=(",", ":")))
        except Exception:
            print(json.dumps({"fatal": traceback.format_exc()[-800:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1])
