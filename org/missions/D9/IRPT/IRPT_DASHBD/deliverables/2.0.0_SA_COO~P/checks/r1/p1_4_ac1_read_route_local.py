"""IRPT_DASHBD round 1 AC (DB-b-4, FWD-1 hop 3) -- the read function hands the page the REAL series and manifest for an account the
viewer's scope covers, and refuses one it does not, invoked locally against the real S3 objects.

Usage: python p1_4_ac1_read_route_local.py <worktree root>
Imports <root>/infra/aws/lambda/investor-reporting/reporting/entry.py (the worker's module) and calls its documented local entry
`serve_series(account_id, scope_accounts, which)` where `which` is "series" or "manifest":
  - ("0027265115", {"0027265115"}, "series")   -> bytes equal to the S3 object at the builder's address (gzip, byte-for-byte);
  - ("0027265115", {"0027265115"}, "manifest") -> bytes equal to the manifest object;
  - ("0027265115", {"0000000000"}, "series")   -> raises entry.AccountNotCovered (the refusal branch; no S3 read is made).
The module must expose ROUTES with exactly one route key and register function name irpt-49f-reporting-read-lambda.
Also reads the worker's saved plan org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/reporting-read.plan.txt:
"0 to destroy" and an aws_lambda_function creation named irpt-49f-reporting-read-lambda.
Pass line: DB-4-AC1 PASS. Base (at the cut): FAIL -- no module.
"""
import importlib.util
import re
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(root))


def _thread_account(root):
    """The thread account: the seat's record deliverables/0.4.0_DS_ClientPlatform~S/THREAD_ACCOUNT.json ({"thread_account": "..."}),
    chosen by census in DB-b-1 (issuer amendment 1, 2026-09-30 17:1xZ); the roster's first account is the fallback."""
    import json as _json
    p = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.4.0_DS_ClientPlatform~S/THREAD_ACCOUNT.json"
    try:
        return str(_json.loads(p.read_text(encoding="utf-8"))["thread_account"])
    except Exception:  # noqa: BLE001
        return "0027265115"
THREAD = _thread_account(root)
SRC = root / "infra/aws/lambda/investor-reporting/reporting/entry.py"
PLAN = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/reporting-read.plan.txt"


def fail(msg):
    print("DB-4-AC1 FAIL: " + msg)
    sys.exit(1)


if not SRC.exists():
    fail("module absent: %s" % SRC)
spec = importlib.util.spec_from_file_location("reporting_entry_under_test", SRC)
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
except Exception as exc:  # noqa: BLE001
    fail("module does not import: %s" % str(exc)[:200])
if not hasattr(mod, "serve_series") or not hasattr(mod, "AccountNotCovered") or not hasattr(mod, "ROUTES"):
    fail("module lacks serve_series / AccountNotCovered / ROUTES")
if len(mod.ROUTES) != 1:
    fail("ROUTES has %d keys (want 1)" % len(mod.ROUTES))
if getattr(mod, "FUNCTION_NAME", None) != "irpt-49f-reporting-read-lambda":
    fail("FUNCTION_NAME %r != irpt-49f-reporting-read-lambda" % getattr(mod, "FUNCTION_NAME", None))

from lib import opal_naming as on  # noqa: E402
import boto3  # noqa: E402

s3 = boto3.client("s3", region_name="us-east-1")


def get(uri):
    b, k = uri[5:].split("/", 1)
    return s3.get_object(Bucket=b, Key=k)["Body"].read()


want_series = get(on.address("irpt", "49financial", "platinum", "reporting", "account=%s" % THREAD, "series.json.gz"))
want_manifest = get(on.address("irpt", "49financial", "platinum", "reporting", "account=%s" % THREAD, "manifest.json"))
got = mod.serve_series(THREAD, {THREAD}, "series")
if got != want_series:
    fail("series bytes differ from the S3 object (%d vs %d bytes)" % (len(got), len(want_series)))
got_m = mod.serve_series(THREAD, {THREAD}, "manifest")
if got_m != want_manifest:
    fail("manifest bytes differ from the S3 object")
try:
    mod.serve_series(THREAD, {"0000000000"}, "series")
    fail("an uncovered account was SERVED (no AccountNotCovered)")
except mod.AccountNotCovered:
    pass
print("  series %d bytes and manifest %d bytes served byte-equal; uncovered account refused" % (len(got), len(got_m)))
if not PLAN.exists():
    fail("plan file absent: %s" % PLAN)
txt = PLAN.read_text(encoding="utf-8", errors="replace")
m = re.search(r"Plan: (\d+) to add, (\d+) to change, (\d+) to destroy", txt)
if not m or int(m.group(3)) != 0:
    fail("plan missing or destroys resources")
if "irpt-49f-reporting-read-lambda" not in txt or not re.search(r"aws_lambda_function\.\S+ will be created", txt):
    fail("plan does not create irpt-49f-reporting-read-lambda")
print("  plan: %s to add, 0 to destroy, function named" % m.group(1))
print("DB-4-AC1 PASS")
