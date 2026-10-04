"""AMGT_CORPUS round 36, CRPS-al-5 -- the /thesis payload serves `model.fiscal_unresolved`. Issuer's file.

  python al5_served.py --where local|deployed
`deployed` invokes the live `opal-amgt-scoped-api` through AMGT_RESAPP's capture helper (`capture_lib._invoke`, the instrument
r66/r67 grade the deployed function with); `local` calls `scoped_amgt.handler` in-process. For 1299_HK_Equity and BA_US_Equity:
  b1  `model.fiscal_unresolved` equals (as a multiset of (mnemonic, fiscal_year, reason)) the newest block's fiscal-scope
      `unresolved` entries -- 1299 HK non-empty, BA empty.
  c1  `model.fiscal_year_figures` length equals the block's fiscal-scope figure count (nothing else in the slice moved).
Prints one line per arm, then `al5 <where> build <p>/1 control <q>/1`.
"""
import argparse
import collections
import importlib.util
import subprocess
import sys

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
sys.path.insert(0, TOP)
from lib.research.api import scoped_amgt  # noqa: E402
from lib.research.checkface.scopes import SCOPE_FISCAL_YEAR_LINE_ITEM  # noqa: E402

CAPTURE_LIB = TOP + "/org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PREFIX = "/api/scoped/amgt"
KEYS = ("1299_HK_Equity", "BA_US_Equity")

ap = argparse.ArgumentParser()
ap.add_argument("--where", choices=("local", "deployed"), required=True)
a = ap.parse_args()

if a.where == "deployed":
    import boto3

    spec = importlib.util.spec_from_file_location("capture_lib", CAPTURE_LIB)
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    lam = boto3.client("lambda", region_name=cl.REGION)

    def call(path):
        body, meta = cl._invoke(lam, path, None)
        return (200, body) if body is not None else (meta.get("status"), None)
else:
    import json

    def call(path):
        r = scoped_amgt.handler({"rawPath": path, "requestContext": {"http": {"method": "GET"}},
                                 "headers": {"x-firm-id": "opal"}, "queryStringParameters": None})
        try:
            return r.get("statusCode"), json.loads(r.get("body") or "null")
        except ValueError:
            return r.get("statusCode"), None

b1, c1 = True, True
b1_notes, c1_notes = [], []
for key in KEYS:
    block = scoped_amgt.read_model_block(key) or {}
    want = collections.Counter(
        (u.get("mnemonic"), str(u.get("fiscal_year")), u.get("reason"))
        for u in block.get("unresolved", []) if u.get("scope") == SCOPE_FISCAL_YEAR_LINE_ITEM
    )
    status, body = call("%s/security/%s/thesis" % (PREFIX, key))
    model = (body or {}).get("model") if isinstance(body, dict) else None
    served = (model or {}).get("fiscal_unresolved")
    if status != 200 or not isinstance(served, list):
        b1 = False
        b1_notes.append("%s status %s fiscal_unresolved %s" % (key, status, "absent" if served is None else type(served).__name__))
    else:
        got = collections.Counter((u.get("mnemonic"), str(u.get("fiscal_year")), u.get("reason")) for u in served)
        if got != want or (key == "1299_HK_Equity" and not want):
            b1 = False
        b1_notes.append("%s served %d block %d" % (key, sum(got.values()), sum(want.values())))
    fiscal_block = sum(1 for f in block.get("figures", []) if f.get("scope") == SCOPE_FISCAL_YEAR_LINE_ITEM)
    fiscal_served = len((model or {}).get("fiscal_year_figures") or [])
    if fiscal_block != fiscal_served:
        c1 = False
    c1_notes.append("%s fiscal_year_figures %d block %d" % (key, fiscal_served, fiscal_block))

print("ARM b1 %s %s" % ("PASS" if b1 else "FAIL", b1_notes))
print("ARM c1 %s %s" % ("PASS" if c1 else "FAIL", c1_notes))
print("al5 %s build %d/1 control %d/1" % (a.where, int(b1), int(c1)))
