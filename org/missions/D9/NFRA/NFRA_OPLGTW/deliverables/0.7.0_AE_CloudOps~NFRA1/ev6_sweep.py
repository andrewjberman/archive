#!/usr/bin/env python
"""OG-ev-6 (round 42): THE WINDOW PAGE SIZE MEASURED ON THE HOST at 30, 60 and 120 partitions per page, THREE fresh guarded processes per size, graded by the rule fixed in the order before any run. READ ONLY; nothing is deployed.
Every gateway-code run is a FRESH process under the cgroup hard guard oom_score_adj_1000_cgroup_memmax_1400mb (systemd-run --scope MemoryMax=1400M, MemoryHigh=1100M, no swap, oom_score_adj 1000, wall limit 120 s); host memory is sampled every
0.25 s and a run stops at 75 percent used. In each process `client_adapter_bd49f.PAGE_PARTITIONS` is ASSIGNED before the first call (no source file changes), the transactions window of the one 49F test account is followed by next_cursor until the
newest 120 partitions are covered (4 pages at 30, 2 at 60, 1 at 120), and each run records max_page_wall_s, first_page_wall_s, median_growth_mb, vmhwm_mb, host_peak_pct, pages and rows_hash_120 (sha256 of the canonical JSON of the rows of the
newest 120 partitions, in order). Hashes only; no row content, account number or name in any record.
  python ev6_sweep.py <out.json> <trunk_sha>            -> RUNNER (repository root): uploads this file, ap38_measure.py, the guard and trunk's client-path files; runs the driver once over SSM
  python ev6_sweep.py --driver <expected_md5_json>      -> HOST DRIVER (runs no gateway code; spawns the guarded children)
  python ev6_sweep.py --sweep <stage> <S>               -> HOST CHILD: one run at page size S
The candidate tree is trunk at trunk_sha: the service's own app/ and lib/ copied into a scratch folder with trunk's client-path files (tools.py, client_core.py, client_adapter_bd49f.py, typed_scope.py) laid over them."""
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
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ap38_measure as m  # noqa: E402

SIZES = (30, 60, 120)
RUNS = 3
COVER = 120
CLIENT_FILES = ("app/tools.py", "app/client_core.py", "app/client_adapter_bd49f.py", "app/typed_scope.py")


def child_sweep(stage, size):
    m.load_env(stage)
    import asyncio
    from app import client_adapter_bd49f as bd
    from app import client_core as cc
    from app import context, tools
    master = m.master_setup()
    ref = open(os.path.join(stage, "ref.txt"), encoding="utf-8").read().strip()
    cc._new_ctx()
    bd.bind_firms()
    bd.PAGE_PARTITIONS = int(size)                    # assigned IN THE PROCESS before the first call; no source file changes
    today = dt.datetime.now(dt.timezone.utc).date()
    frm = (today - dt.timedelta(days=m.WINDOW_DAYS)).isoformat()
    sampler = m.Sampler()
    sampler.start()
    base_rss = m.rss_mb()
    prev, cur, pages, rows_all, covered, why = base_rss, today.isoformat(), [], [], 0, None
    while covered < COVER:
        if m.host_pct() > m.STOP_PCT:
            why = "host above %s percent" % m.STOP_PCT
            break
        context.set_current_principal(master)
        t0 = time.monotonic()
        ans = tools.client_get_transactions(firm=m.FIRM, account=ref, from_date=frm, to_date=cur)
        if asyncio.iscoroutine(ans):
            ans = asyncio.run(ans)
        wall = time.monotonic() - t0
        a = ans if isinstance(ans, dict) else {}
        if a.get("error") or (a.get("absent_reason") and a.get("partitions_read") is None):
            why = "page %d answered %s" % (len(pages) + 1, str(a.get("absent_reason") or a.get("error"))[:40])
            break
        rws = m.rows_of(a)
        rows_all.extend(rws)
        covered += int(a.get("partitions_read") or 0)
        rss = m.rss_mb()
        pages.append({"wall_s": round(wall, 2), "growth_mb": round(rss - prev, 1), "rows": len(rws), "partitions_read": a.get("partitions_read")})
        prev = rss
        nxt = a.get("next_cursor")
        del ans, a
        if nxt is None:
            break
        cur = nxt
    sampler.stop_flag.set()
    growths = [p["growth_mb"] for p in pages[1:]] if len(pages) > 1 else [p["growth_mb"] for p in pages]
    out = {"size": int(size), "pages": len(pages), "covered_partitions": covered, "stop": why, "max_page_wall_s": max([p["wall_s"] for p in pages] or [0]),
           "first_page_wall_s": pages[0]["wall_s"] if pages else None, "median_growth_mb": round(statistics.median(growths), 1) if growths else None,
           "vmhwm_mb": round(m.hwm_mb(), 1), "host_peak_pct": round(max(sampler.peak, m.host_pct()), 1), "rows_total": len(rows_all),
           "rows_hash_120": hashlib.sha256(json.dumps(rows_all, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")).hexdigest(), "page_rows": [p["rows"] for p in pages]}
    m.emit(out)


def run_child(args):
    cmd = ["systemd-run", "--scope", "--quiet", "-p", "MemoryMax=1400M", "-p", "MemoryHigh=1100M", "-p", "MemorySwapMax=0", "--", m.PY, m.GUARD, "--cgroup", "120", os.path.abspath(__file__)] + args
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=200)
    lines = [ln for ln in p.stdout.splitlines() if ln.startswith("AP38_RESULT ")]
    res = json.loads(lines[-1].split(" ", 1)[1]) if lines else {"no_result": True, "stderr_tail": p.stderr[-300:], "stdout_tail": p.stdout[-200:]}
    res["exit_code"] = p.returncode
    return res


def driver(md5s_json):
    exp = json.loads(md5s_json)
    base = "/tmp/ev6_stage_%d" % os.getpid()
    stage = base
    out = {"guard": m.CGROUP_GUARD_NAME, "scratch_removed": False}
    try:
        os.makedirs(stage, mode=0o700)
        shutil.copytree(os.path.join(m.SERVICE, "app"), os.path.join(stage, "app"), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        shutil.copytree(os.path.join(m.SERVICE, "lib"), os.path.join(stage, "lib"), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        live_md5 = {rel: hashlib.md5(open(os.path.join(m.SERVICE, rel), "rb").read()).hexdigest() for rel in CLIENT_FILES}
        for rel in CLIENT_FILES:
            shutil.copyfile("/tmp/ev6_trunk_" + os.path.basename(rel), os.path.join(stage, rel))
        out["trunk_client_files_md5_equal_to_trunk_blobs"] = {rel: hashlib.md5(open(os.path.join(stage, rel), "rb").read()).hexdigest() == exp[rel] for rel in CLIENT_FILES}
        out["trunk_client_files_differing_from_the_live_service"] = [rel for rel in CLIENT_FILES if live_md5[rel] != exp[rel]]
        out["host_pct_idle"] = round(m.host_pct(), 1)
        cmd = ["systemd-run", "--scope", "--quiet", "-p", "MemoryMax=1400M", "-p", "MemoryHigh=1100M", "-p", "MemorySwapMax=0", "--", m.PY, m.GUARD, "--cgroup", "120", "/tmp/ap38_measure.py", "--resolve", stage]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=200)
        out["ref_resolved"] = 'AP38_RESULT {"ref_resolved":true}' in p.stdout
        if not out["ref_resolved"]:
            out["fatal"] = "no account ref resolved: " + (p.stdout[-200:] + p.stderr[-200:])
            return out
        runs = {str(s): [] for s in SIZES}
        for i in range(RUNS):                  # interleaved: round i runs every size once, so a slow minute does not fall on one size
            for s in SIZES:
                runs[str(s)].append(run_child(["--sweep", stage, str(s)]))
        out["runs"] = runs
    finally:
        shutil.rmtree(stage, ignore_errors=True)
        out["scratch_removed"] = not os.path.exists(stage)
        out["host_pct_after"] = round(m.host_pct(), 1)
    return out


def runner(outp, trunk_sha):
    import boto3
    g = "infra/aws/ec2/opal-gateway/"
    here = os.path.dirname(os.path.abspath(__file__))
    s3 = boto3.client("s3")
    exp = {}
    for rel in CLIENT_FILES:
        blob = subprocess.run(["git", "show", "%s:%s" % (trunk_sha, g + rel)], capture_output=True, check=True).stdout
        exp[rel] = hashlib.md5(blob).hexdigest()
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/ev6_trunk_" + os.path.basename(rel), Body=blob)
    for n in ("ev6_sweep.py", "ap38_measure.py", "ap38_guard.py"):
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/" + n, Body=io.open(os.path.join(here, n), "rb").read())
    pulls = " && ".join("aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (m.BUCKET, n, n)
                        for n in ("ev6_sweep.py", "ap38_measure.py", "ap38_guard.py", "ev6_trunk_tools.py", "ev6_trunk_client_core.py", "ev6_trunk_client_adapter_bd49f.py", "ev6_trunk_typed_scope.py"))
    cmd = "cd /opt/opal-gateway && rm -f /tmp/ev6_sweep.py /tmp/ap38_measure.py /tmp/ap38_guard.py /tmp/ev6_trunk_* && %s && %s /tmp/ev6_sweep.py --driver '%s'" % (pulls, m.PY, json.dumps(exp))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[m.INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=2400)["Command"]["CommandId"]
    inv = None
    for _ in range(600):
        time.sleep(4)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=m.INSTANCE)
        except Exception:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    io.open(outp + ".raw.txt", "w", encoding="utf-8", newline="\n").write("status=%s\n--- STDOUT ---\n%s\n--- STDERR ---\n%s\n" % (inv["Status"], so, inv.get("StandardErrorContent", "")[-600:]))
    if "EV6_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("EV6_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps({k: v for k, v in doc.items() if k != "runs"}, indent=1))
    for s, rs in (doc.get("runs") or {}).items():
        for r in rs:
            print(s, {k: r.get(k) for k in ("pages", "max_page_wall_s", "first_page_wall_s", "median_growth_mb", "vmhwm_mb", "host_peak_pct", "covered_partitions", "stop", "exit_code")})


if __name__ == "__main__":
    a = sys.argv
    if "--sweep" in a:
        i = a.index("--sweep")
        child_sweep(a[i + 1], a[i + 2])
    elif "--driver" in a:
        print("EV6_JSON")
        try:
            print(json.dumps(driver(a[a.index("--driver") + 1]), separators=(",", ":"), default=str))
        except Exception:
            import traceback
            print(json.dumps({"fatal": traceback.format_exc()[-900:]}))
            sys.exit(1)
    else:
        runner(a[1], a[2])
