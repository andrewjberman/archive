"""IRPT_BCKEND workstream ~PM round 1 (issuer 2.0.0_SA_COO~P2) -- the checks of two BUILD cells.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
It reuses the round-196/200/201/207 helpers (committed beside r225).

  IB225-1  IB-pr-592  the served manifest names each ratio-absent split security by security and day (CTO half of the 49 Financial split pair, condition 3)
    AC1  the new tests and the existing split and performance tests pass
    AC2  the difference control: with every SPLIT-ADJUST-C block removed in memory the new tests FAIL on assertions
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

H = "data/assets/scripts/gold/irpt_holdings_performance/"
TO1 = "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-592.split-ratio-absent-named.md"
CELLS = {
    "1": dict(
        slot=432, test=H + "tests/test_split_ratio_absent_named.py", min_tests=8, marker="SPLIT-ADJUST-C", rec="IB225-1_record.json",
        regress=[H + "tests/test_split_adjust.py", H + "tests/test_split_unkeyed.py", H + "tests/test_holdings_performance.py"],
        mutants=[H + "holdings_performance.py"],
        allowed=(H + "holdings_performance.py", H + "tests/test_split_ratio_absent_named.py", H + "tests/test_split_adjust.py", H + "tests/test_split_unkeyed.py",
                 H + "tests/test_holdings_performance.py", TO1),
        required=(H + "holdings_performance.py", H + "tests/test_split_ratio_absent_named.py"), any_of=(H + "holdings_performance.py",),
        named=("manifest_names_each_ratio_absent_security_by_day", "ratio_absent_entry_carries_day_security_and_accounts_used",
               "no_ratio_absent_leaves_the_manifest_list_empty", "list_is_sorted_by_day_then_security", "unkeyed_rows_are_listed_by_day_without_a_security",
               "existing_manifest_keys_unchanged")),
}


def rec_path(c):
    return P6.D + "0.9.0_WK_IRPT_BCKEND~%d/%s" % (c["slot"], c["rec"])


P7.rec_path = rec_path
CHECKS = {
    "IB225-1-AC1": lambda: P1.tests_pass(CELLS["1"]), "IB225-1-AC2": lambda: P0.build_ac2(CELLS["1"]), "IB225-1-AC3": lambda: P7.ac3(CELLS["1"]),
}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p225_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
