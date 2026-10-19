"""Positive control and negatives for p256_cells.py (run by the issuer at the cut). Usage: python control256.py <real_repo_root>

Synthetic git repositories: a base commit holding the REAL refresh.py and expiry.py, then ONE worker commit, so the pytest, differential and git-diff arms can each be made to fail.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r256/p256_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p256_cells as P  # noqa: E402

REAL_DIR = REAL / P.DIRP
REFRESH = (REAL_DIR / "refresh.py").read_text(encoding="utf-8")
EXPIRY = (REAL_DIR / "expiry.py").read_text(encoding="utf-8")
HARMLESS = REFRESH + "\n\ndef _failed_command_record_marker():\n    return None\n"
SUCCESS_TRAIL_CHANGED = REFRESH.replace('self.trail.append("dispatched %s for %s as-of %s" % (cid, firm_id, business_date))',
                                        'self.trail.append("sent %s for %s as-of %s" % (cid, firm_id, business_date))')
IN_FLIGHT_NARROWED = REFRESH.replace('COMMAND_IN_FLIGHT = ("Pending", "InProgress", "Delayed")', 'COMMAND_IN_FLIGHT = ("Pending", "Delayed")')
assert SUCCESS_TRAIL_CHANGED != REFRESH and IN_FLIGHT_NARROWED != REFRESH


def tests_src(names, fail_one=False):
    out = ""
    for i, n in enumerate(names):
        out += "def %s():\n    assert %s\n\n\n" % (n, "False" if (fail_one and i == 0) else "True")
    return out


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def build(runner=HARMLESS, names=P.NAMES, fail_one=False, extra=None, drop_runner=False, drop_tests=False):
    root = Path(tempfile.mkdtemp(prefix="c256_"))
    d = root / P.DIRP
    d.mkdir(parents=True)
    (d / "refresh.py").write_text(REFRESH, encoding="utf-8")
    (d / "expiry.py").write_text(EXPIRY, encoding="utf-8")
    shutil.copytree(REAL / "lib", root / "lib", ignore=shutil.ignore_patterns("__pycache__"))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")
    if not drop_runner:
        (root / P.RUNNER).write_text(runner, encoding="utf-8")
    if not drop_tests:
        t = root / P.TESTS
        t.parent.mkdir(parents=True, exist_ok=True)
        t.write_text(tests_src(names, fail_one), encoding="utf-8")
    n = root / (P.DELIV + "IBcw2_note.txt")
    n.parent.mkdir(parents=True, exist_ok=True)
    n.write_text("n\n", encoding="utf-8")
    for e in extra or []:
        (root / e).parent.mkdir(parents=True, exist_ok=True)
        (root / e).write_text("x\n", encoding="utf-8")
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
    print("%s %-12s %-30s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root = build()
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IBCW2-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)

CASES = [
    ("a_test_name_missing", "AC1", dict(names=P.NAMES[1:])),
    ("a_named_test_fails", "AC1", dict(fail_one=True)),
    ("no_test_file", "AC1", dict(drop_tests=True)),
    ("success_path_trail_changed", "AC2", dict(runner=SUCCESS_TRAIL_CHANGED)),
    ("in_flight_no_longer_blocks", "AC2", dict(runner=IN_FLIGHT_NARROWED)),
    ("refresh_py_unchanged", "AC2", dict(runner=REFRESH)),
    ("runner_not_in_commit", "AC3", dict(drop_runner=True)),
    ("tests_not_in_commit", "AC3", dict(drop_tests=True)),
    ("other_file_touched", "AC3", dict(extra=["lib/other_file.py"])),
]
for label, ac, kw in CASES:
    root = build(**kw)
    expect(label, "IBCW2-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c256_"))
git(root, "init", "-q")
for ac in ("AC1", "AC2", "AC3"):
    expect("empty_repo", "IBCW2-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
