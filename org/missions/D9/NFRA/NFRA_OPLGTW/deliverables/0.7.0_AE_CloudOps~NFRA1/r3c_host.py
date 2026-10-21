#!/usr/bin/env python
"""OG-rl-19 Phase B host reads, each in a FRESH process under the cgroup HARD GUARD (ap38_guard.py --cgroup inside a transient systemd scope, MemoryMax=1400M, oom_score_adj 1000, wall limit 120 s), from a SCRATCH copy of the service's own
app/, lib/ and deploy/ (removed after). READ ONLY: S3 GetObject/ListBucket/HeadObject through the gateway's own assumed roles; the access-state store is replaced by a stub that answers nothing and writes nothing (Catalog.snapshot would
otherwise persist a snapshot record); NO SSM write; the running service is not touched; NOTHING arms the probe listener. COUNTS, CODES and DATES only: no object content is printed.
  gate     the GATE READ: as the catalog role (the gateway's assume path), ONE GetObject of schwab/49financial/state/complete/date=2026-10-20/08403355.complete.json and ONE ListBucket with prefix schwab/49financial/state/complete/ on opal-data-49financial
  dual     the DUAL READ measurement for 08403355 and the two old-form masters: list_dates (count, newest), the newest date's snapshot status, and where the marker is read from
  probe    the sk2.AC1 python verbatim on the tree as it is on the host plus trunk's standards copy (13 labelled lines; the planted second-master file is ignored)
  python r3c_host.py <gate|dual|probe> <out.json> <expect.json>      -> RUNNER (repository root)
  python r3c_host.py --driver <mode> | --child <mode> <stage>"""
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

S3_PREFIX = "ec2/opal-gateway/r3c_cand/"
MASTERS = ("08403355", "08242234", "08335338")
GATE_BUCKET, GATE_KEY, GATE_PREFIX = "opal-data-49financial", "schwab/49financial/state/complete/date=2026-10-20/08403355.complete.json", "schwab/49financial/state/complete/"


def code_of(exc):
    resp = getattr(exc, "response", None) or {}
    return str((resp.get("Error") or {}).get("Code") or type(exc).__name__)


def child_gate(stage):
    os.environ.setdefault("MOCK_GRAPH", "1")
    m.load_env(stage)
    from app.integrations.schwab import aws_roles
    from app.integrations.schwab import catalog as cat
    contract = cat.load_contract()
    configs = aws_roles.role_configs(contract.raw, aws_roles.environ_with_external_ids(os.environ))
    role = aws_roles.AssumedRole(configs[aws_roles.CATALOG])
    s3 = role.session(lambda: True).client("s3")
    out = {"as_role": "gateway-schwab-catalog-read-role", "bucket": GATE_BUCKET, "prefix": GATE_PREFIX, "role_kind": configs[aws_roles.CATALOG].kind}
    try:
        s3.get_object(Bucket=GATE_BUCKET, Key=GATE_KEY)
        out["get_object"] = "FOUND"
    except Exception as exc:  # noqa: BLE001
        out["get_object"] = code_of(exc)
    try:
        page = s3.list_objects_v2(Bucket=GATE_BUCKET, Prefix=GATE_PREFIX, MaxKeys=5)
        out["list_key_count"] = len(page.get("Contents") or [])
        out["list_error"] = None
    except Exception as exc:  # noqa: BLE001
        out["list_key_count"] = None
        out["list_error"] = code_of(exc)
    out["vm_hwm_mb"] = round(m.hwm_mb(), 1)
    m.emit(out)


class StubStore:
    """Answers nothing and writes nothing: the catalog's snapshot cache is empty and persist() is a no-op."""

    def __getattr__(self, name):
        def call(*a, **k):
            return None
        return call


def child_dual(stage):
    os.environ.setdefault("MOCK_GRAPH", "1")
    m.load_env(stage)
    from app.integrations.schwab import aws_roles
    from app.integrations.schwab import catalog as cat
    contract = cat.load_contract()
    configs = aws_roles.role_configs(contract.raw, aws_roles.environ_with_external_ids(os.environ))
    catalog = cat.Catalog(contract=contract, catalog_role=aws_roles.AssumedRole(configs[aws_roles.CATALOG]), data_role=aws_roles.AssumedRole(configs[aws_roles.READER]), store=StubStore())
    out = {"code_has_firm_form": hasattr(cat, "firm_form_masters"), "firm_form_masters": (cat.firm_form_masters(contract) if hasattr(cat, "firm_form_masters") else {}), "masters": {}}
    for master in MASTERS:
        rec = {}
        try:
            dates = catalog.list_dates(master, lambda: True)
            rec["dates"], rec["newest"] = len(dates), (dates[0] if dates else None)
            rec["oldest"] = dates[-1] if dates else None
            if dates:
                res = catalog.snapshot(master, dates[0], lambda: True)
                rec["snapshot_status"], rec["snapshot_result"] = str(getattr(res, "status", None)), str(getattr(res, "result", None))
                rec["snapshot_files"] = len((getattr(res, "snapshot", None) or {}).get("files") or []) if isinstance(getattr(res, "snapshot", None), dict) else None
                if hasattr(catalog, "read_marker"):
                    _marker, _ver, located = catalog.read_marker(master, dates[0], lambda: True)
                    rec["marker_location"] = "old" if (located and located[0] == contract.bucket) else ("new" if located else None)
                else:
                    rec["marker_location"] = "old"
        except Exception as exc:  # noqa: BLE001
            rec["error"] = "%s: %s" % (type(exc).__name__, str(exc)[:120])
        out["masters"][master] = rec
    out["vm_hwm_mb"] = round(m.hwm_mb(), 1)
    m.emit(out)


def child_probe(stage):
    os.environ.setdefault("MOCK_GRAPH", "1")
    os.environ["SK2_BASE_CONTRACT"] = "/tmp/r3c_base_contract.json"
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
    planted = [ln for ln in labelled if "PLANTED" in ln]
    m.emit({"lines": len(labelled), "ok": sum(1 for ln in labelled if ": NOT OK" not in ln), "not_ok": [ln[:80] for ln in labelled if ": NOT OK" in ln], "final": lines[-1] if lines else None,
            "planted_second_master_lines": len(planted), "planted_second_master_ignored": bool(planted) and all(": NOT OK" not in ln for ln in planted), "vm_hwm_mb": round(m.hwm_mb(), 1)})


def run_child(args, wall=120):
    cmd = ["systemd-run", "--scope", "--quiet", "-p", "MemoryMax=1400M", "-p", "MemoryHigh=1100M", "-p", "MemorySwapMax=0", "--", m.PY, m.GUARD, "--cgroup", str(wall), os.path.abspath(__file__)] + args
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=wall + 60)
    lines = [ln for ln in p.stdout.splitlines() if ln.startswith("AP38_RESULT ")]
    res = json.loads(lines[-1].split(" ", 1)[1]) if lines else {"no_result": True, "stdout_tail": p.stdout[-300:], "stderr_tail": p.stderr[-500:]}
    res["exit_code"] = p.returncode
    return res


def driver(mode):
    out = {"mode": mode, "guard": m.CGROUP_GUARD_NAME, "scratch_removed": False}
    stage = "/tmp/r3c_stage_%d" % os.getpid()
    try:
        out["marker_host"] = open("/opt/opal-gateway/.deployed_commit").read().strip()
        os.makedirs(stage, mode=0o700)
        for d in ("app", "lib", "deploy"):
            shutil.copytree("/opt/opal-gateway/" + d, stage + "/" + d, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        if mode == "probe":
            os.makedirs(stage + "/org/standards", exist_ok=True)
            shutil.copyfile("/tmp/r3c_std_contract.json", stage + "/org/standards/NFRA_OPLGTW_CONTRACT.json")
        out["pct_before"] = m.host_pct()
        if out["pct_before"] >= m.STOP_PCT:
            out["stop"] = "host at or above %.0f percent used" % m.STOP_PCT
            return out
        out["result"] = run_child(["--child", mode, stage])
        out["pct_after"] = m.host_pct()
    finally:
        shutil.rmtree(stage, ignore_errors=True)
        out["scratch_removed"] = not os.path.exists(stage)
    return out


def runner(mode, outp, expect_path):
    import boto3
    here = os.path.dirname(os.path.abspath(__file__))
    s3 = boto3.client("s3")
    expect = json.load(io.open(expect_path, encoding="utf-8"))
    for n in ("r3c_host.py", "ap38_measure.py", "ap38_guard.py", "rl19_sk2_probe.py"):
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/" + n, Body=io.open(os.path.join(here, n), "rb").read())
    s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + "std_contract.json", Body=io.open(expect["standards_copy_file"], "rb").read())
    s3.put_object(Bucket=m.BUCKET, Key=S3_PREFIX + "base_contract.json", Body=io.open(expect["base_contract_file"], "rb").read())
    pulls = ["aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (m.BUCKET, n, n) for n in ("r3c_host.py", "ap38_measure.py", "ap38_guard.py", "rl19_sk2_probe.py")]
    pulls += ["aws s3 cp s3://%s/%sstd_contract.json /tmp/r3c_std_contract.json --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX),
              "aws s3 cp s3://%s/%sbase_contract.json /tmp/r3c_base_contract.json --region us-east-1 >/dev/null" % (m.BUCKET, S3_PREFIX)]
    cmd = ("cd /opt/opal-gateway && rm -f /tmp/r3c_host.py /tmp/ap38_measure.py /tmp/ap38_guard.py /tmp/rl19_sk2_probe.py /tmp/r3c_std_contract.json /tmp/r3c_base_contract.json && %s && %s /tmp/r3c_host.py --driver %s; rc=$?; "
           "rm -f /tmp/r3c_std_contract.json /tmp/r3c_base_contract.json /tmp/rl19_sk2_probe.py; exit $rc" % (" && ".join(pulls), m.PY, mode))
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
    if "R3C_HOST_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-400:]))
    doc = json.loads(so.split("R3C_HOST_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    doc["captured_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc))


if __name__ == "__main__":
    if "--child" in sys.argv:
        i = sys.argv.index("--child")
        {"gate": child_gate, "dual": child_dual, "probe": child_probe}[sys.argv[i + 1]](sys.argv[i + 2])
    elif "--driver" in sys.argv:
        print("R3C_HOST_JSON")
        try:
            print(json.dumps(driver(sys.argv[sys.argv.index("--driver") + 1]), separators=(",", ":"), default=str))
        except Exception:
            import traceback
            print(json.dumps({"fatal": traceback.format_exc()[-800:]}))
            sys.exit(1)
    else:
        runner(sys.argv[1], sys.argv[2], sys.argv[3])
