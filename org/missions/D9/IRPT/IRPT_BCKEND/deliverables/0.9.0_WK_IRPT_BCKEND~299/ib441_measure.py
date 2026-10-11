#!/usr/bin/env python3
"""IB-pr-441 measure.  Read only.  Counts only: no account key, balance or single account's holding or trade is read or written.

    python -I ib441_measure.py --control
    python -I ib441_measure.py <prep.pkl> <yahoo_cache> <calls.json> <out.json>

TABLE 1: the securities both witnesses carry, each with its type from the transactions table; per type, the reader's bar for day t against the anchor's close.
TABLE 2: every priced fund trade, its Price beside the reader's bar for the trade date, the prior and the next trading day; exactly one outcome.
The classifiers (classify_day, classify_trade) are the ones the real run uses; the control runs them on a planted fixture.
"""
from __future__ import annotations

import collections
import datetime as dt
import json
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOL = 1e-4
COLS4 = ("equal", "one_day_off", "neither", "no_bar")
SIX = ("same_day_only", "prior_day_only", "next_day_only", "more_than_one", "none", "no_bar")
EPOCH = dt.date(1970, 1, 1)
MANY = 3          # a date is "many securities at once" when at least this many securities of the type are one_day_off on it


def same(a, b):
    """relative 1e-4."""
    return abs(a - b) <= TOL * max(abs(a), abs(b))


def cent(a, b):
    return abs(round(a, 2) - round(b, 2)) < 0.005


def classify_day(reader, anchor, tdays, i):
    """-> (label, direction).  reader / anchor: {day: value}.  equal; one_day_off (not equal for t, and the bar equals the anchor close of the prior OR the next trading day;
    direction 'prior' / 'next' / 'both'); neither; no_bar.  `equal` is tested first."""
    t = tdays[i]
    r, a = reader.get(t), anchor.get(t)
    if r is None:
        return "no_bar", None
    if a is not None and same(r, a):
        return "equal", None
    d = []
    for j, name in ((i - 1, "prior"), (i + 1, "next")):
        if 0 <= j < len(tdays):
            n = anchor.get(tdays[j])
            if n is not None and same(r, n):
                d.append(name)
    if d:
        return "one_day_off", ("both" if len(d) == 2 else d[0])
    return "neither", None


def classify_trade(price, bars, tdays, i, match):
    """One outcome per trade.  bars: {day: reader value}; i: index of the trade date in tdays; match(price, bar) -> bool."""
    if i is None or bars.get(tdays[i]) is None:
        return "no_bar"
    hit = [j for j in (i - 1, i, i + 1) if 0 <= j < len(tdays) and bars.get(tdays[j]) is not None and match(price, bars[tdays[j]])]
    if not hit:
        return "none"
    if len(hit) > 1:
        return "more_than_one"
    return {i - 1: "prior_day_only", i: "same_day_only", i + 1: "next_day_only"}[hit[0]]


def control_run():
    """Known by construction.  Trading days d0..d6, graded d1..d5.  A: reader labels one day LATE (bar(t) = close(t-1)); B: reader = anchor; C: a missing bar and a wrong price;
    D: reader labels one day EARLY (bar(t) = close(t+1)).  Three planted trades on a fund series: at the same day's bar, at the prior day's bar, at a price matching none
    (and three more for the other outcomes)."""
    td = ["d0", "d1", "d2", "d3", "d4", "d5", "d6"]
    anc = {"A": [10, 11, 12, 12, 13, 14, 15], "B": [20, 21, 22, 23, 24, 25, 26], "C": [30, 31, 32, 33, 34, 35, 36], "D": [40, 41, 42, 42, 43, 44, 45]}
    rdr = {"A": {td[i]: anc["A"][i - 1] for i in range(1, 6)}, "B": {td[i]: anc["B"][i] for i in range(1, 6)},
           "C": {"d1": 31, "d3": 99, "d4": 34, "d5": 35}, "D": {td[i]: anc["D"][i + 1] for i in range(1, 6)}}
    ov = {}
    for s in anc:
        a = {td[i]: v for i, v in enumerate(anc[s])}
        res = [classify_day(rdr[s], a, td, i)[0] for i in range(1, 6)]
        c = collections.Counter(res)
        moved = sum(1 for k, i in enumerate(range(1, 6)) if res[k] == "equal" and not same(a[td[i]], a[td[i - 1]]))
        ov[s] = {**{k: c.get(k, 0) for k in COLS4}, "equal_on_days_the_close_moved": moved}
    bars = {"d0": 9.0, "d1": 10.0, "d2": 11.0, "d3": 12.0, "d4": 15.0, "d5": 17.0}      # a fund series with distinct bars; trades planted on it
    t_same = classify_trade(11.0, bars, td, 2, same)       # at d2's bar (d1 = 10, d3 = 12 differ) -> same_day_only
    t_prior = classify_trade(10.0, bars, td, 2, same)      # at d1's bar, the trade is on d2 -> prior_day_only
    t_none = classify_trade(55.0, bars, td, 2, same)       # matches no bar -> none
    t_next = classify_trade(12.0, bars, td, 2, same)       # extra: at d3's bar -> next_day_only
    t_nobar = classify_trade(11.0, {"d1": 10.0}, td, 2, same)   # extra: no bar for the trade date -> no_bar
    t_more = classify_trade(12.0, {"d1": 12.0, "d2": 12.0, "d3": 13.0}, td, 2, same)   # extra: the bar did not move between the days it matches
    return {"overlap": ov, "shifted_series_reads_one_day_off": ov["A"]["one_day_off"] == 4 and ov["D"]["one_day_off"] == 4,
            "unshifted_series_reads_equal": ov["B"]["equal"] == 5,
            "trade_at_the_same_day_bar_reads_same_day_only": t_same == "same_day_only",
            "trade_on_the_prior_bar_reads_prior_day_only": t_prior == "prior_day_only",
            "trade_matching_none_reads_none": t_none == "none",
            "trade_on_the_next_bar_reads_next_day_only": t_next == "next_day_only", "trade_with_no_bar_reads_no_bar": t_nobar == "no_bar",
            "trade_on_an_unmoved_bar_reads_more_than_one": t_more == "more_than_one",
            "three_planted_trades": [t_same, t_prior, t_none]}


PLANTED = {"overlap": {"A": {"equal": 1, "one_day_off": 4, "neither": 0, "no_bar": 0, "equal_on_days_the_close_moved": 0},
                       "B": {"equal": 5, "one_day_off": 0, "neither": 0, "no_bar": 0, "equal_on_days_the_close_moved": 5},
                       "C": {"equal": 3, "one_day_off": 0, "neither": 1, "no_bar": 1, "equal_on_days_the_close_moved": 3},
                       "D": {"equal": 1, "one_day_off": 4, "neither": 0, "no_bar": 0, "equal_on_days_the_close_moved": 1}},
           "shifted_series_reads_one_day_off": True, "unshifted_series_reads_equal": True,
           "trade_at_the_same_day_bar_reads_same_day_only": True, "trade_on_the_prior_bar_reads_prior_day_only": True, "trade_matching_none_reads_none": True,
           "trade_on_the_next_bar_reads_next_day_only": True, "trade_with_no_bar_reads_no_bar": True, "trade_on_an_unmoved_bar_reads_more_than_one": True,
           "three_planted_trades": ["same_day_only", "prior_day_only", "none"]}


def type_key(sec_types):
    """-> (key, kind).  The type of a security = the (SEC Asset Type, Share Class Type) pair of its de-duplicated transaction rows; one distinct pair -> that pair;
    none -> NO_TYPE; more than one -> MIXED."""
    if not sec_types:
        return "NO_TYPE", "none"
    if len(sec_types) == 1:
        (a, s), = sec_types
        return "%s / %s" % (a, s), "one"
    return "MIXED", "many"


def main():
    if sys.argv[1:] == ["--control"]:
        r = control_run()
        print(json.dumps(r), "\nEQUAL:", r == PLANTED)
        return 0 if r == PLANTED else 1
    prep, ycache, calls_f, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    root = HERE.parents[6]
    sys.path[:0] = [str(root / "lib"), str(root), str(root / "data/assets/scripts/silver"), str(root / "data/assets/scripts/analysis")]
    import commonwealth_daily_valuation as dv
    import trading_calendar as tc
    P = pickle.load(open(prep, "rb"))
    calls = json.load(open(calls_f))
    ax, graded, anchor = P["axis"], P["graded"], P["anchor"]
    gi = [ax.index(d) for d in graded]

    def day_iso(n):
        return (EPOCH + dt.timedelta(days=int(n))).isoformat()
    reader_cache = {}

    def bars_of(t):
        if t not in reader_cache:
            s, _ = dv.read_yahoo_close(ycache, t)
            reader_cache[t] = None if s is None else {day_iso(k): float(v) for k, v in s.items()}
        return reader_cache[t]
    # ---------------- TABLE 1
    sec_ticker, types_of = P["sec_ticker"], P["types_of"]
    found = collections.Counter()
    mixed_combos = collections.Counter()
    by_type = collections.defaultdict(lambda: {"securities": 0, "security_days": 0, **{k: 0 for k in COLS4}, "equal_on_days_the_close_moved": 0,
                                               "securities_with_any_one_day_off": 0, "securities_whose_ticker_returned_nothing": 0, "anchor_days_not_carried": 0})
    detail = []                                   # (type, ticker, date, direction)
    sec_off = collections.defaultdict(collections.Counter)    # type -> ticker -> one_day_off days
    date_off = collections.defaultdict(collections.Counter)   # type -> date -> securities one_day_off on it
    for c in sorted(sec_ticker):
        k, kind = type_key(set(types_of.get(c, {})))
        found[kind] += 1
        if kind == "many":
            mixed_combos[" + ".join(sorted("%s / %s" % p for p in types_of[c]))] += 1
        r = by_type[k]
        r["securities"] += 1
        tk = sec_ticker[c]
        bars = bars_of(tk)
        if not bars:
            r["securities_whose_ticker_returned_nothing"] += 1
        a_c = {d: anchor[d].get(c) for d in ax}
        any_off = False
        for i in gi:
            d = ax[i]
            if a_c[d] is None:
                r["anchor_days_not_carried"] += 1
                continue
            lab, dr = classify_day(bars or {}, a_c, ax, i)
            r["security_days"] += 1
            r[lab] += 1
            if lab == "equal" and i > 0 and a_c[ax[i - 1]] is not None and not same(a_c[d], a_c[ax[i - 1]]):
                r["equal_on_days_the_close_moved"] += 1
            if lab == "one_day_off":
                any_off = True
                detail.append((k, tk, d, dr))
                sec_off[k][tk] += 1
                date_off[k][d] += 1
        if any_off:
            r["securities_with_any_one_day_off"] += 1
    overlap = {k: dict(v) for k, v in sorted(by_type.items())}
    empty = sorted(k for k, v in overlap.items() if v["one_day_off"] == 0 and v["equal"] > 0)
    # ---- what is behind every non-empty one-day-off entry
    summary = {}
    many_key = "dates_with_%d_or_more_securities_at_once" % MANY
    for k in sorted(sec_off):
        dates = date_off[k]
        many = {d: n for d, n in dates.items() if n >= MANY}
        summary[k] = {"one_day_off": overlap[k]["one_day_off"], "securities_with_any": overlap[k]["securities_with_any_one_day_off"],
                      "dates_with_one_day_off": len(dates), many_key: len(many),
                      "one_day_off_on_those_many_dates": sum(many.values()), "one_day_off_on_the_other_dates": sum(dates.values()) - sum(many.values()),
                      "dates_by_count_top": sorted(dates.items(), key=lambda x: (-x[1], x[0]))[:10],
                      "securities_by_days_top": sorted(sec_off[k].items(), key=lambda x: (-x[1], x[0]))[:10]}
    detail.sort(key=lambda x: (-sec_off[x[0]][x[1]], x[0], x[1], x[2]))
    detail_lines = [{"type": k, "ticker": tk, "date": d, "direction": dr, "days_for_this_ticker": sec_off[k][tk], "securities_one_day_off_that_date": date_off[k][d]}
                    for k, tk, d, dr in detail[:80]]
    # ---------------- TABLE 2
    fx = [d.isoformat() for d in tc.trading_days_between(dt.date(2026, 6, 5), dt.date(2026, 10, 13))]
    fi = {d: i for i, d in enumerate(fx)}
    trades = P["inside"]
    trade_ids = [t["id"] for t in trades]
    assert len(trade_ids) == len(set(trade_ids))

    def run(date_key, match):
        cnt = collections.Counter()
        per_fund = collections.defaultdict(collections.Counter)
        outc = []
        excluded = 0
        for t in trades:
            dd = t[date_key]
            if dd is None or dd not in fi:
                if date_key == "trade":
                    cnt["no_bar"] += 1
                    per_fund[t["cusip"]]["no_bar"] += 1
                    outc.append("no_bar")
                else:
                    excluded += 1
                    outc.append(None)
                continue
            bars = bars_of(t["ticker"]) if t["ticker"] else None
            o = classify_trade(t["price"], bars or {}, fx, fi[dd], match)
            cnt[o] += 1
            per_fund[t["cusip"]][o] += 1
            outc.append(o)
        return {**{k: cnt.get(k, 0) for k in SIX}, "trades": sum(cnt.values())}, per_fund, outc, excluded
    main_, per_fund, outc, _ = run("trade", same)
    cent_, per_fund_c, outc_c, _ = run("trade", cent)
    settle_, per_fund_s, outc_s, s_excl = run("settle", same)
    settle_c, _, _, _ = run("settle", cent)
    not_trading = sum(1 for t in trades if t["trade"] not in fi)
    ticker_of = {t["cusip"]: t["ticker"] for t in trades}
    by_fund = []
    for c in sorted(per_fund, key=lambda c: (-sum(per_fund[c].values()), ticker_of[c] or "")):
        by_fund.append({"ticker": ticker_of[c], "trades": sum(per_fund[c].values()), **{k: per_fund[c].get(k, 0) for k in SIX}})
    fund_dates = len({(t["cusip"], t["trade"]) for t in trades})
    # concentration of the off-day trades
    conc = {}
    for o in ("prior_day_only", "next_day_only", "more_than_one", "none"):
        sel = [t for t, x in zip(trades, outc) if x == o]
        conc[o] = {"trades": len(sel), "funds": len({t["cusip"] for t in sel}),
                   "by_fund_top": collections.Counter(t["ticker"] for t in sel).most_common(10),
                   "by_trade_date_top": collections.Counter(t["trade"] for t in sel).most_common(10),
                   "by_kind": dict(collections.Counter("%s / %s" % (t["type"], t["sub"]) for t in sel)),
                   "weekday_of_trade_date": dict(collections.Counter(dt.date.fromisoformat(t["trade"]).strftime("%a") for t in sel))}
    conc_c = {}
    for o in ("prior_day_only", "next_day_only"):
        sel = [t for t, x in zip(trades, outc_c) if x == o]
        conc_c[o] = {"trades": len(sel), "funds": len({t["cusip"] for t in sel}), "by_fund_top": collections.Counter(t["ticker"] for t in sel).most_common(10),
                     "by_trade_date_top": collections.Counter(t["trade"] for t in sel).most_common(10), "by_kind": dict(collections.Counter("%s / %s" % (t["type"], t["sub"]) for t in sel))}
    nb_noticker = sum(1 for t, x in zip(trades, outc) if x == "no_bar" and not bars_of(t["ticker"]))
    nb_tickers = sorted({t["ticker"] for t, x in zip(trades, outc) if x == "no_bar" and not bars_of(t["ticker"])})
    rel = []
    for t, x in zip(trades, outc):
        if x == "none":
            b = bars_of(t["ticker"])
            rel.append(abs(t["price"] - b[t["trade"]]) / b[t["trade"]])
    rel.sort()
    none_diag = {"trades": len(rel), "relative_difference_to_the_trade_date_bar": {"median": rel[len(rel) // 2], "p10": rel[len(rel) // 10], "p90": rel[9 * len(rel) // 10]} if rel else {},
                 "under_0.1_percent": sum(1 for x in rel if x < 0.001)}
    kinds_all = dict(collections.Counter("%s / %s" % (t["type"], t["sub"]) for t in trades))
    funds_with_any_off = sum(1 for c, v in per_fund.items() if v.get("prior_day_only", 0) + v.get("next_day_only", 0) > 0)
    ctl = control_run()
    fund_tickers = {t["ticker"] for t in trades}
    fetch = {"calls": [{"call": c["call"], "tickers": c["tickers"], "with_bars": c["with_bars"], "no_bars": c["no_bars"], "rate_limited_not_read": c["rate_limited_not_read"]} for c in calls],
             "call_count": len(calls), "distinct_tickers_asked": sum(c["tickers"] for c in calls),
             "tickers_asked_more_than_once": len([t for t, n in collections.Counter(t for c in calls for t in c["ticker_list"]).items() if n > 1]),
             "pause_between_calls_seconds": 8, "reader_internal_pause_seconds": 6, "parallel_calls": 0, "window": "2026-06-05 to 2026-10-13 (end exclusive 2026-10-14)",
             "reader": "fetch_yahoo (data/assets/scripts/silver/commonwealth_price_basis_census.py) / read_yahoo_close (data/assets/scripts/silver/commonwealth_daily_valuation.py), neither edited; auto_adjust=False, unadjusted Close",
             "tickers_with_bars": sum(c["with_bars"] for c in calls), "tickers_with_no_bars": sum(c["no_bars"] for c in calls),
             "distinct_tickers_made_of": "%d first tickers of the securities both witnesses carry and %d tickers of the funds with a priced trade inside the 85 days; the two lists overlap in %d" % (
                 len(set(sec_ticker.values())), len(fund_tickers), len(set(sec_ticker.values()) & fund_tickers))}
    last_bar = max((max(v) for v in reader_cache.values() if v), default=None)
    edges = {"reader_last_bar_date_in_any_series": last_bar, "anchor_partitions_absent_on_axis_days": P["anc_days_missing"],
             "first_graded_day_prior_day_is": ax[0], "last_graded_day_next_trading_day_is": ax[-1],
             "meaning": "the comparison for 2026-10-09 has no next-trading-day value on the anchor side (the anchor partition for %s is absent) and the reader's latest bar is %s; the prior day of 2026-06-10 is %s, present on both sides" % (ax[-1], last_bar, ax[0])}
    doc = {
        "type_join": {
            "type_fields": "SEC Asset Type and Share Class Type of the silver transactions table beside the holdings table (fact_transactions), joined to a security by CUSIP (stripped); type key '<SEC Asset Type> / <Share Class Type>'",
            "securities_both_witnesses_carry": len(sec_ticker), "found_a_type": found["one"], "found_no_type": found["none"], "found_more_than_one_type": found["many"],
            "how_a_type_is_taken": "all de-duplicated (on TransactionID) transaction rows of the CUSIP are read, of every transaction kind and every date; the set of distinct (SEC Asset Type, Share Class Type) pairs is taken, a blank value written '<blank>'. One pair -> that pair is the type. No row for the CUSIP -> NO_TYPE. More than one pair -> MIXED (the combinations and counts are in mixed_combinations).",
            "mixed_combinations": dict(mixed_combos.most_common()),
            "securities_definition": "held by an account of the holdings source on one or more of the 85 days, carried by the anchor with a positive closing_price on one or more of them, and with a ticker in the source (Ticker or Symbol) that is not the CUSIP itself: %d held, %d of those carried by the anchor, %d of those with a ticker; IB-pr-439 counted 894" % (P["held"], P["both"], P["both_t"]),
            "ticker_taken": "the first, in sorted order, of the tickers (Ticker, Symbol) the source states for the CUSIP",
            "transactions_read": {"partitions": len(P["tx_meta"]["partitions"]), "objects": P["tx_meta"]["objects"], "rows_read": P["tx_meta"]["rows_read"], "distinct_transaction_ids": P["tx_distinct_ids"],
                                  "first_partition": P["tx_meta"]["partitions"][0], "last_partition": P["tx_meta"]["partitions"][-1], "columns_absent_in_objects": P["tx_meta"]["absent_cols"]}},
        "overlap_by_type": overlap,
        "one_day_off_rule": "For a security and a trading day t of the 85 (2026-06-10 to 2026-10-09) on which the anchor carries it: the reader's bar for t is compared with the anchor's closing_price for t at relative 1e-4. equal = within that tolerance. Not equal, and the reader's bar for t is within that tolerance of the anchor's close for the PRIOR or the NEXT trading day = one_day_off. Otherwise neither. No reader bar for t (the ticker returned nothing, or no bar that day) = no_bar. A day on which the anchor does not carry the security is not a security-day (counted in anchor_days_not_carried).",
        "unchanged_price_rule": "When the anchor's close for t equals its close for the prior or next trading day, the reader's bar equals the anchor's for t and the day is `equal` (tested first), never one_day_off; it is counted in `equal` but NOT in `equal_on_days_the_close_moved`, because on an unchanged day a correct date label and a shifted one read the same.",
        "types_with_an_empty_one_day_off_column": empty,
        "one_day_off_summary": summary,
        "one_day_off_detail": detail_lines,
        "one_day_off_detail_note": "up to 80 lines, most-affected ticker first, then ticker, then date; the full per-type counts are in one_day_off_summary; a date is 'many securities at once' when %d or more securities of the type are one_day_off on it" % MANY,
        "edges": edges,
        "fund_trades": {
            "how_a_fund_is_recognised": "a row of the transactions table (de-duplicated on TransactionID) with Transaction Type Buy or Sale, Price above 0, SEC Asset Type 'Securities Issued by Registered Investment Companies or Business Development Companies' and Share Class Type neither 'ETF' nor 'Not Available'; the fund is the CUSIP",
            "unit_counted": "TRADES (rows, de-duplicated by TransactionID) whose Trade Date is one of the 85 graded trading days; fund_dates = distinct (fund, trade date) pairs among them",
            "date_column": "Trade Date (mm/dd/yyyy); the second line uses Settle Date (same format)",
            "tolerance": "relative 1e-4 of the larger of the trade Price and the reader's bar (the instrument's tolerance); the same six counts to the cent (both rounded to 2 decimals, equal) are in to_the_cent",
            "trades": main_["trades"], "fund_dates": fund_dates, "funds": len(per_fund), **{k: main_[k] for k in SIX},
            "count_check": "IB-pr-439 counted 1,099 fund-dates over 103 funds, 1,044 inside the 85 days; this cell: %d fund-dates over %d funds with a Trade Date inside the 85 days; over all dates %d trades on %d fund-dates over %d funds (the %d trades before 2026-06-10 are not compared: the reader's window is fixed at 2026-06-05 to 2026-10-13)" % (
                fund_dates, len(per_fund), len(P["trades"]), len({(t["cusip"], t["trade"]) for t in P["trades"]}), len({t["cusip"] for t in P["trades"]}), len(P["trades"]) - len(trades)),
            "trade_dates_not_a_trading_day": not_trading,
            "to_the_cent": {"trades": cent_["trades"], **{k: cent_[k] for k in SIX}},
            "by_settle_date": {"trades": settle_["trades"], **{k: settle_[k] for k in SIX}, "trades_whose_settle_date_is_outside_the_window_or_not_a_trading_day": s_excl,
                               "to_the_cent": {k: settle_c[k] for k in SIX}},
            "by_fund": by_fund, "funds_with_any_prior_or_next_day_only_trade": funds_with_any_off, "concentration_to_the_cent": conc_c,
            "no_bar_trades_whose_fund_ticker_returned_nothing": nb_noticker, "no_bar_tickers": nb_tickers, "none_diagnostic": none_diag,
            "trade_kinds_all": kinds_all, "concentration": conc},
        "fetch": fetch,
        "control": {"planted": PLANTED, "read": ctl, "equal": ctl == PLANTED,
                    "what_it_is": "four planted securities over trading days d0..d6 (graded d1..d5): A reader one day LATE, B reader = anchor, C one missing bar and one wrong price, D reader one day EARLY; and three planted trades on a fund series (same-day bar, prior-day bar, a price matching none) plus the other three outcomes; the real run uses the same two classifiers"},
        "claims_regraded_in_product": False, "other_sources_asked": 0, "classes_admitted_by_this_cell": 0,
    }
    out.write_text(json.dumps(doc, indent=1, default=str), encoding="utf-8")
    print("wrote", out, "control equal", ctl == PLANTED, "securities", len(sec_ticker), "types", len(overlap), "empty", len(empty), "trades", main_["trades"], {k: main_[k] for k in SIX})
    return 0


if __name__ == "__main__":
    sys.exit(main())
