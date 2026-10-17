"""IRPT_ANLREQ AR-g-159 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g159_checks.py build   the resident's entry module puts the package's lib directory on sys.path with the others (ycharts/generate/resident_main.py, the `for _relative in (...)` tuple), so any
                                     member that imports from lib (lib/trading_calendar.py, imported by intake/yfinance_check.py since AR-g-157) imports in the SERVICE: over a package-layout tree
                                     (intake/yfinance_check.py, lib/trading_calendar.py, ycharts/generate/resident_main.py copied from the repository), in a fresh `python -I` interpreter that sets sys.path from the tuple exactly
                                     as resident_main does, the shipped checker reads a history on a Saturday run as KEPT on Thursday's close. With `lib` taken out of the tuple the same run reads CHECK_FAILED
                                     (the control: the test detects the defect r34j's V2 found). The test file gained a test for the tuple and the layout run.
    python ar_g159_checks.py guard   nothing else moves: the tuple's other entries are unchanged and in order, and resident_main.py differs from its base only in that tuple line
    python ar_g159_checks.py regress each existing test file that loads resident_main on its own, then the scope check
    python ar_g159_checks.py scope   the branch changed only resident_main.py, its test file, the order and the worker's folder (against the merge-base with box/dell2)

Prints one RESULT line: AR-G159-OK / AR-G159-FAIL (or -REGRESS- / -SCOPE-); rc 0 only on OK. ASCII only.
"""
import ast
import os
import shutil
import subprocess
import sys
import tempfile

IR = "infra/aws/lambda/investor-reporting/"
MAIN = IR + "ycharts/generate/resident_main.py"
TEST = IR + "ycharts/generate/tests/test_resident_main.py"
CHECKER = IR + "intake/yfinance_check.py"
CALENDAR = "lib/trading_calendar.py"
OWN = (MAIN, TEST, "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-159.resident-main-lib-on-path.md")
OWN_PREFIX = ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~281/", "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/", "org/tier2_senior/0.7.0_AE_CloudOps~IB2/")
REGRESS_FILES = (TEST, IR + "ycharts/generate/tests/test_package_poll.py")
BASE_TUPLE = ["intake", "ops", "reports", "_keys", "_authz", "_gate", "ycharts/session", "ycharts/extract"]

SNIPPET = '''
import datetime
import sys
from pathlib import Path

root = Path(sys.argv[1])
for rel in %(rels)r:
    path = root / rel
    if path.is_dir():
        sys.path.insert(0, str(path))
import yfinance_check

history = lambda symbol: [("2026-10-14", 100.0), ("2026-10-15", 101.0), ("2026-10-16", 102.0)]
now = lambda: datetime.datetime(2026, 10, 17, 0, 50, tzinfo=datetime.timezone.utc)
out = yfinance_check.YfinanceChecker(history=history, sleep=lambda s: None, now=now).check(["SPY"])["SPY"]
print("%%s %%s %%s" %% (out["state"], out["last_close"], out["reason"]))
'''


def tuple_of(text):
    for node in ast.walk(ast.parse(text)):
        if isinstance(node, ast.For) and getattr(node.target, "id", "") == "_relative" and isinstance(node.iter, (ast.Tuple, ast.List)):
            return [e.value for e in node.iter.elts], node
    return None, None


def layout_run(rels):
    """Copy the three files into a package-layout tree and run the checker in a fresh -I interpreter whose sys.path is set from `rels`."""
    tmp = tempfile.mkdtemp(prefix="ar_g159_")
    try:
        for rel, src in (("intake/yfinance_check.py", CHECKER), ("lib/trading_calendar.py", CALENDAR), ("ycharts/generate/resident_main.py", MAIN)):
            os.makedirs(os.path.dirname(os.path.join(tmp, rel)), exist_ok=True)
            shutil.copy(src, os.path.join(tmp, rel))
        code = SNIPPET % {"rels": rels}
        out = subprocess.run([sys.executable, "-I", "-c", code, tmp], capture_output=True, text=True)
        lines = [ln for ln in out.stdout.splitlines() if ln.strip()]
        return (lines[-1] if lines else "") + ("" if out.returncode == 0 else " rc=%d %s" % (out.returncode, out.stderr.strip()[-120:]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def arms_build():
    fails = []
    rels, _ = tuple_of(open(MAIN, encoding="utf-8").read())
    if rels is None:
        return ["the path tuple in %s was not found" % MAIN]
    if "lib" not in rels:
        fails.append("lib is not in the resident_main path tuple: %r" % (rels,))
    got = layout_run(rels)
    if not got.startswith("KEPT 101.0 HISTORY_ROWS"):
        fails.append("the shipped checker over a package-layout tree with resident_main's own path list: %r" % (got,))
    control = layout_run([r for r in rels if r != "lib"])
    if not control.startswith("CHECK_FAILED"):
        fails.append("the control (lib taken out) did not read CHECK_FAILED: %r" % (control,))
    text = open(TEST, encoding="utf-8").read()
    if "lib" not in text or "-I" not in text or "trading_calendar" not in text:
        fails.append("%s does not hold the tuple and layout tests (no lib, -I or trading_calendar in it)" % TEST)
    return fails


def arms_guard():
    fails = []
    rels, node = tuple_of(open(MAIN, encoding="utf-8").read())
    if rels is None:
        return ["the path tuple was not found"]
    if [r for r in rels if r != "lib"] != BASE_TUPLE:
        fails.append("the other entries of the tuple moved: %r" % (rels,))
    base = subprocess.run(["git", "merge-base", "HEAD", "box/dell2"], capture_output=True, text=True).stdout.strip()
    if base:
        old = subprocess.run(["git", "show", "%s:%s" % (base, MAIN)], capture_output=True, text=True).stdout
        new = open(MAIN, encoding="utf-8").read()
        strip = lambda t: "\n".join(ln for ln in t.splitlines() if not ln.startswith("for _relative in"))  # noqa: E731
        if old and strip(old) != strip(new):
            fails.append("resident_main.py differs from its base beyond the tuple line")
    return fails


def scope():
    rc = subprocess.run(["git", "merge-base", "HEAD", "box/dell2"], capture_output=True)
    base = rc.stdout.decode().strip()
    if rc.returncode != 0 or not base:
        return ["no merge-base with box/dell2"]
    diff = subprocess.run(["git", "diff", "--name-only", base, "HEAD"], capture_output=True)
    if diff.returncode != 0:
        return ["git diff rc=%d" % diff.returncode]
    names = [n for n in diff.stdout.decode().splitlines() if n.strip()]
    stray = [n for n in names if n not in OWN and not n.startswith(OWN_PREFIX + ISSUER)]
    return ["outside the cell's write set: %s" % ", ".join(stray)] if stray else []


def regress():
    fails = []
    for path in REGRESS_FILES:
        out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", path], capture_output=True, text=True)
        if out.returncode != 0:
            fails.append("%s: rc=%d %s" % (path.rsplit("/", 1)[-1], out.returncode, (out.stdout or out.stderr).strip().splitlines()[-1:] or ""))
    return fails + scope()


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode in ("scope", "regress"):
        fails = scope() if mode == "scope" else regress()
        print("AR-G159-%s-%s %s" % (mode.upper(), "FAIL" if fails else "OK", "; ".join(fails)))
        return 1 if fails else 0
    if mode not in ("build", "guard"):
        print("AR-G159-FAIL usage: build | guard | scope | regress")
        return 2
    fails = arms_build() if mode == "build" else arms_guard()
    print("AR-G159-%s %s: %s" % ("FAIL" if fails else "OK", mode, "; ".join(fails) if fails else "all arms"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
