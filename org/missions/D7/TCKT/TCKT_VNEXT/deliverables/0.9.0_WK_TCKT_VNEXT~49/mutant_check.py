"""TCKT_VNEXT R20-lm-2 (TO-R20-LM, AC2) -- the mutant check for the attachment open route's same-member fence.

It copies the ticket_center folder (lambda_function.py and tests/) to a scratch folder inside this worktree's gitignored
.scratch/, runs the new test file against the UNMUTATED copy (a positive control: it must pass), then removes the step-1
equality refusal from the copy's attachment_open_ticket and runs the same test file again. The mutant FIRES only when that
run FAILS. Nothing outside .scratch/ is written; no AWS, no network. Run by path with the interpreter, not under pytest.

Prints MUTANT-FIRES (exit 0) or MUTANT-SURVIVES (exit 1); a control or anchor failure prints CONTROL-FAILS or ANCHOR-MISSING (exit 2).
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
TC = os.path.join(ROOT, "infra", "aws", "lambda", "ticket_center")
TEST_NAME = "test_attachment_open_same_member.py"

# The step-1 equality refusal, exactly as it stands in lambda_function.py (the anchor the mutant removes).
FENCE = (
    '    if req_firm != str((cur.get("answers") or {}).get("firm") or ""):\n'
    '        return _resp(404, {"error": f"ticket {tid} carries no attachment"})\n'
)


def _run_tests(scratch):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    cmd = [sys.executable, "-m", "pytest", os.path.join(scratch, "tests", TEST_NAME),
           "-q", "-p", "no:cacheprovider", "--color=no"]
    proc = subprocess.run(cmd, cwd=scratch, env=env, timeout=120, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = proc.stdout.decode("utf-8", "replace")
    return proc.returncode, out.strip().splitlines()[-1] if out.strip() else "(no output)"


def main():
    scratch = os.path.join(ROOT, ".scratch", "mutant_R20LM")
    if os.path.isdir(scratch):
        shutil.rmtree(scratch)
    os.makedirs(scratch)
    dst = os.path.join(scratch, "ticket_center")
    shutil.copytree(TC, dst, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    lam = os.path.join(dst, "lambda_function.py")
    with open(lam, encoding="utf-8") as f:
        src = f.read()
    if src.count(FENCE) != 1:
        print("ANCHOR-MISSING: the step-1 refusal occurs %d times in lambda_function.py (need exactly 1)" % src.count(FENCE))
        return 2

    rc0, last0 = _run_tests(dst)
    print("CONTROL unmutated copy: rc=%d | %s" % (rc0, last0))
    if rc0 != 0:
        print("CONTROL-FAILS: the unmutated copy does not pass the new test file")
        return 2

    with open(lam, "w", encoding="utf-8") as f:
        f.write(src.replace(FENCE, ""))
    rc1, last1 = _run_tests(dst)
    print("MUTANT step-1 equality refusal removed: rc=%d | %s" % (rc1, last1))
    if rc1 != 0:
        print("MUTANT-FIRES")
        return 0
    print("MUTANT-SURVIVES")
    return 1


if __name__ == "__main__":
    sys.exit(main())
