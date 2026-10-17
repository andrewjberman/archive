#!/usr/bin/env python
"""OG-ap-34 Phase B, CTO CT1 (Amendment 1): the FULL chain of one 13-month transactions window, ONE call at a time, in a FRESH process on the host under the gateway role,
with the SERVICE's own VmRSS and the host percent sampled beside it. READ-ONLY; nothing is deployed. memory_basis: fresh_process.
  python ap34_fullchain.py <out.json> <release_sha>  -> RUNNER (repository root of the release tree): uploads itself and the release adapter and catalog to S3, runs the driver
                                                       once over SSM (Rule 12), writes <out.json> (the record) and <out.json>.driver.json
  python ap34_fullchain.py --driver <md5s>           -> HOST DRIVER: stages the release app in a scratch folder, resolves the test account, runs the chain, removes the folder
  python ap34_fullchain.py --resolve <stage>         -> HOST step
  python ap34_fullchain.py --chain <stage>           -> HOST step: the chain and the sampler
FAIL (no deploy): the service grows more than 300 MB (the chain process's own peak is RECORDED and graded as a second, strict reading), the host passes 80 percent at any sample, or any page takes over 55 s.
A sampler also stops the chain at once on the host or growth limits. Seconds, MB, percentages, UTC times and counts only: no account, row content or name is printed."""
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
HOST_LIMIT = 80.0
GROWTH_LIMIT_MB = 300.0
PAGE_LIMIT_S = 55.0
MAX_PAGES = 25


def utc_now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def host_pct():
    d = {}
    for ln in open("/proc/meminfo"):
        k, v = ln.split(":", 1)
        d[k] = int(v.split()[0])
    return 100.0 * (1.0 - d["MemAvailable"] / d["MemTotal"]), d["MemTotal"] // 1024


def vmrss_mb(pid="self"):
    try:
        for ln in open("/proc/%s/status" % pid):
            if ln.startswith("VmRSS:"):
                return int(ln.split()[1]) / 1024.0
    except OSError:
        return None
    return None


def service_pid():
    r = subprocess.run(["systemctl", "show", "opal-gateway", "-p", "MainPID", "--value"], capture_output=True, text=True)
    try:
        return int(r.stdout.strip())
    except ValueError:
        return None


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
    spid = service_pid()
    out = {"pages": [], "samples": [], "service_pid_known": spid is not None, "fail_reasons": [], "stopped_early": False}
    state = {"stop": False, "svc0": vmrss_mb(spid) if spid else None, "proc0": None}
    out["service_rss_mb_before"] = None if state["svc0"] is None else round(state["svc0"], 1)
    out["host_pct_before"] = round(host_pct()[0], 1)

    def emit():
        print("AP34_PARTIAL " + json.dumps({"pages": len(out["pages"]), "fail_reasons": out["fail_reasons"]}, separators=(",", ":")), flush=True)

    def sample():
        h = host_pct()[0]
        s = vmrss_mb(spid) if spid else None
        p = vmrss_mb("self")
        rec = {"t": utc_now(), "host_pct": round(h, 1), "service_rss_mb": None if s is None else round(s, 1), "chain_rss_mb": None if p is None else round(p, 1)}
        out["samples"].append(rec)
        if h > HOST_LIMIT:
            out["fail_reasons"].append("host %.1f percent above %s at %s" % (h, HOST_LIMIT, rec["t"]))
            state["stop"] = True
        if s is not None and state["svc0"] is not None and s - state["svc0"] > GROWTH_LIMIT_MB:
            out["fail_reasons"].append("service grew %.0f MB above %s at %s" % (s - state["svc0"], GROWTH_LIMIT_MB, rec["t"]))
            state["stop"] = True
        if p is not None and state["proc0"] is not None:
            out["proc_peak_growth_mb"] = round(max(out.get("proc_peak_growth_mb", 0.0), p - state["proc0"]), 1)
            if p - state["proc0"] > GROWTH_LIMIT_MB and "proc_over_300_first_t" not in out:
                out["proc_over_300_first_t"] = rec["t"]
        return h

    def watch():
        while not state["stop"]:
            h = sample()
            if h > HOST_LIMIT + 3:
                out["stopped_early"] = True
                emit()
                print("AP34_RESULT " + json.dumps(out, separators=(",", ":")), flush=True)
                os._exit(3)
            time.sleep(2.0)
    from app import client_core as cc
    from app import client_adapter_bd49f as bd
    call = principal_setup()
    cc._new_ctx()
    bd.bind_firms()
    out["read_workers"] = getattr(bd, "READ_WORKERS", None)
    out["env_arena_max"] = os.environ.get("MALLOC_ARENA_MAX")
    state["proc0"] = vmrss_mb("self")
    out["chain_rss_mb_before"] = round(state["proc0"], 1)
    threading.Thread(target=watch, daemon=True).start()
    today = dt.datetime.now(dt.timezone.utc).date()
    frm = (today - dt.timedelta(days=WINDOW_DAYS)).isoformat()
    cur = today.isoformat()
    ended_flags, end_rss = [], []
    for k in (1, 2):
        cur = today.isoformat()
        ended = False
        for n in range(1, MAX_PAGES + 1):
            if state["stop"]:
                out["stopped_early"] = True
                break
            t0 = time.monotonic()
            ans = call("client_get_transactions", firm=FIRM, account=ref, from_date=frm, to_date=cur)
            wall = time.monotonic() - t0
            a = ans if isinstance(ans, dict) else {}
            reason = a.get("absent_reason") or a.get("_absent_reason")
            if a.get("error") or reason:
                out["fail_reasons"].append("chain %d page %d answered %s" % (k, n, str(reason or a.get("error"))[:50]))
                break
            nxt = a.get("next_cursor")
            rec = {"chain": k, "page": n, "wall_s": round(wall, 2), "chain_rss_mb": round(vmrss_mb("self"), 1),
                   "service_rss_mb": None if not spid else round(vmrss_mb(spid) or 0, 1),
                   "host_pct": round(host_pct()[0], 1), "partitions_read": a.get("partitions_read"), "partitions_in_window": a.get("partitions_in_window"),
                   "window_partial": a.get("window_partial"), "next_cursor_non_null": nxt is not None, "ended_t": utc_now()}
            out["pages"].append(rec)
            if wall > PAGE_LIMIT_S:
                out["fail_reasons"].append("chain %d page %d took %.1f s above %s" % (k, n, wall, PAGE_LIMIT_S))
                break
            del ans, a
            emit()
            if nxt is None:
                ended = True
                break
            cur = nxt
        ended_flags.append(ended)
        end_rss.append(round(vmrss_mb("self"), 1))
        if not ended or out["fail_reasons"] or state["stop"]:
            break
    out["ended_flags"] = ended_flags
    out["end_rss_per_chain"] = end_rss
    ended = len(ended_flags) == 2 and all(ended_flags)
    state["stop"] = True
    sample()
    out["ended_with_null_cursor"] = ended
    print("AP34_RESULT " + json.dumps(out, separators=(",", ":")), flush=True)


def driver(md5s_json):
    exp = json.loads(md5s_json)
    stage = "/tmp/ap34_stage_%d" % os.getpid()
    res = {"stage_removed": False}
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
        p = subprocess.run([PY, os.path.abspath(__file__), "--chain", stage], capture_output=True, text=True, timeout=2400, env=env)
        lines = [ln for ln in p.stdout.splitlines() if ln.startswith("AP34_RESULT ")]
        res["chain"] = json.loads(lines[-1].split(" ", 1)[1]) if lines else {}
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
    for key, body in (("ap34_fullchain.py", io.open(os.path.abspath(__file__), "rb").read()), ("ap34_cand_adapter.py", ad), ("ap34_cand_catalog.yaml", cat)):
        s3.put_object(Bucket=bucket, Key="ec2/opal-gateway/" + key, Body=body)
    names = ("ap34_fullchain.py", "ap34_cand_adapter.py", "ap34_cand_catalog.yaml")
    pulls = " && ".join("aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (bucket, k, k) for k in names)
    cmd = "cd /tmp && rm -f %s && %s && %s /tmp/ap34_fullchain.py --driver '%s'; rm -f %s" % (
        " ".join("/tmp/" + k for k in names), pulls, PY, json.dumps(md5s), " ".join("/tmp/" + k for k in names))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[instance], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=3000)["Command"]["CommandId"]
    inv = None
    for _ in range(720):
        time.sleep(4)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=instance)
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    io.open(outp + ".raw.txt", "w", encoding="utf-8", newline=chr(10)).write("status=%s%s--- STDOUT ---%s%s%s--- STDERR ---%s%s%s" % (
        inv["Status"], chr(10), chr(10), so, chr(10), chr(10), inv.get("StandardErrorContent", "")[-600:], chr(10)))
    if "AP34_DRIVER_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("AP34_DRIVER_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    ch = doc.get("chain", {})
    pages = ch.get("pages", [])
    by = {k: [p for p in pages if p.get("chain") == k] for k in (1, 2)}
    er = ch.get("end_rss_per_chain") or []
    svc = [s["service_rss_mb"] for s in ch.get("samples", []) if s.get("service_rss_mb") is not None]
    def per(k):
        ps = by[k]
        rs = [p["chain_rss_mb"] for p in ps]
        gr = [rs[i] - rs[i - 1] for i in range(1, len(rs))]
        return {"pages": len(ps), "partitions_read_total": sum(p.get("partitions_read") or 0 for p in ps), "longest_page_wall_s": max([p["wall_s"] for p in ps] or [0]),
                "first_page_wall_s": ps[0]["wall_s"] if ps else None, "end_rss_mb": er[k - 1] if len(er) >= k else None,
                "median_page_growth_mb": round(statistics.median(gr), 1) if gr else None, "host_pct_peak_at_page_ends": max([p["host_pct"] for p in ps] or [0])}
    c1, c2 = per(1), per(2)
    net2 = round(er[1] - er[0], 1) if len(er) == 2 else None
    body = {"memory_basis": "fresh_process", "release_sha": release_sha, "read_at": utc_now(), "two_chains_in_one_process": True,
            "chain1": c1, "chain2": c2, "chain_rss_mb_before": ch.get("chain_rss_mb_before"),
            "chain1_net_growth_from_start_mb": round(er[0] - ch["chain_rss_mb_before"], 1) if er else None,
            "chain2_net_growth_from_chain1_end_mb": net2, "chain2_net_growth_limit_mb": 50,
            "chain_process_peak_growth_from_start_mb": ch.get("proc_peak_growth_mb"),
            "ended_with_null_cursor_both": ch.get("ended_flags") == [True, True], "fail_reasons": ch.get("fail_reasons"),
            "service_rss_mb_before": ch.get("service_rss_mb_before"), "service_rss_mb_min": min(svc) if svc else None, "service_rss_mb_max": max(svc) if svc else None,
            "host_pct_before": ch.get("host_pct_before"), "host_pct_peak": max([s["host_pct"] for s in ch.get("samples", [])] + [p["host_pct"] for p in pages] or [0]),
            "longest_page_wall_s": max([p["wall_s"] for p in pages] or [0]), "sample_count": len(ch.get("samples", [])),
            "per_page": pages, "samples_every_about_s": 2, "samples": ch.get("samples", [])}
    body["verdict"] = "PASS" if (not body["fail_reasons"] and body["ended_with_null_cursor_both"] and net2 is not None and net2 <= 50
                                 and body["host_pct_peak"] < HOST_LIMIT and body["longest_page_wall_s"] <= PAGE_LIMIT_S) else "FAIL"
    io.open(outp + ".driver.json", "w", encoding="utf-8", newline=chr(10)).write(json.dumps(doc, indent=1) + chr(10))
    io.open(outp, "w", encoding="utf-8", newline=chr(10)).write(json.dumps({"body": body}, indent=1) + chr(10))
    print(json.dumps({k: v for k, v in body.items() if k not in ("samples", "per_page")}, indent=1))
    print([(p["chain"], p["page"], p["wall_s"], p["chain_rss_mb"], p["host_pct"], p["partitions_read"]) for p in pages])


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
