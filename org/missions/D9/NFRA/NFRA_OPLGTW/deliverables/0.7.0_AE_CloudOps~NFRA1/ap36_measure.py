#!/usr/bin/env python
"""OG-ap-36 Phase A step 3: THE HOST MEASUREMENTS (a) to (e). READ ONLY; nothing is deployed. The candidate code is staged in a SCRATCH folder on the host (the service's own app/ and
lib/ copied, then the candidate's tools.py, client_core.py and client_adapter_bd49f.py laid over them), the LIVE code in a second scratch folder (the service's app/ as it is: the
host md5 walk equals the live ref); both folders are removed after. Every run is a FRESH process under the gateway role; ONE windowed call at a time; the host is watched and a
run stops at 75 percent used (a sampler kills it at 78). Counts, seconds, percentages and hashes only: the account is resolved in-process and is never printed.
  python ap36_measure.py <out_dir> <release_sha>    -> RUNNER (repository root of the release tree): uploads itself and the candidate's three files, runs the driver once over SSM
  python ap36_measure.py --driver <md5s>            -> HOST DRIVER
  python ap36_measure.py --resolve <stage>          -> HOST: the test account into <stage>/ref.txt (mode 600)
  python ap36_measure.py --chain <stage> <pages>    -> HOST: the transactions chain, <pages> pages (0 = to the null cursor), per page RSS, host percent, wall, row count and the sha256 of the canonical rows
  python ap36_measure.py --plateau <stage>          -> HOST: the whole chain TWICE in one process
  python ap36_measure.py --first <stage>            -> HOST: the first page's wall
  python ap36_measure.py --health <stage> <async|sync> -> HOST: (e) the event loop's /health handler probed every 0.5 s while ONE full page runs through the tool wrapper
(a) the chain (b) the plateau test (c) the first-page wall live vs candidate (d) byte equality of the pages (e) health during a page."""
from __future__ import annotations

import asyncio
import base64
import contextvars
import datetime as dt
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import threading
import time
import traceback
import zlib

SERVICE = "/opt/opal-gateway"
PY = "/opt/opal-gateway/.venv/bin/python"
FIRM = "49financial"
WINDOW_DAYS = 395
STOP_PCT = 75.0
KILL_PCT = 78.0
CAND_FILES = ("app/tools.py", "app/client_core.py", "app/client_adapter_bd49f.py")
GW = "infra/aws/ec2/opal-gateway/"


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


def guard():
    def watch():
        while True:
            if host_pct()[0] > KILL_PCT:
                print("AP36_KILLED host above %s" % KILL_PCT, flush=True)
                os._exit(3)
            time.sleep(0.2)
    threading.Thread(target=watch, daemon=True).start()


def principal_setup():
    from app import audit, context, identity_scope, tools
    from app.config import get_config
    audit.log_call = lambda *a, **k: None
    dom = identity_scope.OPAL_USERS_DOMAIN
    roster = list(getattr(get_config(), "MASTER_ADMIN_PRINCIPALS", ()) or ())
    tid, oid = str(roster[0]).strip().split("/")
    master = context.make_principal(tid, oid, "ap36.master@%s" % dom)
    tools._user_token = lambda: ("ap36.master@%s" % dom, "harness-no-token")
    return master


def rows_of(ans):
    best = []
    for k, v in ans.items():
        if isinstance(v, list) and v and isinstance(v[0], dict) and k != "candidates" and len(v) > len(best):
            best = v
    return best


def canon_hash(ans):
    rows = rows_of(ans) if isinstance(ans, dict) else []
    return len(rows), hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")).hexdigest()


def resolve(stage):
    load_env(stage)
    from app import client_core as cc
    from app import client_adapter_bd49f as bd
    from app import context, tools
    master = principal_setup()
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
        context.set_current_principal(master)
        res = tools.client_resolve_account(firm=FIRM, account_last4=l4)
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


def setup(stage):
    load_env(stage)
    guard()
    from app import context, tools
    master = principal_setup()
    ref = open(os.path.join(stage, "ref.txt"), encoding="utf-8").read().strip()
    from app import client_core as cc
    from app import client_adapter_bd49f as bd
    cc._new_ctx()
    bd.bind_firms()
    today = dt.datetime.now(dt.timezone.utc).date()
    frm = (today - dt.timedelta(days=WINDOW_DAYS)).isoformat()

    def call(cur):
        context.set_current_principal(master)
        try:
            ans = tools.client_get_transactions(firm=FIRM, account=ref, from_date=frm, to_date=cur)
            if asyncio.iscoroutine(ans):                     # the candidate's wrapper is async: run it as the service does, off the loop
                ans = asyncio.run(ans)
            return ans
        except Exception as exc:
            return {"error": "%s: %s" % (type(exc).__name__, str(exc)[:120])}
    return call, today.isoformat(), frm, master, ref, tools, context


def chain_pages(call, start, npages):
    """One chain. Returns pages (rss_mb, host_pct, wall_s, rows, sha, cursor_used, next_cursor) and whether it ended on a null cursor."""
    cur, pages, ended = start, [], False
    n = 0
    while True:
        n += 1
        if npages and n > npages:
            break
        if host_pct()[0] > STOP_PCT:
            return pages, ended, "host above %s" % STOP_PCT
        t0 = time.monotonic()
        ans = call(cur)
        wall = time.monotonic() - t0
        a = ans if isinstance(ans, dict) else {}
        if a.get("error") or a.get("absent_reason"):
            return pages, ended, "page %d answered %s" % (n, str(a.get("absent_reason") or a.get("error"))[:50])
        count, sha = canon_hash(a)
        nxt = a.get("next_cursor")
        pages.append({"page": n, "rss_mb": round(rss_mb(), 1), "host_pct": round(host_pct()[0], 1), "wall_s": round(wall, 2), "rows": count, "sha256": sha,
                      "cursor_used": cur, "next_cursor": nxt, "partitions_read": a.get("partitions_read")})
        del ans, a
        if nxt is None:
            ended = True
            break
        cur = nxt
    return pages, ended, None


def run_chain(stage, npages):
    call, today, _frm, _m, _r, _t, _c = setup(stage)
    before = round(rss_mb(), 1)
    host0 = round(host_pct()[0], 1)
    pages, ended, why = chain_pages(call, today, npages)
    print("AP36_RESULT " + json.dumps({"rss_before_mb": before, "host_pct_before": host0, "pages": pages, "ended_with_null_cursor": ended, "stop": why}, separators=(",", ":")), flush=True)


def run_plateau(stage):
    call, today, _frm, _m, _r, _t, _c = setup(stage)
    before = round(rss_mb(), 1)
    peak = host_pct()[0]
    stop = {"x": False}

    def samp():
        nonlocal peak
        while not stop["x"]:
            peak = max(peak, host_pct()[0])
            time.sleep(0.25)
    threading.Thread(target=samp, daemon=True).start()
    out = {"rss_before_mb": before, "chains": []}
    for k in (1, 2):
        pages, ended, why = chain_pages(call, today, 0)
        out["chains"].append({"pages": len(pages), "rss_end_mb": round(rss_mb(), 1), "ended_with_null_cursor": ended, "stop": why, "max_page_wall_s": max([p["wall_s"] for p in pages] or [0]),
                              "partitions_read_total": sum(p.get("partitions_read") or 0 for p in pages)})
        if why or not ended:
            break
    stop["x"] = True
    out["peak_host_pct"] = round(peak, 1)
    print("AP36_RESULT " + json.dumps(out, separators=(",", ":")), flush=True)


def run_first(stage):
    call, today, _frm, _m, _r, _t, _c = setup(stage)
    t0 = time.monotonic()
    ans = call(today)
    wall = time.monotonic() - t0
    a = ans if isinstance(ans, dict) else {}
    print("AP36_RESULT " + json.dumps({"first_page_wall_s": round(wall, 2), "ok": not (a.get("error") or a.get("absent_reason")), "partitions_read": a.get("partitions_read")}), flush=True)


def run_health(stage, kind):
    load_env(stage)
    guard()
    from app import context
    master = principal_setup()
    ref = open(os.path.join(stage, "ref.txt"), encoding="utf-8").read().strip()
    from app import client_core as cc
    from app import client_adapter_bd49f as bd
    from app import tools
    import app.server as server
    from starlette.requests import Request
    cc._new_ctx()
    bd.bind_firms()
    today = dt.datetime.now(dt.timezone.utc).date()
    frm = (today - dt.timedelta(days=WINDOW_DAYS)).isoformat()
    req = Request({"type": "http", "method": "GET", "path": "/health", "headers": []})

    async def body():
        done = {"x": False, "page_start": None}
        probes = []

        async def tool_call():
            done["page_start"] = time.monotonic()
            try:
                if kind == "async":
                    return await tools.client_get_transactions(FIRM, ref, from_date=frm, to_date=today.isoformat())
                return tools.client_get_transactions(FIRM, ref, from_date=frm, to_date=today.isoformat())     # a sync tool: the loop is blocked while it runs
            finally:
                done["x"] = True

        async def prober():
            t_start = time.monotonic()
            k = 0
            while not done["x"]:
                due = t_start + 0.5 * k
                k += 1
                delay = due - time.monotonic()
                if delay > 0:
                    await asyncio.sleep(delay)
                resp = await server.health(req)
                probes.append({"due": due, "late_s": round(time.monotonic() - due, 3), "status": resp.status_code})
        probe_task = asyncio.ensure_future(prober())
        await asyncio.sleep(0.7)                       # the prober runs alone for a moment, then the page starts
        t0 = time.monotonic()
        ans = await asyncio.ensure_future(tool_call())
        done["x"] = True
        await asyncio.wait_for(probe_task, 60)
        during = [p for p in probes if p["due"] >= done["page_start"]]
        return ans, during, time.monotonic() - t0, len(probes), done["page_start"]
    ctx = contextvars.copy_context()
    ctx.run(context.set_current_principal, master)
    ans, probes, wall, all_probes, done_start = ctx.run(asyncio.run, body())
    a = ans if isinstance(ans, dict) else {}
    print("AP36_RESULT " + json.dumps({"kind": kind, "page_wall_s": round(wall, 2), "probes": len(probes), "probes_before_and_during": all_probes, "max_probe_s": max([p["late_s"] for p in probes] or [0]),
                                       "all_200": all(p["status"] == 200 for p in probes),
                                       "late_probes_over_0p2s": [[round(p["due"] - done_start, 2), p["late_s"]] for p in probes if p["late_s"] > 0.2], "page_ok": not (a.get("error") or a.get("absent_reason")), "partitions_read": a.get("partitions_read")}), flush=True)


def child(args, env=None, timeout=2400):
    p = subprocess.run([PY, os.path.abspath(__file__)] + args, capture_output=True, text=True, timeout=timeout, env=env or dict(os.environ))
    lines = [ln for ln in p.stdout.splitlines() if ln.startswith("AP36_RESULT ")]
    res = json.loads(lines[-1].split(" ", 1)[1]) if lines else {"no_result": True, "stdout_tail": p.stdout[-200:], "stderr_tail": p.stderr[-300:]}
    res["exit_code"] = p.returncode
    return res


def settle(idle):
    for _ in range(120):
        if host_pct()[0] <= idle + 3.0:
            return
        time.sleep(2)


def driver(md5s_json):
    exp = json.loads(md5s_json)
    base = "/tmp/ap36_stage_%d" % os.getpid()
    cand, live = base + "_cand", base + "_live"
    res = {"stage_removed": False}
    try:
        for d in (cand, live):
            os.makedirs(d, mode=0o700)
            shutil.copytree(os.path.join(SERVICE, "app"), os.path.join(d, "app"), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            shutil.copytree(os.path.join(SERVICE, "lib"), os.path.join(d, "lib"), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for rel in CAND_FILES:
            shutil.copyfile("/tmp/ap36_cand_" + os.path.basename(rel), os.path.join(cand, rel))
        res["staged_md5_equals_release"] = {rel: hashlib.md5(open(os.path.join(cand, rel), "rb").read()).hexdigest() == md5 for rel, md5 in exp.items()}
        res["live_stage_files_md5"] = {rel: hashlib.md5(open(os.path.join(live, rel), "rb").read()).hexdigest()[:10] for rel in CAND_FILES}
        idle, total_mb = host_pct()
        res["host_total_mb"], res["idle_host_pct"] = total_mb, round(idle, 1)
        r = subprocess.run([PY, os.path.abspath(__file__), "--resolve", cand], capture_output=True, text=True, timeout=600)
        res["resolve_ok"] = '"ref_resolved": true' in r.stdout
        if not res["resolve_ok"]:
            res["fatal"] = "no account resolved: " + r.stderr[-200:]
            return res
        shutil.copyfile(os.path.join(cand, "ref.txt"), os.path.join(live, "ref.txt"))
        os.chmod(os.path.join(live, "ref.txt"), 0o600)
        env = dict(os.environ)
        env.pop("MALLOC_ARENA_MAX", None)
        steps = [("plateau_cand", ["--plateau", cand]), ("chain_cand", ["--chain", cand, "4"]), ("chain_live", ["--chain", live, "4"])]
        for tag, args in steps:
            settle(idle)
            res[tag] = child(args, env)
        res["first_live"], res["first_cand"] = [], []
        for _ in range(3):
            settle(idle)
            res["first_live"].append(child(["--first", live], env))
            settle(idle)
            res["first_cand"].append(child(["--first", cand], env))
        settle(idle)
        res["health_cand"] = child(["--health", cand, "async"], env)
        settle(idle)
        res["health_live"] = child(["--health", live, "sync"], env)
    finally:
        shutil.rmtree(cand, ignore_errors=True)
        shutil.rmtree(live, ignore_errors=True)
        res["stage_removed"] = not (os.path.exists(cand) or os.path.exists(live))
        res["host_pct_end"] = round(host_pct()[0], 1)
    return res


def diag(md5s_json):
    base = "/tmp/ap36_diag_%d" % os.getpid()
    cand = base + "_cand"
    res = {"stage_removed": False}
    try:
        os.makedirs(cand, mode=0o700)
        shutil.copytree(os.path.join(SERVICE, "app"), os.path.join(cand, "app"), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        shutil.copytree(os.path.join(SERVICE, "lib"), os.path.join(cand, "lib"), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for rel in CAND_FILES:
            shutil.copyfile("/tmp/ap36_cand_" + os.path.basename(rel), os.path.join(cand, rel))
        idle = host_pct()[0]
        r = subprocess.run([PY, os.path.abspath(__file__), "--resolve", cand], capture_output=True, text=True, timeout=600)
        res["resolve_ok"] = '"ref_resolved": true' in r.stdout
        env = dict(os.environ)
        env.pop("MALLOC_ARENA_MAX", None)
        res["health_cand"] = []
        for _ in range(3):
            settle(idle)
            res["health_cand"].append(child(["--health", cand, "async"], env))
    finally:
        shutil.rmtree(cand, ignore_errors=True)
        res["stage_removed"] = not os.path.exists(cand)
    return res


def runner(out_dir, release_sha):
    import boto3
    instance, bucket = "i-07dccb1615503ac99", "opal-313476888478-lambda-artifacts"

    def blob(p):
        return subprocess.run(["git", "show", "%s:%s" % (release_sha, GW + p)], capture_output=True, check=True).stdout
    blobs = {rel: blob(rel) for rel in CAND_FILES}
    md5s = {rel: hashlib.md5(b).hexdigest() for rel, b in blobs.items()}
    s3 = boto3.client("s3")
    names = ["ap36_measure.py"] + ["ap36_cand_" + os.path.basename(rel) for rel in CAND_FILES]
    bodies = [io.open(os.path.abspath(__file__), "rb").read()] + [blobs[rel] for rel in CAND_FILES]
    for k, b in zip(names, bodies):
        s3.put_object(Bucket=bucket, Key="ec2/opal-gateway/" + k, Body=b)
    pulls = " && ".join("aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (bucket, k, k) for k in names)
    rmall = " ".join("/tmp/" + k for k in names)
    mode = "--diag" if os.environ.get("AP36_DIAG") else "--driver"
    cmd = "cd /tmp && rm -f %s && %s && %s /tmp/ap36_measure.py %s '%s'; rm -f %s" % (rmall, pulls, PY, mode, json.dumps(md5s), rmall)
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[instance], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=3500)["Command"]["CommandId"]
    inv = None
    for _ in range(900):
        time.sleep(4)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=instance)
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    nl = chr(10)
    tag = "ap36_diag" if os.environ.get("AP36_DIAG") else "ap36_measure"
    io.open(os.path.join(out_dir, tag + ".raw.txt"), "w", encoding="utf-8", newline=nl).write("status=%s%s--- STDOUT ---%s%s%s--- STDERR ---%s%s%s" % (
        inv["Status"], nl, nl, so[-6000:], nl, nl, inv.get("StandardErrorContent", "")[-600:], nl))
    if "AP36_DRIVER_B64" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    blob64 = so.split("AP36_DRIVER_B64", 1)[1].strip().split()[0]
    doc = json.loads(zlib.decompress(base64.b64decode(blob64)).decode("utf-8"))
    doc["ssm_command_id"] = cid
    io.open(os.path.join(out_dir, tag + ".driver.json"), "w", encoding="utf-8", newline=nl).write(json.dumps(doc, indent=1) + nl)
    print("driver record written; keys:", sorted(doc))


if __name__ == "__main__":
    try:
        if "--diag" in sys.argv:
            print("AP36_DRIVER_B64")
            print(base64.b64encode(zlib.compress(json.dumps(diag(sys.argv[sys.argv.index("--diag") + 1]), separators=(",", ":")).encode("utf-8"), 9)).decode("ascii"))
        elif "--driver" in sys.argv:
            print("AP36_DRIVER_B64")
            print(base64.b64encode(zlib.compress(json.dumps(driver(sys.argv[sys.argv.index("--driver") + 1]), separators=(",", ":")).encode("utf-8"), 9)).decode("ascii"))
        elif "--resolve" in sys.argv:
            resolve(sys.argv[sys.argv.index("--resolve") + 1])
        elif "--chain" in sys.argv:
            i = sys.argv.index("--chain")
            run_chain(sys.argv[i + 1], int(sys.argv[i + 2]))
        elif "--plateau" in sys.argv:
            run_plateau(sys.argv[sys.argv.index("--plateau") + 1])
        elif "--first" in sys.argv:
            run_first(sys.argv[sys.argv.index("--first") + 1])
        elif "--health" in sys.argv:
            i = sys.argv.index("--health")
            run_health(sys.argv[i + 1], sys.argv[i + 2])
        else:
            runner(sys.argv[1], sys.argv[2])
    except SystemExit:
        raise
    except Exception:
        print(json.dumps({"fatal": traceback.format_exc()[-900:]}))
        sys.exit(1)
