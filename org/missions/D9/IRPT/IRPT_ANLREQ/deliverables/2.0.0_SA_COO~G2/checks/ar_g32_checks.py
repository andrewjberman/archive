"""IRPT_ANLREQ AR-g-32 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g32_checks.py g32       no ticket read is left, the conflict code is read, the own-store tests pass
    python ar_g32_checks.py regress   the research tests (0 failed, at least 259 passed) and the resident factory tests

Prints one RESULT line: AR-G32-<MODE>OK or AR-G32-<MODE>FAIL <reason>; rc 0 only on OK. ASCII only.
"""
import re
import subprocess
import sys

R = "infra/aws/lambda/investor-reporting/"
PACKAGER = R + "ycharts/research/opal_packager.py"
PRODUCER = R + "ycharts/research/opal_producer.py"
INSTALLED = R + "reports/resident_installed.py"


def bad_count(line):
    """Failed tests plus errors named in a pytest summary line. `1 xfailed` is an expected failure and is not counted."""
    return sum(int(n) for n in re.findall(r"(?<![A-Za-z])([0-9]+) (?:failed|errors?)(?![A-Za-z])", line))


def pytest_line(target):
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", target],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    lines = [ln for ln in (out.stdout + out.stderr).splitlines() if re.search(r"[0-9]+ (passed|failed|error)", ln)]
    line = lines[-1].strip() if lines else "(no summary line)"
    m = re.search(r"([0-9]+) passed", line)
    return out.returncode, line, int(m.group(1)) if m else 0


def main(mode):
    if mode == "g32":
        src = {p: open(p, encoding="utf-8").read() for p in (PACKAGER, PRODUCER, INSTALLED)}
        left = {p.rsplit("/", 1)[1]: src[p].count("ticket_package") for p in (PACKAGER, INSTALLED)}
        facts = {"ticket_package left": sum(left.values()),
                 "TICKET_READ_REFUSED left": src[PACKAGER].count("TICKET_READ_REFUSED"),
                 "PACKAGE_ALREADY_ATTACHED named": src[PACKAGER].count("PACKAGE_ALREADY_ATTACHED"),
                 "retained_package named": src[PACKAGER].count("retained_package"),
                 "old logical id form left": len(re.findall(r"-package-%s\" % \(request_id, sha\)", src[PRODUCER]))}
        rc, line, passed = pytest_line(R + "ycharts/research/tests/test_packager_own_store.py")
        print(" | ".join("%s %d" % kv for kv in facts.items()))
        print(line)
        wrong = [k for k in ("ticket_package left", "TICKET_READ_REFUSED left", "old logical id form left") if facts[k]]
        wrong += [k for k in ("PACKAGE_ALREADY_ATTACHED named", "retained_package named") if not facts[k]]
        if wrong or rc != 0 or bad_count(line) or passed < 9:
            print("AR-G32-FAIL %s; rc=%d passed=%d (need 0 failed, at least 9 passed)" % (", ".join(wrong) or "source ok", rc, passed))
            return 1
        print("AR-G32-OK passed=%d" % passed)
        return 0
    if mode == "regress":
        rc1, line1, passed1 = pytest_line(R + "ycharts/research/tests")
        rc2, line2, passed2 = pytest_line(R + "reports/tests/test_resident_installed.py")
        print("research: %s" % line1)
        print("resident factory: %s" % line2)
        if rc1 != 0 or bad_count(line1) or passed1 < 259 or rc2 != 0 or bad_count(line2) or passed2 < 1:
            print("AR-G32-REGRESS-FAIL research rc=%d passed=%d (need >= 259); factory rc=%d passed=%d" % (rc1, passed1, rc2, passed2))
            return 1
        print("AR-G32-REGRESS-OK research=%d factory=%d" % (passed1, passed2))
        return 0
    raise SystemExit(__doc__)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
