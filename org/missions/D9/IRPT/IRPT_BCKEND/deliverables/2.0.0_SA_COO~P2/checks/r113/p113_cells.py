"""IRPT_BCKEND round 113 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order (CTO ADDENDUM 18/19; red list IB109-1, ~P2's NAMED entries):
  IB113-1  IB-pr-412  publish responses/custody-report-read and custody-report-persist response contracts; routes.json keeps
                      response_schema null for both (worker ~275)

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB113-1-AC1  `pytest _contracts/tests/test_seam_paired.py -k custody` (investor-reporting) passes, with >= 2 selected. Base: FAIL.
  IB113-1-AC2  `pytest _contracts -rf`: the failing set is a subset of the two entries this cell does not own (the route census test and
               the analysis-request-original control), and the custody controls are not in it. Base: FAIL (custody controls red).
  IB113-1-AC3  routes.json rows for custody-report-read and custody-report-persist still read response_schema null (portal wire
               generator unchanged). Base: PASS (control).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

IR = "infra/aws/lambda/investor-reporting"
ROUTES = "docs/contracts/investor-reporting/v1/routes.json"
NOT_MINE = ("test_every_declared_route_has_a_response_contract_whose_refs_resolve", "[analysis-request-original]")


def run(cwd, *args):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args], cwd=str(cwd), capture_output=True,
                       timeout=580)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace"))
    return p.returncode, out


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB113"))
        sys.exit(1)

    if cid == "IB113-1-AC1":
        rc, out = run(root / IR, "_contracts/tests/test_seam_paired.py", "-k", "custody")
        last = out.strip().splitlines()[-1] if out.strip() else ""
        m = re.search(r"\b(\d+) passed", last)
        if rc != 0 or not m or int(m.group(1)) < 2:
            fail("rc %d: %s" % (rc, last))
        print("OK: %s" % last)
    elif cid == "IB113-1-AC2":
        rc, out = run(root / IR, "_contracts", "-rf")
        failed = [m.group(1) for m in re.finditer(r"^FAILED (\S+)", out, re.M)]
        mine = [f for f in failed if not any(n in f for n in NOT_MINE)]
        if mine:
            fail("red beyond the two not owned: %s" % mine)
        if any("custody" in f for f in failed):
            fail("a custody test is red")
        print("OK: %d red, all outside this cell (%s)" % (len(failed), ", ".join(f.split("::")[-1] for f in failed)))
    elif cid == "IB113-1-AC3":
        doc = json.loads((root / ROUTES).read_text(encoding="utf-8"))
        rows = {r.get("operation"): r for r in doc.get("routes") or [] if isinstance(r, dict)}
        for op in ("custody-report-read", "custody-report-persist"):
            if op not in rows or rows[op].get("response_schema") is not None:
                fail("%s row %r" % (op, rows.get(op, {}).get("response_schema", "ABSENT")))
        print("OK: both custody rows keep response_schema null")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
