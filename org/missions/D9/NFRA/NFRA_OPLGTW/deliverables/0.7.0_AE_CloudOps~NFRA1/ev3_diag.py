#!/usr/bin/env python
"""OG-ev-3 diagnostic (read-only, single-threaded, seconds only): where does one read_rows call spend its time on the fees table?
  python ev3_diag.py <out.json>  -> RUNNER (uploads itself to S3, runs once over SSM); python ev3_diag.py --host -> HOST program.
Times, for the newest fees partition: (a) typed_scope.list_keys over the prefix (what ctx.read_rows does first, every call), (b) typed_scope.read_parquet of the one key,
(c) the whole ctx.read_rows call. 3 repetitions each. No value is printed."""
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
    with open(os.path.join(ROOT, ".env"), encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v)
    from app import client_core as cc
    from app import client_adapter_bd49f as bd
    from app import typed_scope
    ctx = cc._new_ctx()
    bd.bind_firms()
    prefix = bd._live_prefix(ctx, bd._firm(ctx, "49financial"), "fees")
    part = bd._partitions(ctx, prefix)[-1]
    scope = ctx._scope(prefix)
    real = scope.served_prefixes[0]
    out = {"table": "fees", "partition_is_newest": True}
    t_list, t_read, t_all, n_listed, rows = [], [], [], 0, 0
    for _ in range(3):
        t0 = time.monotonic()
        listed = typed_scope.list_keys(scope, real)
        t_list.append(round(time.monotonic() - t0, 3))
        n_listed = len(listed)
    keys = [o["key"] for o in listed if o["key"].endswith(".parquet") and cc._partition_of(cc._tail(o["key"], real)) == part]
    key = keys[0]
    for _ in range(3):
        t0 = time.monotonic()
        r, _total, _nbytes = typed_scope.read_parquet(scope, key, columns=list(bd.FEE_READ_COLUMNS), filters=None)
        t_read.append(round(time.monotonic() - t0, 3))
        rows = len(r)
    for _ in range(3):
        t0 = time.monotonic()
        ctx.read_rows(prefix, part, columns=list(bd.FEE_READ_COLUMNS))
        t_all.append(round(time.monotonic() - t0, 3))
    out.update({"objects_listed": n_listed, "rows_in_partition": rows, "list_keys_seconds": t_list, "read_parquet_seconds": t_read, "read_rows_seconds": t_all})
    return out


def runner(outp: str) -> None:
    import boto3
    instance, bucket, key = "i-07dccb1615503ac99", "opal-313476888478-lambda-artifacts", "ec2/opal-gateway/ev3_diag.py"
    boto3.client("s3").put_object(Bucket=bucket, Key=key, Body=io.open(os.path.abspath(__file__), "rb").read())
    cmd = ("cd /opt/opal-gateway && rm -f /tmp/ev3_diag.py && aws s3 cp s3://%s/%s /tmp/ev3_diag.py --region us-east-1 >/dev/null && "
           "/opt/opal-gateway/.venv/bin/python /tmp/ev3_diag.py --host" % (bucket, key))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[instance], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=300)["Command"]["CommandId"]
    inv = None
    for _ in range(80):
        time.sleep(3)
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=instance)
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    if "EV3_DIAG" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("EV3_DIAG", 1)[1].strip())
    doc["ssm_command_id"] = cid
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc))


if __name__ == "__main__":
    if "--host" in sys.argv:
        print("EV3_DIAG")
        try:
            print(json.dumps(host(), separators=(",", ":"), default=str))
        except Exception:
            print(json.dumps({"fatal": traceback.format_exc()[-900:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1])
