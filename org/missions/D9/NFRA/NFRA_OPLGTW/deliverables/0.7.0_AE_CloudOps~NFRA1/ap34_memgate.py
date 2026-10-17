#!/usr/bin/env python
"""OG-ap-34 Phase A step 3, THE MEMORY GATE: the candidate release code in a FRESH process on the host, the transactions page chain for the one test account, 13-month window, ONE call at a time, to_date = the previous next_cursor, FOUR pages. READ-ONLY; nothing is deployed.
  python ap34_memgate.py <out.json> <release_sha>  -> RUNNER (repository root of the release tree): uploads itself and the release adapter and catalog to S3, runs the driver once over SSM (Rule 12)
  python ap34_memgate.py --driver <md5s>  -> HOST DRIVER: stages the release app in a SCRATCH folder, resolves the test account, runs the chain in a fresh process, removes the folder
  python ap34_memgate.py --resolve <stage>  and  --chain <stage>  -> HOST steps
SAFETY: a sampler kills the chain if host memory used passes 78 percent; it also stops after any page that leaves the host above 75 percent. Seconds, MB and percentages only."""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import os
import shutil
import statistics
import subprocess
import sys
import threading
import time
import traceback

SERVICE = "/opt/opal-gateway"
PY = "/opt/opal-gateway/.venv/bin/python"
FIRM = "49financial"
WINDOW_DAYS = 395
STOP_PCT = 75.0
KILL_PCT = 78.0
PAGES = 4


def host_pct():
    d = {}
    for ln in open("/proc/meminfo"):
        k, v = ln.split(":", 1)
        d[k] = int(v.split()[0])
    return 100.0 * (1.0 - d["MemAvailable"] / d["MemTotal"]), d["MemTotal"] // 1024


def rss_mb():
    for ln in open("/proc/self/status"):
        if ln.startswith("VmRSS:"):
            return int(ln.split()[1]) / 1024.0
    return 0.0


def load_env(stage):
    with open(os.path.join(SERVICE, ".env"), encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v)
    sys.path.insert(0, stage)
    os.chdir(stage)


def principal_setup():
    from app import audit, context, identity_scope, tools
    from app.config import get_config
    audit.log_call = lambda *a, **k: None
    dom = identity_scope.OPAL_USERS_DOMAIN
    roster = list(getattr(get_config(), "MASTER_ADMIN_PRINCIPALS", ()) or ())
    tid, oid = str(roster[0]).strip().split("/")
    master = context.make_principal(tid, oid, "ap34.master@%s" % dom)
    tools._user_token = lambda: ("ap34.master@%s" % dom, "harness-no-token")

    def call(tool, **kw):
        context.set_current_principal(master)
        try:
            return getattr(tools, tool)(**kw)
        except Exception as exc:
            return {"error": "%s: %s" % (type(exc).__name__, str(exc)[:120]), "_exc": True}
    return call


def resolve(stage):
    load_env(stage)
    from app import client_core as cc
    from app import client_adapter_bd49f as bd
    call = principal_setup()
    today = dt.datetime.now(dt.timezone.utc).date()
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
    if ref:
        fd = os.open(os.path.join(stage, "ref.txt"), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        os.write(fd, ref.encode("utf-8"))
        os.close(fd)
    print(json.dumps({"ref_resolved": ref is not None}))


def chain(stage):
    load_env(stage)
    ref = open(os.path.join(stage, "ref.txt"), encoding="utf-8").read().strip()
    out = {"pages": [], "stopped_at_host_pct": False}
    state = {"out": out}

    def emit():
        print("AP34_PARTIAL " + json.dumps(state["out"], separators=(",", ":")), flush=True)

    def watch():
        while True:
            if host_pct()[0] > KILL_PCT:
                state["out"]["stopped_at_host_pct"] = True
                state["out"]["killed_at_host_pct"] = round(host_pct()[0], 1)
                emit()
                os._exit(3)
            time.sleep(0.2)
    threading.Thread(target=watch, daemon=True).start()
    from app import client_core as cc
    from app import client_adapter_bd49f as bd
    call = principal_setup()
    cc._new_ctx()
    bd.bind_firms()
    out["read_workers"] = getattr(bd, "READ_WORKERS", None)
    today = dt.datetime.now(dt.timezone.utc).date()
    frm = (today - dt.timedelta(days=WINDOW_DAYS)).isoformat()
    cur = today.isoformat()
    out["rss_before_mb"] = round(rss_mb(), 1)
    out["host_pct_before"] = round(host_pct()[0], 1)
    out["env_arena_max"] = os.environ.get("MALLOC_ARENA_MAX")
    for n in range(1, PAGES + 1):
        t0 = time.monotonic()
        ans = call("client_get_transactions", firm=FIRM, account=ref, from_date=frm, to_date=cur)
        wall = time.monotonic() - t0
        a = ans if isinstance(ans, dict) else {}
        reason = a.get("absent_reason") or a.get("_absent_reason")
        if a.get("error") or reason:
            out["error"] = "page %d answered %s" % (n, str(reason or a.get("error"))[:50])
            break
        nxt = a.get("next_cursor")
        del ans, a
        out["pages"].append({"page": n, "rss_mb": round(rss_mb(), 1), "host_pct": round(host_pct()[0], 1), "wall_s": round(wall, 2)})
        emit()
        if nxt is None or host_pct()[0] > STOP_PCT:
            out["stopped_at_host_pct"] = host_pct()[0] > STOP_PCT
            break
        cur = nxt
    print("AP34_RESULT " + json.dumps(out, separators=(",", ":")), flush=True)


def driver(md5s_json):
    exp = json.loads(md5s_json)
    stage = "/tmp/ap34_stage_%d" % os.getpid()
    res = {"stage_removed": False, "variants": {}}
    try:
        os.makedirs(stage, mode=0o700)
        shutil.copytree(os.path.join(SERVICE, "app"), os.path.join(stage, "app"), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        shutil.copytree(os.path.join(SERVICE, "lib"), os.path.join(stage, "lib"), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for rel, src in (("app/client_adapter_bd49f.py", "/tmp/ap34_cand_adapter.py"), ("app/refs/DATA_CATALOG.yaml", "/tmp/ap34_cand_catalog.yaml")):
            shutil.copyfile(src, os.path.join(stage, rel))
        res["staged_md5_equals_release"] = {rel: hashlib.md5(open(os.path.join(stage, rel), "rb").read()).hexdigest() == md5 for rel, md5 in exp.items()}
        idle, total_mb = host_pct()
        res["host_total_mb"] = total_mb
        res["idle_host_pct"] = round(idle, 1)
        r = subprocess.run([PY, os.path.abspath(__file__), "--resolve", stage], capture_output=True, text=True, timeout=600)
        res["resolve_ok"] = '"ref_resolved": true' in r.stdout
        if not res["resolve_ok"]:
            res["fatal"] = "no account resolved: " + r.stderr[-200:]
            return res
        env = dict(os.environ)
        env.pop("MALLOC_ARENA_MAX", None)
        res["chain"] = {"host_pct_at_start": round(host_pct()[0], 1)}
        p = subprocess.run([PY, os.path.abspath(__file__), "--chain", stage], capture_output=True, text=True, timeout=1500, env=env)
        lines = [ln for ln in p.stdout.splitlines() if ln.startswith("AP34_RESULT ") or ln.startswith("AP34_PARTIAL ")]
        if lines:
            res["chain"].update(json.loads(lines[-1].split(" ", 1)[1]))
        res["chain"]["exit_code"] = p.returncode
        if p.returncode not in (0, 3):
            res["chain"]["stderr_tail"] = p.stderr[-300:]
    finally:
        shutil.rmtree(stage, ignore_errors=True)
        res["stage_removed"] = not os.path.exists(stage)
        res["host_pct_end"] = round(host_pct()[0], 1)
    return res


def runner(outp, release_sha):
    import boto3
    instance, bucket = "i-07dccb1615503ac99", "opal-313476888478-lambda-artifacts"
    g = "infra/aws/ec2/opal-gateway/"

    def blob(p):
        return subprocess.run(["git", "show", "%s:%s" % (release_sha, g + p)], capture_output=True, check=True).stdout
    ad, cat = blob("app/client_adapter_bd49f.py"), blob("app/refs/DATA_CATALOG.yaml")
    md5s = {"app/client_adapter_bd49f.py": hashlib.md5(ad).hexdigest(), "app/refs/DATA_CATALOG.yaml": hashlib.md5(cat).hexdigest()}
    s3 = boto3.client("s3")
    for key, body in (("ap34_measure.py", io.open(os.path.abspath(__file__), "rb").read()), ("ap34_cand_adapter.py", ad), ("ap34_cand_catalog.yaml", cat)):
        s3.put_object(Bucket=bucket, Key="ec2/opal-gateway/" + key, Body=body)
    pulls = " && ".join("aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (bucket, k, k) for k in ("ap34_measure.py", "ap34_cand_adapter.py", "ap34_cand_catalog.yaml"))
    cmd = "cd /tmp && rm -f /tmp/ap34_measure.py /tmp/ap34_cand_adapter.py /tmp/ap34_cand_catalog.yaml && %s && %s /tmp/ap34_measure.py --driver '%s'; rm -f /tmp/ap34_measure.py /tmp/ap34_cand_adapter.py /tmp/ap34_cand_catalog.yaml" % (
        pulls, PY, json.dumps(md5s))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[instance], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=2700)["Command"]["CommandId"]
    inv = None
    for _ in range(720):
        time.sleep(4)
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=instance)
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    io.open(outp + ".raw.txt", "w", encoding="utf-8", newline="\n").write("status=%s\n--- STDOUT ---\n%s\n--- STDERR ---\n%s\n" % (inv["Status"], so, inv.get("StandardErrorContent", "")[-600:]))
    if "AP34_DRIVER_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("AP34_DRIVER_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    io.open(outp + ".driver.json", "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    ch = doc.get("chain", {})
    pages = ch.get("pages", [])
    rs = [p["rss_mb"] for p in pages]
    growth = [rs[i] - rs[i - 1] for i in range(1, len(rs))]
    body = {"release_sha": release_sha, "rss_before_mb": ch.get("rss_before_mb"), "pages": pages,
            "median_growth_mb": round(statistics.median(growth), 1) if growth else None, "threshold_mb_per_page": 20,
            "peak_host_pct": max([p["host_pct"] for p in pages] + [ch.get("host_pct_before") or 0]) if pages else None}
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps({"body": body}, indent=1) + "\n")
    print(json.dumps({k: v for k, v in doc.items() if k != "chain"}, indent=1))
    print(json.dumps(body, indent=1))
    print({k: v for k, v in ch.items() if k not in ("pages",)})


def median_growth(before, pages):
    rs = [p["rss_mb"] for p in pages]
    g = [rs[i] - rs[i - 1] for i in range(1, len(rs))]
    return round(statistics.median(g), 1) if g else None


if __name__ == "__main__":
    try:
        if "--driver" in sys.argv:
            print("AP34_DRIVER_JSON")
            print(json.dumps(driver(sys.argv[sys.argv.index("--driver") + 1]), separators=(",", ":")))
        elif "--resolve" in sys.argv:
            resolve(sys.argv[sys.argv.index("--resolve") + 1])
        elif "--chain" in sys.argv:
            chain(sys.argv[sys.argv.index("--chain") + 1])
        else:
            runner(sys.argv[1], sys.argv[2])
    except SystemExit:
        raise
    except Exception:
        print(json.dumps({"fatal": traceback.format_exc()[-900:]}))
        sys.exit(1)
