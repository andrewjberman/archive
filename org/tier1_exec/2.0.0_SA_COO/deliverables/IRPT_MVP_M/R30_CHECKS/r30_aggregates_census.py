"""Workstream ~M, STATUS~M.md next-list item 1: the aggregates census on the 291 base (CTO sweep-5 analysis, section 2
item 4; built under the FAST lease IRPT_BCKEND~M, no order).

Item 1 ports IB-mr-261's producer-served `security_aggregates` and `class_totals` onto CLOUD's narrowed classifier
(IB-mr-291: canonical table first, the declared bd-securities fallback behind it). The census rule is the round-26 one,
unchanged (one aggregate per security identity; weights sum to 1 with the named held-out remainder; class amounts sum
to the custody total within one cent; the grain named; the built document validates against the contract). Only the
census file is new, because the round-26 census was measured on the held table-only classifier.

Run from the repo (or worktree) root. Prints AGG-CENSUS <firm=securities/classes ...> or NOT-CENSUSED: <reason>.
"""
import importlib.util
import os
import sys

PATH = "org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_M/R30_AGGREGATES_CENSUS_20261001.json"
R26 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "R26_CHECKS", "r26_aggregates_census.py")


def main():
    spec = importlib.util.spec_from_file_location("r26_aggregates_census", R26)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.PATH = PATH
    return mod.main()


if __name__ == "__main__":
    sys.exit(main())
