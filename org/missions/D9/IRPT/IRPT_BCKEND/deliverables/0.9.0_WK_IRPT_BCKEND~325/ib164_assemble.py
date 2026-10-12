#!/usr/bin/env python3
"""IB-pr-470: assemble IB164-1_status_set_and_base.json and IB164-1_STATUS_SET_AND_BASE_READ.md from the files ib164_measure.py wrote to the
scratch folder.   python -I ib164_assemble.py <scratch> <out_dir> <base_commit>
Counts only.  Reads local files; touches no AWS."""
import json
import sys
from pathlib import Path

WINDOWS = ("SI", "YTD", "QTD", "1Y")
ENTRIES = (("49F", "the 49F entry"), ("orion", "orion"))
HELD = ("held_none", "held_included_only_or_mixed", "held_only_excluded", "held_only_negative", "held_other", "not_determinable")
NOHOLD = ("held_none", "not_determinable")
P = "data/assets/scripts/gold/irpt_holdings_performance/holdings_performance.py"
R = "infra/aws/lambda/investor-reporting/performance/holdings_gold.py"

TOKENS = [
    {"token": "OK", "defined_at": P + ":219", "assigned_at": P + ":873",
     "condition_in_words": "np.select default (:874): none of the three conditions is true, i.e. the basket (included holdings plus positive cash) is above zero or the account is pure cash; "
                           "the return is computed (:875-878). It can later be overwritten by IMPLAUSIBLE-RETURN (:883) or FOLLOWS-DISCONTINUITY (:952)."},
    {"token": "NO-PRIOR-HOLDINGS", "defined_at": P + ":220", "assigned_at": P + ":873",
     "condition_in_words": "np.select choice 1, condition at :869: held_count == 0 and cash_value == 0.0 -- no position row (included, excluded or negative) and exactly zero cash on the prior trading day."},
    {"token": "ALL-HOLDINGS-EXCLUDED", "defined_at": P + ":222", "assigned_at": P + ":873",
     "condition_in_words": "np.select choice 2, conditions at :870-871: held_count > 0, included_count == 0, negative_count == 0 and cash_value <= 0.0 -- the account held positions, none reached "
                           "the basket (no identifier, or no price on both days), none was negative, and there is no positive cash."},
    {"token": "NON-POSITIVE-BASE", "defined_at": P + ":221", "assigned_at": P + ":873",
     "condition_in_words": "np.select choice 3, condition at :872: account_value <= 0.0 (account_value = included_value + positive cash, :856), reached only when neither earlier condition is true. "
                           "By the first two conditions that means: (a) no position row and non-zero cash that is negative (a debit; positive cash would make the basket positive); (b) at least one "
                           "negative position row, no included row, cash <= 0; (c) at least one included row of total value exactly 0 (included rows are value >= 0) and cash <= 0."},
    {"token": "IMPLAUSIBLE-RETURN", "defined_at": P + ":223", "assigned_at": P + ":883",
     "condition_in_words": "after the grade, a row that is status OK whose computed daily_return is <= -1.0 or >= 1.0 (_IMPLAUSIBLE_LO/_HI, :169; mask :881-882) is overwritten (:883) and its return nulled (:884)."},
    {"token": "FOLLOWS-DISCONTINUITY", "defined_at": P + ":224", "assigned_at": P + ":952",
     "condition_in_words": "apply_follow_day_rule (:939-955): a row that is still OK whose account was IMPLAUSIBLE-RETURN on the previous trading day (ImplausibleIndex, :907-936) is overwritten; does not cascade."},
]


def main(scratch, out_dir, base):
    sc, out = Path(scratch), Path(out_dir)
    root = Path(__file__).resolve().parent.parents[6]
    prior = {(c["entry"], c["window"]): c for c in json.loads(
        (root / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~322/IB161-1_excluded_day_base.json").read_text(encoding="utf-8"))["per_entry_and_window"]}
    names = {t["token"] for t in TOKENS}
    gold, avail_info, cells = {}, {}, []
    for e, nm in ENTRIES:
        cen = json.loads((sc / ("census_%s.json" % e)).read_text())
        avail_info[e] = json.loads((sc / e / "avail_all_count.json").read_text())
        gold[nm] = {"partitions_read": cen["partitions_read"], "rows_read": cen["rows_read"], "by_token": cen["by_token"],
                    "tokens_in_the_gold_not_in_the_code": sorted(set(cen["by_token"]) - names),
                    "first_partition": cen["first_partition"], "last_partition": cen["last_partition"],
                    "partitions_lacking_any_held_column": cen["partitions_lacking_any_held_column"], "partitions_with_zero_rows": cen["partitions_with_zero_rows"]}
        for w in WINDOWS:
            c = json.loads((sc / ("cell164_%s_%s.json" % (e, w))).read_text())
            p = prior[(c["entry"], c["window"])]
            want = sum((p["interior_by_status_and_prior_value"].get("NON-POSITIVE-BASE") or {}).values())
            c["interior_reproduces_ib_pr_467"] = c["non_positive_base_days"]["interior"] == want
            c["ib_pr_467_interior_non_positive_base_days"] = want
            cells.append(c)
    ctl = json.loads((sc / "control.json").read_text())
    excl_only_npb = sum(c["non_positive_base_all_positions_by_prior_day_holdings"]["held_only_excluded"] + c["non_positive_base_interior_by_prior_day_holdings"]["held_only_excluded"] +
                        c["non_positive_base_days_in_accounts_without_a_figure_by_prior_day_holdings"]["held_only_excluded"] for c in cells)
    doc = {
        "base_commit": base,
        "arm": "READER_CODE_OVER_SERVED_GOLD",
        "arm_in_words": "NOT the deployed route. IB-pr-467's arm, unchanged: the route reader's own code at the base commit (holdings_gold.calculate, with the source the route composes at "
                        "installed.py:75 for each of its two firms) run locally over the SERVED holdings gold read from S3 (list and get only; no Lambda invoked, no sign-in, nothing written to AWS). "
                        "Every partition at or before 2026-10-08 was read once into a local cache outside the worktree; the reader's calculate() was run once per account per window with the rows "
                        "served from memory by IB-pr-464's stand-in for the source's transport (copied). The status census, the day placement and the claim counter are this driver's, over the same cached rows.",
        "latest_landed_day": "2026-10-08",
        "latest_landed_day_note": "Partitions listed: the 49F entry %d (last %s), orion %d (last %s); used (<= 2026-10-08): %d and %d." % (
            avail_info["49F"]["listed"], avail_info["49F"]["last_listed"], avail_info["orion"]["listed"], avail_info["orion"]["last_listed"],
            avail_info["49F"]["used"], avail_info["orion"]["used"]),
        "status_tokens_in_code": TOKENS,
        "can_a_token_outside_the_constants_be_written": {
            "answer": "NO",
            "in_words": "The column is written at three places in the whole producer package (data/assets/scripts/gold/irpt_holdings_performance/, two modules): np.select (%s:873-874) whose choices are "
                        "three constants and whose default is STATUS_OK; the implausible overwrite (:883, STATUS_IMPLAUSIBLE); the follow-day overwrite (:952, STATUS_FOLLOWS_DISCONTINUITY). "
                        "holdings_comparison.py only reads the column (:223). A grep of the package for assignments to the status column finds no other writer. The gold's tokens are checked in "
                        "status_counts_over_the_served_gold." % P,
            "line": P + ":873"},
        "status_counts_over_the_served_gold": gold,
        "per_entry_and_window": cells,
        "prior_day_holdings_rule_in_words": "The gold carries the four count columns the face names, under these served names: held_count, included_count, negative_count, cash_value (plus excluded_count, "
                                            "which was already read). They describe the account's positions on the BASE day, the prior trading day (or the last close that exists when the row links across a gap): "
                                            "holdings_return(p0, p1, cash, ..., prev_day=base_day) is called with the base-day positions p0 and the base-day cash (%s:1065; counts at :843-847; the call "
                                            "reads prev_positions at :758). A 'position row' is a key (identifier, lots summed): held_count = included + excluded + negative keys. The six classes, from the "
                                            "NON-POSITIVE-BASE row's own columns: held_none = held_count 0; held_included_only_or_mixed = included_count >= 1; held_only_negative = every key negative "
                                            "(negative_count == held_count > 0); held_only_excluded = held_count > 0 with included_count 0 and negative_count 0; held_other = held_count > 0, included_count 0, "
                                            "negative_count > 0 and excluded_count > 0; not_determinable = any of the four counts null, or held_count != included + excluded + negative. "
                                            "non_positive_base_all_positions_with_nonzero_cash counts the days (all positions) whose cash_value is not zero." % P,
        "assignment_order": {
            "order_in_words": "np.select takes the FIRST true condition (%s:873-874): NO-PRIOR-HOLDINGS (:869), then ALL-HOLDINGS-EXCLUDED (:870-871), then NON-POSITIVE-BASE (:872), default OK. "
                              "The code comment at :861-868 states that ALL-HOLDINGS-EXCLUDED is evaluated first so a full exit does not read NON-POSITIVE-BASE." % P,
            "cites": [P + ":869", P + ":870", P + ":872", P + ":873", P + ":861"],
            "only_excluded_holdings_can_be_stamped_non_positive_base": "NO",
            "in_words": "An account holding only excluded, non-negative positions (held_count > 0, included_count 0, negative_count 0) has cash_value either <= 0, which meets the ALL-HOLDINGS-EXCLUDED "
                        "condition (:870-871) first, or > 0, which makes account_value > 0 (:856, the OK default), so NON-POSITIVE-BASE is unreachable for it. The cases that DO receive "
                        "NON-POSITIVE-BASE are exactly: (a) no position row and negative cash (a debit); (b) one or more negative position rows, no included row, cash <= 0 (any excluded rows beside them); "
                        "(c) one or more included rows all valued exactly 0, with cash <= 0 (any excluded or negative rows beside them). Measured cross-check: NON-POSITIVE-BASE days placed "
                        "held_only_excluded in all cells, all positions, with or without a figure: %d." % excl_only_npb,
            "measured_non_positive_base_days_placed_held_only_excluded": excl_only_npb},
        "control": ctl,
        "not_established": [
            "the deployed route's own answer: no Lambda invoked, no sign-in; the deployed package, mapping loader, authorization and envelope were not exercised",
            "the C-CHAINCLAIM contract's own definition of 'excluded day' and of the claim: only the face's description was used; the PRD addendum text was not graded here",
            "whether a NON-POSITIVE-BASE day in an account that held a position left a return out in the account's real history: the gold carries the base-day counts and cash, not prices or cash flows, so a zero-valued included position or a negative key is seen, its cause is not",
            "accounts the reader refuses (no OK row in the window) are not part of 'accounts with a figure'; their NON-POSITIVE-BASE days are reported separately by class and are in no claim-move count",
            "the producer's status grade was read from the code at the base commit; the gold's partitions were not regenerated, and the silver (prices, identifiers, balances) was not read",
            "the gold was read once, at the time of this run, capped at 2026-10-08; a later partition may have landed",
            "the transport check of IB-pr-464 (stand-in versus the reader's own HoldingsGoldSource class) was not repeated: the same stand-in is used; the reproduction of IB-pr-467's interior NON-POSITIVE-BASE counts is the check",
        ],
        "functions_invoked": 0, "sign_ins_made": 0, "aws_writes_made": 0, "accounts_written": 0, "values_written": 0, "product_files_edited": 0,
    }
    (out / "IB164-1_status_set_and_base.json").write_text(json.dumps(doc, indent=1), encoding="utf-8")

    def held_pos(t):
        return sum(v for k, v in t.items() if k not in NOHOLD)
    L = ["# IB-pr-470: the closed status set, the NON-POSITIVE-BASE days by what the account held the day before, and the accounts whose claim moves", "",
         "Base `%s`. READ ONLY. Arm `READER_CODE_OVER_SERVED_GOLD` (IB-pr-467's, not the deployed route). Latest landed day read: 2026-10-08. Partitions read: the 49F entry %d, orion %d. "
         "Counts only; no account id, balance, return or cash amount is written." % (base, gold["the 49F entry"]["partitions_read"], gold["orion"]["partitions_read"]), "",
         "## Answer first: NON-POSITIVE-BASE days in an account that held a position the day before", ""]
    for e, nm in ENTRIES:
        for c in cells:
            if c["entry"] == nm:
                ti, ta = c["non_positive_base_interior_by_prior_day_holdings"], c["non_positive_base_all_positions_by_prior_day_holdings"]
                L.append("- %s %s: all positions %d of %d days (interior %d of %d); not_determinable %d; with non-zero cash %d" % (
                    nm, c["window"], held_pos(ta), c["non_positive_base_days"]["all_positions"], held_pos(ti), c["non_positive_base_days"]["interior"],
                    ta["not_determinable"], c["non_positive_base_all_positions_with_nonzero_cash"]))
    L += ["", "Reading the classes: a `held_none` NON-POSITIVE-BASE day is, by the producer's conditions (:869, :872), a day with no position row and a non-zero cash balance that is negative (a debit); "
          "the 49F entry's days are almost all of that kind (the `with non-zero cash` figure beside each cell). The orion days all carry zero cash and a position row: by the conditions, included rows all valued "
          "exactly zero (held_included_only_or_mixed), or negative keys with no included row (held_other). The gold carries counts and cash, not the cause.", ""]
    L += ["", "## Status tokens in the producer (%s)" % P, ""]
    for t in TOKENS:
        L.append("- `%s` defined %s, assigned %s: %s" % (t["token"], t["defined_at"].split(":")[1], t["assigned_at"].split(":")[1], t["condition_in_words"]))
    L += ["", "Can a token outside the constants be written: NO. " + doc["can_a_token_outside_the_constants_be_written"]["in_words"], "",
          "## Counts over the served gold (every landed partition <= 2026-10-08)", "", "| entry | partitions | rows | " + " | ".join(t["token"] for t in TOKENS) + " | in gold, not in code |",
          "|---|---|---|" + "---|" * (len(TOKENS) + 1)]
    for nm, g in gold.items():
        L.append("| %s | %d | %d | %s | %s |" % (nm, g["partitions_read"], g["rows_read"], " | ".join(str(g["by_token"].get(t["token"], 0)) for t in TOKENS),
                                                  ", ".join(g["tokens_in_the_gold_not_in_the_code"]) or "none"))
    L += ["", "## Assignment order", "", doc["assignment_order"]["order_in_words"], "",
          "Can an account holding only excluded, non-negative positions receive NON-POSITIVE-BASE: **NO**. " + doc["assignment_order"]["in_words"], "",
          "## Prior-day holdings rule", "", doc["prior_day_holdings_rule_in_words"], ""]
    for e, nm in ENTRIES:
        L += ["## %s: NON-POSITIVE-BASE days by what the account held the prior day" % nm, "",
              "| window | scope | days | " + " | ".join(HELD) + " | nonzero cash | accounts with a figure | claim: measured today | as written | if NPB with a prior position also |", "|---|---|---|" + "---|" * (len(HELD) + 5)]
        for c in cells:
            if c["entry"] != nm:
                continue
            m = c["accounts_whose_claim_moves"]
            for part, key in (("interior", "non_positive_base_interior_by_prior_day_holdings"), ("all positions", "non_positive_base_all_positions_by_prior_day_holdings")):
                t = c[key]
                L.append("| %s | %s | %d | %s | %s | %s | %s | %s | %s |" % (
                    c["window"], part, sum(t.values()), " | ".join(str(t[k]) for k in HELD),
                    c["non_positive_base_all_positions_with_nonzero_cash"] if part != "interior" else "-",
                    c["accounts_with_a_figure"], m["accounts_with_a_figure_saying_measured"], m["under_the_contract_as_written"], m["if_non_positive_base_with_a_prior_position_also_moves"]))
        L += ["", "Where the all-positions days sit (before the first OK day / interior / after the last OK day, of which the last row):", ""]
        for c in cells:
            if c["entry"] == nm:
                p = c["non_positive_base_all_positions_by_position_in_window"]
                L.append("- %s: %d / %d / %d (last row %d); excluded days in accounts with a figure, by status: %s; interior reproduces IB-pr-467 (%d): %s" % (
                    c["window"], p["before_first_ok"], p["interior"], p["after_last_ok"], p["of_which_the_last_row"], json.dumps(c["excluded_days_in_accounts_with_a_figure_by_status"]),
                    c["ib_pr_467_interior_non_positive_base_days"], "yes" if c["interior_reproduces_ib_pr_467"] else "NO"))
        L.append("")
    L += ["## Control", "", ctl["what"], "", "Reading: " + json.dumps(ctl["reading"], sort_keys=True), "", "## Not established", ""] + ["- " + x for x in doc["not_established"]] + [
        "", "Zeros: functions invoked 0, sign-ins 0, AWS writes 0, accounts written 0, values written 0, product files edited 0.", ""]
    (out / "IB164-1_STATUS_SET_AND_BASE_READ.md").write_text("\n".join(L), encoding="utf-8")
    print("assembled", len(cells), "cells; non-positive-base days placed held_only_excluded:", excl_only_npb)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
