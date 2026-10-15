"""IRPT_BCKEND workstream ~PL round 3 (issuer 2.0.0_SA_COO~P2) -- the checks of two BUILD cells.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
It reuses the round-196/200/201/207 helpers (committed beside r235).

  IB235-1  IB-pr-604  (RE-CUT 2026-10-15 ~21:1xZ, CTO ADDENDUM 1 @9fef489152, msg 8644) the absent_at_source exemption names `smartx_map_present` as the
           evidence of an exempted account the candidate day's SmartX map shows; the two-consecutive-day threshold and the 95 percent floor unchanged
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
TO1 = "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-604.account-join-49f.md"
CELLS = {
    "1": dict(
        slot=441, test=F + "tests/test_absent_at_source_smartx_evidence.py", min_tests=8, marker="ABSENT-AT-SOURCE-D", rec="IB235-1_record.json",
        regress=[F + "tests/test_holdings_publish_gate.py", F + "tests/test_absent_at_source_exemption.py", F + "tests/test_absent_at_source_wiring.py",
                 F + "tests/test_absent_at_source_receipts.py", F + "tests/test_holdings_bypass_one_date.py"],
        mutants=[F + "holdings_snapshot.py"],
        allowed=(F + "holdings_snapshot.py", F + "tests/test_absent_at_source_smartx_evidence.py", F + "tests/test_absent_at_source_exemption.py",
                 F + "tests/test_absent_at_source_wiring.py", F + "tests/test_absent_at_source_receipts.py", TO1),
        required=(F + "holdings_snapshot.py", F + "tests/test_absent_at_source_smartx_evidence.py"), any_of=(F + "holdings_snapshot.py",),
        named=("smartx_present_account_absent_two_days_is_exempt_with_evidence", "account_absent_one_day_is_not_exempt_even_with_a_smartx_row",
               "account_with_positions_on_either_day_is_not_exempt_with_a_smartx_row", "account_not_in_smartx_is_exempt_without_an_evidence_key",
               "a_failed_or_empty_smartx_read_changes_no_decision_and_adds_no_evidence", "a_firm_with_no_smartx_reader_has_a_byte_unchanged_manifest",
               "the_evidence_id_form_matches_the_custody_id_form", "the_floor_and_the_two_day_threshold_are_unchanged")),
}


def rec_path(c):
    return P6.D + "0.9.0_WK_IRPT_BCKEND~%d/%s" % (c["slot"], c["rec"])


P7.rec_path = rec_path
CHECKS = {
    "IB235-1-AC1": lambda: P1.tests_pass(CELLS["1"]), "IB235-1-AC2": lambda: P0.build_ac2(CELLS["1"]), "IB235-1-AC3": lambda: P7.ac3(CELLS["1"]),
}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p235_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
