"""IRPT_BCKEND round 63 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-341 (the over-age status is public).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Every check finishes inside 120 s.

  IB63-1-AC1  directory/tests/test_search_overage_public_status.py passes (names internal_correlation_id) and the directory suite
              passes. Base: FAIL (no test).
  IB63-1-AC2  the four portal reader tests in portal/src/pages/InvestorReporting/__tests__/ir-62-overage/ carry no test.failing and pass
              with bun (0 fail) on the over-age fixture regenerated from the fixed entry.search. Base: FAIL (folder absent on portal DEV /
              four test.failing at d53a7a0f).
  IB63-G-143  A GUARD: worker ~143's workspace commits touch only its grant. Base: PASS.
"""
import re
import subprocess
import sys
from pathlib import Path

BASE = "1758606f46"
P = "org/missions/D9/IRPT/IRPT_BCKEND"
DIR = "infra/aws/lambda/investor-reporting/directory"
PT = "portal/src/pages/InvestorReporting/__tests__/ir-62-overage"
GRANT = (DIR + "/entry.py", DIR + "/tests/test_search_overage_public_status.py", "portal",
         P + "/surprise-channel/investigations/INVESTIGATION_v1.md", P + "/task-orders/IRPT_BCKEND.TO-IB-pr-341.",
         P + "/deliverables/0.9.0_WK_IRPT_BCKEND~143/")


def _run(cmd, cwd, timeout=110):
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, timeout=timeout)
    out = (r.stdout or b"").decode("utf-8", "replace") + (r.stderr or b"").decode("utf-8", "replace")
    return r.returncode, re.sub(r"\x1b\[[0-9;]*m", "", out)


def _last(out):
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return lines[-1] if lines else "(no output)"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB63"))
        sys.exit(1)

    if cid == "IB63-1-AC1":
        t = root / DIR / "tests/test_search_overage_public_status.py"
        if not t.is_file():
            fail("no %s/tests/test_search_overage_public_status.py" % DIR)
        if "internal_correlation_id" not in t.read_text(encoding="utf-8"):
            fail("the test never names internal_correlation_id")
        rc, out = _run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/test_search_overage_public_status.py"],
                       root / DIR)
        last = _last(out)
        if rc or "passed" not in last or re.search(r"\d+ (failed|error)", last):
            fail("new tests: %s" % last)
        rc, out = _run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/"], root / DIR)
        last2 = _last(out)
        if rc or re.search(r"\d+ (failed|error)", last2):
            fail("directory suite: %s" % last2)
        print("OK: new %s; directory suite %s" % (last, last2))
    elif cid == "IB63-1-AC2":
        d = root / PT
        tests = sorted(d.glob("*.test.ts")) if d.is_dir() else []
        if not tests:
            fail("no portal reader tests under %s" % PT)
        flagged = [t.name for t in tests if "test.failing" in t.read_text(encoding="utf-8")]
        if flagged:
            fail("still written test.failing: %s" % flagged)
        bun = "bun"
        rc, out = _run([bun, "test", "src/pages/InvestorReporting/__tests__/ir-62-overage/"], root / "portal")
        m = re.search(r"(\d+) pass", out)
        f = re.search(r"(\d+) fail", out)
        if rc or not m or (f and int(f.group(1)) > 0):
            fail("bun test rc %d: %s" % (rc, _last(out)))
        print("OK: %s pass, %s fail" % (m.group(1), f.group(1) if f else "0"))
    elif cid == "IB63-G-143":
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=0.9.0_WK_IRPT_BCKEND~143", "--name-only", "--format="],
                           cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if not c.startswith(GRANT)]
        if bad:
            fail("out-of-grant changes: %s" % bad[:8])
        print("OK: %d changed path(s), all inside slot ~143's grant" % len(changed))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
