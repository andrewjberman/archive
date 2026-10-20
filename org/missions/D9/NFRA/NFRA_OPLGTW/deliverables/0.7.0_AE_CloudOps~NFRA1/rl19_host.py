#!/usr/bin/env python
"""OG-rl-19 Phase A step 3: the HOST MEASUREMENTS (a) and (b), every gateway-code run in a FRESH process under the cgroup HARD GUARD (ap38_guard.py --cgroup inside a transient systemd scope, MemoryMax=1400M, oom_score_adj 1000, wall limit 120 s).
READ-ONLY: no AWS call is made by any child (the probes use fake S3 clients behind fake role objects); the running service is not touched; NOTHING arms the probe listener; NO SSM write. The candidate is a SCRATCH copy of the service's own app/, lib/ and
deploy/ with the release's four files laid over it (each compared with the release blob); a LIVE copy (the service's tree as it is) is the second stage. Both are removed after.
  (a) THE PROBES: the python of sk2.AC1 (W/rl19_sk2_probe.py, verbatim but for one file read) in ONE fresh process on the candidate stage: the labelled lines that read ok.
  (b) OLD-FORM READS UNCHANGED: in ONE fresh process per stage, with a fake S3 client, Catalog.read_marker and Catalog.list_dates for 08242234 and 08335338 (and catalog.marker_locations where the tree has it): the answers and the calls made, compared across the two stages.
  python rl19_host.py <out.json> <expect.json>    -> RUNNER (repository root)
  python rl19_host.py --driver | --probe <stage> | --oldform <stage>"""
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

S3_PREFIX = "ec2/opal-gateway/rl19_cand/"
TREE = "C:/tmp/og-rel-r3c/infra/aws/ec2/opal-gateway/"
G = "infra/aws/ec2/opal-gateway/"
OVERLAY = ["app/integrations/schwab/catalog.py", "app/integrations/schwab/integration.py", "deploy/NFRA_OPLGTW_CONTRACT.json"]
OLD_MASTERS = ("08242234", "08335338")


def child_probe(stage):
    os.environ.setdefault("MOCK_GRAPH", "1")
    os.environ["SK2_BASE_CONTRACT"] = "/tmp/rl19_base_contract.json"
    os.chdir(stage)
    sys.path.insert(0, stage)
    src = open("/tmp/rl19_sk2_probe.py", encoding="utf-8").read()
    buf, real = io.StringIO(), sys.stdout
    sys.stdout = buf
    sys.argv = ["rl19_sk2_probe.py", stage]
    try:
        exec(compile(src, "rl19_sk2_probe.py", "exec"), {"__name__": "__probe__"})
    except SystemExit:
        pass
    finally:
        sys.stdout = real
    lines = [ln for ln in buf.getvalue().splitlines() if ln.strip()]
    labelled = [ln for ln in lines if ln.endswith(": ok") or ": ok (" in ln or ": NOT OK" in ln]
    m.emit({"lines": len(labelled), "ok": sum(1 for ln in labelled if ": NOT OK" not in ln), "not_ok": [ln[:80] for ln in labelled if ": NOT OK" in ln], "final": lines[-1] if lines else None, "vm_hwm_mb": round(m.hwm_mb(), 1)})


def child_oldform(stage):
    os.environ.setdefault("MOCK_GRAPH", "1")
    m.load_env(stage)
    from botocore.exceptions import ClientError
    from app.integrations.schwab import aws_roles
    from app.integrations.schwab import catalog as C
    raw = json.load(open(os.path.join(stage, "deploy", "NFRA_OPLGTW_CONTRACT.json"), encoding="utf-8"))
    cont = C.parse_contract(raw, "stage")

    class FakeS3:
        def __init__(self, objs):
            self.objs, self.calls = objs, []

        def get_object(self, Bucket, Key, **kw):
            self.calls.append(("get", Bucket, Key))
            if (Bucket, Key) not in self.objs:
                raise ClientError({"Error": {"Code": "NoSuchKey", "Message": "x"}}, "GetObject")
            body = self.objs[(Bucket, Key)]
            return {"Body": types.SimpleNamespace(read=lambda n=None, b=body: b), "VersionId": "v1"}

        def list_objects_v2(self, Bucket, Prefix, MaxKeys=1000, ContinuationToken=None, **kw):
            self.calls.append(("list", Bucket, Prefix))
            return {"Contents": [{"Key": k} for (b, k) in sorted(self.objs) if b == Bucket and k.startswith(Prefix)], "IsTruncated": False}

    def role(kind, fake):
        return types.SimpleNamespace(config=types.SimpleNamespace(kind=kind), session=lambda pc: types.SimpleNamespace(client=lambda n: fake))

    out = {"has_marker_locations": hasattr(C, "marker_locations"), "has_firm_form_masters": hasattr(C, "firm_form_masters"), "masters": {}}
    for master in OLD_MASTERS:
        objs = {}
        for d in ("2026-10-19", "2026-10-20"):
            objs[("opal-data-assets", "schwab/%s/meta/complete/date=%s.json" % (master, d))] = json.dumps({"master": master, "date": d, "closure": {"x": 1}}).encode()
        fake = FakeS3(objs)
        cat = C.Catalog(contract=cont, catalog_role=role(aws_roles.CATALOG, fake), data_role=role(aws_roles.READER, fake), store=object())
        key = "schwab/%s/meta/complete/date=2026-10-20.json" % master
        legacy = new_api = None
        calls_legacy, calls_new = [], []
        if hasattr(cat, "_read_marker"):                 # the live ref's read path (private); the candidate keeps it too if it still exists
            fake.calls.clear()
            try:
                rm = cat._read_marker(key, lambda *a, **k: None)
                legacy = [rm[0], rm[1]]
            except Exception as exc:  # noqa: BLE001
                legacy = "raised %s" % type(exc).__name__
            calls_legacy = list(fake.calls)
        if hasattr(cat, "read_marker"):                  # the OG-sk-2 public read (candidate only)
            fake.calls.clear()
            try:
                rm = cat.read_marker(master, "2026-10-20", lambda *a, **k: None)
                new_api = [rm[0], rm[1]]
            except Exception as exc:  # noqa: BLE001
                new_api = "raised %s" % type(exc).__name__
            calls_new = list(fake.calls)
        calls_rm = calls_legacy + calls_new
        try:
            ld = cat.list_dates(master, lambda *a, **k: None)
        except Exception as exc:  # noqa: BLE001
            ld = "raised %s" % type(exc).__name__
        calls_ld = list(fake.calls)
        locs = [list(t) for t in C.marker_locations(cont, master, "2026-10-20")] if out["has_marker_locations"] else None
        out["masters"][master] = {"legacy_read_marker": legacy, "legacy_read_marker_calls": calls_legacy, "read_marker": new_api, "read_marker_calls": calls_new, "list_dates": ld, "list_dates_calls": calls_ld, "marker_locations": locs,
                                  "state_bucket_called": any(c[1] == "opal-data-49financial" for c in calls_rm + calls_ld)}
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
    expect = json.load(open("/tmp/rl19_expect.json"))
    out = {"guard": m.CGROUP_GUARD_NAME, "scratch_removed": False}
    cand, live = "/tmp/rl19_stage_c_%d" % os.getpid(), "/tmp/rl19_stage_l_%d" % os.getpid()
    try:
        pid0, nr0 = read_pid()
        for st in (cand, live):
            os.makedirs(st, mode=0o700)
            for d in ("app", "lib", "deploy"):
                shutil.copytree("/opt/opal-gateway/" + d, st + "/" + d, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for rel in OVERLAY:
            shutil.copyfile("/tmp/rl19_cand/" + rel.replace("/", "__"), os.path.join(cand, rel))
        os.makedirs(cand + "/org/standards", exist_ok=True)
        shutil.copyfile("/tmp/rl19_cand/org_standards_contract.json", cand + "/org/standards/NFRA_OPLGTW_CONTRACT.json")
        out["candidate_bytes_equal_release"] = all(hashlib.sha256(open(os.path.join(cand, rel), "rb").read()).hexdigest() == expect["sha256"][rel] for rel in OVERLAY)
        out["standards_copy_equals_deploy_copy"] = open(cand + "/org/standards/NFRA_OPLGTW_CONTRACT.json", "rb").read() == open(cand + "/deploy/NFRA_OPLGTW_CONTRACT.json", "rb").read()
        out["live_stage_equals_host"] = all(hashlib.sha256(open(live + "/app/integrations/schwab/catalog.py", "rb").read()).hexdigest() == hashlib.sha256(open("/opt/opal-gateway/app/integrations/schwab/catalog.py", "rb").read()).hexdigest() for _ in (0,))
        out["marker_host"] = open("/opt/opal-gateway/.deployed_commit").read().strip()
        if not out["candidate_bytes_equal_release"]:
            out["stop"] = "candidate bytes differ from the release blobs"
            return out
        out["pct_before"] = m.host_pct()
        if out["pct_before"] >= m.STOP_PCT:
            out["stop"] = "host at or above %.0f percent used" % m.STOP_PCT
            return out
        out["probe"] = run_child(["--probe", cand])
        out["pct_mid1"] = m.host_pct()
        out["oldform_live"] = run_child(["--oldform", live])
        out["pct_mid2"] = m.host_pct()
        if out["pct_mid2"] >= m.STOP_PCT:
            out["stop"] = "host at or above %.0f percent used before the candidate old-form child" % m.STOP_PCT
            return out
        out["oldform_candidate"] = run_child(["--oldform", cand])
        out["pct_after"] = m.host_pct()
        pid1, nr1 = read_pid()
        out["service"] = {"pid_before": pid0, "pid_after": pid1, "pid_stable": pid0 == pid1, "nrestarts_before": nr0, "nrestarts_after": nr1}
    finally:
        for st in (cand, live):
            shutil.rmtree(st, ignore_errors=True)
        out["scratch_removed"] = not (os.path.exists(cand) or os.path.exists(live))
    return out


def runner(outp, expect_path):
    import boto3
    here = os.path.dirname(os.path.abspath(__file__))
    s3 = boto3.client("s3")
    expect = json.load(io.open(expect_path, encoding="utf-8"))
    for n in ("rl19_host.py", "ap38_measure.py", "ap38_guard.py", "rl19_sk2_probe.py"):
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/" + n, Body=io.open(os.path.join(here, n), "rb").read())
    expect["sha256"] = {}
    for rel in OVERLAY:
        body = io.open(TREE + rel, "rb").read()
        expect["sha256"][rel] = hashlib.sha256(body).hexdigest()
        s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + rel.replace("/", "__"), Body=body)
    s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + "org_standards_contract.json", Body=io.open(expect["standards_copy_file"], "rb").read())
    s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + "base_contract.json", Body=io.open(expect["base_contract_file"], "rb").read())
    s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + "expect.json", Body=json.dumps(expect).encode("utf-8"))
    pulls = ["aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (m.BUCKET, n, n) for n in ("rl19_host.py", "ap38_measure.py", "ap38_guard.py", "rl19_sk2_probe.py")]
    pulls += ["mkdir -p /tmp/rl19_cand", "aws s3 cp s3://%s/%sexpect.json /tmp/rl19_expect.json --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX),
              "aws s3 cp s3://%s/%sbase_contract.json /tmp/rl19_base_contract.json --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX),
              "aws s3 cp s3://%s/%sorg_standards_contract.json /tmp/rl19_cand/org_standards_contract.json --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX)]
    pulls += ["aws s3 cp s3://%s/%s%s /tmp/rl19_cand/%s --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX, r.replace("/", "__"), r.replace("/", "__")) for r in OVERLAY]
    cmd = ("cd /opt/opal-gateway && rm -rf /tmp/rl19_host.py /tmp/ap38_measure.py /tmp/ap38_guard.py /tmp/rl19_sk2_probe.py /tmp/rl19_cand /tmp/rl19_expect.json /tmp/rl19_base_contract.json && %s && %s /tmp/rl19_host.py --driver; rc=$?; rm -rf /tmp/rl19_cand /tmp/rl19_expect.json /tmp/rl19_base_contract.json /tmp/rl19_sk2_probe.py; exit $rc"
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
    if "RL19_HOST_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-400:]))
    doc = json.loads(so.split("RL19_HOST_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    doc["captured_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1)[:3000])


if __name__ == "__main__":
    if "--probe" in sys.argv:
        child_probe(sys.argv[sys.argv.index("--probe") + 1])
    elif "--oldform" in sys.argv:
        child_oldform(sys.argv[sys.argv.index("--oldform") + 1])
    elif "--driver" in sys.argv:
        print("RL19_HOST_JSON")
        try:
            print(json.dumps(driver(), separators=(",", ":"), default=str))
        except Exception:
            import traceback
            print(json.dumps({"fatal": traceback.format_exc()[-800:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1], sys.argv[2])
