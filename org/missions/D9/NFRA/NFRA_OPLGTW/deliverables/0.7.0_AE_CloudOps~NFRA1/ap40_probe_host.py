#!/usr/bin/env python
"""OG-ap-40 Phase B: the HOST side of the probes THROUGH THE LISTENER of the running service. Runs under the service's venv python; imports NO gateway code except in the two guarded fresh-process children
(--resolve, --pair), which run under the cgroup hard guard. Counts, MB, seconds, hashes and status words only: a response body is read into memory, reduced to a row count and a sha256, and never written.
  python ap40_probe_host.py state                       -> the service PID, NRestarts, VmRSS, whether the SIGUSR2 handler is installed, the port bind
  python ap40_probe_host.py gather                      -> guarded children: the test account's reference (printed once, for the orchestrator to put in the lease) and a valid period and axis
  python ap40_probe_host.py call [tool]                 -> one POST to the listener with an empty object (default etfs_compare_peers): the status word
  python ap40_probe_host.py peers <period> <axis>       -> SIGUSR2 heap read, ONE etfs_compare_peers call, SIGUSR2 heap read; the C15 retry
  python ap40_probe_host.py chain [max_pages]           -> the window chain of the lease's account, page after page, VmRSS before and after each page (CT3: over 1200 MB stops)
  python ap40_probe_host.py refuse                      -> a third tool name and another account reference
The lease's account reference is read ON THE HOST from the lease parameter (the instance role may read it) and is never printed."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

PORT = 8099
FIRM = "49financial"
WINDOW_DAYS = 395
RSS_STOP_MB = 1200.0
LEASE = "/opal-gateway/probe/lease"
SIGUSR2_BIT = 1 << 11
GUARD = "/tmp/ap38_guard.py"
PY = "/opt/opal-gateway/.venv/bin/python"


def sh(cmd):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def service():
    _rc, out = sh("systemctl show opal-gateway -p MainPID -p NRestarts")
    kv = dict(ln.split("=", 1) for ln in out.splitlines() if "=" in ln)
    return int(kv.get("MainPID") or 0), kv.get("NRestarts")


def proc(pid):
    out = {"rss_mb": None, "hwm_mb": None, "sigusr2_handler": False}
    try:
        for ln in open("/proc/%d/status" % pid, encoding="utf-8", errors="replace"):
            if ln.startswith("VmRSS:"):
                out["rss_mb"] = round(int(ln.split()[1]) / 1024.0, 1)
            elif ln.startswith("VmHWM:"):
                out["hwm_mb"] = round(int(ln.split()[1]) / 1024.0, 1)
            elif ln.startswith("SigCgt:"):
                out["sigusr2_handler"] = bool(int(ln.split()[1], 16) & SIGUSR2_BIT)
    except OSError:
        pass
    return out


def usr2(pid):
    """SIGUSR2 over SSM, only when the handler is installed (an unhandled SIGUSR2 would terminate the service). Returns the heap line the service wrote."""
    if not proc(pid)["sigusr2_handler"]:
        return {"sent": False, "why": "no SIGUSR2 handler installed; nothing was sent"}
    os.kill(pid, 12)
    line = None
    for _ in range(8):
        time.sleep(0.6)
        _rc, out = sh("journalctl -u opal-gateway --since=-12s --no-pager -o cat | grep 'probe heap pid=' | tail -1")
        if "probe heap pid=%d" % pid in out:
            line = out
            break
    res = {"sent": True, "line_found": line is not None}
    if line:
        for tok in line.split():
            for key in ("VmRSS", "VmHWM"):
                if tok.startswith(key + "="):
                    digits = "".join(ch for ch in tok.split("=", 1)[1] if ch.isdigit())
                    res[key] = round(int(digits) / 1024.0, 1) if digits else None
    return res


def post(tool, body, timeout=120):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request("http://127.0.0.1:%d/probe/%s" % (PORT, tool), data=data, method="POST", headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode("utf-8")), round(time.time() - t0, 2)
    except urllib.error.HTTPError as exc:
        try:
            return exc.code, json.loads(exc.read().decode("utf-8")), round(time.time() - t0, 2)
        except Exception:
            return exc.code, {}, round(time.time() - t0, 2)
    except Exception as exc:
        return -1, {"error": "connection:" + type(exc).__name__}, round(time.time() - t0, 2)


def lease_ref():
    rc, out = sh("aws ssm get-parameter --name %s --region us-east-1 --query Parameter.Value --output text" % LEASE)
    if rc != 0:
        return None
    try:
        return json.loads(out).get("account_ref")
    except Exception:
        return None


def rows_of(ans):
    best = []
    if isinstance(ans, dict):
        for k, v in ans.items():
            if isinstance(v, list) and v and isinstance(v[0], dict) and k != "candidates" and len(v) > len(best):
                best = v
    return best


def peers_rows(ans):
    def under(obj, key):
        if isinstance(obj, dict):
            if isinstance(obj.get(key), dict):
                return obj[key]
            for v in obj.values():
                got = under(v, key)
                if got is not None:
                    return got
        return None
    return len((under(ans, "buying") or {}).get("rows") or []) + len((under(ans, "contribution") or {}).get("rows") or [])


def digest(rows):
    return hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------------------------------- modes
def mode_state():
    pid, nr = service()
    _rc, ss = sh("ss -ltnp")
    rows = [ln.split() for ln in ss.splitlines() if (":%d " % PORT) in (ln + " ")]
    return {"pid": pid, "nrestarts": nr, "proc": proc(pid), "bound": sorted({r[3].rsplit(":", 1)[0] for r in rows if len(r) > 3}), "bound_to_service_pid": any(("pid=%d," % pid) in " ".join(r) for r in rows)}


def run_child(flag, stage):
    cmd = ["systemd-run", "--scope", "--quiet", "-p", "MemoryMax=1400M", "-p", "MemoryHigh=1100M", "-p", "MemorySwapMax=0", "--", PY, GUARD, "--cgroup", "120", os.path.abspath(__file__), flag, stage]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=200)
    lines = [ln for ln in p.stdout.splitlines() if ln.startswith("AP38_RESULT ")]
    res = json.loads(lines[-1].split(" ", 1)[1]) if lines else {"no_result": True}
    res["exit_code"] = p.returncode
    return res


def mode_gather():
    stage = "/tmp/ap40_gather_%d" % os.getpid()
    out = {"guard": "oom_score_adj_1000_cgroup_memmax_1400mb", "scratch_removed": False}
    try:
        os.makedirs(stage, mode=0o700)
        os.symlink("/opt/opal-gateway/app", stage + "/app")
        os.symlink("/opt/opal-gateway/lib", stage + "/lib")
        out["resolve"] = run_child("--resolve", stage)
        out["pair"] = run_child("--pair", stage)
    finally:
        shutil.rmtree(stage, ignore_errors=True)
        out["scratch_removed"] = not os.path.exists(stage)
    ref = (out.get("resolve") or {}).pop("ref", None)
    return out, ref


def mode_call(tool="etfs_compare_peers"):
    pid, nr = service()
    st, b, wall = post(tool, {})
    return {"status": st, "error": b.get("error"), "wall_s": wall, "pid": pid, "nrestarts": nr}


def mode_peers(period, axis):
    pid0, _ = service()
    h0 = usr2(pid0)
    p0 = proc(pid0)
    body = {"home_ticker": "IDVZ", "period": period, "axis": axis}
    st, b, wall = post("etfs_compare_peers", body)
    retried = False
    if st == 403 and b.get("error") == "probe_not_armed":      # C15: the first real SSM read; wait the cache window and try ONCE more
        retried = True
        time.sleep(6)
        st, b, wall = post("etfs_compare_peers", body)
    p1 = proc(pid0)
    h1 = usr2(pid0)
    pid1, nr1 = service()
    return {"status": st, "error": b.get("error"), "wall_s": wall, "rows_matched": peers_rows(b) if st == 200 else 0, "c15_retried": retried, "c15_stop": retried and st == 403,
            "pid_before": pid0, "pid_after": pid1, "nrestarts_after": nr1, "heap_before_signal": h0, "heap_after_signal": h1, "rss_before_proc_mb": p0["rss_mb"], "rss_after_proc_mb": p1["rss_mb"],
            "hwm_after_proc_mb": p1["hwm_mb"], "over_1200": bool(p1["rss_mb"] is not None and p1["rss_mb"] > RSS_STOP_MB)}


def mode_chain(max_pages):
    ref = lease_ref()
    pid0, _ = service()
    h0 = usr2(pid0)
    today = dt.datetime.now(dt.timezone.utc).date()
    frm = (today - dt.timedelta(days=WINDOW_DAYS)).isoformat()
    cur = today.isoformat()
    pages = []
    stopped = False
    for n in range(1, max_pages + 1):
        before = proc(pid0)["rss_mb"]
        st, b, wall = post("client_get_transactions", {"firm": FIRM, "account": ref, "platform": None, "from_date": frm, "to_date": cur})
        after = proc(pid0)["rss_mb"]
        rws = rows_of(b)
        pages.append({"page": n, "status": st, "error": b.get("error"), "wall_s": wall, "rows": len(rws), "sha": digest(rws), "rss_before_mb": before, "rss_after_mb": after,
                      "growth_mb": None if (before is None or after is None) else round(after - before, 1), "next_cursor_present": b.get("next_cursor") is not None})
        if after is not None and after > RSS_STOP_MB:
            stopped = True
            break
        if st != 200 or b.get("next_cursor") is None:
            break
        cur = b.get("next_cursor")
    pid1, nr1 = service()
    h1 = usr2(pid0)
    return {"pages": pages, "pages_run": len(pages), "stopped_over_1200": stopped, "pid_before": pid0, "pid_after": pid1, "nrestarts_after": nr1, "heap_before_signal": h0, "heap_after_signal": h1,
            "account_ref_found": ref is not None}


def mode_refuse():
    ref = lease_ref()
    s1, b1, _ = post("client_get_fees", {"firm": FIRM, "account": ref})
    s2, b2, _ = post("client_get_transactions", {"firm": FIRM, "account": "****0000/blackdiamond/other", "platform": None, "from_date": None, "to_date": None})
    return {"other_tool": {"status": s1, "error": b1.get("error")}, "other_account": {"status": s2, "error": b2.get("error")}}


# ---------------------------------------------------------------------------------------------------- guarded children (fresh processes)
def _load(stage):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import ap38_measure as m
    return m


def child_resolve(stage):
    m = _load(stage)
    cap = []
    real_emit = m.emit
    m.emit = cap.append
    try:
        m.child_resolve(stage)
    finally:
        m.emit = real_emit
    ref = None
    path = os.path.join(stage, "ref.txt")
    if os.path.exists(path):
        ref = open(path, encoding="utf-8").read().strip()
    real_emit({"ref_resolved": ref is not None, "ref": ref})


def child_pair(stage):
    m = _load(stage)
    cap = []
    real_emit = m.emit
    m.emit = cap.append
    try:
        m.child_peers(stage, "x", "x")
    finally:
        m.emit = real_emit
    res = cap[-1] if cap else {}
    real_emit({"period": res.get("first_period"), "axis": res.get("first_axis"), "periods_listed": res.get("periods_listed"), "axes_listed": res.get("axes_listed"), "outcome": res.get("outcome"),
               "peak_rss_mb": res.get("vm_hwm_mb")})


def main():
    a = sys.argv[1:]
    if a[0] == "--resolve":
        return child_resolve(a[1])
    if a[0] == "--pair":
        return child_pair(a[1])
    out = None
    if a[0] == "state":
        out = mode_state()
    elif a[0] == "gather":
        out, ref = mode_gather()
        print("AP40_REF " + (ref or ""), flush=True)
    elif a[0] == "call":
        out = mode_call(*(a[1:2]))
    elif a[0] == "peers":
        out = mode_peers(a[1], a[2])
    elif a[0] == "chain":
        out = mode_chain(int(a[1]) if len(a) > 1 else 8)
    elif a[0] == "refuse":
        out = mode_refuse()
    print("AP40_PROBE_JSON")
    print(json.dumps(out, separators=(",", ":"), default=str))
    return None


if __name__ == "__main__":
    main()
