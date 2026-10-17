#!/usr/bin/env python
"""OG-ap-34 Phase A step 2: the host-shaped import check. Builds the host layout /<tmp>/a/b/c/opal-gateway/{app,lib}
twice (WITH and WITHOUT lib/opal_naming.py), imports every taken module and app.tools in a FRESH interpreter,
and exercises the client tools' firm resolution. Zero reads: boto3.client is replaced by a counter that records and refuses."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile

TREE = "C:/tmp/og-rel-batch5"
GW = TREE + "/infra/aws/ec2/opal-gateway"
MODS = ["client_core", "client_role", "client_adapter_bd49f", "data_entitlement", "integrations.opal_discover.integration", "server", "tools"]

CHILD = r'''
import json, sys, importlib, types
root = sys.argv[1]
sys.path.insert(0, root)
reads = []
import boto3
def _refuse(*a, **k):
    reads.append(a[:1]); raise RuntimeError("a read was attempted in the zero-read check")
boto3.client = _refuse; boto3.resource = _refuse
out = {"imported": [], "failed": []}
for m in json.loads(sys.argv[2]):
    try:
        importlib.import_module("app." + m); out["imported"].append(m)
    except BaseException as exc:
        out["failed"].append([m, type(exc).__name__, str(exc)[:160]])
from app import client_core as cc
out["vendors"] = list(cc.registered_vendors())
firms = {}
for v in cc.registered_vendors():
    for mod in cc._adapters[v]:
        try:
            firms[mod.__name__.split(".")[-1]] = sorted(cc._firms_of(mod))
        except cc.CoreRefusal as exc:
            firms[mod.__name__.split(".")[-1]] = "REFUSED:" + exc.code
        except BaseException as exc:
            firms[mod.__name__.split(".")[-1]] = "ERR:" + type(exc).__name__ + ":" + str(exc)[:80]
out["firms"] = firms
try:
    r = cc.client_resolve_account("49 Financial", "1234")
    out["resolve_probe"] = {"keys": sorted(r)[:8], "refused": r.get("refused") or r.get("absent_reason") or r.get("error")}
except BaseException as exc:
    out["resolve_probe"] = "RAISED:" + type(exc).__name__ + ":" + str(exc)[:100]
out["reads"] = len(reads)
print("JSON:" + json.dumps(out))
'''


def build(with_naming: bool) -> str:
    d = tempfile.mkdtemp(prefix="hostshape_")
    root = os.path.join(d, "a", "b", "c", "opal-gateway")
    shutil.copytree(GW + "/app", root + "/app", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    os.makedirs(root + "/lib")
    shutil.copy(TREE + "/lib/trading_calendar.py", root + "/lib/trading_calendar.py")
    if with_naming:
        shutil.copy(TREE + "/lib/opal_naming.py", root + "/lib/opal_naming.py")
    return root


res = {}
for label, wn in (("with_opal_naming", True), ("without_opal_naming", False)):
    root = build(wn)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, "-c", CHILD, root, json.dumps(MODS)], capture_output=True, env=env,
                       cwd=os.path.dirname(root))
    txt = r.stdout.decode("utf-8", "replace")
    line = next((ln for ln in txt.splitlines() if ln.startswith("JSON:")), None)
    res[label] = json.loads(line[5:]) if line else {"error": (r.stderr.decode("utf-8", "replace") or txt)[-600:]}
    res[label]["scopes_json_present"] = os.path.isfile(root + "/app/refs/scopes.json")
    res[label]["opal_naming_present"] = os.path.isfile(root + "/lib/opal_naming.py")
    res[label]["trading_calendar_present"] = os.path.isfile(root + "/lib/trading_calendar.py")
    shutil.rmtree(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(root)))), ignore_errors=True)
json.dump(res, open(sys.argv[1], "w"), indent=1)
for k, v in res.items():
    print(k, "imported %s/%s failed %s reads %s" % (len(v.get("imported", [])), len(MODS), v.get("failed"), v.get("reads")))
    print("  vendors", v.get("vendors"))
    print("  firms", json.dumps(v.get("firms"))[:600])
    print("  probe", json.dumps(v.get("resolve_probe"))[:300])
    if "error" in v:
        print("  ERROR", v["error"])
