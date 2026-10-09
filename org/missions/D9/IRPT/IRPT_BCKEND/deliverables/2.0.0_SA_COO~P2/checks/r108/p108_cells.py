"""IRPT_BCKEND round 108 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order (CTO ADDENDUM 17, msg 3220):
  IB108-1  IB-pr-407  publish IB-pr-405's include=persist_inputs: the read route's routes.json entry and its response schema
                      (worker ~270)

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB108-1-AC1  `pytest _contracts -k persist_inputs` (investor-reporting) passes >= 2 tests. Base: FAIL (0 selected).
  IB108-1-AC2  _authz/tests/test_unguarded_census.py and ops/tests/test_persist_inputs.py pass. Base: PASS (control).
  IB108-1-AC3  docs/contracts/investor-reporting/v1/routes.json's analysis-request-read entry names persist_inputs in its query, and
               its response schema declares a `persist_inputs` property. Base: FAIL.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

IR = "infra/aws/lambda/investor-reporting"
CON = "docs/contracts/investor-reporting/v1/"
KEY = "GET /api/scoped/investor-reporting/analysis/requests/{requestId}"


def pyt(cwd, *args):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args], cwd=str(cwd), capture_output=True,
                       timeout=280)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace")).strip().splitlines()
    last = out[-1] if out else ""
    m = re.search(r"\b(\d+) passed", last)
    return p.returncode, (int(m.group(1)) if m else 0), last


def props(node, seen=0):
    """Every property name declared anywhere in a JSON schema (local refs are not followed)."""
    found = set()
    if isinstance(node, dict):
        found |= set((node.get("properties") or {}).keys())
        for v in node.values():
            found |= props(v)
    elif isinstance(node, list):
        for v in node:
            found |= props(v)
    return found


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB108"))
        sys.exit(1)

    if cid == "IB108-1-AC1":
        rc, n, last = pyt(root / IR, "_contracts", "-k", "persist_inputs")
        if rc != 0 or n < 2:
            fail("-k persist_inputs rc %d: %s" % (rc, last))
        print("OK: %s" % last)
    elif cid == "IB108-1-AC2":
        rc, n, last = pyt(root / IR, "_authz/tests/test_unguarded_census.py", "ops/tests/test_persist_inputs.py")
        if rc != 0:
            fail("rc %d: %s" % (rc, last))
        print("OK: %s" % last)
    elif cid == "IB108-1-AC3":
        doc = json.loads((root / CON / "routes.json").read_text(encoding="utf-8"))
        rows = [r for r in (doc.get("routes") if isinstance(doc, dict) else doc) or [] if isinstance(r, dict) and r.get("route_key") == KEY]
        if len(rows) != 1:
            fail("%d routes.json row(s) for %s" % (len(rows), KEY))
        row = rows[0]
        if "persist_inputs" not in json.dumps(row.get("query") or {}):
            fail("query does not name persist_inputs")
        sp = root / CON / str(row.get("response_schema") or "")
        if not sp.is_file():
            fail("no response schema %s" % sp)
        if "persist_inputs" not in props(json.loads(sp.read_text(encoding="utf-8"))):
            fail("response schema declares no persist_inputs property")
        print("OK: routes.json query and response schema publish persist_inputs")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
