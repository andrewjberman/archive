"""IRPT_BCKEND workstream ~PH round 1 (issuer 2.0.0_SA_COO~P2) -- the checks of two BUILD cells.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
It reuses the round-196/200/201/207 helpers (committed beside r216).

  IB216-1  IB-pr-577  the absent_at_source exemption goes LIVE together with its visible listing (CTO msgs 8284, 8290, 8302, 8311): per-firm source evidence loaders, run_firm passes them to the gate, the exempted account stays listed with the not-reported words and no value, the published manifest carries it, and the old closed names are renamed
    AC1  the new tests and the existing publish-gate, exemption, bypass and publication tests pass
    AC2  the difference control: with every ABSENT-AT-SOURCE-B block removed in memory the new tests FAIL on assertions
    AC3  the record: the diff bounded to the grant; the named tests present; no typed object address; counters
  IB216-2  IB-pr-578  the holdings price return is split-adjusted for the 49 Financial channel (CTO ruling @9913bf3ed4, READ IB-pr-572)
    AC1  the new tests and the existing performance tests pass
    AC2  the difference control: with every SPLIT-ADJUST-A block removed in memory the new tests FAIL on assertions
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
PUB = "infra/aws/lambda/investor-reporting/holdings/publication.py"
H = "data/assets/scripts/gold/irpt_holdings_performance/"
# The order files themselves: a worker that flips its own status leaves the order in its commits (AMENDMENT of the check, issuer ruling).
TO1 = "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-577.wire-absent-at-source.md"
TO2 = "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-578.split-adjust-49f.md"
CELLS = {
    "1": dict(
        slot=420, test=G + "tests/test_absent_at_source_wiring.py", min_tests=14, marker="ABSENT-AT-SOURCE-B", rec="IB216-1_record.json",
        regress=[G + "tests/test_holdings_publish_gate.py", G + "tests/test_absent_at_source_exemption.py", G + "tests/test_holdings_bypass_one_date.py",
                 "infra/aws/lambda/investor-reporting/holdings/tests/test_publication.py"],
        mutants=[G + "holdings_snapshot.py", PUB],
        allowed=(G + "holdings_snapshot.py", PUB, G + "tests/test_absent_at_source_wiring.py", G + "tests/test_absent_at_source_exemption.py",
                 G + "tests/test_closed_at_source_exemption.py", G + "tests/test_holdings_publish_gate.py", G + "tests/test_holdings_bypass_one_date.py",
                 "infra/aws/lambda/investor-reporting/holdings/tests/test_publication.py", TO1),
        required=(G + "holdings_snapshot.py", PUB, G + "tests/test_absent_at_source_wiring.py"), any_of=(G + "holdings_snapshot.py",),
        named=("evidence_49f_counts_accounts_and_positions_in_both_tables", "evidence_cottonwood_reads_holdings_and_allocations",
               "evidence_missing_prior_partition_fails_closed", "loader_error_keeps_the_refusal", "run_firm_publishes_with_the_account_still_listed",
               "listed_account_has_the_not_reported_words_and_no_value", "scope_and_unique_count_include_the_listed_account",
               "published_manifest_carries_absent_at_source_never_closed", "second_fire_exempts_again_with_the_same_since_date",
               "reappearing_account_is_included_normally", "no_exemption_leaves_nodes_and_manifest_unchanged", "no_closed_names_remain")),
    "2": dict(
        slot=421, test=H + "tests/test_split_adjust.py", min_tests=10, marker="SPLIT-ADJUST-A", rec="IB216-2_record.json",
        regress=[H + "tests/test_holdings_performance.py", H + "tests/test_holdings_comparison.py"],
        mutants=[H + "holdings_performance.py"],
        allowed=(H + "holdings_performance.py", H + "sources.json", H + "tests/test_split_adjust.py", H + "tests/test_holdings_performance.py", TO2),
        required=(H + "holdings_performance.py", H + "tests/test_split_adjust.py"), any_of=(H + "holdings_performance.py",),
        named=("split_day_unchanged_holding_reads_zero_return", "ratio_is_the_median_over_accounts_without_other_activity",
               "unclean_ratio_is_split_ratio_absent_and_not_graded", "no_split_day_is_identical_to_the_unadjusted_return",
               "reverse_split_ratio_below_one", "firm_without_a_split_declaration_is_unchanged", "declaration_shape_is_validated",
               "manifest_carries_the_reason_codes_and_counts", "partial_sale_on_the_split_day_is_not_used_for_the_ratio")),
}


def rec_path(c):
    return P6.D + "0.9.0_WK_IRPT_BCKEND~%d/%s" % (c["slot"], c["rec"])


P7.rec_path = rec_path
CHECKS = {
    "IB216-1-AC1": lambda: P1.tests_pass(CELLS["1"]), "IB216-1-AC2": lambda: P0.build_ac2(CELLS["1"]), "IB216-1-AC3": lambda: P7.ac3(CELLS["1"]),
    "IB216-2-AC1": lambda: P1.tests_pass(CELLS["2"]), "IB216-2-AC2": lambda: P0.build_ac2(CELLS["2"]), "IB216-2-AC3": lambda: P7.ac3(CELLS["2"]),
}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p216_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
