"""AMGT_CORPUS round 28 -- the Model-tab census at base, over the newest block of every key (read-only).

  -> 'REFUSE <unit_status> | <mnemonic> | <reason-head> n' per refusal signature over fiscal-year figures
  -> 'NULLROW <label> <mnemonic> names_with_figure n of K' for the five rows modelSheet.ts maps to null
  -> 'r28 keys K fiscal_figures F refuse R refuse_zero_sample Z'
"""
import collections
import json
import subprocess
import sys

import boto3

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
sys.path.insert(0, TOP)
from lib.research.checkface.run_checks import unit_status_for  # noqa: E402

B = "opal-data-harvest"
P = "derived/model_block/"
CAND = [("Revenue/Sh", "REVENUE_PER_SH"), ("FCF yield", "FREE_CASH_FLOW_YIELD"), ("FCF margin", "FREE_CASH_FLOW_MARGIN"),
        ("RoTA", "RETURN_ON_TANGIBLE_ASSETS"), ("Earnings margin", "PROF_MARGIN")]

s3 = boto3.client("s3")
stamps = collections.defaultdict(list)
for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix=P):
    for o in pg.get("Contents", []):
        rest = o["Key"][len(P):]
        if rest.endswith("/model_block.json"):
            k = rest.rsplit("/", 2)[0]
            if "/" not in k:
                stamps[k].append(o["Key"])
sig = collections.Counter()
have = collections.Counter()
figs = refuse = zs = 0
for k in sorted(stamps):
    blk = json.loads(s3.get_object(Bucket=B, Key=max(stamps[k]))["Body"].read())
    fy = [f for f in blk.get("figures", []) if f.get("scope") == "fiscal_year_line_item"]
    mns = {f.get("mnemonic") for f in fy if f.get("value") is not None}
    for _, m in CAND:
        have[m] += int(m in mns)
    for f in fy:
        figs += 1
        st = unit_status_for(f)
        if st not in ("MEASURED", "PENDING"):
            refuse += 1
            why = str(f.get("sign") if st == "SIGN-UNRESOLVED" else f.get("unit")).split(": ", 1)[-1][:60]
            zs += int("exactly zero" in why)
            sig["%s | %s | %s" % (st, f.get("mnemonic"), why)] += 1
for s, n in sorted(sig.items(), key=lambda x: -x[1])[:40]:
    print("REFUSE %s %d" % (s, n))
for lab, m in CAND:
    print("NULLROW %s %s names_with_figure %d of %d" % (lab, m, have[m], len(stamps)))
print("r28 keys %d fiscal_figures %d refuse %d refuse_zero_sample %d" % (len(stamps), figs, refuse, zs))
