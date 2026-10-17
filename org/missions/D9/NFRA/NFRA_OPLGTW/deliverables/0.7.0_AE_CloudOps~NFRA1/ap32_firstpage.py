#!/usr/bin/env python
"""OG-ap-32 Phase A (redo): the FIRST PAGE of the repaired window read, run on the gateway host WITHOUT deploying it. READ-ONLY.
  python ap32_firstpage.py <out.json>  -> RUNNER (repository root of the release tree's sibling: uploads itself and the release's client_adapter_bd49f.py to S3,
                                          runs once over SSM, Rule 12)
  python ap32_firstpage.py --host      -> HOST program, in a NEW process (the running service is untouched)
The release's adapter source is loaded under the installed module's own name BEFORE anything imports it, so client_get_transactions and client_get_fees in this
process go through the candidate code. A master_admin stand-in asks for a 13-month window, first page only. Records: wall seconds, partitions read, window_partial,
whether a cursor is returned, and the host memory percent before, at the PEAK (sampled every 0.25 s) and after. Also: a second call made while the first is in
flight must answer window_read_busy and read nothing. Seconds, counts and percentages only; no value is printed."""
from __future__ import annotations

import datetime as dt
import io
import json
import os
import sys
import threading
import time
import traceback

ROOT = "/opt/opal-gateway"
FIRM = "49financial"
WINDOW_DAYS = 395
ABORT_AT_START_PCT = 50.0


def mem_used_pct():
    d = {}
    for ln in open("/proc/meminfo"):
        k, v = ln.split(":", 1)
        d[k] = int(v.split()[0])
    return 100.0 * (1.0 - d["MemAvailable"] / d["MemTotal"])


class Sampler(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.peak = 0.0
        self.stop_flag = threading.Event()

    def run(self):
        while not self.stop_flag.is_set():
            self.peak = max(self.peak, mem_used_pct())
            time.sleep(0.25)


def host() -> dict:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    out = {"detail": {}}
    D = out["detail"]
    with open(os.path.join(ROOT, ".env"), encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v)
    import importlib.util
    import app as app_pkg
    spec = importlib.util.spec_from_file_location("app.client_adapter_bd49f", "/tmp/ap32_cand_adapter.py")
    bd = importlib.util.module_from_spec(spec)
    bd.__package__ = "app"
    sys.modules["app.client_adapter_bd49f"] = bd
    spec.loader.exec_module(bd)
    app_pkg.client_adapter_bd49f = bd
    D["candidate_page_partitions"] = getattr(bd, "PAGE_PARTITIONS", None)
    D["candidate_read_workers"] = getattr(bd, "READ_WORKERS", None)
    from app import audit, client_core as cc, context, identity_scope, tools
    from app.config import get_config
    audit.log_call = lambda *a, **k: None
    dom = identity_scope.OPAL_USERS_DOMAIN
    roster = list(getattr(get_config(), "MASTER_ADMIN_PRINCIPALS", ()) or ())
    tid, oid = str(roster[0]).strip().split("/")
    master = context.make_principal(tid, oid, "ap32.master@%s" % dom)
    tools._user_token = lambda: ("ap32.master@%s" % dom, "harness-no-token")
    today = dt.datetime.now(dt.timezone.utc).date()
    D["host_mem_used_pct_before"] = round(mem_used_pct(), 1)
    if mem_used_pct() > ABORT_AT_START_PCT:
        out["fatal"] = "host memory already above %s percent; not started" % ABORT_AT_START_PCT
        return out

    def call(tool, **kw):
        context.set_current_principal(master)
        try:
            return getattr(tools, tool)(**kw)
        except Exception as exc:
            return {"error": "%s: %s" % (type(exc).__name__, str(exc)[:120]), "_exc": True}

    # ---- an account the resolver returns that the live tables hold (the OG-ap-28 method) ----------------------------------
    ctx = cc._new_ctx()
    bd.bind_firms()
    segment = bd._firm(ctx, FIRM)
    pre = ctx.prefix(bd.VENDOR, segment, "silver", "dim_account_xref")
    part = bd._select(ctx, pre, None)
    rows = ctx.read_rows(pre, part, columns=list(bd.DIM_COLUMNS)) if part else []
    kept, _x = bd._fence(rows, "bd_account_id")
    xr = {r.get("bd_account_id"): r.get("bd_account_number") for r in kept}
    sets = {}
    for tname in ("transactions", "fees"):
        lp = bd._live_prefix(ctx, segment, tname)
        lpart = bd._select(ctx, lp, None)
        cutoff = (today - dt.timedelta(days=WINDOW_DAYS)).isoformat()
        cols = ["account_id", "trade_date"] + (list(bd.FEE_COLUMNS) if tname == "fees" else [])
        sets[tname] = {r.get("account_id") for r in ctx.read_rows(lp, lpart, columns=cols)
                       if str(r.get("trade_date") or "")[:10] >= cutoff and (tname != "fees" or any(r.get(c) not in (None, 0) for c in bd.FEE_COLUMNS))} if lpart else set()
    common = sorted(set.intersection(*sets.values()) & set(xr)) if all(sets.values()) else []
    ref = None
    for pick in common[:60]:
        l4 = bd._last4(xr.get(pick))
        if not l4:
            continue
        res = call("client_resolve_account", firm=FIRM, account_last4=l4)
        for c in [c for c in ((res or {}).get("candidates") or []) if isinstance(c, dict) and c.get("vendor") == "blackdiamond"]:
            if str(pick) in str(c.get("account_ref") or ""):
                ref = c.get("account_ref")
                break
        if ref:
            break
    D["ref_resolved"] = ref is not None
    if not ref:
        out["fatal"] = "no account ref resolved"
        return out
    frm, to = (today - dt.timedelta(days=WINDOW_DAYS)).isoformat(), today.isoformat()
    sampler = Sampler()
    sampler.start()
    pages = {}
    for tool in ("client_get_transactions", "client_get_fees"):
        sampler.peak = 0.0
        before = mem_used_pct()
        t0 = time.monotonic()
        ans = call(tool, firm=FIRM, account=ref, from_date=frm, to_date=to)
        wall = time.monotonic() - t0
        a = ans if isinstance(ans, dict) else {}
        nrows = sum(len(v) for k, v in a.items() if isinstance(v, list) and v and isinstance(v[0], dict) and k != "candidates")
        pages[tool] = {"wall_seconds": round(wall, 2), "partitions_in_window": a.get("partitions_in_window"), "partitions_read": a.get("partitions_read"),
                       "window_partial": a.get("window_partial"), "next_cursor_non_null": a.get("next_cursor") is not None, "rows_in_answer": nrows,
                       "absent_reason": a.get("absent_reason"), "error": str(a.get("error", ""))[:100] if a.get("error") else None,
                       "host_mem_used_pct": {"before": round(before, 1), "peak": round(sampler.peak, 1), "after": round(mem_used_pct(), 1)}}
    D["first_page"] = pages
    # ---- the busy gate: a second windowed call while one is in flight reads nothing ----------------------------------------
    bd.WINDOW_GATE_WAIT_SECONDS = 0.5
    holder = {}

    def first():
        holder["a"] = call("client_get_fees", firm=FIRM, account=ref, from_date=frm, to_date=to)
    th = threading.Thread(target=first)
    th.start()
    time.sleep(0.6)
    t0 = time.monotonic()
    second = call("client_get_fees", firm=FIRM, account=ref, from_date=frm, to_date=to)
    sw = time.monotonic() - t0
    th.join()
    sd = second if isinstance(second, dict) else {}
    D["busy_gate"] = {"second_call_absent_reason": sd.get("absent_reason"), "second_call_retry_after_seconds": sd.get("retry_after_seconds"),
                      "second_call_partitions_read": sd.get("partitions_read"), "second_call_wall_seconds": round(sw, 2),
                      "first_call_completed": isinstance(holder.get("a"), dict) and holder["a"].get("partitions_read") is not None}
    sampler.stop_flag.set()
    D["host_mem_used_pct_after_all"] = round(mem_used_pct(), 1)
    return out


def runner(outp: str, adapter_path: str) -> None:
    import boto3
    instance, bucket = "i-07dccb1615503ac99", "opal-313476888478-lambda-artifacts"
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket, Key="ec2/opal-gateway/ap32_firstpage.py", Body=io.open(os.path.abspath(__file__), "rb").read())
    s3.put_object(Bucket=bucket, Key="ec2/opal-gateway/ap32_cand_adapter.py", Body=io.open(adapter_path, "rb").read())
    cmd = ("cd /opt/opal-gateway && rm -f /tmp/ap32_firstpage.py /tmp/ap32_cand_adapter.py && "
           "aws s3 cp s3://%s/ec2/opal-gateway/ap32_firstpage.py /tmp/ap32_firstpage.py --region us-east-1 >/dev/null && "
           "aws s3 cp s3://%s/ec2/opal-gateway/ap32_cand_adapter.py /tmp/ap32_cand_adapter.py --region us-east-1 >/dev/null && "
           "/opt/opal-gateway/.venv/bin/python /tmp/ap32_firstpage.py --host" % (bucket, bucket))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[instance], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=900)["Command"]["CommandId"]
    inv = None
    for _ in range(200):
        time.sleep(4)
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=instance)
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    io.open(outp + ".raw.txt", "w", encoding="utf-8", newline="\n").write("status=%s\n--- STDOUT ---\n%s\n--- STDERR ---\n%s\n" % (inv["Status"], so, inv.get("StandardErrorContent", "")[-600:]))
    if "AP32_FP_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("AP32_FP_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1))


if __name__ == "__main__":
    if "--host" in sys.argv:
        print("AP32_FP_JSON")
        try:
            print(json.dumps(host(), separators=(",", ":"), default=str))
        except Exception:
            print(json.dumps({"fatal": traceback.format_exc()[-900:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1], sys.argv[2])
