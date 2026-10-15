"""IRPT_BCKEND workstream ~PN round 3 (issuer 2.0.0_SA_COO~P2) -- the checks of two BUILD cells.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
It reuses the round-196/200/201/207 helpers (committed beside r231).

  IB231-1  IB-pr-599  the Scope account feed writes a day's keys ONLY when the day is complete (CTO msg 8536 item 4)
    AC1  the new tests and the feed's existing tests pass
    AC2  the difference control: with every SCOPE-FEED-C block removed in memory the new tests FAIL on assertions
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

F = "data/inf/manual_api/"
TO1 = "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-599.scope-feed-day-complete.md"
CELLS = {
    "1": dict(
        slot=436, test=F + "test_scope_feed_day_complete.py", min_tests=9, marker="SCOPE-FEED-C", rec="IB231-1_record.json",
        regress=[F + "test_pull_inflection_scope_account_returns.py", F + "test_scope_feed_daily_factor.py", "data/inf/scripts/gold/tests/test_aor_resolution.py"],
        mutants=[F + "pull_inflection_scope_account_returns.py"],
        allowed=(F + "pull_inflection_scope_account_returns.py", F + "test_scope_feed_day_complete.py", F + "test_pull_inflection_scope_account_returns.py",
                 F + "test_scope_feed_daily_factor.py", TO1),
        required=(F + "pull_inflection_scope_account_returns.py", F + "test_scope_feed_day_complete.py"), any_of=(F + "pull_inflection_scope_account_returns.py",),
        named=("day_with_a_failed_household_writes_no_key", "complete_day_writes_both_keys", "failed_households_are_named_in_the_output_and_the_exit_is_nonzero",
               "rerun_after_a_failed_day_writes_the_day", "from_date_window_writes_only_complete_days", "a_throttle_stop_writes_no_key_for_the_day",
               "existing_behaviours_unchanged")),
}


def rec_path(c):
    return P6.D + "0.9.0_WK_IRPT_BCKEND~%d/%s" % (c["slot"], c["rec"])


P7.rec_path = rec_path
CHECKS = {
    "IB231-1-AC1": lambda: P1.tests_pass(CELLS["1"]), "IB231-1-AC2": lambda: P0.build_ac2(CELLS["1"]), "IB231-1-AC3": lambda: P7.ac3(CELLS["1"]),
}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p231_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
