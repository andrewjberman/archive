#!/usr/bin/env python
"""OG-ap-36 PHASE A ADDENDUM (amendment A2), READ ONLY: 4a the CTO's CT1 (two concurrent windowed calls through the candidate's own async wrapper), 4b the CVO's added condition
(partition_rows and fence_excluded per page, candidate against the live code, over six pages). The candidate code is staged in a SCRATCH folder on the host (the service's own app/ and
lib/ with the candidate's three code files laid over them), the live code in a second one; both removed after. Every run is a FRESH process under the gateway role. Counts, outcome words,
seconds, hashes and booleans only; the account is resolved in-process and never printed.
  python ap36_ct1.py <out_dir> <release_sha>   -> RUNNER (repository root): uploads this file, ap36_measure.py (helpers) and the candidate's three files; runs the driver once over SSM
  python ap36_ct1.py --driver <md5s>           -> HOST DRIVER
  python ap36_ct1.py --counts <stage>          -> HOST: the six-page transactions chain with per page rows, sha256, partition_rows, fence_excluded
  python ap36_ct1.py --ct1 <stage> <real|short> -> HOST: (i) solo (ii) the pair, 0.3 s apart, on one loop, the gate wait real (15 s) or set to 0.5 s in this scratch process, /health probed throughout
The helpers (staging, host watch, principal, hashing) are those of ap36_measure.py, uploaded beside this file."""
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
import time
import traceback
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ap36_measure as m  # noqa: E402

FIRM, WINDOW_DAYS, GW = m.FIRM, m.WINDOW_DAYS, m.GW


def run_counts(stage):
    call, today, _frm, _m, _r, _t, _c = m.setup(stage)
    cur, pages = today, []
    for n in range(1, 7):
        if m.host_pct()[0] > m.STOP_PCT:
            break
        t0 = time.monotonic()
        a = call(cur)
        wall = time.monotonic() - t0
        if not isinstance(a, dict) or a.get("error") or a.get("absent_reason"):
            print("AP36_RESULT " + json.dumps({"pages": pages, "stop": "page %d answered an error or an absent reason" % n}), flush=True)
            return
        count, sha = m.canon_hash(a)
        den = a.get("denominator") or a.get("_denominator") or {}
        pages.append({"page": n, "rows": count, "sha256": sha, "partition_rows": den.get("partition_rows"), "fence_excluded": den.get("fence_excluded"),
                      "cursor_used": cur, "next_cursor": a.get("next_cursor"), "wall_s": round(wall, 2)})
        if a.get("next_cursor") is None:
            break
        cur = a["next_cursor"]
    print("AP36_RESULT " + json.dumps({"pages": pages}, separators=(",", ":")), flush=True)


def run_ct1(stage, mode):
    m.load_env(stage)
    m.guard()
    from app import context
    master = m.principal_setup()
    ref = open(os.path.join(stage, "ref.txt"), encoding="utf-8").read().strip()
    from app import client_core as cc
    from app import client_adapter_bd49f as bd
    from app import tools
    import app.server as server
    from starlette.requests import Request
    cc._new_ctx()
    bd.bind_firms()
    if mode == "short":
        bd.WINDOW_GATE_WAIT_SECONDS = 0.5              # a scratch-process override only: no file of the release is changed
    today = dt.datetime.now(dt.timezone.utc).date()
    frm = (today - dt.timedelta(days=WINDOW_DAYS)).isoformat()
    req = Request({"type": "http", "method": "GET", "path": "/health", "headers": []})

    async def one():
        return await tools.client_get_transactions(FIRM, ref, from_date=frm, to_date=today.isoformat())

    def sha_of(a):
        return m.canon_hash(a) if isinstance(a, dict) else (0, "")

    rss0 = round(m.rss_mb(), 1)

    async def body():
        t0 = time.monotonic()
        solo = await one()
        solo_wall = time.monotonic() - t0
        rss_after_solo = round(m.rss_mb(), 1)
        s_rows, s_sha = sha_of(solo)
        interval = 0.05 if solo_wall < 3.0 else 0.5
        done = {"x": False}
        probes = []

        async def prober():
            t_start = time.monotonic()
            k = 0
            while not done["x"]:
                due = t_start + interval * k
                k += 1
                delay = due - time.monotonic()
                if delay > 0:
                    await asyncio.sleep(delay)
                resp = await server.health(req)
                probes.append({"late_s": round(time.monotonic() - due, 3), "status": resp.status_code})
        pt = asyncio.ensure_future(prober())
        await asyncio.sleep(0.2)
        tp = time.monotonic()
        t1 = asyncio.ensure_future(one())
        await asyncio.sleep(0.3)
        t2 = asyncio.ensure_future(one())
        a1 = await t1
        t1_done = time.monotonic() - tp
        a2 = await t2
        t2_done = time.monotonic() - tp
        done["x"] = True
        await asyncio.wait_for(pt, 30)
        r1, h1 = sha_of(a1)
        r2, h2 = sha_of(a2)
        busy_key = None
        if isinstance(a2, dict):
            for k, v in a2.items():
                if v == "window_read_busy":
                    busy_key = k
                    break
        reason = str(a2.get("absent_reason"))[:80] if isinstance(a2, dict) else None
        busy = r2 == 0 and ((busy_key is not None) or (reason is not None and "window_read_busy" in reason))
        retry = a2.get("retry_after_seconds") if isinstance(a2, dict) else None
        second = ("window_read_busy" if busy else ("waited_then_equal_solo" if (h2 == s_sha and r2 == s_rows and s_rows > 0)
                                                   else ("busy_reason_not_surfaced" if (r2 == 0 and retry is not None) else "other")))
        return {"mode": mode, "rss_before_mb": rss0, "rss_after_solo_mb": rss_after_solo, "rss_after_pair_mb": round(m.rss_mb(), 1), "gate_wait_s": getattr(bd, "WINDOW_GATE_WAIT_SECONDS", None), "solo_wall_s": round(solo_wall, 2), "solo_rows": s_rows,
                "first_equals_solo": bool(h1 == s_sha and r1 == s_rows and s_rows > 0), "second_outcome": second, "second_busy_key": busy_key, "second_absent_reason": reason, "second_retry_after_seconds": (a2.get("retry_after_seconds") if isinstance(a2, dict) else None), "second_keys_when_other": (sorted(a2)[:12] if (second == "other" and isinstance(a2, dict)) else None), "first_done_s": round(t1_done, 2), "second_done_s": round(t2_done, 2),
                "probe_interval_s": interval, "probes": len(probes), "max_probe_s": max([p["late_s"] for p in probes] or [0]), "all_200": all(p["status"] == 200 for p in probes)}
    ctx = contextvars.copy_context()
    ctx.run(context.set_current_principal, master)
    out = ctx.run(asyncio.run, body())
    print("AP36_RESULT " + json.dumps(out), flush=True)


def driver(md5s_json):
    exp = json.loads(md5s_json)
    base = "/tmp/ap36ct1_stage_%d" % os.getpid()
    cand, live = base + "_cand", base + "_live"
    res = {"stage_removed": False}
    try:
        for d in (cand, live):
            os.makedirs(d, mode=0o700)
            shutil.copytree(os.path.join(m.SERVICE, "app"), os.path.join(d, "app"), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            shutil.copytree(os.path.join(m.SERVICE, "lib"), os.path.join(d, "lib"), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for rel in m.CAND_FILES:
            shutil.copyfile("/tmp/ap36_cand_" + os.path.basename(rel), os.path.join(cand, rel))
        res["staged_md5_equals_release"] = {rel: hashlib.md5(open(os.path.join(cand, rel), "rb").read()).hexdigest() == md5 for rel, md5 in exp.items()}
        idle = m.host_pct()[0]
        res["idle_host_pct"] = round(idle, 1)
        me = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ap36_measure.py")
        r = subprocess.run([m.PY, me, "--resolve", cand], capture_output=True, text=True, timeout=600)
        res["resolve_ok"] = '"ref_resolved": true' in r.stdout
        if not res["resolve_ok"]:
            res["fatal"] = "no account resolved: " + r.stderr[-200:]
            return res
        shutil.copyfile(os.path.join(cand, "ref.txt"), os.path.join(live, "ref.txt"))
        os.chmod(os.path.join(live, "ref.txt"), 0o600)
        env = dict(os.environ)
        env.pop("MALLOC_ARENA_MAX", None)
        me2 = os.path.abspath(__file__)
        for tag, args in (("counts_cand", ["--counts", cand]), ("counts_live", ["--counts", live]), ("ct1_real", ["--ct1", cand, "real"]), ("ct1_short", ["--ct1", cand, "short"])):
            m.settle(idle)
            p = subprocess.run([m.PY, me2] + args, capture_output=True, text=True, timeout=2400, env=env)
            lines = [ln for ln in p.stdout.splitlines() if ln.startswith("AP36_RESULT ")]
            res[tag] = json.loads(lines[-1].split(" ", 1)[1]) if lines else {"no_result": True, "stdout_tail": p.stdout[-200:], "stderr_tail": p.stderr[-300:]}
            res[tag]["exit_code"] = p.returncode
    finally:
        shutil.rmtree(cand, ignore_errors=True)
        shutil.rmtree(live, ignore_errors=True)
        res["stage_removed"] = not (os.path.exists(cand) or os.path.exists(live))
        res["host_pct_end"] = round(m.host_pct()[0], 1)
    return res


def runner(out_dir, release_sha):
    import boto3
    instance, bucket = "i-07dccb1615503ac99", "opal-313476888478-lambda-artifacts"

    def blob(p):
        return subprocess.run(["git", "show", "%s:%s" % (release_sha, GW + p)], capture_output=True, check=True).stdout
    blobs = {rel: blob(rel) for rel in m.CAND_FILES}
    md5s = {rel: hashlib.md5(b).hexdigest() for rel, b in blobs.items()}
    here = os.path.dirname(os.path.abspath(__file__))
    s3 = boto3.client("s3")
    names = ["ap36_ct1.py", "ap36_measure.py"] + ["ap36_cand_" + os.path.basename(rel) for rel in m.CAND_FILES]
    bodies = [io.open(os.path.join(here, "ap36_ct1.py"), "rb").read(), io.open(os.path.join(here, "ap36_measure.py"), "rb").read()] + [blobs[rel] for rel in m.CAND_FILES]
    for k, b in zip(names, bodies):
        s3.put_object(Bucket=bucket, Key="ec2/opal-gateway/" + k, Body=b)
    pulls = " && ".join("aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (bucket, k, k) for k in names)
    rmall = " ".join("/tmp/" + k for k in names)
    cmd = "cd /tmp && rm -f %s && %s && %s /tmp/ap36_ct1.py --driver '%s'; rm -f %s" % (rmall, pulls, m.PY, json.dumps(md5s), rmall)
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[instance], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=3000)["Command"]["CommandId"]
    inv = None
    for _ in range(600):
        time.sleep(4)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=instance)
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    nl = chr(10)
    if "AP36_DRIVER_B64" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(zlib.decompress(base64.b64decode(so.split("AP36_DRIVER_B64", 1)[1].strip().split()[0])).decode("utf-8"))
    doc["ssm_command_id"] = cid
    io.open(os.path.join(out_dir, "ap36_ct1.driver.json"), "w", encoding="utf-8", newline=nl).write(json.dumps(doc, indent=1) + nl)
    print("driver record written; keys:", sorted(doc))


if __name__ == "__main__":
    try:
        if "--driver" in sys.argv:
            print("AP36_DRIVER_B64")
            print(base64.b64encode(zlib.compress(json.dumps(driver(sys.argv[sys.argv.index("--driver") + 1]), separators=(",", ":")).encode("utf-8"), 9)).decode("ascii"))
        elif "--counts" in sys.argv:
            run_counts(sys.argv[sys.argv.index("--counts") + 1])
        elif "--ct1" in sys.argv:
            i = sys.argv.index("--ct1")
            run_ct1(sys.argv[i + 1], sys.argv[i + 2])
        else:
            runner(sys.argv[1], sys.argv[2])
    except SystemExit:
        raise
    except Exception:
        print(json.dumps({"fatal": traceback.format_exc()[-900:]}))
        sys.exit(1)
