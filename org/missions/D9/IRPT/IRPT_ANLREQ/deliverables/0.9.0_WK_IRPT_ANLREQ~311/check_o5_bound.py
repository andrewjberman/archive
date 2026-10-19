"""O5 bound check (IRPT_ANLREQ AR-y-417): the branch's committed change is exactly the O5 trigger rule.

Stdlib only. Run from the worktree root:
    python -I org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~311/check_o5_bound.py
Branch point = git merge-base HEAD box/dell2. Changed paths = the committed diff from that point to HEAD, excluding org/.
Pass = exactly the three named files AND, in resident_worker.py, only send_ready_if_ticketed differs (ast.dump).
"""
import ast
import subprocess
import sys

BASE_REF = "box/dell2"
GENERATE = "infra/aws/lambda/investor-reporting/ycharts/generate/"
RESIDENT = GENERATE + "resident_worker.py"
EXPECTED = [
    RESIDENT,
    GENERATE + "tests/test_ready_signal_commentary_gate.py",
    GENERATE + "tests/test_ready_signal_on_ready.py",
]
ONLY_CHANGED = "send_ready_if_ticketed"


def git(*args):
    proc = subprocess.run(["git"] + list(args), capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        raise RuntimeError("git %s rc=%d %s" % (" ".join(args), proc.returncode, proc.stderr.strip()))
    return proc.stdout


def bad(what):
    print("O5-BOUND-BAD " + what)
    sys.exit(1)


def top_level(source):
    """Map each top-level def/class name to its dumps, and keep the other top-level statements in order."""
    defs, rest = {}, []
    for node in ast.parse(source).body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defs.setdefault(node.name, []).append(ast.dump(node))
        else:
            rest.append(ast.dump(node))
    return defs, rest


def main():
    base = git("merge-base", "HEAD", BASE_REF).strip()
    changed = [p for p in git("diff", "--name-only", base, "HEAD").splitlines() if p and not p.startswith("org/")]
    if sorted(changed) != sorted(EXPECTED):
        bad("changed-outside-org=%s expected=%s base=%s" % (sorted(changed), sorted(EXPECTED), base))
    old_defs, old_rest = top_level(git("show", base + ":" + RESIDENT))
    new_defs, new_rest = top_level(git("show", "HEAD:" + RESIDENT))
    differs = sorted(name for name in set(old_defs) | set(new_defs) if old_defs.get(name) != new_defs.get(name))
    if differs != [ONLY_CHANGED]:
        bad("definitions-differing=%s base=%s" % (differs, base))
    if old_rest != new_rest:
        bad("non-definition top-level statements differ base=%s" % base)
    print("O5-BOUND-OK files=%d" % len(changed))


if __name__ == "__main__":
    main()
