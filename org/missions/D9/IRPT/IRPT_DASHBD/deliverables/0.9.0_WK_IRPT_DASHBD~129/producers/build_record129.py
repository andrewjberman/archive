import json
import re
import os

Q = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~129/"
R = json.load(open(Q + "results.json"))
c = R["control"]
res = R["result"]


def flags(nm):
    e, s, es, se = res["start"]["moves"][nm]
    e2, mm, em, me = res["mid"]["moves"][nm]
    assert e == e2
    return {
        "under_end": e,
        "under_start": s,
        "under_mid": mm,
        "end_not_start": es,
        "start_not_end": se,
        "end_not_mid": em,
        "mid_not_end": me,
    }


F = {"FLOW_UNRECONCILED": flags("FLOW_UNRECONCILED"), "LARGE_FLOW": flags("LARGE_FLOW")}


def sens(key):
    out = {}
    for lab in ("start", "mid"):
        out[lab] = {}
        for nm in ("FLOW_UNRECONCILED", "LARGE_FLOW"):
            e, s, en, sn = res[lab][key][nm]
            out[lab][nm] = {
                "under_end": e,
                "under_" + lab: s,
                "end_not_" + lab: en,
                lab + "_not_end": sn,
            }
    return out


P = R["paths"]
fb = {k: res[k]["fallback"] for k in ("start", "mid")}


def fbrec(k):
    x = fb[k]
    return {
        "null_to_value": x["null_to_value"],
        "value_to_null": x["value_to_null"],
        "total_return_switches": x["null_to_value"] + x["value_to_null"],
        "class_changed_any": x["class_changed_any"],
        "flag_only_class_moves_return_unchanged_in_kind": x[
            "flag_only_moves_no_change_to_return"
        ],
    }


rec = {
    "record": "IRPT_DASHBD.TO-DB-b-160 -- the guard flags FLOW_UNRECONCILED and LARGE_FLOW under each flow convention, counted on a private copy",
    "worker": "0.9.0_WK_IRPT_DASHBD~129",
    "firm": "the one firm the tie-out reads, its own gold prefix only, as copied by 0.9.0_WK_IRPT_DASHBD~128",
    "account_days": R["n"],
    "on_a_copy": True,
    "s3_writes": 0,
    "s3_reads": 0,
    "s3_reads_note": "none: the previous cell private table and served copy held every column the guard reads (served day_quality, guard_state, holdings_price_return, income_return, income_received, external_flow, market_value_eod, carried_days)",
    "guard_rule": {
        "file": "data/assets/scripts/gold/irpt_reporting/account_return_daily.py",
        "line": 1498,
        "lines": {
            "selection_chain": "1498-1528",
            "incomplete_flow_to_FLOW_UNRECONCILED": "1502-1505",
            "ungraded_day_flow_share_over_tolerance_to_FLOW_UNRECONCILED": "1506-1517",
            "graded_and_disagreed_to_FLOW_UNRECONCILED": "1518-1522",
            "LARGE_FLOW": "1523-1525",
            "guard_difference": "1414",
            "flow_share": "1413",
            "vocabulary": "138-159",
            "eligible_band_gate": "1097-1137 (called at 1529)",
        },
        "prd": "org/missions/D9/IRPT/IRPT_DASHBD/prd/IRPT_DASHBD_PRD.md ADDENDUM v0.4 rulings 17-19 (lines 445-473)",
    },
    "flag_rules": {
        "FLOW_UNRECONCILED": "three entries: (a) F_t knowably incomplete (unvalued in-kind leg, unparseable cash, unknown cash above the tolerance of V_(t-1)); (b) the guard did not grade the day (outside the comparability domain) and |F_t|/V_(t-1) is above the guard tolerance; (c) the guard graded the day and |r_t - (holdings price return + income return)| is above the guard tolerance. The day is served with a null return and return_basis NOT_MEASURABLE.",
        "LARGE_FLOW": "reached only after the guard graded the day and agreed: |F_t|/V_(t-1) above the measured large-flow share (a p99 of the share). The day KEEPS its TWR return; the flag is a reader warning, not a refusal.",
    },
    "flag_depends_on_convention": True,
    "depends_basis": "FLOW_UNRECONCILED entry (c) compares the day return r_t, which IS the flow-convention quantity, with the holdings price return plus income; entries (a) and (b) use only V_(t-1) and the flow, so as the code is written they do not depend on the convention. LARGE_FLOW tests |F_t|/V_(t-1), which does not depend on the convention, but is reached only when entry (c) passes and the band gate accepts r_t, so it moves with the convention through those two. The base V_(t-1) in the code neither includes nor excludes the flow; the base follows the convention only in the sensitivity block.",
    "per_flag_basis": {
        "FLOW_UNRECONCILED": {
            "depends": True,
            "through": "the guard difference on graded days (entry c); entries a and b do not move",
        },
        "LARGE_FLOW": {
            "depends": True,
            "through": "ordering behind the guard difference and the plausibility band, not through its own test",
        },
    },
    "thresholds": {
        "how_obtained": "not read from S3; inferred from the served flags by bracketing and checked two independent ways. The tolerance lies between the largest guard difference of a served GRADED_AGREED day and the smallest of a served GRADED_DISAGREED day not explained by a skipped-day chain, and the same interval brackets the ungraded days by flow share; the large-flow share lies between the largest flow share of a served MEASURED graded day and the smallest of a served LARGE_FLOW day. Each interval holds exactly one value at the six decimals the code rounds to (lines 1556 and 1563). The plausibility band is the code default and the served returns sit inside it.",
        "tolerance_consistent_two_ways": True,
        "large_flow_share_interval_holds_one_6dp_value": True,
    },
    "end_reproduces": {
        "FLOW_UNRECONCILED": {
            k: c["FLOW_UNRECONCILED"][k]
            for k in ("flagged_served", "flagged_restated", "differ")
        },
        "LARGE_FLOW": {
            k: c["LARGE_FLOW"][k]
            for k in ("flagged_served", "flagged_restated", "differ")
        },
        "evaluated_days": c["evaluated_days"],
        "days_whose_class_differs_at_all": c["all_class_differ_days"],
        "differ_explained_by": "all %d differing days carry carried_days 2 and a non-zero flow: a custodian valuation on the skipped day sits inside the window and the served END chains through it (account_return_daily.py lines 1383-1406); the day-pair restatement cannot see it. Same cause the previous cell recorded for its not-equal days. %d of the %d differing days carry carried_days 1."
        % (
            c["differ_days_carried_days_gt1"],
            c["differ_days_carried_days_1"],
            c["all_class_differ_days"],
        ),
        "share_not_reproduced": "6 of 6096 served FLOW_UNRECONCILED days and 6 of 42458 served LARGE_FLOW days (the same 6 days: served disagreed, the day-pair form agrees); under 1 in 1000",
        "left_as_served": "the 6 differing days and the 19 days the previous cell left as served (its not-equal and no-prior-value days) keep their served class under START and MID, so they are in neither move",
    },
    "entry_paths_under_end": {
        "incomplete_flow_convention_independent": P[
            "incomplete_unknown_flow_convention_independent"
        ],
        "ungraded_flow_share_over_tolerance_convention_independent": P[
            "ungraded_flow_share_over_tolerance"
        ],
        "graded_disagreed_depends": P["graded_disagreed"],
        "note": "the served FLOW_UNRECONCILED days are the sum of the three; only the graded_disagreed ones can move as the code is written",
    },
    "flags": F,
    "flags_note": "Headline: the code own rule with the day return restated and everything else as served (base V_(t-1), thresholds as served). under_end is the served count. A day moves only if its class under the convention differs; days left as served never move.",
    "what_a_flagged_day_becomes": {
        "FLOW_UNRECONCILED": "total_return_daily null, return_basis NOT_MEASURABLE, the link breaks with a stated gap (account_return_daily.py lines 1502-1505, 1515-1517, 1520-1522; PRD addendum v0.4 ruling 17, lines 454-461)",
        "LARGE_FLOW": "total_return_daily kept, return_basis TWR (lines 1523-1525): a flag only",
        "price_return_fallback": "none. The order and the original C-GUARD clause say a flagged day falls back to the price return; the code does not: HOLDINGS_INCOME_FALLBACK is never emitted (lines 164-170, NEVER EMITTED; PRD ruling 17 withdraws it) and the previous cell counted 0 such days.",
    },
    "fallback_days_moved": {
        "definition": "days whose served treatment changes: the served return switches between a value (MEASURED, LARGE_FLOW) and null with NOT_MEASURABLE (FLOW_UNRECONCILED, NOT_MEASURABLE). There is no price-return fallback to switch to, so the count is of null/value switches.",
        "start": fbrec("start"),
        "mid": fbrec("mid"),
        "price_return_fallback_days_moved": 0,
    },
    "sensitivity": {
        "exclude_carried_days_over_1": {
            "what": "days with a skipped day inside the window left as served, since an intervening valuation is not visible",
            "counts": sens("sens_exclude_carried_gt1"),
        },
        "base_follows_convention": {
            "what": "flow share and income return divided by V_(t-1)+F_t under START and V_(t-1)+F_t/2 under MID instead of V_(t-1); evaluated on the days that already have a prior value",
            "counts": sens("sens_base_follows_convention"),
            "not_evaluable": "days with no usable prior value under END (null return, NOT_MEASURABLE, guard not reached) whose convention base would be positive and whose flow is non-zero: %d under START, %d under MID; their guard status is not in the copy, so they are not classified and are in no move"
            % (
                res["start"]["base_invalid_days_with_positive_convention_base"],
                res["mid"]["base_invalid_days_with_positive_convention_base"],
            ),
        },
    },
    "limits": [
        "thresholds (guard tolerance, large-flow share) are inferred from the served flags by bracketing, not read from the published method row; the two checks agree and the control reproduces all but 6 days per flag",
        "the base V_(t-1) is held as the code has it; a convention that also changed the base would move more (see sensitivity.base_follows_convention)",
        "the day-pair restatement cannot see an intervening custodian valuation on a skipped day (6 differing days; the sensitivity leaves every skipped-day window as served)",
        "the previous cell left 643 days with a zero START denominator as served; here those keep their served class under START and are restated under MID where the MID denominator is non-zero (so MID differs from the previous cell for those days)",
        "a day whose START or MID return is not defined keeps its served class",
        "the plausibility band gate is applied as the code default to the restated return",
        "no return is written; no figure of any account appears in this record",
    ],
    "the_39": {
        "count": 39,
        "accrual_class": 31,
        "unclassed": 8,
        "statement": "39 of the 90 two-sided segments close under NO timing (31 of the accrual class, 8 unclassed); nothing in this record changes them, and a change of convention would not close the tie-out.",
    },
}
s = json.dumps(rec, indent=1)
assert not re.search(r"\d{8,}", s), re.findall(r".{20}\d{8,}", s)
d = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~129/"
os.makedirs(d, exist_ok=True)
open(d + "GUARD_INTERPLAY.json", "wb").write((s + "\n").encode("ascii"))
print("written", len(s))
