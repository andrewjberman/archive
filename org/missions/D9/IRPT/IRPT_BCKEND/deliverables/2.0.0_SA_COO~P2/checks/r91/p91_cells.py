"""IRPT_BCKEND round 91 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-379 (CTO ruling msg 1949, row D2-S13: why the
inflection and cottonwood directory builds drop clients the previous build carried; fixed before those directories go OVER_AGE).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB91-1-AC1  the diagnosis file D names, for BOTH inflection and cottonwood: disappeared_count >= 1, opaque ids only (no names,
              emails or raw account numbers), cause in {BUILD_BUG, KEY_CHANGE, SOURCE_REMOVAL}, and evidence; plus
              overage_deadline (an ISO date computed with lib/trading_calendar). Base: FAIL (no file).
  IB91-1-AC2  in the directory tests, `-k dropped_entry` passes (>= 1 test reproducing the drop and its fix), and
              tests/test_refresh_previous_state.py passes alone. Base: FAIL (no such tests).
  IB91-1-AC3  the release packet P names the fix pin, the built sha256 of irpt-directory-refresh, the live rollback sha
              RbpsijC23XVUFPE0W34Gr/xqtDil94xYRqDuuZlaYx8=, Branch A and Branch B; the census file C records
              build_only rc 0 on a clean tree and the same built sha256. Base: FAIL (no files).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~187/IB91-1_dropped_entry_diagnosis.json"
TESTS = "infra/aws/lambda/investor-reporting/directory/tests"
WK = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~187/"
P = WK + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-379.md"
C = WK + "IB91-1_refresh_census.json"
ROLLBACK = "RbpsijC23XVUFPE0W34Gr/xqtDil94xYRqDuuZlaYx8="
CAUSES = {"BUILD_BUG", "KEY_CHANGE", "SOURCE_REMOVAL"}
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
ACCT = re.compile(r"\b\d{8,}\b")


def pytest(cwd, *args):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args], cwd=str(cwd),
                       capture_output=True, timeout=280)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace"))
    last = [ln for ln in out.splitlines() if ln.strip()]
    return p.returncode, (last[-1] if last else "")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB91-1"))
        sys.exit(1)

    if cid == "IB91-1-AC1":
        f = root / D
        if not f.is_file():
            fail("no %s" % D)
        raw = f.read_text(encoding="utf-8")
        if EMAIL.search(raw) or ACCT.search(raw):
            fail("the diagnosis carries an email or an account-shaped number")
        d = json.loads(raw)
        firms = d.get("firms") or {}
        for firm in ("inflection", "cottonwood"):
            r = firms.get(firm) or {}
            if not isinstance(r.get("disappeared_count"), int) or r["disappeared_count"] < 1:
                fail("%s disappeared_count %r" % (firm, r.get("disappeared_count")))
            if r.get("cause") not in CAUSES or not str(r.get("evidence", "")).strip():
                fail("%s cause %r / evidence %r" % (firm, r.get("cause"), r.get("evidence")))
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(d.get("overage_deadline", ""))):
            fail("overage_deadline %r" % d.get("overage_deadline"))
        print("OK: inflection %s, cottonwood %s; over-age deadline %s" % (
            firms["inflection"]["cause"], firms["cottonwood"]["cause"], d["overage_deadline"]))
    elif cid == "IB91-1-AC2":
        t = root / TESTS
        rc, last = pytest(t.parent, "tests", "-k", "dropped_entry")
        if rc != 0 or not re.search(r"\b[1-9]\d* passed", last):
            fail("-k dropped_entry rc %d: %s" % (rc, last))
        rc2, last2 = pytest(t.parent, "tests/test_refresh_previous_state.py")
        if rc2 != 0:
            fail("test_refresh_previous_state.py rc %d: %s" % (rc2, last2))
        print("OK: -k dropped_entry: %s; previous_state: %s" % (last, last2))
    elif cid == "IB91-1-AC3":
        if not (root / P).is_file() or not (root / C).is_file():
            fail("missing %s or %s" % (P, C))
        pk = (root / P).read_text(encoding="utf-8")
        c = json.loads((root / C).read_text(encoding="utf-8"))
        bo = c.get("build_only") or {}
        built = str(bo.get("built_sha256", ""))
        if bo.get("rc") != 0 or bo.get("tree_clean") is not True or len(built) < 40:
            fail("census build_only %r" % bo)
        pin = str(c.get("pin", ""))
        for need in (pin, built, ROLLBACK, "Branch A", "Branch B"):
            if not need or need not in pk:
                fail("packet lacks %r" % need)
        print("OK: pin %s built %s" % (pin, built))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
