#!/usr/bin/env python3
"""IB-pr-452 measure.  READ ONLY; counts only: no account key, balance or single account's holding is written.  Nothing is re-graded in the product, no class admitted or excluded.

    python -I ib452_measure.py --control
    python -I ib452_measure.py <phase1.pkl> <prep442.pkl> <yahoo_cache> <calls.json> <meta.json> <ib142_record.json> <out.json>

The sizing code is IB-pr-445's (ib445_measure.sizing, copied and generalised to a set of admitted classes, a guard mode and a set of securities the second witness does not
grade): same row grade (ib442_measure.classify), account-day order, sizing claim and serving counter (imported unchanged), same price rule, tolerance, trading-day axis.

GUARD MODES.  "first": guard sentence (1) ALONE, IB-pr-445's own function (m445.grade_row).  "both": the PRODUCT function second_witness_grades(bars, t)
(data/assets/scripts/gold/irpt_reporting/second_witness_guard.py, imported, not reproduced): a positive bar for t, a positive bar for the calendar's prior trading day, and the two
differ by more than the relative tolerance 1e-4; otherwise the row gets no grade and blocks its account-day exactly as a row with no bar.
"""
from __future__ import annotations

import collections
import datetime as dt
import json
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ib441_measure as m441  # noqa: E402
import ib442_measure as m442  # noqa: E402
import ib445_measure as m445  # noqa: E402
import ib429_claims_v035 as v35  # noqa: E402

ROOT = HERE.parents[6]
sys.path[:0] = [str(ROOT / "lib"), str(ROOT), str(ROOT / "data/assets/scripts/silver"), str(ROOT / "data/assets/scripts/analysis"),
                str(ROOT / "data/assets/scripts/gold/irpt_reporting")]
import second_witness_guard as swg  # noqa: E402  the product function

EPOCH = dt.date(1970, 1, 1)
CLAIMS = m442.CLAIMS
OUTC = m442.OUTC
NOBAR = "no_bar_for_the_day_or_prior"
same = m441.same
RIC = "Securities Issued by Registered Investment Companies or Business Development Companies"
SEVEN_AND_INST_CLASSES = ("admitted_type", "left_out_type_inst")
NINE_CLASSES = ("admitted_type", "left_out_type_inst", "left_out_type_ric_not_available")
FIVE = ["ADLYX", "BISOX", "EIBLX", "GPPIX", "OLCYX"]
GUARD_USED = ("the PRODUCT function: second_witness_grades(bars, t) in data/assets/scripts/gold/irpt_reporting/second_witness_guard.py, imported and called for every row and every "
              "security-day of the sizings and of the repeat count (its three conditions: a positive bar for t; a positive bar for the calendar's prior trading day; the two differ by more "
              "than the relative tolerance 1e-4). The reproduction under guard sentence (1) alone uses IB-pr-445's own function (ib445_measure.grade_row with relative 1e-4), unchanged.")
RULE_IN_WORDS = ("For a security of one of the nine admitted pairs that is OUTSIDE the first witness (it sits behind an OUTSIDE_ANCHOR row of the sizing's account-days) and has at least one bar, "
                 "take the 85 graded days (2026-06-10 to 2026-10-09). days_with_a_bar = the graded days on which the reader (Yahoo Finance unadjusted Close) has a positive bar for the day. "
                 "days_not_graded = those days on which the guard (the product function second_witness_grades, both sentences: no grade where the bar equals the prior trading day's bar within "
                 "relative 1e-4, and no grade where there is no bar for the calendar's prior trading day) gives no grade. The security repeats on more than half its days when "
                 "2 * days_not_graded > days_with_a_bar. A security the first witness also carries on some days counts as outside it when it has an OUTSIDE_ANCHOR row on some graded day "
                 "(the cell's own definition of the sizing population).")
ASSUMED = ("A SIZING, not a stamp: IF every account-day that holds, outside the first witness, only securities graded by the second witness at the day's close took the claim its rows give "
           "(IB-pr-442's rule, imported unchanged), with the guard's two sentences (no grade where the reader's bar equals its bar for the prior trading day; no grade where it has no bar for the "
           "calendar's prior trading day) and, in the second sizing, with five named securities given no grade on any day, the claim counts and the serving rule would read as below; every "
           "other account-day keeps the claim it has under the cash rule in force, and nothing is re-graded, admitted or excluded in the product.")
NOT_ESTABLISHED = [
    "Whether the nine pairs should be admitted, or any security excluded: this cell sizes and recommends nothing.",
    "Whether the moved days of the five securities (ADLYX, BISOX, EIBLX, GPPIX, OLCYX) are dated right: no anchor close exists for them, so nothing here checks the date of a moved bar.",
    "Why the reader's bar repeats (a stale feed, a fund that does not move, or a late publication): the counts cannot tell them apart.",
    "That the claims counted as freed would be correct: freed account-days are a count of account-days no witness is barred from grading, not a check that the claim is right.",
    "Anything outside the 85 graded days (2026-06-10 to 2026-10-09) or outside the 303 tickers asked; securities with no ticker, no type or mixed types, or another type are not graded and are not counted in the repeat list.",
    "Securities for which the reader returned nothing are not graded (their rows block the account-day); the count is in fetch.tickers_with_no_bars.",
    "The second sentence's cost is read from rows of the sizing's population only; a security-day nobody holds is counted in the repeat list, not in any cost.",
]


def day_iso(n):
    return (EPOCH + dt.timedelta(days=int(n))).isoformat()


# ------------------------------------------------------------------ the row grade (the function the real run and the control both use)
def row_outcome(price, bars, t, prev, ticker, mode, not_graded):
    """bars {datetime.date: close}; t, prev dates; -> the row outcome of ib442_measure.classify or NOBAR when the second witness gives no grade."""
    if ticker in not_graded:
        return NOBAR
    if mode == "first":
        o = m445.grade_row(price, bars.get(t), bars.get(prev), same)
        return NOBAR if o == m445.GUARD else o          # a guard-ungraded row is a row no witness may grade (ib445_measure.day_outcome's own mapping)
    if not swg.second_witness_grades(bars, t):
        return NOBAR
    return m442.classify(price, bars[t], bars[prev])


# ------------------------------------------------------------------ the control
def control_run():
    """Planted: security S (an admitted pair) moves 10 -> 11 on the second day, repeats on the third, moves again on the fourth; real trading days of the calendar.
    An account-day holding S on a moved day is freed with S graded and NOT freed when S is in the not-graded list; on the repeated day it is not freed either way;
    a security with no bar for the prior trading day is not graded on the day after the gap."""
    d = [dt.date(2026, 7, 6), dt.date(2026, 7, 7), dt.date(2026, 7, 8), dt.date(2026, 7, 9), dt.date(2026, 7, 10)]
    bars = {d[0]: 10.0, d[1]: 11.0, d[2]: 11.0, d[3]: 12.0, d[4]: 13.0}
    gap = {d[0]: 10.0, d[2]: 11.0, d[3]: 12.0}              # no bar on d[1]: d[2] has none for its prior trading day

    def freed(price, b, t, prev, tk, ng, mode="both"):
        o = row_outcome(price, b, t, prev, tk, mode, ng)
        return {"row": o, "freed": m442.day_outcome([o]) == OUTC[3]}
    return {"moved_day_security_graded": freed(11.0, bars, d[1], d[0], "SECA", set()),
            "moved_day_security_in_the_not_graded_list": freed(11.0, bars, d[1], d[0], "SECA", {"SECA"}),
            "repeated_day_security_graded": freed(11.0, bars, d[2], d[1], "SECA", set()),
            "moved_day_after_the_repeat_security_graded": freed(12.0, bars, d[3], d[2], "SECA", set()),
            "day_after_a_missing_bar": freed(11.0, gap, d[2], d[1], "SECA", set()),
            "day_after_a_missing_bar_under_sentence_one_alone": freed(11.0, gap, d[2], d[1], "SECA", set(), "first")}


PLANTED = {"moved_day_security_graded": {"row": "equals_day_only", "freed": True},
           "moved_day_security_in_the_not_graded_list": {"row": NOBAR, "freed": False},
           "repeated_day_security_graded": {"row": NOBAR, "freed": False},
           "moved_day_after_the_repeat_security_graded": {"row": "equals_day_only", "freed": True},
           "day_after_a_missing_bar": {"row": NOBAR, "freed": False},
           "day_after_a_missing_bar_under_sentence_one_alone": {"row": NOBAR, "freed": False}}


# ------------------------------------------------------------------ main
def main():
    if sys.argv[1:] == ["--control"]:
        r = control_run()
        print(json.dumps(r, indent=1), "\nEQUAL:", r == PLANTED)
        return 0 if r == PLANTED else 1
    p1f, p442f, ycache, calls_f, meta_f, prior_f, out = sys.argv[1:8]
    import commonwealth_daily_valuation as dv
    P = pickle.load(open(p1f, "rb"))
    R = pickle.load(open(p442f, "rb"))
    calls = json.load(open(calls_f))
    meta = json.load(open(meta_f))
    prior = json.load(open(prior_f, encoding="utf-8"))["sizings"]["seven_types_and_inst_under_the_guard"]
    graded_p, prev_of, ad, secs = P["graded"], P["prev_of"], P["ad"], P["secs"]
    sec_t2, sec_cls0, pair_of = R["sec_ticker"], dict(R["sec_cls"]), R["sec_pair"]

    sers = {}

    def series(t):                       # {int day: close}, or None when the ticker returned nothing
        if t not in sers:
            s, _ = dv.read_yahoo_close(ycache, t)
            sers[t] = None if s is None else {int(k): float(v) for k, v in s.items()}
        return sers[t]
    bars_of = {}
    for c in secs:
        s = series(sec_t2[c]) if sec_t2[c] else None
        bars_of[c] = {EPOCH + dt.timedelta(days=k): v for k, v in s.items()} if s else {}
    d_of = {d: dt.date.fromisoformat(d) for d in graded_p}
    prev_d = {d: dt.date.fromisoformat(prev_of[d]) for d in graded_p}
    # the calendar's prior trading day, read by the product function, must be the phase-1 axis's
    import trading_calendar as tc
    assert all(tc.prev_trading_day(d_of[d]) == prev_d[d] for d in graded_p)

    def sizing(admitted_classes, mode, not_graded):
        cls = {}
        for c, k in sec_cls0.items():
            cls[c] = ("admitted_type_with_bars" if bars_of.get(c) else "no_bar") if k in admitted_classes else k
        row_out, oc_counts, freed_clean = collections.Counter(), collections.Counter(), 0
        new_claims = {}
        for (a, d), r in ad.items():
            outs = []
            for cu, price in r["rows"]:
                if cls[cu] != "admitted_type_with_bars":
                    o = NOBAR
                else:
                    o = row_outcome(price, bars_of[cu], d_of[d], prev_d[d], sec_t2[cu], mode, not_graded)
                outs.append(o)
                row_out[o] += 1
            oc = m442.day_outcome(outs)
            oc_counts[oc] += 1
            other = any(k != "OUTSIDE_ANCHOR" for k in r["kinds"]) or r["sixth"]
            if oc == OUTC[3] and not other:
                freed_clean += 1
            nc = m442.new_claim(r["c1"], outs, r["kinds"], r["sixth"], oc)
            if nc is not None:
                new_claims[(a, d)] = nc
        claims = {a: dict(v) for a, v in P["claims_cash"].items()}
        for (a, d), nc in new_claims.items():
            claims[a][d] = nc
        tally = collections.Counter(v for byday in claims.values() for v in byday.values())
        sv = v35.serve_v035(claims, graded_p)
        pa = [v for v in sv["per_account"].values() if v[0]]
        return {"account_days": {"present": sum(tally.values()), **{k: tally.get(k, 0) for k in CLAIMS}},
                "serving_rule": {"eligible": sv["eligible"], "served": sv["served"], "blank": sv["blank"],
                                 "blank_share_percent": round(100.0 * sv["blank"] / sv["eligible"], 4),
                                 "accounts_never_served": sum(1 for e, s_ in pa if s_ == 0)},
                "freed_and_holding_no_other_ungradeable_kind": freed_clean,
                "account_day_outcomes": {k: oc_counts[k] for k in OUTC}, "row_outcomes": dict(row_out)}

    # 1. reproduce IB-pr-445: seven pairs plus Inst, sentence (1) alone
    rep = sizing(SEVEN_AND_INST_CLASSES, "first", set())
    rep_sr = dict(rep["serving_rule"], blank_share_percent=round(100.0 * rep["serving_rule"]["blank"] / rep["serving_rule"]["eligible"], 3))
    reproduces = (rep["account_days"] == prior["account_days"] and rep_sr == prior["serving_rule"] and
                  rep["freed_and_holding_no_other_ungradeable_kind"] == prior["freed_and_holding_no_other_ungradeable_kind"])
    reproduction = {"reproduces": bool(reproduces),
                    "read": {"account_days": rep["account_days"], "serving_rule": rep_sr,
                             "freed_and_holding_no_other_ungradeable_kind": rep["freed_and_holding_no_other_ungradeable_kind"]},
                    "expected": {"account_days": prior["account_days"], "serving_rule": prior["serving_rule"],
                                 "freed_and_holding_no_other_ungradeable_kind": prior["freed_and_holding_no_other_ungradeable_kind"]},
                    "expected_source": "IB-pr-445's record, org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~303/IB142-1_unmoved_bar_guard.json, sizings.seven_types_and_inst_under_the_guard",
                    "guard_sentence_applied": "(1) alone: ib445_measure.grade_row, relative 1e-4"}
    print("reproduces", reproduces, rep_sr, rep["account_days"], rep["freed_and_holding_no_other_ungradeable_kind"], flush=True)
    if not reproduces:
        Path(out).write_text(json.dumps({"reproduces_ib_pr_445_seven_and_inst_first_sentence_only": reproduction}, indent=1), encoding="utf-8")
        print("DOES NOT REPRODUCE: stop")
        return 2

    # 2. nine pairs: sentence (1) alone (for the second sentence's cost), both sentences, and with the five not graded
    nine_first = sizing(NINE_CLASSES, "first", set())
    nine_both = sizing(NINE_CLASSES, "both", set())
    nine_five = sizing(NINE_CLASSES, "both", set(FIVE))
    cost2 = nine_first["freed_and_holding_no_other_ungradeable_kind"] - nine_both["freed_and_holding_no_other_ungradeable_kind"]
    second_sentence = {
        "second_sentence_cost_in_freed_account_days": cost2,
        "freed_nine_pairs_under_sentence_one_alone": nine_first["freed_and_holding_no_other_ungradeable_kind"],
        "freed_nine_pairs_under_both_sentences": nine_both["freed_and_holding_no_other_ungradeable_kind"],
        "account_days_ungradeable_nine_pairs_sentence_one_alone": nine_first["account_days"]["UNGRADEABLE"],
        "account_days_ungradeable_nine_pairs_both_sentences": nine_both["account_days"]["UNGRADEABLE"],
        "blank_share_percent_nine_pairs_sentence_one_alone": round(100.0 * nine_first["serving_rule"]["blank"] / nine_first["serving_rule"]["eligible"], 4),
        "accounts_never_served_nine_pairs_sentence_one_alone": nine_first["serving_rule"]["accounts_never_served"],
        "why": ("In the sizing a row is graded only against a positive bar for the day AND for the prior trading day (ib442_measure.classify returns no_bar_for_the_day_or_prior when either is "
                "missing), so the no-prior-bar sentence is already how rows were blocked under sentence (1) alone; the cost is the difference this run measures, not an assumption.")}
    sz = {"nine_pairs_under_both_guard_sentences": {k: v for k, v in nine_both.items()},
          "nine_pairs_with_the_five_not_graded": {k: v for k, v in nine_five.items()}}

    # 3. the five's cost
    five_secs = {t: [c for c in secs if sec_t2[c] == t] for t in FIVE}
    by_ticker = {}
    for t in FIVE:
        cs = set(five_secs[t])
        rows = 0
        accts = set()
        graded_rows = 0
        for (a, d), r in ad.items():
            for cu, _ in r["rows"]:
                if cu in cs:
                    rows += 1
                    accts.add(a)
                    graded_rows += 1 if swg.second_witness_grades(bars_of[cu], d_of[d]) else 0
        by_ticker[t] = {"row_days": rows, "accounts_holding_it": len(accts), "row_days_the_guard_grades_under_both_sentences": graded_rows}
    five_cost = {"account_days_no_longer_freed": nine_both["freed_and_holding_no_other_ungradeable_kind"] - nine_five["freed_and_holding_no_other_ungradeable_kind"],
                 "accounts_no_longer_ever_served": nine_five["serving_rule"]["accounts_never_served"] - nine_both["serving_rule"]["accounts_never_served"],
                 "row_days_of_the_five": sum(v["row_days"] for v in by_ticker.values()),
                 "by_ticker": by_ticker,
                 "basis": "freed = freed_and_holding_no_other_ungradeable_kind; accounts_no_longer_ever_served = accounts_never_served with the five not graded less the same with them graded; counts only"}

    # 4. securities of the nine pairs outside the first witness that have bars: repeating on more than half their days
    pair_names = sorted(R["admitted"]) + [RIC + " / Inst", RIC + " / Not Available"]
    rows_by_sec = collections.Counter(cu for r in ad.values() for cu, _ in r["rows"])
    by_pair = {p: {"securities_outside_the_first_witness_with_bars": 0, "repeating_on_more_than_half": 0} for p in pair_names}
    listed = []
    for c in sorted(secs, key=lambda c: (pair_of[c] or "", sec_t2[c] or "")):
        if sec_cls0[c] not in NINE_CLASSES or not bars_of[c]:
            continue
        p = pair_of[c]
        wb = ng = 0
        for d in graded_p:
            if swg._bar(bars_of[c], d_of[d]) is None:
                continue
            wb += 1
            ng += 0 if swg.second_witness_grades(bars_of[c], d_of[d]) else 1
        if wb == 0:
            continue
        by_pair[p]["securities_outside_the_first_witness_with_bars"] += 1
        if 2 * ng > wb:
            by_pair[p]["repeating_on_more_than_half"] += 1
            listed.append({"ticker": sec_t2[c], "pair": p, "days_with_a_bar": wb, "days_not_graded": ng, "row_days": rows_by_sec[c]})
    listed.sort(key=lambda x: (-x["days_not_graded"] / x["days_with_a_bar"], x["ticker"]))
    in_list = {x["ticker"] for x in listed}
    five_not_listed = {}
    for t in FIVE:
        if t not in in_list:
            (c,) = five_secs[t]
            wb = sum(1 for d in graded_p if swg._bar(bars_of[c], d_of[d]) is not None)
            ng = sum(1 for d in graded_p if swg._bar(bars_of[c], d_of[d]) is not None and not swg.second_witness_grades(bars_of[c], d_of[d]))
            five_not_listed[t] = "days_with_a_bar %d, days_not_graded %d: not more than half" % (wb, ng)
    # JSOSX
    js = [c for c in secs if sec_t2[c] == "JSOSX"]
    jsosx = {"in_the_sizing_population_outside_the_first_witness": bool(js)}
    if js:
        c = js[0]
        jsosx.update({"pair": pair_of[c], "class": sec_cls0[c], "in_the_repeat_list": "JSOSX" in in_list,
                      "row_days_in_the_sizing_population": rows_by_sec[c],
                      "stands": ("JSOSX counts as outside the first witness on this cell's rule (it has an OUTSIDE_ANCHOR row on some graded day, %d row-days, so it is in the sizing's population) although the "
                                 "anchor carries it on most days (row IRPT_BCKEND-D2-W306-S1); it is %s the repeat list." % (rows_by_sec[c], "in" if "JSOSX" in in_list else "not in"))})
    repeat = {"rule_in_words": RULE_IN_WORDS, "by_pair": by_pair, "total": len(listed), "securities": listed,
              "securities_outside_the_first_witness_with_bars_total": sum(v["securities_outside_the_first_witness_with_bars"] for v in by_pair.values()),
              "jsosx": jsosx}
    if five_not_listed:
        repeat["of_the_five_not_listed_explained"] = five_not_listed

    # 5. fetch and control
    ticks = [t for c_ in calls for t in c_["ticker_list"]]
    fetch = {"call_count": len(calls), "distinct_tickers_asked": len(set(ticks)), "tickers_asked_in_all": len(ticks),
             "tickers_asked_more_than_once": len([t for t, n in collections.Counter(ticks).items() if n > 1]),
             "tickers_with_bars": sum(c_["with_bars"] for c_ in calls), "tickers_with_no_bars": sum(c_["no_bars"] for c_ in calls),
             "rate_limited_not_read": sum(c_["rate_limited_not_read"] for c_ in calls), "tickers_per_call": [c_["tickers"] for c_ in calls],
             "counted_before_fetching": True, "counted": meta, "stop_above": 1500,
             "window": "2026-06-05 to 2026-10-13 (end exclusive 2026-10-14)", "pause_between_calls_seconds": 8, "parallel_calls": 0,
             "reader": "fetch_yahoo (data/assets/scripts/silver/commonwealth_price_basis_census.py) / read_yahoo_close (data/assets/scripts/silver/commonwealth_daily_valuation.py), neither edited; unadjusted Close"}
    ctl = control_run()
    pairs_admitted = sorted(R["admitted"]) + [RIC + " / Inst", RIC + " / Not Available"]
    assert len(pairs_admitted) == 9 and sorted(pairs_admitted) == sorted(by_pair)
    doc = {"reproduces_ib_pr_445_seven_and_inst_first_sentence_only": reproduction,
           "pairs_admitted": pairs_admitted, "guard_used": GUARD_USED,
           "sizings": sz, "second_sentence_cost_in_freed_account_days": cost2, "second_sentence": second_sentence,
           "the_five_not_graded": list(FIVE), "the_five_cost": five_cost,
           "repeating_on_more_than_half_their_days": repeat,
           "fetch": fetch,
           "control": {"planted": PLANTED, "read": ctl,
                       "what_it_is": ("planted trading days of the calendar: a security of an admitted pair whose bar moves, repeats, moves again, and a gap; an account-day holding it on a moved day "
                                      "is freed with the security graded and NOT freed when it is in the not-graded list; on the repeated day and on the day after a missing bar it is not freed. "
                                      "Run through row_outcome / day_outcome, the functions the real run uses.")},
           "claims_regraded_in_product": 0, "classes_admitted_by_this_cell": 0, "securities_excluded_by_this_cell": 0, "other_sources_asked": 0,
           "what_is_assumed": ASSUMED, "not_established": NOT_ESTABLISHED}
    Path(out).write_text(json.dumps(doc, indent=1), encoding="utf-8")
    print("wrote", out, "control equal", ctl == PLANTED)
    for k, v in sz.items():
        print(k, v["account_days"], v["serving_rule"], v["freed_and_holding_no_other_ungradeable_kind"])
    print("second sentence cost", second_sentence)
    print("five cost", five_cost)
    print("repeat", repeat["total"], by_pair)
    print("jsosx", jsosx)
    return 0


if __name__ == "__main__":
    sys.exit(main())
