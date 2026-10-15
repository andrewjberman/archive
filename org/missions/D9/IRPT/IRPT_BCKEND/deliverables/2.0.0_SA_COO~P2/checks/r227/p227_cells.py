"""IRPT_BCKEND workstream ~PN round 2 (issuer 2.0.0_SA_COO~P2) -- the checks of two BUILD cells.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
It reuses the round-196/200/201/207 helpers (committed beside r227).

  IB227-1  IB-pr-594  the Scope account feed stores the DAILY FACTOR only, adds SERIES_ENDED_AT_SOURCE and walks calendar days (CTO msg 8484, round-118 ADDENDUM 3)
    AC1  the new tests and the feed's existing tests pass
    AC2  the difference control: with every SCOPE-FEED-B block removed in memory the new tests FAIL on assertions
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
TO1 = "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-594.scope-feed-daily-factor.md"
CELLS = {
    "1": dict(
        slot=433, test=F + "test_scope_feed_daily_factor.py", min_tests=12, marker="SCOPE-FEED-B", rec="IB227-1_record.json",
        regress=[F + "test_pull_inflection_scope_account_returns.py", "data/inf/scripts/gold/tests/test_aor_resolution.py"],
        mutants=[F + "pull_inflection_scope_account_returns.py"],
        allowed=(F + "pull_inflection_scope_account_returns.py", F + "test_scope_feed_daily_factor.py", F + "test_pull_inflection_scope_account_returns.py", TO1),
        required=(F + "pull_inflection_scope_account_returns.py", F + "test_scope_feed_daily_factor.py"), any_of=(F + "pull_inflection_scope_account_returns.py",),
        named=("daily_factor_is_the_point_factor_and_the_return_column_is_gone", "the_summary_performance_is_never_stored",
               "series_ended_at_source_marks_days_after_the_last_point_absent", "series_end_reason_claim_is_measured",
               "calendar_days_include_weekends_in_the_window_and_the_rows", "scheduled_window_starts_after_the_newest_landed_day_and_is_capped",
               "first_run_window_is_the_pull_date_only", "factor_chains_to_the_period_return_in_a_fixture", "existing_reason_classes_unchanged",
               "from_date_window_emits_calendar_days_including_weekends")),
}


def rec_path(c):
    return P6.D + "0.9.0_WK_IRPT_BCKEND~%d/%s" % (c["slot"], c["rec"])


P7.rec_path = rec_path
CHECKS = {
    "IB227-1-AC1": lambda: P1.tests_pass(CELLS["1"]), "IB227-1-AC2": lambda: P0.build_ac2(CELLS["1"]), "IB227-1-AC3": lambda: P7.ac3(CELLS["1"]),
}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p227_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
