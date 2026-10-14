"""AR327-y-AC1 (IRPT_ANLREQ AR-y-327): run the new test file and every neighbour test file in ycharts/research/tests whose
name contains packager, producer or layout. Prints the file list and each file's summary. Prints TESTS-OK only when every
case a to f of the new file PASSES and the neighbour files have 0 failed; otherwise TESTS-BAD <why> and exit 1."""
import re
import subprocess
import sys
from pathlib import Path

NEW = "test_commentary_standalone_pdf.py"
CASES = ("a", "b", "c", "d", "e", "f")
WORDS = ("packager", "producer", "layout")
TESTS_REL = "infra/aws/lambda/investor-reporting/ycharts/research/tests"
ANSI = re.compile(r"\x1b\[[0-9;]*m")
COUNT = re.compile(r"(\d+) (passed|failed|errors?)\b")


def root():
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / ".tools").is_dir() and (p / "org").is_dir():
            return p
    print("TESTS-BAD root with .tools and org not found above " + str(here))
    sys.exit(1)


def run(tests_dir, name):
    proc = subprocess.run([sys.executable, "-m", "pytest", "-v", "--color=no", "-p", "no:cacheprovider", name],
                          cwd=str(tests_dir), capture_output=True, text=True, timeout=110)
    text = ANSI.sub("", proc.stdout + proc.stderr)
    lines = [ln for ln in text.splitlines() if "::" in ln and (" PASSED" in ln or " FAILED" in ln or " ERROR" in ln)]
    summary = [ln for ln in text.splitlines() if COUNT.search(ln) and " in " in ln]
    last = summary[-1].strip() if summary else "NO-SUMMARY"
    counts = {"passed": 0, "failed": 0, "error": 0}
    for n, kind in COUNT.findall(last):
        counts["error" if kind.startswith("error") else kind] += int(n)
    return proc.returncode, lines, counts, last


def main():
    r = root()
    tests_dir = r / TESTS_REL
    files = sorted(p.name for p in tests_dir.glob("test_*.py"))
    others = [f for f in files if f != NEW and any(w in f for w in WORDS)]
    print("NEW-FILE " + NEW)
    print("NEIGHBOUR-FILES " + str(len(others)))
    for f in others:
        print("  " + f)
    rc, lines, counts, last = run(tests_dir, NEW)
    print("NEW rc=%d %s" % (rc, last))
    missing = [c for c in CASES if not any("::test_%s_" % c in ln and " PASSED" in ln for ln in lines)]
    if rc != 0 or counts["failed"] or counts["error"] or missing:
        print("TESTS-BAD new file: cases not all passing: %s" % (", ".join(missing) or "see NEW line"))
        return 1
    other_passed = other_failed = 0
    for f in others:
        rc2, _lines2, c2, last2 = run(tests_dir, f)
        print("OTHER rc=%d %s :: %s" % (rc2, f, last2))
        other_passed += c2["passed"]
        other_failed += c2["failed"] + c2["error"]
        if rc2 != 0 and not (c2["failed"] or c2["error"]):
            other_failed += 1  # a non-zero exit with no counted failure is not a pass
    if other_failed:
        print("TESTS-BAD %d failing or erroring test(s) in the neighbour files: see the OTHER lines" % other_failed)
        return 1
    print("TESTS-OK %d new, %d others, 0 failed" % (counts["passed"], other_passed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
