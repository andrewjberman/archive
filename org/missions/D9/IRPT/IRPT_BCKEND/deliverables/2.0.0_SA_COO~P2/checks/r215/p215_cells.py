"""IRPT_BCKEND workstream ~PG round 1 (issuer 2.0.0_SA_COO~P2) -- the check of one BUILD cell: the closed_at_source exemption of the account_lost condition (CTO msgs 8268 and 8284).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
It reuses the round-196/200/201/207 helpers (committed beside r215).

  IB215-1  IB-pr-576  the publish gate exempts an account_lost ONLY when the source shows the account with no positions (absent or zero) in BOTH the positions and balance tables on the candidate date AND the prior trading day, each of those partitions complete (account count at least 95 percent of the prior day's), and records each exempted account in the publication manifest as closed_at_source with its dates
    AC1  the new tests and the existing publish-gate tests pass
    AC2  the difference control: with every CLOSED-AT-SOURCE-A block removed in memory the new tests FAIL on assertions
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
CELLS = {
    "1": dict(
        slot=419, test=G + "tests/test_closed_at_source_exemption.py", min_tests=9, marker="CLOSED-AT-SOURCE-A", rec="IB215-1_record.json",
        regress=[G + "tests/test_holdings_publish_gate.py", G + "tests/test_holdings_bypass_one_date.py", G + "tests/test_directory_exemption_source_marks.py"],
        mutants=[G + "holdings_snapshot.py"],
        allowed=(G + "holdings_snapshot.py", G + "tests/test_closed_at_source_exemption.py", G + "tests/test_holdings_publish_gate.py",
                 G + "tests/test_holdings_bypass_one_date.py", G + "tests/test_directory_exemption_source_marks.py"),
        required=(G + "holdings_snapshot.py", G + "tests/test_closed_at_source_exemption.py"), any_of=(G + "holdings_snapshot.py",),
        named=("exempts_when_both_days_have_no_positions_and_both_partitions_are_complete", "one_zero_day_still_refuses", "truncated_partition_never_exempts",
               "present_in_either_table_refuses", "manifest_records_absent_at_source_with_dates_never_closed", "terminated_path_unchanged", "other_conditions_still_refuse",
               "served_snapshot_keeps_the_account_listed_with_the_not_reported_words")),
}


def rec_path(c):
    return P6.D + "0.9.0_WK_IRPT_BCKEND~%d/%s" % (c["slot"], c["rec"])


P7.rec_path = rec_path
CHECKS = {
    "IB215-1-AC1": lambda: P1.tests_pass(CELLS["1"]), "IB215-1-AC2": lambda: P0.build_ac2(CELLS["1"]), "IB215-1-AC3": lambda: P7.ac3(CELLS["1"]),
}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p215_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
