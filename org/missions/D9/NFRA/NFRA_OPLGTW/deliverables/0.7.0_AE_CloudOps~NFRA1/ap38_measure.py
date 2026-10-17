#!/usr/bin/env python
"""OG-ap-38 Phase A step 3: THE HOST MEASUREMENTS (a) to (d), every gateway-code run in a FRESH process under the HARD GUARD (W/ap38_guard.py: oom_score_adj 1000, RLIMIT_AS 1400 MB, wall
limit 120 s). READ ONLY; nothing is deployed. The candidate's files are staged in a SCRATCH folder on the host (the service's own app/ and lib/ copied, the candidate's typed_scope.py and
etfs_rivals_flow.py laid over them); the LIVE code is a second scratch folder (the service's app/ as it is: the host md5 walk equals the live ref). Both folders are removed after.
  python ap38_measure.py <out.json> <release_sha>     -> RUNNER (repository root of the release tree's records): uploads this file, the guard and the candidate's files, runs the driver once over SSM
  python ap38_measure.py --driver <expected_md5_json> -> HOST DRIVER (runs no gateway code itself; spawns the guarded children)
  python ap38_measure.py --resolve <stage>            -> HOST CHILD: the test account into <stage>/ref.txt (mode 600)
  python ap38_measure.py --peers <stage> <period> <axis> -> HOST CHILD: etfs_rivals_flow.etfs_compare_peers("IDVZ", period, axis): outcome, rows matched, wall, VmHWM
  python ap38_measure.py --chain <stage> <pages>      -> HOST CHILD: the transactions chain, <pages> pages, per page RSS, host percent, wall, rows and a canonical sha256 (the driver compares; no hash is written)
(a) the call that ran away (candidate bounded; live code stopped by the guard) (b) a valid pair (c) the 49F chain unchanged (d) the unit acceptable to systemd and cgroup v2 with the memory controller."""
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

SERVICE = "/opt/opal-gateway"
PY = "/opt/opal-gateway/.venv/bin/python"
GUARD = "/tmp/ap38_guard.py"
GUARD_NAME = "oom_score_adj_1000_rlimit_as_1400mb"
CGROUP_GUARD_NAME = "oom_score_adj_1000_cgroup_memmax_1400mb"
GUARD_MODE = ["rlimit"]            # "cgroup" with --driver ... cgroup: each child runs in a transient systemd scope with MemoryMax=1400M (and MemoryHigh, no swap)
FIRM = "49financial"
WINDOW_DAYS = 395
STOP_PCT = 75.0
CAND_FILES = ("app/typed_scope.py", "app/etfs_rivals_flow.py")
PROBE_LOCAL, PROBE_OID = "ap38.probe", "00000000-0000-0000-0000-000000000a38"
INSTANCE, BUCKET = "i-07dccb1615503ac99", "opal-313476888478-lambda-artifacts"


def meminfo():
    d = {}
    for ln in open("/proc/meminfo"):
        k, v = ln.split(":", 1)
        d[k] = int(v.split()[0])
    return d


def host_pct():
    d = meminfo()
    return 100.0 * (1.0 - d["MemAvailable"] / d["MemTotal"])


def status_kb(key):
    for ln in open("/proc/self/status"):
        if ln.startswith(key + ":"):
            return int(ln.split()[1])
    return 0


def rss_mb():
    return status_kb("VmRSS") / 1024.0


def hwm_mb():
    return status_kb("VmHWM") / 1024.0


def load_env(stage):
    with open(os.path.join(SERVICE, ".env"), encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v)
    sys.path.insert(0, stage)
    os.chdir(stage)


def lists_under(obj, key, out=None):
    out = [] if out is None else out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key and isinstance(v, list):
                out.append(v)
            else:
                lists_under(v, key, out)
    elif isinstance(obj, list):
        for v in obj:
            lists_under(v, key, out)
    return out


def dict_under(obj, key):
    if isinstance(obj, dict):
        if isinstance(obj.get(key), dict):
            return obj[key]
        for v in obj.values():
            r = dict_under(v, key)
            if r is not None:
                return r
    return None


def rows_of(ans):
    best = []
    for k, v in ans.items():
        if isinstance(v, list) and v and isinstance(v[0], dict) and k != "candidates" and len(v) > len(best):
            best = v
    return best


class Sampler(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.peak = 0.0
        self.stop_flag = threading.Event()

    def run(self):
        while not self.stop_flag.is_set():
            self.peak = max(self.peak, host_pct())
            time.sleep(0.25)


def emit(obj):
    print("AP38_RESULT " + json.dumps(obj, separators=(",", ":")), flush=True)


# ----------------------------------------------------------------------------------------------------- children (run INSIDE the guard)
def master_setup():
    from app import audit, context, identity_scope, tools
    from app.config import get_config
    audit.log_call = lambda *a, **k: None
    dom = identity_scope.OPAL_USERS_DOMAIN
    roster = list(getattr(get_config(), "MASTER_ADMIN_PRINCIPALS", ()) or ())
    tid, oid = str(roster[0]).strip().split("/")
    master = context.make_principal(tid, oid, "ap38.master@%s" % dom)
    tools._user_token = lambda: ("ap38.master@%s" % dom, "harness-no-token")
    return master


def child_resolve(stage):
    load_env(stage)
    import asyncio
    from app import client_adapter_bd49f as bd
    from app import client_core as cc
    from app import context, tools
    master = master_setup()
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
        if asyncio.iscoroutine(res):
            res = asyncio.run(res)
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
    emit({"ref_resolved": ref is not None})


def frames_of(tb, n=9):
    import traceback
    return ["%s:%d:%s" % (os.path.basename(f.filename), f.lineno, f.name) for f in traceback.extract_tb(tb)[-n:]]


def child_peers(stage, period, axis):
    load_env(stage)
    from app import audit, context, identity_scope
    from app import etfs_rivals_flow as rf
    audit.log_call = lambda *a, **k: None
    opal = context.make_principal(context.MOCK_TENANT_ID, PROBE_OID, "%s@%s" % (PROBE_LOCAL, identity_scope.OPAL_USERS_DOMAIN))
    context.set_current_principal(opal)
    before = rss_mb()
    t0 = time.monotonic()
    out = {"period_arg_is_x": period == "x", "rss_before_mb": round(before, 1)}
    try:
        res = rf.etfs_compare_peers("IDVZ", period, axis)
        out["wall_s"] = round(time.monotonic() - t0, 2)
        res = res if isinstance(res, dict) else {}
        refused = bool(res.get("code") or res.get("error") or res.get("refused") or res.get("refusal"))
        b = (dict_under(res, "buying") or {}).get("rows") or []
        c = (dict_under(res, "contribution") or {}).get("rows") or []
        ps, axs = lists_under(res, "available_periods"), lists_under(res, "available_axes")
        out.update({"outcome": "refusal" if refused else ("rows" if (b or c) else "empty_section"), "rows_matched": len(b) + len(c),
                    "first_period": next((v[0] for v in ps if v), None), "first_axis": next((v[0] for v in axs if v), None),
                    "periods_listed": sum(len(v) for v in ps), "axes_listed": sum(len(v) for v in axs), "answer_keys": sorted(res.keys())[:12]})
    except MemoryError:
        out["wall_s"] = round(time.monotonic() - t0, 2)
        out["outcome"] = "MemoryError"
        out["where"] = frames_of(sys.exc_info()[2])
    except Exception as exc:
        out["wall_s"] = round(time.monotonic() - t0, 2)
        out["outcome"] = "error:" + type(exc).__name__
        out["where"] = frames_of(sys.exc_info()[2])
        out["error_text"] = str(exc)[:160]
    out["vm_hwm_mb"] = round(hwm_mb(), 1)
    emit(out)


def child_chain(stage, npages):
    try:
        _child_chain(stage, npages)
    except BaseException as exc:                      # a diagnostic, never a silent zero
        emit({"pages": [], "stop": "child raised %s" % type(exc).__name__, "error_text": str(exc)[:200], "where": frames_of(sys.exc_info()[2])})


def _child_chain(stage, npages):
    load_env(stage)
    import asyncio
    from app import client_adapter_bd49f as bd
    from app import client_core as cc
    from app import context, tools
    master = master_setup()
    ref = open(os.path.join(stage, "ref.txt"), encoding="utf-8").read().strip()
    cc._new_ctx()
    bd.bind_firms()
    today = dt.datetime.now(dt.timezone.utc).date()
    frm = (today - dt.timedelta(days=WINDOW_DAYS)).isoformat()
    sampler = Sampler()
    sampler.start()
    cur, pages, why = today.isoformat(), [], None
    for n in range(1, npages + 1):
        if host_pct() > STOP_PCT:
            why = "host above %s percent" % STOP_PCT
            break
        context.set_current_principal(master)
        t0 = time.monotonic()
        ans = tools.client_get_transactions(firm=FIRM, account=ref, from_date=frm, to_date=cur)
        if asyncio.iscoroutine(ans):
            ans = asyncio.run(ans)
        wall = time.monotonic() - t0
        a = ans if isinstance(ans, dict) else {}
        if a.get("error") or (a.get("absent_reason") and a.get("partitions_read") is None):
            why = "page %d answered %s" % (n, str(a.get("absent_reason") or a.get("error"))[:40])
            break
        rws = rows_of(a)
        sha = hashlib.sha256(json.dumps(rws, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")).hexdigest()
        pages.append({"page": n, "rss_mb": round(rss_mb(), 1), "wall_s": round(wall, 2), "rows": len(rws), "sha": sha, "next": a.get("next_cursor"), "used": cur})
        nxt = a.get("next_cursor")
        del ans, a
        if nxt is None:
            break
        cur = nxt
    sampler.stop_flag.set()
    emit({"pages": pages, "stop": why, "host_peak_pct": round(max(sampler.peak, host_pct()), 1), "vm_hwm_mb": round(hwm_mb(), 1)})


# ----------------------------------------------------------------------------------------------------- driver (runs NO gateway code)
TUNED_ENV = {}      # set by --driver ... tuned: Arrow's pools shrunk so pyarrow can start under the 1400 MB ADDRESS-SPACE cap (the guard itself is unchanged)


def guarded(args, wall=120):
    env = dict(os.environ)
    env.update(TUNED_ENV)
    if GUARD_MODE[0] == "cgroup":
        cmd = ["systemd-run", "--scope", "--quiet", "-p", "MemoryMax=1400M", "-p", "MemoryHigh=1100M", "-p", "MemorySwapMax=0", "--", PY, GUARD, "--cgroup", str(wall), os.path.abspath(__file__)] + args
    else:
        cmd = [PY, GUARD, str(wall), os.path.abspath(__file__)] + args
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=wall + 60, env=env)
    lines = [ln for ln in p.stdout.splitlines() if ln.startswith("AP38_RESULT ")]
    res = json.loads(lines[-1].split(" ", 1)[1]) if lines else {}
    res["exit_code"] = p.returncode
    res["guard_marker"] = "AP38_GUARD_MEMORYERROR" if "AP38_GUARD_MEMORYERROR" in p.stdout else ("AP38_GUARD_WALL" if "AP38_GUARD_WALL" in p.stdout else None)
    if not lines or res.get("exit_code") not in (0, None):
        res["stdout_tail"] = p.stdout[-300:]
        res["stderr_tail"] = p.stderr[-400:]
    return res


def sh(cmd):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def _chain_part(body, cand, live):
    cc_ = guarded(["--chain", cand, "4"])
    cl_ = guarded(["--chain", live, "4"])
    pgc, pgl = cc_.get("pages") or [], cl_.get("pages") or []
    growth = [pgc[i]["rss_mb"] - pgc[i - 1]["rss_mb"] for i in range(1, len(pgc))]
    equal = len(pgc) == len(pgl) and len(pgc) >= 4 and all(a["rows"] == b["rows"] and a["sha"] == b["sha"] and a["next"] == b["next"] and a["used"] == b["used"] for a, b in zip(pgc, pgl))
    body["chain"] = {"pages": len(pgc), "median_growth_mb": round(statistics.median(growth), 1) if growth else None, "first_page_wall_s": pgc[0]["wall_s"] if pgc else None,
                     "host_peak_pct": max(cc_.get("host_peak_pct") or 0, cl_.get("host_peak_pct") or 0), "pages_equal_live": bool(equal),
                     "live_pages": len(pgl), "live_first_page_wall_s": pgl[0]["wall_s"] if pgl else None, "rows_per_page": [p["rows"] for p in pgc],
                     "candidate_rss_mb_per_page": [p["rss_mb"] for p in pgc], "live_rss_mb_per_page": [p["rss_mb"] for p in pgl],
                     "live_median_growth_mb": (round(statistics.median([pgl[i]["rss_mb"] - pgl[i - 1]["rss_mb"] for i in range(1, len(pgl))]), 1) if len(pgl) > 1 else None),
                     "candidate_stop": cc_.get("stop"), "live_stop": cl_.get("stop"), "candidate_diag": {k: cc_.get(k) for k in ("error_text", "where", "exit_code", "guard_marker", "stderr_tail")},
                     "live_diag": {k: cl_.get(k) for k in ("error_text", "where", "exit_code", "guard_marker", "stderr_tail")}, "candidate_vm_hwm_mb": cc_.get("vm_hwm_mb"), "live_vm_hwm_mb": cl_.get("vm_hwm_mb"), "guard": GUARD_NAME}
    return body


def driver(md5s_json, tuned=False, cgroup=False, chainonly=False):
    global GUARD_NAME
    exp = json.loads(md5s_json)
    if cgroup:
        GUARD_MODE[0] = "cgroup"
        GUARD_NAME = CGROUP_GUARD_NAME
    if tuned:
        TUNED_ENV.update({"ARROW_DEFAULT_MEMORY_POOL": "system", "OMP_NUM_THREADS": "1", "ARROW_IO_THREADS": "1"})
    base = "/tmp/ap38_stage_%d" % os.getpid()
    cand, live = base + "_cand", base + "_live"
    unitdir = "/tmp/ap38_unit_%d" % os.getpid()
    body = {"guard": GUARD_NAME, "scratch_removed": False, "arrow_tuned_env": dict(TUNED_ENV) if tuned else None}
    try:
        for d in (cand, live):
            os.makedirs(d, mode=0o700)
            shutil.copytree(os.path.join(SERVICE, "app"), os.path.join(d, "app"), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            shutil.copytree(os.path.join(SERVICE, "lib"), os.path.join(d, "lib"), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for rel in CAND_FILES:
            shutil.copyfile("/tmp/ap38_cand_" + os.path.basename(rel), os.path.join(cand, rel))
        body["staged_md5_equals_release"] = {rel: hashlib.md5(open(os.path.join(cand, rel), "rb").read()).hexdigest() == md5 for rel, md5 in exp.items() if rel in CAND_FILES}
        body["live_stage_md5_equals_service"] = all(hashlib.md5(open(os.path.join(live, rel), "rb").read()).hexdigest() ==
                                                    hashlib.md5(open(os.path.join(SERVICE, rel), "rb").read()).hexdigest() for rel in CAND_FILES)
        body["host_pct_idle"] = round(host_pct(), 1)
        res = guarded(["--resolve", live])
        body["ref_resolved"] = res.get("ref_resolved") is True
        if not body["ref_resolved"]:
            body["fatal"] = "no account ref resolved: %s" % json.dumps(res)[:300]
            return body
        shutil.copyfile(os.path.join(live, "ref.txt"), os.path.join(cand, "ref.txt"))
        os.chmod(os.path.join(cand, "ref.txt"), 0o600)
        if chainonly:                        # the chain alone (the runaway call is NOT repeated under a 1400 MB cgroup ceiling on a 1.8 GB host)
            return _chain_part(body, cand, live)
        # (a) the call that ran away
        pc = guarded(["--peers", cand, "x", "y"])
        pl = guarded(["--peers", live, "x", "y"])
        body["peers_candidate_raw"] = {k: pc.get(k) for k in ("outcome", "rows_matched", "wall_s", "vm_hwm_mb", "first_period", "first_axis", "periods_listed", "axes_listed", "exit_code", "guard_marker",
                                                                 "where", "error_text", "stdout_tail", "stderr_tail")}
        live_out = pl.get("outcome")
        if live_out not in ("MemoryError",) and (pl.get("guard_marker") or pl.get("exit_code") not in (0, None) or not pl.get("outcome")):
            live_out = "killed_by_guard"
        body["peers_live_raw"] = {k: pl.get(k) for k in ("outcome", "wall_s", "vm_hwm_mb", "exit_code", "guard_marker", "where", "stderr_tail")}
        body["peers"] = {"candidate_outcome": pc.get("outcome"), "candidate_peak_rss_mb": pc.get("vm_hwm_mb"), "candidate_wall_s": pc.get("wall_s"), "live_outcome": live_out, "guard": GUARD_NAME}
        # (b) a valid pair
        pv = guarded(["--peers", cand, str(pc.get("first_period")), str(pc.get("first_axis"))]) if pc.get("first_period") and pc.get("first_axis") else {}
        body["valid_pair"] = {"answered": pv.get("outcome") in ("rows", "empty_section") and pv.get("outcome") == "rows", "peak_rss_mb": pv.get("vm_hwm_mb"), "rows_matched": pv.get("rows_matched"),
                              "outcome": pv.get("outcome"), "wall_s": pv.get("wall_s")}
        _chain_part(body, cand, live)
        # (d) the unit
        os.makedirs(unitdir, mode=0o700)
        shutil.copyfile("/tmp/ap38_cand_opal-gateway.service", os.path.join(unitdir, "opal-gateway.service"))
        rc_v, out_v = sh("systemd-analyze verify %s/opal-gateway.service" % unitdir)
        rc_f, out_f = sh("stat -fc %T /sys/fs/cgroup")
        rc_c, out_c = sh("cat /sys/fs/cgroup/cgroup.controllers")
        body["unit"] = {"cgroup_v2": out_f.strip() == "cgroup2fs", "memory_controller": "memory" in out_c.split(), "verify_rc": rc_v, "verify_output_lines": len([x for x in out_v.splitlines() if x.strip()]),
                        "verify_output_head": out_v[:300], "unit_md5_equals_release": hashlib.md5(open(os.path.join(unitdir, "opal-gateway.service"), "rb").read()).hexdigest() == exp.get("deploy/opal-gateway.service")}
    finally:
        for d in (cand, live, unitdir):
            shutil.rmtree(d, ignore_errors=True)
        body.setdefault("unit", {})["scratch_removed"] = not any(os.path.exists(d) for d in (cand, live, unitdir))
        body["scratch_removed"] = body["unit"]["scratch_removed"]
        body["host_pct_after"] = round(host_pct(), 1)
    return body


def runner(outp, release_sha, tuned=False, cgroup=False, chainonly=False):
    import boto3
    g = "infra/aws/ec2/opal-gateway/"
    me = os.path.abspath(__file__)
    here = os.path.dirname(me)
    s3 = boto3.client("s3")
    exp = {}
    for rel, local in (("app/typed_scope.py", g + "app/typed_scope.py"), ("app/etfs_rivals_flow.py", g + "app/etfs_rivals_flow.py"), ("deploy/opal-gateway.service", g + "deploy/opal-gateway.service")):
        blob = subprocess.run(["git", "show", "%s:%s" % (release_sha, local)], capture_output=True, check=True).stdout
        exp[rel] = hashlib.md5(blob).hexdigest()
        s3.put_object(Bucket=BUCKET, Key="ec2/opal-gateway/ap38_cand_" + os.path.basename(rel), Body=blob)
    s3.put_object(Bucket=BUCKET, Key="ec2/opal-gateway/ap38_measure.py", Body=io.open(me, "rb").read())
    s3.put_object(Bucket=BUCKET, Key="ec2/opal-gateway/ap38_guard.py", Body=io.open(os.path.join(here, "ap38_guard.py"), "rb").read())
    pulls = " && ".join("aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (BUCKET, n, n)
                        for n in ("ap38_measure.py", "ap38_guard.py", "ap38_cand_typed_scope.py", "ap38_cand_etfs_rivals_flow.py", "ap38_cand_opal-gateway.service"))
    cmd = "cd /opt/opal-gateway && rm -f /tmp/ap38_measure.py /tmp/ap38_guard.py /tmp/ap38_cand_* && %s && %s /tmp/ap38_measure.py --driver '%s'%s%s" % (pulls, PY, json.dumps(exp), " tuned" if tuned else "", (" cgroup" if cgroup else "") + (" chainonly" if chainonly else ""))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=1500)["Command"]["CommandId"]
    inv = None
    for _ in range(400):
        time.sleep(4)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except Exception:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    io.open(outp + ".raw.txt", "w", encoding="utf-8", newline="\n").write("status=%s\n--- STDOUT ---\n%s\n--- STDERR ---\n%s\n" % (inv["Status"], so, inv.get("StandardErrorContent", "")[-600:]))
    if "AP38_DRIVER_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("AP38_DRIVER_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1))


if __name__ == "__main__":
    a = sys.argv
    if "--resolve" in a:
        child_resolve(a[a.index("--resolve") + 1])
    elif "--peers" in a:
        i = a.index("--peers")
        child_peers(a[i + 1], a[i + 2], a[i + 3])
    elif "--chain" in a:
        i = a.index("--chain")
        child_chain(a[i + 1], int(a[i + 2]))
    elif "--driver" in a:
        print("AP38_DRIVER_JSON")
        try:
            print(json.dumps(driver(a[a.index("--driver") + 1], tuned=("tuned" in a), cgroup=("cgroup" in a), chainonly=("chainonly" in a)), separators=(",", ":"), default=str))
        except Exception:
            import traceback
            print(json.dumps({"fatal": traceback.format_exc()[-900:]}))
            sys.exit(1)
    else:
        runner(a[1], a[2], tuned=("tuned" in a[3:]), cgroup=("cgroup" in a[3:]), chainonly=("chainonly" in a[3:]))
