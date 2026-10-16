"""IRPT_ANLREQ AR-g-101 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g101_checks.py g101     the issuer's 29 installer tests pass against the worker's change (the real runtime built with a pinned
                                     swap-pool binding), and the worker's six named tests (new file reports/tests/test_opal_swap_pool_binding.py)
                                     exist and pass
    python ar_g101_checks.py regress   seven existing test files (run one at a time) still pass, 82 tests in all, and the branch changed only the
                                     cell's own files (measured against the merge-base with box/dell2)

Prints one RESULT line: AR-G101-OK / AR-G101-FAIL or AR-G101-REGRESS-OK / AR-G101-REGRESS-FAIL; rc 0 only on OK. ASCII only.
"""
import re
import subprocess
import sys

R = "infra/aws/lambda/investor-reporting/"
T = R + "reports/tests/"
OWNED = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/ar_g101_owned_tests.py"
WORKER = T + "test_opal_swap_pool_binding.py"
NAMED = ["test_absent_binding_adds_no_swap_store", "test_binding_supplies_the_pool_and_a_history_port",
         "test_the_run_date_is_the_clock_date_and_an_old_pool_is_stale", "test_a_changed_or_absent_pool_file_refuses_the_job",
         "test_bad_bindings_refuse_the_load", "test_offline_extras_win"]
OWNED_COUNT = 29
REGRESS = [T + "test_resident_installed.py", T + "test_opal_pricing_binding.py", T + "test_resident_packager_binding.py",
           T + "test_resident_package_imports.py", T + "test_resident_r31_packager_bindings.py", T + "test_resident_r31_source.py",
           T + "test_resident_r32_source.py"]
MIN_TOTAL = 82
OWN_FILES = (R + "reports/resident_installed.py", WORKER)
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")


def pytest_run(targets, extra=()):
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", *extra, *targets],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    text = out.stdout + out.stderr
    lines = [ln for ln in text.splitlines() if re.search(r"[0-9]+ (passed|failed|error)", ln)]
    line = lines[-1].strip() if lines else "(no summary line)"
    m = re.search(r"([0-9]+) passed", line)
    bad = sum(int(n) for n in re.findall(r"(?<![A-Za-z])([0-9]+) (?:failed|errors?)(?![A-Za-z])", line))
    return out.returncode, line, int(m.group(1)) if m else 0, bad, text


def g101():
    rc1, line1, passed1, bad1, _ = pytest_run([OWNED])
    rc0, _, _, _, listing = pytest_run([WORKER], extra=("--collect-only",))
    have = set(re.findall(r"::(test_[A-Za-z0-9_]+)", listing))
    missing = [n for n in NAMED if n not in have]
    rc2, line2, passed2, bad2, _ = pytest_run([WORKER])
    print("issuer tests: %s" % line1)
    print("named tests missing: %s" % (missing or "none"))
    print("worker tests: %s" % line2)
    if rc1 != 0 or bad1 or passed1 < OWNED_COUNT or missing or rc2 != 0 or bad2 or passed2 < len(NAMED):
        print("AR-G101-FAIL issuer=%d/%d missing=%s worker=%d/%d" % (passed1, OWNED_COUNT, missing or "none", passed2, len(NAMED)))
        return 1
    print("AR-G101-OK issuer=%d named=%d worker=%d" % (passed1, len(NAMED), passed2))
    return 0


def regress():
    total, bad = 0, []
    for path in REGRESS:
        rc, line, passed, nbad, _ = pytest_run([path])
        total += passed
        if rc != 0 or nbad:
            bad.append((path.rsplit("/", 1)[-1], line))
    diff = subprocess.run(["git", "diff", "--name-only", "box/dell2...HEAD"], capture_output=True, text=True).stdout.split()
    folder = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~"
    order = "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-101."
    stray = [p for p in diff if p not in OWN_FILES and not p.startswith(ISSUER) and not p.startswith(folder) and not p.startswith(order)]
    if bad or total < MIN_TOTAL or stray:
        print("AR-G101-REGRESS-FAIL total=%d (want at least %d) bad=%s stray=%s" % (total, MIN_TOTAL, str(bad)[:200], str(stray[:5])))
        return 1
    print("AR-G101-REGRESS-OK %d tests in %d files, %d changed paths all the cell's own" % (total, len(REGRESS), len(diff)))
    return 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "g101":
        sys.exit(g101())
    if mode == "regress":
        sys.exit(regress())
    print("usage: ar_g101_checks.py g101 | regress")
    sys.exit(2)
