#!/usr/bin/env python
"""OG-rl-17 Phase A step 3: the HOST MEASUREMENTS, every gateway-code run in a FRESH process under the cgroup HARD GUARD (ap38_guard.py --cgroup inside a transient systemd scope, MemoryMax=1400M,
oom_score_adj 1000, wall limit 120 s). READ-ONLY on AWS (the fences child reads the deployed catalog only); the running service is not touched; NOTHING arms the probe listener; NO SSM write.
The candidate is a SCRATCH copy of the service's own app/ and lib/ with the release's 13 app files and the contract laid over it (each overlay compared with the release blob); removed after.
  (a) THE GUARD. A burst of six concurrent tools.mcp.call_tool("whoami") against a scratch InflightGuard(2, 0.1) through a fake slow parent, as tests/test_og_mg3.py::test_ogmg3_call_tool_busy_envelope does:
      two run, four return the gateway_busy result.
  (b) THE FENCES. The deployed catalog: client_core.Ctx().firm_segments for the three served pairs (firm keys from client_core._names()["canonical"]): the segment COUNT of each.
  (c) THE CONTRACT. The deploy contract copy's sha256 equals the repo standards copy's, and capacity.target_memory_mib.
  python rl17_host.py <out.json> <expect.json>      -> RUNNER (repository root)
  python rl17_host.py --driver | --guard <stage> | --fences <stage> | --imports <stage>"""
from __future__ import annotations

import asyncio
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

S3_PREFIX = "ec2/opal-gateway/rl17_cand/"
TREE = "C:/tmp/og-rel-batch16/infra/aws/ec2/opal-gateway/"
OVERLAY = ["app/client_core.py", "app/client_adapter_bdcottonwood.py", "app/family_depth.py", "app/integrations/ycharts/integration.py", "app/integrations/opal_portal/integration.py", "app/harvest_typed.py",
           "app/integrations/portal_index/integration.py", "app/integrations/opal_discover/integration.py", "app/inflight_guard.py", "app/tools.py", "app/admin_gateway_breakdown.py", "app/news_typed.py",
           "app/admin_people_access.py", "deploy/NFRA_OPLGTW_CONTRACT.json"]


def child_guard(stage):
    os.environ.setdefault("MOCK_GRAPH", "1")
    m.load_env(stage)
    from mcp.server.fastmcp import FastMCP
    from mcp.types import CallToolResult

    from app import audit, data_entitlement, inflight_guard as ig, tools
    state = {"now": 0, "max": 0, "ran": 0}

    async def fake_call(self, name, arguments):
        state["now"] += 1
        state["max"] = max(state["max"], state["now"])
        try:
            await asyncio.sleep(0.4)
            state["ran"] += 1
            return {"ok": True}
        finally:
            state["now"] -= 1
    logged = []
    FastMCP.call_tool = fake_call
    audit.log_call = lambda *a, **k: logged.append((a, k))
    data_entitlement.tool_denial = lambda name, principal=None, *a, **k: None
    data_entitlement.remember_allowed = lambda name, principal=None: None
    data_entitlement.forget = lambda token: None
    g = ig.InflightGuard(2, 0.1)
    ig.guard = g

    async def burst(n):
        return await asyncio.gather(*[tools.mcp.call_tool("whoami", {}) for _ in range(n)], return_exceptions=True)
    res = asyncio.run(burst(6))
    ran = [r for r in res if isinstance(r, dict)]
    busy = [r for r in res if isinstance(r, CallToolResult)]
    raised = [r for r in res if isinstance(r, BaseException)]
    codes = {(r.structuredContent or {}).get("code") for r in busy}
    single = asyncio.run(burst(1))
    out = {"limit": 2, "ran": len(ran), "refused": len(busy), "raised": len(raised), "code": (sorted(codes)[0] if len(codes) == 1 else "mixed:%s" % sorted(map(str, codes))), "max_concurrent_bodies": state["max"],
           "busy_results_are_errors": all(r.isError is True for r in busy), "audit_rows_denied_gateway_busy": sum(1 for a, _ in logged if a[3:5] == ("denied", "gateway_busy")), "snapshot": g.snapshot(),
           "single_call_after_burst_runs": single == [{"ok": True}], "module_max_inflight": ig.MAX_INFLIGHT, "module_queue_wait_s": ig.QUEUE_WAIT_S, "vm_hwm_mb": round(m.hwm_mb(), 1)}
    m.emit(out)


def child_fences(stage):
    os.environ.setdefault("MOCK_GRAPH", "1")
    m.load_env(stage)
    from app import client_core as core
    k49, kct, kinf = core._names()["canonical"]
    ctx = core.Ctx()
    out = {"fences": {"orion": len(ctx.firm_segments("orion", kinf)), "eclipse": len(ctx.firm_segments("eclipse", kinf)), "commonwealth": len(ctx.firm_segments("commonwealth", kct))},
           "controls": {"orion_with_cottonwood_firm": len(ctx.firm_segments("orion", kct)), "eclipse_with_49financial": len(ctx.firm_segments("eclipse", k49)), "commonwealth_with_inflection": len(ctx.firm_segments("commonwealth", kinf))},
           "vm_hwm_mb": round(m.hwm_mb(), 1)}
    m.emit(out)


def child_imports(stage):
    """HOST-SHAPED IMPORT CHECK: every .py of the overlay imports in a fresh process from the candidate scratch tree (the service's own lib/ and .venv)."""
    import importlib
    os.environ.setdefault("MOCK_GRAPH", "1")
    m.load_env(stage)
    mods = [r[:-3].replace("/", ".") for r in OVERLAY if r.endswith(".py")]
    ok, bad = [], []
    for name in mods:
        try:
            importlib.import_module(name)
            ok.append(name)
        except BaseException as exc:  # noqa: BLE001
            bad.append([name, type(exc).__name__])
    from app import tools
    out = {"modules": len(mods), "imported": len(ok), "failed": bad, "registry_count_in_candidate": len(tools.mcp._tool_manager.list_tools()), "vm_hwm_mb": round(m.hwm_mb(), 1)}
    m.emit(out)


def run_child(args, wall=120):
    cmd = ["systemd-run", "--scope", "--quiet", "-p", "MemoryMax=1400M", "-p", "MemoryHigh=1100M", "-p", "MemorySwapMax=0", "--", m.PY, m.GUARD, "--cgroup", str(wall), os.path.abspath(__file__)] + args
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=wall + 60)
    lines = [ln for ln in p.stdout.splitlines() if ln.startswith("AP38_RESULT ")]
    res = json.loads(lines[-1].split(" ", 1)[1]) if lines else {"no_result": True, "stdout_tail": p.stdout[-300:], "stderr_tail": p.stderr[-500:]}
    res["exit_code"] = p.returncode
    return res


def read_pid():
    rc, out = m.sh("systemctl show opal-gateway -p MainPID -p NRestarts")
    kv = dict(ln.split("=", 1) for ln in out.splitlines() if "=" in ln)
    return kv.get("MainPID"), kv.get("NRestarts")


def driver():
    expect = json.load(open("/tmp/rl17_expect.json"))
    out = {"guard": m.CGROUP_GUARD_NAME, "scratch_removed": False}
    stage = "/tmp/rl17_stage_%d" % os.getpid()
    try:
        pid0, nr0 = read_pid()
        os.makedirs(stage, mode=0o700)
        shutil.copytree("/opt/opal-gateway/app", stage + "/app", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        shutil.copytree("/opt/opal-gateway/lib", stage + "/lib", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        os.makedirs(stage + "/deploy", exist_ok=True)
        for rel in OVERLAY:
            os.makedirs(os.path.dirname(os.path.join(stage, rel)), exist_ok=True)
            shutil.copyfile("/tmp/rl17_cand/" + rel.replace("/", "__"), os.path.join(stage, rel))
        shutil.copyfile("/tmp/rl17_deploy_to_ec2.sh", stage + "/deploy-to-ec2.sh")
        out["candidate_bytes_equal_release"] = all(hashlib.sha256(open(os.path.join(stage, rel), "rb").read()).hexdigest() == expect["sha256"][rel] for rel in OVERLAY)
        out["overlay_files"] = len(OVERLAY)
        out["marker_host"] = open("/opt/opal-gateway/.deployed_commit").read().strip()
        con = json.load(open(stage + "/deploy/NFRA_OPLGTW_CONTRACT.json"))
        out["contract"] = {"copies_equal": hashlib.sha256(open(stage + "/deploy/NFRA_OPLGTW_CONTRACT.json", "rb").read()).hexdigest() == expect["org_contract_sha256"],
                           "target_memory_mib": (con.get("capacity") or {}).get("target_memory_mib")}
        if not out["candidate_bytes_equal_release"]:
            out["stop"] = "candidate bytes differ from the release blobs"
            return out
        out["pct_before"] = m.host_pct()
        if out["pct_before"] >= m.STOP_PCT:
            out["stop"] = "host at or above %.0f percent used" % m.STOP_PCT
            return out
        out["guard_burst"] = run_child(["--guard", stage])
        out["pct_mid"] = m.host_pct()
        if out["pct_mid"] >= m.STOP_PCT:
            out["stop"] = "host at or above %.0f percent used before the fences child" % m.STOP_PCT
            return out
        out["fences"] = run_child(["--fences", stage])
        out["imports"] = run_child(["--imports", stage])
        out["pct_after"] = m.host_pct()
        pid1, nr1 = read_pid()
        out["service"] = {"pid_before": pid0, "pid_after": pid1, "pid_stable": pid0 == pid1, "nrestarts_before": nr0, "nrestarts_after": nr1}
    finally:
        shutil.rmtree(stage, ignore_errors=True)
        out["scratch_removed"] = not os.path.exists(stage)
    return out


def runner(outp, expect_path):
    import boto3
    here = os.path.dirname(os.path.abspath(__file__))
    s3 = boto3.client("s3")
    expect = json.load(io.open(expect_path, encoding="utf-8"))
    for n in ("rl17_host.py", "ap38_measure.py", "ap38_guard.py"):
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/" + n, Body=io.open(os.path.join(here, n), "rb").read())
    expect["sha256"] = {}
    for rel in OVERLAY:
        body = io.open(TREE + rel, "rb").read()
        expect["sha256"][rel] = hashlib.sha256(body).hexdigest()
        s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + rel.replace("/", "__"), Body=body)
    ds = io.open(TREE + "deploy-to-ec2.sh", "rb").read()
    s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + "deploy-to-ec2.sh", Body=ds)
    s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + "expect.json", Body=json.dumps(expect).encode("utf-8"))
    pulls = ["aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (m.BUCKET, n, n) for n in ("rl17_host.py", "ap38_measure.py", "ap38_guard.py")]
    pulls += ["mkdir -p /tmp/rl17_cand", "aws s3 cp s3://%s/%sexpect.json /tmp/rl17_expect.json --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX),
              "aws s3 cp s3://%s/%sdeploy-to-ec2.sh /tmp/rl17_deploy_to_ec2.sh --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX),
              ]
    pulls += ["aws s3 cp s3://%s/%s%s /tmp/rl17_cand/%s --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX, r.replace("/", "__"), r.replace("/", "__")) for r in OVERLAY]   # one GetObject each: the host role holds no s3:ListBucket here
    cmd = ("cd /opt/opal-gateway && rm -rf /tmp/rl17_host.py /tmp/ap38_measure.py /tmp/ap38_guard.py /tmp/rl17_cand /tmp/rl17_expect.json /tmp/rl17_deploy_to_ec2.sh && %s && %s /tmp/rl17_host.py --driver; rc=$?; rm -rf /tmp/rl17_cand /tmp/rl17_expect.json /tmp/rl17_deploy_to_ec2.sh; exit $rc"
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
    if "RL17_HOST_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-400:]))
    doc = json.loads(so.split("RL17_HOST_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    doc["captured_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1))


if __name__ == "__main__":
    if "--guard" in sys.argv:
        child_guard(sys.argv[sys.argv.index("--guard") + 1])
    elif "--imports" in sys.argv:
        child_imports(sys.argv[sys.argv.index("--imports") + 1])
    elif "--fences" in sys.argv:
        child_fences(sys.argv[sys.argv.index("--fences") + 1])
    elif "--driver" in sys.argv:
        print("RL17_HOST_JSON")
        try:
            print(json.dumps(driver(), separators=(",", ":"), default=str))
        except Exception:
            import traceback
            print(json.dumps({"fatal": traceback.format_exc()[-800:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1], sys.argv[2])
