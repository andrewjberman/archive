"""Round 37 (IRPT_BCKEND ~P, CTO batch 205) -- the PATH B export pins and renders THROUGH the 49F reporting route; the fence is
untouched. One grader, three criteria.

Usage: python <this file> <repo_root> <criterion_id>
  IB37-1-AC1  infra/aws/lambda/investor-reporting/export/tests/test_export_path_b_route.py names "X-Opal-Version-Id", "sha256",
              "mismatch" and "frozen_as_of"; at least 4 pass, 0 failed.
  IB37-1-AC2  regression, three suites (each bounded at 110 s): export/tests at least 185 passed and 0 failed; reporting/tests
              at least 21 passed and 0 failed; _authz/tests at least 203 passed, and its ONLY failures are the 6 tests of
              test_unguarded_census.py that fail at the base (row S15, placed at the P-2 drain, not this cell).
  IB37-1-AC3  the IaC and contract text match batch 205 and row W104-S4:
              - infra/aws/terraform/investor-reporting/export/iam.tf names no "series.json.gz" (the export role's platinum
                policy is dropped);
              - infra/aws/terraform/investor-reporting/reporting-read/iam.tf grants "s3:GetObjectVersion" in a statement whose
                resources name the platinum reporting prefix, and no statement grants it on "*";
              - both ExportReceipt.schema.json copies (infra/aws/lambda/investor-reporting/_contracts/ and
                docs/contracts/investor-reporting/v1/) are byte-equal and declare a property named "frozen_as_of" or "as_of"
                carrying the frozen series date.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import re
import subprocess
import sys
from pathlib import Path

L = "infra/aws/lambda/investor-reporting/"
T = "infra/aws/terraform/investor-reporting/"
CENSUS = "test_unguarded_census.py"


def run_suite(root, target):
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", "-rf", target],
                           cwd=str(root), capture_output=True, text=True, timeout=110)
    except subprocess.TimeoutExpired:
        return None, None, ["TIMEOUT"]
    out = (r.stdout or "") + (r.stderr or "")
    passed = re.search(r"(\d+) passed", out)
    failed_ids = re.findall(r"^(?:FAILED|ERROR) (\S+)", out, re.M)
    return int(passed.group(1)) if passed else 0, out, failed_ids


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB37"))
        sys.exit(1)

    if cid == "IB37-1-AC1":
        t = root / (L + "export/tests/test_export_path_b_route.py")
        if not t.is_file():
            fail("no export/tests/test_export_path_b_route.py")
        src = t.read_text(encoding="utf-8")
        for w in ("X-Opal-Version-Id", "sha256", "mismatch", "frozen_as_of"):
            if w not in src:
                fail("the test file never names %r" % w)
        n, out, failed = run_suite(root, L + "export/tests/test_export_path_b_route.py")
        if failed or n is None or n < 4:
            fail("route-pin tests: %s passed, failures %s" % (n, failed[:3]))
        print("OK: %d route-pin tests passed, 0 failed" % n)
    elif cid == "IB37-1-AC2":
        for suite, floor in (("export/tests", 185), ("reporting/tests", 21)):
            n, out, failed = run_suite(root, L + suite)
            if failed or n is None or n < floor:
                fail("%s: %s passed (floor %d), failures %s" % (suite, n, floor, failed[:3]))
        n, out, failed = run_suite(root, L + "_authz/tests")
        foreign = [f for f in failed if CENSUS not in f]
        if n is None or n < 203 or foreign or len(failed) > 6:
            fail("_authz: %s passed (floor 203), failures outside the base census set: %s, total failed %d"
                 % (n, foreign[:3], len(failed)))
        print("OK: export and reporting suites at their floors with 0 failed; _authz %d passed, %d failed, all in %s (row S15)"
              % (n, len(failed), CENSUS))
    elif cid == "IB37-1-AC3":
        ex = (root / (T + "export/iam.tf")).read_text(encoding="utf-8")
        if "series.json.gz" in ex:
            fail("export/iam.tf still names series.json.gz (batch 205: drop the export role's platinum policy)")
        rr = (root / (T + "reporting-read/iam.tf")).read_text(encoding="utf-8")
        blocks = [b for b in re.split(r"\n\s*statement\s*\{", rr) if "s3:GetObjectVersion" in b]
        if not blocks:
            fail("reporting-read/iam.tf grants no s3:GetObjectVersion")
        for b in blocks:
            res = re.search(r"resources\s*=\s*(\[.*?\]|[^\n]+)", b, re.S)
            if not res or '"*"' in res.group(1):
                fail("a GetObjectVersion statement has no resources or a wildcard")
        if not any("platinum" in b or "irpt_rr_" in b for b in blocks):
            fail("no GetObjectVersion statement names the platinum reporting prefix")
        a = root / (L + "_contracts/ExportReceipt.schema.json")
        b = root / "docs/contracts/investor-reporting/v1/ExportReceipt.schema.json"
        if not a.is_file() or not b.is_file():
            fail("an ExportReceipt.schema.json copy is missing")
        if a.read_bytes() != b.read_bytes():
            fail("the two ExportReceipt.schema.json copies differ")
        if '"frozen_as_of"' not in a.read_text(encoding="utf-8") and '"as_of"' not in a.read_text(encoding="utf-8"):
            fail("ExportReceipt declares no frozen as_of slot")
        print("OK: export role's platinum policy dropped; reporting-read reads by VersionId on the platinum prefix only; "
              "ExportReceipt copies equal and carry the frozen as_of slot")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
