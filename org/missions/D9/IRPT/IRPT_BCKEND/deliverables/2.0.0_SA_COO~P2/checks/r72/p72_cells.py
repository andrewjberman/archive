"""IRPT_BCKEND round 72 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cells IB-pr-355 (the scoped read of a retained
CUSTODY_REPORT by ref, irpt-export-render) and IB-pr-356 (the print page resolves and mounts it), per 1.0.0_SA_CTO~DELL2 ruling msg 973
(option (a)) on row W162-S1. IB-pr-356 supersedes IB-pr-353.

THE SHARED CONTRACT (both cells build to it):
  route    GET /api/scoped/investor-reporting/custody-report/{reportId}   query: revision=<revision>
  op       custody-report-read          handler irpt-export-render
  200 body {"report_kind": "CUSTODY_REPORT", "report_id": ..., "revision": ..., "report": <the custody document>}
  refusal  another firm, or an account the caller's scope does not cover -> the export's OBJECT_NOT_COVERED envelope

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Every check finishes inside 120 s.

  IB72-1-AC1  export/tests/test_custody_read.py exists, names OBJECT_NOT_COVERED and custody-report-read, and passes with
              test_submit_custody_report.py (one process) and _authz/tests/test_unguarded_census.py (a second). Base: FAIL (no test).
  IB72-1-AC2  docs/contracts/investor-reporting/v1/routes.json names the route key with handler irpt-export-render and operation
              custody-report-read, and export/entry.py ROUTES maps the same key to the same operation. Base: FAIL (absent).
  IB72-2-AC1  portal __tests__/ir-72-custody-print/ holds a test naming custody-report, ClientReportDocument and resolveBundle; it and the
              ir-66 print-kind test pass with `bun --no-install test`. Base: FAIL (folder absent).
  IB72-2-AC2  in portal/: tsc -b --noEmit exits 0, and eslint on PrintEntry.tsx, resolveBundle.ts and manifest.ts exits 0. Base: PASS.
  IB72-3-AC1  _authz/tests/test_response_envelope_public_status.py exists, names internal_correlation_id and response_envelope, and
              passes; _authz/tests/test_unguarded_census.py passes in a second process. Base: FAIL (no test). (IB-pr-357, row
              IRPT_YCDGEN-S16, CTO msg 998.)
  IB72-4-AC1  intake/tests/test_upload_door_reads_allowed_firms.py exists, names allowedFirmIds, profile_reader and analysis-input-upload,
              and passes with _scope/tests/test_interactive_access_on_behalf.py. Base: FAIL (no test). (IB-pr-358, row W163-S1.)
  IB72-G-<n>  A GUARD for slot ~<n> (164, 165, 166): that worker's workspace commits touch only its grant, never the portal gitlink. Base: PASS.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "0d2aff87b3"
P = "org/missions/D9/IRPT/IRPT_BCKEND"
IR = "infra/aws/lambda/investor-reporting"
CONTRACT = "docs/contracts/investor-reporting/v1/routes.json"
ROUTE = "GET /api/scoped/investor-reporting/custody-report/{reportId}"
OP = "custody-report-read"
PT = "src/pages/InvestorReporting/__tests__/"
CH = P + "/surprise-channel/investigations/INVESTIGATION_v1.md"
TO = P + "/task-orders/IRPT_BCKEND.TO-IB-pr-"
GRANTS = {
    "164": (IR + "/export/custody_read.py", IR + "/export/entry.py", IR + "/export/tests/test_custody_read.py", CONTRACT, CH,
            TO + "355.", P + "/deliverables/0.9.0_WK_IRPT_BCKEND~164/"),
    "165": (CH, TO + "356.", P + "/deliverables/0.9.0_WK_IRPT_BCKEND~165/"),
    "166": (IR + "/_authz/served.py", IR + "/_authz/tests/test_response_envelope_public_status.py",
            IR + "/reports/generate_installed.py", IR + "/ycharts/generate/prospect_submission.py", IR + "/intake/upload_resolution.py",
            IR + "/intake/tests/test_upload_door_reads_allowed_firms.py", CH, TO + "357.", TO + "358.",
            P + "/deliverables/0.9.0_WK_IRPT_BCKEND~166/"),
}


def _run(cmd, cwd, timeout=110):
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, timeout=timeout)
    out = (r.stdout or b"").decode("utf-8", "replace") + (r.stderr or b"").decode("utf-8", "replace")
    return r.returncode, re.sub(r"\x1b\[[0-9;]*m", "", out)


def _last(out):
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return lines[-1] if lines else "(no output)"


def _routes(doc):
    items = doc.get("routes", doc) if isinstance(doc, dict) else doc
    return items if isinstance(items, list) else []


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB72"))
        sys.exit(1)

    if cid == "IB72-1-AC1":
        t = root / IR / "export/tests/test_custody_read.py"
        if not t.is_file():
            fail("no %s/export/tests/test_custody_read.py" % IR)
        src = t.read_text(encoding="utf-8")
        for need in ("OBJECT_NOT_COVERED", OP):
            if need not in src:
                fail("the test never names %s" % need)
        # Two processes: the export tests and the _authz route census share module names, so one pytest session pollutes
        # the other (measured at base 0d2aff87b3: test_submit_custody_report passes alone, fails beside the census).
        lasts = []
        for cwd, targets in ((root / IR / "export", ["tests/test_custody_read.py", "tests/test_submit_custody_report.py"]),
                             (root / IR, ["_authz/tests/test_unguarded_census.py"])):
            rc, out = _run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *targets], cwd)
            last = _last(out)
            if rc or "passed" not in last or re.search(r"\d+ (failed|error)", last):
                fail("tests (%s): %s" % (targets[0], last))
            lasts.append(last)
        print("OK: export %s; census %s" % tuple(lasts))
    elif cid == "IB72-1-AC2":
        doc = json.loads((root / CONTRACT).read_text(encoding="utf-8"))
        hit = [r for r in _routes(doc) if isinstance(r, dict) and r.get("route_key") == ROUTE]
        if len(hit) != 1:
            fail("routes.json names %r %d time(s)" % (ROUTE, len(hit)))
        if hit[0].get("handler") != "irpt-export-render" or hit[0].get("operation") != OP:
            fail("routes.json row: handler %r operation %r" % (hit[0].get("handler"), hit[0].get("operation")))
        entry = (root / IR / "export/entry.py").read_text(encoding="utf-8")
        block = entry[entry.index("ROUTES = {"):entry.index("}", entry.index("ROUTES = {"))]
        if ROUTE not in block or OP not in block:
            fail("export/entry.py ROUTES does not map the route to %s" % OP)
        print("OK: routes.json and entry.ROUTES both map %s -> %s" % (ROUTE, OP))
    elif cid == "IB72-2-AC1":
        portal = root / "portal"
        d = portal / PT / "ir-72-custody-print"
        tests = sorted(d.glob("*.test.ts*")) if d.is_dir() else []
        if not tests:
            fail("no portal test under portal/%sir-72-custody-print/" % PT)
        text = "\n".join(x.read_text(encoding="utf-8") for x in tests)
        for need in ("custody-report", "ClientReportDocument", "resolveBundle"):
            if need not in text:
                fail("the test does not name %s" % need)
        rc, out = _run(["bun", "--no-install", "test", PT + "ir-72-custody-print/", PT + "ir-66-print-kind/"], portal)
        m = re.search(r"(\d+) pass", out)
        f = re.search(r"(\d+) fail", out)
        if rc or not m or (f and int(f.group(1)) > 0):
            fail("bun test rc %d: %s" % (rc, _last(out)))
        print("OK: %s pass, %s fail" % (m.group(1), f.group(1) if f else "0"))
    elif cid == "IB72-2-AC2":
        portal = root / "portal"
        rc, out = _run(["node", "node_modules/typescript/bin/tsc", "-b", "--noEmit"], portal, timeout=115)
        if rc:
            fail("tsc -b --noEmit rc %d: %s" % (rc, _last(out)))
        rc, out = _run(["node", "node_modules/eslint/bin/eslint.js", "src/pages/InvestorReporting/render/PrintEntry.tsx",
                        "src/pages/InvestorReporting/export/resolveBundle.ts", "src/pages/InvestorReporting/render/manifest.ts"],
                       portal)
        if rc:
            fail("eslint rc %d: %s" % (rc, _last(out)))
        print("OK: tsc -b --noEmit rc 0; eslint on the three files rc 0")
    elif cid == "IB72-3-AC1":
        t = root / IR / "_authz/tests/test_response_envelope_public_status.py"
        if not t.is_file():
            fail("no %s/_authz/tests/test_response_envelope_public_status.py" % IR)
        src = t.read_text(encoding="utf-8")
        for need in ("internal_correlation_id", "response_envelope"):
            if need not in src:
                fail("the test never names %s" % need)
        lasts = []
        for targets in (["_authz/tests/test_response_envelope_public_status.py"], ["_authz/tests/test_unguarded_census.py"]):
            rc, out = _run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *targets], root / IR)
            last = _last(out)
            if rc or "passed" not in last or re.search(r"\d+ (failed|error)", last):
                fail("tests (%s): %s" % (targets[0], last))
            lasts.append(last)
        print("OK: envelope %s; census %s" % tuple(lasts))
    elif cid == "IB72-4-AC1":
        t = root / IR / "intake/tests/test_upload_door_reads_allowed_firms.py"
        if not t.is_file():
            fail("no %s/intake/tests/test_upload_door_reads_allowed_firms.py" % IR)
        src = t.read_text(encoding="utf-8")
        for need in ("allowedFirmIds", "profile_reader", "analysis-input-upload"):
            if need not in src:
                fail("the test never names %s" % need)
        rc, out = _run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                        "intake/tests/test_upload_door_reads_allowed_firms.py",
                        "_scope/tests/test_interactive_access_on_behalf.py"], root / IR)
        last = _last(out)
        if rc or "passed" not in last or re.search(r"\d+ (failed|error)", last):
            fail("tests: %s" % last)
        print("OK: %s" % last)
    elif cid.startswith("IB72-G-"):
        slot = cid.rsplit("-", 1)[1]
        grant = GRANTS.get(slot)
        if not grant:
            fail("unknown slot %r" % slot)
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=0.9.0_WK_IRPT_BCKEND~%s" % slot, "--name-only", "--format="],
                           cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if not c.startswith(grant) or c == "portal"]
        if bad:
            fail("out-of-grant changes (the portal gitlink is never committed): %s" % bad[:8])
        print("OK: %d changed path(s), all inside slot ~%s's grant" % (len(changed), slot))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
