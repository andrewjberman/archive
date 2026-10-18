#!/usr/bin/env python
"""OG-ev-7 Step 2: the HOST side of the peers measurement THROUGH THE LISTENER of the running service. Runs under the service's venv python; imports NO gateway code except in the two guarded fresh-process
children (--firm, --pair/--peers), which run under the cgroup hard guard. Reuses ap40_probe_host.py (same directory, uploaded with it) for state(), service(), proc(), usr2(), post(), peers_rows(), mode_call(),
run_child() mechanics and child_pair(). Counts, MB, seconds, status words only: a response body is read into memory, reduced to a row count, and never written.
  python ev7_probe_host.py firmpair            -> guarded children: client_core.canonical_firm(<the test firm>) read on the host, and the first valid period and axis
  python ev7_probe_host.py three <period> <axis> -> THREE etfs_compare_peers calls through the listener, back to back: calls 1 and 2 with the SIGUSR2 heap read around them, call 3 with NO signal;
                                                     VmRSS and VmHWM from /proc after each; stops at once on VmRSS over 1200 MB, a PID change or host memory over 85 percent
  python ev7_probe_host.py fresh <period> <axis> -> the SAME call once in a FRESH guarded process (the cgroup hard guard oom_score_adj_1000_cgroup_memmax_1400mb)
  python ev7_probe_host.py state | call [tool]   -> as ap40_probe_host.py"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ap40_probe_host as ph  # noqa: E402

HOST_STOP_PCT = 85.0
GUARD = ph.GUARD
PY = ph.PY


def host_pct():
    import ap38_measure as m
    return round(m.host_pct(), 1)


def run_child(flag, stage, *extra):
    cmd = ["systemd-run", "--scope", "--quiet", "-p", "MemoryMax=1400M", "-p", "MemoryHigh=1100M", "-p", "MemorySwapMax=0", "--", PY, GUARD, "--cgroup", "120", os.path.abspath(__file__), flag, stage] + list(extra)
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=200)
    lines = [ln for ln in p.stdout.splitlines() if ln.startswith("AP38_RESULT ")]
    res = json.loads(lines[-1].split(" ", 1)[1]) if lines else {"no_result": True}
    res["exit_code"] = p.returncode
    return res


def staged(fn):
    stage = "/tmp/ev7_stage_%d" % os.getpid()
    try:
        os.makedirs(stage, mode=0o700)
        os.symlink("/opt/opal-gateway/app", stage + "/app")
        os.symlink("/opt/opal-gateway/lib", stage + "/lib")
        return fn(stage), stage
    finally:
        shutil.rmtree(stage, ignore_errors=True)


def mode_firmpair():
    def go(stage):
        return {"firm": run_child("--firm", stage), "pair": run_child("--pair", stage)}
    out, stage = staged(go)
    out["guard"] = "oom_score_adj_1000_cgroup_memmax_1400mb"
    out["scratch_removed"] = not os.path.exists(stage)
    return out


def mode_fresh(period, axis):
    def go(stage):
        return run_child("--peers", stage, period, axis)
    out, stage = staged(go)
    out["guard"] = "oom_score_adj_1000_cgroup_memmax_1400mb"
    out["scratch_removed"] = not os.path.exists(stage)
    return out


def one_call(n, signal_on, body, pid0):
    heap_before = ph.usr2(pid0) if signal_on else {"sent": False, "why": "heap_signal off for this call"}
    st, b, wall = ph.post("etfs_compare_peers", body)
    retried = False
    if st == 403 and b.get("error") == "probe_not_armed" and n == 1:      # C15: the first real SSM read; wait the cache window and try ONCE more
        retried = True
        time.sleep(6)
        st, b, wall = ph.post("etfs_compare_peers", body)
    p = ph.proc(pid0)
    heap_after = ph.usr2(pid0) if signal_on else {"sent": False}
    pid1, nr1 = ph.service()
    pct = host_pct()
    return {"n": n, "heap_signal": "on" if signal_on else "off", "status": st, "error": b.get("error"), "wall_s": wall, "rows_matched": ph.peers_rows(b) if st == 200 else 0, "c15_retried": retried,
            "c15_stop": retried and st == 403, "vmrss_mb": p["rss_mb"], "hwm_mb": p["hwm_mb"], "service_pid": pid1, "nrestarts": nr1, "host_pct_after": pct,
            "heap_line_before": heap_before, "heap_line_after": heap_after,
            "stop": bool((p["rss_mb"] or 0) > ph.RSS_STOP_MB or pid1 != pid0 or pct > HOST_STOP_PCT or st != 200)}


def mode_three(period, axis):
    pid0, _nr0 = ph.service()
    body = {"home_ticker": "IDVZ", "period": period, "axis": axis}
    calls = []
    for n, sig in ((1, True), (2, True), (3, False)):
        c = one_call(n, sig, body, pid0)
        calls.append(c)
        if c["stop"]:
            break
    return {"pid_before": pid0, "calls": calls, "calls_made": len(calls), "stopped_early": any(c["stop"] for c in calls), "rss_stop_mb": ph.RSS_STOP_MB, "host_stop_pct": HOST_STOP_PCT}


# ---------------------------------------------------------------------------------------------------- guarded children (fresh processes)
def child_firm(stage):
    ph._load(stage)
    import ap38_measure as m
    m.load_env(stage)
    from app import client_core as cc
    m.emit({"asked": m.FIRM, "canonical_firm": cc.canonical_firm(m.FIRM)})


def child_peers(stage, period, axis):
    m = ph._load(stage)
    m.child_peers(stage, period, axis)


def main():
    a = sys.argv[1:]
    if a[0] == "--firm":
        return child_firm(a[1])
    if a[0] == "--pair":
        return ph.child_pair(a[1])
    if a[0] == "--peers":
        return child_peers(a[1], a[2], a[3])
    out = None
    if a[0] == "state":
        out = ph.mode_state()
    elif a[0] == "call":
        out = ph.mode_call(*(a[1:2]))
    elif a[0] == "firmpair":
        out = mode_firmpair()
    elif a[0] == "three":
        out = mode_three(a[1], a[2])
    elif a[0] == "fresh":
        out = mode_fresh(a[1], a[2])
    print("EV7_PROBE_JSON")
    print(json.dumps(out, separators=(",", ":"), default=str))
    return None


if __name__ == "__main__":
    main()
