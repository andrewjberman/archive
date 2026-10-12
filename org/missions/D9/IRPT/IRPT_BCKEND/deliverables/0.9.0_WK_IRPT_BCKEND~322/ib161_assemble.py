#!/usr/bin/env python3
"""IB-pr-467: assemble IB161-1_excluded_day_base.json and IB161-1_EXCLUDED_DAY_BASE_READ.md from the per-cell results
ib161_measure.py wrote to the scratch folder.   python -I ib161_assemble.py <scratch> <out_dir> <base_commit>
Counts only.  Reads local files; touches no AWS."""
import json
import sys
from pathlib import Path

WINDOWS = ("SI", "YTD", "QTD", "1Y")
ENTRIES = ("49F", "orion")
PV = ("zero", "negative", "positive", "no_prior_row")
BINS = ("1", "2", "3-5", "6-20", "21-60", "more")
P = "data/assets/scripts/gold/irpt_holdings_performance/holdings_performance.py"
PRIOR = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~319/IB160-1_reader_excluded_days.json"


def table(c, part, mode):
    t = c[mode][part + "_by_status_and_prior_value"]
    toks = sorted(t)
    lines = ["| status | zero | negative | positive | no prior row |", "|---|---|---|---|---|"]
    for s in toks:
        lines.append("| %s | %d | %d | %d | %d |" % (s, *[t[s][k] for k in PV]))
    return "\n".join(lines) if toks else "(no days)"


def main(scratch, out_dir, base):
    sc, out = Path(scratch), Path(out_dir)
    here = Path(__file__).resolve().parent
    root = here.parents[6]
    prior = {(c["entry"], c["window"]): c for c in json.loads((root / PRIOR).read_text(encoding="utf-8"))["per_entry_and_window"]}
    cells, avail_info = [], {}
    for e in ENTRIES:
        avail_info[e] = json.loads((sc / e / "avail_all_count.json").read_text())
        for w in WINDOWS:
            c = json.loads((sc / ("cell161_%s_%s.json" % (e, w))).read_text())
            p = prior[(c["entry"], c["window"])]["position_of_the_excluded_days"]
            c["accounts_in_ib_pr_464"] = p["interior_only"] + p["first_and_interior"] + p["last_day_involved"]
            c["reproduces_ib_pr_464"] = c["accounts_with_an_interior_or_last_row_excluded_day"] == c["accounts_in_ib_pr_464"]
            prim = c["primary_own_row_base"]
            for k, v in prim.items():
                c[k] = v
            cells.append(c)
    ctl = json.loads((sc / "control.json").read_text())
    last_day = "2026-10-08"
    doc = {
        "base_commit": base,
        "arm": "READER_CODE_OVER_SERVED_GOLD",
        "arm_in_words": "NOT the deployed route. IB-pr-464's arm, unchanged: the route reader's OWN code at the base commit (holdings_gold.calculate and map_account, with the source the route "
                        "composes at installed.py:75 for each of its two firms) run locally over the SERVED holdings gold read from S3 (list and get only; no Lambda invoked, no sign-in, no "
                        "Secrets Manager read, nothing written to AWS). Every partition at or before 2026-10-08 was read once into a local cache outside the worktree; the reader's calculate() was "
                        "run once per account per window with the rows served from memory by IB-pr-464's stand-in for HoldingsGoldSource's transport (copied into ib161_measure.py), and the account "
                        "set, window rule and position classifier are IB-pr-464's. The days counted, the base classes and the zero runs are counted by this driver from the same cached rows.",
        "latest_landed_day": last_day,
        "latest_landed_day_note": "Read at 2026-10-08, the day IB-pr-464 read. Partitions listed: the 49F entry %d (last %s), orion %d (last %s); partitions used (<= 2026-10-08): %d and %d." % (
            avail_info["49F"]["listed"], avail_info["49F"]["last_listed"], avail_info["orion"]["listed"], avail_info["orion"]["last_listed"],
            avail_info["49F"]["used"], avail_info["orion"]["used"]),
        "per_entry_and_window": cells,
        "day_rule_in_words": "Per account that the reader gives a figure and with a non-OK day (IB-pr-464's set), take its rows inside the window in date order. A non-OK row (the reader's test, "
                             "holdings_gold.py:246) is INTERIOR when it lies after the account's first OK row and before its last OK row (between two OK days, chained across); it is the "
                             "LAST ROW when it is the account's final row in the window and non-OK. A non-OK row before the first OK row is a first-day exclusion and is not counted. A non-OK row "
                             "after the last OK row that is not the final row (a trailing run longer than one) is neither of the two and is counted only in "
                             "trailing_nonok_days_neither_interior_nor_last_row. days_counted = interior_days + last_row_days.",
        "prior_value_rule_in_words": "The producer's base is the row's OWN account_value: holdings_performance.py:856 sets account_value = included_value + basket_cash, from the PREVIOUS trading day's "
                                     "positions (holdings_return(prev_positions, day_positions, ...), :743-758; the comment at :857-858 'the whole t-1 book'), and the third np.select condition at "
                                     ":872 (account_value <= 0.0 -> NON-POSITIVE-BASE, assigned at :873-874) tests that same column; daily_return is account-value-divided at :876. The gold therefore "
                                     "carries the base in its own column, and the PRIMARY classes in this file use it: a day's 'prior value' is the row's own account_value, which is the account's "
                                     "basket at the close of the day before. The account_value on the account's PREVIOUS row is a different number, the basket at the close of the day before that, "
                                     "and so a proxy, not the base; it is reported separately for every cell under literal_previous_row (same tables, same sums). Not the reader's end_value: the "
                                     "reader reads the first and last OK rows' account_value (holdings_gold.py:274-275).",
        "primary_basis": "own_row_account_value",
        "zero_rule_tolerance": "Exactly 0.0 (v == 0.0). No tolerance. A nonzero value is negative or positive by its sign however small; the count of counted days within a cent (0 < |v| < 0.01) of "
                               "zero but not zero is days_within_a_cent_of_zero_but_not_zero per cell under primary_own_row_base and literal_previous_row. no_prior_row: for the primary basis, the "
                               "row's own account_value is null; for the literal rule, the account has no earlier row in the gold or it is null.",
        "zero_run_rule_in_words": "For a counted day whose prior value is zero, count the consecutive rows of the account in the gold (across all landed partitions up to 2026-10-08, not only the window) "
                                  "whose account_value is exactly 0.0, going back from the day's own row for the primary basis (row i is zero means the close of the day before is zero; 1 = only "
                                  "the close of the day before), and going back from the previous row for literal_previous_row (1 = only the previous row). Bins 1, 2, 3-5, 6-20, 21-60, more (over 60).",
        "primary_vs_literal_note": "The face asks for the prior row's account_value and also for the base column where the gold carries it; the gold does, so the primary tables use the row's own "
                                   "account_value. The literal previous-row reading is kept beside it in every cell (literal_previous_row) so the first can be read either way.",
        "control": ctl,
        "not_established": [
            "the deployed route's own answer: no Lambda invoked, no sign-in; the deployed package, mapping loader, authorization and envelope were not exercised",
            "whether the zero base days are 'empty and re-funded' in the account's real history: the gold carries the account's basket, not its cash flows, so an account that went to zero and later returned is seen, a funding event is not",
            "why a given base is positive on a non-OK day beyond the status token (IMPLAUSIBLE-RETURN, FOLLOWS-DISCONTINUITY, ALL-HOLDINGS-EXCLUDED): the producer's inputs (prices, identifiers) were not read",
            "the producer's status grade was read from the code at the base commit; the gold's partitions were not regenerated or recomputed",
            "the transport check of IB-pr-464 (stand-in versus the reader's own HoldingsGoldSource class) was not repeated: the same stand-in is used; the reproduction of IB-pr-464's account counts is the check",
            "the gold was read once, at the time of this run, capped at 2026-10-08; a later partition may have landed",
            "accounts the reader refuses (no mapping at the last partition, or no OK row in the window) are not placed, as in IB-pr-464",
        ],
        "functions_invoked": 0, "sign_ins_made": 0, "aws_writes_made": 0, "accounts_written": 0, "values_written": 0,
    }
    (out / "IB161-1_excluded_day_base.json").write_text(json.dumps(doc, indent=1, sort_keys=False), encoding="utf-8")

    L = ["# IB-pr-467: the reader's interior and last-row excluded days -- what the base was (zero, negative, positive) and how long the zero run",
         "",
         "Base `%s`. READ ONLY. Arm `READER_CODE_OVER_SERVED_GOLD` (IB-pr-464's, unchanged; NOT the deployed route). Latest landed day read: %s (both entries). Every partition at or before it read once: "
         "the 49F entry %d, orion %d. Counts only; no account id, balance or return is written." % (base, last_day, avail_info["49F"]["used"], avail_info["orion"]["used"]), "",
         "## Answer, leading with the negative and positive-flagged counts (accounts with an interior or last-row excluded day)", ""]
    for e, nm in (("49F", "the 49F entry"), ("orion", "orion")):
        L.append("**%s** (primary basis: the row's own account_value, the producer's base):" % nm)
        for c in cells:
            if c["entry"] == nm:
                L.append("- %s: %d accounts; negative base on one or more days: %d; positive flagged base on one or more days: %d; every counted day on a zero base: %d; reproduces IB-pr-464: %s" % (
                    c["window"], c["accounts_with_an_interior_or_last_row_excluded_day"], c["accounts_with_a_negative_base"],
                    c["accounts_with_a_positive_flagged_base"], c["accounts_all_zero_base"], "yes" if c["reproduces_ib_pr_464"] else "NO"))
        L.append("")
    L += ["## What the base is (producer)", "",
          "- " + doc["prior_value_rule_in_words"], "",
          "- Tolerance: " + doc["zero_rule_tolerance"], "- Day rule: " + doc["day_rule_in_words"], "- Zero run: " + doc["zero_run_rule_in_words"], ""]
    for e, nm in (("49F", "the 49F entry"), ("orion", "orion")):
        L.append("## %s" % nm)
        L.append("")
        L.append("| window | accounts | interior days | last-row days | days counted | all-zero accounts | with a negative | with a positive flagged | within a cent, not zero | trailing (neither) | previous row not the previous partition |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for c in cells:
            if c["entry"] == nm:
                L.append("| %s | %d | %d | %d | %d | %d | %d | %d | %d | %d | %d |" % (
                    c["window"], c["accounts_with_an_interior_or_last_row_excluded_day"], c["interior_days"], c["last_row_days"], c["days_counted"],
                    c["accounts_all_zero_base"], c["accounts_with_a_negative_base"], c["accounts_with_a_positive_flagged_base"],
                    c["days_within_a_cent_of_zero_but_not_zero"], c["trailing_nonok_days_neither_interior_nor_last_row"],
                    c["counted_days_whose_previous_gold_row_is_not_the_previous_landed_partition"]))
        L.append("")
        for c in cells:
            if c["entry"] != nm:
                continue
            L.append("### %s %s" % (nm, c["window"]))
            for part, label in (("interior", "Interior days"), ("last_row", "Last-row days")):
                L.append("")
                L.append("%s (%d) by status and base class (own-row basis):" % (label, c[part + "_days"]))
                L.append("")
                L.append(table(c, part, "primary_own_row_base"))
                L.append("")
                L.append("Zero run (own-row basis): " + ", ".join("%s=%d" % (k, c[part + "_zero_run_lengths"][k]) for k in BINS))
                lp = c["literal_previous_row"]
                L.append("")
                L.append("Literal previous-row reading, by class: " + "; ".join("%s: %s" % (s, ", ".join("%s=%d" % (k, v[k]) for k in PV)) for s, v in sorted(lp[part + "_by_status_and_prior_value"].items())) +
                         ("; zero run: " + ", ".join("%s=%d" % (k, lp[part + "_zero_run_lengths"][k]) for k in BINS)))
            lp = c["literal_previous_row"]
            L.append("")
            L.append("Literal previous-row reading, accounts: all zero %d, with a negative %d, with a positive flagged %d." % (
                lp["accounts_all_zero_base"], lp["accounts_with_a_negative_base"], lp["accounts_with_a_positive_flagged_base"]))
            L.append("")
    L += ["## Control", "", ctl["what"], "", "Reading: " + json.dumps(ctl["reading"], sort_keys=True), "",
          "## Not established", ""] + ["- " + x for x in doc["not_established"]] + ["",
          "Zeros: functions invoked 0, sign-ins 0, AWS writes 0, accounts written 0, values written 0.", ""]
    (out / "IB161-1_EXCLUDED_DAY_BASE_READ.md").write_text("\n".join(L), encoding="utf-8")
    print("assembled", len(cells), "cells")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
