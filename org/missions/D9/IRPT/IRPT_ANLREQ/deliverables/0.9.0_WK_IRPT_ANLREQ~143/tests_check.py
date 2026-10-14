"""AR336-y-AC1 checker (written by 0.9.0_WK_IRPT_ANLREQ~143). ASCII only.

Runs the new test file AND every test file in reports/tests/ and ycharts/generate/tests/ whose name contains resident,
packager, bindings, installed or build. One pytest process per file, run in parallel. Prints the file list, then
TESTS-OK <new passed> new, <others passed> others, 0 failed  only when the new file has every case passing and the
others have 0 failed; otherwise TESTS-BAD <why> and exit 1.
"""
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
WT = next(p for p in HERE.parents if (p / ".tools").is_dir() and (p / "org").is_dir())
NEW_REL = "infra/aws/lambda/investor-reporting/reports/tests/test_resident_r31_packager_bindings.py"
DIRS = ("infra/aws/lambda/investor-reporting/reports/tests",
        "infra/aws/lambda/investor-reporting/ycharts/generate/tests")
KEYS = ("resident", "packager", "bindings", "installed", "build")
COUNT = re.compile(r"(\d+) (passed|failed|errors?)\b")


def run(path):
    env = dict(os.environ, MSYS_NO_PATHCONV="1")
    proc = subprocess.run([sys.executable, "-m", "pytest", str(path), "-q", "-p", "no:cacheprovider",
                           "--color=no", "--tb=line"],
                          capture_output=True, text=True, env=env, cwd=str(WT), timeout=900)
    text = proc.stdout + proc.stderr
    summary = [line for line in text.splitlines() if re.search(r"\b(passed|failed|errors?|no tests ran)\b", line)]
    last = summary[-1].strip() if summary else "UNPARSED"
    counts = {"passed": 0, "failed": 0, "error": 0}
    for number, word in COUNT.findall(last):
        counts["error" if word.startswith("error") else word] += int(number)
    return path, proc.returncode, counts, last


def main():
    new = WT / NEW_REL
    files = []
    for rel in DIRS:
        for path in sorted((WT / rel).glob("test_*.py")):
            if any(key in path.name for key in KEYS) and path.resolve() != new.resolve():
                files.append(path)
    print("NEW    " + NEW_REL)
    for path in files:
        print("OTHER  " + path.relative_to(WT).as_posix())
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run, [new] + files))
    problems = []
    for path, rc, counts, last in results:
        print("RESULT rc=%s %s :: %s" % (rc, path.relative_to(WT).as_posix(), last))
    _, new_rc, new_counts, _ = results[0]
    defined = len(re.findall(r"^def test_", new.read_text(encoding="utf-8"), re.M))
    if new_rc != 0 or new_counts["failed"] or new_counts["error"] or new_counts["passed"] != defined:
        problems.append("new file rc=%s passed=%s failed=%s error=%s defined=%s"
                        % (new_rc, new_counts["passed"], new_counts["failed"], new_counts["error"], defined))
    other_passed = 0
    for path, rc, counts, last in results[1:]:
        if rc != 0 or counts["failed"] or counts["error"] or last == "UNPARSED":
            problems.append("%s rc=%s failed=%s error=%s" % (path.name, rc, counts["failed"], counts["error"]))
        other_passed += counts["passed"]
    if problems:
        print("TESTS-BAD " + "; ".join(problems))
        return 1
    print("TESTS-OK %d new, %d others, 0 failed" % (new_counts["passed"], other_passed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
