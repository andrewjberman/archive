"""IRPT_BCKEND workstream ~PS round 5 (issuer 2.0.0_SA_COO~P2) -- the checks of two BUILD cells (CTO round-5 analysis @25f361860e, msg 8183).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
It reuses the round-196/200/201 helpers (committed beside r207).

  IB207-1  IB-pr-566  W407-S1: freeze_filled_report gets its production caller -- the export submit path (PATH C) calls it through the injected ports["filled_reader"], tested THROUGH THE REAL HANDLER
    AC1  the new tests and the existing filled-report and export tests pass
    AC2  the difference control: with every FILLED-REPORT-F block removed in memory the new tests FAIL on assertions
    AC3  the record: the diff bounded to the grant; the named tests present; no typed object address; counters
  IB207-2  IB-pr-567  W407-S2: the export render installs the filled reader -- the filled-source branch reads the pinned object through the shared named-account reader; one pinned filled report rendered from a fixture
    AC1  the new tests and the existing filled-report and export tests pass
    AC2  the difference control: with every FILLED-REPORT-G block removed in memory the new tests FAIL on assertions
    AC3  the record: the diff bounded to the grant; the named tests present; no typed object address; counters
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for sub in ("r196", "r200", "r201"):
    sys.path.insert(0, str(HERE.parent / sub))
import p196_cells as P6  # noqa: E402
import p200_cells as P0  # noqa: E402
import p201_cells as P1  # noqa: E402

D = P6.D
LAM = P0.LAMBDA
fail, load, is_int, counters, no_long_digits = P6.fail, P6.load, P6.is_int, P6.counters, P6.no_long_digits
X = LAM + "export/"
REGRESS = [X + "tests/test_filled_report_server_pin.py", X + "tests/test_filled_report_source.py", X + "tests/test_filled_report_freeze_scope.py",
           X + "tests/test_export_bundle_filled_report_contract.py"]

CELLS = {
    "1": dict(
        slot=410, test=X + "tests/test_filled_report_submit_handler.py", min_tests=6, marker="FILLED-REPORT-F", rec="IB207-1_record.json", regress=REGRESS,
        mutants=[X + "submit_async.py", X + "submit_service.py", X + "retained_export.py"],
        allowed=(X + "submit_async.py", X + "submit_service.py", X + "retained_export.py", X + "entry.py", X + "handler.py", X + "bundle.py",
                 X + "tests/test_filled_report_submit_handler.py", X + "tests/test_filled_report_server_pin.py", X + "tests/test_filled_report_source.py",
                 X + "tests/test_filled_report_freeze_scope.py", X + "tests/test_export_bundle_filled_report_contract.py"),
        required=(X + "tests/test_filled_report_submit_handler.py",), any_of=(X + "submit_async.py", X + "submit_service.py"),
        named=("submit_filled_report_through_handler_queues", "forged_pin_ignored_through_handler", "uncovered_account_refused_through_handler",
               "no_filled_reader_refused_unavailable")),
    "2": dict(
        slot=411, test=X + "tests/test_filled_report_installed_reader_render.py", min_tests=5, marker="FILLED-REPORT-G", rec="IB207-2_record.json", regress=REGRESS,
        mutants=[X + "entry.py", X + "filled_reader_installed.py", X + "render.py", X + "download.py", X + "dispatch.py"],
        allowed=(X + "entry.py", X + "filled_reader_installed.py", X + "render.py", X + "download.py", X + "dispatch.py", X + "package.py", X + "handler.py",
                 X + "tests/test_filled_report_installed_reader_render.py", "infra/logic/registry/"),
        required=(X + "tests/test_filled_report_installed_reader_render.py", X + "filled_reader_installed.py"), any_of=(X + "entry.py", X + "handler.py"),
        named=("installed_reader_reads_pinned_version", "render_pinned_filled_report_from_fixture", "installed_reader_never_reads_current_object_for_a_pin")),
}


def rec_path(c):
    return D + "0.9.0_WK_IRPT_BCKEND~%d/%s" % (c["slot"], c["rec"])


def in_grant(path, allowed):
    return any(path == a or (a.endswith("/") and path.startswith(a)) for a in allowed)


def ac3(c):
    r = load(rec_path(c))
    base = r.get("base_commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", base):
        fail("base_commit must be 40 hex")
    changed = P0.own_changes(c, base)
    if sorted(r.get("changed_paths", [])) != changed:
        fail("changed_paths differs from the worker's own commits since base")
    stray = [x for x in changed if not in_grant(x, c["allowed"])]
    if stray:
        fail("paths outside the grant: %r" % stray[:4])
    miss = sorted(set(c["required"]) - set(changed))
    if miss:
        fail("these files must change: %r" % miss[:4])
    if not set(c["any_of"]) & set(changed):
        fail("one of %r must change" % (c["any_of"],))
    txt = (P6.ROOT / c["test"]).read_text(encoding="utf-8")
    neg = r.get("negative_tests")
    if not isinstance(neg, list) or not set(c["named"]) <= set(neg):
        fail("negative_tests must list %r" % (c["named"],))
    for n in c["named"]:
        if not re.search(r"def test_\w*%s\w*\(" % n, txt):
            fail("the new test file has no test named for %s" % n)
    add, _ = P0.added_removed(base, [x for x in changed if x.endswith(".py") and "/tests/" not in x])
    if any(re.search(r"s3://|opal-data-", x) for x in add):
        fail("a typed object address in a product file (an address is lib/opal_naming.address() output; a missing registry row is a row to add)")
    if not is_int(r.get("tests_total")) or r.get("tests_passed") != r.get("tests_total") or not is_int(r.get("mutant_tests_failed")) or r["mutant_tests_failed"] < 1:
        fail("tests_total equal to tests_passed and mutant_tests_failed >= 1 must be recorded")
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: the diff bounded, the named tests present, no typed address")


CHECKS = {
    "IB207-1-AC1": lambda: P1.tests_pass(CELLS["1"]), "IB207-1-AC2": lambda: P0.build_ac2(CELLS["1"]), "IB207-1-AC3": lambda: ac3(CELLS["1"]),
    "IB207-2-AC1": lambda: P1.tests_pass(CELLS["2"]), "IB207-2-AC2": lambda: P0.build_ac2(CELLS["2"]), "IB207-2-AC3": lambda: ac3(CELLS["2"]),
}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p207_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
