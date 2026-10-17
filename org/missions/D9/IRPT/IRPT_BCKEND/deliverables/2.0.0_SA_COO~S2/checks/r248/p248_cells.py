"""IRPT_BCKEND workstream ~PS round 8 (issuer 2.0.0_SA_COO~S2) -- the check of one BUILD order: the export reads the CURRENT filled-report object and refuses on a sha256 or size mismatch
(IB-pr-551 ADDENDUM 3; XA-20261017T010553Z-d493 RULED (B)).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. <repo_root> is the worker's worktree (it shares the git objects).

  IB248-1  IB-pr-617  retained_export.read_pinned_filled reads the current object (no VersionId), refuses on a changed object with a worded state; the tests move with it
    AC1  the built behaviour: the three export filled-report test files pass, the planted-changed-object test and the overwritten-object-refusal test are among the passed tests
    AC2  the seam: read_pinned_filled passes no version_id to the reader and keeps the sha256 and size refusal, its refusal is worded (changed, resubmit), and filled_reader_installed.py is byte-equal to the base
    AC3  the difference control: the same new tests run against the BASE retained_export.py FAIL (at least the two behaviour tests), so the tests discriminate
"""
import ast
import os
import subprocess
import sys
from pathlib import Path

EXPORT = "infra/aws/lambda/investor-reporting/export"
TARGET = EXPORT + "/retained_export.py"
UNTOUCHED = EXPORT + "/filled_reader_installed.py"
TESTS = [EXPORT + "/tests/test_filled_report_server_pin.py", EXPORT + "/tests/test_filled_report_freeze_scope.py", EXPORT + "/tests/test_filled_report_source.py"]
NEW_TESTS = ("test_changed_object_is_refused_with_a_worded_state", "test_overwritten_object_is_refused_at_render")
BASE = os.environ.get("P248_BASE", "bba05481507ac91952de027f7b71020cd3dfde0d")
ROOT = Path(".")
GIT_ROOT = None  # the tree whose git objects hold BASE; default the repo root given
CID = ""


def fail(msg):
    print("%s FAIL: %s" % (CID, msg))
    sys.exit(1)


def sh(args, cwd=None, timeout=110):
    return subprocess.run(args, cwd=str(cwd or ROOT), capture_output=True, text=True, timeout=timeout)


def show(commit, rel):
    p = sh(["git", "show", "%s:%s" % (commit, rel)], cwd=GIT_ROOT or ROOT)
    if p.returncode != 0:
        fail("git show %s:%s failed: %s" % (commit, rel, p.stderr.strip()[:200]))
    return p.stdout


def pytest(root, files, extra=()):
    return sh([sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rA", *extra, *files], cwd=Path(root) / EXPORT, timeout=115)


def ac1(_):
    for t in TESTS:
        if not (ROOT / t).is_file():
            fail("no test file %s" % t)
    rels = [Path(t).name for t in TESTS]
    p = pytest(ROOT, [str(Path("tests") / r) for r in rels])
    out = p.stdout + p.stderr
    if p.returncode != 0:
        fail("the export filled-report tests must all pass (rc %d): %s" % (p.returncode, out[-400:].replace("\n", " | ")))
    for name in NEW_TESTS:
        if "PASSED" not in "".join(ln for ln in out.splitlines() if name in ln):
            fail("the test %s must exist and pass" % name)
    print("OK: the three test files pass, including %s" % " and ".join(NEW_TESTS))


def _fn(src, name):
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    fail("no function %s in %s" % (name, TARGET))


def ac2(_):
    src = (ROOT / TARGET).read_text(encoding="utf-8")
    fn = _fn(src, "read_pinned_filled")
    for node in ast.walk(fn):
        if isinstance(node, ast.Call) and any(k.arg == "version_id" for k in node.keywords):
            fail("read_pinned_filled must not pass version_id to the reader (the current object is read; GetObjectVersion is not granted)")
    seg = ast.get_source_segment(src, fn) or ""
    if 'pin["sha256"]' not in seg or 'pin["size"]' not in seg or "hashlib.sha256" not in seg:
        fail("read_pinned_filled must keep the sha256 and size comparison against the pin")
    if "changed" not in seg or "resubmit" not in seg:
        fail("the refusal must be worded: it must say the report changed and the person must resubmit")
    if (ROOT / UNTOUCHED).read_bytes() != show(BASE, UNTOUCHED).encode("utf-8"):
        fail("%s must be byte-equal to the base %s (the reader already reads the current object when no version is named)" % (UNTOUCHED, BASE[:10]))
    print("OK: read_pinned_filled reads without a version, keeps the sha256 and size refusal, words it, and the installed reader is unchanged")


def ac3(_):
    """In the worker's own tree, put the BASE retained_export.py back in place of the built one, run the new tests, and restore the built bytes."""
    target = ROOT / TARGET
    built = target.read_bytes()
    try:
        target.write_text(show(BASE, TARGET), encoding="utf-8", newline="")
        p = pytest(ROOT, [str(Path("tests") / Path(t).name) for t in TESTS], extra=("-k", " or ".join(NEW_TESTS)))
        out = p.stdout + p.stderr
    finally:
        target.write_bytes(built)
    if p.returncode == 0:
        fail("the new tests must FAIL against the base retained_export.py; they passed (or none were selected), so they do not discriminate")
    failed = [n for n in NEW_TESTS if any(n in ln and "FAILED" in ln for ln in out.splitlines())]
    if len(failed) < 2:
        fail("both behaviour tests must fail against the base (failed: %s)" % failed)
    print("OK: against the base retained_export.py both %s fail; the built file is restored" % " and ".join(NEW_TESTS))


CHECKS = {"IB248-1-AC1": ac1, "IB248-1-AC2": ac2, "IB248-1-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p248_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    ROOT, CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    GIT_ROOT = Path(os.environ["P248_GIT_ROOT"]) if os.environ.get("P248_GIT_ROOT") else None
    CHECKS[sys.argv[2]](None)
    print("%s PASS" % sys.argv[2])
