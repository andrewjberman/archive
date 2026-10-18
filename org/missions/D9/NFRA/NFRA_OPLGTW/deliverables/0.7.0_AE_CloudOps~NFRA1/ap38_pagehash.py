#!/usr/bin/env python
"""OG-ap-38 Phase B, arm e15 (the first two pages of the chain equal what the live code produced in Phase A): the INSTALLED code's first two transactions pages, as sha256 of their canonical rows plus the cursors and
row counts, in a FRESH process under the cgroup hard guard. Run twice: BEFORE the deploy (the live code, the baseline) and AFTER (the installed release), then compared locally. READ ONLY.
The scratch stage holds symlinks app/ and lib/ to the installed folders (no copy) and the test account's ref (mode 600); it is removed after.
  python ap38_pagehash.py <out.json>        -> RUNNER (repository root): uploads this file, ap38_measure.py and the guard; runs once over SSM
  python ap38_pagehash.py --driver          -> HOST DRIVER (runs no gateway code; spawns the guarded children of ap38_measure.py)
The output is hash-bearing: the caller keeps it untracked (git-excluded); only equality and counts go into a record."""
from __future__ import annotations

import io
import json
import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ap38_measure as m  # noqa: E402


def child(args):
    cmd = ["systemd-run", "--scope", "--quiet", "-p", "MemoryMax=1400M", "-p", "MemoryHigh=1100M", "-p", "MemorySwapMax=0", "--", m.PY, m.GUARD, "--cgroup", "120", "/tmp/ap38_measure.py"] + args
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=200)
    lines = [ln for ln in p.stdout.splitlines() if ln.startswith("AP38_RESULT ")]
    res = json.loads(lines[-1].split(" ", 1)[1]) if lines else {"no_result": True, "stderr_tail": p.stderr[-300:], "stdout_tail": p.stdout[-200:]}
    res["exit_code"] = p.returncode
    return res


def driver():
    stage = "/tmp/ap38_ph_%d" % os.getpid()
    out = {"guard": m.CGROUP_GUARD_NAME, "scratch_removed": False}
    try:
        os.makedirs(stage, mode=0o700)
        os.symlink("/opt/opal-gateway/app", stage + "/app")
        os.symlink("/opt/opal-gateway/lib", stage + "/lib")
        r = child(["--resolve", stage])
        out["ref_resolved"] = r.get("ref_resolved") is True
        if not out["ref_resolved"]:
            out["fatal"] = json.dumps(r)[:300]
            return out
        c = child(["--chain", stage, "2"])
        out["pages"] = [{k: p.get(k) for k in ("page", "rows", "sha", "used", "next", "wall_s", "rss_mb")} for p in (c.get("pages") or [])]
        out["stop"], out["vm_hwm_mb"], out["host_peak_pct"], out["exit_code"] = c.get("stop"), c.get("vm_hwm_mb"), c.get("host_peak_pct"), c.get("exit_code")
    finally:
        shutil.rmtree(stage, ignore_errors=True)
        out["scratch_removed"] = not os.path.exists(stage)
    return out


def runner(outp):
    import boto3
    here = os.path.dirname(os.path.abspath(__file__))
    s3 = boto3.client("s3")
    for n in ("ap38_pagehash.py", "ap38_measure.py", "ap38_guard.py"):
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/" + n, Body=io.open(os.path.join(here, n), "rb").read())
    pulls = " && ".join("aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (m.BUCKET, n, n) for n in ("ap38_pagehash.py", "ap38_measure.py", "ap38_guard.py"))
    cmd = "cd /opt/opal-gateway && rm -f /tmp/ap38_pagehash.py /tmp/ap38_measure.py /tmp/ap38_guard.py && %s && %s /tmp/ap38_pagehash.py --driver" % (pulls, m.PY)
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[m.INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=600)["Command"]["CommandId"]
    inv = None
    for _ in range(150):
        time.sleep(4)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=m.INSTANCE)
        except Exception:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    if "AP38_PH_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("AP38_PH_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    doc["captured_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps({"pages": len(doc.get("pages") or []), "rows": [p["rows"] for p in doc.get("pages") or []], "scratch_removed": doc.get("scratch_removed"), "stop": doc.get("stop"), "host_peak_pct": doc.get("host_peak_pct")}))


if __name__ == "__main__":
    if "--driver" in sys.argv:
        print("AP38_PH_JSON")
        try:
            print(json.dumps(driver(), separators=(",", ":"), default=str))
        except Exception:
            import traceback
            print(json.dumps({"fatal": traceback.format_exc()[-800:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1])
