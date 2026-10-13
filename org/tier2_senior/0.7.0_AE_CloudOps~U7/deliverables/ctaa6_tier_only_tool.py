#!/usr/bin/env python3
"""NFRA_CTLPLN TO-CT-aa-6 exercise tool (copy of ctaa4_dev_fence_tool.py for the tier-only fence): reuses ctu7_fence_tool.py and ctw10_logging_fix_tool.py. ASCII only.

Subcommands:
  row-create | row-delete   one synthetic partner row (firm 49financial, tier advisor), same rules as before.
  walker                    the UI walker row AS IT IS: arm, real login, print the NON-SECRET claim values the
                            fence reads (tier, userType, role, firmId), read one class-(ii) route, disarm.
  partner                   the synthetic partner caller on the same class-(ii) route.
  logread <apply_epoch>     counts of the log events written after the apply (jwt_shaped, bearer).
No token or password value is printed or stored. The decoded claims are read from the walker's own access token
in memory; only the four named claim values are printed.
"""
from __future__ import annotations

import base64
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ctw10_logging_fix_tool as w  # noqa: E402
import ctu7_fence_tool as t  # noqa: E402

t.EMAIL = "ctlpln-ctaa6-tierfence-20261013@opal.invalid"
t.PK = "USER#" + t.EMAIL
t.NAME = "NFRA_CTLPLN CT-aa-6 synthetic partner caller"
t.NAME_PREFIX = "NFRA_CTLPLN CT-aa-6 synthetic"
t.CENSUS_TOKEN = "ctlpln-ctaa6"
t.CREATED_BY = "0.7.0_AE_CloudOps~U7 NFRA_CTLPLN CT-aa-6 (first pair CTO half section 2 option a)"


def _claims(token):
    seg = token.split(".")[1]
    seg += "=" * (-len(seg) % 4)
    obj = json.loads(base64.urlsafe_b64decode(seg.encode("ascii")))
    return {k: obj.get(k, "<ABSENT>") for k in ("tier", "userType", "role", "firmId")}


def walker(label):
    arm = t._walker("arm")
    holder = ""
    for line in arm.stdout.splitlines():
        if line.startswith("HOLDER "):
            holder = line.split(" ", 1)[1].strip()
    t._stamp("WALKER-ARM", "holder_present=%s rc=%d" % (bool(holder), arm.returncode))
    if not holder:
        raise SystemExit("STOP: walker not armed: %s" % (arm.stdout + arm.stderr)[:120])
    code = -1
    try:
        itok = t._internal_login()
        t._stamp("WALKER-CLAIMS", "token claim values the fence reads: %s" % json.dumps(_claims(itok), sort_keys=True))
        code = t._report("%s class-ii walker row as it is" % label, t.ROUTE_II, *t._get(itok, t.ROUTE_II))
        del itok
    finally:
        dis = t._walker("disarm", holder)
        for line in (dis.stdout + dis.stderr).splitlines():
            t._stamp("WALKER-DISARM", line[:160])
    print("walker class-ii=%d" % code)


def partner():
    ptok = t._mint()
    code = t._report("R2 class-ii partner (synthetic row)", t.ROUTE_II, *t._get(ptok, t.ROUTE_II))
    del ptok
    print("partner=%d" % code)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "logread":
        w.logread(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "walker":
        walker(sys.argv[2])
    elif len(sys.argv) == 2 and sys.argv[1] in ("row-create", "partner", "row-delete"):
        {"row-create": t.row_create, "partner": partner, "row-delete": t.row_delete}[sys.argv[1]]()
    else:
        raise SystemExit("usage: ctaa6_dev_fence_tool.py row-create|partner|row-delete | walker <label> | logread <apply_epoch>")
