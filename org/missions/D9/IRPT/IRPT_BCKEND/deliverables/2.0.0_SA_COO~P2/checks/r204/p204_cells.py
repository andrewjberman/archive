"""IRPT_BCKEND workstream ~PS round 4 (issuer 2.0.0_SA_COO~P2) -- the checks of two cells (CTO round-4 analysis @ac865e2d91, msg 8138).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
It reuses the round-196/200/201 helpers (committed beside r204).

  IB204-1  IB-pr-562  the lambda source map stages the shared reader `_scope/filled_named_accounts.py` into every function that packages an importing module, with a build-only import test per function
    AC1  the new test and the existing tests pass
    AC2  the difference control: with the BASE source-map bytes served in memory the new test FAILS on assertions
    AC3  the record: the diff bounded to the map and the new test; every importing function has the entry (pin and sha256 recomputed by the check); a PASS build-only import per function; counters
  IB204-2  IB-pr-563  the server pins the filled report at submit (CTO ruling on call f50a, msg 8104): freeze_filled_report reads the current object's VersionId, sha256 and size and the submit handler calls it
    AC1  the new tests and the existing export tests pass
    AC2  the difference control: with every FILLED-REPORT-E block removed in memory the new tests FAIL on assertions
    AC3  the record: the diff bounded; the two named tests present (an overwritten version still exports the pinned bytes; a forged client pin is ignored); counters
"""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
for sub in ("r196", "r200", "r201"):
    sys.path.insert(0, str(HERE.parent / sub))
import p196_cells as P6  # noqa: E402
import p200_cells as P0  # noqa: E402
import p201_cells as P1  # noqa: E402

D = P6.D
LAMBDA = P0.LAMBDA
MAP = "infra/aws/lambda/ci/lambda-source-map.json"
SHARED = LAMBDA + "_scope/filled_named_accounts.py"
IMPORTERS = ("reporting/entry.py", "export/retained_export.py", "export/bundle.py")
fail, load, is_int, counters, no_long_digits = P6.fail, P6.load, P6.is_int, P6.counters, P6.no_long_digits

CELLS = {
    "1": dict(
        slot=406, test="infra/aws/lambda/ci/tests/test_source_map_filled_named_accounts.py", min_tests=4, rec="IB204-1_record.json",
        regress=["infra/aws/lambda/ci/tests/test_source_map_filled_named_accounts.py"],
        allowed={MAP, "infra/aws/lambda/ci/tests/test_source_map_filled_named_accounts.py"},
        required={MAP, "infra/aws/lambda/ci/tests/test_source_map_filled_named_accounts.py"}),
    "2": dict(
        slot=407, test=LAMBDA + "export/tests/test_filled_report_server_pin.py", min_tests=6, marker="FILLED-REPORT-E", rec="IB204-2_record.json",
        regress=[LAMBDA + "export/tests/test_filled_report_source.py", LAMBDA + "export/tests/test_filled_report_freeze_scope.py", LAMBDA + "export/tests/test_retained_export.py"],
        mutants=[LAMBDA + "export/retained_export.py", LAMBDA + "export/entry.py"],
        allowed={LAMBDA + "export/retained_export.py", LAMBDA + "export/entry.py", LAMBDA + "export/handler.py", LAMBDA + "export/bundle.py",
                 LAMBDA + "export/tests/test_filled_report_server_pin.py", LAMBDA + "export/tests/test_filled_report_source.py",
                 LAMBDA + "export/tests/test_filled_report_freeze_scope.py"},
        required={LAMBDA + "export/retained_export.py", LAMBDA + "export/tests/test_filled_report_server_pin.py"}),
}


def rec_path(c):
    return D + "0.9.0_WK_IRPT_BCKEND~%d/%s" % (c["slot"], c["rec"])


def importing_functions():
    """The map's functions that package one of the modules importing the shared reader: a function whose source_dir is the
    module's package directory and whose files list names the module, or any entry that names the module's repository path."""
    m = json.loads((P6.ROOT / MAP).read_text(encoding="utf-8"))
    out = []
    for name, e in sorted(m.get("functions", {}).items()):
        blob = json.dumps(e)
        sd, files = str(e.get("source_dir", "")), e.get("files") or []
        by_dir = any(sd.endswith(LAMBDA + pkg.rsplit("/", 1)[0]) and pkg.rsplit("/", 1)[1] in files for pkg in IMPORTERS)
        if by_dir or any(x in blob for x in IMPORTERS):
            out.append(name)
    return out, m


# ----------------------------------------------------------------------------- IB204-1
def map_ac1(c):
    P1.tests_pass(c)


def map_ac2(c):
    r = load(rec_path(c))
    base = r.get("base_commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", base):
        fail("base_commit must be 40 hex")
    p = subprocess.run(["git", "-C", str(P6.ROOT), "show", "%s:%s" % (base, MAP)], capture_output=True, timeout=60)
    if p.returncode != 0:
        fail("no source map at the base commit")
    targets = {str((P6.ROOT / MAP).resolve()): p.stdout.decode("utf-8")}
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / "targets.json").write_text(json.dumps(targets), encoding="utf-8")
        (Path(td) / "run_mutant.py").write_text(P1.DATA_RUNNER, encoding="utf-8")
        rc, out = P0.run_pytest([str(Path(td) / "targets.json"), str((P6.ROOT / c["test"]).resolve())], {"PYTHONPYCACHEPREFIX": str(Path(td) / "pyc")},
                                runner=str(Path(td) / "run_mutant.py"))
    if rc == 0:
        fail("the new test still passes with the BASE source map served: it cannot discriminate")
    if not re.search(r"\d+ failed", out) or re.search(r"\d+ error", out):
        fail("the base-map run must fail on assertions, not on errors (rc %s):\n%s" % (rc, out[-500:]))
    print("OK: serving the base source map fails the new test")


def map_ac3(c):
    r = load(rec_path(c))
    base = r.get("base_commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", base):
        fail("base_commit must be 40 hex")
    changed = P0.own_changes(c, base)
    if sorted(r.get("changed_paths", [])) != changed:
        fail("changed_paths differs from the worker's own commits since base")
    stray = [x for x in changed if x not in c["allowed"]]
    if stray:
        fail("paths outside the grant: %r" % stray[:4])
    miss = sorted(c["required"] - set(changed))
    if miss:
        fail("these files must change: %r" % miss[:4])
    funcs, m = importing_functions()
    if not funcs:
        fail("no function in the map packages an importing module: the check cannot grade")
    shared_sha = None
    for name in funcs:
        entries = [x for x in (m["functions"][name].get("staged_from") or []) if x.get("repo_path") == SHARED]
        if len(entries) != 1:
            fail("function %s: exactly one staged_from entry for %s is required (found %d)" % (name, SHARED, len(entries)))
        e = entries[0]
        if e.get("packaged_as") != "filled_named_accounts.py" or not re.fullmatch(r"[0-9a-f]{40}", str(e.get("pin", ""))):
            fail("function %s: the entry needs packaged_as filled_named_accounts.py and a 40-hex pin" % name)
        shown = subprocess.run(["git", "-C", str(P6.ROOT), "show", "%s:%s" % (e["pin"], SHARED)], capture_output=True, timeout=60)
        if shown.returncode != 0:
            fail("function %s: the pin %s does not hold %s" % (name, e["pin"][:10], SHARED))
        shared_sha = hashlib.sha256(shown.stdout).hexdigest()
        if e.get("sha256") != shared_sha:
            fail("function %s: the entry's sha256 is not the file's sha256 at its pin" % name)
        if "filled_named_accounts.py" not in (m["functions"][name].get("files") or []):
            fail("function %s: its files list must name filled_named_accounts.py" % name)
    got = r.get("build_only_imports")
    if not isinstance(got, list) or sorted(x.get("function") for x in got) != funcs or any(x.get("result") != "PASS" for x in got):
        fail("build_only_imports must list every importing function %r with result PASS" % funcs)
    if not is_int(r.get("tests_total")) or r.get("tests_passed") != r.get("tests_total") or not is_int(r.get("mutant_tests_failed")) or r["mutant_tests_failed"] < 1:
        fail("tests_total equal to tests_passed and mutant_tests_failed >= 1 must be recorded")
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: %d importing function(s) staged with the shared reader, build-only imports PASS" % len(funcs))


# ----------------------------------------------------------------------------- IB204-2
def pin_ac3(c):
    r = load(rec_path(c))
    base = r.get("base_commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", base):
        fail("base_commit must be 40 hex")
    changed = P0.own_changes(c, base)
    if sorted(r.get("changed_paths", [])) != changed:
        fail("changed_paths differs from the worker's own commits since base")
    stray = [x for x in changed if x not in c["allowed"]]
    if stray:
        fail("paths outside the grant: %r" % stray[:4])
    miss = sorted(c["required"] - set(changed))
    if miss:
        fail("these files must change: %r" % miss[:4])
    if not ({LAMBDA + "export/entry.py", LAMBDA + "export/handler.py"} & set(changed)):
        fail("the submit handler (export/entry.py or export/handler.py) must call the server-side pin")
    txt = (P6.ROOT / c["test"]).read_text(encoding="utf-8")
    need = ("overwritten_version_still_exports_pinned_bytes", "forged_client_pin_ignored")
    neg = r.get("negative_tests")
    if not isinstance(neg, list) or not set(need) <= set(neg):
        fail("negative_tests must list %r" % (need,))
    for n in need:
        if not re.search(r"def test_\w*%s\w*\(" % n, txt):
            fail("the new test file has no test named for %s" % n)
    add, _ = P0.added_removed(base, [x for x in changed if x.endswith(".py") and "/tests/" not in x])
    if any(re.search(r"s3://|opal-data-", x) for x in add):
        fail("a typed object address in a product file")
    if not is_int(r.get("tests_total")) or r.get("tests_passed") != r.get("tests_total") or not is_int(r.get("mutant_tests_failed")) or r["mutant_tests_failed"] < 1:
        fail("tests_total equal to tests_passed and mutant_tests_failed >= 1 must be recorded")
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: the server-side pin, both named tests, the diff bounded")


CHECKS = {
    "IB204-1-AC1": lambda: map_ac1(CELLS["1"]), "IB204-1-AC2": lambda: map_ac2(CELLS["1"]), "IB204-1-AC3": lambda: map_ac3(CELLS["1"]),
    "IB204-2-AC1": lambda: P1.tests_pass(CELLS["2"]), "IB204-2-AC2": lambda: P0.build_ac2(CELLS["2"]), "IB204-2-AC3": lambda: pin_ac3(CELLS["2"]),
}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p204_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
