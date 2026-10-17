"""Positive control and negatives for p248_cells.py (run by the issuer at the cut). Usage: python control248.py <real_repo_root>

Builds small synthetic git repositories (a base commit, then ONE worker commit) so the AST, pytest and git-diff arms can each be made to fail.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r248/p248_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p248_cells as P  # noqa: E402

RUNNER_OK = '''def land(*a):
    return {"ok": True}


def emit_hmac_list(*a):
    return None


def run_firm(*a):
    landed = land()
    try:
        emit_hmac_list()
    except Exception:
        pass
    return {"landed": landed}
'''


def tests_src(names, fail_one=False):
    out = ""
    for i, n in enumerate(names):
        out += "def %s():\n    assert %s\n\n\n" % (n, "False" if (fail_one and i == 0) else "True")
    return out


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def build(runner=RUNNER_OK, names=P.NAMES, fail_one=False, extra=None, drop_runner=False, drop_tests=False):
    root = Path(tempfile.mkdtemp(prefix="c248_"))
    shutil.copytree(REAL / "lib", root / "lib", ignore=shutil.ignore_patterns("__pycache__"))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    (root / "README").write_text("base\n", encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")
    paths = []
    if not drop_runner:
        f = root / P.RUNNER
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(runner, encoding="utf-8")
        paths.append(P.RUNNER)
    if not drop_tests:
        t = root / P.TESTS
        t.parent.mkdir(parents=True, exist_ok=True)
        t.write_text(tests_src(names, fail_one), encoding="utf-8")
        paths.append(P.TESTS)
    d = root / (P.DELIV + "IBhm2_note.txt")
    d.parent.mkdir(parents=True, exist_ok=True)
    d.write_text("n\n", encoding="utf-8")
    paths.append(P.DELIV + "IBhm2_note.txt")
    for e in extra or []:
        (root / e).parent.mkdir(parents=True, exist_ok=True)
        (root / e).write_text("x\n", encoding="utf-8")
        paths.append(e)
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "worker")
    return root


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=300, env=dict(os.environ))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


bad = 0


def expect(label, cid, root, want):
    global bad
    r = run(root, cid)
    ok = r == cid + (" PASS" if want else " FAIL")
    bad += 0 if ok else 1
    print("%s %-12s %-26s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root = build()
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IBHM2-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)

CASES = [
    ("a_test_name_missing", "AC1", dict(names=P.NAMES[1:])),
    ("a_named_test_fails", "AC1", dict(fail_one=True)),
    ("no_test_file", "AC1", dict(drop_tests=True)),
    ("stage_before_land", "AC2", dict(runner=RUNNER_OK.replace("    landed = land()\n    try:\n        emit_hmac_list()\n    except Exception:\n        pass\n", "    try:\n        emit_hmac_list()\n    except Exception:\n        pass\n    landed = land()\n"))),
    ("stage_not_in_try", "AC2", dict(runner=RUNNER_OK.replace("    try:\n        emit_hmac_list()\n    except Exception:\n        pass\n", "    emit_hmac_list()\n"))),
    ("handler_too_narrow", "AC2", dict(runner=RUNNER_OK.replace("except Exception:", "except ValueError:"))),
    ("no_return", "AC2", dict(runner=RUNNER_OK.replace("    return {\"landed\": landed}\n", "    pass\n"))),
    ("runner_not_in_commit", "AC3", dict(drop_runner=True)),
    ("tests_not_in_commit", "AC3", dict(drop_tests=True)),
    ("other_file_touched", "AC3", dict(extra=["lib/other_file.py"])),
]
for label, ac, kw in CASES:
    root = build(**kw)
    expect(label, "IBHM2-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c248_"))
git(root, "init", "-q")
for ac in ("AC1", "AC2", "AC3"):
    expect("empty_repo", "IBHM2-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
