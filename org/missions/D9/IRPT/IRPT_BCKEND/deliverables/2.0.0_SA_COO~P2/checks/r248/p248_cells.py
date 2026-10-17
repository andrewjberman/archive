"""IRPT_BCKEND workstream ~PM round 6 (issuer 2.0.0_SA_COO~P2) -- the check of one BUILD order: the per-firm HMAC list stage of the directory runner (CTO msg 10203).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IBHM2  IB-hm-2  a LAST stage in directory_runner.run_firm that writes HMAC-SHA256(key, UPPER(raw account key)) and the minted hex to one key per firm; its failure cannot touch the directory
    AC1  the ten named tests exist in tests/test_directory_hmac_list.py and ALL pass (run now)
    AC2  the stage is wired right (AST): in run_firm the call to land() comes before the stage's call, the stage's call sits inside a try whose handler catches Exception, and run_firm still returns the landed result
    AC3  the worker's ONE commit (HEAD~1..HEAD) touches only the runner, the new test file and the order's deliverables folder, and both code files are in it
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
DELIV = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~449/"
NAMES = (
    "test_known_raw_key_yields_the_reference_hmac",
    "test_minted_hex_is_hashed_uppercase_with_the_prefix_dropped",
    "test_output_is_sorted_unique_lines_of_hex_only",
    "test_output_holds_no_plain_sha256_of_any_known_id",
    "test_same_input_is_byte_identical",
    "test_empty_input_writes_nothing",
    "test_a_planted_failure_in_the_stage_leaves_the_directory_result_untouched",
    "test_stage_is_skipped_without_the_two_arguments",
    "test_no_id_appears_in_any_printed_line",
    "test_hyphen_stripped_variant_is_included_when_different",
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
    rf = _find(tree, "run_firm")
    if rf is None:
        fail("run_firm not found")
    lands, stages = _calls(rf, "land"), _calls(rf, STAGE_CALL)
    if not lands or not stages:
        fail("run_firm must call land() and %s()" % STAGE_CALL)
    if min(c.lineno for c in stages) <= max(c.lineno for c in lands):
        fail("the stage call must come AFTER land() in run_firm (it is the LAST stage)")
    inside = False
    for n in ast.walk(rf):
        if isinstance(n, ast.Try):
            body_calls = [c for s in n.body for c in _calls(s, STAGE_CALL)]
            if body_calls and any((h.type is None) or (isinstance(h.type, ast.Name) and h.type.id in ("Exception", "BaseException")) for h in n.handlers):
                inside = True
    if not inside:
        fail("the stage call must sit inside a try whose handler catches Exception")
    if not any(isinstance(n, ast.Return) for n in ast.walk(rf)):
        fail("run_firm must still return its result")
    print("OK: the stage runs after land(), inside a catch-all, and run_firm still returns")


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


CHECKS = {"IBHM2-AC1": ac1, "IBHM2-AC2": ac2, "IBHM2-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p248_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](None)
    print("%s PASS" % sys.argv[2])
