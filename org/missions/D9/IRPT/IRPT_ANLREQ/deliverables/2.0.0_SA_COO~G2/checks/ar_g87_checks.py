"""IRPT_ANLREQ AR-g-87 check (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g87_checks.py g87   the issuer's four installer tests pass against the worker's change, and the worker's two named
                                  tests (one edited, one new, both in reports/tests/test_resident_installed.py) exist and pass

Prints one RESULT line: AR-G87-OK / AR-G87-FAIL; rc 0 only on OK. ASCII only.
"""
import re
import subprocess
import sys

R = "infra/aws/lambda/investor-reporting/"
OWNED = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/ar_g87_owned_tests.py"
WORKER = R + "reports/tests/test_resident_installed.py"
NAMED = ["test_installer_wires_ycdgen_research_revision", "test_installer_registers_the_commentary_family_under_its_revision"]


def pytest_run(targets, extra=()):
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", *extra, *targets],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    text = out.stdout + out.stderr
    lines = [ln for ln in text.splitlines() if re.search(r"[0-9]+ (passed|failed|error)", ln)]
    line = lines[-1].strip() if lines else "(no summary line)"
    m = re.search(r"([0-9]+) passed", line)
    bad = sum(int(n) for n in re.findall(r"(?<![A-Za-z])([0-9]+) (?:failed|errors?)(?![A-Za-z])", line))
    return out.returncode, line, int(m.group(1)) if m else 0, bad, text


def main(mode):
    if mode != "g87":
        print("usage: ar_g87_checks.py g87")
        return 2
    rc1, line1, passed1, bad1, _ = pytest_run([OWNED])
    rc0, _, _, _, listing = pytest_run([WORKER], extra=("--collect-only",))
    have = set(re.findall(r"::(test_[A-Za-z0-9_]+)", listing))
    missing = [n for n in NAMED if n not in have]
    rc2, line2, passed2, bad2, _ = pytest_run([WORKER], extra=("-k", " or ".join(NAMED)))
    print("issuer tests: %s" % line1)
    print("named tests missing: %s" % (missing or "none"))
    print("worker tests: %s" % line2)
    if rc1 != 0 or bad1 or passed1 < 4 or missing or rc2 != 0 or bad2 or passed2 < len(NAMED):
        print("AR-G87-FAIL issuer=%d/4 missing=%s named=%d/%d" % (passed1, missing or "none", passed2, len(NAMED)))
        return 1
    print("AR-G87-OK issuer=%d named=%d" % (passed1, passed2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
