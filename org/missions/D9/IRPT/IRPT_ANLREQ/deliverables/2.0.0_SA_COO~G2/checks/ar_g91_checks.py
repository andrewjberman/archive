"""IRPT_ANLREQ AR-g-91 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root, after the last commit (the builder reads HEAD).

    python ar_g91_checks.py g91       the issuer's six release tests pass (the builder runs over HEAD and its tarball is checked), and
                                      the worker's five named tests (new file reports/tests/test_resident_r32_source.py) exist and pass
    python ar_g91_checks.py regress   ten existing test files (run one at a time) still pass

Prints one RESULT line: AR-G91-OK / AR-G91-FAIL or AR-G91-REGRESS-OK / AR-G91-REGRESS-FAIL; rc 0 only on OK. ASCII only.
"""
import re
import subprocess
import sys

R = "infra/aws/lambda/investor-reporting/"
OWNED = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/ar_g91_owned_tests.py"
WORKER = R + "reports/tests/test_resident_r32_source.py"
NAMED = ["test_the_bindings_pin_all_three_maps_by_content", "test_every_shipped_pin_verifies_and_loads",
         "test_pricing_is_shipped_off", "test_the_tarball_carries_the_price_modules_and_the_maps",
         "test_the_producer_list_is_andrew_and_run_3s_address"]
OWNED_COUNT = 6
EXISTING = [R + "reports/tests/test_resident_r31_source.py", R + "ycharts/generate/tests/test_resident_worker.py",
            R + "ycharts/generate/tests/test_producer_for_ticket.py", R + "ycharts/generate/tests/test_acceptance_actor.py",
            R + "ycharts/generate/tests/test_commentary_requested_member.py", R + "ycharts/generate/tests/test_ready_signal_ticket_gate.py",
            R + "ycharts/generate/tests/test_producer_actor.py", R + "ycharts/generate/tests/test_opal_thread_integration.py",
            R + "reports/tests/test_resident_installed.py", R + "reports/tests/test_generate_installed.py"]
MIN_TOTAL = 131


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
    if mode == "g91":
        rc1, line1, passed1, bad1, _ = pytest_run([OWNED])
        rc0, _, _, _, listing = pytest_run([WORKER], extra=("--collect-only",))
        have = set(re.findall(r"::(test_[A-Za-z0-9_]+)", listing))
        missing = [n for n in NAMED if n not in have]
        rc2, line2, passed2, bad2, _ = pytest_run([WORKER])
        print("issuer tests: %s" % line1)
        print("named tests missing: %s" % (missing or "none"))
        print("worker tests: %s" % line2)
        if rc1 != 0 or bad1 or passed1 < OWNED_COUNT or missing or rc2 != 0 or bad2 or passed2 < len(NAMED):
            print("AR-G91-FAIL issuer=%d/%d missing=%s worker=%d/%d" % (passed1, OWNED_COUNT, missing or "none", passed2, len(NAMED)))
            return 1
        print("AR-G91-OK issuer=%d named=%d worker=%d" % (passed1, len(NAMED), passed2))
        return 0
    if mode == "regress":
        total, bad = 0, []
        for path in EXISTING:
            rc, line, passed, nbad, _ = pytest_run([path])
            print("%s: %s" % (path.split("/")[-1], line[:70]))
            total += passed
            if rc != 0 or nbad or passed == 0:
                bad.append(path.split("/")[-1])
        if bad or total < MIN_TOTAL:
            print("AR-G91-REGRESS-FAIL files=%s passed=%d (need >= %d)" % (bad or "none", total, MIN_TOTAL))
            return 1
        print("AR-G91-REGRESS-OK passed=%d" % total)
        return 0
    print("usage: ar_g91_checks.py g91|regress")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
