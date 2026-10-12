"""Builds CONVENTION_CHANGE_SIZE.json from the private counts draft written by size128.py (counts only; no client literal).
Usage: python -I build_record128.py <repo_root>
"""
import json
import sys
from pathlib import Path

P = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~128/"
d = json.loads(Path(P + "record_counts_draft.json").read_bytes().decode("utf-8"))
root = Path(sys.argv[1])
out = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~128/CONVENTION_CHANGE_SIZE.json"
ec = d["end_reproduces"]
rec = {
    "record": "IRPT_DASHBD.TO-DB-b-159 -- the size of a change of flow convention, on a private copy",
    "worker": "0.9.0_WK_IRPT_DASHBD~128",
    "firm": "the one firm the tie-out reads (49 Financial), its own gold prefix only",
    **{k: d[k] for k in ("served_accounts", "account_days", "date_range", "on_a_copy", "s3_writes", "s3_reads")},
    "served_rule": {
        "END": "data/assets/scripts/gold/irpt_reporting/account_return_daily.py lines 1383-1406 (chain of sub-periods; with no intervening "
               "custodian valuation it is the endpoint form (V_t - F_t) / V_(t-1) - 1 at line 1400) and the module docstring lines 28-45; "
               "the flow F_t is summed over the custodian partition days after t-1 up to t; the PRD's C-METHOD / C-FLOWTIME name the same rule",
        "windows": "infra/aws/lambda/investor-reporting/reporting-publish/publisher.py lines 275-310: a window is the geometric link of "
                   "total_return_daily over the days dated after its anchor up to as_of; not spanned if the first data date is after the "
                   "anchor; a null-return day inside the window breaks it (no figure). YTD, QTD, 1Y, 3Y and SI are served; MTD is NOT a "
                   "served window: here MTD uses the same rule with the anchor at the prior month end, and ITD is the served SI rule",
    },
    "restatement": {
        "definition": "reused, not re-implemented: the three one-day formulas of org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
                      "0.9.0_WK_IRPT_DASHBD~121/y1_place.py relink, lines 44-52 (START v1/(v0+f)-1; MID (v1-f/2)/(v0+f/2)-1; END (v1-f)/v0-1), "
                      "the definition cited in TIMING_CLASSES_PROPOSAL.json definitions_cited.admitted_timings. Applied per served day instead "
                      "of chained over a segment; v0 is the previous served row's market_value_eod of the same account, f the served "
                      "external_flow of the day",
        "difference_from_121": "121 skips a day whose served return is null before choosing the prior day; here the prior value is the previous "
                               "served row whether or not its return is null, and a null-return day is not restated (left null)",
    },
    "end_reproduces": {
        "account_days": ec["account_days"], "equal_within": ec["equal_within"],
        "equal": ec["reproduces"], "not_equal": ec["not_equal"], "no_prior_value": ec["no_prior_value_left_as_served"],
        "null_served_days_not_restated": ec["null_served_days_not_restated"],
        "not_equal_explained_by": "all not_equal days carry carried_days 2 and a flow: a custodian valuation on the skipped day sits "
                                  "inside the window and the served END chains through it (account_return_daily.py lines 1383-1406); "
                                  "a day-pair restatement cannot see that valuation. no_prior_value is NOT explained",
        "share_not_reproduced": "19 of %d served-return days (about 7 in a million), under the 1 in 100 stop line" % ec["account_days"],
        "price_return_fallback_days": 0,
        "price_return_fallback_note": "no served row carries return_basis HOLDINGS_INCOME_FALLBACK (return_basis is TWR or NOT_MEASURABLE only; "
                                      "account_return_daily.py line 164 'NEVER EMITTED'), so the named class is empty; nothing to leave as served",
        "left_as_served": "the not_equal days, the no_prior_value days and days where the START denominator is zero are left as served under "
                          "START and MID (not differing); null-return days stay null",
        "start_denominator_zero_days": 643,
    },
    "differing_precision": "the served file is float64; a day differs when the absolute difference exceeds 1e-12 of a return (above float64 "
                           "round-off of a ratio of two sums); days differing only below that floor are counted in differing_strictly_above_zero",
    "daily": d["daily"],
    "windows": d["windows"],
    "bands_edges": "absolute difference: under_1bp is below 1 basis point; from_1_to_10bp is 1 to 10 inclusive; over_10bp is above 10",
    "flow_day_definition": "flow_days: restated account-days (served return present, END reproduced) whose served external_flow is nonzero; "
                           "a day with no flow has the same return under all three conventions and is not a differing day",
    "largest_band_note_daily": "under_1bp holds the most differing days both ways; over_10bp holds the fewest, and END-to-START has more over_10bp days than END-to-MID",
    "private_table": "the private evidence folder for worker ~128 under IRPT_DASHBD (account_day_table.parquet, README.txt), outside the repo",
    "limits": [
        "A day-pair restatement from the served row: it does not see an intervening custodian valuation on a skipped day, so 17 served-return "
        "days that chain through one are not reproduced and are left as served.",
        "For a day with carried_days 2 the served flow is the two-day sum and START/MID treat it as one day's flow: sizes on those days (a few "
        "thousand rows in the copy) are an approximation.",
        "Windows follow the publisher's rule for a window carried (spanned and no null-return day inside it); accounts that break or are not "
        "spanned are not counted in the window and are listed under windows.not_carried. Under START and MID a window is the chain of the "
        "restated days and a not-restated day keeps its served return.",
        "The copy begins at the first served partition; ITD is anchored at each account's first served row, so for an account that was already "
        "in the book then it is since the start of the copy.",
        "The served flag of a restated day (day_quality, guard_state) is read as served; how the guard's flags would move under START or MID "
        "is DB-b-160's question and is not answered here.",
        "The guard's thresholds were not re-run; no restated day was re-graded.",
    ],
    "the_39": {
        "count": 39, "accrual_class": 31, "unclassed": 8,
        "statement": "39 of the 90 two-sided segments close under NO timing (31 of the accrual class, 8 unclassed); nothing in this record changes "
                     "them, and a change of flow convention would not close the tie-out.",
    },
}
out.write_bytes((json.dumps(rec, indent=1) + "\n").encode("utf-8"))
print("written", out.name)
