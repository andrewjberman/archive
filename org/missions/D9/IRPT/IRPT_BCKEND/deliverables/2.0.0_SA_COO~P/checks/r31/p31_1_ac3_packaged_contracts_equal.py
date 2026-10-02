"""IB31-1-AC3 -- (c) the packaged AnalysisReport and ExportBundle schemas are byte-equal to their docs copies, a test asserts it,
and the real report (cutoff 2026-09-29) validates against the packaged copy.

Grades, in order:
  1. THIS check compares the bytes of infra/aws/lambda/investor-reporting/_contracts/{AnalysisReport,ExportBundle}.schema.json with
     docs/contracts/investor-reporting/v1/ (both differ at the base).
  2. export/tests/test_packaged_contracts_match_docs.py names both schema files; at least 2 tests pass, 0 failed or errored
     (bounded at 110 s).
  3. The record deliverables/0.9.0_WK_IRPT_BCKEND~101/PACKAGED_CONTRACT_R31.json:
     {"report_ref": {"bucket", "key", "report_id"}, "schema_path": "<the packaged AnalysisReport path>", "valid": true,
      "cutoff": "YYYY-MM-DD"}: report_id RPT-1f49504f501a6633b1f9cccc5f37ecf6, schema_path the packaged path, valid true,
     cutoff 2026-09-29.
  4. The _contracts folder's own suite in its own process fails 0 (184 passed at the base).
Usage: python <this file> <repo_root>
"""
import json
import re
import subprocess
import sys
from pathlib import Path

B = "infra/aws/lambda/investor-reporting/"
DOCS = "docs/contracts/investor-reporting/v1/"
NAMES = ("AnalysisReport.schema.json", "ExportBundle.schema.json")
TEST = B + "export/tests/test_packaged_contracts_match_docs.py"
REC = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~101/PACKAGED_CONTRACT_R31.json"
REPORT_ID = "RPT-1f49504f501a6633b1f9cccc5f37ecf6"


def fail(msg):
    print("FAIL: " + msg)
    print("IB31-1-AC3 FAIL")
    sys.exit(1)


def pytest(root, target):
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", target],
                           cwd=str(root), capture_output=True, text=True, timeout=110)
    except subprocess.TimeoutExpired:
        fail("pytest exceeded 110 s on %s" % target)
    out = (r.stdout or "") + (r.stderr or "")
    bad = re.search(r"(\d+) (failed|error)", out)
    passed = re.search(r"(\d+) passed", out)
    if bad:
        fail("%s: %s" % (target, bad.group(0)))
    return int(passed.group(1)) if passed else 0


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    for n in NAMES:
        if (root / B / "_contracts" / n).read_bytes() != (root / DOCS / n).read_bytes():
            fail("packaged %s is not byte-equal to the docs copy" % n)
    t = root / TEST
    if not t.is_file():
        fail("no test file at %s" % TEST)
    src = t.read_text(encoding="utf-8")
    for n in NAMES:
        if n not in src:
            fail("the test file never names %s" % n)
    k = pytest(root, TEST)
    if k < 2:
        fail("fewer than 2 tests passed in the new file (%d)" % k)
    rp = root / REC
    if not rp.is_file():
        fail("no record at %s" % REC)
    rec = json.loads(rp.read_text(encoding="utf-8"))
    if (rec.get("report_ref") or {}).get("report_id") != REPORT_ID:
        fail("the record is not for %s" % REPORT_ID)
    if str(rec.get("schema_path", "")).replace("\\", "/") != B + "_contracts/" + NAMES[0]:
        fail("schema_path is not the packaged AnalysisReport copy: %r" % rec.get("schema_path"))
    if rec.get("valid") is not True or rec.get("cutoff") != "2026-09-29":
        fail("valid=%r cutoff=%r (want true, 2026-09-29)" % (rec.get("valid"), rec.get("cutoff")))
    c = pytest(root, B + "_contracts")
    print("OK: both packaged schemas byte-equal to docs; new file %d passed; real report valid on the packaged copy "
          "(cutoff 2026-09-29); _contracts %d passed, 0 failed" % (k, c))
    print("IB31-1-AC3 PASS")


if __name__ == "__main__":
    main()
