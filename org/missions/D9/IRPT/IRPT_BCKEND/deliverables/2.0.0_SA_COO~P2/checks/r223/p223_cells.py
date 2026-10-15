"""IRPT_BCKEND workstream ~PN round 1 (issuer 2.0.0_SA_COO~P2) -- the checks of two BUILD cells.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
It reuses the round-196/200/201/207 helpers (committed beside r223).

  IB223-1  IB-pr-586  the Scope account feed: a pull step with the coverage rule, fee_basis NET, its own prefixes, the catalog row (CTO msgs 8411, rounds 118 to 121)
    AC1  the new tests and the regression test pass
    AC2  the difference control: with every SCOPE-FEED-A block removed in memory the new tests FAIL on assertions
    AC3  the record: the diff bounded to the grant; the named tests present; no typed object address; counters
  IB223-2  IB-pr-587  the one-account limit of orion_account_mapping.py lifted, a household-members helper added (same release as the feed)
    AC1  the new tests and the flipped existing test pass
    AC2  the difference control: with every ORION-HOUSEHOLD-A block removed in memory the new tests FAIL on assertions
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
L = "infra/aws/lambda/investor-reporting/performance/"
DISP = "data/inf/scripts/gold/orion-gold-dispatch.sh"
TO1 = "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-586.scope-account-feed.md"
TO2 = "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-587.orion-household-accounts.md"
CELLS = {
    "1": dict(
        slot=429, test=F + "test_pull_inflection_scope_account_returns.py", min_tests=16, marker="SCOPE-FEED-A", rec="IB223-1_record.json",
        regress=["data/inf/scripts/gold/tests/test_aor_resolution.py"],
        mutants=[F + "pull_inflection_scope_account_returns.py"],
        allowed=(F + "pull_inflection_scope_account_returns.py", F + "test_pull_inflection_scope_account_returns.py", DISP, TO1),
        required=(F + "pull_inflection_scope_account_returns.py", F + "test_pull_inflection_scope_account_returns.py", DISP), any_of=(F + "pull_inflection_scope_account_returns.py",),
        named=("request_body_is_the_inner_scope_with_account_grouping", "every_request_keeps_calcgrossoffees_false", "fee_basis_net_recorded_with_its_note",
               "covered_account_carries_orion_return", "missing_account_is_absent_no_group_never_zero", "group_without_series_is_group_no_series_not_determined",
               "null_start_date_account_is_no_start_date_at_source_with_claim", "claim_promoted_to_measured_when_the_call_misses_a_null_start_account",
               "no_zero_and_no_fill_for_an_absent_account", "one_call_per_household_paced_no_retry", "prefixes_are_address_output_and_bronze_is_json_gz",
               "key_read_absent_first_and_never_overwritten", "catalog_row_and_chain_entries_present_and_tolerated",
               "from_date_window_splits_series_into_per_day_rows_and_skips_existing_keys")),
    "2": dict(
        slot=430, test=L + "tests/test_orion_account_mapping_household.py", min_tests=8, marker="ORION-HOUSEHOLD-A", rec="IB223-2_record.json",
        regress=[L + "tests/test_orion_account_mapping.py"],
        mutants=[L + "orion_account_mapping.py"],
        allowed=(L + "orion_account_mapping.py", L + "tests/test_orion_account_mapping_household.py", L + "tests/test_orion_account_mapping.py", TO2),
        required=(L + "orion_account_mapping.py", L + "tests/test_orion_account_mapping_household.py"), any_of=(L + "orion_account_mapping.py",),
        named=("household_with_many_accounts_is_no_longer_refused", "household_members_listed_for_a_household", "single_account_household_unchanged",
               "unknown_account_still_refused", "unmapped_household_still_refused", "each_account_attributed_to_itself")),
}


def rec_path(c):
    return P6.D + "0.9.0_WK_IRPT_BCKEND~%d/%s" % (c["slot"], c["rec"])


P7.rec_path = rec_path
CHECKS = {
    "IB223-1-AC1": lambda: P1.tests_pass(CELLS["1"]), "IB223-1-AC2": lambda: P0.build_ac2(CELLS["1"]), "IB223-1-AC3": lambda: P7.ac3(CELLS["1"]),
    "IB223-2-AC1": lambda: P1.tests_pass(CELLS["2"]), "IB223-2-AC2": lambda: P0.build_ac2(CELLS["2"]), "IB223-2-AC3": lambda: P7.ac3(CELLS["2"]),
}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p223_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
