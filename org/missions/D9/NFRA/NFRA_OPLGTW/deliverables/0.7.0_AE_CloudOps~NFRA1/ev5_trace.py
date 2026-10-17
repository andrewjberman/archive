#!/usr/bin/env python
"""OG-ev-5 (round 41), READ ONLY: per dated fees partition of the 13-month window, how many rows does the SOURCE hold and how many does the one test account hold?
  python ev5_trace.py <out_counts.json>   -> the RUNNER (run from the repository root): uploads itself to S3, runs once over SSM (Rule 12), writes the per-date counts locally
  python ev5_trace.py --host              -> the HOST program (on i-07dccb1615503ac99 under /opt/opal-gateway/.venv/bin/python), a NEW process through the installed code
The installed adapter's own read path (release 9d5b712557): ctx.read_rows over the served fees prefix with FEE_READ_COLUMNS, 30 partitions at a time (bd._read_partitions, 8 in flight,
the page the gateway itself reads), the host memory checked between pages (stop at 75 percent). The test account is resolved in-process by the OG-ap-34 chains' own method and
is never printed. Counts and dates only: per date, ALL rows of the partition (source), the rows kept by the 49F fence, the account's rows, the account's non-zero fee amounts.
Audit sink stubbed; nothing is written to any bucket or table. One run; no retry loop."""
from __future__ import annotations

import base64
import io
import json
import os
import sys
import time
import traceback
import zlib

ROOT = "/opt/opal-gateway"
FIRM = "49financial"
WINDOW_DAYS = 395
STOP_PCT = 75.0
PAGE = 30


def mem_used_pct():
    d = {}
    for ln in open("/proc/meminfo"):
        k, v = ln.split(":", 1)
        d[k] = int(v.split()[0])
    return 100.0 * (1.0 - d["MemAvailable"] / d["MemTotal"])


def load_env():
    with open(os.path.join(ROOT, ".env"), encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v)


def host() -> dict:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    load_env()
    import datetime as dt
    from app import audit, client_core as cc, context, identity_scope, tools
    from app import client_adapter_bd49f as bd
    from app.config import get_config
    audit.log_call = lambda *a, **k: None
    dom = identity_scope.OPAL_USERS_DOMAIN
    roster = list(getattr(get_config(), "MASTER_ADMIN_PRINCIPALS", ()) or ())
    tid, oid = str(roster[0]).strip().split("/")
    master = context.make_principal(tid, oid, "ev5.trace@%s" % dom)
    tools._user_token = lambda: ("ev5.trace@%s" % dom, "harness-no-token")
    today = dt.datetime.now(dt.timezone.utc).date()
    start = today - dt.timedelta(days=WINDOW_DAYS)
    out = {"read_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "window": {"from": start.isoformat(), "to": today.isoformat()},
           "host_pct_before": round(mem_used_pct(), 1), "stopped_on_memory": False}

    def call(tool, **kw):
        context.set_current_principal(master)
        try:
            return getattr(tools, tool)(**kw)
        except Exception as exc:
            return {"error": "%s: %s" % (type(exc).__name__, str(exc)[:120])}

    ctx = cc._new_ctx()
    bd.bind_firms()
    segment = bd._firm(ctx, FIRM)
    pre = ctx.prefix(bd.VENDOR, segment, "silver", "dim_account_xref")
    part = bd._select(ctx, pre, None)
    kept, _x = bd._fence(ctx.read_rows(pre, part, columns=list(bd.DIM_COLUMNS)), "bd_account_id")
    xr = {r.get("bd_account_id"): r.get("bd_account_number") for r in kept}
    cutoff = start.isoformat()
    sets = {}
    for tname in ("transactions", "fees"):
        lp = bd._live_prefix(ctx, segment, tname)
        lpart = bd._select(ctx, lp, None)
        cols = ["account_id", "trade_date"] + (list(bd.FEE_COLUMNS) if tname == "fees" else [])
        rows = ctx.read_rows(lp, lpart, columns=cols) if lpart else []
        rows = [r for r in rows if str(r.get("trade_date") or "")[:10] >= cutoff and (tname != "fees" or any(r.get(c) not in (None, 0) for c in bd.FEE_COLUMNS))]
        sets[tname] = {r.get("account_id") for r in rows}
        del rows
    common = sorted(set.intersection(*sets.values()) & set(xr)) if all(sets.values()) else []
    bd_id = None
    for pick in common[:60]:
        l4 = bd._last4(xr.get(pick))
        if not l4:
            continue
        res = call("client_resolve_account", firm=FIRM, account_last4=l4)
        for c in [c for c in ((res or {}).get("candidates") or []) if isinstance(c, dict) and c.get("vendor") == "blackdiamond"]:
            if str(pick) in str(c.get("account_ref") or ""):
                bd_id = str(pick)
                break
        if bd_id:
            break
    out["account_resolved"] = bd_id is not None
    if not bd_id:
        return out
    prefix = bd._live_prefix(ctx, segment, "fees")
    parts = [p for p in bd._partitions(ctx, prefix) if start.isoformat() <= p <= today.isoformat()]
    out["partitions_in_window"] = len(parts)
    rows_out = []
    for i in range(0, len(parts), PAGE):
        if mem_used_pct() > STOP_PCT:
            out["stopped_on_memory"] = True
            break
        chunk = parts[i:i + PAGE]
        for p, kept_rows, count, excluded in bd._read_partitions(ctx, prefix, chunk, bd.FEE_READ_COLUMNS, bd_id):
            items = 0
            for r in kept_rows:
                for c in bd.FEE_COLUMNS:
                    a = bd._num(r.get(c))
                    if a is not None and a != 0:
                        items += 1
            rows_out.append([p, count, count - excluded, len(kept_rows), items])
        out["host_pct_peak"] = round(max(out.get("host_pct_peak", 0.0), mem_used_pct()), 1)
    out["columns"] = ["date", "source_rows_all", "source_rows_fenced", "account_rows", "account_nonzero_fee_amounts"]
    out["partitions"] = rows_out
    return out


def runner(outp: str) -> None:
    import boto3
    instance = "i-07dccb1615503ac99"
    bucket = "opal-313476888478-lambda-artifacts"
    key = "ec2/opal-gateway/ev5_trace.py"
    boto3.client("s3").put_object(Bucket=bucket, Key=key, Body=io.open(os.path.abspath(__file__), "rb").read())
    cmd = ("cd /opt/opal-gateway && rm -f /tmp/ev5_trace.py && aws s3 cp s3://%s/%s /tmp/ev5_trace.py --region us-east-1 >/dev/null && "
           "/opt/opal-gateway/.venv/bin/python /tmp/ev5_trace.py --host; rm -f /tmp/ev5_trace.py" % (bucket, key))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[instance], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=1800)["Command"]["CommandId"]
    inv = None
    for _ in range(420):
        time.sleep(4)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=instance)
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    if "EV5_B64" not in so:
        raise SystemExit("no marker; status=%s stderr=%s stdout_chars=%d" % (inv["Status"], inv.get("StandardErrorContent", "")[-200:], len(so)))
    blob = so.split("EV5_B64", 1)[1].strip().split()[0]
    doc = json.loads(zlib.decompress(base64.b64decode(blob)).decode("utf-8"))
    doc["ssm_command_id"] = cid
    io.open(outp, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(doc, indent=1) + chr(10))
    print("stdout chars %d; wrote the counts; partitions %s of %s in the window; stopped_on_memory %s; account_resolved %s" % (
        len(so), len(doc.get("partitions", [])), doc.get("partitions_in_window"), doc.get("stopped_on_memory"), doc.get("account_resolved")))


if __name__ == "__main__":
    if "--host" in sys.argv:
        print("EV5_B64")
        try:
            print(base64.b64encode(zlib.compress(json.dumps(host(), separators=(",", ":"), default=str).encode("utf-8"), 9)).decode("ascii"))
        except Exception:
            print(base64.b64encode(zlib.compress(json.dumps({"fatal": traceback.format_exc()[-800:]}).encode("utf-8"))).decode("ascii"))
            sys.exit(1)
    else:
        runner(sys.argv[1])
