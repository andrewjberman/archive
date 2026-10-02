"""Round 39 shared check (issuer, LOCAL): both harvest test suites run with 0 failures.

Runs `python -m pytest lib/research/harvest -q` and `python -m pytest lib/opal_data_harvest -q` from the repo root and
reads each summary line. PASS requires a summary with "passed" and no "failed" and no "error" in both. At the round-39 cut
the base read 334 passed (research) and 597 passed, 3 skipped (collector).
"""
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()


def summary(path):
    p = subprocess.run([sys.executable, "-m", "pytest", path, "-q", "-p", "no:cacheprovider"], cwd=ROOT,
                       capture_output=True, text=True, timeout=1800)
    text = re.sub(r"\x1b\[[0-9;]*m", "", p.stdout + p.stderr)
    lines = [ln for ln in text.splitlines() if re.search(r"\b(passed|failed|error)\b", ln)]
    return p.returncode, (lines[-1] if lines else "NO SUMMARY")


def main():
    failures = []
    for path in ("lib/research/harvest", "lib/opal_data_harvest"):
        rc, line = summary(path)
        print("%s rc=%s: %s" % (path, rc, line))
        if rc != 0 or "passed" not in line or re.search(r"\b(failed|error)\b", line):
            failures.append("%s: %s" % (path, line))
    print("SUITES RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
