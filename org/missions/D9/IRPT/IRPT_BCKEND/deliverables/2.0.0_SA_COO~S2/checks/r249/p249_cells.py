"""IRPT_BCKEND workstream ~PS round 9 (issuer 2.0.0_SA_COO~S2) -- the check of one BUILD order: four stale comments and a docstring in retained_export.py that still
describe the pinned-VersionId filled-report read are made true (comments and docstrings only; no code token changes).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. <repo_root> is the worker's worktree.

  IB249-1  IB-pr-619  the four stale statements are replaced by true ones, in comments and one docstring only
    AC1  the bound: the three export filled-report test files still pass (31 passed)
    AC2  the seam: the module's syntax tree with docstrings removed equals the one at the build commit 302d7fc367 (no code token changed), and no other source file differs from it
    AC3  the build: the four stale statements are gone and each site now says the CURRENT object is re-read and refused on a sha256 or size mismatch
"""
import ast
import subprocess
import sys
from pathlib import Path

EXPORT = "infra/aws/lambda/investor-reporting/export"
TARGET = EXPORT + "/retained_export.py"
TESTS = [EXPORT + "/tests/test_filled_report_server_pin.py", EXPORT + "/tests/test_filled_report_freeze_scope.py", EXPORT + "/tests/test_filled_report_source.py"]
BUILD = "302d7fc367da57bf4c1563934e79e65f3163860c"
STALE = (
    "The freeze reads that VersionId through the injected reader",
    "The pinned read that follows reads back exactly that VersionId",
    "reads back exactly the pinned VersionId and never the current object",
    "The current object is never consulted",
)
ROOT = Path(".")
CID = ""


def fail(msg):
    print("%s FAIL: %s" % (CID, msg))
    sys.exit(1)


def sh(args, cwd=None, timeout=110):
    return subprocess.run(args, cwd=str(cwd or ROOT), capture_output=True, text=True, timeout=timeout)


def stripped_dump(src):
    tree = ast.parse(src)
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if isinstance(body, list) and body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
                and isinstance(body[0].value.value, str):
            node.body = body[1:] or [ast.Pass()]
    return ast.dump(tree)


def ac1(_):
    p = sh([sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", *[str(Path("tests") / Path(t).name) for t in TESTS]], cwd=ROOT / EXPORT, timeout=115)
    out = p.stdout + p.stderr
    if p.returncode != 0 or "31 passed" not in out:
        fail("the three export filled-report test files must pass with 31 passed (rc %d): %s" % (p.returncode, out[-300:].replace("\n", " | ")))
    print("OK: the three test files pass, 31 passed")


def ac2(_):
    built = sh(["git", "show", "%s:%s" % (BUILD, TARGET)])
    if built.returncode != 0:
        fail("cannot read %s at the build commit %s" % (TARGET, BUILD[:10]))
    now = (ROOT / TARGET).read_text(encoding="utf-8")
    if stripped_dump(now) != stripped_dump(built.stdout):
        fail("retained_export.py differs from the build commit in code (docstrings and comments are the only allowed change)")
    changed = [f for f in sh(["git", "diff", "--name-only", BUILD]).stdout.split() if f.startswith(("infra/", "lib/", ".tools/", "data/"))]
    others = [f for f in changed if f != TARGET]
    if others:
        fail("only %s may differ from the build commit among source files; also differing: %s" % (TARGET, others[:5]))
    print("OK: the code (docstrings removed) equals the build commit; only retained_export.py differs")


def ac3(_):
    src = (ROOT / TARGET).read_text(encoding="utf-8")
    still = [s for s in STALE if s in src]
    if still:
        fail("stale statements remain: %s" % still)
    lines = src.splitlines()
    sites = ("PATH C -- THE FILLED_REPORT SOURCE KIND", "IB-pr-563 (CTO ruling on call f50a)", "PATH C through the export submit", "def filled_leg_read")
    for site in sites:
        idx = next((i for i, ln in enumerate(lines) if site in ln), None)
        if idx is None:
            fail("site not found: %s" % site)
        window = " ".join(lines[idx: idx + 9])
        if "CURRENT object" not in window and "current object" not in window:
            fail("the comment at %r must say the CURRENT object is re-read" % site)
        if "sha256" not in window:
            fail("the comment at %r must say the read is refused on a sha256 or size mismatch" % site)
    print("OK: the four stale statements are gone and each site says the current object is re-read and refused on a mismatch")


CHECKS = {"IB249-1-AC1": ac1, "IB249-1-AC2": ac2, "IB249-1-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p249_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    ROOT, CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](None)
    print("%s PASS" % sys.argv[2])
