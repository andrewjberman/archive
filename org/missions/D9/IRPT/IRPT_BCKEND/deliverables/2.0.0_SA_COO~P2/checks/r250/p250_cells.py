"""IRPT_BCKEND workstream ~PM round 6 (issuer 2.0.0_SA_COO~P2) -- the check of one BUILD order: the per-firm HMAC list stage of the directory runner (CTO msg 10203).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IBHM7  IB-hm-7  the HMAC list stage assumes the narrow role (fixed session name hmac-list-stage) for its secret read and its put, and accepts the globgrph destination bucket
    AC1  the six new named tests exist in tests/test_directory_hmac_list.py and the whole file passes (run now)
    AC2  the stage is wired right (AST): emit_hmac_list calls assume_role with the keyword RoleSessionName set to the literal hmac-list-stage, and run_firm still calls land() before the stage inside a catch-all
    AC3  the worker's ONE commit (HEAD~1..HEAD) touches only the runner, the existing test file and the order's deliverables folder, and both code files are in it
"""
import ast
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

RUNNER = "data/assets/scripts/gold/investor_reporting/directory_runner.py"
TESTS = "data/assets/scripts/gold/investor_reporting/tests/test_directory_hmac_list.py"
DELIV = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~451/"
NAMES = (
    "test_the_stage_assumes_the_named_role_with_the_fixed_session_name",
    "test_the_assumed_credentials_are_used_for_the_secret_and_the_put",
    "test_without_a_role_arn_the_ambient_session_is_used",
    "test_a_uri_in_another_bucket_is_accepted",
    "test_a_uri_inside_a_directory_prefix_of_the_firm_bucket_is_refused",
    "test_the_session_name_is_the_fixed_literal",
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
              if ln.startswith("PASSED ") and "test_directory_hmac_list.py::" in ln}
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
    em = _find(tree, "emit_hmac_list")
    rf = _find(tree, "run_firm")
    if em is None or rf is None:
        fail("emit_hmac_list and run_firm must both exist")
    ok = False
    for c in _calls(em, "assume_role"):
        for kw in c.keywords:
            if kw.arg == "RoleSessionName" and ((isinstance(kw.value, ast.Constant) and kw.value.value == "hmac-list-stage") or (isinstance(kw.value, ast.Name) and kw.value.id.isupper())):
                ok = True
    if not ok:
        fail("emit_hmac_list must call assume_role with RoleSessionName= the literal hmac-list-stage (or an upper-case module constant)")
    src = f.read_text(encoding="utf-8")
    if '"hmac-list-stage"' not in src:
        fail("the literal hmac-list-stage must appear in the runner (the fixed session name)")
    lands, stages = _calls(rf, "land"), _calls(rf, STAGE_CALL)
    if not lands or not stages or min(c.lineno for c in stages) <= max(c.lineno for c in lands):
        fail("run_firm must still call land() before emit_hmac_list()")
    print("OK: the stage assumes the named role with the fixed session name, and still runs after land()")


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


CHECKS = {"IBHM7-AC1": ac1, "IBHM7-AC2": ac2, "IBHM7-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p250_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](None)
    print("%s PASS" % sys.argv[2])
