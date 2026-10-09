"""IRPT_BCKEND round 92 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-380 (CTO ruling msg 1959 on row D2-W187-S1:
an entry absent from both the build and the source snapshot is carried forward TERMINATED + source_removed_on and the build goes READY;
an entry still in the source but missing from the build stays REFRESH_FAILED).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB92-1-AC1  in the directory tests, `-k terminated_carry_forward` passes with >= 3 tests, and the whole directory suite passes.
              Base: FAIL (no such tests).
  IB92-1-AC2  the replay file R, per firm (inflection, cottonwood), on the real 2026-10 inputs: the built zip gives a non-FAILED
              reason_code with terminated_count 1; the live zip gives REFRESH_FAILED; the negative arm (the dropped id put back into
              the source only) gives REFRESH_FAILED on the built zip. Base: FAIL (no file).
  IB92-1-AC3  the release packet P names the fix pin, the built sha256 of irpt-directory-refresh, the live rollback sha
              RbpsijC23XVUFPE0W34Gr/xqtDil94xYRqDuuZlaYx8=, Branch A and Branch B; the census file C records build_only rc 0 on a
              clean tree and the same built sha256. Base: FAIL (no files).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

WK = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~188/"
R = WK + "IB92-1_terminated_replay.json"
P = WK + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-380.md"
C = WK + "IB92-1_refresh_census.json"
ROLLBACK = "RbpsijC23XVUFPE0W34Gr/xqtDil94xYRqDuuZlaYx8="
DIRECTORY = "infra/aws/lambda/investor-reporting/directory"


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
        print("%s FAIL" % (cid or "IB92-1"))
        sys.exit(1)

    if cid == "IB92-1-AC1":
        d = root / DIRECTORY
        rc, last = pytest(d, "tests", "-k", "terminated_carry_forward")
        m = re.search(r"\b(\d+) passed", last)
        if rc != 0 or not m or int(m.group(1)) < 3:
            fail("-k terminated_carry_forward rc %d: %s" % (rc, last))
        rc2, last2 = pytest(d, "tests")
        if rc2 != 0:
            fail("directory suite rc %d: %s" % (rc2, last2))
        print("OK: -k terminated_carry_forward: %s; suite: %s" % (last, last2))
    elif cid == "IB92-1-AC2":
        f = root / R
        if not f.is_file():
            fail("no %s" % R)
        firms = (json.loads(f.read_text(encoding="utf-8")).get("firms") or {})
        for firm in ("inflection", "cottonwood"):
            r = firms.get(firm) or {}
            b, lv, ng = r.get("built") or {}, r.get("live") or {}, r.get("negative") or {}
            if b.get("reason_code") in (None, "", "REFRESH_FAILED") or b.get("terminated_count") != 1:
                fail("%s built %r" % (firm, b))
            if lv.get("reason_code") != "REFRESH_FAILED":
                fail("%s live %r" % (firm, lv))
            if ng.get("reason_code") != "REFRESH_FAILED":
                fail("%s negative %r" % (firm, ng))
        print("OK: built %s/%s, live and negative REFRESH_FAILED at both firms" % (
            firms["inflection"]["built"]["reason_code"], firms["cottonwood"]["built"]["reason_code"]))
    elif cid == "IB92-1-AC3":
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
