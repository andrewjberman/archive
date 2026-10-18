#!/usr/bin/env python
"""OG-ap-38 Phase B, arm e13 and the `peers_through_service` field (C16): THE INSTALLED CODE answers etfs_compare_peers("IDVZ","x","y") BOUNDED, and a valid pair (the first period and axis it lists) answers rows, each in a FRESH process under the
hard guard oom_score_adj_1000_rlimit_as_1400mb. The scratch stage holds symlinks app/ and lib/ to the installed folders (no copy); it is removed after. READ ONLY; counts, MB, seconds and words only.
  python ap38_installed.py <out.json>     -> RUNNER (repository root): uploads this file, ap38_measure.py and the guard; runs once over SSM
  python ap38_installed.py --driver       -> HOST DRIVER (runs no gateway code; spawns the guarded children of ap38_measure.py)
The service is NOT called: /mcp takes only a bearer signed by the gateway key, and no seat mints one; so the basis recorded is fresh_process."""
from __future__ import annotations

import io
import json
import os
import shutil
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ap38_measure as m  # noqa: E402


def driver():
    stage = "/tmp/ap38_inst_%d" % os.getpid()
    out = {"guard": m.GUARD_NAME, "scratch_removed": False}
    try:
        os.makedirs(stage, mode=0o700)
        os.symlink("/opt/opal-gateway/app", stage + "/app")
        os.symlink("/opt/opal-gateway/lib", stage + "/lib")
        a = m.guarded(["--peers", stage, "x", "y"])
        out["peers"] = {k: a.get(k) for k in ("outcome", "rows_matched", "wall_s", "vm_hwm_mb", "first_period", "first_axis", "periods_listed", "axes_listed", "exit_code", "guard_marker", "where")}
        if a.get("first_period") and a.get("first_axis"):
            b = m.guarded(["--peers", stage, str(a["first_period"]), str(a["first_axis"])])
            out["valid_pair"] = {k: b.get(k) for k in ("outcome", "rows_matched", "wall_s", "vm_hwm_mb", "exit_code")}
    finally:
        shutil.rmtree(stage, ignore_errors=True)
        out["scratch_removed"] = not os.path.exists(stage)
    return out


def runner(outp):
    import boto3
    here = os.path.dirname(os.path.abspath(__file__))
    s3 = boto3.client("s3")
    for n in ("ap38_installed.py", "ap38_measure.py", "ap38_guard.py"):
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/" + n, Body=io.open(os.path.join(here, n), "rb").read())
    pulls = " && ".join("aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (m.BUCKET, n, n) for n in ("ap38_installed.py", "ap38_measure.py", "ap38_guard.py"))
    cmd = "cd /opt/opal-gateway && rm -f /tmp/ap38_installed.py /tmp/ap38_measure.py /tmp/ap38_guard.py && %s && %s /tmp/ap38_installed.py --driver" % (pulls, m.PY)
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
    if "AP38_INST_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("AP38_INST_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    doc["captured_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1))


if __name__ == "__main__":
    if "--driver" in sys.argv:
        print("AP38_INST_JSON")
        try:
            print(json.dumps(driver(), separators=(",", ":"), default=str))
        except Exception:
            import traceback
            print(json.dumps({"fatal": traceback.format_exc()[-800:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1])
