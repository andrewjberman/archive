"""IRPT_BCKEND workstream ~PK round 1 (issuer 2.0.0_SA_COO~P2) -- the checks of two BUILD cells.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
It reuses the round-196/200/201/207 helpers (committed beside r219).

  IB219-1  IB-pr-582  the source receipts record the absent_at_source exemption's evidence reads (CTO msg 8359 item 4)
    AC1  the new tests and the existing publish-gate and wiring tests pass
    AC2  the difference control: with every ABSENT-AT-SOURCE-C block removed in memory the new tests FAIL on assertions
    AC3  the record: the diff bounded to the grant; the named tests present; no typed object address; counters
  IB219-2  IB-pr-583  a split row with no key makes the day SPLIT_RATIO_ABSENT and is counted, never skipped silently (CTO msg 8359 item 3)
    AC1  the new tests and the existing performance and split tests pass
    AC2  the difference control: with every SPLIT-ADJUST-B block removed in memory the new tests FAIL on assertions
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

G = "data/assets/scripts/gold/investor_reporting/"
H = "data/assets/scripts/gold/irpt_holdings_performance/"
TO1 = "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-582.receipts-evidence.md"
TO2 = "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-583.split-unkeyed.md"
CELLS = {
    "1": dict(
        slot=424, test=G + "tests/test_absent_at_source_receipts.py", min_tests=8, marker="ABSENT-AT-SOURCE-C", rec="IB219-1_record.json",
        regress=[G + "tests/test_holdings_publish_gate.py", G + "tests/test_absent_at_source_wiring.py"],
        mutants=[G + "holdings_snapshot.py"],
        allowed=(G + "holdings_snapshot.py", G + "tests/test_absent_at_source_receipts.py", G + "tests/test_absent_at_source_wiring.py", G + "tests/test_holdings_publish_gate.py", TO1),
        required=(G + "holdings_snapshot.py", G + "tests/test_absent_at_source_receipts.py"), any_of=(G + "holdings_snapshot.py",),
        named=("evidence_reads_are_recorded_in_the_source_objects", "source_set_revision_digest_covers_the_evidence_reads", "no_evidence_read_leaves_source_objects_unchanged",
               "recorded_evidence_keys_carry_the_pinned_version_ids", "refused_run_publishes_nothing_extra", "second_fire_records_its_own_evidence_reads")),
    "2": dict(
        slot=425, test=H + "tests/test_split_unkeyed.py", min_tests=9, marker="SPLIT-ADJUST-B", rec="IB219-2_record.json",
        regress=[H + "tests/test_split_adjust.py", H + "tests/test_holdings_performance.py", H + "tests/test_holdings_comparison.py"],
        mutants=[H + "holdings_performance.py"],
        allowed=(H + "holdings_performance.py", H + "tests/test_split_unkeyed.py", H + "tests/test_split_adjust.py", H + "tests/test_holdings_performance.py", TO2),
        required=(H + "holdings_performance.py", H + "tests/test_split_unkeyed.py"), any_of=(H + "holdings_performance.py",),
        named=("unkeyed_split_row_marks_the_day_ratio_absent_and_counts", "blank_cusip_falls_back_to_ticker", "no_key_at_all_never_skips_silently",
               "keyed_rows_unchanged_when_no_unkeyed_row", "manifest_counts_unkeyed_split_rows", "unkeyed_row_does_not_adjust_a_keyed_security")),
}


def rec_path(c):
    return P6.D + "0.9.0_WK_IRPT_BCKEND~%d/%s" % (c["slot"], c["rec"])


P7.rec_path = rec_path
CHECKS = {
    "IB219-1-AC1": lambda: P1.tests_pass(CELLS["1"]), "IB219-1-AC2": lambda: P0.build_ac2(CELLS["1"]), "IB219-1-AC3": lambda: P7.ac3(CELLS["1"]),
    "IB219-2-AC1": lambda: P1.tests_pass(CELLS["2"]), "IB219-2-AC2": lambda: P0.build_ac2(CELLS["2"]), "IB219-2-AC3": lambda: P7.ac3(CELLS["2"]),
}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p219_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
