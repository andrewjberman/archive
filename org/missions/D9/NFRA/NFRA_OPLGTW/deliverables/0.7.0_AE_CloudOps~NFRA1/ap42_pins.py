#!/usr/bin/env python
"""OG-ap-42 Phase A step 3: exercise the CANDIDATE pins on the gateway host, in a FRESH process under the cgroup hard guard, with a FAKE lease source (from ap40_listener.py).
The probe-lease FIRM PIN (OG-pr-4) and the GRAPH HOST PIN (OG-sec-2). The running service is NOT touched (its MainPID is read before and after) and NO SSM PARAMETER IS WRITTEN: the lease is an in-process fake.
The candidate is a scratch copy of the installed app/ and lib/ with the two modified release files laid over it (their sha256 are checked against the release blobs); the audit call is captured in memory.
The service holds 127.0.0.1:8099 now, so the scratch listener binds a TEST port. Counts, booleans and fixed words only.
  python ap42_pins.py <out.json> <expect.json>   -> RUNNER (repository root)
  python ap42_pins.py --driver | --resolve <stage> | --pins <stage>"""
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

CAND = {"probe_listener.py": "app/probe_listener.py", "graph.py": "app/graph.py"}
S3_PREFIX = "ec2/opal-gateway/ap42_cand/"
PORT = 18099                   # a TEST port: the running service holds 8099 (the live listener)
LEASE_MIN = 45


def parse_rss_mb(line, key):
    for tok in line.split():
        if tok.startswith(key + "="):
            digits = "".join(ch for ch in tok.split("=", 1)[1] if ch.isdigit())
            return round(int(digits) / 1024.0, 1) if digits else None
    return None


# ----------------------------------------------------------------------------------------------------- child 1: the test account's reference
def child_resolve(stage):
    cap = []
    real_emit = m.emit
    m.emit = cap.append
    try:
        m.child_resolve(stage)
    finally:
        m.emit = real_emit
    real_emit({"ref_resolved": bool(cap and cap[-1].get("ref_resolved"))})


# ----------------------------------------------------------------------------------------------------- child 2: the pins
def child_pins(stage):
    m.load_env(stage)
    import asyncio
    import datetime as dt
    import types
    import urllib.error
    import urllib.request
    from app import audit
    from app import graph as g
    from app import probe_listener as pl

    ref = open(os.path.join(stage, "ref.txt"), encoding="utf-8").read().strip()
    records = []
    audit.log_call = lambda *a, **k: records.append((a[1], a[3], str(a[4])))
    tool_calls = []
    real_tx = pl._cc.client_get_transactions

    def recorder(*a, **k):
        tool_calls.append(1)
        return real_tx(*a, **k)

    pl._cc.client_get_transactions = recorder
    lease = [None]
    pl.LEASE_READER = lambda: lease[0]

    def lease_obj(minutes=45):
        now = dt.datetime.now(dt.timezone.utc)
        return {"order": "OG-ap-42", "account_ref": ref, "set_at": now.isoformat(), "expires_at": (now + dt.timedelta(minutes=minutes)).isoformat()}

    def post_sync(tool, body):
        req = urllib.request.Request("http://127.0.0.1:%d/probe/%s" % (PORT, tool), data=json.dumps(body).encode("utf-8"), method="POST", headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=100) as r:
                return r.status, json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            try:
                return exc.code, json.loads(exc.read().decode("utf-8"))
            except Exception:
                return exc.code, {}
        except Exception as exc:
            return -1, {"error": "connection:" + type(exc).__name__}

    async def main():
        loop = asyncio.get_running_loop()
        out = {}
        task = pl.start(PORT)
        for _ in range(200):
            if getattr(pl._state.get("server"), "started", False):
                break
            await asyncio.sleep(0.05)
        out["listener_started"] = bool(getattr(pl._state.get("server"), "started", False))
        ss = subprocess.run(["ss", "-ltn"], capture_output=True, text=True).stdout
        rows = [ln.split() for ln in ss.splitlines() if (":%d " % PORT) in (ln + " ")]
        out["bound"] = sorted({r[3].rsplit(":", 1)[0] for r in rows if len(r) > 3})

        async def post(tool, body):
            return await loop.run_in_executor(None, post_sync, tool, body)

        today = dt.datetime.now(dt.timezone.utc).date()
        frm = (today - dt.timedelta(days=m.WINDOW_DAYS)).isoformat()
        tx = {"firm": m.FIRM, "account": ref, "platform": None, "from_date": frm, "to_date": today.isoformat()}
        # unarmed
        lease[0] = None
        pl.reset_lease_cache()
        s, b = await post("client_get_transactions", tx)
        out["unarmed"] = {"status": s, "error": b.get("error"), "tool_calls": len(tool_calls)}
        # armed WITH a firm
        body0 = lease_obj()
        body0["firm"] = m.FIRM
        lease[0] = json.dumps(body0)
        pl.reset_lease_cache()
        n0 = len(tool_calls)
        s, b = await post("client_get_transactions", tx)
        out["matched_firm"] = {"status": s, "error": b.get("error"), "rows": len(m.rows_of(b)), "tool_calls": len(tool_calls) - n0}
        n1 = len(tool_calls)
        mism = {}
        for label, firm in (("other_firm", "cottonwood"), ("firm_absent", None), ("firm_trailing_newline", m.FIRM + "\n"), ("firm_upper", m.FIRM.upper())):
            body = dict(tx)
            if firm is None:
                body.pop("firm")
            else:
                body["firm"] = firm
            s, b = await post("client_get_transactions", body)
            mism[label] = {"status": s, "error": b.get("error")}
        out["mismatched_firm"] = mism
        out["tool_calls_on_mismatch"] = len(tool_calls) - n1
        # a lease WITHOUT a valid firm is malformed
        wf = {}
        for label, firm in (("no_firm", None), ("firm_not_a_string", 5), ("firm_bad_form", "Bad Firm!")):
            body = lease_obj()
            if firm is not None:
                body["firm"] = firm
            lease[0] = json.dumps(body)
            pl.reset_lease_cache()
            s, b = await post("client_get_transactions", tx)
            wf[label] = {"status": s, "error": b.get("error")}
        out["lease_without_valid_firm"] = wf
        out["tool_calls_total"] = len(tool_calls)
        pl._state["server"].should_exit = True
        await pl.stop(task)

        # the Graph host pin, with httpx.Client stubbed: no socket is opened and no token is real
        built = []

        class _Resp:
            status_code = 200
            headers = {"content-type": "application/json"}
            content = b"{}"

            def json(self):
                return {"value": []}

        class _Client:
            def __init__(self, **kw):
                built.append(1)

            def __enter__(self):
                return self

            def __exit__(self, *e):
                return False

            def request(self, *a, **k):
                return _Resp()

        g.httpx.Client = _Client
        g.get_config = lambda: types.SimpleNamespace(MOCK_GRAPH=False)
        forged = ("https://evil.example/v1.0/me", "https://graph.microsoft.com.evil.example/v1.0/me", "https://graph.microsoft.com@evil.example/v1.0/me", "http://graph.microsoft.com/v1.0/me",
                  "https://graph.microsoft.com:8443/v1.0/me", "HTTPS://GRAPH.MICROSOFT.COM.EVIL.EXAMPLE/v1.0/me", "https://evil.example/graph.microsoft.com/v1.0/me")
        refused = 0
        for url in forged:
            try:
                g.call("stub-token", "GET", url)
            except g.GraphError:
                refused += 1
            except Exception:
                pass
        sent_to_forged = len(built)
        ok_calls = 0
        for path in ("/me", "https://graph.microsoft.com/v1.0/me/messages?$skip=10", "HTTPS://Graph.Microsoft.com/v1.0/me"):
            try:
                g.call("stub-token", "GET", path)
                ok_calls += 1
            except Exception:
                pass
        out["graph"] = {"forged_tried": len(forged), "forged_refused": refused, "clients_built_for_forged": sent_to_forged, "allowed_tried": 3, "allowed_reached_stub": len(built) - sent_to_forged, "allowed_answered": ok_calls}
        return out

    res = asyncio.run(main())
    res["audit_records"] = len(records)
    res["vm_hwm_mb"] = round(m.hwm_mb(), 1)
    m.emit(res)


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
    expect = json.load(open("/tmp/ap42_expect.json"))
    stage = "/tmp/ap42_stage_%d" % os.getpid()
    out = {"guard": m.CGROUP_GUARD_NAME, "scratch_removed": False}
    try:
        pid0, nr0 = read_pid()
        os.makedirs(stage, mode=0o700)
        shutil.copytree("/opt/opal-gateway/app", stage + "/app", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        shutil.copytree("/opt/opal-gateway/lib", stage + "/lib", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        got = {}
        for name, rel in CAND.items():
            shutil.copyfile("/tmp/ap42_cand_" + name, os.path.join(stage, rel))
            got[name] = hashlib.sha256(open(os.path.join(stage, rel), "rb").read()).hexdigest()
        out["candidate_bytes_equal_release"] = {n: got[n] == expect[n] for n in CAND}
        if not all(out["candidate_bytes_equal_release"].values()):
            out["stop"] = "candidate bytes differ from the release blobs"
            return out
        out["pct_before"] = m.host_pct()
        out["resolve"] = run_child("--resolve", stage)
        if out["resolve"].get("ref_resolved"):
            out["pins"] = run_child("--pins", stage)
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
    for n in ("ap42_pins.py", "ap38_measure.py", "ap38_guard.py"):
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/" + n, Body=io.open(os.path.join(here, n), "rb").read())
    gw = "C:/tmp/og-rel-batch10/infra/aws/ec2/opal-gateway/"
    for name, rel in CAND.items():
        s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + name, Body=io.open(gw + rel, "rb").read())
    s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + "expect.json", Body=json.dumps(expect).encode("utf-8"))
    pulls = ["aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (m.BUCKET, n, n) for n in ("ap42_pins.py", "ap38_measure.py", "ap38_guard.py")]
    pulls += ["aws s3 cp s3://%s/%s%s /tmp/ap42_cand_%s --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX, n, n) for n in CAND]
    pulls += ["aws s3 cp s3://%s/%sexpect.json /tmp/ap42_expect.json --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX)]
    cmd = "cd /opt/opal-gateway && rm -f /tmp/ap42_pins.py /tmp/ap38_measure.py /tmp/ap38_guard.py /tmp/ap42_cand_* /tmp/ap42_expect.json && %s && %s /tmp/ap42_pins.py --driver" % (" && ".join(pulls), m.PY)
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
    if "AP42_PINS_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("AP42_PINS_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    doc["captured_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1))
    os.chdir(root)


if __name__ == "__main__":
    if "--resolve" in sys.argv:
        child_resolve(sys.argv[sys.argv.index("--resolve") + 1])
    elif "--pins" in sys.argv:
        child_pins(sys.argv[sys.argv.index("--pins") + 1])
    elif "--driver" in sys.argv:
        print("AP42_PINS_JSON")
        try:
            print(json.dumps(driver(), separators=(",", ":"), default=str))
        except Exception:
            import traceback
            print(json.dumps({"fatal": traceback.format_exc()[-800:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1], sys.argv[2])
