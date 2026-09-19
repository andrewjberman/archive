"""DIAGNOSTIC ONLY (operator credentials, never a proof): the DEPLOYED zip bytes + the DEPLOYED layer (mapped onto a local
stand-in for /opt/python) + the DEPLOYED environment, run in-process OUTSIDE the repository (so no walk-up can find a repo
copy of the registry), with the boundary's recorder patched to print the swallowed exception.
Modes: bare | +raw_keys.json | +raw_keys.json +firm_registry.json, each member the HEAD blob placed at the package root.
Answers, per function: what the deployed path raises today, and whether the proposed staged members make the scope resolve."""
from __future__ import annotations

import importlib
import io
import json
import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile

import boto3

WS = r"C:\tmp\wk-irpt-6-ae1"
ROOT = sys.argv[1]
FN = sys.argv[2]
ROUTE = sys.argv[3]
MODE = sys.argv[4]  # bare | raw | raw+reg
BODY = json.loads(sys.argv[5]) if len(sys.argv) > 5 else None
lam = boto3.client("lambda", region_name="us-east-1")
cfg = lam.get_function_configuration(FunctionName=FN)
base = os.path.join(ROOT, FN + "-" + MODE.replace("+", "_"))
shutil.rmtree(base, ignore_errors=True)
task, opt = os.path.join(base, "var_task"), os.path.join(base, "opt")
os.makedirs(task)
os.makedirs(opt)
zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(lam.get_function(FunctionName=FN)["Code"]["Location"], timeout=120).read())).extractall(task)
for layer in cfg.get("Layers") or []:
    lv = lam.get_layer_version_by_arn(Arn=layer["Arn"])
    zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(lv["Content"]["Location"], timeout=120).read())).extractall(opt)


def head_blob(path: str) -> bytes:
    return subprocess.run(["git", "show", "HEAD:" + path], cwd=WS, capture_output=True, check=True).stdout


if MODE in ("raw", "raw+reg"):
    open(os.path.join(task, "raw_keys.json"), "wb").write(head_blob("infra/aws/lambda/investor-reporting/_ids/raw_keys.json"))
if MODE == "raw+reg":
    open(os.path.join(task, "firm_registry.json"), "wb").write(head_blob("data/firm_registry.json"))
env = dict((cfg.get("Environment") or {}).get("Variables") or {})
for k, v in list(env.items()):
    if isinstance(v, str) and v.startswith("/opt/"):
        env[k] = os.path.join(opt, v[len("/opt/"):].replace("/", os.sep))
    elif isinstance(v, str) and v.startswith("/var/task/"):
        env[k] = os.path.join(task, v[len("/var/task/"):].replace("/", os.sep))
for k, v in env.items():
    os.environ[k] = v
sys.path[:0] = [task, os.path.join(opt, "python")]
captured = []
for m in ("errors",):
    try:
        em = importlib.import_module(m)
        orig = em.record_internal

        def rec(sink, cid, op, exc, _orig=orig):
            captured.append("%s: %s" % (type(exc).__module__ + "." + type(exc).__name__, str(exc)[:220]))
            return _orig(sink, cid, op, exc)
        em.record_internal = rec
    except ImportError:
        pass
where = {}
for m in ("ids", "keys"):
    try:
        where[m] = "var_task" if importlib.import_module(m).__file__.startswith(task) else "layer"
    except Exception as exc:  # noqa: BLE001
        where[m] = "IMPORT FAILED %s" % type(exc).__name__
mod_name, fn_name = cfg["Handler"].rsplit(".", 1)
method, path = ROUTE.split(" ", 1)
concrete = path.replace("{accountSetId}", "acc_diag").replace("{reportId}", "rep_diag").replace("{exportId}", "EXP-diag").replace("{jobId}", "REQ-diag")
event = {"version": "2.0", "routeKey": ROUTE, "rawPath": concrete, "rawQueryString": "",
         "headers": {"x-contract-version": "v1", "x-firm-id": "49financial", "x-advisor-id": "abby_horton", "x-user-role": "user",
                     "content-type": "application/json"},
         "pathParameters": {k: v for k, v in (("accountSetId", "acc_diag"), ("reportId", "rep_diag"), ("exportId", "EXP-diag"), ("jobId", "REQ-diag")) if "{" + k + "}" in path},
         "requestContext": {"http": {"method": method, "path": concrete}, "routeKey": ROUTE,
                            "authorizer": {"lambda": {"firmId": "49financial", "advisorId": "abby_horton", "role": "user"}}},
         "body": json.dumps(BODY) if BODY is not None else None, "isBase64Encoded": False}
try:
    res = getattr(importlib.import_module(mod_name), fn_name)(event, None)
    body = res.get("body") if isinstance(res, dict) else None
    j = json.loads(body) if isinstance(body, str) else res
    code = ((j or {}).get("status") or {}).get("public_reason_code") if isinstance(j, dict) else None
    firm = (j or {}).get("firm_id") if isinstance(j, dict) else None
    verdict = "SCOPE-RESOLVED" if firm else ("UNEXPECTED" if code == "UNEXPECTED" else "NOT RESOLVED")
except Exception as exc:  # noqa: BLE001
    code, firm, verdict = "HANDLER RAISED %s" % type(exc).__name__, None, "RAISED"
print("%-26s %-8s ids.py from %-8s keys.py from %-8s -> %-15s code %-22s firm_id %s | swallowed: %s" % (
    FN, MODE, where.get("ids"), where.get("keys"), verdict, code, "present" if firm else "ABSENT", captured[-1] if captured else "none"))
