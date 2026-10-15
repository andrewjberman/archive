"""IRPT_BCKEND workstream ~PL round 3 (issuer 2.0.0_SA_COO~P2) -- the checks of two BUILD cells.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
It reuses the round-196/200/201/207 helpers (committed beside r235).

  IB235-1  IB-pr-604  the account the 49 Financial candidate drops on the join is kept (CTO ruling @334382c7f4 item 1, msg 8527), the guard unchanged
    AC1  the new tests and the existing publish-gate, exemption and wiring tests pass
    AC2  the difference control: with every ACCOUNT-JOIN-A block removed in memory the new tests FAIL on assertions
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
        slot=440, test=F + "tests/test_account_join.py", min_tests=6, marker="ACCOUNT-JOIN-A", rec="IB235-1_record.json",
        regress=[F + "tests/test_holdings_publish_gate.py", F + "tests/test_absent_at_source_exemption.py", F + "tests/test_absent_at_source_wiring.py",
                 F + "tests/test_holdings_bypass_one_date.py"],
        mutants=[F + "holdings_snapshot.py"],
        allowed=(F + "holdings_snapshot.py", F + "tests/test_account_join.py", F + "tests/test_holdings_publish_gate.py",
                 F + "tests/test_absent_at_source_exemption.py", F + "tests/test_absent_at_source_wiring.py", TO1),
        required=(F + "holdings_snapshot.py", F + "tests/test_account_join.py"), any_of=(F + "holdings_snapshot.py",),
        named=("account_dropped_on_the_join_key_is_kept", "closed_account_absent_from_source_is_not_a_false_fail",
               "other_accounts_are_unchanged", "the_guard_threshold_is_unchanged", "the_build_prints_counts_only")),
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
