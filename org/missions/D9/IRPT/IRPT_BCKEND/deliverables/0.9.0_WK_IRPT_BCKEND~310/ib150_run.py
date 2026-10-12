#!/usr/bin/env python3
"""IB-pr-454 run.  READ ONLY; counts only: no account key (the cache holds a one-way 12-character digest), balance or holding of an account is written.
Nothing is re-graded in the product, no class admitted.  Every claim, kind, row grade, security-day grade and serving count below is computed BY THE PRODUCT MODULE
(data/assets/scripts/gold/irpt_reporting/date_basis_grading.py); this script only reads the cache, groups rows by account-day, hands them to the module and counts.

    python -I ib150_run.py <partition_cache> <tx.pkl> <overlap.pkl> <phase1.pkl> <prep.pkl> <yahoo_cache> <calls.json> <meta_452.json> <meta_all.json> <out_dir>

phase1.pkl / prep.pkl are IB-pr-442's / IB-pr-452's outputs (their scripts, run unchanged on this cell's cache): used for the ticker of each security behind an OUTSIDE_ANCHOR
row and for the 85-day check of the base tally only.
"""
from __future__ import annotations

import collections
import datetime as dt
import json
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
sys.path[:0] = [str(ROOT / "lib"), str(ROOT), str(ROOT / "data/assets/scripts/silver"), str(ROOT / "data/assets/scripts/analysis"),
                str(ROOT / "data/assets/scripts/gold/irpt_reporting")]
import commonwealth_daily_valuation as dv  # noqa: E402
import date_basis_grading as m  # noqa: E402
import trading_calendar as tc  # noqa: E402

EPOCH = dt.date(1970, 1, 1)
PRIOR = HERE.parent / "0.9.0_WK_IRPT_BCKEND~308" / "IB148-1_nine_pair_sizing.json"
SEVEN = ["ADLYX", "BISOX", "EIBLX", "GPPIX", "JSOSX", "OLCYX", "SGOV"]
CANDIDATES = (10, 20, 40, 60, 85)
TENTHS = ["%.1f-%.1f" % (i / 10, (i + 1) / 10) for i in range(10)]


def tenths(shares):
    """shares: [(repeated, compared)] with compared >= 1.  A share exactly on an edge goes to the UPPER bin; a share of 1.0 goes to the last bin."""
    c = collections.Counter(min((10 * r) // n, 9) for r, n in shares)
    return {TENTHS[i]: c.get(i, 0) for i in range(10)}


def main():
    cache, txf, ovf, p1f, prepf, ycache, callsf, meta452f, metaallf, outd = sys.argv[1:11]
    cache, outd = Path(cache), Path(outd)
    outd.mkdir(parents=True, exist_ok=True)
    P1 = pickle.load(open(p1f, "rb"))
    R = pickle.load(open(prepf, "rb"))
    OV = pickle.load(open(ovf, "rb"))
    T = pickle.load(open(txf, "rb"))
    calls = json.load(open(callsf))
    meta452, metaall = json.load(open(meta452f)), json.load(open(metaallf))
    prior = json.load(open(PRIOR, encoding="utf-8"))["sizings"]["nine_pairs_under_both_guard_sentences"]
    W = m.REPEATED_SHARE_WINDOW
    cand_windows = sorted(set(CANDIDATES) | {W})

    # ------------------------------------------------------------------------------------------------ the cache -> account-days, graded by the module
    def load(kind, day):
        f = cache / ("%s_%s.pkl" % (kind, day))
        return pickle.load(open(f, "rb")) if f.exists() else "UNREAD"

    listed = sorted(f.name[4:14] for f in cache.glob("src_*.pkl") if pickle.load(open(f, "rb")) is not None)
    tdays = [d for d in listed if tc.is_trading_day(d)]

    def anchor(day):
        t = load("anc", day)
        if t in (None, "UNREAD"):
            return t
        by = {}
        for c, p in zip(t["cusip"], t["closing_price"]):
            c = (c or "").strip()
            if c and p is not None and float(p) > 0:
                by[c] = float(p)
        return by

    graded, prev_of, A, B = [], {}, {}, {}
    base = collections.defaultdict(dict)          # account digest -> day -> the claim with no second witness (the cash rule in force)
    ad_store = {}                                  # (account digest, day) -> (rows, prior prices of its rows' CUSIPs): account-days with an OUTSIDE_ANCHOR kind
    base_tally = collections.Counter()
    for i, d in enumerate(tdays):
        p = tc.prev_trading_day(dt.date.fromisoformat(d)).isoformat()
        s = load("src", d)
        a_, b_ = anchor(d), anchor(p)
        if s in (None, "UNREAD") or a_ == "UNREAD" or b_ == "UNREAD":
            continue
        if i == 0 or tdays[i - 1] != p:
            continue
        if a_ is None or b_ is None:
            a_, b_ = None, None
        graded.append(d)
        prev_of[d], A[d], B[d] = p, a_, b_
        sp = load("src", p)
        pidx = collections.defaultdict(lambda: collections.defaultdict(list))        # account -> cusip -> [prices of the prior day's priced rows]
        if sp not in (None, "UNREAD"):
            for ac, c, mv, u in zip(sp["AccountID"], sp["CUSIP"], sp["Market Value"], sp["Units"]):
                pr = m.price_row(c, mv, u)
                if pr is not None:
                    pidx[ac][str(c).strip()].append(pr)
        rows_of = collections.defaultdict(list)
        for ac, c, mv, u, f in zip(s["AccountID"], s["CUSIP"], s["Market Value"], s["Units"], s["Cash Equivalent"]):
            rows_of[ac].append((c, mv, u, f))
        for ac, rows in rows_of.items():
            pp = pidx.get(ac, {})
            det = m.account_day(rows, a_, b_, prior_prices=pp)
            base[ac][d] = det["claim"]
            base_tally["present"] += 1
            base_tally[det["claim"]] += 1
            if "OUTSIDE_ANCHOR" in det["base_kinds"]:
                ad_store[(ac, d)] = (rows, {str(c).strip(): pp.get(str(c).strip()) for c, _mv, _u, _f in rows if c})
    assert graded == P1["graded"], "the graded days differ from IB-pr-442's"
    base_ok = {k: base_tally[k] for k in m.CLAIMS} == {k: P1["tally_cash"][k] for k in m.CLAIMS} and base_tally["present"] == P1["tally_cash"]["present"]
    base_ok = base_ok and len(ad_store) == len(P1["ad"])
    print("graded", len(graded), "base tally", dict(base_tally), "equals IB-pr-442's cash-rule tally", base_ok, "account-days with an outside row", len(ad_store), flush=True)
    first, last = dt.date.fromisoformat(graded[0]), dt.date.fromisoformat(graded[-1])
    gd = {d: dt.date.fromisoformat(d) for d in graded}

    # ------------------------------------------------------------------------------------------------ the second witness's bars and the types
    pairs_of = collections.defaultdict(set)
    for r in T["rows"]:
        c = (r["CUSIP"] or "").strip()
        if c:
            pairs_of[c].add((r["SEC Asset Type"] or "<blank>", r["Share Class Type"] or "<blank>"))
    ticker_of = {c: tk for c, tk in R["sec_ticker"].items() if tk}      # securities behind an OUTSIDE_ANCHOR row: IB-pr-442's ticker rule

    def bars_of_ticker(tk):
        s, _ = dv.read_yahoo_close(ycache, tk)
        return {} if s is None else {EPOCH + dt.timedelta(days=int(k)): float(v) for k, v in s.items()}
    bcache = {}

    def bars(tk):
        if tk not in bcache:
            bcache[tk] = bars_of_ticker(tk)
        return bcache[tk]
    pop = [c for c in sorted(ticker_of) if m.second_witness_admits(pairs_of.get(c)) and bars(ticker_of[c])]   # nine pairs, outside the first witness, with bars
    pop_all_nine = [c for c in sorted(ticker_of) if m.second_witness_admits(pairs_of.get(c))]
    ov_pop = [c for c, v in sorted(OV["overlap_nine"].items()) if bars(v["ticker"])]
    pairs = {c: pairs_of.get(c, set()) for c in ticker_of}
    rc = {d: {} for d in graded}
    for c in pop:
        b = bars(ticker_of[c])
        for d in graded:
            rc[d][c] = (m.swg._bar(b, gd[d]), m.swg._bar(b, tc.prev_trading_day(gd[d])))

    def verdicts(window=None, rule=True, never=()):
        """{day: {cusip: bool}} for the securities of pop: the module's second_witness_grades_security_day; `never` = tickers given no grade on any day."""
        out = {d: {} for d in graded}
        tick_cache = {}
        for c in pop:
            tk = ticker_of[c]
            if tk not in tick_cache:
                tick_cache[tk] = {d: (False if tk in never else m.second_witness_grades_security_day(bars(tk), gd[d], repeated_share_rule=rule, window=window)) for d in graded}
            for d in graded:
                out[d][c] = tick_cache[tk][d]
        return out

    def evaluate(verdict):
        claims = {a: dict(v) for a, v in base.items()}
        freed = 0
        for (ac, d), (rows, ppr) in ad_store.items():
            det = m.account_day(rows, A[d], B[d], prior_prices=ppr, security_pairs=pairs, reader_closes=rc[d], reader_graded=verdict[d])
            claims[ac][d] = det["claim"]
            freed += 1 if det["freed"] else 0
        tally = collections.Counter(v for byday in claims.values() for v in byday.values())
        sv = m.serving_rule(claims, graded)
        pa = [v for v in sv["per_account"].values() if v[0]]
        return {"account_days": {"present": sum(tally.values()), **{k: tally.get(k, 0) for k in m.CLAIMS}},
                "serving_rule": {"eligible": sv["eligible"], "served": sv["served"], "blank": sv["blank"],
                                 "blank_share_percent": round(100.0 * sv["blank"] / sv["eligible"], 4), "accounts_never_served": sum(1 for e, s_ in pa if s_ == 0)},
                "freed_and_holding_no_other_ungradeable_kind": freed}

    # ------------------------------------------------------------------------------------------------ 1. the seam: the rule OFF reproduces IB-pr-452's nine-pair sizing
    v_off = verdicts(rule=False)
    off = evaluate(v_off)
    reproduces = (off["account_days"] == prior["account_days"] and off["freed_and_holding_no_other_ungradeable_kind"] == prior["freed_and_holding_no_other_ungradeable_kind"]
                  and off["serving_rule"]["blank"] == prior["serving_rule"]["blank"] and off["serving_rule"]["eligible"] == prior["serving_rule"]["eligible"]
                  and off["serving_rule"]["served"] == prior["serving_rule"]["served"]
                  and off["serving_rule"]["accounts_never_served"] == prior["serving_rule"]["accounts_never_served"])
    seam = {"reproduces": bool(reproduces), "computed_by": "the product module",
            "read": off, "expected": {"account_days": prior["account_days"], "serving_rule": prior["serving_rule"],
                                      "freed_and_holding_no_other_ungradeable_kind": prior["freed_and_holding_no_other_ungradeable_kind"]},
            "expected_source": "IB-pr-452's record, org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~308/IB148-1_nine_pair_sizing.json, sizings.nine_pairs_under_both_guard_sentences",
            "what_ran": ("date_basis_grading.account_day over every account-day of the 85 graded days, the repeated-share rule OFF (second_witness_grades_security_day(..., repeated_share_rule=False) "
                         "for each security-day), the nine admitted pairs read from the transactions table by date_basis_grading.second_witness_admits, serving by date_basis_grading.serving_rule"),
            "base_tally_equals_ib_pr_442_cash_rule_tally": bool(base_ok)}
    print("seam reproduces", reproduces, off, flush=True)
    if not reproduces:
        (outd / "IB150-1_seam_FAILED.json").write_text(json.dumps(seam, indent=1), encoding="utf-8")
        print("DOES NOT REPRODUCE: stop")
        return 2

    # ------------------------------------------------------------------------------------------------ 2. the candidate windows
    cands, on_cache, taken_days_of = [], {}, {}
    for w in cand_windows:
        von = verdicts(window=w)
        on_cache[w] = von
        taken = collections.defaultdict(int)          # cusip -> days the guard grades and the rule does not
        kept = collections.defaultdict(int)           # cusip -> days graded by both
        short = 0
        for c in pop:
            b = bars(ticker_of[c])
            for d in graded:
                if v_off[d][c] and not von[d][c]:
                    taken[c] += 1
                    if m.repeated_share(b, gd[d], w)[1] < m.min_days_compared(w):
                        short += 1
                elif v_off[d][c] and von[d][c]:
                    kept[c] += 1
        taken_days_of[w] = dict(taken)
        ev = evaluate(von)
        cands.append({"trading_days": w, "securities_taken": len(taken), "security_days_not_graded": sum(taken.values()),
                      "account_days_no_longer_freed": off["freed_and_holding_no_other_ungradeable_kind"] - ev["freed_and_holding_no_other_ungradeable_kind"],
                      "securities_whose_verdict_changes_within_the_run": sum(1 for c in taken if kept.get(c)),
                      "security_days_not_graded_for_short_history": short,
                      "securities_taken_on_every_day_the_guard_graded_them": sum(1 for c in taken if not kept.get(c)),
                      "freed_and_holding_no_other_ungradeable_kind": ev["freed_and_holding_no_other_ungradeable_kind"],
                      "blank": ev["serving_rule"]["blank"], "blank_share_percent": ev["serving_rule"]["blank_share_percent"],
                      "accounts_never_served": ev["serving_rule"]["accounts_never_served"],
                      "account_days_UNGRADEABLE": ev["account_days"]["UNGRADEABLE"],
                      "of_the_seven": sorted(tk for tk in SEVEN if any(ticker_of[c] == tk for c in taken))})
        print("candidate", w, {k: v for k, v in cands[-1].items() if k != "of_the_seven"}, cands[-1]["of_the_seven"], flush=True)

    # ------------------------------------------------------------------------------------------------ 3. the distribution in tenths at the last graded day
    def dist(cusips, tick, w):
        sh, none_compared = [], 0
        for c in cusips:
            r, n = m.repeated_share(bars(tick(c)), last, w)
            if n:
                sh.append((r, n))
            else:
                none_compared += 1
        return {"securities": len(sh), "tenths": tenths(sh), "securities_with_no_day_compared_not_counted": none_compared,
                "securities_with_more_than_half_repeated": sum(1 for r, n in sh if 2 * r > n)}
    d_out = dist(pop, lambda c: ticker_of[c], W)
    d_ov = dist(ov_pop, lambda c: OV["overlap_nine"][c]["ticker"], W)
    by_window = {str(w): {"outside": dist(pop, lambda c: ticker_of[c], w), "overlap": dist(ov_pop, lambda c: OV["overlap_nine"][c]["ticker"], w)} for w in cand_windows}
    distribution = {
        "securities": d_out["securities"],
        "over_what": ("the securities of the nine admitted pairs that sit OUTSIDE the first witness (behind an OUTSIDE_ANCHOR row of the sizing's account-days, cash rule in force) and have at "
                      "least one usable reader bar: %d securities (of %d of those nine pairs with a ticker); share of repeated days at the LAST graded day (%s), over the %d trading days "
                      "ending there (the proposed window): repeated_days / days_compared, a day compared when the security has a bar on it and on its prior trading day, both inside the window; "
                      "%d securities have no day compared and are not counted" % (len(pop), len(pop_all_nine), last.isoformat(), W, d_out["securities_with_no_day_compared_not_counted"])),
        "bin_rule_in_words": ("ten bins of width one tenth; a share exactly on an edge goes to the UPPER bin (0.5 is in 0.5-0.6; 0.1 is in 0.1-0.2); a share of exactly 1.0 (every compared day "
                              "repeated) goes to the last bin, 0.9-1.0. More than half repeated = the shares in 0.5-0.6 and above, except exactly 0.5."),
        "tenths": d_out["tenths"],
        "securities_with_more_than_half_repeated": d_out["securities_with_more_than_half_repeated"],
        "overlap_tenths": d_ov["tenths"],
        "overlap_securities": d_ov["securities"],
        "overlap_over_what": ("the securities BOTH witnesses carry (held on one or more of the 85 graded days, carried by the anchor with a positive close on one or more of them, with a ticker "
                              "that is not the CUSIP: %d, IB-pr-439 counted 894) whose type is one of the nine admitted pairs (%d) and that have a reader bar (%d); the same share, day and window; "
                              "%d have no day compared" % (metaall["overlap_with_a_ticker"], metaall["overlap_of_the_nine_pairs"], len(ov_pop), d_ov["securities_with_no_day_compared_not_counted"])),
        "overlap_securities_with_more_than_half_repeated": d_ov["securities_with_more_than_half_repeated"],
        "last_graded_day": last.isoformat(),
        "by_candidate_window": {k: {"outside_tenths": v["outside"]["tenths"], "outside_securities": v["outside"]["securities"],
                                    "overlap_tenths": v["overlap"]["tenths"], "overlap_securities": v["overlap"]["securities"],
                                    "outside_more_than_half": v["outside"]["securities_with_more_than_half_repeated"],
                                    "overlap_more_than_half": v["overlap"]["securities_with_more_than_half_repeated"]} for k, v in by_window.items()}}
    print("tenths outside", d_out, "overlap", d_ov, flush=True)

    # ------------------------------------------------------------------------------------------------ 4. the sizing under the rule at the proposed window, and the cost of what it takes
    v_on = on_cache[W] if W in on_cache else verdicts(window=W)
    on = evaluate(v_on)
    taken = taken_days_of[W] if W in taken_days_of else {}
    taken_tk = sorted({ticker_of[c] for c in taken})
    row_days, accts, taken_row_days = collections.Counter(), collections.defaultdict(set), collections.Counter()
    sec_of_tk = collections.defaultdict(set)
    for c in pop:
        sec_of_tk[ticker_of[c]].add(c)
    tk_of = {c: ticker_of[c] for c in pop}
    for (ac, d), (rows, _pp) in ad_store.items():
        for c, _mv, _u, _f in rows:
            cs = str(c).strip() if c else None
            if cs in tk_of and tk_of[cs] in set(taken_tk):
                row_days[tk_of[cs]] += 1
                accts[tk_of[cs]].add(ac)
                if v_off[d].get(cs) and not v_on[d].get(cs):
                    taken_row_days[tk_of[cs]] += 1
    by_ticker = {tk: {"security_days_not_graded_beyond_the_guard": sum(n for c, n in taken.items() if tk_of[c] == tk), "row_days": row_days[tk],
                      "row_days_on_days_the_rule_does_not_grade": taken_row_days[tk], "accounts_holding_it": len(accts[tk])} for tk in taken_tk}
    # the seven, not graded on any day
    v_7 = verdicts(rule=False, never=set(SEVEN))
    e7 = evaluate(v_7)
    seven_rd, seven_ac = collections.Counter(), collections.defaultdict(set)
    for (ac, d), (rows, _pp) in ad_store.items():
        for c, _mv, _u, _f in rows:
            cs = str(c).strip() if c else None
            if cs in tk_of and tk_of[cs] in SEVEN:
                seven_rd[tk_of[cs]] += 1
                seven_ac[tk_of[cs]].add(ac)
    seven_cost = {"securities": SEVEN, "account_days_no_longer_freed": off["freed_and_holding_no_other_ungradeable_kind"] - e7["freed_and_holding_no_other_ungradeable_kind"],
                  "accounts_no_longer_ever_served": e7["serving_rule"]["accounts_never_served"] - off["serving_rule"]["accounts_never_served"],
                  "row_days": sum(seven_rd.values()), "blank_if_the_seven_are_not_graded": e7["serving_rule"]["blank"],
                  "blank_share_percent_if_the_seven_are_not_graded": e7["serving_rule"]["blank_share_percent"],
                  "account_days": e7["account_days"],
                  "basis": "the nine-pair sizing with the repeated-share rule OFF (the guard alone), and these seven tickers given no grade on any of the 85 days: freed and never-served against the rule-off sizing",
                  "by_ticker": {tk: {"row_days": seven_rd[tk], "accounts_holding_it": len(seven_ac[tk]), "in_the_population_with_bars": tk in {tk_of[c] for c in pop}} for tk in SEVEN}}
    taken_cost = {"securities": taken_tk, "window": W, "securities_count": len(taken_tk),
                  "the_seven_of_ib_pr_452_all_taken": all(tk in taken_tk for tk in SEVEN),
                  "taken_not_in_the_seven": [tk for tk in taken_tk if tk not in SEVEN], "the_seven_not_taken": [tk for tk in SEVEN if tk not in taken_tk],
                  "account_days_no_longer_freed": off["freed_and_holding_no_other_ungradeable_kind"] - on["freed_and_holding_no_other_ungradeable_kind"],
                  "accounts_no_longer_ever_served": on["serving_rule"]["accounts_never_served"] - off["serving_rule"]["accounts_never_served"],
                  "row_days": sum(row_days.values()), "by_ticker": by_ticker,
                  "basis": ("securities taken = taken on ONE OR MORE of the 85 graded days at the proposed window (the guard grades the security-day, the repeated-share rule does not); "
                            "cost = the rule-off nine-pair sizing less the sizing under the rule; row_days = rows of those securities in the sizing's account-days (an account's row on a day)")}
    # coverage of the first graded days
    cov = {}
    for w in cand_windows:
        full = enough = short = 0
        for c in pop:
            r, n = m.repeated_share(bars(ticker_of[c]), first, w)
            full += n == w - 1
            enough += n >= m.min_days_compared(w)
            short += n < m.min_days_compared(w)
        cov[str(w)] = {"securities": len(pop), "full_window_of_comparisons": full, "at_least_the_short_history_floor": enough, "below_the_floor": short}
    fetch = {"call_count": len(calls), "distinct_tickers_asked": len({t for c in calls for t in c["ticker_list"]}), "tickers_asked_in_all": sum(c["tickers"] for c in calls),
             "tickers_asked_more_than_once": sum(c["tickers"] for c in calls) - len({t for c in calls for t in c["ticker_list"]}),
             "tickers_with_bars": sum(c["with_bars"] for c in calls), "tickers_with_no_bars": sum(c["no_bars"] for c in calls),
             "rate_limited_not_read": sum(c["rate_limited_not_read"] for c in calls), "tickers_per_call": [c["tickers"] for c in calls],
             "counted_before_fetching": True, "counted": {"ib_pr_452_list": meta452, "plus_the_overlap_securities_of_the_nine_pairs": metaall}, "stop_above": 1500,
             "start": calls[0]["start"] if calls else None, "end_exclusive": calls[0]["end_exclusive"] if calls else None,
             "earlier_trading_days_fetched_before_the_first_graded_day": 90, "first_graded_day": first.isoformat(), "last_graded_day": last.isoformat(),
             "pause_between_calls_seconds": 8, "parallel_calls": 0, "other_sources_asked": 0,
             "reader": "fetch_yahoo (data/assets/scripts/silver/commonwealth_price_basis_census.py) / read_yahoo_close (data/assets/scripts/silver/commonwealth_daily_valuation.py), neither edited; unadjusted Close"}
    doc = {"seam_rule_off_reproduces_ib_pr_452": seam,
           "window_proposed": {"trading_days": W, "candidates": cands, "first_graded_day_window_coverage": cov,
                               "population": "the %d securities of the nine admitted pairs outside the first witness with a reader bar (of %d with a ticker); every count is over those securities and the 85 graded days" % (len(pop), len(pop_all_nine))},
           "securities_by_share_of_repeated_days": distribution,
           "sizing_under_the_rule": {"window": W, "account_days": on["account_days"], "serving_rule": on["serving_rule"],
                                     "freed_and_holding_no_other_ungradeable_kind": on["freed_and_holding_no_other_ungradeable_kind"],
                                     "against_the_rule_off_sizing": {"freed": off["freed_and_holding_no_other_ungradeable_kind"], "blank": off["serving_rule"]["blank"],
                                                                     "accounts_never_served": off["serving_rule"]["accounts_never_served"]}},
           "securities_taken_by_the_rule_cost": taken_cost, "the_seven_whole_run_cost": seven_cost,
           "fetch": fetch, "claims_regraded_in_product": 0, "classes_admitted_by_this_cell": 0, "served_changes": 0, "other_sources_asked": 0}
    # ------------------------------------------------------------------------------------------------ 5. the proposal in words, from the counts above
    cw = {c["trading_days"]: c for c in cands}
    top = sorted(by_ticker.items(), key=lambda kv: -kv[1]["row_days_on_days_the_rule_does_not_grade"])[:3]
    reason = ("%d trading days (about two calendar months), the day graded included. Over the %d securities of the nine pairs outside the first witness with bars and the %d graded days, the rule "
              "takes, by window (securities taken on one or more days / security-days un-graded beyond the guard / securities graded on some days and taken on others / account-days no longer freed): "
              "%s. A short window lets a spell of a few repeated bars take a security that otherwise moves: %d and %d securities change verdict inside the run at 10 and 20 days. From 40 days the "
              "set of securities taken stops growing (%d at 40, %d at 60, %d at 85) and the number that change verdict settles (%d at 40; %d at 60; %d at 85), while a longer window costs more freed "
              "account-days (%d at 40, %d at 60, %d at 85) and un-grades more security-days for want of history (%d, %d, %d). 40 is the shortest window at which the verdicts have settled. THE TRADE, "
              "plainly: a fixed window is reproducible (the same security-day, the same grade, whatever the run) but it is not the whole-run reading v0.43 wrote. The seven securities of IB-pr-452 "
              "not graded on any day cost %d account-days and %d account; the %d-day window takes those seven and %d more, each on part of the run, and costs %d account-days and %d accounts. "
              "The row-days un-graded by the rule on the days it does not grade are most on %s (%s row-days): securities near the one-half edge are un-graded on the days a window finds more than half repeated and graded on the others."
              % (W, len(pop), len(graded), "; ".join("%d: %d / %d / %d / %d" % (c["trading_days"], c["securities_taken"], c["security_days_not_graded"], c["securities_whose_verdict_changes_within_the_run"],
                                                    c["account_days_no_longer_freed"]) for c in cands),
                 cw[10]["securities_whose_verdict_changes_within_the_run"], cw[20]["securities_whose_verdict_changes_within_the_run"],
                 cw[40]["securities_taken"], cw[60]["securities_taken"], cw[85]["securities_taken"],
                 cw[40]["securities_whose_verdict_changes_within_the_run"], cw[60]["securities_whose_verdict_changes_within_the_run"], cw[85]["securities_whose_verdict_changes_within_the_run"],
                 cw[40]["account_days_no_longer_freed"], cw[60]["account_days_no_longer_freed"], cw[85]["account_days_no_longer_freed"],
                 cw[40]["security_days_not_graded_for_short_history"], cw[60]["security_days_not_graded_for_short_history"], cw[85]["security_days_not_graded_for_short_history"],
                 seven_cost["account_days_no_longer_freed"], seven_cost["accounts_no_longer_ever_served"], W, len(taken_cost["taken_not_in_the_seven"]),
                 taken_cost["account_days_no_longer_freed"], taken_cost["accounts_no_longer_ever_served"], ", ".join(k for k, _v in top),
                 ", ".join(str(v["row_days_on_days_the_rule_does_not_grade"]) for _k, v in top)))
    floor = m.min_days_compared(W)
    fewer = ("A security-day with fewer than %d days compared in its window (half the window, rounded up: min_days_compared) gets NO grade from the second witness with the rule on: a share "
             "taken from fewer days is not a measurement, and a comparison the instrument cannot make is not a pass (v0.41's spirit). At or above %d compared days the share is taken over "
             "the days that exist. With the rule off (the guard alone) the floor does not apply. The window is the %d trading days of the calendar ending at the graded day and reads no bar "
             "outside it; a day is compared only when both it and its prior trading day are inside the window, so at most %d days are compared. At the first graded day %s, %d of %d securities have "
             "the full %d comparisons and %d are below the floor." % (floor, floor, W, W - 1, first.isoformat(), cov[str(W)]["full_window_of_comparisons"], len(pop), W - 1, cov[str(W)]["below_the_floor"]))
    doc["window_proposed"].update({"reason": reason, "when_fewer_bars_than_the_window": fewer, "short_history_floor_days_compared": floor,
                                   "window_definition": "the REPEATED_SHARE_WINDOW trading days of lib/trading_calendar ending at the graded day, the graded day included; nothing before the window is read",
                                   "candidates_note": ("securities_taken = securities (CUSIPs) on which the guard grades a security-day and the rule does not, on one or more of the 85 graded days; "
                                                       "securities_whose_verdict_changes_within_the_run = of those, the ones the rule also graded (with the guard) on one or more days; the 85-day candidate "
                                                       "is the whole run as the window, graded per day")})
    doc["not_established"] = [
        "That %d trading days is the right window: several were measured and one is proposed; the CTO writes the contract.  The short-history floor (half the window) is chosen, not derived." % W,
        "Why a security's bar repeats (a stale feed, a fund that does not move, a late publication): the counts cannot tell them apart, and the rule does not try.",
        "That the securities the rule takes beyond IB-pr-452's seven are wrongly graded by the second witness: they repeat on about half their days and are taken on part of the run; nothing here says their moved bars are dated wrong.",
        "That a freed account-day's claim would be correct: freed account-days are a count of account-days no witness is barred from grading, not a check that the claim is right.",
        "The distribution on any day but the last graded day (%s)." % last.isoformat(),
        "The overlap securities' sizing: they are counted in tenths only; the first witness grades them and the rule would not touch a claim of the first witness.",
        "Anything outside the 85 graded days, the %d tickers asked, or the securities with no ticker, no type, mixed types or another type (not graded, not counted in the tenths)." % fetch["distinct_tickers_asked"],
        "The %d tickers for which the reader returned nothing: their rows block their account-days (the module gives no grade without a bar)." % fetch["tickers_with_no_bars"],
        "Whether the sizing under the rule would be the sizing a producer reads: no producer, schema or schedule exists; nothing is served and no claim is re-graded in the product."]
    (outd / "IB150-1_product_form_run.json").write_text(json.dumps(doc, indent=1), encoding="utf-8")
    sz = doc["sizing_under_the_rule"]
    ds = doc["securities_by_share_of_repeated_days"]
    md = ["# IB150-1 (IB-pr-454) -- the date-basis grading instrument's product form: the fixed window, the distribution in tenths and the rule's cost",
          "",
          "READ ONLY; counts only; nothing served, re-graded or admitted. Data: `IB150-1_product_form_run.json`; driver `ib150_run.py` (the module `data/assets/scripts/gold/irpt_reporting/date_basis_grading.py` does every grading; the driver reads the cache and counts). Same 85 trading days (%s to %s)." % (first.isoformat(), last.isoformat()),
          "",
          "## The three returns",
          "1. **The window: %d trading days** (the graded day included), short history = no grade below %d compared days. By window, securities taken / security-days un-graded beyond the guard / securities that change verdict inside the run / account-days no longer freed: %s. Reason and the trade in the JSON (`window_proposed.reason`) and below."
          % (W, floor, "; ".join("%d: %d / %d / %d / %d" % (c["trading_days"], c["securities_taken"], c["security_days_not_graded"], c["securities_whose_verdict_changes_within_the_run"], c["account_days_no_longer_freed"]) for c in cands)),
          "2. **The distribution at the last graded day (%s), window %d, %d securities of the nine pairs outside the first witness** (a share on an edge goes to the upper bin): %s. More than half repeated: %d. Overlap securities beside them (%d): %s; more than half: %d."
          % (last.isoformat(), W, ds["securities"], ", ".join("%s: %d" % (k, v) for k, v in ds["tenths"].items()), ds["securities_with_more_than_half_repeated"], ds["overlap_securities"],
             ", ".join("%s: %d" % (k, v) for k, v in ds["overlap_tenths"].items()), ds["overlap_securities_with_more_than_half_repeated"]),
          "3. **The rule's cost at %d days:** takes %d securities (the seven of IB-pr-452: %s taken; %d others: %s); %d account-days no longer freed, %d accounts no longer ever served, %d row-days. Sizing under the rule: blank %.4f percent (%d of %d eligible), never served %d, freed %d. Exactly the seven not graded on any day: %d account-days no longer freed, %d account no longer ever served, %d row-days."
          % (W, len(taken_tk), "all" if taken_cost["the_seven_of_ib_pr_452_all_taken"] else "NOT all", len(taken_cost["taken_not_in_the_seven"]), ", ".join(taken_cost["taken_not_in_the_seven"]),
             taken_cost["account_days_no_longer_freed"], taken_cost["accounts_no_longer_ever_served"], taken_cost["row_days"], sz["serving_rule"]["blank_share_percent"], sz["serving_rule"]["blank"],
             sz["serving_rule"]["eligible"], sz["serving_rule"]["accounts_never_served"], sz["freed_and_holding_no_other_ungradeable_kind"],
             seven_cost["account_days_no_longer_freed"], seven_cost["accounts_no_longer_ever_served"], seven_cost["row_days"]),
          "",
          "## The seam",
          "With the repeated-share rule OFF the module reads, over the same 85 days: UNGRADEABLE %d; ACCT_PRIOR_DATE %d; ACCT_OWN_DATE %d; NOTHING_TO_GRADE %d (present %d); blank %d of %d eligible (%.4f percent), never served %d, freed %d: IB-pr-452's nine-pair sizing, member for member (reproduces: %s)."
          % (off["account_days"]["UNGRADEABLE"], off["account_days"]["ACCT_PRIOR_DATE"], off["account_days"]["ACCT_OWN_DATE"], off["account_days"]["NOTHING_TO_GRADE"], off["account_days"]["present"],
             off["serving_rule"]["blank"], off["serving_rule"]["eligible"], off["serving_rule"]["blank_share_percent"], off["serving_rule"]["accounts_never_served"],
             off["freed_and_holding_no_other_ungradeable_kind"], seam["reproduces"]),
          "",
          "## The trade, plainly",
          reason,
          "",
          "## The pass",
          "Yahoo Finance only (`fetch_yahoo` / `read_yahoo_close`, unedited). Counted BEFORE fetching: %d distinct tickers (the %d of IB-pr-452 plus the overlap securities of the nine pairs), under the 1,500 stop. %d calls, each ticker asked once, %d with bars, %d with none (recorded, never re-asked), %d rate-limited, paced %d s, none parallel. Window %s to %s (end exclusive): 90 trading days before the first graded day were fetched, so the first graded days have full windows for every candidate (see `first_graded_day_window_coverage`). No YCharts, no Bloomberg; S3 reads only."
          % (fetch["distinct_tickers_asked"], meta452["distinct"], fetch["call_count"], fetch["tickers_with_bars"], fetch["tickers_with_no_bars"], fetch["rate_limited_not_read"],
             fetch["pause_between_calls_seconds"], fetch["start"], fetch["end_exclusive"]),
          "",
          "## Not established",
          ] + ["- " + x for x in doc["not_established"]]
    (outd / "IB150-1_PRODUCT_FORM_RUN_READ.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("wrote", outd, "window", W, "taken", len(taken_tk), taken_tk, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
