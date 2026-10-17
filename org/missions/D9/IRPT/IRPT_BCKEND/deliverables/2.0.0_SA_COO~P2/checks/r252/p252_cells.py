"""IRPT_BCKEND workstream ~PM round 6 (issuer 2.0.0_SA_COO~P2) -- the check of one BUILD order: the dispatch half of the per-firm HMAC list in refresh.py (CTO msgs 10203 and 10234).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IBHM9  IB-hm-9  refresh.py hands the runner's three HMAC arguments to each firm's build, from the Lambda's environment, validated, only when all three are configured
    AC1  the six named tests exist in tests/test_refresh_hmac_args.py and ALL pass (run now)
    AC2  by AST: runner_script takes hmac_args, the module defines _hmac_args_for, and no string constant of refresh.py holds secretsmanager, globgrph, opal-data-assets or an s3:// address
    AC3  the worker's ONE commit (HEAD~1..HEAD) touches only refresh.py, the new test file and the order's paths, and both code files are in it
"""
import ast
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

RUNNER = "infra/aws/lambda/investor-reporting/directory/refresh.py"
TESTS = "infra/aws/lambda/investor-reporting/directory/tests/test_refresh_hmac_args.py"
DELIV = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~453/"
NAMES = (
    "test_all_three_values_yield_the_six_tokens_for_a_firm",
    "test_a_missing_value_yields_no_tokens",
    "test_a_firm_absent_from_the_uri_map_yields_no_tokens",
    "test_an_unsafe_value_is_dropped_never_quoted_around",
    "test_the_script_without_hmac_args_is_byte_identical_to_the_old_script",
    "test_the_dispatcher_passes_the_tokens_into_the_script_and_trails_the_firm_id_only",
)
STAGE_CALL = "emit_hmac_list"
fail = P6.fail


def ac1(_):
    f = P6.ROOT / TESTS
    if not f.is_file():
        fail("no %s" % TESTS)
    src = f.read_text(encoding="utf-8")
    missing = [n for n in NAMES if "def %s(" % n not in src]
    if missing:
        fail("missing tests: %s" % ", ".join(missing))
    p = subprocess.run([sys.executable, "-m", "pytest", TESTS, "-q", "-rA", "--color=no", "-p", "no:cacheprovider"], cwd=str(P6.ROOT), capture_output=True, text=True, timeout=300)
    out = p.stdout
    if p.returncode != 0:
        fail("pytest rc %s: %s" % (p.returncode, out[-300:].replace("\n", " | ")))
    passed = {ln.strip().split("::")[-1].strip() for ln in out.replace("\\", "/").splitlines()
              if ln.startswith("PASSED ") and "test_refresh_hmac_args.py::" in ln}
    notpassed = [n for n in NAMES if n not in passed]
    if notpassed:
        fail("named tests not reported PASSED: %s" % ", ".join(notpassed))
    print("OK: the ten named tests exist and all pass")


def _find(tree, name):
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef) and n.name == name:
            return n
    return None


def _calls(node, name):
    out = []
    for n in ast.walk(node):
        if isinstance(n, ast.Call):
            f = n.func
            nm = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else None)
            if nm == name:
                out.append(n)
    return out


def ac2(_):
    f = P6.ROOT / RUNNER
    if not f.is_file():
        fail("no %s" % RUNNER)
    tree = ast.parse(f.read_text(encoding="utf-8"))
    rs = _find(tree, "runner_script")
    if rs is None or "hmac_args" not in [a.arg for a in rs.args.args + rs.args.kwonlyargs]:
        fail("runner_script must exist and take a parameter named hmac_args")
    if _find(tree, "_hmac_args_for") is None:
        fail("the module must define _hmac_args_for")
    bad = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            v = n.value.lower()
            if "secretsmanager" in v or "globgrph" in v or "opal-data-assets" in v or "s3://" in v:
                # the pre-existing bundle uri handling is by argument, never a literal; any hit is a defect
                bad.append(n.value[:40])
    if bad:
        fail("string constants naming a secret, globgrph, the shared bucket or an s3 address: %s" % bad[:3])
    print("OK: runner_script takes hmac_args, _hmac_args_for is defined, no literal secret or bucket or s3 address")


def ac3(_):
    p = subprocess.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"], cwd=str(P6.ROOT), capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        fail("git diff HEAD~1 HEAD failed: %s" % p.stderr.strip()[:200])
    files = [x.replace("\\", "/") for x in p.stdout.split() if x.strip()]
    if RUNNER not in files or TESTS not in files:
        fail("the worker's commit must contain both the runner and the new test file; it contains %s" % files)
    bad = [x for x in files if x not in (RUNNER, TESTS) and not x.startswith(DELIV) and "INVESTIGATION_v1.md" not in x and "TO-IB-hm-2" not in x]
    if bad:
        fail("the commit touches files outside the order's paths: %s" % bad)
    print("OK: one commit, the runner and the test file in it, nothing outside the order's paths")


CHECKS = {"IBHM9-AC1": ac1, "IBHM9-AC2": ac2, "IBHM9-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p252_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](None)
    print("%s PASS" % sys.argv[2])
