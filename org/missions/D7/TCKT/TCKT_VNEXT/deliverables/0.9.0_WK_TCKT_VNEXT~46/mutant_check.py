"""TO-R19-L2 AC2 (R19-ai-2): the intake firm filter mutant.

Copies lambda_function.py to a scratch folder with the svc-analyst-intake firm filter removed (the filter's `if` is
replaced by `if False:`, so every firm is returned), runs the new test file against the copy with pytest, and prints
MUTANT-FIRES only when that run FAILS on its assertions (pytest exit 1). Otherwise it prints MUTANT-SURVIVES and exits 1.

    python C:/dev/wk-tckt-vnext-46/org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~46/mutant_check.py

The product tree is only read. The scratch copy lives under the worktree's .scratch/ folder (git-ignored), never in infra/aws.
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAMBDA_REL = os.path.join("infra", "aws", "lambda", "ticket_center")
TESTS_REL = os.path.join(LAMBDA_REL, "tests")
NEW_TEST = "test_analyst_intake_scoped.py"
MUTATION_FROM = "    if pc == SVC_ANALYST_INTAKE:\n        # R19-ai-2: the intake principal sees only"
MUTATION_TO = "    if False:  # MUTANT: intake firm filter removed\n        # R19-ai-2: the intake principal sees only"


def _worktree_root():
    p = HERE
    for _ in range(16):
        if os.path.isfile(os.path.join(p, LAMBDA_REL, "lambda_function.py")):
            return p
        parent = os.path.dirname(p)
        if parent == p:
            break
        p = parent
    return None


def main():
    root = _worktree_root()
    if root is None:
        print("MUTANT-SURVIVES: worktree root with lambda_function.py not found")
        return 1
    src_dir = os.path.join(root, LAMBDA_REL)
    with open(os.path.join(src_dir, "lambda_function.py"), encoding="utf-8") as f:
        src = f.read()
    hits = src.count(MUTATION_FROM)
    if hits != 1:
        print("MUTANT-SURVIVES: mutation point found %d times (expected 1); no mutant built" % hits)
        return 1
    mutated = src.replace(MUTATION_FROM, MUTATION_TO)

    scratch = os.path.join(root, ".scratch", "mutant_r19_ai_2_%d" % os.getpid())
    if os.path.isdir(scratch):
        shutil.rmtree(scratch)
    tc = os.path.join(scratch, "ticket_center")
    try:
        shutil.copytree(os.path.join(root, TESTS_REL), os.path.join(tc, "tests"),
                        ignore=shutil.ignore_patterns("__pycache__"))
        with open(os.path.join(tc, "lambda_function.py"), "w", encoding="utf-8", newline="") as f:
            f.write(mutated)
        test_path = os.path.join(tc, "tests", NEW_TEST)
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        proc = subprocess.run([sys.executable, "-m", "pytest", test_path, "-q", "-p", "no:cacheprovider", "--color=no"],
                              cwd=scratch, env=env, capture_output=True, text=True, timeout=120)
        tail = [ln for ln in (proc.stdout or "").splitlines() if ln.strip()][-1:]
        print("mutant run (copy of lambda_function.py with the intake firm filter removed, file %s):" % NEW_TEST)
        print("  pytest rc=%d  summary: %s" % (proc.returncode, tail[0] if tail else "(none)"))
        if proc.returncode == 1:
            print("MUTANT-FIRES")
            return 0
        print("MUTANT-SURVIVES: the run did not fail on assertions (pytest rc=%d)" % proc.returncode)
        return 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
