"""IRPT_ANLREQ TO-APPLY-R37 (applier 0.7.0_AE_CloudOps~IB2): the reads and the record of the irpt-ycharts-generate release.

  python r37.py r0       R0 before-reads: clock, live CodeSha256, the key's version list (whole JSON), the PRE-WINDOW ZIP (saved under the scratch folder), the credential-less envelope
  python r37.py after    V after-reads G1 to G4 (the live object against the PRE-WINDOW ZIP member by member, the envelope, the function CodeSha256)

State lives in state_r37.json beside this file. The API base is imported from the AQ2 sitting module, never typed. Nothing secret, no signed URL is printed or stored:
the envelope is recorded as a status and a body sha256 only.
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import sys
import urllib.error
import urllib.request
import zipfile
import base64
from datetime import datetime, timezone
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
STATE = HERE / "state_r37.json"
SCRATCH = Path("C:/Users/Test/AppData/Local/Temp/r37_scratch")
REGION = "us-east-1"
BUCKET, KEY = "opal-313476888478-lambda-artifacts", "investor-reporting/irpt-ycharts-generate.zip"
FN = "irpt-ycharts-generate"
BEFORE_SHA = "kxOEgpbspky10PYWQ28y0+7V2UXG28whJ2riMa4CkTE="
AFTER_SHA = "PlCjNms/RRLRB/c15zW8Sdzl7w3ptodi3o8sSxnWjYA="
AFTER_ZIP_SHA = "3e50a3366b3f4512d107f735e735bc49dce5ef0de9b68762de8f2c4b19d68d80"
MOVERS = ["served.py", "ticket_confirmation.py"]


def utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load():
    return json.loads(STATE.read_text(encoding="ascii")) if STATE.exists() else {}


def save(d):
    STATE.write_text(json.dumps(d, indent=1, sort_keys=True) + "\n", encoding="ascii")


def envelope():
    spec = importlib.util.spec_from_file_location("aq2_r28", str(ROOT / "org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r28/sitting_r28.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["aq2_r28"] = mod
    spec.loader.exec_module(mod)
    req = urllib.request.Request(mod.BASE + "/api/scoped/investor-reporting/analysis/inputs?selected_tenant=49financial", data=b"{}", method="POST",
                                 headers={"Content-Type": "application/json", "Accept": "application/json", "X-Contract-Version": "v1"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            status, raw = r.status, r.read()
    except urllib.error.HTTPError as e:
        status, raw = e.code, e.read()
    return {"status": status, "body_sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def r0():
    now = datetime.now(timezone.utc)
    s3, lam = boto3.client("s3", region_name=REGION), boto3.client("lambda", region_name=REGION)
    d = {"clock_utc": utc(), "weekday": now.strftime("%A")}
    d["function_codesha256"] = lam.get_function(FunctionName=FN)["Configuration"]["CodeSha256"]
    d["function_equals_expected"] = d["function_codesha256"] == BEFORE_SHA
    vs, marks = [], []
    for pg in s3.get_paginator("list_object_versions").paginate(Bucket=BUCKET, Prefix=KEY):
        vs += [v for v in pg.get("Versions", []) if v["Key"] == KEY]
        marks += [v for v in pg.get("DeleteMarkers", []) if v["Key"] == KEY]
    latest = [v for v in vs if v["IsLatest"]]
    d["versions"] = len(vs)
    d["delete_markers"] = len(marks)
    d["latest_version_id"] = latest[0]["VersionId"] if latest else None
    d["latest_size"] = latest[0]["Size"] if latest else None
    SCRATCH.mkdir(parents=True, exist_ok=True)
    body = s3.get_object(Bucket=BUCKET, Key=KEY, VersionId=d["latest_version_id"])["Body"].read()
    (SCRATCH / "pre_window.zip").write_bytes(body)
    d["pre_window_codesha256"] = base64.b64encode(hashlib.sha256(body).digest()).decode("ascii")
    d["pre_window_equals_live"] = d["pre_window_codesha256"] == d["function_codesha256"]
    z = zipfile.ZipFile(io.BytesIO(body))
    d["pre_window_members"] = len(z.namelist())
    d["envelope_before"] = envelope()
    save(d)
    print(json.dumps({k: v for k, v in d.items()}, sort_keys=True))
    ok = d["function_equals_expected"] and d["pre_window_equals_live"] and d["pre_window_members"] == 107
    print("R0 %s" % ("GREEN" if ok else "RED"))
    return 0 if ok else 3


def after():
    d = load()
    s3, lam = boto3.client("s3", region_name=REGION), boto3.client("lambda", region_name=REGION)
    d["g1_codesha256"] = lam.get_function(FunctionName=FN)["Configuration"]["CodeSha256"]
    d["g1_ok"] = d["g1_codesha256"] == AFTER_SHA
    vs = []
    for pg in s3.get_paginator("list_object_versions").paginate(Bucket=BUCKET, Prefix=KEY):
        vs += [v for v in pg.get("Versions", []) if v["Key"] == KEY]
    latest = [v for v in vs if v["IsLatest"]][0]
    d["uploaded_version_id"] = latest["VersionId"]
    live = s3.get_object(Bucket=BUCKET, Key=KEY, VersionId=latest["VersionId"])["Body"].read()
    d["live_object_sha256"] = hashlib.sha256(live).hexdigest()
    d["live_object_sha256_ok"] = d["live_object_sha256"] == AFTER_ZIP_SHA
    pre = zipfile.ZipFile(SCRATCH / "pre_window.zip")
    cur = zipfile.ZipFile(io.BytesIO(live))
    a, b = set(pre.namelist()), set(cur.namelist())
    differ = sorted(n for n in a & b if pre.read(n) != cur.read(n))
    d["g2_members_pre"], d["g2_members_live"] = len(a), len(b)
    d["g2_added"], d["g2_removed"] = sorted(b - a), sorted(a - b)
    d["g2_differ"] = differ
    d["g2_ok"] = [n.split("/")[-1] for n in differ] == MOVERS or sorted(n.split("/")[-1] for n in differ) == sorted(MOVERS)
    d["g2_ok"] = d["g2_ok"] and not d["g2_added"] and not d["g2_removed"] and len(a) == 107
    d["envelope_after"] = envelope()
    d["g3_ok"] = d["envelope_after"] == d.get("envelope_before")
    save(d)
    print(json.dumps({k: v for k, v in d.items() if k.startswith(("g", "uploaded", "live"))}, sort_keys=True))
    return 0 if (d["g1_ok"] and d["g2_ok"] and d["g3_ok"] and d["live_object_sha256_ok"]) else 3


if __name__ == "__main__":
    sys.exit({"r0": r0, "after": after}[sys.argv[1]]())
