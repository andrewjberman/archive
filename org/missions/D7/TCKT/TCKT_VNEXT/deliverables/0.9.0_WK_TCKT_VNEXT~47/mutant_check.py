"""TCKT_VNEXT TO-R19-L3 (cell R19-ps-3) -- AC2, the one mutant that must FIRE.

    python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~47/mutant_check.py

Copies the ticket_center folder (lambda_function.py and tests/) to a scratch directory OUTSIDE the product tree, puts
back the PRE-R19 tail of _profile_scope (a missing or empty allowedFirmIds reads every firm), runs the new test file
against that copy with pytest, and prints MUTANT-FIRES only when pytest reports failing tests. Otherwise it prints
MUTANT-SURVIVES and exits 1. The product tree is read, never written.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
NEW_TEST = "test_profile_scope_fail_closed.py"
HEAD_MARK = "    has_marker = \"scope_all_firms\" in got\n"
TAIL_END = "\n\n\ndef _resolve_scope(actor: dict, pc: str):"
# the pre-R19 tail, verbatim from b84a2ca293 (what _profile_scope returned before this cell)
OLD_TAIL = (
    "    val = got.get(\"allowedFirmIds\")\n"
    "    if val is None:\n"
    "        return None, None\n"
    "    if isinstance(val, list):\n"
    "        if not val:\n"
    "            return None, None\n"
    "        if all(isinstance(f, str) and f for f in val):\n"
    "            return frozenset(val), None\n"
    "    return None, _resp(403, {\"error\": \"firm scope malformed\"})\n"
)


def _root():
    d = HERE
    while not os.path.isdir(os.path.join(d, ".tools")):
        parent = os.path.dirname(d)
        if parent == d:
            sys.exit("ERROR: no .tools/ directory above this checker")
        d = parent
    return d


def main():
    src_dir = os.path.join(_root(), "infra", "aws", "lambda", "ticket_center")
    src_path = os.path.join(src_dir, "lambda_function.py")
    with open(src_path, "rb") as f:
        src = f.read().decode("utf-8")
    a = src.find(HEAD_MARK)
    b = src.find(TAIL_END)
    if a < 0 or b < 0 or b < a or src.count(HEAD_MARK) != 1:
        print("ERROR: the _profile_scope tail anchors were not found exactly once; the mutant cannot be built")
        return 1
    mutant = src[:a] + OLD_TAIL + src[b:]
    if mutant == src:
        print("ERROR: the mutant is identical to the source; the check would prove nothing")
        return 1

    dst = tempfile.mkdtemp(prefix="r19l3-mutant-")
    try:
        tc = os.path.join(dst, "infra", "aws", "lambda", "ticket_center")
        shutil.copytree(src_dir, tc, ignore=shutil.ignore_patterns("__pycache__"))
        with open(os.path.join(tc, "lambda_function.py"), "wb") as f:
            f.write(mutant.encode("utf-8"))
        test_path = os.path.join(tc, "tests", NEW_TEST)
        try:
            run = subprocess.run(
                [sys.executable, "-m", "pytest", test_path, "-q", "-p", "no:cacheprovider", "--color=no"],
                cwd=tc, capture_output=True, text=True, timeout=110)
        except subprocess.TimeoutExpired:
            print("MUTANT-SURVIVES: pytest on the mutant timed out (rc 124 is not a kill)")
            return 1
        out = (run.stdout or "") + (run.stderr or "")
        failed_lines = [ln for ln in out.splitlines() if ln.startswith("FAILED ")]
        for ln in failed_lines:
            print(ln[:200])
        tail = [ln for ln in out.splitlines() if re.search(r"\d+ (passed|failed|error)", ln)]
        print("pytest rc=%d on the mutant copy; summary: %s" % (run.returncode, tail[-1] if tail else "none"))
        print("mutant: the pre-R19 tail restored in %s" % os.path.join("<scratch>", "lambda_function.py"))
        if run.returncode == 1 and failed_lines and re.search(r"\d+ failed", out):
            print("MUTANT-FIRES")
            return 0
        print("MUTANT-SURVIVES")
        return 1
    finally:
        shutil.rmtree(dst, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
