#!/usr/bin/env python3
"""exercise_switch_on -- the placement switch's wiring in .tools/safe-commit.sh and .tools/safe-apply.sh (LGIC_BLANKFIX BF-x-3).

    python org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~2/exercise_switch_on.py

WHAT RUNS. Nothing in the repository is run in place and nothing is written in it. The exercise builds ONE temporary tree (outside
the repository) that holds byte copies of .tools/naming-gate.py, .tools/naming-apply-gate.py, lib/*.py and the registry's json,
plus a git repository with one baseline commit (git plumbing). It then cuts the REAL naming limbs out of the real scripts -- the
text of .tools/safe-commit.sh from its `if [ -n "$IN_SCOPE" ]` naming stage to the line before the LAYER 2 banner, and the text
of .tools/safe-apply.sh from the `SA_TARGETED=0` argument parse to the line before the TAG-AUTHORIZATION banner -- and runs each
cut in bash with SCRIPT_DIR pointed at the temporary tree, so the switch the script tests is the temporary tree's
org/mcp/naming-place.enforce. The repository's own org/mcp/ is never read as a switch and no switch file is created in it.

THE ONE STAND-IN. The placement decision itself (lib/opal_naming_rootcheck.py place()) is cell BF-w-1's and costs about 13 s a
root; this cell wires its refusal into the two scripts. In the temporary tree that module is replaced by a recorder that answers
FIX for a hand-built name ("irpt-directory-newjob") and RIGHT for any other, and writes each call (the root it was handed, and
whether the root was found by a name) to a file. Everything else -- the gates, the grader, the registry, the scripts' limbs -- is
the real text. The pre-plan arms (B) use a second tree whose apply gate is a ten-line stand-in that prints the placement line:
the real gate's directory mode cannot refuse (it cannot tell an addition from an existing resource), so that arm shows the script
acts on the line, not that the gate emits it. terraform is a fake script that renders a one-resource plan.

ARMS (the older switch, naming-gate.enforce, is ABSENT unless the arm says so):
  A1  commit, placement switch PRESENT          -> blocked (exit 1), the gate's placement line printed
  A2  commit, placement switch ABSENT           -> not blocked (the DIFFERENCE CONTROL of A1: same name, same tree)
  A3  commit, switch PRESENT and older ON       -> blocked
  A4  commit, an older-limb REFUSE, both OFF    -> not blocked (the warn window is unchanged)
  A5  commit, the same name, older ON           -> blocked (the older limb still blocks)
  B1  apply pre-plan stage, switch PRESENT      -> exit 6 (stand-in gate prints the placement line)
  B2  apply pre-plan stage, switch ABSENT       -> not blocked (difference control of B1)
  P1  apply plan stage, switch PRESENT          -> exit 7
  P2  apply plan stage, switch ABSENT           -> not blocked (difference control of P1)
  P3  plan stage: the gate received the tree    -> the placement call got the -chdir root, and no root was looked up by name
  P4  plan stage with no -chdir (control)       -> the gate was given ".", and the root was looked up by the added name
One line per arm: expected and got. Last line, printed once: SWITCH-ON ok=<bool> arms=<n> held=<n>
Python 3.9; ASCII only; standard library only.
"""
import os
import shutil
import stat
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def repo_root(start):
    d = start
    for _ in range(40):
        if os.path.isdir(os.path.join(d, ".tools")) and os.path.isdir(os.path.join(d, "org")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("SWITCH-ON ok=False arms=0 held=0 (no repository root above %s)" % start)


ROOT = repo_root(HERE)
SAFE_COMMIT = os.path.join(ROOT, ".tools", "safe-commit.sh")
SAFE_APPLY = os.path.join(ROOT, ".tools", "safe-apply.sh")
ROOT_REL = "infra/aws/terraform/zz-stub-root"
TF_REL = ROOT_REL + "/main.tf"
BAD_NAME = "irpt-directory-newjob"
OLD_REFUSE_NAME = "irpt-directory-bad_name"

BASE_TF = '''resource "aws_scheduler_schedule" "existing" {
  name = "zz-existing-daily"
}
'''
BLOCK = '''
resource "aws_scheduler_schedule" "added" {
  name = "%s"
}
'''

STUB_ROOTCHECK = '''"""Temporary stand-in for lib/opal_naming_rootcheck.py in the BF-x-3 exercise: records the calls, answers by name."""
import os

_TF_PREFIX = "infra/aws/terraform/"
ROOT = "infra/aws/terraform/zz-stub-root"


def map_key(root):
    r = str(root).replace("\\\\", "/").strip().strip("/")
    return r[len(_TF_PREFIX):] if r.startswith(_TF_PREFIX) else r


def _rec(line):
    with open(os.environ["STUB_REC"], "a") as fh:
        fh.write(line + "\\n")


def _res(name):
    if name == "irpt-directory-" + "newjob":
        return {"kind": "FIX", "detail": name, "form": name + "-daily", "mapped": True, "fills": [], "owed": []}
    return {"kind": "RIGHT", "detail": name, "form": None, "mapped": True, "fills": [], "owed": []}


def root_of_path(path):
    return ROOT if str(path).replace("\\\\", "/").startswith(ROOT + "/") else None


def roots_of_name(name, typ=None):
    _rec("roots_of_name %s" % name)
    return [ROOT]


def place_many(root, map_path, wants, texts=None):
    _rec("place_many root=%s" % root)
    return [_res(w[0]) for w in wants]


def place_root(root, map_path, wants, post_texts, head_texts, ratchet=True):
    _rec("place_root root=%s" % root)
    return {"results": [_res(w[0]) for w in wants], "mapped": True, "root": root, "post_holes": 0, "head_holes": 0,
            "new_holes": [], "names_post": 1, "names_head": 1}


def refusal_text(res):
    return res["form"], "NEW name the canon places as FIX. Owed: use %s." % res["form"]


def ratchet_text(root_res):
    return "the unplaceable-name list grew"
'''

STAND_IN_APPLY_GATE = '''import sys
if "--plan-json" in sys.argv:
    print("NAMING-PLAN: PASS 0 graded")
    sys.exit(0)
print("NAMING-PLACE: REFUSE 1")
print("NAMING-GATE: REFUSE 1 graded")
sys.exit(1)
'''

FAKE_TERRAFORM = r'''#!/bin/bash
# a fake terraform: `plan ... -out=F` writes F; `show -json F` prints a plan that ADDS one scheduler schedule
for a in "$@"; do
  case "$a" in
    -out=*) echo fake-plan > "${a#-out=}" ;;
  esac
done
prev=""
for a in "$@"; do prev="$a"; done
if [ "$1" != "" ]; then
  for a in "$@"; do
    if [ "$a" = "show" ]; then
      cat <<'JSON'
{"format_version":"1.2","resource_changes":[{"address":"aws_scheduler_schedule.added","mode":"managed","type":"aws_scheduler_schedule","name":"added","change":{"actions":["create"],"before":null,"after":{"name":"irpt-directory-newjob"}}}]}
JSON
      exit 0
    fi
  done
fi
exit 0
'''


def fwd(p):
    return p.replace("\\", "/")


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="\n", encoding="utf-8") as fh:
        fh.write(text)


def git(tree, *args, input_text=None):
    p = subprocess.run(["git"] + list(args), cwd=tree, capture_output=True, input=input_text)
    if p.returncode != 0:
        raise RuntimeError("git %s failed rc=%d: %s" % (" ".join(args), p.returncode, p.stderr.decode("utf-8", "replace")[:300]))
    return p.stdout.decode("utf-8", "replace").strip()


def build_tree(td, name, gate_apply_stand_in=False):
    """One temporary tree: copies of the gates, lib/*.py (rootcheck replaced), the registry json, a git repo with a baseline."""
    t = os.path.join(td, name)
    for rel in ("naming-gate.py", "naming-apply-gate.py"):
        os.makedirs(os.path.join(t, ".tools"), exist_ok=True)
        shutil.copyfile(os.path.join(ROOT, ".tools", rel), os.path.join(t, ".tools", rel))
    if gate_apply_stand_in:
        write(os.path.join(t, ".tools", "naming-apply-gate.py"), STAND_IN_APPLY_GATE)
    os.makedirs(os.path.join(t, "lib"))
    for fn in os.listdir(os.path.join(ROOT, "lib")):
        src = os.path.join(ROOT, "lib", fn)
        if fn.endswith(".py") and os.path.isfile(src):
            shutil.copyfile(src, os.path.join(t, "lib", fn))
    write(os.path.join(t, "lib", "opal_naming_rootcheck.py"), STUB_ROOTCHECK)
    reg = os.path.join(t, "infra", "logic", "registry")
    os.makedirs(reg)
    for fn in os.listdir(os.path.join(ROOT, "infra", "logic", "registry")):
        src = os.path.join(ROOT, "infra", "logic", "registry", fn)
        if os.path.isfile(src):
            shutil.copyfile(src, os.path.join(reg, fn))
    os.makedirs(os.path.join(t, "org", "mcp"))
    os.makedirs(os.path.join(t, "org", "standards"))
    for rel in ("org/standards/NAMING_SCHEMA.json", "org/missions/DIRECTIVES.yaml"):
        os.makedirs(os.path.dirname(os.path.join(t, rel)), exist_ok=True)
        shutil.copyfile(os.path.join(ROOT, rel), os.path.join(t, rel))
    write(os.path.join(t, TF_REL), BASE_TF)
    git(t, "init", "-q")
    git(t, "add", "-A")
    tree_id = git(t, "write-tree")
    env_commit = git(t, "-c", "user.name=ex", "-c", "user.email=ex@example.invalid", "commit-tree", tree_id, "-m", "baseline")
    git(t, "update-ref", "HEAD", env_commit)
    ft = os.path.join(t, ".tools", "terraform")
    write(ft, FAKE_TERRAFORM)
    os.chmod(ft, os.stat(ft).st_mode | stat.S_IEXEC)
    return t


def set_switch(t, fname, on):
    p = os.path.join(t, "org", "mcp", fname)
    if on:
        write(p, "temporary switch for the BF-x-3 exercise\n")
    elif os.path.exists(p):
        os.remove(p)


def cut(path, start_marker, end_marker):
    """The text of `path` from the line that starts with start_marker to the line before the last `# ----` banner line that
    precedes end_marker. Raises when either marker is absent or not unique."""
    with open(path, "r", encoding="utf-8", newline="") as fh:
        lines = fh.read().replace("\r\n", "\n").split("\n")
    starts = [i for i, ln in enumerate(lines) if ln.startswith(start_marker)]
    ends = [i for i, ln in enumerate(lines) if ln.startswith(end_marker)]
    if len(starts) != 1 or len(ends) != 1:
        raise RuntimeError("markers in %s: start %r x%d, end %r x%d" % (path, start_marker, len(starts), end_marker, len(ends)))
    e = ends[0]
    while e > starts[0] and not lines[e - 1].startswith("# ----"):
        e -= 1
    return "\n".join(lines[starts[0]:e - 1]) + "\n"


def run_bash(script_text, t, extra_env=None):
    env = dict(os.environ)
    for k in ("NAMING_GATE_ENFORCE", "NAMING_PLACE_PREVIEW"):
        env.pop(k, None)
    env["OPAL_AGENT_SERIAL"] = "0.9.0_WK_LGIC_BLANKFIX~2"
    env["STUB_REC"] = os.path.join(t, "stub.rec")
    env.update(extra_env or {})
    sf = os.path.join(t, "cut.sh")
    write(sf, script_text)
    p = subprocess.run(["bash", fwd(sf)], cwd=t, env=env, capture_output=True)
    return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")


def commit_limb(t, name, older_on, place_on):
    """Stage a one-resource addition named `name`, then run safe-commit.sh's real naming stage. (rc, text)."""
    set_switch(t, "naming-gate.enforce", older_on)
    set_switch(t, "naming-place.enforce", place_on)
    write(os.path.join(t, TF_REL), BASE_TF + BLOCK % name)
    git(t, "add", "--", TF_REL)
    body = cut(SAFE_COMMIT, 'if [ -n "$IN_SCOPE" ] && [ -f "$SCRIPT_DIR/naming-gate.py" ]; then',
               "# LAYER 2 of the CANONICAL FABRIC WORKFLOW")
    script = 'SCRIPT_DIR="%s"\nIN_SCOPE="%s"\n%s\necho REACHED-END\n' % (fwd(os.path.join(t, ".tools")), TF_REL, body)
    rc, out = run_bash(script, t)
    git(t, "reset", "-q", "HEAD", "--", TF_REL)
    write(os.path.join(t, TF_REL), BASE_TF)
    return rc, out


def apply_limb(t, older_on, place_on, tree_arg):
    """Run safe-apply.sh's real naming stages (pre-plan, then plan) with the fake terraform. (rc, text)."""
    set_switch(t, "naming-gate.enforce", older_on)
    set_switch(t, "naming-place.enforce", place_on)
    write(os.path.join(t, "stub.rec"), "")
    body = cut(SAFE_APPLY, "SA_TARGETED=0; SA_PLANFILE=", "# TAG-AUTHORIZATION pre-apply gate")
    args = ("%s " % tree_arg if tree_arg else "") + "apply"
    script = 'SCRIPT_DIR="%s"\nTERRAFORM="%s"\nset -- %s\n%s\necho REACHED-END\n' % (
        fwd(os.path.join(t, ".tools")), fwd(os.path.join(t, ".tools", "terraform")), args, body)
    rc, out = run_bash(script, t)
    with open(os.path.join(t, "stub.rec"), "r") as fh:
        rec = fh.read().splitlines()
    return rc, out, rec


def main():
    arms = []  # (label, expected, got, held)

    def arm(label, expected, got, held):
        arms.append((label, expected, got, bool(held)))

    td = tempfile.mkdtemp(prefix="bfx3_switch_on_")
    try:
        t = build_tree(td, "tree")
        # ---- commit limb
        rc, out = commit_limb(t, BAD_NAME, older_on=False, place_on=True)
        arm("A1 commit, placement switch PRESENT, older OFF", "rc=1 blocked, NAMING-PLACE line",
            "rc=%d %s" % (rc, "blocked" if "REACHED-END" not in out else "passed")
            + (", NAMING-PLACE line" if "NAMING-PLACE: REFUSE" in out else ", no placement line"),
            rc == 1 and "REACHED-END" not in out and "placement step refused" in out and "NAMING-PLACE: REFUSE" in out)
        rc, out = commit_limb(t, BAD_NAME, older_on=False, place_on=False)
        arm("A2 commit, placement switch ABSENT, older OFF (control of A1)", "rc=0 not blocked",
            "rc=%d %s" % (rc, "passed" if "REACHED-END" in out else "blocked"), rc == 0 and "REACHED-END" in out)
        rc, out = commit_limb(t, BAD_NAME, older_on=True, place_on=True)
        arm("A3 commit, placement switch PRESENT, older ON", "rc=1 blocked",
            "rc=%d %s" % (rc, "passed" if "REACHED-END" in out else "blocked"), rc == 1 and "REACHED-END" not in out)
        rc, out = commit_limb(t, OLD_REFUSE_NAME, older_on=False, place_on=False)
        old_refused = "NAMING REFUSE" in out
        arm("A4 commit, an older-limb REFUSE name, both OFF (warn window)", "rc=0 not blocked, the REFUSE verdict printed",
            "rc=%d %s, REFUSE verdict %s" % (rc, "passed" if "REACHED-END" in out else "blocked",
                                             "printed" if old_refused else "absent"),
            rc == 0 and "REACHED-END" in out and old_refused)
        rc, out = commit_limb(t, OLD_REFUSE_NAME, older_on=True, place_on=False)
        arm("A5 commit, the same name, older ON, placement OFF", "rc=1 blocked by the older limb",
            "rc=%d %s%s" % (rc, "passed" if "REACHED-END" in out else "blocked",
                            ", older-limb message" if "the naming limb refused (LGIC_ENFORCE" in out else ""),
            rc == 1 and "REACHED-END" not in out and "the naming limb refused (LGIC_ENFORCE" in out)
        # ---- apply limb, pre-plan stage (stand-in gate)
        t2 = build_tree(td, "tree2", gate_apply_stand_in=True)
        rc, out, _rec = apply_limb(t2, older_on=False, place_on=True, tree_arg="-chdir=" + ROOT_REL)
        arm("B1 apply pre-plan, placement switch PRESENT, older OFF", "rc=6 blocked",
            "rc=%d %s" % (rc, "passed" if "REACHED-END" in out else "blocked"), rc == 6 and "REACHED-END" not in out)
        rc, out, _rec = apply_limb(t2, older_on=False, place_on=False, tree_arg="-chdir=" + ROOT_REL)
        arm("B2 apply pre-plan, placement switch ABSENT, older OFF (control of B1)", "rc=0 not blocked",
            "rc=%d %s" % (rc, "passed" if "REACHED-END" in out else "blocked"), rc == 0 and "REACHED-END" in out)
        # ---- apply limb, plan stage (real gates, recorder rootcheck, fake terraform)
        t3 = os.path.join(td, "tree")
        rc, out, rec = apply_limb(t3, older_on=False, place_on=True, tree_arg="-chdir=" + ROOT_REL)
        arm("P1 apply plan stage, placement switch PRESENT, older OFF", "rc=7 blocked, NAMING-PLACE line",
            "rc=%d %s%s" % (rc, "passed" if "REACHED-END" in out else "blocked",
                            ", NAMING-PLACE line" if "NAMING-PLACE: REFUSE" in out else ", no placement line"),
            rc == 7 and "REACHED-END" not in out and "NAMING-PLACE: REFUSE" in out)
        got_tree = [ln for ln in rec if ln.startswith("place_many root=")]
        by_name = [ln for ln in rec if ln.startswith("roots_of_name")]
        arm("P3 apply plan stage: the gate received the tree", "place_many root=%s and no roots_of_name" % ROOT_REL,
            "%s; roots_of_name calls=%d" % (got_tree[0] if got_tree else "no place_many call", len(by_name)),
            got_tree == ["place_many root=%s" % ROOT_REL] and not by_name)
        rc, out, rec = apply_limb(t3, older_on=False, place_on=False, tree_arg="-chdir=" + ROOT_REL)
        arm("P2 apply plan stage, placement switch ABSENT, older OFF (control of P1)", "rc=0 not blocked",
            "rc=%d %s" % (rc, "passed" if "REACHED-END" in out else "blocked"), rc == 0 and "REACHED-END" in out)
        rc, out, rec = apply_limb(t3, older_on=False, place_on=True, tree_arg="")
        by_name = [ln for ln in rec if ln.startswith("roots_of_name")]
        arm("P4 apply plan stage, no -chdir (control of P3)", "tree '.' is no root; the root is looked up by the added name",
            "roots_of_name calls=%d, place_many roots=%s" % (len(by_name), [ln.split("=", 1)[1] for ln in rec
                                                                            if ln.startswith("place_many root=")]),
            len(by_name) == 1 and ["place_many root=%s" % ROOT_REL] == [ln for ln in rec if ln.startswith("place_many root=")])
    finally:
        def _onerr(func, path, _exc):
            try:
                os.chmod(path, stat.S_IWRITE)
                func(path)
            except OSError:
                pass
        shutil.rmtree(td, onerror=_onerr)
    held = 0
    for label, expected, got, ok in arms:
        held += 1 if ok else 0
        print("ARM %s | expected: %s | got: %s | %s" % (label, expected, got, "ok" if ok else "FAIL"))
    print("SWITCH-ON ok=%s arms=%d held=%d" % (held == len(arms), len(arms), held))
    return 0 if held == len(arms) else 1


if __name__ == "__main__":
    sys.exit(main())
