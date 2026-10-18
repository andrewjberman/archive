#!/usr/bin/env python
"""OG-ap-44 Phase A step 3: exercise the CANDIDATE's make_server (OG-pr-5, the logger snapshot and restore) on the gateway host, in a FRESH process under the cgroup hard guard (from ap42_pins.py).
In ONE process: the service-style uvicorn.Config is built (as `uvicorn app.server:app --workers 1` builds it: the default log config, the access log on), a capturing handler is attached to uvicorn.access, the four loggers
(uvicorn, uvicorn.error, uvicorn.access, uvicorn.asgi) are snapshotted (level, handler objects, propagate, disabled, filters), then the LIVE ref's make_server (the regression reproduced) and the CANDIDATE's make_server are
called in turn on a fresh service-style state and the snapshots compared; the restore is shown on a raising Config; the listener binds loopback on a TEST port and answers 403 unarmed. The running service is NOT touched and
NO SSM PARAMETER IS WRITTEN. Counts, booleans and fixed words only.
  python ap44_loggers.py <out.json> <expect.json>   -> RUNNER (repository root)
  python ap44_loggers.py --driver | --loggers <stage>"""
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

CAND = {"probe_listener.py": "app/probe_listener.py"}
S3_PREFIX = "ec2/opal-gateway/ap44_cand/"
PORT = 18099                   # a TEST port: the running service holds 8099 (the live listener)
LEASE_MIN = 45


def parse_rss_mb(line, key):
    for tok in line.split():
        if tok.startswith(key + "="):
            digits = "".join(ch for ch in tok.split("=", 1)[1] if ch.isdigit())
            return round(int(digits) / 1024.0, 1) if digits else None
    return None


# ----------------------------------------------------------------------------------------------------- the child: the uvicorn loggers
def child_loggers(stage):
    m.load_env(stage)
    import asyncio
    import importlib.util
    import logging
    import urllib.error
    import urllib.request

    import uvicorn
    from starlette.applications import Starlette

    names = ("uvicorn", "uvicorn.error", "uvicorn.access", "uvicorn.asgi")

    def snap():
        out = {}
        for n in names:
            lg = logging.getLogger(n)
            out[n] = {"level": lg.level, "handlers": [id(h) for h in lg.handlers], "handler_types": [type(h).__name__ for h in lg.handlers], "propagate": lg.propagate,
                      "disabled": lg.disabled, "filters": [id(f) for f in lg.filters]}
        return out

    captured = []

    class Cap(logging.Handler):
        def emit(self, record):
            captured.append((record.name, record.getMessage()))

    cap = Cap()

    def service_style():
        # the service is started as `uvicorn app.server:app --host 0.0.0.0 --port 8080 --workers 1` (the unit's ExecStart): the default log config, the access log on
        uvicorn.Config(Starlette(), host="0.0.0.0", port=8080, workers=1)
        for n in ("uvicorn.access",):
            lg = logging.getLogger(n)
            if cap in lg.handlers:
                lg.removeHandler(cap)
            lg.addHandler(cap)

    def load(modname, path):
        spec = importlib.util.spec_from_file_location("app." + modname, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["app." + modname] = mod
        spec.loader.exec_module(mod)
        return mod

    cand = load("probe_listener_candidate", os.path.join(stage, "app", "probe_listener.py"))
    live = load("probe_listener_live", "/opt/opal-gateway/app/probe_listener.py")
    out = {"uvicorn_version": uvicorn.__version__}

    # 1. the LIVE ref's make_server, the regression reproduced
    service_style()
    before = snap()
    live.make_server(port=0)
    after = snap()
    captured.clear()
    logging.getLogger("uvicorn.access").info('127.0.0.1:1 - "POST /mcp HTTP/1.1" 200')
    out["live_ref"] = {"loggers_unchanged": before == after, "access_record_reaches_handler": any(c[0] == "uvicorn.access" for c in captured),
                       "access_handlers_before": before["uvicorn.access"]["handler_types"], "access_handlers_after": after["uvicorn.access"]["handler_types"],
                       "access_level_before": logging.getLevelName(before["uvicorn.access"]["level"]), "access_level_after": logging.getLevelName(after["uvicorn.access"]["level"])}

    # 2. the CANDIDATE's make_server
    service_style()
    before = snap()
    server = cand.make_server(port=0)
    after = snap()
    captured.clear()
    logging.getLogger("uvicorn.access").info('127.0.0.1:1 - "POST /mcp HTTP/1.1" 200')
    reached = any(c[0] == "uvicorn.access" for c in captured)
    out["candidate"] = {"loggers_unchanged": before == after, "changed_loggers": [n for n in names if before[n] != after[n]], "access_record_reaches_handler": reached,
                        "access_handlers": after["uvicorn.access"]["handler_types"], "access_level": logging.getLevelName(after["uvicorn.access"]["level"]),
                        "listener_access_log": bool(server.config.access_log), "listener_host": server.config.host}

    # 3. the restore runs when the Config raises: the real Config mutates the loggers, then raises
    service_style()
    s1 = snap()
    real_cfg = uvicorn.Config
    bare = None

    def boom(*a, **k):
        real_cfg(*a, **k)
        raise RuntimeError("boom")

    uvicorn.Config = boom
    raised = False
    try:
        cand.make_server(port=0)
    except RuntimeError:
        raised = True
    finally:
        uvicorn.Config = real_cfg
    s2 = snap()
    real_cfg(Starlette(), host="127.0.0.1", port=0, log_level="warning", access_log=False, lifespan="off")      # the same Config WITHOUT the candidate's restore
    bare = snap()
    out["candidate_on_raise"] = {"raised": raised, "loggers_unchanged": s1 == s2, "unrestored_config_would_have_changed": s1 != bare}
    service_style()

    # 4. the listener still serves nothing unarmed, binds loopback, and its INFO startup lines now reach the journal handler (a stated consequence)
    err_lines = []

    class ErrCap(logging.Handler):
        def emit(self, record):
            err_lines.append(record.getMessage()[:80])

    errcap = ErrCap()
    logging.getLogger("uvicorn.error").addHandler(errcap)
    cand.reset_lease_cache()
    cand.LEASE_READER = lambda: None

    def post_sync():
        req = urllib.request.Request("http://127.0.0.1:%d/probe/etfs_compare_peers" % PORT, data=b"{}", method="POST", headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            return exc.code, json.loads(exc.read().decode("utf-8") or "{}")
        except Exception as exc:
            return -1, {"error": "connection:" + type(exc).__name__}

    async def serve():
        task = cand.start(PORT)
        for _ in range(200):
            if getattr(cand._state.get("server"), "started", False):
                break
            await asyncio.sleep(0.05)
        started = bool(getattr(cand._state.get("server"), "started", False))
        ss = subprocess.run(["ss", "-ltn"], capture_output=True, text=True).stdout
        rows = [ln.split() for ln in ss.splitlines() if (":%d " % PORT) in (ln + " ")]
        bound = sorted({r[3].rsplit(":", 1)[0] for r in rows if len(r) > 3})
        status, body = await asyncio.get_running_loop().run_in_executor(None, post_sync)
        access_before_stop = len([c for c in captured if c[0] == "uvicorn.access"])
        cand._state["server"].should_exit = True
        await cand.stop(task)
        return {"started": started, "bound": bound, "unarmed_status": status, "unarmed_error": body.get("error"), "listener_access_lines_in_handler": access_before_stop}

    captured.clear()
    out["listener_run"] = asyncio.run(serve())
    logging.getLogger("uvicorn.error").removeHandler(errcap)
    out["listener_run"]["info_startup_lines"] = [ln for ln in err_lines if ln.startswith(("Started server process", "Uvicorn running on", "Waiting for application", "Application startup"))]
    out["audit_records"] = 0
    out["vm_hwm_mb"] = round(m.hwm_mb(), 1)
    m.emit(out)


# ----------------------------------------------------------------------------------------------------- host driver
def read_pid():
    rc, out = m.sh("systemctl show opal-gateway -p MainPID -p NRestarts")
    kv = dict(ln.split("=", 1) for ln in out.splitlines() if "=" in ln)
    return kv.get("MainPID"), kv.get("NRestarts")


def run_child(flag, stage):
    cmd = ["systemd-run", "--scope", "--quiet", "-p", "MemoryMax=1400M", "-p", "MemoryHigh=1100M", "-p", "MemorySwapMax=0", "--", m.PY, m.GUARD, "--cgroup", "120",
           os.path.abspath(__file__), flag, stage]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=200)
    lines = [ln for ln in p.stdout.splitlines() if ln.startswith("AP38_RESULT ")]
    res = json.loads(lines[-1].split(" ", 1)[1]) if lines else {"no_result": True, "stdout_tail": p.stdout[-300:], "stderr_tail": p.stderr[-400:]}
    res["exit_code"] = p.returncode
    return res


def driver():
    import hashlib
    expect = json.load(open("/tmp/ap44_expect.json"))
    stage = "/tmp/ap44_stage_%d" % os.getpid()
    out = {"guard": m.CGROUP_GUARD_NAME, "scratch_removed": False}
    try:
        pid0, nr0 = read_pid()
        os.makedirs(stage, mode=0o700)
        shutil.copytree("/opt/opal-gateway/app", stage + "/app", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        shutil.copytree("/opt/opal-gateway/lib", stage + "/lib", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        got = {}
        for name, rel in CAND.items():
            shutil.copyfile("/tmp/ap44_cand_" + name, os.path.join(stage, rel))
            got[name] = hashlib.sha256(open(os.path.join(stage, rel), "rb").read()).hexdigest()
        out["candidate_bytes_equal_release"] = {n: got[n] == expect[n] for n in CAND}
        if not all(out["candidate_bytes_equal_release"].values()):
            out["stop"] = "candidate bytes differ from the release blobs"
            return out
        out["pct_before"] = m.host_pct()
        out["loggers"] = run_child("--loggers", stage)
        out["pct_after"] = m.host_pct()
        pid1, nr1 = read_pid()
        out["service"] = {"pid_before": pid0, "pid_after": pid1, "pid_stable": pid0 == pid1, "nrestarts_before": nr0, "nrestarts_after": nr1}
        rc, ssout = m.sh("ss -ltn")
        out["port_free_after"] = (":%d " % PORT) not in (ssout + " ")
    finally:
        shutil.rmtree(stage, ignore_errors=True)
        out["scratch_removed"] = not os.path.exists(stage)
    return out


def runner(outp, expect_path):
    import boto3
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.getcwd()
    s3 = boto3.client("s3")
    expect = json.load(io.open(expect_path, encoding="utf-8"))
    for n in ("ap44_loggers.py", "ap38_measure.py", "ap38_guard.py"):
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/" + n, Body=io.open(os.path.join(here, n), "rb").read())
    gw = "C:/tmp/og-rel-batch11/infra/aws/ec2/opal-gateway/"
    for name, rel in CAND.items():
        s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + name, Body=io.open(gw + rel, "rb").read())
    s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + "expect.json", Body=json.dumps(expect).encode("utf-8"))
    pulls = ["aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (m.BUCKET, n, n) for n in ("ap44_loggers.py", "ap38_measure.py", "ap38_guard.py")]
    pulls += ["aws s3 cp s3://%s/%s%s /tmp/ap44_cand_%s --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX, n, n) for n in CAND]
    pulls += ["aws s3 cp s3://%s/%sexpect.json /tmp/ap44_expect.json --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX)]
    cmd = "cd /opt/opal-gateway && rm -f /tmp/ap44_loggers.py /tmp/ap38_measure.py /tmp/ap38_guard.py /tmp/ap44_cand_* /tmp/ap44_expect.json && %s && %s /tmp/ap44_loggers.py --driver" % (" && ".join(pulls), m.PY)
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
    if "AP44_LOGGERS_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("AP44_LOGGERS_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    doc["captured_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1))
    os.chdir(root)


if __name__ == "__main__":
    if "--loggers" in sys.argv:
        child_loggers(sys.argv[sys.argv.index("--loggers") + 1])
    elif "--driver" in sys.argv:
        print("AP44_LOGGERS_JSON")
        try:
            print(json.dumps(driver(), separators=(",", ":"), default=str))
        except Exception:
            import traceback
            print(json.dumps({"fatal": traceback.format_exc()[-800:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1], sys.argv[2])
