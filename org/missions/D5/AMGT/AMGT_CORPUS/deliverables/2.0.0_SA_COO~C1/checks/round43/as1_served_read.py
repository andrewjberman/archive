"""AMGT_CORPUS round 43, CRPS-as-1 -- the served /9 read (round-42 analysis s.2 item 1). Issuer's file. Read-only.

GET-shaped direct invokes of the DEPLOYED function `opal-amgt-scoped-api` (round 40's ap10d_live_route.py invoke shape), route
/api/scoped/amgt/security/<key>/thesis, field dossier_fields.management, for three names:
  BABA_US_Equity  must EQUAL its /9 NEW line in evidence/r42_ar2_changes_whole_20261009.txt (the prefix dropped: opens "Eddie Wu")
  SHOP_CN_Equity  must EQUAL its /9 NEW line there (its sentence read to its end)
  8766_JP_Equity  must EQUAL the stored /7 value (row D1-W1-S3: the trailing comma unchanged from /7)
and, for BABA and SHOP, the served value must not end in "..." and must not open with a scorecard label.
Prints the function's LastModified and CodeSha256, one line per name, then `as1 served <m>/3`. NO write.

  PYTHONPATH=. python as1_served_read.py
"""
import json
import os
import re
import sys
import types

sys.modules.setdefault("fitz", types.ModuleType("fitz"))

import boto3  # noqa: E402

from lib.research.corpus import dossier  # noqa: E402
from lib.research.harvest import store  # noqa: E402

FN = "opal-amgt-scoped-api"
HERE = os.path.dirname(os.path.abspath(__file__))
PRE = os.path.join(os.path.dirname(os.path.dirname(HERE)), "evidence", "r42_ar2_changes_whole_20261009.txt")
RE_PREFIX = re.compile(r"^[A-Z][A-Za-z/&\- ]{2,40} \d{1,3} (?=[A-Z])")


def _pre_new(key, name):
    t = open(PRE, encoding="utf-8").read()
    for blk in t.split("=== ")[1:]:
        head, rest = blk.split("\n", 1)
        _n, k, f = head.split()
        if (k, f) == (key, name):
            return re.search(r"NEW:    (.*?)(?:\n=== |\nar2 |\Z)", rest + "\n", re.S).group(1).rstrip("\n")
    return None


def _stored_v7(key):
    current = dossier.METHOD_VERSION
    dossier.METHOD_VERSION = "amgt-corpus-dossier/7"
    try:
        doc = dossier.read_dossier(key, client=store._default_client())["document"]
    finally:
        dossier.METHOD_VERSION = current
    return ((doc.get("fields") or {}).get("management") or {}).get("value")


def _served(lam, key):
    event = {"rawPath": "/api/scoped/amgt/security/%s/thesis" % key, "requestContext": {"http": {"method": "GET"}},
             "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
    raw = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    body = raw.get("body")
    payload = json.loads(body) if isinstance(body, str) else body
    fields = (payload or {}).get("dossier_fields") or {}
    entry = fields.get("management") if isinstance(fields, dict) else None
    return raw.get("statusCode"), (entry or {}).get("value") if isinstance(entry, dict) else None


def main():
    lam = boto3.client("lambda", region_name="us-east-1")
    cfg = lam.get_function_configuration(FunctionName=FN)
    print("function %s LastModified %s CodeSha256 %s" % (FN, cfg.get("LastModified"), cfg.get("CodeSha256")))
    want = {"BABA_US_Equity": _pre_new("BABA_US_Equity", "management"),
            "SHOP_CN_Equity": _pre_new("SHOP_CN_Equity", "management"),
            "8766_JP_Equity": _stored_v7("8766_JP_Equity")}
    met = 0
    for key, expect in want.items():
        status, got = _served(lam, key)
        ok = isinstance(got, str) and got == expect
        if key != "8766_JP_Equity" and isinstance(got, str):
            ok = ok and not got.rstrip().endswith("...") and not RE_PREFIX.match(got)
        met += int(ok)
        head = got[:40] if isinstance(got, str) else got
        tail = got[-60:] if isinstance(got, str) else got
        print("%-16s http %s %s | len %s opens %r ends %r | expected len %s" % (
            key, status, "MATCH" if ok else "DIFFERS", len(got) if isinstance(got, str) else None, head, tail,
            len(expect) if isinstance(expect, str) else None))
    print("as1 served %d/3" % met)
    return 0 if met == 3 else 1


if __name__ == "__main__":
    sys.exit(main())
