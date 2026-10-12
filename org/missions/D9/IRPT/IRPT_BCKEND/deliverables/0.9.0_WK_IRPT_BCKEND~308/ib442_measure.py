#!/usr/bin/env python3
"""IB-pr-442 measure.  READ ONLY; a SIZING, nothing is re-graded in the product.  Counts only: no account key, balance, quantity or single account's holding or trade is written.

    python -I ib442_measure.py --control
    python -I ib442_measure.py <phase1.pkl> <prep.pkl> <yahoo_cache> <calls.json> <out.json>

Classes, row grading and account-day outcomes follow PRD ADDENDUM v0.39 and the face of IB-pr-442.  The row grade (classify), the account-day order, the sizing claim (new_claim) and
the serving counter are IB-pr-438's (copied; same tolerance, relative 1e-4); the fund-trade classifiers are IB-pr-441's (copied).

ROW (mark m = the row's own price; N = reader's bar of the day; P = of the prior trading day; eq = relative 1e-4):
  no_bar_for_the_day_or_prior  the row's security is not of class admitted_type_with_bars, or N or P is not in the reader's series -> no witness may grade it
  equals_both_unchanged / equals_day_only / equals_prior_day_only / equals_neither
ACCOUNT-DAY, the first that applies: holds_a_security_no_witness_may_grade; admitted_but_one_or_more_at_neither; admitted_but_one_or_more_at_prior_day_only;
freed_every_security_admitted_and_at_the_day_close.
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
import ib429_claims as old  # noqa: E402
import ib429_claims_v035 as v35  # noqa: E402
import ib442_prepare as prep  # noqa: E402

EPOCH = dt.date(1970, 1, 1)
OUTC = ("holds_a_security_no_witness_may_grade", "admitted_but_one_or_more_at_neither", "admitted_but_one_or_more_at_prior_day_only", "freed_every_security_admitted_and_at_the_day_close")
CLAIMS = ("UNGRADEABLE", "ACCT_PRIOR_DATE", "ACCT_OWN_DATE", "NOTHING_TO_GRADE")
WAIT = ("left_out_type_inst", "left_out_type_ric_not_available", "no_type_or_mixed", "another_type_not_admitted", "no_ticker_to_ask_with", "no_bar")
CLASSES = ("admitted_type_with_bars",) + WAIT
SIX = ("same_day_only", "prior_day_only", "next_day_only", "more_than_one", "none", "no_bar")
PRECEDENCE = ("1 no_ticker_to_ask_with (the holdings source states no ticker other than the security's own identifier); then by type (the pair SEC Asset Type / Share Class Type the transactions table states "
              "for its CUSIP; exactly one pair over all its rows = that type, none or more than one = no type): 2 no_type_or_mixed; 3 left_out_type_inst; 4 left_out_type_ric_not_available; "
              "5 another_type_not_admitted; then for an admitted type: 6 no_bar (its ticker returned no bar in the one pass) or 7 admitted_type_with_bars")
ASSUMED = ("A SIZING, not a claim anybody stamped. IF every freed account-day with no other ungradeable kind took the claim its graded rows give (its anchor-graded rows by the anchor as today, "
           "its outside-first-witness rows at the reader's close of the day: so ACCT_OWN_DATE unless an anchor-graded row says ACCT_PRIOR_DATE), and an account-day whose only obstacle is one or more "
           "rows at the prior day's close only (no row of a security no witness may grade, none at neither, no other ungradeable kind) read ACCT_PRIOR_DATE, the four claim counts and the serving rule "
           "would read as below. Every other account-day keeps the claim it has under the cash rule in force. Only securities of the seven admitted pairs are graded by the reader. "
           "Nothing is re-graded in the product.")


# ---- IB-pr-438's row grade, account-day order and sizing claim (copied) ----
def classify(mark, nav_d, nav_p):
    if nav_d is None or nav_p is None:
        return "no_bar_for_the_day_or_prior"
    e_d, e_p, e_n = old.same(mark, nav_d), old.same(mark, nav_p), old.same(nav_d, nav_p)
    if e_d and e_p and e_n:
        return "equals_both_unchanged"
    if e_d and not e_p:
        return "equals_day_only"
    if e_p and not e_d:
        return "equals_prior_day_only"
    return "equals_neither"


def day_outcome(row_outcomes):
    if any(o == "no_bar_for_the_day_or_prior" for o in row_outcomes):
        return OUTC[0]
    if any(o == "equals_neither" for o in row_outcomes):
        return OUTC[1]
    if any(o == "equals_prior_day_only" for o in row_outcomes):
        return OUTC[2]
    return OUTC[3]


def new_claim(c1, row_outcomes, kinds, sixth, outcome):
    other = any(k != "OUTSIDE_ANCHOR" for k in kinds) or sixth
    if other or outcome not in (OUTC[2], OUTC[3]):
        return None
    c2 = collections.Counter(c1)
    n = c2["outside_anchor"]
    assert n == len(row_outcomes), (n, len(row_outcomes))
    c2["outside_anchor"] = 0
    npr = sum(1 for o in row_outcomes if o == "equals_prior_day_only")
    c2["prior"] += npr
    c2["own"] += n - npr
    return v35.claim_v035(c2)[0]


# ---- IB-pr-441's fund-trade classifiers (copied) ----
def same(a, b):
    return abs(a - b) <= 1e-4 * max(abs(a), abs(b))


def cent(a, b):
    return abs(round(a, 2) - round(b, 2)) < 0.005


def classify_trade(price, bars, tdays, i, match):
    if i is None or bars.get(tdays[i]) is None:
        return "no_bar"
    hit = [j for j in (i - 1, i, i + 1) if 0 <= j < len(tdays) and bars.get(tdays[j]) is not None and match(price, bars[tdays[j]])]
    if not hit:
        return "none"
    if len(hit) > 1:
        return "more_than_one"
    return {i - 1: "prior_day_only", i: "same_day_only", i + 1: "next_day_only"}[hit[0]]


def grade_rows(rows, cls_of, nav, d, p):
    """rows: [(security, mark)].  Returns the list of row outcomes: a row of a security not in admitted_type_with_bars has no witness; else classify against the reader's bars."""
    out = []
    for s, mark in rows:
        if cls_of[s] != "admitted_type_with_bars":
            out.append("no_bar_for_the_day_or_prior")
        else:
            out.append(classify(mark, nav[s].get(d), nav[s].get(p)))
    return out


# ---- planted control: three account-days, run through the real class function (sec_class) and the real row / account-day functions ----
def control_run():
    ra = prep.ADMITTED[1]            # an admitted pair
    li = prep.LEFT_INST              # the left-out pair
    cls_of = {"ADM": prep.sec_class("TKA", {ra})[0], "LEFT": prep.sec_class("TKL", {li})[0], "NOTK": prep.sec_class(None, {ra})[0], "MIX": prep.sec_class("TKM", {ra, li})[0]}
    cls_of = {k: ("admitted_type_with_bars" if v == "admitted_type" else v) for k, v in cls_of.items()}
    nav = {"ADM": {"d": 10.0, "p": 9.9}, "LEFT": {"d": 20.0, "p": 19.8}}
    ad1 = day_outcome(grade_rows([("ADM", 10.0)], cls_of, nav, "d", "p"))                      # only an admitted-type security, at the day's close
    ad2 = day_outcome(grade_rows([("ADM", 10.0), ("LEFT", 20.0)], cls_of, nav, "d", "p"))      # the same plus a left-out-type security at the day's close
    ad3 = day_outcome(grade_rows([("ADM", 9.9)], cls_of, nav, "d", "p"))                       # an admitted security at the prior day's close
    sz1 = new_claim({"own": 3, "outside_anchor": 1}, ["equals_day_only"], [], False, ad1)
    sz3 = new_claim({"own": 3, "outside_anchor": 1}, ["equals_prior_day_only"], [], False, ad3)
    return {"classes": cls_of, "account_day_1_admitted_only_at_the_day_close": ad1, "account_day_2_plus_a_left_out_type_at_the_day_close": ad2,
            "account_day_3_admitted_at_the_prior_day_close": ad3, "sizing_claim_of_account_day_1": sz1, "sizing_claim_of_account_day_3": sz3,
            "admitted_security_at_the_day_close_frees_its_day": ad1 == OUTC[3], "left_out_type_does_not_free_its_day": ad2 != OUTC[3] and ad2 == OUTC[0]}


PLANTED = {"classes": {"ADM": "admitted_type_with_bars", "LEFT": "left_out_type_inst", "NOTK": "no_ticker_to_ask_with", "MIX": "no_type_or_mixed"},
           "account_day_1_admitted_only_at_the_day_close": OUTC[3], "account_day_2_plus_a_left_out_type_at_the_day_close": OUTC[0],
           "account_day_3_admitted_at_the_prior_day_close": OUTC[2], "sizing_claim_of_account_day_1": "ACCT_OWN_DATE", "sizing_claim_of_account_day_3": "ACCT_PRIOR_DATE",
           "admitted_security_at_the_day_close_frees_its_day": True, "left_out_type_does_not_free_its_day": True}


def main():
    if sys.argv[1:] == ["--control"]:
        r = control_run()
        print(json.dumps(r, indent=1), "\nEQUAL:", r == PLANTED)
        return 0 if r == PLANTED else 1
    p1f, prepf, ycache, calls_f, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]), Path(sys.argv[5])
    root = HERE.parents[6]
    sys.path[:0] = [str(root / "lib"), str(root), str(root / "data/assets/scripts/silver"), str(root / "data/assets/scripts/analysis")]
    import commonwealth_daily_valuation as dv
    import trading_calendar as tc
    P, R = pickle.load(open(p1f, "rb")), pickle.load(open(prepf, "rb"))
    calls = json.load(open(calls_f))
    graded, prev_of, ad, secs = P["graded"], P["prev_of"], P["ad"], P["secs"]
    sec_ticker, sec_cls0 = R["sec_ticker"], dict(R["sec_cls"])

    def day_int(iso):
        return (dt.date.fromisoformat(iso) - EPOCH).days
    reader_cache = {}

    def series(t):
        if t not in reader_cache:
            s, _ = dv.read_yahoo_close(ycache, t)
            reader_cache[t] = None if s is None else {int(i): float(v) for i, v in s.items()}
        return reader_cache[t]
    # ---- 1. CLASS every security the first witness does not carry
    cls = {}
    for c, k in sec_cls0.items():
        cls[c] = k if k != "admitted_type" else ("admitted_type_with_bars" if series(sec_ticker[c]) else "no_bar")
    cnt = collections.Counter(cls.values())
    admitted_by_type = {p: 0 for p in R["admitted"]}
    for c, k in cls.items():
        if k == "admitted_type_with_bars":
            admitted_by_type[R["sec_pair"][c]] += 1
    nav = {c: series(sec_ticker[c]) for c in secs if sec_ticker[c] and cls[c] == "admitted_type_with_bars"}
    # ---- 2. GRADE each row; place each account-day
    row_out = collections.Counter()
    day_missing_only_prior = 0
    oc_counts, freed_clean, prior_clean = collections.Counter(), 0, 0
    holding_any = {k: 0 for k in WAIT}
    only_on, only_on_clean = {k: 0 for k in WAIT}, {k: 0 for k in WAIT}
    new_claims = {}
    sec_ad = collections.Counter()           # security -> account-days holding it
    for (a, d), r in ad.items():
        dd, pp = day_int(d), day_int(prev_of[d])
        rows = [(cu, pr) for cu, pr in r["rows"]]
        outs = []
        for cu, price in rows:
            if cls[cu] != "admitted_type_with_bars":
                o = "no_bar_for_the_day_or_prior"
            else:
                nd, npp = nav[cu].get(dd), nav[cu].get(pp)
                if nd is not None and npp is None:
                    day_missing_only_prior += 1
                o = classify(price, nd, npp)
            outs.append(o)
            row_out[o] += 1
        oc = day_outcome(outs)
        oc_counts[oc] += 1
        other = any(k != "OUTSIDE_ANCHOR" for k in r["kinds"]) or r["sixth"]
        if oc == OUTC[3] and not other:
            freed_clean += 1
        if oc == OUTC[2] and not other:
            prior_clean += 1
        nc = new_claim(r["c1"], outs, r["kinds"], r["sixth"], oc)
        if nc is not None:
            new_claims[(a, d)] = nc
        held_classes = {cls[cu] for cu, _ in rows}
        for cu in {cu for cu, _ in rows}:
            sec_ad[cu] += 1
        for k in WAIT:
            if k in held_classes:
                holding_any[k] += 1
                # freed if ONLY class k were admitted and graded at the day's close: every row outside class k must already be admitted-with-bars at the day's close (or unchanged)
                if oc != OUTC[3] and all(o in ("equals_day_only", "equals_both_unchanged") for (cu, _), o in zip(rows, outs) if cls[cu] != k):
                    only_on[k] += 1
                    if not other:
                        only_on_clean[k] += 1
    # ---- 3. THE SIZING
    claims = {a: dict(v) for a, v in P["claims_cash"].items()}
    changed = collections.Counter()
    for (a, d), nc in new_claims.items():
        if claims[a][d] != nc:
            changed[(claims[a][d], nc)] += 1
        claims[a][d] = nc
    tally = collections.Counter(v for byday in claims.values() for v in byday.values())
    sv = v35.serve_v035(claims, graded)
    pa = [v for v in sv["per_account"].values() if v[0]]
    ec = P["tally_cash"]
    sizing = {"what_is_assumed": ASSUMED, "account_days": {"present": sum(tally.values()), **{k: tally.get(k, 0) for k in CLAIMS}},
              "claims_moved": {"%s -> %s" % k: v for k, v in sorted(changed.items())},
              "serving_rule": {"eligible": sv["eligible"], "served": sv["served"], "blank": sv["blank"], "blank_share_percent": round(100.0 * sv["blank"] / sv["eligible"], 3),
                               "accounts_never_served": sum(1 for e, s_ in pa if s_ == 0), "accounts_with_eligible_days": len(pa), "accounts_always_served": sum(1 for e, s_ in pa if s_ == e),
                               "blank_by_reason": dict(sv["blank_by_reason"])},
              "rule_in_force": {"basis": "the cash rule of IB-pr-435 (v0.35 names)", "account_days": {"present": ec["present"], **{k: ec.get(k, 0) for k in CLAIMS}},
                                "eligible": P["serve_cash"]["eligible"], "served": P["serve_cash"]["served"], "blank": P["serve_cash"]["blank"],
                                "blank_share_percent": round(100.0 * P["serve_cash"]["blank"] / P["serve_cash"]["eligible"], 3), "accounts_never_served": P["serve_cash"]["never"]},
              "withdrawn_sizing_for_reference_only": {"blank_share_percent": 36.989, "accounts_never_served": 181,
                                                     "meaning": "the v0.37 sizing that counted every fund as graded (IB-pr-438); withdrawn by v0.38"}}
    # ---- the largest no-bar fund: among the outside securities whose ticker was asked and returned no bar, the RIC/BDC ones, most account-days
    asked = {t for c_ in calls for t in c_["ticker_list"]}
    nb = []
    for c in secs:
        t = sec_ticker[c]
        if t and t in asked and not series(t):
            nb.append({"ticker": t, "account_days": sec_ad[c], "type": R["sec_pair"][c] or "NO_TYPE_OR_MIXED", "class": cls[c]})
    nb.sort(key=lambda x: (-x["account_days"], x["ticker"]))
    nb_fund = [x for x in nb if x["type"].startswith(prep.RIC)]
    largest = {"ticker": nb_fund[0]["ticker"], "account_days": nb_fund[0]["account_days"]} if nb_fund else {"ticker": None, "account_days": 0}
    # ---- 6. THE REVIEWER'S TWO POINTS
    fx = [d.isoformat() for d in tc.trading_days_between(dt.date(2026, 6, 5), dt.date(2026, 10, 13))]
    fi = {d: i for i, d in enumerate(fx)}

    def bars_iso(t):
        s = series(t) if t else None
        return None if not s else {(EPOCH + dt.timedelta(days=k)).isoformat(): v for k, v in s.items()}
    trades = R["inside"]
    assert len({t["id"] for t in trades}) == len(trades)
    bcache = {}
    res, res_c = [], []
    for t in trades:
        if t["ticker"] not in bcache:
            bcache[t["ticker"]] = bars_iso(t["ticker"])
        b = bcache[t["ticker"]] or {}
        i = fi.get(t["trade"])
        res.append(classify_trade(t["price"], b, fx, i, same))
        res_c.append(classify_trade(t["price"], b, fx, i, cent))
    tot, tot_c = collections.Counter(res), collections.Counter(res_c)
    nxt = []
    for t, o in zip(trades, res_c):
        if o == "next_day_only":
            b, i = bcache[t["ticker"]], fi[t["trade"]]
            nxt.append({"ticker": t["ticker"], "trade_date": t["trade"], "kind": "%s / %s" % (t["kind"], t["sub"]), "price": t["price"], "bar_prior": b.get(fx[i - 1]), "bar_day": b.get(fx[i]),
                        "bar_next": b.get(fx[i + 1]), "fund_pair": R["fund_pair"][t["cusip"]]})
    nxt.sort(key=lambda x: (x["trade_date"], x["ticker"]))
    by_pair_tr, by_pair_out, by_pair_out_c, by_pair_funds = collections.Counter(), {}, {}, collections.defaultdict(set)
    for t, o, oc_ in zip(trades, res, res_c):
        pr_ = R["fund_pair"][t["cusip"]]
        by_pair_tr[pr_] += 1
        by_pair_funds[pr_].add(t["cusip"])
        by_pair_out.setdefault(pr_, collections.Counter())[o] += 1
        by_pair_out_c.setdefault(pr_, collections.Counter())[oc_] += 1
    funds_total = len({t["cusip"] for t in trades})
    reviewer = {"next_day_only_to_the_cent": nxt, "next_day_only_to_the_cent_count": len(nxt),
                "next_day_only_to_the_cent_note": "the count is %d (IB-pr-441 counted 3)" % len(nxt) + ("" if len(nxt) == 3 else "; it differs from 3, see the read"),
                "tolerance_note": "the six outcomes are IB-pr-441's: the trade's Price against the reader's bar for the trade date and the trading day either side; relative 1e-4, and to the cent (both rounded to 2 decimals equal)",
                "trades_total": len(trades), "funds_total": funds_total,
                "totals_relative_1e-4": {k: tot.get(k, 0) for k in SIX}, "totals_to_the_cent": {k: tot_c.get(k, 0) for k in SIX},
                "ib441_totals_relative_1e-4": {"same_day_only": 4490, "next_day_only": 0, "prior_day_only": 28, "more_than_one": 1102, "none": 245, "no_bar": 284},
                "trades_by_fund_pair": dict(sorted(by_pair_tr.items())),
                "funds_by_fund_pair": {k: len(v) for k, v in sorted(by_pair_funds.items())},
                "outcomes_by_fund_pair": {k: {"funds": len(by_pair_funds[k]), "trades": by_pair_tr[k], **{o: by_pair_out[k].get(o, 0) for o in SIX}} for k in sorted(by_pair_tr)},
                "outcomes_by_fund_pair_to_the_cent": {k: {"funds": len(by_pair_funds[k]), "trades": by_pair_tr[k], **{o: by_pair_out_c[k].get(o, 0) for o in SIX}} for k in sorted(by_pair_tr)}}
    # ---- control + fetch record
    ctl = control_run()
    fetch = {"calls": [{"call": c["call"], "tickers": c["tickers"], "with_bars": c["with_bars"], "no_bars": c["no_bars"], "rate_limited_not_read": c["rate_limited_not_read"]} for c in calls],
             "call_count": len(calls), "distinct_tickers_asked": sum(c["tickers"] for c in calls),
             "tickers_asked_more_than_once": sum(c["tickers"] for c in calls) - len({t for c in calls for t in c["ticker_list"]}),
             "tickers_with_bars": sum(c["with_bars"] for c in calls), "tickers_with_no_bars": sum(c["no_bars"] for c in calls),
             "of_which": {"tickers_of_admitted_type_securities_outside_the_first_witness": len({sec_ticker[c] for c in secs if sec_cls0[c] == "admitted_type"}),
                          "fund_tickers_of_the_priced_fund_trades": len(set(R["fund_ticker"].values()) & {t["ticker"] for t in trades}),
                          "in_both_lists": len({sec_ticker[c] for c in secs if sec_cls0[c] == "admitted_type"} & {t["ticker"] for t in trades})},
             "window": "2026-06-05 to 2026-10-13 (end exclusive 2026-10-14)", "pause_between_calls_seconds": 8, "reader_internal_pause_seconds": 6, "parallel_calls": 0,
             "reader": "fetch_yahoo (data/assets/scripts/silver/commonwealth_price_basis_census.py) / read_yahoo_close (data/assets/scripts/silver/commonwealth_daily_valuation.py), neither edited; unadjusted Close"}
    same_days = {k: ec.get(k, 0) for k in CLAIMS} == {"UNGRADEABLE": 43310, "ACCT_PRIOR_DATE": 55, "ACCT_OWN_DATE": 19832, "NOTHING_TO_GRADE": 13599} and ec["present"] == 76796
    doc = {
        "same_account_days_read": bool(same_days and P["same_cash"]),
        "same_account_days_read_basis": "this run's totals under the cash rule: %s; IB-pr-438's: UNGRADEABLE 43,310; ACCT_PRIOR_DATE 55; ACCT_OWN_DATE 19,832; NOTHING_TO_GRADE 13,599; present 76,796" % dict(ec),
        "graded_days": len(graded), "first_graded_day": graded[0], "last_graded_day": graded[-1],
        "admitted_types": R["admitted"], "class_precedence": PRECEDENCE,
        "securities_outside_the_first_witness": {"total": len(secs), **{k: cnt.get(k, 0) for k in CLASSES},
                                                 "basis": "the securities behind an OUTSIDE_ANCHOR row under the cash rule in force (IB-pr-438 counted 737)"},
        "admitted_by_type": admitted_by_type,
        "other_pairs_not_admitted": R["other_pairs"], "no_type_or_mixed_combinations": R["mixed_combos"],
        "type_join": {"domain": "the %d securities the first witness does NOT carry (IB-pr-441 joined the 894 both witnesses carry: a different set)" % len(secs),
                      **{k: R["join"].get(k, 0) for k in ("found_one_pair", "found_no_row", "found_more_than_one_pair")},
                      "of_those_with_a_ticker": {k: R["join_with_ticker"].get(k, 0) for k in ("found_one_pair", "found_no_row", "found_more_than_one_pair")},
                      "how": "all de-duplicated (TransactionID) transaction rows of the CUSIP, any kind and date; one pair = that type; none = no row; more than one = MIXED",
                      "transactions_read": {"partitions": len(R["tx_meta"]["partitions"]), "objects": R["tx_meta"]["objects"], "rows_read": R["tx_meta"]["rows_read"], "distinct_transaction_ids": R["tx_distinct_ids"]}},
        "fetch": fetch,
        "account_day_effect": {"account_days_holding_such_a_security": len(ad), **{k: oc_counts[k] for k in OUTC}, "freed_and_holding_no_other_ungradeable_kind": freed_clean,
                               "at_prior_day_only_and_holding_no_other_ungradeable_kind": prior_clean,
                               "no_other_ungradeable_kind_means": "no NO_CUSIP, NEITHER_CLOSE or NEGATIVE_POSITION kind (after the cash rule) and no sixth-reason row on the account-day",
                               "basis_check": "IB-pr-438 counted 34,789 account-days holding an outside-first-witness row; this run: %d" % len(ad),
                               "rows": dict(row_out), "rows_with_a_day_bar_but_no_prior_bar_counted_as_no_bar": day_missing_only_prior},
        "sizing_under_v039": sizing,
        "still_waiting": {"account_days_holding_any": holding_any, "account_days_waiting_only_on": only_on,
                          "account_days_waiting_only_on_and_holding_no_other_ungradeable_kind": only_on_clean,
                          "waiting_only_on_is": "an UPPER BOUND: the account-days not freed today that WOULD be freed if that ONE class were admitted and graded at the day's close (every one of its rows of that class taken to sit at the day's close), every other row unchanged; an account-day counts under every class it holds in holding_any",
                          "largest_no_bar_fund": largest, "no_bar_securities_by_account_days_top": nb[:10]},
        "reviewer_points": reviewer,
        "control": {"planted": PLANTED, "read": ctl, "equal": ctl == PLANTED,
                    "what_it_is": "three planted account-days run through the real class function and the real row / account-day / sizing functions: an admitted-type security at the day's close (freed), the same plus a left-out-type security at the day's close (not freed), an admitted security at the prior day's close (blocked, prior day only)"},
        "claims_regraded_in_product": False, "other_sources_asked": 0,
    }
    out.write_text(json.dumps(doc, indent=1, default=str), encoding="utf-8")
    print("wrote", out, "classes", dict(cnt), "outcomes", dict(oc_counts), "freed_clean", freed_clean, "control equal", ctl == PLANTED)
    print("serve", sizing["serving_rule"]["eligible"], sizing["serving_rule"]["served"], sizing["serving_rule"]["blank"], sizing["serving_rule"]["blank_share_percent"], sizing["serving_rule"]["accounts_never_served"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
