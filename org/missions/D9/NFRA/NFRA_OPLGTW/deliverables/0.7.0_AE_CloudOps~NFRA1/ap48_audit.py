#!/usr/bin/env python
"""OG-ap-48 Phase A step 3: the audit lake leg, measured on the gateway host in a FRESH process under the cgroup hard guard. READ-ONLY on AWS (no S3 write, no SSM write): the audit client is pointed at a NON-ROUTABLE endpoint
(AWS_ENDPOINT_URL_S3=http://10.255.255.1:9) with a throwaway bucket name, so the one put can only fail; the real audit lake is never touched and the running service is not touched. For the CANDIDATE's app/audit.py and, as a
disclosure, the LIVE ref's: build the S3 client through audit._emit (ONE call with a small record), read the client's configuration (connect_timeout, read_timeout, retries), the wall time of the failed put, the failure
counter (candidate only), the stderr lines written, and the local floor file's line count. The live ref's default Config is 60 s connect with legacy retries, so its run has a 70 s wall limit and a timeout is reported as such.
  python ap48_audit.py <out.json> <expect.json>     -> RUNNER (repository root)
  python ap48_audit.py --driver | --audit <stage> <which>"""
from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ap38_measure as m  # noqa: E402

S3_PREFIX = "ec2/opal-gateway/ap48_cand/"
BLACK_HOLE = "http://10.255.255.1:9"
THROWAWAY_BUCKET = "ap48-throwaway-no-such-bucket"
LIVE_WALL_LIMIT_S = 70.0


# ----------------------------------------------------------------------------------------------------- the child: one failed put
def child_audit(stage, which):
    os.environ["AUDIT_S3_BUCKET"] = THROWAWAY_BUCKET                       # set BEFORE the service's .env is loaded (setdefault) and before app.config is imported
    os.environ["AUDIT_PATH"] = os.path.join(stage, "floor.jsonl")
    os.environ["AWS_ENDPOINT_URL_S3"] = BLACK_HOLE
    m.load_env(stage)
    import datetime
    import threading
    buf = io.StringIO()
    real_err = sys.stderr
    sys.stderr = buf
    try:
        import boto3
        attempts = [0]
        real_client = boto3.client

        def counting_client(*a, **k):
            c = real_client(*a, **k)
            c.meta.events.register("before-send.s3.PutObject", lambda **kw: attempts.__setitem__(0, attempts[0] + 1))
            return c
        boto3.client = counting_client
        from app import audit
        rec = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(), "event": "ap48_black_hole_probe", "outcome": "n/a"}
        result = {}

        def go():
            t0 = time.monotonic()
            try:
                audit._emit(rec)
            finally:
                result["wall"] = time.monotonic() - t0
        th = threading.Thread(target=go, daemon=True)
        t0 = time.monotonic()
        th.start()
        th.join(LIVE_WALL_LIMIT_S if which == "live" else 30.0)
        finished = not th.is_alive()
        wall = round(result.get("wall", time.monotonic() - t0), 2)
        cfg = audit._s3_client.meta.config if audit._s3_client is not None else None
        retries = (getattr(cfg, "retries", None) or {}) if cfg is not None else {}
        counter = audit.lake_put_failure_count() if hasattr(audit, "lake_put_failure_count") else None
    finally:
        sys.stderr = real_err
    lines = [ln for ln in buf.getvalue().splitlines() if ln.strip()]
    floor = 0
    fp = os.environ["AUDIT_PATH"]
    if os.path.exists(fp):
        floor = sum(1 for ln in open(fp, encoding="utf-8") if ln.strip())
    out = {"which": which, "finished_within_limit": finished, "failed_put_wall_s": wall, "client_built": cfg is not None,
           "config": {"connect_timeout": getattr(cfg, "connect_timeout", None), "read_timeout": getattr(cfg, "read_timeout", None), "retries_as_read": {str(k): v for k, v in retries.items()}},
           "send_attempts_made": attempts[0],
           "counter_after_failure": counter, "stderr_lines": len(lines), "stderr_line_has_warn_prefix": all("audit-lake WARN" in ln for ln in lines) if lines else None,
           "stderr_line_carries_only_class_and_count": (all(("count=" in ln and "bucket" not in ln.lower() and THROWAWAY_BUCKET not in ln and "10.255" not in ln) for ln in lines) if lines else None),
           "floor_lines": floor, "floor_line_written": floor == 1, "vm_hwm_mb": round(m.hwm_mb(), 1)}
    m.emit(out)
    sys.stdout.flush()
    os._exit(0)                                                           # a daemon thread still blocked in the live ref's 60 s connect must not hold the process


# ----------------------------------------------------------------------------------------------------- host driver
def run_child(flag, stage, which):
    cmd = ["systemd-run", "--scope", "--quiet", "-p", "MemoryMax=1400M", "-p", "MemoryHigh=1100M", "-p", "MemorySwapMax=0", "--", m.PY, m.GUARD, "--cgroup", "120",
           os.path.abspath(__file__), flag, stage, which]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
    lines = [ln for ln in p.stdout.splitlines() if ln.startswith("AP38_RESULT ")]
    res = json.loads(lines[-1].split(" ", 1)[1]) if lines else {"no_result": True, "stdout_tail": p.stdout[-300:], "stderr_tail": p.stderr[-400:]}
    res["exit_code"] = p.returncode
    return res


def read_pid():
    rc, out = m.sh("systemctl show opal-gateway -p MainPID -p NRestarts")
    kv = dict(ln.split("=", 1) for ln in out.splitlines() if "=" in ln)
    return kv.get("MainPID"), kv.get("NRestarts")


def driver():
    expect = json.load(open("/tmp/ap48_expect.json"))
    out = {"guard": m.CGROUP_GUARD_NAME, "scratch_removed": False}
    stages = ["/tmp/ap48_stage_c_%d" % os.getpid(), "/tmp/ap48_stage_l_%d" % os.getpid()]
    try:
        pid0, nr0 = read_pid()
        for st in stages:
            os.makedirs(st, mode=0o700)
            shutil.copytree("/opt/opal-gateway/app", st + "/app", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            shutil.copytree("/opt/opal-gateway/lib", st + "/lib", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        shutil.copyfile("/tmp/ap48_cand_audit.py", stages[0] + "/app/audit.py")
        got = hashlib.sha256(open(stages[0] + "/app/audit.py", "rb").read()).hexdigest()
        out["candidate_bytes_equal_release"] = {"audit.py": got == expect["audit.py"]}
        out["live_stage_audit_equals_host_audit"] = hashlib.sha256(open(stages[1] + "/app/audit.py", "rb").read()).hexdigest() == hashlib.sha256(open("/opt/opal-gateway/app/audit.py", "rb").read()).hexdigest()
        if not out["candidate_bytes_equal_release"]["audit.py"]:
            out["stop"] = "candidate bytes differ from the release blob"
            return out
        out["pct_before"] = m.host_pct()
        out["candidate"] = run_child("--audit", stages[0], "candidate")
        out["pct_mid"] = m.host_pct()
        out["live"] = run_child("--audit", stages[1], "live")
        out["pct_after"] = m.host_pct()
        pid1, nr1 = read_pid()
        out["service"] = {"pid_before": pid0, "pid_after": pid1, "pid_stable": pid0 == pid1, "nrestarts_before": nr0, "nrestarts_after": nr1}
    finally:
        for st in stages:
            shutil.rmtree(st, ignore_errors=True)
        out["scratch_removed"] = not any(os.path.exists(s) for s in stages)
    return out


def runner(outp, expect_path):
    import boto3
    here = os.path.dirname(os.path.abspath(__file__))
    s3 = boto3.client("s3")
    expect = json.load(io.open(expect_path, encoding="utf-8"))
    for n in ("ap48_audit.py", "ap38_measure.py", "ap38_guard.py"):
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/" + n, Body=io.open(os.path.join(here, n), "rb").read())
    gw = "C:/tmp/og-rel-batch13/infra/aws/ec2/opal-gateway/"
    s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + "audit.py", Body=io.open(gw + "app/audit.py", "rb").read())
    s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + "expect.json", Body=json.dumps(expect).encode("utf-8"))
    pulls = ["aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (m.BUCKET, n, n) for n in ("ap48_audit.py", "ap38_measure.py", "ap38_guard.py")]
    pulls += ["aws s3 cp s3://%s/%saudit.py /tmp/ap48_cand_audit.py --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX), "aws s3 cp s3://%s/%sexpect.json /tmp/ap48_expect.json --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX)]
    cmd = "cd /opt/opal-gateway && rm -f /tmp/ap48_audit.py /tmp/ap38_measure.py /tmp/ap38_guard.py /tmp/ap48_cand_audit.py /tmp/ap48_expect.json && %s && %s /tmp/ap48_audit.py --driver" % (" && ".join(pulls), m.PY)
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
    if "AP48_AUDIT_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("AP48_AUDIT_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    doc["captured_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1))


if __name__ == "__main__":
    if "--audit" in sys.argv:
        i = sys.argv.index("--audit")
        child_audit(sys.argv[i + 1], sys.argv[i + 2])
    elif "--driver" in sys.argv:
        print("AP48_AUDIT_JSON")
        try:
            print(json.dumps(driver(), separators=(",", ":"), default=str))
        except Exception:
            import traceback
            print(json.dumps({"fatal": traceback.format_exc()[-800:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1], sys.argv[2])
