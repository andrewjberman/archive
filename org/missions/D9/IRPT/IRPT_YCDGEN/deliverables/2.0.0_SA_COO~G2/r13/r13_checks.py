"""IRPT_YCDGEN round 13 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python r13_checks.py d13        the dead-letter record carries cause_claim "measured": driven through poll_once
    python r13_checks.py d13suite   the ycharts/generate tests: 0 failed, 0 errors, at least 507 passed

Prints one RESULT line: R13-<MODE>-OK or R13-<MODE>-FAIL <reason>; rc 0 only on OK. ASCII only.
"""
import re
import subprocess
import sys

GEN = "infra/aws/lambda/investor-reporting/ycharts/generate"
WANT = {"code", "cause", "receives", "cause_claim"}


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
    if mode == "d13":
        src = open(GEN + "/resident_worker.py", encoding="utf-8").read()
        start = src.index("def _record_deliveries_exhausted")
        body = src[start:src.index("\ndef ", start + 10)]
        stamped = len(re.findall(r'"cause_claim"\s*:\s*"measured"', body))
        elsewhere = len(re.findall(r"cause_claim", src)) - len(re.findall(r"cause_claim", body))
        test = open(GEN + "/tests/test_dead_letter_record.py", encoding="utf-8").read()
        four = len(re.findall(r'"cause_claim"\s*:\s*"measured"', test))
        rc, line, passed = pytest_line(GEN + "/tests/test_dead_letter_record.py")
        print("stamp in the record function: %d | cause_claim elsewhere in the worker: %d | tests asserting it: %d | %s"
              % (stamped, elsewhere, four, line))
        if stamped != 1 or elsewhere != 0 or four < 2 or rc != 0 or bad_count(line) or passed < 9:
            print("R13-D13-FAIL stamped=%d elsewhere=%d asserting=%d rc=%d passed=%d "
                  "(need 1, 0, at least 2, rc 0, 0 failed, at least 9 passed)" % (stamped, elsewhere, four, rc, passed))
            return 1
        print("R13-D13-OK stamped=1 asserting=%d passed=%d" % (four, passed))
        return 0
    if mode == "d13suite":
        rc, line, passed = pytest_line(GEN + "/tests")
        print(line)
        if rc != 0 or bad_count(line) or passed < 507:
            print("R13-D13SUITE-FAIL rc=%d passed=%d (need >= 507, 0 failed, 0 errors)" % (rc, passed))
            return 1
        print("R13-D13SUITE-OK passed=%d" % passed)
        return 0
    raise SystemExit(__doc__)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
