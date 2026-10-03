"""Round 36 (IRPT_BCKEND ~P, CTO batch 202 section 2) -- one pytest grader for the round's four criteria.

Usage: python <this file> <repo_root> <criterion_id>
  IB36-1-AC1  infra/aws/lambda/investor-reporting/performance/tests/test_holdings_gold_calendar_gap.py names "trading", "missing"
              and "measured"; at least 3 pass, 0 failed.
  IB36-1-AC2  the whole infra/aws/lambda/investor-reporting/performance/tests suite: at least 242 pass (239 at the base,
              2026-10-03, plus 3), 0 failed.
  IB36-2-AC1  infra/aws/lambda/investor-reporting/holdings-performance/tests/test_catch_up.py names "catch", "trading" and
              "missed"; at least 4 pass, 0 failed.
  IB36-2-AC2  the producer's own suite, data/assets/scripts/gold/irpt_holdings_performance/tests: at least 60 pass (the base),
              0 failed -- the producer is not edited by the catch-up cell.
  IB36-3-AC1  infra/aws/lambda/investor-reporting/export/tests/test_export_path_b.py names "PLATINUM", "VersionId", "as_of" and
              "OBJECT_NOT_COVERED"; at least 5 pass, 0 failed (CTO batch 203).
  IB36-3-AC2  the whole infra/aws/lambda/investor-reporting/export/tests suite: at least 173 pass (168 at the base, 2026-10-03,
              plus 5), 0 failed -- it includes test_packaged_contracts_match_docs, so both ExportBundle.schema.json copies agree.
Each run is bounded at 110 s. Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import re
import subprocess
import sys
from pathlib import Path

L = "infra/aws/lambda/investor-reporting/"
SPEC = {
    "IB36-1-AC1": (L + "performance/tests/test_holdings_gold_calendar_gap.py", ("trading", "missing", "measured"), 3),
    "IB36-1-AC2": (L + "performance/tests", (), 242),
    "IB36-2-AC1": (L + "holdings-performance/tests/test_catch_up.py", ("catch", "trading", "missed"), 4),
    "IB36-2-AC2": ("data/assets/scripts/gold/irpt_holdings_performance/tests", (), 60),
    "IB36-3-AC1": (L + "export/tests/test_export_path_b.py", ("PLATINUM", "VersionId", "as_of", "OBJECT_NOT_COVERED"), 5),
    "IB36-3-AC2": (L + "export/tests", (), 173),
}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    if cid not in SPEC:
        print("FAIL: unknown criterion %r" % cid)
        print("%s FAIL" % (cid or "IB36"))
        sys.exit(1)
    target, words, floor = SPEC[cid]

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % cid)
        sys.exit(1)

    p = root / target
    if not p.exists():
        fail("no %s" % target)
    if words:
        src = p.read_text(encoding="utf-8")
        for w in words:
            if w not in src:
                fail("%s never names %r" % (target, w))
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", target],
                           cwd=str(root), capture_output=True, text=True, timeout=110)
    except subprocess.TimeoutExpired:
        fail("pytest exceeded 110 s")
    out = (r.stdout or "") + (r.stderr or "")
    bad = re.search(r"(\d+) (failed|error)", out)
    passed = re.search(r"(\d+) passed", out)
    if bad:
        fail("pytest: %s" % bad.group(0))
    if not passed or int(passed.group(1)) < floor:
        fail("fewer than %d passed: %s" % (floor, passed.group(0) if passed else out.strip()[-200:]))
    print("OK: %s %s, 0 failed" % (target, passed.group(0)))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
