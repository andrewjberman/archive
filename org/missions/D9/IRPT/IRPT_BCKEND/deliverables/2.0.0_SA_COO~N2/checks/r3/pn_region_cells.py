"""IRPT_BCKEND workstream ~PN round 5 (issuer 2.0.0_SA_COO~N2) -- the checks of the BUILD cell IB-pn-3.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL: <reason>" last, exit 0 or 1.
The second scheduled run of the Scope feed (2026-10-17 11:33Z chain) died at `boto3.client("secretsmanager")` in session_token(): the
runner has no default AWS region (botocore NoRegionError). The in-runner import smoke could not see it (no client was built).

  IBN3-AC1  in the runner's flat layout, with every AWS_* variable removed and no AWS config file, session_token() builds its REAL
            boto3 client (the API call itself is replaced, so no network) and returns; at base it raises NoRegionError
  IBN3-AC2  every boto3.client / boto3.resource / boto3.Session call in the feed script names region_name (static, covers the
            paths a run does not reach)
  IBN3-AC3  the new tests (at least 3) and the feed's four existing test files pass, and the worker's record names only paths
            inside the grant
"""
import ast
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r1"))
import pn1_cells as P1  # noqa: E402  (flat_dir, SCRIPT, F, EXISTING)

SCRIPT = P1.SCRIPT
NEW_TEST = P1.F + "test_scope_feed_region.py"
EXISTING = P1.EXISTING + [P1.NEW_TEST]
SLOT = 481
RECORD = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~%d/IBN3-1_record.json" % SLOT
ALLOWED = {SCRIPT, NEW_TEST, "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pn-3.scope-feed-region.md"}
SMOKE = r"""
import base64, importlib.util, json, os, sys, time
src_path, flat = sys.argv[1], sys.argv[2]
for key in list(os.environ):
    if key.startswith("AWS_"):
        del os.environ[key]
os.environ.update({"AWS_ACCESS_KEY_ID": "x", "AWS_SECRET_ACCESS_KEY": "y",
                   "AWS_CONFIG_FILE": os.path.join(flat, "no_config"),
                   "AWS_SHARED_CREDENTIALS_FILE": os.path.join(flat, "no_credentials"),
                   "HOME": flat, "USERPROFILE": flat})
sys.path.insert(0, flat)
spec = importlib.util.spec_from_file_location("scope_feed_region_smoke", src_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
import botocore.client


def part(value):
    return base64.urlsafe_b64encode(json.dumps(value).encode()).decode().rstrip("=")


token = part({"alg": "none"}) + "." + part({"exp": int(time.time()) + 3600}) + ".sig"
botocore.client.BaseClient._make_api_call = lambda self, operation, params: {"SecretString": token}
module.session_token()
print("REGION-OK")
"""


def fail(cid, why):
    print("%s FAIL: %s" % (cid, why))
    sys.exit(1)


def ac1(root):
    with tempfile.TemporaryDirectory() as tmp:
        flat = P1.flat_dir(root, tmp)
        out = subprocess.run([sys.executable, "-I", "-c", SMOKE, str(flat / Path(SCRIPT).name), str(flat)], cwd=str(flat),
                             capture_output=True, text=True, timeout=100)
    if out.returncode != 0 or "REGION-OK" not in out.stdout:
        fail("IBN3-AC1", (out.stderr.strip().splitlines() or ["no output"])[-1])


def ac2(root):
    tree = ast.parse((root / SCRIPT).read_text(encoding="utf-8"))
    missing = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in ("client", "resource", "Session"):
            owner = node.func.value
            if isinstance(owner, ast.Name) and owner.id == "boto3":
                if not any(kw.arg == "region_name" for kw in node.keywords):
                    missing.append("line %d boto3.%s" % (node.lineno, node.func.attr))
    if missing:
        fail("IBN3-AC2", "no region_name: " + ", ".join(missing))


def ac3(root):
    new = root / NEW_TEST
    if not new.is_file():
        fail("IBN3-AC3", "new test file absent")
    count = new.read_text(encoding="utf-8").count("\ndef test_")
    if count < 3:
        fail("IBN3-AC3", "new test file holds %d tests, need at least 3" % count)
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", NEW_TEST] + EXISTING, cwd=str(root),
                         capture_output=True, text=True, timeout=110)
    if out.returncode != 0:
        fail("IBN3-AC3", "pytest rc=%d: %s" % (out.returncode, (out.stdout.strip().splitlines() or ["no output"])[-1]))
    record = root / RECORD
    if not record.is_file():
        fail("IBN3-AC3", "record absent: " + RECORD)
    data = json.loads(record.read_text(encoding="utf-8"))
    changed = data.get("changed_paths", [])
    outside = [p for p in changed if p not in ALLOWED]
    if outside or SCRIPT not in changed:
        fail("IBN3-AC3", "changed_paths outside the grant or missing the script: %s" % outside)


CHECKS = {"IBN3-AC1": ac1, "IBN3-AC2": ac2, "IBN3-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: pn_region_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    CHECKS[sys.argv[2]](Path(sys.argv[1]).resolve())
    print("%s PASS" % sys.argv[2])
