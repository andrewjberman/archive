"""IRPT_ANLREQ AR-g-109 / AR-g-110 checks (issuer 2.0.0_SA_COO~G2). Run from the worker's worktree root, WITHOUT -I.

    python ar_g109_checks.py g109       issuer tests (21) + the worker's named tests for the hop_failure writers pass
    python ar_g109_checks.py g110       issuer tests (5) + the worker's named tests for the yfinance wiring pass
    python ar_g109_checks.py regress109 existing test files (run one at a time) still pass; the branch changed only AR-g-109's own files
    python ar_g109_checks.py regress110 same for AR-g-110

Prints one RESULT line: AR-G109-OK / AR-G110-OK / AR-G109-REGRESS-OK ... or ...FAIL <why>; rc 0 only on OK. ASCII only. Writes nothing.
"""
import os
import re
import subprocess
import sys

R = "infra/aws/lambda/investor-reporting/"
CHECKS = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/"
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", CHECKS, "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/",
          "org/tier1_exec/2.0.0_SA_COO~G2/", "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")
CELLS = {
    "109": {
        "issuer": CHECKS + "ar_g109_issuer_tests.py", "env": ("AR109_ROOT", "AR-G109"), "issuer_count": 29,
        "worker": R + "ycharts/generate/tests/test_hop_failure.py",
        "named": ["test_mark_hop_failure_is_set_once", "test_get_state_carries_hop_failure", "test_a_failed_ready_send_records_the_hop",
                  "test_a_packager_failure_records_the_hop", "test_a_failing_hop_write_never_masks_the_error",
                  "test_mark_hop_failure_keyed_is_set_once_without_a_read"],
        "own": [R + "ycharts/generate/durable_job.py", R + "ycharts/generate/resident_worker.py", R + "reports/resident_installed.py"],
        "regress": [R + "ycharts/generate/tests/test_durable_job.py", R + "ycharts/generate/tests/test_resident_worker.py",
                    R + "reports/tests/test_resident_installed.py", R + "reports/tests/test_resident_packager_binding.py",
                    R + "reports/tests/test_resident_r31_packager_bindings.py", R + "ycharts/research/tests/test_opal_packager.py"],
        "min_total": 136, "order": "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-109."},
    "110": {
        "issuer": CHECKS + "ar_g110_issuer_tests.py", "env": ("AR110_ROOT", "AR-G110"), "issuer_count": 5,
        "worker": R + "ycharts/session/tests/test_resident_session_checker.py",
        "named": ["test_the_door_resolver_keeps_a_yfinance_known_symbol", "test_a_missing_library_is_a_failed_check"],
        "own": [R + "ycharts/session/resident_session.py"],
        "regress": [R + "ycharts/session/tests/test_resident_session.py", R + "intake/tests/test_yfinance_check.py",
                    R + "intake/tests/test_kept_holding.py", R + "ycharts/generate/tests/test_resolve_upload.py"],
        "min_total": 71, "order": "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-110."},
}


def pytest_run(targets, extra=(), env=None):
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", *extra, *targets],
                         capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    text = out.stdout + out.stderr
    lines = [ln for ln in text.splitlines() if re.search(r"[0-9]+ (passed|failed|error)", ln)]
    line = lines[-1].strip() if lines else "(no summary line)"
    m = re.search(r"([0-9]+) passed", line)
    bad = sum(int(n) for n in re.findall(r"(?<![A-Za-z])([0-9]+) (?:failed|errors?)(?![A-Za-z])", line))
    return out.returncode, line, int(m.group(1)) if m else 0, bad, text


def grade(key):
    cell = CELLS[key]
    var, tag = cell["env"]
    env = dict(os.environ, **{var: os.path.abspath(R.rstrip("/")), "IRPT_FIRM_REGISTRY": os.path.abspath("data/firm_registry.json")})
    rc1, line1, passed1, bad1, _ = pytest_run([cell["issuer"]], env=env)
    if not os.path.isfile(cell["worker"]):
        print("%s-FAIL issuer=%d/%d, the worker's test file %s is absent" % (tag, passed1, cell["issuer_count"], cell["worker"]))
        return 1
    rc0, _, _, _, listing = pytest_run([cell["worker"]], extra=("--collect-only",))
    have = set(re.findall(r"::(test_[A-Za-z0-9_]+)", listing))
    missing = [n for n in cell["named"] if n not in have]
    rc2, line2, passed2, bad2, _ = pytest_run([cell["worker"]])
    print("issuer tests: %s" % line1)
    print("named tests missing: %s" % (missing or "none"))
    print("worker tests: %s" % line2)
    if rc1 != 0 or bad1 or passed1 < cell["issuer_count"] or missing or rc2 != 0 or bad2 or passed2 < len(cell["named"]):
        print("%s-FAIL issuer=%d/%d missing=%s worker=%d/%d" % (tag, passed1, cell["issuer_count"], missing or "none", passed2, len(cell["named"])))
        return 1
    print("%s-OK issuer=%d named=%d worker=%d" % (tag, passed1, len(cell["named"]), passed2))
    return 0


def regress(key):
    cell = CELLS[key]
    tag = cell["env"][1]
    total, bad = 0, []
    for path in cell["regress"]:
        rc, line, passed, nbad, _ = pytest_run([path])
        total += passed
        if rc != 0 or nbad:
            bad.append((path.rsplit("/", 1)[-1], line))
    diff = subprocess.run(["git", "diff", "--name-only", "box/dell2...HEAD"], capture_output=True, text=True).stdout.split()
    folder = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~"
    stray = [p for p in diff if p not in cell["own"] and p != cell["worker"] and not p.startswith(ISSUER)
             and not p.startswith(folder) and not p.startswith(cell["order"])]
    if bad or total < cell["min_total"] or stray:
        print("%s-REGRESS-FAIL total=%d (want at least %d) bad=%s stray=%s" % (tag, total, cell["min_total"], str(bad)[:200], str(stray[:5])))
        return 1
    print("%s-REGRESS-OK %d tests in %d files, %d changed paths all the cell's own" % (tag, total, len(cell["regress"]), len(diff)))
    return 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode in ("g109", "g110"):
        sys.exit(grade(mode[1:]))
    if mode in ("regress109", "regress110"):
        sys.exit(regress(mode[7:]))
    print("usage: ar_g109_checks.py g109 | g110 | regress109 | regress110")
    sys.exit(2)
