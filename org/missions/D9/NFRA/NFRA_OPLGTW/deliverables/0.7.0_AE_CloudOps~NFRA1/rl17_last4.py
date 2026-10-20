#!/usr/bin/env python
"""OG-rl-17 Phase B proof D1 prerequisite: take ONE real last-4 per vendor from the vendor's own silver table by a BOUNDED read (one partition, one column), on the host under the hard guard, from the DEPLOYED tree as the instance role.
READ ONLY. The last-4 values go to the scratch file named on the command line (off-repo, never committed); the repo record is counts only. The deployed tree's own adapters and Ctx do the read (no re-implementation of the access path).
One file, two roles: python rl17_last4.py <out_scratch.json> (RUNNER, repository root) / python rl17_last4.py --host (HOST child under the guard)."""
from __future__ import annotations

import io
import json
import os
import re
import sys
import time
import traceback

ROOT = "/opt/opal-gateway"
INSTANCE, BUCKET, PY = "i-07dccb1615503ac99", "opal-313476888478-lambda-artifacts", ROOT + "/.venv/bin/python"


def alnum_last4(number):
    a = re.sub(r"[^A-Za-z0-9]", "", str(number or ""))
    return a[-4:].upper() if len(a) >= 4 else None


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
    from app import client_adapter_bdcottonwood as bdc
    from app import client_adapter_orion as orion
    from app import client_core as core
    _k49, kct, kinf = core._names()["canonical"]
    ctx = core.Ctx()
    out = {}
    segs = [kinf]          # the new fence maps (orion, inflection firm) to the firm's own segment key (firm_segments == [firm]); the old code refuses, so the segment is named directly
    prefix = ctx.prefix(orion.VENDOR, segs[0], "silver", "fact_positions")
    part = orion._newest(ctx, prefix, None)
    rows = ctx.read_rows(prefix, part, columns=("accountNumber",))
    cand = [alnum_last4(r.get("accountNumber")) for r in rows]
    cand = [c for c in cand if c]
    out["orion"] = {"rows_read": len(rows), "last4": cand[0] if cand else None, "partition": str(part)}
    out["eclipse"] = dict(out["orion"], note="eclipse resolves from the same orion fact_positions table")
    seg = kct
    p_alloc = ctx.prefix(bdc.VENDOR, seg, "silver", bdc.TABLE_ALLOC)
    part_a = bdc._partition(ctx, p_alloc, None)
    rows_a = ctx.read_rows(p_alloc, part_a, columns=bdc.COLS_ALLOC)
    l4 = [bdc._last4(r.get("Account Number")) for r in rows_a if isinstance(r.get("AccountID"), str) and r["AccountID"].startswith(bdc.ACCOUNT_PREFIX)]
    l4 = [c for c in l4 if c]
    out["commonwealth"] = {"rows_read": len(rows_a), "last4": l4[0] if l4 else None, "partition": str(part_a)}
    p_txn = ctx.prefix(bdc.VENDOR, seg, "silver", bdc.TABLE_TXN)
    out["commonwealth_txn_newest_partition"] = str(bdc._partition(ctx, p_txn, None))
    return out


def runner(outp):
    import boto3
    here = os.path.dirname(os.path.abspath(__file__))
    s3 = boto3.client("s3")
    for name in ("ap38_guard.py", "rl17_last4.py"):
        s3.put_object(Bucket=BUCKET, Key="ec2/opal-gateway/" + name, Body=io.open(os.path.join(here, name), "rb").read())
    cmd = ("cd /opt/opal-gateway && rm -f /tmp/ap38_guard.py /tmp/rl17_last4.py && "
           "aws s3 cp s3://%(b)s/ec2/opal-gateway/ap38_guard.py /tmp/ap38_guard.py --region us-east-1 >/dev/null && "
           "aws s3 cp s3://%(b)s/ec2/opal-gateway/rl17_last4.py /tmp/rl17_last4.py --region us-east-1 >/dev/null && "
           "%(py)s /tmp/ap38_guard.py 120 /tmp/rl17_last4.py --host" % {"b": BUCKET, "py": PY})
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
    if "RL17_L4_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-400:]))
    doc = json.loads(so.split("RL17_L4_JSON", 1)[1].strip().splitlines()[0])
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps({k: (v if not isinstance(v, dict) else {a: (b if a != "last4" else ("set" if b else None)) for a, b in v.items()}) for k, v in doc.items()}))


if __name__ == "__main__":
    if "--host" in sys.argv:
        print("RL17_L4_JSON")
        try:
            print(json.dumps(host(), separators=(",", ":")))
        except Exception:
            print(json.dumps({"fatal": traceback.format_exc()[-800:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1])
