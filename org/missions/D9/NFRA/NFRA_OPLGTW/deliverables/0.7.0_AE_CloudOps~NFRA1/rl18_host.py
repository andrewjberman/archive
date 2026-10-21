#!/usr/bin/env python
"""OG-rl-18 Phase A step 3: the HOST MEASUREMENTS (a) and (b), every gateway-code run in a FRESH process under the cgroup HARD GUARD (ap38_guard.py --cgroup inside a transient systemd scope, MemoryMax=1400M, oom_score_adj 1000,
wall limit 120 s). READ-ONLY: no AWS call is made by any child (the probes use fakes); the running service is not touched; NOTHING arms the probe listener; NO SSM write. The candidate is a SCRATCH copy of the service's own
app/, lib/ and deploy/ with the release's app files laid over it (each compared with the release blob) and the probe fixtures (ops/schwab_entitlement_admin.py, tests/test_email_deny.py) from the release tree; a LIVE copy (the service's
tree as it is) is the second stage for (b). Both are removed after.
  (a) THE PROBES: the python of rt1.AC1, rt1.AC2, ed1.AC1 and mp1.AC1 (W/rl18_probe_*.py, verbatim) each in ONE fresh process on the candidate stage: the labelled lines that read ok.
  (b) EXPLICIT SCOPES UNCHANGED: in ONE fresh process per stage, the SAME explicit-list scope (two masters, eight-digit fixture ids built at run time) is parsed and check_scope is asked an in-list id, an out-of-list id and an empty
      list; the account list the resolver builds and the Schwab account filter are built; the answers are compared between the live ref's code and the candidate's.
  python rl18_host.py <out.json> <expect.json>    -> RUNNER (repository root)
  python rl18_host.py --driver | --probe <stage> <label> | --explicit <stage>"""
from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import time
import types

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ap38_measure as m  # noqa: E402

S3_PREFIX = "ec2/opal-gateway/rl18_cand/"
TREE = "C:/tmp/og-rel-batch17/infra/aws/ec2/opal-gateway/"
OVERLAY = ["app/data_entitlement.py", "app/account_ref.py", "app/integrations/schwab/integration.py", "app/server.py", "app/token_broker.py", "app/admin_api.py"]
FIXTURES = ["ops/schwab_entitlement_admin.py", "tests/test_email_deny.py"]
PROBES = ["rt1ac1", "rt1ac2", "ed1ac1", "mp1ac1"]
HERE_FILES = ["rl18_host.py", "ap38_measure.py", "ap38_guard.py"] + ["rl18_probe_%s.py" % p for p in PROBES]
FLAT = lambda rel: rel.replace("/", "__")  # noqa: E731


def child_probe(stage, label):
    os.environ["MOCK_GRAPH"] = "1"
    os.chdir(stage)
    sys.path.insert(0, stage)
    try:
        import pytest  # noqa: F401
    except ImportError:                      # the host venv carries no pytest: the fixture test_email_deny.py imports it at module level only for its own tests
        stub = types.ModuleType("pytest")
        stub.fixture = lambda *a, **k: (lambda f: f) if not (a and callable(a[0])) else a[0]
        stub.mark = types.SimpleNamespace(parametrize=lambda *a, **k: (lambda f: f))
        stub.raises = lambda *a, **k: None
        sys.modules["pytest"] = stub
    src = open("/tmp/rl18_probe_%s.py" % label, encoding="utf-8").read()
    buf, real = io.StringIO(), sys.stdout
    sys.stdout = buf
    sys.argv = ["probe_%s.py" % label, stage]
    err = None
    try:
        exec(compile(src, "probe_%s.py" % label, "exec"), {"__name__": "__probe__"})
    except SystemExit:
        pass
    except Exception as exc:  # noqa: BLE001
        import traceback
        err = "%s %s | %s" % (type(exc).__name__, str(exc)[:120], " / ".join(ln.strip() for ln in traceback.format_exc().splitlines()[-4:])[:300])
    finally:
        sys.stdout = real
    lines = [ln for ln in buf.getvalue().splitlines() if ln.strip()]
    labelled = [ln for ln in lines if ": ok" in ln or ": NOT OK" in ln or ": NO" in ln]
    ok = [ln for ln in labelled if ": ok" in ln and ": NOT OK" not in ln and not ln.rstrip().endswith(": NO")]
    m.emit({"label": label, "lines": len(labelled), "ok": len(ok), "not_ok": [ln[:90] for ln in labelled if ln not in ok], "final": lines[-1] if lines else None, "head": [ln[:160] for ln in lines[:3]], "error": err, "vm_hwm_mb": round(m.hwm_mb(), 1)})


def child_explicit(stage):
    os.environ["MOCK_GRAPH"] = "1"
    os.chdir(stage)
    sys.path.insert(0, stage)
    from app import account_ref as ar
    from app import data_entitlement as de
    from app.integrations.schwab import integration as si
    m1, m2 = "08242234", "08335338"
    ids1 = ["7%07d" % i for i in range(1, 4)]          # built at run time: eight-digit fixture ids
    ids2 = ["8%07d" % i for i in range(1, 3)]
    raw = {"masters": [m1, m2], "datasets": ["dim_position"], "accounts": {m1: ids1, m2: ids2}, "dates": {"mode": "rolling_complete_window"},
           "columns": {"dim_position": ["symbol"]}, "operations": ["list", "describe", "query"]}
    scope = de.parse_scope(raw)
    out = {"parsed": {k: sorted(v) for k, v in scope.accounts.items()}, "masters": sorted(scope.masters)}
    checks = {}
    for label, master, ids in (("in_list", m1, ids1[:2]), ("out_of_list", m1, ["99999999"]), ("empty_list", m1, []), ("in_list_m2", m2, ids2[:1]), ("mixed", m2, [ids2[0], "99999999"])):
        req = {"operation": "query", "master": master, "dataset": "dim_position", "account_ids": ids}
        try:
            checks[label] = [list(map(str, f)) for f in de.check_scope(scope, req)]
        except Exception as exc:  # noqa: BLE001
            checks[label] = "raised %s" % type(exc).__name__
    out["check_scope"] = checks
    resolver, filt = {}, {}
    for master in (m1, m2):
        if hasattr(ar, "candidate_accounts"):
            resolver[master] = ar.candidate_accounts(scope, master, None)
        else:
            resolver[master] = sorted(scope.accounts.get(master, frozenset()))     # the live ref's _resolve builds exactly this (account_ref.py line 248)
        if hasattr(si, "account_filter_for"):
            f = si.account_filter_for(scope, master)
        else:
            f = tuple(scope.accounts.get(master, ()))                              # the live ref's inline filter
        filt[master] = sorted(f) if f is not None else None
    out["resolver_candidate_list"], out["schwab_account_filter"] = resolver, filt
    out["scope_summary_account_count"] = si.scope_summary(scope).get("account_count")
    out["vm_hwm_mb"] = round(m.hwm_mb(), 1)
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
    expect = json.load(open("/tmp/rl18_expect.json"))
    out = {"guard": m.CGROUP_GUARD_NAME, "scratch_removed": False}
    cand_root, live_root = "/tmp/rl18_stage_c_%d" % os.getpid(), "/tmp/rl18_stage_l_%d" % os.getpid()
    gw = "/infra/aws/ec2/opal-gateway"          # the fixtures resolve a repo root with parents[5], so the stage sits at the repo-relative depth
    cand, live = cand_root + gw, live_root + gw
    try:
        pid0, nr0 = read_pid()
        for st in (cand, live):
            os.makedirs(st, mode=0o700, exist_ok=True)
            for d in ("app", "lib", "deploy"):
                shutil.copytree("/opt/opal-gateway/" + d, st + "/" + d, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for rel in OVERLAY:
            shutil.copyfile("/tmp/rl18_cand/" + FLAT(rel), os.path.join(cand, rel))
        for rel in FIXTURES:
            os.makedirs(os.path.dirname(os.path.join(cand, rel)), exist_ok=True)
            shutil.copyfile("/tmp/rl18_cand/" + FLAT(rel), os.path.join(cand, rel))
        out["candidate_bytes_equal_release"] = all(hashlib.sha256(open(os.path.join(cand, rel), "rb").read()).hexdigest() == expect["sha256"][rel] for rel in OVERLAY + FIXTURES)
        out["live_stage_equals_host"] = all(hashlib.sha256(open(live + "/" + rel, "rb").read()).hexdigest() == hashlib.sha256(open("/opt/opal-gateway/" + rel, "rb").read()).hexdigest() for rel in OVERLAY)
        out["marker_host"] = open("/opt/opal-gateway/.deployed_commit").read().strip()
        if not out["candidate_bytes_equal_release"]:
            out["stop"] = "candidate bytes differ from the release blobs"
            return out
        out["pct_before"] = m.host_pct()
        if out["pct_before"] >= m.STOP_PCT:
            out["stop"] = "host at or above %.0f percent used" % m.STOP_PCT
            return out
        out["probes"] = {}
        for lab in PROBES:
            out["probes"][lab] = run_child(["--probe", cand, lab])
            out["pct_after_" + lab] = m.host_pct()
            if out["pct_after_" + lab] >= m.STOP_PCT:
                out["stop"] = "host at or above %.0f percent used after probe %s" % (m.STOP_PCT, lab)
                return out
        out["explicit_live"] = run_child(["--explicit", live])
        out["explicit_candidate"] = run_child(["--explicit", cand])
        keys = ("parsed", "masters", "check_scope", "resolver_candidate_list", "schwab_account_filter", "scope_summary_account_count")
        out["explicit_equal"] = all(out["explicit_live"].get(k) is not None and out["explicit_live"].get(k) == out["explicit_candidate"].get(k) for k in keys)
        out["pct_after"] = m.host_pct()
        pid1, nr1 = read_pid()
        out["service"] = {"pid_before": pid0, "pid_after": pid1, "pid_stable": pid0 == pid1, "nrestarts_before": nr0, "nrestarts_after": nr1}
    finally:
        for st in (cand_root, live_root):
            shutil.rmtree(st, ignore_errors=True)
        out["scratch_removed"] = not (os.path.exists(cand_root) or os.path.exists(live_root))
    return out


def runner(outp, expect_path):
    import boto3
    here = os.path.dirname(os.path.abspath(__file__))
    s3 = boto3.client("s3")
    expect = json.load(io.open(expect_path, encoding="utf-8"))
    for n in HERE_FILES:
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/" + n, Body=io.open(os.path.join(here, n), "rb").read())
    expect["sha256"] = {}
    for rel in OVERLAY + FIXTURES:
        body = io.open(TREE + rel, "rb").read()
        expect["sha256"][rel] = hashlib.sha256(body).hexdigest()
        s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + FLAT(rel), Body=body)
    s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + "expect.json", Body=json.dumps(expect).encode("utf-8"))
    pulls = ["aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (m.BUCKET, n, n) for n in HERE_FILES]
    pulls += ["mkdir -p /tmp/rl18_cand", "aws s3 cp s3://%s/%sexpect.json /tmp/rl18_expect.json --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX)]
    pulls += ["aws s3 cp s3://%s/%s%s /tmp/rl18_cand/%s --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX, FLAT(r), FLAT(r)) for r in OVERLAY + FIXTURES]
    cmd = ("cd /opt/opal-gateway && rm -rf %s /tmp/rl18_cand /tmp/rl18_expect.json && %s && %s /tmp/rl18_host.py --driver; rc=$?; rm -rf %s /tmp/rl18_cand /tmp/rl18_expect.json; exit $rc"
           % (" ".join("/tmp/" + n for n in HERE_FILES), " && ".join(pulls), m.PY, " ".join("/tmp/" + n for n in HERE_FILES)))
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
    if "RL18_HOST_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-400:]))
    doc = json.loads(so.split("RL18_HOST_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    doc["captured_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1)[:3500])


if __name__ == "__main__":
    if "--probe" in sys.argv:
        i = sys.argv.index("--probe")
        child_probe(sys.argv[i + 1], sys.argv[i + 2])
    elif "--explicit" in sys.argv:
        child_explicit(sys.argv[sys.argv.index("--explicit") + 1])
    elif "--driver" in sys.argv:
        print("RL18_HOST_JSON")
        try:
            print(json.dumps(driver(), separators=(",", ":"), default=str))
        except Exception:
            import traceback
            print(json.dumps({"fatal": traceback.format_exc()[-800:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1], sys.argv[2])
