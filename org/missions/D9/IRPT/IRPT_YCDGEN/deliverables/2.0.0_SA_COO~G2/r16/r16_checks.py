"""IRPT_YCDGEN round 16 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python r16_checks.py a16        analysis_ready needs a ticket id AND commentary_requested exactly true: the new tests pass
    python r16_checks.py a16suite   the ycharts/generate tests: 0 failed, 0 errors, at least 527 passed

Prints one RESULT line: R16-<MODE>-OK or R16-<MODE>-FAIL <reason>; rc 0 only on OK. ASCII only.
"""
import re
import subprocess
import sys

GEN = "infra/aws/lambda/investor-reporting/ycharts/generate"
NEW = GEN + "/tests/test_ready_signal_commentary_gate.py"
NAMES = ("test_a_", "test_b_", "test_c_", "test_d_", "test_e_")


def pytest_line(target):
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", target],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    lines = [ln for ln in (out.stdout + out.stderr).splitlines() if re.search(r"[0-9]+ (passed|failed|error)", ln)]
    line = lines[-1].strip() if lines else "(no summary line)"
    m = re.search(r"([0-9]+) passed", line)
    return out.returncode, line, int(m.group(1)) if m else 0


def bad_count(line):
    """Failed tests plus errors named in a pytest summary line. `1 xfailed` is an expected failure and is not counted."""
    return sum(int(n) for n in re.findall(r"(?<![A-Za-z])([0-9]+) (?:failed|errors?)(?![A-Za-z])", line))


def main(mode):
    if mode == "a16":
        try:
            src = open(NEW, encoding="utf-8").read()
        except OSError:
            print("R16-A16-FAIL the new test file is absent: " + NEW)
            return 1
        have = [p for p in NAMES if re.search(r"^def %s" % p, src, re.M)]
        rc, line, passed = pytest_line(NEW)
        print("test groups present: %s | %s" % (",".join(have), line))
        if len(have) != len(NAMES) or rc != 0 or bad_count(line) or passed < 5:
            print("R16-A16-FAIL groups=%d of %d rc=%d passed=%d (need all 5 groups, rc 0, 0 failed, at least 5 passed)"
                  % (len(have), len(NAMES), rc, passed))
            return 1
        print("R16-A16-OK groups=5 passed=%d" % passed)
        return 0
    if mode == "a16suite":
        rc, line, passed = pytest_line(GEN + "/tests")
        print(line)
        if rc != 0 or bad_count(line) or passed < 527:
            print("R16-A16SUITE-FAIL rc=%d passed=%d (need >= 527, 0 failed, 0 errors)" % (rc, passed))
            return 1
        print("R16-A16SUITE-OK passed=%d" % passed)
        return 0
    raise SystemExit(__doc__)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
