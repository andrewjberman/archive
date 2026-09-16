"""CONTROL harness for LGIC_ENFORCE.TO-EN-t-2 -- NOT a criterion invocation.

It runs check_en.py's own t2 code (its stub terraform, its env, its -chdir trees, its assertions and its VERDICT line)
with TWO disclosed substitutions and nothing else:
  1. argv[0] 'bash' -> shutil.which('bash') (Git Bash). On this box CreateProcess resolves a bare 'bash' to
     C:\\Windows\\System32\\bash.exe, the WSL launcher, before PATH (row LGIC_ENFORCE-W3-S5).
  2. '.tools/safe-apply.sh' -> '.scratch/ctl_<variant>/safe-apply.sh', a byte copy whose sibling halt-gate-check.sh is
     a pass-through stub: the real library fails closed IDENTITY UNRESOLVED in a worker worktree (row LGIC_ENFORCE-W3-S6).

Variants:
  new   the worktree's .tools/safe-apply.sh WITH the naming stage (copied at setup; its naming-apply-gate.py sibling is
        a shim that runs the real .tools/naming-apply-gate.py, so the limb's REPO resolves to the worktree)
  base  the base commit's safe-apply.sh WITHOUT the stage (CLOUD @39aae459ed): the mutant; the refusal must disappear
Arms:
  refuse  check_en.t2_refuse        pass  check_en.t2_pass
  warn    check_en._apply('bad_tree') with NAMING_GATE_ENFORCE removed: WARN mode must reach terraform

Usage, from the worktree root (writes only under .scratch/):
  python org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/controls/t2_controls.py all
  python .../t2_controls.py <new|base> <refuse|pass|warn>
Expected: new refuse PASS-REFUSED-BEFORE-PLAN; new pass PASS-STAGE-PASSES; new warn 'terraform called: True';
          base refuse FAIL-NOT-REFUSED-BEFORE-PLAN; base pass FAIL-GOOD-TREE-BLOCKED.
Standard library only. ASCII only.
"""
import importlib.machinery
import importlib.util
import os
import shutil
import subprocess
import sys

CHECK = "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/check_en.py"
BASE = "39aae459ed"
STUB = ("# CONTROL STUB -- NOT the real library: the real .tools/halt-gate-check.sh fails closed IDENTITY UNRESOLVED in a\n"
        "# worker worktree (no org/mcp/sessions/<CLAUDE_CODE_SESSION_ID>.serial there). Sourced where the real one is.\n"
        "halt_gate_check() {\n"
        "  echo \"HALT-GATE: STUBBED for the control (the real library blocks IDENTITY UNRESOLVED in this worktree)\" >&2\n"
        "  return 0\n"
        "}\n")
SHIM = ("import os, runpy, sys\n"
        "REAL = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.tools', 'naming-apply-gate.py'))\n"
        "sys.argv[0] = REAL\n"
        "runpy.run_path(REAL, run_name='__main__')\n")


def _write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def setup():
    for v in ("new", "base"):
        os.makedirs(os.path.join(".scratch", "ctl_" + v), exist_ok=True)
        _write(os.path.join(".scratch", "ctl_" + v, "halt-gate-check.sh"), STUB)
    shutil.copyfile(os.path.join(".tools", "safe-apply.sh"), os.path.join(".scratch", "ctl_new", "safe-apply.sh"))
    _write(os.path.join(".scratch", "ctl_new", "naming-apply-gate.py"), SHIM)
    p = subprocess.run(["git", "show", "%s:.tools/safe-apply.sh" % BASE], capture_output=True, check=True)
    with open(os.path.join(".scratch", "ctl_base", "safe-apply.sh"), "wb") as fh:
        fh.write(p.stdout)
    print("SETUP: .scratch/ctl_new/safe-apply.sh = worktree bytes (%d); .scratch/ctl_base/safe-apply.sh = %s bytes (%d)" % (
        os.path.getsize(os.path.join(".scratch", "ctl_new", "safe-apply.sh")), BASE, len(p.stdout)))


def arm(variant, which):
    loader = importlib.machinery.SourceFileLoader("check_en_t2_control", CHECK)
    spec = importlib.util.spec_from_loader("check_en_t2_control", loader)
    m = importlib.util.module_from_spec(spec)
    loader.exec_module(m)
    gb = shutil.which("bash")
    sa = ".scratch/ctl_%s/safe-apply.sh" % variant
    orig = m.run

    def run(cmd, cwd=None, env=None, timeout=110, stdin=None):
        if cmd and cmd[0] == "bash":
            cmd = [gb] + [sa if a == ".tools/safe-apply.sh" else a for a in cmd[1:]]
        if env and which == "warn":
            env = dict(env)
            env.pop("NAMING_GATE_ENFORCE", None)
        return orig(cmd, cwd=cwd, env=env, timeout=timeout, stdin=stdin)

    m.run = run
    print("CONTROL variant=%s arm=%s: bash -> %s; safe-apply -> %s" % (variant, which, gb, sa))
    if which == "refuse":
        m.t2_refuse()
    elif which == "pass":
        m.t2_pass()
    else:
        rc, out, called = m._apply("bad_tree")
        print(out.strip()[-600:])
        print("WARN ARM: rc=%d  terraform called: %s" % (rc, called))


if __name__ == "__main__":
    if sys.argv[1:] == ["all"]:
        setup()
        for v, a in (("new", "refuse"), ("new", "pass"), ("new", "warn"), ("base", "refuse"), ("base", "pass")):
            r = subprocess.run([sys.executable, os.path.abspath(__file__), v, a], capture_output=True, text=True)
            lines = (r.stdout + r.stderr).strip().splitlines()
            print("%-4s %-6s rc=%d  %s" % (v, a, r.returncode, " | ".join(ln for ln in lines if ln.startswith(("VERDICT:", "WARN ARM:", "rc=")))))
    else:
        arm(sys.argv[1], sys.argv[2])
