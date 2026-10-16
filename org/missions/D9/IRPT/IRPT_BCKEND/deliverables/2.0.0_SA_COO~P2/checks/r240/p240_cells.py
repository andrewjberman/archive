"""IRPT_BCKEND workstream ~PL round 7 (issuer 2.0.0_SA_COO~P2) -- the check of one BUILD cell.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
It reuses the round-196/200/201/207 helpers (committed beside r240).

  IB240-1  IB-pr-609  (CTO half of the exemption ADDENDUM 1, revision note msg 8774) every exempted account carries exactly one of smartx_map_present, smartx_map_absent, unread (with a reason category); the decision unchanged
    AC1  the new tests and the existing publish-gate, exemption, wiring, receipts and bypass tests pass
    AC2  the difference control: with every ABSENT-AT-SOURCE-D block removed in memory the new tests FAIL on assertions
    AC3  the record: the diff bounded to the grant; the named tests present; no typed object address; counters
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for sub in ("r196", "r200", "r201", "r207"):
    sys.path.insert(0, str(HERE.parent / sub))
import p196_cells as P6  # noqa: E402
import p200_cells as P0  # noqa: E402
import p201_cells as P1  # noqa: E402
import p207_cells as P7  # noqa: E402

F = "data/assets/scripts/gold/investor_reporting/"
TO1 = "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-609.smartx-evidence-absent.md"
CELLS = {
    "1": dict(
        slot=445, test=F + "tests/test_absent_at_source_smartx_evidence.py", min_tests=12, marker="ABSENT-AT-SOURCE-D", rec="IB240-1_record.json",
        regress=[F + "tests/test_holdings_publish_gate.py", F + "tests/test_absent_at_source_exemption.py", F + "tests/test_absent_at_source_wiring.py",
                 F + "tests/test_absent_at_source_receipts.py", F + "tests/test_holdings_bypass_one_date.py"],
        mutants=[F + "holdings_snapshot.py"],
        allowed=(F + "holdings_snapshot.py", F + "tests/test_absent_at_source_smartx_evidence.py", F + "tests/test_absent_at_source_exemption.py",
                 F + "tests/test_absent_at_source_wiring.py", F + "tests/test_absent_at_source_receipts.py", TO1),
        required=(F + "holdings_snapshot.py", F + "tests/test_absent_at_source_smartx_evidence.py"), any_of=(F + "holdings_snapshot.py",),
        named=("smartx_present_account_absent_two_days_is_exempt_with_evidence", "account_absent_one_day_is_not_exempt_even_with_a_smartx_row",
               "account_with_positions_on_either_day_is_not_exempt_with_a_smartx_row", "an_account_the_obtained_map_does_not_show_gets_evidence_smartx_map_absent",
               "a_failed_smartx_read_gives_evidence_unread_with_a_reason_and_changes_no_decision", "a_missing_or_empty_map_gives_evidence_unread_with_a_reason",
               "the_unread_reason_is_a_category_with_no_identifier", "every_exempted_account_carries_exactly_one_of_the_three_evidence_values",
               "a_firm_with_no_smartx_reader_has_a_byte_unchanged_manifest", "the_evidence_id_form_matches_the_custody_id_form",
               "the_floor_and_the_two_day_threshold_are_unchanged")),
}


def rec_path(c):
    return P6.D + "0.9.0_WK_IRPT_BCKEND~%d/%s" % (c["slot"], c["rec"])


P7.rec_path = rec_path
NEW_TESTS = ("an_account_the_obtained_map_does_not_show_gets_evidence_smartx_map_absent", "every_exempted_account_carries_exactly_one_of_the_three_evidence_values")


def ac2():
    """The difference control grades the NEW behaviour: the two new tests must exist, and fail on assertions with the D spans removed."""
    c = CELLS["1"]
    fp = P6.ROOT / c["test"]
    txt = fp.read_text(encoding="utf-8") if fp.is_file() else ""
    for n in NEW_TESTS:
        if "def test_" + n not in txt:
            P6.fail("the new test file must define test_%s before the difference control means anything" % n)
    P0.build_ac2(c)


CHECKS = {
    "IB240-1-AC1": lambda: P1.tests_pass(CELLS["1"]), "IB240-1-AC2": ac2, "IB240-1-AC3": lambda: P7.ac3(CELLS["1"]),
}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p240_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
