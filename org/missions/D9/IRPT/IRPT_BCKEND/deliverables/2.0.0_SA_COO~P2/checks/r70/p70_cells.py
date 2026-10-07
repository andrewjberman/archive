"""IRPT_BCKEND round 70 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cells IB-pr-351 (P-c1: the custody write path),
IB-pr-352 (P-c2: accept reads the business date by kind) and IB-pr-353 (P-c3: PrintEntry mounts the custody template), per the
CTO's IRPT_CUSTDY round-6 addendum 1 @c3addc6f25 ruling item 2 (breaks 1, 2 and 4 of IRPT_CUSTDY-S14).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Every check finishes inside 120 s.

  IB70-1-AC1  reports/tests/test_custody_write.py exists, names CUSTODY_REPORT, as_of_date and retained_export.resolve, and passes;
              the reports suite and export/tests/test_submit_custody_report.py pass. Base: FAIL (no test).
  IB70-2-AC1  export/tests/test_accept_business_date.py exists, calls submit_async.accept and names as_of_date and actual_end, and
              passes; export/tests/test_submit_custody_report.py still passes. Base: FAIL (no test).
  IB70-3-AC1  portal/src/pages/InvestorReporting/__tests__/ir-70-custody-print/ holds a test naming custody-report and
              ClientReportDocument; it and the ir-66 print-kind test pass with `bun --no-install test`. Base: FAIL (folder absent).
  IB70-3-AC2  in portal/: tsc -b --noEmit exits 0, and eslint on render/PrintEntry.tsx exits 0. Base: PASS (a control).
  IB70-G-<n>  A GUARD for slot ~<n>: that worker's own workspace commits touch only its grant, never the portal gitlink. Base: PASS.
"""
import re
import subprocess
import sys
from pathlib import Path

BASE = "c09237491c"
P = "org/missions/D9/IRPT/IRPT_BCKEND"
IR = "infra/aws/lambda/investor-reporting"
CH = P + "/surprise-channel/investigations/INVESTIGATION_v1.md"
TO = P + "/task-orders/IRPT_BCKEND.TO-IB-pr-"
PT = "src/pages/InvestorReporting/__tests__/"
GRANTS = {
    "150": (IR + "/reports/custody_write.py", IR + "/reports/tests/test_custody_write.py", CH, TO + "351.",
            P + "/deliverables/0.9.0_WK_IRPT_BCKEND~150/"),
    "151": (IR + "/export/submit_async.py", IR + "/export/tests/test_accept_business_date.py", CH, TO + "352.",
            P + "/deliverables/0.9.0_WK_IRPT_BCKEND~151/"),
    "152": (CH, TO + "353.", P + "/deliverables/0.9.0_WK_IRPT_BCKEND~152/"),
}


def _run(cmd, cwd, timeout=110):
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, timeout=timeout)
    out = (r.stdout or b"").decode("utf-8", "replace") + (r.stderr or b"").decode("utf-8", "replace")
    return r.returncode, re.sub(r"\x1b\[[0-9;]*m", "", out)


def _last(out):
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return lines[-1] if lines else "(no output)"


def _pytest(cwd, *targets):
    rc, out = _run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *targets], cwd)
    last = _last(out)
    ok = rc == 0 and "passed" in last and not re.search(r"\d+ (failed|error)", last)
    return ok, last


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB70"))
        sys.exit(1)

    if cid == "IB70-1-AC1":
        t = root / IR / "reports/tests/test_custody_write.py"
        if not t.is_file():
            fail("no %s/reports/tests/test_custody_write.py" % IR)
        src = t.read_text(encoding="utf-8")
        for need in ("CUSTODY_REPORT", "as_of_date", "resolve"):
            if need not in src:
                fail("the test never names %s" % need)
        ok, last = _pytest(root / IR / "reports", "tests/")
        if not ok:
            fail("reports suite: %s" % last)
        ok2, last2 = _pytest(root / IR / "export", "tests/test_submit_custody_report.py")
        if not ok2:
            fail("test_submit_custody_report: %s" % last2)
        print("OK: reports suite %s; custody submit %s" % (last, last2))
    elif cid == "IB70-2-AC1":
        t = root / IR / "export/tests/test_accept_business_date.py"
        if not t.is_file():
            fail("no %s/export/tests/test_accept_business_date.py" % IR)
        src = t.read_text(encoding="utf-8")
        if "accept(" not in src or "as_of_date" not in src or "actual_end" not in src:
            fail("the test does not drive accept( over both as_of_date and actual_end")
        ok, last = _pytest(root / IR / "export", "tests/test_accept_business_date.py", "tests/test_submit_custody_report.py")
        if not ok:
            fail("export tests: %s" % last)
        print("OK: %s" % last)
    elif cid == "IB70-3-AC1":
        portal = root / "portal"
        d = portal / PT / "ir-70-custody-print"
        tests = sorted(d.glob("*.test.ts*")) if d.is_dir() else []
        if not tests:
            fail("no portal test under portal/%sir-70-custody-print/" % PT)
        text = "\n".join(x.read_text(encoding="utf-8") for x in tests)
        if "custody-report" not in text or "ClientReportDocument" not in text:
            fail("the test does not name custody-report and ClientReportDocument")
        rc, out = _run(["bun", "--no-install", "test", PT + "ir-70-custody-print/", PT + "ir-66-print-kind/"], portal)
        m = re.search(r"(\d+) pass", out)
        f = re.search(r"(\d+) fail", out)
        if rc or not m or (f and int(f.group(1)) > 0):
            fail("bun test rc %d: %s" % (rc, _last(out)))
        print("OK: %s pass, %s fail" % (m.group(1), f.group(1) if f else "0"))
    elif cid == "IB70-3-AC2":
        portal = root / "portal"
        rc, out = _run(["node", "node_modules/typescript/bin/tsc", "-b", "--noEmit"], portal, timeout=115)
        if rc:
            fail("tsc -b --noEmit rc %d: %s" % (rc, _last(out)))
        rc, out = _run(["node", "node_modules/eslint/bin/eslint.js", "src/pages/InvestorReporting/render/PrintEntry.tsx"], portal)
        if rc:
            fail("eslint PrintEntry.tsx rc %d: %s" % (rc, _last(out)))
        print("OK: tsc -b --noEmit rc 0; eslint PrintEntry.tsx rc 0")
    elif cid.startswith("IB70-G-"):
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
