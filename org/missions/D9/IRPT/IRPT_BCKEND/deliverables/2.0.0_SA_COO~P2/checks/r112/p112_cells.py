"""IRPT_BCKEND round 112 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order (IRPT_DASHBD ADDENDUM 12 item 3, CTO msg 3370; W64-S1):
  IB112-1  IB-pr-411  persist_inputs.report_index carries the stored object's sha256 (the persist response already returns it);
                      contract updated (worker ~274)

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB112-1-AC1  `pytest ops/tests -k report_index_sha256` (investor-reporting) passes >= 2 tests. Base: FAIL (0 selected).
  IB112-1-AC2  ops/tests passes in full and `_contracts -k persist_inputs` passes. Base: PASS (control).
  IB112-1-AC3  docs/contracts/investor-reporting/v1/OwnedAnalysisRequest.schema.json: persist_inputs.report_index (non-null branch)
               declares a required `sha256` with a 64-hex pattern. Base: FAIL.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

IR = "infra/aws/lambda/investor-reporting"
SCHEMA = "docs/contracts/investor-reporting/v1/OwnedAnalysisRequest.schema.json"


def pyt(cwd, *args):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args], cwd=str(cwd), capture_output=True,
                       timeout=280)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace")).strip().splitlines()
    last = out[-1] if out else ""
    m = re.search(r"\b(\d+) passed", last)
    return p.returncode, (int(m.group(1)) if m else 0), last


def walk(node):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB112"))
        sys.exit(1)

    if cid == "IB112-1-AC1":
        rc, n, last = pyt(root / IR, "ops/tests", "-k", "report_index_sha256")
        if rc != 0 or n < 2:
            fail("-k report_index_sha256 rc %d: %s" % (rc, last))
        print("OK: %s" % last)
    elif cid == "IB112-1-AC2":
        rc, n, last = pyt(root / IR, "ops/tests")
        if rc != 0:
            fail("ops/tests rc %d: %s" % (rc, last))
        rc2, n2, last2 = pyt(root / IR, "_contracts", "-k", "persist_inputs")
        if rc2 != 0 or n2 < 1:
            fail("_contracts -k persist_inputs rc %d: %s" % (rc2, last2))
        print("OK: ops %s; contracts %s" % (last, last2))
    elif cid == "IB112-1-AC3":
        doc = json.loads((root / SCHEMA).read_text(encoding="utf-8"))
        ok = False
        for node in walk(doc):
            props = node.get("properties") if isinstance(node.get("properties"), dict) else {}
            if {"report_id", "revision", "retention_ref"} <= set(props):
                sha = props.get("sha256") or {}
                if "sha256" in (node.get("required") or []) and "64" in str(sha.get("pattern", "")):
                    ok = True
        if not ok:
            fail("no report_index object declares a required 64-hex sha256")
        print("OK: report_index declares sha256")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
