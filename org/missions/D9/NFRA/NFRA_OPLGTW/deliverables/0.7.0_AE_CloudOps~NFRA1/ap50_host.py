#!/usr/bin/env python
"""OG-ap-50 Phase A step 3: the HOST MEASUREMENTS, every gateway-code run in a FRESH process under the cgroup HARD GUARD (ap38_guard.py --cgroup, inside a transient systemd scope with MemoryMax=1400M,
oom_score_adj 1000, wall limit 120 s). READ-ONLY on AWS (describes, gets and lists only: no S3 write, no SSM write); the running service is not touched; NOTHING arms the probe listener.
  (a) THE ROUTE LEG. LIVE ref's app.admin_api in ONE fresh process (route count), the CANDIDATE's in a SECOND (route count, then a TestClient (or an ASGI call when httpx is absent) on the real admin_app
      with app.family_depth.read replaced by a call-counting stub, the owner roster set to the owner address, app.owner_gate._alb_oidc_identity replaced by a fake): GET /gateway/families with no identity,
      with a verified non-owner, with the owner (an extra arm), GET /whoami with no identity, GET /gateway/no-such-route; whether the stub ran on a refusal.
  (b) THE HOST READ. ONE fresh process from the candidate scratch tree calls the REAL app.family_depth.read() once (100 s wall guard) as the gateway instance role (sts get-caller-identity shows the
      instance's role; the account number is never printed) and records counts only: families, denominator, values_total, measured / inferred / absent, claim-less, absent-with-reason, wall_s, peak_rss_mb.
  python ap50_host.py <out.json> <expect.json>      -> RUNNER (repository root)
  python ap50_host.py --driver | --route <stage> <which> | --hostread <stage>"""
from __future__ import annotations

import asyncio
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

S3_PREFIX = "ec2/opal-gateway/ap50_cand/"
GROUP = "/gateway/families"
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


# ----------------------------------------------------------------------------------------------------- children
def child_route(stage, which):
    os.environ.setdefault("MOCK_GRAPH", "1")
    m.load_env(stage)
    from app import admin_api
    out = {"which": which, "routes": len(admin_api.routes), "families_route_present": any(getattr(r, "path", None) == GROUP for r in admin_api.routes),
           "route_paths_count": len({getattr(r, "path", None) for r in admin_api.routes})}
    if which == "candidate":
        from app import config as app_config, family_depth, owner_gate
        from app.identity import IdentityError
        owner = owner_gate._DASHBOARD_OWNER
        other = "someone.else@opalinvest.com"
        cfg = app_config.get_config()
        cfg.DASHBOARD_OWNER_EMAILS = (owner,)
        owner_gate._cfg = cfg
        state = {"id": None}

        def fake(request):
            if state["id"] is None:
                raise IdentityError("no identity")
            return state["id"]
        owner_gate._alb_oidc_identity = fake
        calls = []

        def stub_read():
            calls.append(1)
            return {"denominator": 1, "families": []}
        family_depth.read = stub_read
        try:
            from starlette.testclient import TestClient
            client = TestClient(admin_api.admin_app, base_url="http://localhost", raise_server_exceptions=False)
            out["method"] = "starlette TestClient on the real admin_app"

            def get(path):
                return client.get(path).status_code
        except Exception as exc:  # noqa: BLE001 -- httpx absent on the host: drive the ASGI app directly
            out["method"] = "direct ASGI call on the real admin_app (TestClient unavailable: %s)" % type(exc).__name__

            async def _call(path):
                sent = []
                scope = {"type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1", "method": "GET", "path": path, "raw_path": path.encode(), "query_string": b"",
                         "root_path": "", "scheme": "http", "headers": [(b"host", b"localhost")], "client": ("127.0.0.1", 50000), "server": ("localhost", 80)}

                async def receive():
                    return {"type": "http.request", "body": b"", "more_body": False}

                async def send(msg):
                    sent.append(msg)
                await admin_api.admin_app(scope, receive, send)
                return next(x["status"] for x in sent if x["type"] == "http.response.start")

            def get(path):
                return asyncio.run(_call(path))
        state["id"] = None
        out["unauth_status"] = get(GROUP)
        state["id"] = other
        out["nonowner_status"] = get(GROUP)
        out["read_calls_after_refusals"] = len(calls)
        state["id"] = None
        out["whoami_control_unauth_status"] = get("/whoami")
        out["missing_route_control_status"] = get("/gateway/no-such-route")
        out["read_called_on_refusal"] = len(calls) > 0
        state["id"] = owner
        out["owner_status"] = get(GROUP)
        out["read_calls_after_owner"] = len(calls)
    out["vm_hwm_mb"] = round(m.hwm_mb(), 1)
    m.emit(out)


def child_hostread(stage):
    m.load_env(stage)
    import boto3
    ident = boto3.client("sts", region_name="us-east-1").get_caller_identity()["Arn"]
    role = ident.split(":", 5)[-1]                                         # assumed-role/<role>/<instance>: the account number is not part of it
    from app import family_depth
    res = {}

    def go():
        t0 = time.monotonic()
        try:
            res["doc"] = family_depth.read()
        except BaseException as exc:  # noqa: BLE001
            res["error"] = type(exc).__name__ + ": " + str(exc)[:160]
        res["wall"] = time.monotonic() - t0
    th = threading.Thread(target=go, daemon=True)
    t0 = time.monotonic()
    th.start()
    th.join(READ_WALL_S)
    finished = not th.is_alive()
    out = {"finished_within_wall_guard": finished, "wall_s": round(res.get("wall", time.monotonic() - t0), 2), "peak_rss_mb": round(m.hwm_mb(), 1),
           "identity_role_path": role.rsplit("/", 1)[0] if role.startswith("assumed-role/") else role, "identity_is_assumed_role": role.startswith("assumed-role/")}
    if "error" in res:
        out["error"] = res["error"]
    doc = res.get("doc")
    if doc:
        leaves = []
        _leaves(doc, leaves)
        claims = {"measured": 0, "inferred": 0, "absent": 0}
        claimless = absent_reason = 0
        for lf in leaves:
            c = lf.get("claim")
            if c in claims:
                claims[c] += 1
            else:
                claimless += 1
            if c == "absent" and isinstance(lf.get("source"), str) and lf["source"].strip():
                absent_reason += 1
        rows = doc.get("families", [])
        blob = json.dumps(doc)
        keys_total = sum(len(((r.get("depth") or {}).get("backfill_status_keys")) or []) for r in rows)
        err_sourced = sum(1 for lf in leaves if lf.get("claim") == "absent" and re.search(r"\w+(?:Error|Exception): ", str(lf.get("source", ""))))
        out["response_scan"] = {"response_bytes": len(blob), "twelve_digit_runs": len(re.findall(r"(?<!\d)\d{12}(?!\d)", blob)), "nine_plus_digit_runs": len(re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", blob)),
                                "arn_strings": blob.count("arn:aws"), "email_shaped_strings": len(re.findall(r"[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Za-z]+", blob)), "s3_uri_strings": blob.count("s3://"),
                                "backfill_status_keys_listed": keys_total, "absent_values_sourced_from_an_exception": err_sourced,
                                "rows_with_a_channel": sum(1 for r in rows if r.get("channel")), "rows_with_a_family": sum(1 for r in rows if r.get("family"))}
        def shape(lf):
            t = re.sub(r"arn:aws:[^\s,;)\"']+", "arn:aws:<masked>", str(lf.get("source", "")))
            t = re.sub(r"\d{6,}", "#", t)
            t = re.sub(r"s3://[^\s,;)]+", "s3://<masked>", t)
            return t[:120]
        from collections import Counter
        shapes = Counter((lf.get("claim"), shape(lf)) for lf in leaves if ("arn:aws" in str(lf.get("source", "")) or lf.get("claim") == "absent"))
        out["leaf_shapes_masked"] = [[c, sh, n] for (c, sh), n in shapes.most_common(14)]
        denied = []
        for lf in leaves:
            src = str(lf.get("source", ""))
            for mt in re.finditer(r"s3://[^/\s]+/([^/\s]+)/[^\s]*?meta/backfill-status\.json[ :]+AccessDenied:([^;]{0,260})", src):
                tail = mt.group(2)
                clause = ("explicit deny" if "explicit deny" in tail else "because no identity-based policy allows" if "no identity-based policy" in tail else "because " + re.sub(r"arn:aws:[^\s,;)\"']+", "arn:aws:<masked>", tail.split("because", 1)[1][:70]) if "because" in tail else "(message truncated before any cause)")
                denied.append([mt.group(1), re.sub(r"\d{6,}", "#", clause)])
        out["denied_status_keys_by_root"] = Counter(d[0] for d in denied).most_common()
        out["denied_clauses_masked"] = Counter(d[1] for d in denied).most_common(4)
        arn_in = Counter(lf.get("claim") for lf in leaves if "arn:aws" in str(lf.get("source", "")))
        out["arn_in_source_by_claim"] = dict(arn_in)
        out["arn_outside_source_field"] = blob.count("arn:aws") - sum(str(lf.get("source", "")).count("arn:aws") for lf in leaves)
        out.update({"families": len(rows), "denominator": doc.get("denominator"), "distinct_families": len({r.get("family") for r in rows if r.get("family")}),
                    "values_total": len(leaves), "measured_values": claims["measured"], "inferred_values": claims["inferred"], "absent_values": claims["absent"],
                    "claim_less_values": claimless, "absent_with_reason": absent_reason, "claims_sum_equals_total": sum(claims.values()) + claimless == len(leaves)})
    m.emit(out)
    sys.stdout.flush()
    os._exit(0)


# ----------------------------------------------------------------------------------------------------- host driver
def run_child(args, stage_wall=120):
    cmd = ["systemd-run", "--scope", "--quiet", "-p", "MemoryMax=1400M", "-p", "MemoryHigh=1100M", "-p", "MemorySwapMax=0", "--", m.PY, m.GUARD, "--cgroup", str(stage_wall),
           os.path.abspath(__file__)] + args
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=stage_wall + 60)
    lines = [ln for ln in p.stdout.splitlines() if ln.startswith("AP38_RESULT ")]
    res = json.loads(lines[-1].split(" ", 1)[1]) if lines else {"no_result": True, "stdout_tail": p.stdout[-300:], "stderr_tail": p.stderr[-500:]}
    res["exit_code"] = p.returncode
    return res


def read_pid():
    rc, out = m.sh("systemctl show opal-gateway -p MainPID -p NRestarts")
    kv = dict(ln.split("=", 1) for ln in out.splitlines() if "=" in ln)
    return kv.get("MainPID"), kv.get("NRestarts")


def driver():
    expect = json.load(open("/tmp/ap50_expect.json"))
    out = {"guard": m.CGROUP_GUARD_NAME, "scratch_removed": False}
    stages = ["/tmp/ap50_stage_c_%d" % os.getpid(), "/tmp/ap50_stage_l_%d" % os.getpid()]
    try:
        pid0, nr0 = read_pid()
        for st in stages:
            os.makedirs(st, mode=0o700)
            shutil.copytree("/opt/opal-gateway/app", st + "/app", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            shutil.copytree("/opt/opal-gateway/lib", st + "/lib", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            shutil.copyfile("/tmp/ap50_deploy_to_ec2.sh", st + "/deploy-to-ec2.sh")      # family_depth.DEPLOY_SCRIPT reads it (the tree root's sibling of app/); NOT on the host at /opt/opal-gateway
        shutil.copyfile("/tmp/ap50_cand_admin_api.py", stages[0] + "/app/admin_api.py")
        got = hashlib.sha256(open(stages[0] + "/app/admin_api.py", "rb").read()).hexdigest()
        out["candidate_bytes_equal_release"] = {"admin_api.py": got == expect["admin_api.py"]}
        out["live_stage_admin_api_equals_host"] = hashlib.sha256(open(stages[1] + "/app/admin_api.py", "rb").read()).hexdigest() == hashlib.sha256(open("/opt/opal-gateway/app/admin_api.py", "rb").read()).hexdigest()
        out["live_stage_family_depth_equals_host"] = hashlib.sha256(open(stages[1] + "/app/family_depth.py", "rb").read()).hexdigest() == hashlib.sha256(open("/opt/opal-gateway/app/family_depth.py", "rb").read()).hexdigest()
        if not out["candidate_bytes_equal_release"]["admin_api.py"]:
            out["stop"] = "candidate bytes differ from the release blob"
            return out
        out["deploy_script_on_host_opt"] = os.path.exists("/opt/opal-gateway/deploy-to-ec2.sh")
        out["staged_deploy_script_equals_release_blob"] = hashlib.sha256(open(stages[0] + "/deploy-to-ec2.sh", "rb").read()).hexdigest() == expect["deploy-to-ec2.sh"]
        out["pct_before"] = m.host_pct()
        if out["pct_before"] >= m.STOP_PCT:
            out["stop"] = "host at or above %.0f percent used" % m.STOP_PCT
            return out
        out["route_live"] = run_child(["--route", stages[1], "live"])
        out["pct_mid1"] = m.host_pct()
        out["route_candidate"] = run_child(["--route", stages[0], "candidate"])
        out["pct_mid2"] = m.host_pct()
        if out["pct_mid2"] >= m.STOP_PCT:
            out["stop"] = "host at or above %.0f percent used before the host read" % m.STOP_PCT
            return out
        out["host_read"] = run_child(["--hostread", stages[0]], stage_wall=120)
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
    for n in ("ap50_host.py", "ap38_measure.py", "ap38_guard.py"):
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/" + n, Body=io.open(os.path.join(here, n), "rb").read())
    gw = "C:/tmp/og-rel-batch14/infra/aws/ec2/opal-gateway/"
    s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + "admin_api.py", Body=io.open(gw + "app/admin_api.py", "rb").read())
    ds = io.open(gw + "deploy-to-ec2.sh", "rb").read()
    s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + "deploy-to-ec2.sh", Body=ds)
    expect["deploy-to-ec2.sh"] = hashlib.sha256(ds).hexdigest()
    s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + "expect.json", Body=json.dumps(expect).encode("utf-8"))
    pulls = ["aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (m.BUCKET, n, n) for n in ("ap50_host.py", "ap38_measure.py", "ap38_guard.py")]
    pulls += ["aws s3 cp s3://%s/%sadmin_api.py /tmp/ap50_cand_admin_api.py --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX),
              "aws s3 cp s3://%s/%sexpect.json /tmp/ap50_expect.json --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX),
              "aws s3 cp s3://%s/%sdeploy-to-ec2.sh /tmp/ap50_deploy_to_ec2.sh --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX)]
    cmd = "cd /opt/opal-gateway && rm -f /tmp/ap50_host.py /tmp/ap38_measure.py /tmp/ap38_guard.py /tmp/ap50_cand_admin_api.py /tmp/ap50_expect.json /tmp/ap50_deploy_to_ec2.sh && %s && %s /tmp/ap50_host.py --driver" % (" && ".join(pulls), m.PY)
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
    if "AP50_HOST_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("AP50_HOST_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    doc["captured_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1))


if __name__ == "__main__":
    if "--route" in sys.argv:
        i = sys.argv.index("--route")
        child_route(sys.argv[i + 1], sys.argv[i + 2])
    elif "--hostread" in sys.argv:
        child_hostread(sys.argv[sys.argv.index("--hostread") + 1])
    elif "--driver" in sys.argv:
        print("AP50_HOST_JSON")
        try:
            print(json.dumps(driver(), separators=(",", ":"), default=str))
        except Exception:
            import traceback
            print(json.dumps({"fatal": traceback.format_exc()[-800:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1], sys.argv[2])
