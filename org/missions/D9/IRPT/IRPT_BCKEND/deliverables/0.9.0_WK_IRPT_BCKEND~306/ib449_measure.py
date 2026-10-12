#!/usr/bin/env python3
"""IB-pr-449 measure.  READ ONLY; counts only: no account key, balance or single account's holding is written.  Nothing is re-graded in the product, no class admitted.

    python -I ib449_measure.py --control
    python -I ib449_measure.py <prep441.pkl> <phase1.pkl> <prep442.pkl> <parts_cache> <yahoo_cache> <calls.json> <meta.json> <ib142_record.json> <out.json>

What the second witness's bar is when it MOVES after a repeated run (two fund pairs), the six institutional securities' moved days, and (AMENDMENT 1, PRD v0.41) how many
security-days of the overlap table the "no bar for the trading day before t" sentence un-grades that IB-pr-445's guard graded.  The classifiers are imported from
ib441_measure / ib445_measure (IB-pr-445's own functions, unchanged): same price rule, relative tolerance 1e-4, trading-day axis, type rule, guard.
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
import ib445_measure as m445  # noqa: E402

EPOCH = dt.date(1970, 1, 1)
same = m441.same
GUARD = m445.GUARD
RIC = "Securities Issued by Registered Investment Companies or Business Development Companies"
PAIRS = (RIC + " / Inst", RIC + " / Not Available")
SIX = ("ADLYX", "BISOX", "EIBLX", "GPPIX", "JSOSX", "OLCYX")
RUN_OUT = ("equals_the_anchor_same_day", "equals_the_anchor_prior_day", "equals_neither", "no_anchor_that_day", "no_moved_day_in_window")
ROW_OUT = ("equals_the_bar_same_day", "equals_the_bar_prior_day", "equals_neither")

RUN_RULE = ("For one security, a REPEATED RUN is a maximal sequence of consecutive trading days (of the 85 graded days, 2026-06-10 to 2026-10-09) on each of which the reader's "
            "(Yahoo Finance unadjusted Close) bar exists and equals its bar for the prior trading day within the relative tolerance 1e-4 (|a-b| <= 1e-4 * max(|a|,|b|)); the prior trading "
            "day of 2026-06-10 is 2026-06-09. A day on which the reader has no bar, or none for the prior trading day, is not a repeated day and ends a run.")
FIRST_MOVED_RULE = ("The FIRST MOVED DAY after a run is the first trading day after the run's last day, within the 85 graded days, on which the reader has a bar and a bar for the prior "
                    "trading day and the two differ (not equal within 1e-4). It is placed against the anchor (the Schwab closing price by CUSIP), in this order: no_anchor_that_day if the anchor has "
                    "no close for that day; equals_the_anchor_same_day if the moved bar equals the anchor's close for that day; equals_the_anchor_prior_day if it equals the anchor's close "
                    "for the prior trading day and not that day's (a late bar); else equals_neither. A run with no such day up to 2026-10-09 is no_moved_day_in_window.")
NO_PRIOR_RULE = ("AMENDMENT 1 / PRD v0.41: where the reader has NO bar for the trading day before t (the trading calendar's prior day, not the prior row), it gives no grade for that "
                 "security on t. Counted over the overlap table's security-days (a day on which the first witness carries the security and the reader has a bar for t) that "
                 "IB-pr-445's guard graded (equal, one_day_off or neither) and this sentence un-grades.")


NOT_ESTABLISHED = [
    "Whether the class should be admitted or refused: this cell admits no class and recommends neither.",
    "Why the reader's bar repeats: a stale feed, a fund that does not move, or a late publication cannot be told apart by these counts.",
    "What the reader's bar is on a moved day for any security with no anchor close that day: 'no_anchor_that_day' is counted, not graded.",
    "Anything about securities outside the two pairs and the six: only the no-prior-bar count reaches the other ten types, and it is a count, not a grade.",
    "Days after 2026-10-09: the window ends there; a run that reaches it is counted as no_moved_day_in_window, and the anchor partition for 2026-10-12 is absent.",
    "Whether the six, all outside or partly outside the first witness, would be graded by any rule other than the reader's bar: no second witness exists for them on the days the anchor lacks them.",
    "Rows of the six with no price (market value or units not positive) are not graded against the bar; they are counted beside, not in, the three outcomes.",
    "The size of the first moved bar's error where it equals neither the anchor's same-day nor prior-day close: no such case exists in the two pairs, so none is sized.",
]


def day_iso(n):
    return (EPOCH + dt.timedelta(days=int(n))).isoformat()


def find_runs(bars, ax, win):
    """bars {iso day: close}; ax the trading-day axis; win the axis indexes of the window's days.  -> list of (first_index, last_index) of repeated runs (consecutive window days)."""
    runs, cur = [], None
    for i in win:
        r, p = bars.get(ax[i]), bars.get(ax[i - 1])
        rep = r is not None and p is not None and same(r, p)
        if rep and cur is not None and cur[1] == i - 1:
            cur[1] = i
        elif rep:
            cur = [i, i]
            runs.append(cur)
    return [(a, b) for a, b in runs]


def first_moved(bars, anchor, ax, win, run):
    """-> (outcome, index of the moved day or None).  The first window day after the run with a bar and a prior bar that differ, placed against the anchor."""
    last_win = win[-1]
    for j in range(run[1] + 1, last_win + 1):
        r, p = bars.get(ax[j]), bars.get(ax[j - 1])
        if r is None or p is None or same(r, p):
            continue
        a = anchor.get(ax[j])
        if a is None:
            return "no_anchor_that_day", j
        if same(r, a):
            return "equals_the_anchor_same_day", j
        ap = anchor.get(ax[j - 1])
        if ap is not None and same(r, ap):
            return "equals_the_anchor_prior_day", j
        return "equals_neither", j
    return "no_moved_day_in_window", None


def control_run():
    """Two planted five-day series (d1..d5, prior day d0 for the axis): the bar repeats on days 2 and 3 and moves on day 4; the anchor's closes are 10/11/12/13/14.
    Case 1: the day-4 bar is the anchor's day-4 close.  Case 2: the day-4 bar is the anchor's day-3 close.  Run through find_runs / first_moved, the functions the real run uses."""
    ax = ["d0", "d1", "d2", "d3", "d4", "d5"]
    anc = {"d0": 9.0, "d1": 10.0, "d2": 11.0, "d3": 12.0, "d4": 13.0, "d5": 14.0}
    out = {}
    for name, d4 in (("case_1_day_4_bar_is_the_anchors_day_4_close", 13.0), ("case_2_day_4_bar_is_the_anchors_day_3_close", 12.0)):
        bars = {"d0": 9.0, "d1": 10.0, "d2": 10.0, "d3": 10.0, "d4": d4, "d5": 14.0}
        win = [1, 2, 3, 4, 5]
        runs = find_runs(bars, ax, win)
        out[name] = {"runs": [(ax[a], ax[b]) for a, b in runs], "first_moved_day": [first_moved(bars, anc, ax, win, r)[0] for r in runs]}
    return {k: {"runs": [list(x) for x in v["runs"]], "first_moved_day": v["first_moved_day"]} for k, v in out.items()}


PLANTED = {"case_1_day_4_bar_is_the_anchors_day_4_close": {"runs": [["d2", "d3"]], "first_moved_day": ["equals_the_anchor_same_day"]},
           "case_2_day_4_bar_is_the_anchors_day_3_close": {"runs": [["d2", "d3"]], "first_moved_day": ["equals_the_anchor_prior_day"]}}


def main():
    if sys.argv[1:] == ["--control"]:
        r = control_run()
        print(json.dumps(r, indent=1), "\nEQUAL:", r == PLANTED)
        return 0 if r == PLANTED else 1
    p441f, p1f, p442f, parts, ycache, calls_f, meta_f, prior_f, out = sys.argv[1:10]
    root = HERE.parents[6]
    sys.path[:0] = [str(root / "lib"), str(root), str(root / "data/assets/scripts/silver"), str(root / "data/assets/scripts/analysis")]
    import commonwealth_daily_valuation as dv
    import ib429_claims as old
    A = pickle.load(open(p441f, "rb"))
    P = pickle.load(open(p1f, "rb"))
    R = pickle.load(open(p442f, "rb"))
    calls = json.load(open(calls_f))
    meta = json.load(open(meta_f))
    prior = json.load(open(prior_f, encoding="utf-8"))

    sers = {}

    def bars_iso(t):
        if not t:
            return {}
        if t not in sers:
            s, _ = dv.read_yahoo_close(ycache, t)
            sers[t] = None if s is None else {day_iso(k): float(v) for k, v in s.items()}
        return sers[t] or {}

    ax, graded, anchor = A["axis"], A["graded"], A["anchor"]
    gi = [ax.index(d) for d in graded]
    sec_ticker, types_of = A["sec_ticker"], A["types_of"]

    # ---------------------------------------------------------------- 1. reproduce Table 1 under the guard (all twelve types) and the new sentence
    tab = collections.defaultdict(lambda: {"securities": 0, "security_days": 0, **{k: 0 for k in m445.COLS5}})
    np_by_type, np_equal = collections.Counter(), 0
    type_of_sec = {}
    for c in sorted(sec_ticker):
        k, _ = m441.type_key(set(types_of.get(c, {})))
        type_of_sec[c] = k
        bars = bars_iso(sec_ticker[c])
        a_c = {d: anchor[d].get(c) for d in ax}
        tab[k]["securities"] += 1
        for i in gi:
            if a_c[ax[i]] is None:
                continue
            lab, _, _ = m445.label_day(bars, a_c, ax, i, same)
            tab[k]["security_days"] += 1
            tab[k][lab] += 1
            if lab in ("equal", "one_day_off", "neither") and bars.get(ax[i - 1]) is None:       # the reader has a bar for t (lab is not no_bar) and none for the prior trading day
                np_by_type[k] += 1
                np_equal += 1 if lab == "equal" else 0
    rep_all = prior["overlap_by_type_under_the_guard"]
    all_types_reproduce = sorted(tab) == sorted(rep_all) and all(
        all(tab[k][c] == rep_all[k][c] for c in ("securities", "security_days") + m445.COLS5) for k in tab)

    # ---------------------------------------------------------------- 2. runs and first moved day, the two pairs
    by_pair = {}
    for pair in PAIRS:
        secs = [c for c in sorted(sec_ticker) if type_of_sec[c] == pair]
        n_runs = n_days = n_sec_with = 0
        lengths = collections.Counter()
        outc = collections.Counter()
        inside = moved_a = also = noanc = 0
        gap = 0
        for c in secs:
            bars = bars_iso(sec_ticker[c])
            a_c = {d: anchor[d].get(c) for d in ax}
            runs = find_runs(bars, ax, gi)
            n_sec_with += 1 if runs else 0
            for run in runs:
                n_runs += 1
                n_days += run[1] - run[0] + 1
                lengths[run[1] - run[0] + 1] += 1
                o, j = first_moved(bars, a_c, ax, gi, run)
                outc[o] += 1
                if j is not None and j != run[1] + 1:
                    gap += 1
                if o == "equals_neither":
                    if any(a_c[ax[k]] is not None and same(bars[ax[j]], a_c[ax[k]]) for k in range(run[0], run[1] + 1)):
                        inside += 1
                for k in range(run[0], run[1] + 1):
                    a, ap = a_c[ax[k]], a_c[ax[k - 1]]
                    if a is None or ap is None:
                        noanc += 1
                    elif same(a, ap):
                        also += 1
                    else:
                        moved_a += 1
        by_pair[pair] = {
            "securities": len(secs), "securities_with_a_repeated_run": n_sec_with, "repeated_runs": n_runs, "days_in_runs": n_days,
            "run_lengths": {str(k): v for k, v in sorted(lengths.items())},
            "reproduces_ib_pr_445_under_the_guard": {c: tab[pair][c] for c in m445.COLS5},
            "first_moved_day_after_a_run": {o: outc.get(o, 0) for o in RUN_OUT},
            "equals_an_anchor_close_inside_the_run": inside,
            "run_days_the_anchor_moved": moved_a, "run_days_the_anchor_also_unmoved": also, "run_days_with_no_anchor": noanc,
            "runs_whose_first_moved_day_is_not_the_day_after_the_run": gap,
            "security_days_ungraded_by_the_no_prior_bar_sentence": np_by_type.get(pair, 0)}
    repro_ok = all(by_pair[p]["reproduces_ib_pr_445_under_the_guard"][c] == prior["overlap_by_type_under_the_guard"][p][c] for p in PAIRS for c in m445.COLS5)

    # ---------------------------------------------------------------- 3. the six
    sec_t2, sec_cls0, secs_p = R["sec_ticker"], R["sec_cls"], P["secs"]
    named = json.dumps(prior["inst_under_the_guard"]["securities_ungraded_on_more_than_half_their_days"])
    six_in_prior = all(t in named for t in SIX)
    cus = {t: [c for c in secs_p if sec_t2[c] == t] for t in SIX}
    the_six = {}
    for t in SIX:
        (c,) = cus[t]
        bars = bars_iso(t)
        have_a = sum(1 for d in ax if anchor[d].get(c) is not None)
        x = {"days_with_a_bar": 0, "days_unmoved": 0, "days_moved": 0, "days_with_no_prior_bar": 0, "moved_days_under_a_tenth_of_a_percent": 0}
        moved = {}
        for i in gi:
            r, p = bars.get(ax[i]), bars.get(ax[i - 1])
            if r is None:
                continue
            x["days_with_a_bar"] += 1
            if p is None:
                x["days_with_no_prior_bar"] += 1
            elif same(r, p):
                x["days_unmoved"] += 1
            else:
                x["days_moved"] += 1
                moved[ax[i]] = (r, p)
                if abs(r - p) < 0.001 * abs(p):
                    x["moved_days_under_a_tenth_of_a_percent"] += 1
        rows = collections.Counter()
        unpriced = 0
        for d in graded:
            if d not in moved:
                continue
            s = pickle.load(open(Path(parts) / ("src_%s.pkl" % d), "rb"))
            pr = old.price_rows(s["CUSIP"], s["Market Value"], s["Units"])
            unpriced += sum(1 for i, cu in enumerate(s["CUSIP"]) if cu and cu.strip() == c and i not in pr)
            r, p = moved[d]
            for i, (cu, price) in pr.items():
                if cu != c:
                    continue
                rows["equals_the_bar_same_day" if same(price, r) else ("equals_the_bar_prior_day" if same(price, p) else "equals_neither")] += 1
        sizing_rows = sum(1 for (a, d), rr in P["ad"].items() if d in moved for cu, _ in rr["rows"] if cu == c)
        x.update({"anchor_carries_it": have_a > 0, "anchor_days_carrying_it_of_the_axis": have_a,
                  "rows_held_on_moved_days": sum(rows.values()), "held_rows_on_moved_days": {o: rows.get(o, 0) for o in ROW_OUT},
                  "rows_of_the_security_on_moved_days_with_no_price": unpriced, "rows_on_moved_days_in_the_ib_pr_445_sizing": sizing_rows,
                  "name_the_holdings_rows_state": secs_p[c]["name"], "class_before_any_bar": sec_cls0[c]})
        x["what_kind_of_fund"] = ("The holdings rows name it '%s' and the transactions table types it %s; neither says it is a money-market or stable-value fund or that it holds a constant price: not told." % (
            secs_p[c]["name"], "Registered Investment Companies or Business Development Companies / Inst"))
        the_six[t] = x

    # ---------------------------------------------------------------- 4. fetch, control, outputs
    ticks = [t for c_ in calls for t in c_["ticker_list"]]
    fetch = {"call_count": len(calls), "distinct_tickers_asked": len(set(ticks)), "tickers_asked_in_all": len(ticks),
             "tickers_asked_more_than_once": len([t for t, n in collections.Counter(ticks).items() if n > 1]),
             "tickers_with_bars": sum(c_["with_bars"] for c_ in calls), "tickers_with_no_bars": sum(c_["no_bars"] for c_ in calls),
             "rate_limited_not_read": sum(c_["rate_limited_not_read"] for c_ in calls),
             "tickers_per_call": [c_["tickers"] for c_ in calls], "counted_before_fetching": True, "counted": meta,
             "why_more_than_400": "AMENDMENT 1 lifts the stop to 1,100 distinct tickers for the all-twelve-types count: the overlap table's %d tickers plus %d of the six not in it = %d" % (
                 meta["overlap_tickers"], meta["six_added"], meta["distinct"]),
             "window": "2026-06-05 to 2026-10-13 (end exclusive 2026-10-14)", "pause_between_calls_seconds": 8, "parallel_calls": 0,
             "reader": "fetch_yahoo (data/assets/scripts/silver/commonwealth_price_basis_census.py) / read_yahoo_close (data/assets/scripts/silver/commonwealth_daily_valuation.py), neither edited; unadjusted Close"}
    ctl = control_run()
    doc = {"run_rule_in_words": RUN_RULE, "first_moved_day_rule_in_words": FIRST_MOVED_RULE,
           "first_moved_bar_by_pair": by_pair,
           "reproduction": {"all_twelve_types_equal_ib_pr_445_under_the_guard": bool(all_types_reproduce), "the_two_pairs_equal": bool(repro_ok),
                            "totals": {"securities": sum(v["securities"] for v in tab.values()), "security_days": sum(v["security_days"] for v in tab.values())}},
           "no_prior_bar_sentence": {"in_words": NO_PRIOR_RULE, "overlap_all_types_security_days_ungraded": sum(np_by_type.values()),
                                     "by_type": {k: np_by_type.get(k, 0) for k in sorted(tab)}, "of_which_were_equal": np_equal,
                                     "first_day_of_window_treatment": "The prior trading day of the first graded day (2026-06-10) is 2026-06-09, which the fetch window (from 2026-06-05) holds, so the first day is graded like any other: "
                                                                      "a security with no bar for 2026-06-09 is un-graded on 2026-06-10 and counted; no day is skipped for lack of an earlier fetched bar."},
           "the_six": the_six, "the_six_are_those_ib_pr_445_named": bool(six_in_prior),
           "fetch": fetch, "control": {"planted": PLANTED, "read": ctl},
           "not_established": NOT_ESTABLISHED,
           "claims_regraded_in_product": 0, "classes_admitted_by_this_cell": 0, "other_sources_asked": 0}
    Path(out).write_text(json.dumps(doc, indent=1), encoding="utf-8")
    print("wrote", out, "control equal", ctl == PLANTED, "all types reproduce", all_types_reproduce, "pairs", repro_ok, "six named", six_in_prior)
    for p in PAIRS:
        print(p[-12:], {k: v for k, v in by_pair[p].items() if k != "reproduces_ib_pr_445_under_the_guard"})
    print("no_prior", sum(np_by_type.values()), "equal", np_equal, dict(np_by_type))
    for t in SIX:
        print(t, the_six[t])
    return 0


if __name__ == "__main__":
    sys.exit(main())
