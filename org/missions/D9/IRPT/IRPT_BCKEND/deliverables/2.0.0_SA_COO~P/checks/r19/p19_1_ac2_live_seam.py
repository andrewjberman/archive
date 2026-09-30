"""IB-pr-191 AC2 -- the seam probe against the REAL neighbour: the 49F engine's live twr_daily, read-only.

Usage: python p19_1_ac2_live_seam.py <worktree root>
Reads s3 (registry address: opal_naming.lookup('49financial') bucket + advi gold_root) through the package's own
EngineSource and calculate(). No write, no vendor call. Window: YTD at the latest partition.

Arm A: the NEW-01 account (row S177: OK r_net -1.0 on 2026-04-16) refuses as EngineReturnImplausible.
Arm B (control): an invested account of similar size with no r_net <= -1 day computes a finite value above -1.
"""
import math
import sys
from pathlib import Path

import boto3

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _engine_path import install  # noqa: E402

install(sys.argv[1] if len(sys.argv) > 1 else ".")
import f49_engine as f49  # noqa: E402
import tenants  # noqa: E402
from ids import opaque_account  # noqa: E402
from opal_naming import lookup  # noqa: E402

BAD, GOOD = "0049615236", "0010498003"
firm = lookup("49financial")
src_args = dict(bucket=firm["bucket"], root=firm["trees"]["advi"]["gold_root"])
s3 = boto3.client("s3")
latest = f49.EngineSource(s3, **src_args).partition_dates()[-1]
start = latest[:4] + "-01-01"
ok = True


def run(raw):
    account = opaque_account(tenants._CANONICAL_49F, raw)
    scope = {"verified_request_firm_id": tenants._LEGACY_SHORT_ID["49F"], "permitted_account_set": [account],
             "resolved_scope": {"scope_ids": [account]}}
    return f49.calculate(scope, start, latest, f49.EngineSource(s3, **src_args))


cls = getattr(f49, "EngineReturnImplausible", None)
try:
    out = run(BAD)
    print("FAIL A: YTD %s..%s SERVED %r for the NEW-01 account" % (start, latest,
          out["report"]["returns"]["account_detail"][0]["value"]))
    ok = False
except Exception as exc:
    if cls is not None and isinstance(exc, cls):
        print("PASS A: YTD %s..%s refuses as %s" % (start, latest, type(exc).__name__))
    else:
        print("FAIL A: refused as %s, not EngineReturnImplausible" % type(exc).__name__)
        ok = False

try:
    value = run(GOOD)["report"]["returns"]["account_detail"][0]["value"]
    if math.isfinite(value) and value > -1.0:
        print("PASS B: control YTD %s..%s computes %.6f" % (start, latest, value))
    else:
        print("FAIL B: control computes %r" % value)
        ok = False
except Exception as exc:
    print("FAIL B: control refused as %s" % type(exc).__name__)
    ok = False

if ok:
    print("P19-1-AC2 PASS")
else:
    print("P19-1-AC2 FAIL")
sys.exit(0 if ok else 1)
