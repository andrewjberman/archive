#!/usr/bin/env python
"""OG-ls-1 Phase B step 4 (a copy of ap50_driven.py with the OG-ls-1 names and the batch15 tree for the staged deploy script): THE ONE DRIVEN READ (FWD-20 proof). ONE fresh process under the cgroup HARD GUARD (oom_score_adj_1000_cgroup_memmax_1400mb), from a SCRATCH copy of the DEPLOYED tree (/opt/opal-gateway/app and lib,
copied; each copied file is compared with the deployed file), as the gateway instance role: app.family_depth.read() called ONCE. The release's byte-equal deploy-to-ec2.sh is staged in the SCRATCH tree only, NEVER in /opt/opal-gateway
(COO ruling on row Z-S406, condition G7); the scratch tree is removed after. READ-ONLY: every boto3 operation is counted by name and any not starting Get, List, Describe or Head is a write attempt (expected 0).
The record holds COUNTS and, for ONE chosen family, its schedule expression and two dates; no ARN, account number, principal or error text is kept.
  python ls1_driven.py <out.json> <expect.json>     -> RUNNER (repository root)
  python ls1_driven.py --driver | --read <stage>"""
from __future__ import annotations

import collections
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ap38_measure as m  # noqa: E402

S3_PREFIX = "ec2/opal-gateway/ls1_cand/"
READ_WALL_S = 100.0


def _leaves(obj, out):
    if isinstance(obj, dict):
        if "claim" in obj and "value" in obj:
            out.append(obj)
        else:
            for v in obj.values():
                _leaves(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _leaves(v, out)


def child_read(stage):
    m.load_env(stage)
    import boto3
    ident = boto3.client("sts", region_name="us-east-1").get_caller_identity()["Arn"]
    role = ident.split(":", 5)[-1]
    ops = collections.Counter()
    real_client = boto3.client

    def counting(*a, **k):
        c = real_client(*a, **k)
        svc = c.meta.service_model.service_name
        c.meta.events.register("before-call.*.*", lambda model=None, **kw: ops.update([svc + ":" + model.name]))
        return c
    boto3.client = counting
    from app import family_depth
    res = {}

    def go():
        t0 = time.monotonic()
        try:
            res["doc"] = family_depth.read()
        except BaseException as exc:  # noqa: BLE001
            res["error"] = type(exc).__name__
        res["wall"] = time.monotonic() - t0
    th = threading.Thread(target=go, daemon=True)
    t0 = time.monotonic()
    th.start()
    th.join(READ_WALL_S)
    out = {"finished_within_wall_guard": not th.is_alive(), "wall_s": round(res.get("wall", time.monotonic() - t0), 2), "peak_rss_mb": round(m.hwm_mb(), 1),
           "identity_is_instance_role": role.startswith("assumed-role/opal-gateway-role/"), "read_calls_made": 1}
    if "error" in res:
        out["error"] = res["error"]
    doc = res.get("doc")
    if doc:
        leaves = []
        _leaves(doc, leaves)
        cl = {"measured": 0, "inferred": 0, "absent": 0}
        claimless = absent_reason = 0
        for lf in leaves:
            c = lf.get("claim")
            if c in cl:
                cl[c] += 1
            else:
                claimless += 1
            if c == "absent" and isinstance(lf.get("source"), str) and lf["source"].strip():
                absent_reason += 1
        rows = doc.get("families", [])
        out.update({"families": len(rows), "denominator": doc.get("denominator"), "values_total": len(leaves), "claims": cl, "claim_less_values": claimless, "absent_with_reason": absent_reason})
        cands = []
        for r in sorted((r for r in rows if r.get("family")), key=lambda r: r["family"]):
            d = r.get("depth") or {}
            keys = d.get("backfill_status_keys") or []
            sc, fr, er = r.get("schedule") or {}, d.get("backfill_frontier") or {}, d.get("earliest_served_date") or {}
            if sc.get("claim") == "measured" and fr.get("claim") == "measured" and er.get("claim") == "measured" and len(keys) == 1:
                mt = re.match(r"s3://([^/]+)/([^/]+)/([^/]+)/meta/backfill-status\.json$", keys[0])
                if mt:
                    cands.append({"family": r["family"], "bucket": mt.group(1), "source": mt.group(2), "scope": mt.group(3), "schedule": sc.get("value"), "frontier": fr.get("value"), "earliest": er.get("value")})
        seen, uniq = set(), []
        for c in cands:
            if c["family"] not in seen:
                seen.add(c["family"])
                uniq.append(c)
        out["single_key_measured_family_candidates"] = len(uniq)
        out["chosen"] = uniq[0] if uniq else None
    out["boto3_operations"] = dict(sorted(ops.items()))
    out["writes_attempted"] = sum(n for k, n in ops.items() if not k.split(":", 1)[1].startswith(("Get", "List", "Describe", "Head")))
    m.emit(out)
    sys.stdout.flush()
    os._exit(0)


def run_child(args, wall=120):
    cmd = ["systemd-run", "--scope", "--quiet", "-p", "MemoryMax=1400M", "-p", "MemoryHigh=1100M", "-p", "MemorySwapMax=0", "--", m.PY, m.GUARD, "--cgroup", str(wall), os.path.abspath(__file__)] + args
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=wall + 60)
    lines = [ln for ln in p.stdout.splitlines() if ln.startswith("AP38_RESULT ")]
    res = json.loads(lines[-1].split(" ", 1)[1]) if lines else {"no_result": True, "stdout_tail": p.stdout[-300:], "stderr_tail": p.stderr[-400:]}
    res["exit_code"] = p.returncode
    return res


def tree_hashes(root):
    h = {}
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d != "__pycache__"]
        for f in fn:
            if not f.endswith(".pyc"):
                p = os.path.join(dp, f)
                h[os.path.relpath(p, root)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def driver():
    expect = json.load(open("/tmp/ls1_expect.json"))
    out = {"guard": m.CGROUP_GUARD_NAME, "scratch_removed": False}
    stage = "/tmp/ls1_drive_%d" % os.getpid()
    try:
        out["marker"] = open("/opt/opal-gateway/.deployed_commit").read().strip()
        out["marker_equals_release_sha"] = out["marker"] == expect["release_sha"]
        out["deploy_script_absent_from_opt"] = not os.path.exists("/opt/opal-gateway/deploy-to-ec2.sh")
        os.makedirs(stage, mode=0o700)
        shutil.copytree("/opt/opal-gateway/app", stage + "/app", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        shutil.copytree("/opt/opal-gateway/lib", stage + "/lib", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        out["scratch_app_equals_deployed_app"] = tree_hashes(stage + "/app") == tree_hashes("/opt/opal-gateway/app")
        shutil.copyfile("/tmp/ls1_deploy_to_ec2.sh", stage + "/deploy-to-ec2.sh")
        out["staged_deploy_script_equals_release_blob"] = hashlib.sha256(open(stage + "/deploy-to-ec2.sh", "rb").read()).hexdigest() == expect["deploy-to-ec2.sh"]
        out["deploy_script_still_absent_from_opt_after_staging"] = not os.path.exists("/opt/opal-gateway/deploy-to-ec2.sh")
        out["pct_before"] = m.host_pct()
        if out["pct_before"] >= m.STOP_PCT or not out["marker_equals_release_sha"] or not out["scratch_app_equals_deployed_app"] or not out["staged_deploy_script_equals_release_blob"]:
            out["stop"] = "precondition failed"
            return out
        out["read"] = run_child(["--read", stage])
        out["pct_after"] = m.host_pct()
    finally:
        shutil.rmtree(stage, ignore_errors=True)
        out["scratch_removed"] = not os.path.exists(stage)
    return out


def runner(outp, expect_path):
    import boto3
    here = os.path.dirname(os.path.abspath(__file__))
    s3 = boto3.client("s3")
    expect = json.load(io.open(expect_path, encoding="utf-8"))
    for n in ("ls1_driven.py", "ap38_measure.py", "ap38_guard.py"):
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/" + n, Body=io.open(os.path.join(here, n), "rb").read())
    ds = io.open("C:/tmp/og-rel-batch15/infra/aws/ec2/opal-gateway/deploy-to-ec2.sh", "rb").read()
    expect["deploy-to-ec2.sh"] = hashlib.sha256(ds).hexdigest()
    s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + "deploy-to-ec2.sh", Body=ds)
    s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + "expect_drv.json", Body=json.dumps(expect).encode("utf-8"))
    pulls = ["aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (m.BUCKET, n, n) for n in ("ls1_driven.py", "ap38_measure.py", "ap38_guard.py")]
    pulls += ["aws s3 cp s3://%s/%sdeploy-to-ec2.sh /tmp/ls1_deploy_to_ec2.sh --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX), "aws s3 cp s3://%s/%sexpect_drv.json /tmp/ls1_expect.json --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX)]
    cmd = ("cd /opt/opal-gateway && rm -f /tmp/ls1_driven.py /tmp/ls1_deploy_to_ec2.sh /tmp/ls1_expect.json && %s && %s /tmp/ls1_driven.py --driver; rc=$?; rm -f /tmp/ls1_deploy_to_ec2.sh /tmp/ls1_expect.json; exit $rc"
           % (" && ".join(pulls), m.PY))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[m.INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=900)["Command"]["CommandId"]
    inv = None
    for _ in range(220):
        time.sleep(4)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=m.INSTANCE)
        except Exception:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    if "LS1_DRIVEN_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("LS1_DRIVEN_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    doc["captured_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps({k: v for k, v in doc.items()}, indent=1))


if __name__ == "__main__":
    if "--read" in sys.argv:
        child_read(sys.argv[sys.argv.index("--read") + 1])
    elif "--driver" in sys.argv:
        print("LS1_DRIVEN_JSON")
        try:
            print(json.dumps(driver(), separators=(",", ":"), default=str))
        except Exception:
            import traceback
            print(json.dumps({"fatal": traceback.format_exc()[-800:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1], sys.argv[2])
