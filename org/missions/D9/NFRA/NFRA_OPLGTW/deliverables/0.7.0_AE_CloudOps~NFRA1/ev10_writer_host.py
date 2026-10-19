#!/usr/bin/env python
"""OG-ev-10 STEP 2 (amendment A1): the HOST side of the ONE-OBJECT WRITER TEST. Runs under the service's venv python; imports NO gateway code except in the guarded fresh-process child (--writer), which runs under the
cgroup hard guard. Counts, status words and the one lake key only: no row content beyond field names is printed.
  python ev10_writer_host.py state     -> the service PID, NRestarts, host memory percent, whether AUDIT_S3_BUCKET is a key of the service's .env (the value is never printed) and equals the lake bucket the runner names
  python ev10_writer_host.py writer    -> ONE guarded fresh process: ratelimit.record_identity_refusal(<synthetic key>) with audit's own S3 client wrapped in a recording shim (the key, returned or raised by class name),
                                          the object READ BACK by key, the module's failure counter read. The object is never deleted."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ap40_probe_host as ph  # noqa: E402

SYNTH_KEY = "OG-ev-10/00000000-0000-4000-8000-00000000e10a"
BUCKET_EXPECT = "opal-mcp-audit"
HOST_STOP_PCT = 75.0
GUARD = ph.GUARD
PY = ph.PY


def env_bucket():
    got = None
    for ln in open("/opt/opal-gateway/.env", encoding="utf-8", errors="replace"):
        if ln.startswith("AUDIT_S3_BUCKET="):
            got = ln.rstrip("\n").split("=", 1)[1].strip().strip('"').strip("'")
    return got


def mode_state():
    import ap38_measure as m
    pid, nr = ph.service()
    b = env_bucket()
    return {"pid": pid, "nrestarts": nr, "host_pct": round(m.host_pct(), 1), "audit_bucket_is_set": bool(b), "audit_bucket_equals_lake_bucket": b == BUCKET_EXPECT}


def run_child(flag, stage):
    cmd = ["systemd-run", "--scope", "--quiet", "-p", "MemoryMax=1400M", "-p", "MemoryHigh=1100M", "-p", "MemorySwapMax=0", "--", PY, GUARD, "--cgroup", "120", os.path.abspath(__file__), flag, stage]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=200, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    lines = [ln for ln in p.stdout.splitlines() if ln.startswith("AP38_RESULT ")]
    res = json.loads(lines[-1].split(" ", 1)[1]) if lines else {"no_result": True, "stderr_tail": p.stderr[-300:]}
    res["exit_code"] = p.returncode
    return res


def mode_writer():
    stage = "/tmp/ev10_stage_%d" % os.getpid()
    out = {"guard": "oom_score_adj_1000_cgroup_memmax_1400mb", "scratch_removed": False}
    try:
        os.makedirs(stage, mode=0o700)
        os.symlink("/opt/opal-gateway/app", stage + "/app")
        os.symlink("/opt/opal-gateway/lib", stage + "/lib")
        out["writer"] = run_child("--writer", stage)
    finally:
        shutil.rmtree(stage, ignore_errors=True)
        out["scratch_removed"] = not os.path.exists(stage)
    return out


def child_writer(stage):
    import ap38_measure as m
    os.environ["AUDIT_PATH"] = os.path.join(stage, "audit_scratch.jsonl")          # the local floor of THIS process only; set before the service's .env is loaded
    m.load_env(stage)
    import boto3
    from app import audit, ratelimit

    class Recorder:
        """Records the key and whether put_object returned or raised (the class name only); passes every call through unchanged."""
        def __init__(self, real):
            self.real = real
            self.key = None
            self.put_returned = False
            self.put_error_class = None

        def put_object(self, **kw):
            self.key = kw.get("Key")
            try:
                resp = self.real.put_object(**kw)
                self.put_returned = True
                return resp
            except Exception as exc:
                self.put_error_class = type(exc).__name__
                raise

    bucket = audit._cfg.AUDIT_S3_BUCKET
    real = boto3.client("s3", region_name=audit._cfg.AWS_REGION)
    rec = Recorder(real)
    audit._s3_client = rec
    ratelimit.record_identity_refusal(SYNTH_KEY, 60, {"count": 121, "clients": {"none": 121}})
    out = {"bucket_set": bool(bucket), "key_printed": rec.key, "written": bool(rec.put_returned), "put_error_class": rec.put_error_class, "audit_failure_count_after": ratelimit.audit_failure_count(),
           "read_back": False, "rows_in_object": None, "event_is_gw_ratelimit": None, "principal_is_synthetic": None, "field_names": None}
    if rec.put_returned and rec.key:
        try:
            body = real.get_object(Bucket=bucket, Key=rec.key)["Body"].read().decode("utf-8", "replace")
            rows = [json.loads(ln) for ln in body.splitlines() if ln.strip()]
            out["rows_in_object"] = len(rows)
            out["read_back"] = len(rows) == 1
            if rows:
                out["event_is_gw_ratelimit"] = rows[0].get("event") == "gw_ratelimit"
                out["principal_is_synthetic"] = str(rows[0].get("principal", "")).startswith("OG-ev-10/")
                out["field_names"] = sorted(rows[0].keys())
        except Exception as exc:
            out["read_back_error_class"] = type(exc).__name__
    local = audit._cfg.AUDIT_PATH
    out["local_floor_is_scratch"] = str(local).startswith(stage)
    out["vm_hwm_mb"] = round(m.hwm_mb(), 1)
    m.emit(out)


def main():
    a = sys.argv[1:]
    if a[0] == "--writer":
        return child_writer(a[1])
    out = mode_state() if a[0] == "state" else mode_writer()
    print("EV10_WRITER_JSON")
    print(json.dumps(out, separators=(",", ":"), default=str))
    return None


if __name__ == "__main__":
    main()
