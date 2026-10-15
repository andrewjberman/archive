"""IRPT_BCKEND workstream ~PS round 3 (issuer 2.0.0_SA_COO~P2) -- the checks of the two export cells (CTO round-3 analysis @a4718eab10).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
It reuses the round-200 helpers (checks/r200/p200_cells.py, committed beside r201).

  IB201-1  IB-pr-557  the packaged ExportBundle contract gains the `filled_report` source kind (docs copy and packaged copy byte-equal; a minor revision step)
    AC1  the new tests (both arms: a new bundle with filled_report validates; an existing bundle validates unchanged) and the existing contract tests pass
    AC2  the difference control: with the BASE schema bytes served in memory for both copies the new tests FAIL on assertions
    AC3  the record: the diff bounded to the two schema copies and the new test; byte-equal copies; revision 1.N to 1.N+1; filled_report in the schema; counters
  IB201-2  IB-pr-558  the export freeze scopes on the route's ONE named-account reader (a shared module), with its negative test
    AC1  the new tests and the existing route, entry and export tests pass
    AC2  the difference control: with every FILLED-REPORT-D block removed in memory the new tests FAIL on assertions
    AC3  the record: the diff bounded; the reader defined exactly once in the shared module and imported by entry.py and by the export freeze; the inline copy gone; the negative test by name; counters
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
sys.path.insert(0, str(HERE.parent / "r200"))
import p196_cells as P6  # noqa: E402
import p200_cells as P0  # noqa: E402

D = P6.D
LAMBDA = P0.LAMBDA
DOCS_SCHEMA = "docs/contracts/investor-reporting/v1/ExportBundle.schema.json"
PKG_SCHEMA = LAMBDA + "_contracts/ExportBundle.schema.json"
SHARED = LAMBDA + "_scope/filled_named_accounts.py"
fail, load, is_int, counters, no_long_digits = P6.fail, P6.load, P6.is_int, P6.counters, P6.no_long_digits

CELLS = {
    "1": dict(
        slot=401, test=LAMBDA + "export/tests/test_export_bundle_filled_report_contract.py", min_tests=6,
        regress=[LAMBDA + "export/tests/test_packaged_contracts_match_docs.py", LAMBDA + "export/tests/test_export.py"],
        allowed={DOCS_SCHEMA, PKG_SCHEMA, LAMBDA + "export/tests/test_export_bundle_filled_report_contract.py"},
        required={DOCS_SCHEMA, PKG_SCHEMA, LAMBDA + "export/tests/test_export_bundle_filled_report_contract.py"}, rec="IB201-1_record.json"),
    "2": dict(
        slot=402, test=LAMBDA + "export/tests/test_filled_report_freeze_scope.py", min_tests=6, marker="FILLED-REPORT-D",
        regress=[LAMBDA + "export/tests/test_filled_report_source.py", LAMBDA + "export/tests/test_retained_export.py",
                 LAMBDA + "reporting/tests/test_reporting_filled_report.py", LAMBDA + "reporting/tests/test_reporting_entry.py"],
        mutants=[SHARED, LAMBDA + "export/retained_export.py"],
        allowed={SHARED, LAMBDA + "reporting/entry.py", LAMBDA + "export/retained_export.py", LAMBDA + "export/bundle.py",
                 LAMBDA + "export/tests/test_filled_report_freeze_scope.py", LAMBDA + "export/tests/test_filled_report_source.py",
                 LAMBDA + "reporting/tests/test_reporting_filled_report.py"},
        required={SHARED, LAMBDA + "reporting/entry.py", LAMBDA + "export/retained_export.py", LAMBDA + "export/tests/test_filled_report_freeze_scope.py"},
        rec="IB201-2_record.json"),
}


def rec_path(c):
    return D + "0.9.0_WK_IRPT_BCKEND~%d/%s" % (c["slot"], c["rec"])


def tests_pass(c):
    for rel in [c["test"], *c["regress"]]:
        if not (P6.ROOT / rel).is_file():
            fail("no %s" % rel)
    rc, out = P0.run_pytest([c["test"], *c["regress"]])
    m = re.search(r"(\d+) passed", out)
    if rc != 0 or not m:
        fail("the tests do not all pass:\n" + out[-600:])
    if (P6.ROOT / c["test"]).read_text(encoding="utf-8").count("def test_") < c["min_tests"]:
        fail("the new test file must hold at least %d tests" % c["min_tests"])
    print("OK: %s passed" % m.group(1))


# the in-memory file substitution for DATA files (the contract is JSON, read with open or Path.read_text)
DATA_RUNNER = (
    "import builtins, io, json, os, pathlib, sys, pytest\n"
    "targets = json.loads(open(sys.argv[1], encoding='utf-8').read())\n"
    "targets = {os.path.normcase(os.path.abspath(k)): v for k, v in targets.items()}\n"
    "orig_open = builtins.open\n"
    "def _hit(f):\n"
    "    try:\n"
    "        return os.path.normcase(os.path.abspath(os.fspath(f))) in targets\n"
    "    except TypeError:\n"
    "        return False\n"
    "def fake_open(f, mode='r', *a, **k):\n"
    "    if _hit(f) and not any(c in mode for c in 'wax+'):\n"
    "        text = targets[os.path.normcase(os.path.abspath(os.fspath(f)))]\n"
    "        return io.BytesIO(text.encode('utf-8')) if 'b' in mode else io.StringIO(text)\n"
    "    return orig_open(f, mode, *a, **k)\n"
    "builtins.open = fake_open\n"
    "io.open = fake_open\n"
    "orig_rt, orig_rb = pathlib.Path.read_text, pathlib.Path.read_bytes\n"
    "def read_text(self, *a, **k):\n"
    "    return targets[os.path.normcase(os.path.abspath(str(self)))] if _hit(self) else orig_rt(self, *a, **k)\n"
    "def read_bytes(self):\n"
    "    return targets[os.path.normcase(os.path.abspath(str(self)))].encode('utf-8') if _hit(self) else orig_rb(self)\n"
    "pathlib.Path.read_text, pathlib.Path.read_bytes = read_text, read_bytes\n"
    "sys.dont_write_bytecode = True\n"
    "sys.exit(pytest.main(['-q', '-p', 'no:cacheprovider', sys.argv[2]]))\n")


def contract_ac2(c):
    r = load(rec_path(c))
    base = r.get("base_commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", base):
        fail("base_commit must be 40 hex")
    targets = {}
    for rel in (DOCS_SCHEMA, PKG_SCHEMA):
        p = subprocess.run(["git", "-C", str(P6.ROOT), "show", "%s:%s" % (base, rel)], capture_output=True, timeout=60)
        if p.returncode != 0:
            fail("no %s at the base commit" % rel)
        targets[str((P6.ROOT / rel).resolve())] = p.stdout.decode("utf-8")
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / "targets.json").write_text(json.dumps(targets), encoding="utf-8")
        (Path(td) / "run_mutant.py").write_text(DATA_RUNNER, encoding="utf-8")
        rc, out = P0.run_pytest([str(Path(td) / "targets.json"), str((P6.ROOT / c["test"]).resolve())], {"PYTHONPYCACHEPREFIX": str(Path(td) / "pyc")},
                                runner=str(Path(td) / "run_mutant.py"))
    if rc == 0:
        fail("the new tests still pass with the BASE schema served: the tests cannot discriminate")
    if not re.search(r"\d+ failed", out) or re.search(r"\d+ error", out):
        fail("the base-schema run must fail on assertions, not on errors (rc %s):\n%s" % (rc, out[-500:]))
    print("OK: serving the base schema fails the new tests")


def lf(rel):
    return (P6.ROOT / rel).read_bytes().replace(b"\r\n", b"\n")


def contract_ac3(c):
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
    if lf(DOCS_SCHEMA) != lf(PKG_SCHEMA):
        fail("the docs copy and the packaged copy of the schema must be byte-equal")
    new = json.loads(lf(DOCS_SCHEMA).decode("utf-8"))
    old = json.loads(subprocess.run(["git", "-C", str(P6.ROOT), "show", "%s:%s" % (base, DOCS_SCHEMA)], capture_output=True, timeout=60).stdout.decode("utf-8"))
    a, b = str(old.get("x-contract-revision")), str(new.get("x-contract-revision"))
    ma, mb = re.fullmatch(r"(\d+)\.(\d+)", a), re.fullmatch(r"(\d+)\.(\d+)", b)
    if not ma or not mb or ma.group(1) != mb.group(1) or int(mb.group(2)) != int(ma.group(2)) + 1:
        fail("x-contract-revision must take one MINOR step (%s to %s)" % (a, b))
    if "filled_report" not in json.dumps(new) or "filled_report" in json.dumps(old):
        fail("the new schema names filled_report and the base schema did not")
    if not {"new_bundle_validates", "old_bundle_validates_unchanged"} <= set(r.get("arms_tested", [])):
        fail("arms_tested must name new_bundle_validates and old_bundle_validates_unchanged")
    if not is_int(r.get("tests_total")) or r.get("tests_passed") != r.get("tests_total") or not is_int(r.get("mutant_tests_failed")) or r["mutant_tests_failed"] < 1:
        fail("tests_total equal to tests_passed and mutant_tests_failed >= 1 must be recorded")
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: record, copies byte-equal, one minor step, both arms")


def freeze_ac2(c):
    for rel in c["mutants"]:
        if not (P6.ROOT / rel).is_file():
            fail("no %s" % rel)
    P0.build_ac2(c)


def freeze_ac3(c):
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
    root = P6.ROOT / LAMBDA
    defs = [str(p) for p in root.rglob("*.py") if "tests" not in p.parts and re.search(r"^def filled_named_accounts\(", p.read_text(encoding="utf-8", errors="replace"), re.M)]
    if len(defs) != 1 or Path(defs[0]).resolve() != (P6.ROOT / SHARED).resolve():
        fail("the reader `def filled_named_accounts(` must be defined exactly once, in %s (found %d)" % (SHARED, len(defs)))
    entry = (P6.ROOT / (LAMBDA + "reporting/entry.py")).read_text(encoding="utf-8")
    freeze = (P6.ROOT / (LAMBDA + "export/retained_export.py")).read_text(encoding="utf-8") + (P6.ROOT / (LAMBDA + "export/bundle.py")).read_text(encoding="utf-8")
    imp = re.compile(r"^\s*(import filled_named_accounts\b|from filled_named_accounts import)", re.M)
    if not imp.search(entry) or not imp.search(freeze):
        fail("entry.py and the export freeze (retained_export.py or bundle.py) must both import filled_named_accounts")
    if re.search(r"^def _filled_named_accounts\(|^def _by_row_keys\(", entry, re.M):
        fail("the inline copy of the reader in entry.py must be gone")
    neg = r.get("negative_tests")
    txt = (P6.ROOT / c["test"]).read_text(encoding="utf-8")
    if not isinstance(neg, list) or "export_freeze_refuses_uncovered_account" not in neg or not re.search(r"def test_\w*export_freeze_refuses_uncovered_account\w*\(", txt):
        fail("the negative test export_freeze_refuses_uncovered_account must be listed and present by name")
    if not is_int(r.get("tests_total")) or r.get("tests_passed") != r.get("tests_total") or not is_int(r.get("mutant_tests_failed")) or r["mutant_tests_failed"] < 1:
        fail("tests_total equal to tests_passed and mutant_tests_failed >= 1 must be recorded")
    add, _ = P0.added_removed(base, [x for x in changed if x.endswith(".py") and "/tests/" not in x])
    if any(re.search(r"s3://|opal-data-", x) for x in add):
        fail("a typed object address in a product file")
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: one shared reader, imported by the route and the freeze, the negative test")


CHECKS = {
    "IB201-1-AC1": lambda: tests_pass(CELLS["1"]), "IB201-1-AC2": lambda: contract_ac2(CELLS["1"]), "IB201-1-AC3": lambda: contract_ac3(CELLS["1"]),
    "IB201-2-AC1": lambda: tests_pass(CELLS["2"]), "IB201-2-AC2": lambda: freeze_ac2(CELLS["2"]), "IB201-2-AC3": lambda: freeze_ac3(CELLS["2"]),
}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p201_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
