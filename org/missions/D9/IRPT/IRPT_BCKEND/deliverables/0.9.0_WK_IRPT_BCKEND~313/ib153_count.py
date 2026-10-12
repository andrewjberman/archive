#!/usr/bin/env python3
"""IB-pr-457 count.  READ ONLY; counts only: no account key (the cache holds a one-way 12-character digest), balance or holding of an account is written,
and no security is named.  Every grade below is computed BY THE PRODUCT MODULE (data/assets/scripts/gold/irpt_reporting/date_basis_grading.py); this script only
reads the cache, groups rows by account-day, hands them to the module and counts.  The set-up (cache -> account-days -> bars -> verdicts) is the driver of
IB-pr-454 (deliverables/0.9.0_WK_IRPT_BCKEND~310/ib150_run.py), copied for its set-up lines; nothing in it is changed.

    python -I ib153_count.py <partition_cache> <overlap.pkl> <phase1.pkl> <prep.pkl> <yahoo_cache> <out.json>

(the cache, pickles and Yahoo cache are rebuilt in C:/dev/_scratch313 by the ~308 and ~310 scripts, unchanged, this cell's one Yahoo pass.)
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
W = m.REPEATED_SHARE_WINDOW
FLOOR = m.min_days_compared(W)


def main(argv=None):
    cache, ovf, p1f, prepf, ycache, out = sys.argv[1:7]
    cache = Path(cache)
    P1 = pickle.load(open(p1f, "rb"))
    R = pickle.load(open(prepf, "rb"))
    T = pickle.load(open(str(Path(cache).parent / "tx.pkl"), "rb"))

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

    # ---------------------------------------------------------------- account-days graded by the module (the cash rule in force), as ib150_run does
    graded, A, B = [], {}, {}
    base = collections.defaultdict(dict)
    ad_store = {}
    first_held = {}                        # cusip -> first listed partition day on which any account holds it (the 86 listed partitions)
    for d in listed:
        s = load("src", d)
        for c in s["CUSIP"]:
            c = (c or "").strip()
            if c and c not in first_held:
                first_held[c] = d
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
        A[d], B[d] = a_, b_
        sp = load("src", p)
        pidx = collections.defaultdict(lambda: collections.defaultdict(list))
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
            if "OUTSIDE_ANCHOR" in det["base_kinds"]:
                ad_store[(ac, d)] = (rows, {str(c).strip(): pp.get(str(c).strip()) for c, _mv, _u, _f in rows if c})
    assert graded == P1["graded"], "the graded days differ from IB-pr-442's"
    assert len(graded) == 85
    first, last = dt.date.fromisoformat(graded[0]), dt.date.fromisoformat(graded[-1])
    gd = {d: dt.date.fromisoformat(d) for d in graded}

    # ---------------------------------------------------------------- bars and types (the same population as IB-pr-454: nine pairs, outside the first witness, with bars)
    pairs_of = collections.defaultdict(set)
    for r in T["rows"]:
        c = (r["CUSIP"] or "").strip()
        if c:
            pairs_of[c].add((r["SEC Asset Type"] or "<blank>", r["Share Class Type"] or "<blank>"))
    ticker_of = {c: tk for c, tk in R["sec_ticker"].items() if tk}

    bcache = {}

    def bars(tk):
        if tk not in bcache:
            s, _ = dv.read_yahoo_close(ycache, tk)
            bcache[tk] = {} if s is None else {EPOCH + dt.timedelta(days=int(k)): float(v) for k, v in s.items()}
        return bcache[tk]
    pop = [c for c in sorted(ticker_of) if m.second_witness_admits(pairs_of.get(c)) and bars(ticker_of[c])]
    pairs = {c: pairs_of.get(c, set()) for c in ticker_of}
    rc = {d: {} for d in graded}
    for c in pop:
        b = bars(ticker_of[c])
        for d in graded:
            rc[d][c] = (m.swg._bar(b, gd[d]), m.swg._bar(b, tc.prev_trading_day(gd[d])))

    v_off, v_on, cmpd = {d: {} for d in graded}, {d: {} for d in graded}, {d: {} for d in graded}
    for c in pop:
        b = bars(ticker_of[c])
        for d in graded:
            v_off[d][c] = m.second_witness_grades_security_day(b, gd[d], repeated_share_rule=False)
            v_on[d][c] = m.second_witness_grades_security_day(b, gd[d], repeated_share_rule=True, window=W)
            cmpd[d][c] = m.repeated_share(b, gd[d], W)[1]
    # the waiver: a security-day the guard grades and ONLY the short-history floor takes is given the guard's grade
    v_wv = {d: {c: v_on[d][c] or (v_off[d][c] and cmpd[d][c] < FLOOR) for c in pop} for d in graded}

    def evaluate(verdict):
        claims = {a: dict(v) for a, v in base.items()}
        freed = 0
        for (ac, d), (rows, ppr) in ad_store.items():
            det = m.account_day(rows, A[d], B[d], prior_prices=ppr, security_pairs=pairs, reader_closes=rc[d], reader_graded=verdict[d])
            claims[ac][d] = det["claim"]
            freed += 1 if det["freed"] else 0
        sv = m.serving_rule(claims, graded)
        return {"freed": freed, "blank": sv["blank"], "eligible": sv["eligible"], "never_served": sum(1 for e, s_ in sv["per_account"].values() if e and s_ == 0)}
    e_off, e_on, e_wv = evaluate(v_off), evaluate(v_on), evaluate(v_wv)

    # ---------------------------------------------------------------- the count: security-days the rule leaves ungraded, split
    taken = short = repeat = repeat_full = 0
    sec_short_days, sec_taken_days = collections.Counter(), collections.Counter()
    for c in pop:
        for d in graded:
            if v_off[d][c] and not v_on[d][c]:
                taken += 1
                sec_taken_days[c] += 1
                if cmpd[d][c] < FLOOR:
                    short += 1
                    sec_short_days[c] += 1
                else:
                    repeat += 1
                    repeat_full += 1 if cmpd[d][c] == W - 1 else 0
    # securities short of FLOOR compared days on one or more graded days, whether or not the guard grades them that day (the face's wording), and the narrower
    # reading (a security-day the guard grades and ONLY the floor takes)
    short_any = {c for c in pop if any(cmpd[d][c] < FLOOR for d in graded)}
    short_taken = set(sec_short_days)
    # newly held: first held by any account on a listed partition after the first listed partition
    day0 = listed[0]
    newly = [c for c in pop if first_held.get(c, day0) > day0]
    newly_blank = [c for c in newly if any(v_off[d][c] and not v_on[d][c] and cmpd[d][c] < FLOOR for d in graded if d >= first_held[c])]
    newly_short_at_first_held = [c for c in newly if first_held[c] in cmpd and cmpd[first_held[c]][c] < FLOOR]
    newly_floor_met_at_first_held = [c for c in newly if first_held[c] in cmpd and cmpd[first_held[c]][c] >= FLOOR]
    newly_not_in_graded = [c for c in newly if first_held[c] not in cmpd]
    # securities whose bars begin inside the run (no bar before the first graded day)
    inrun = [c for c in pop if min(bars(ticker_of[c])) > first]
    inrun_days = sorted(sum(1 for d in graded if v_off[d][c] and not v_on[d][c] and cmpd[d][c] < FLOOR) for c in inrun)
    inrun_cmp_lt = sorted(sum(1 for d in graded if cmpd[d][c] < FLOOR and gd[d] > min(bars(ticker_of[c]))) for c in inrun)
    # bars that begin after the fetch's first day but before the run (a young security at the start of the run)
    fetch_first = min(min(bars(ticker_of[c])) for c in pop)
    young_before_run = [c for c in pop if fetch_first < min(bars(ticker_of[c])) <= first and cmpd[graded[0]][c] < FLOOR]
    doc = {
        "computed_by": "the product module",
        "module": "data/assets/scripts/gold/irpt_reporting/date_basis_grading.py",
        "window": W, "floor_days_compared": FLOOR,
        "graded_days": len(graded), "first_graded_day": first.isoformat(), "last_graded_day": last.isoformat(),
        "population_securities": len(pop),
        "security_days_the_guard_grades_and_the_rule_does_not": taken,
        "of_which_short_history_only": short,
        "of_which_repeat_rule_with_a_full_or_sufficient_window": repeat,
        "of_which_repeat_rule_with_the_full_window_of_comparisons": repeat_full,
        "securities_ever_short_of_history_any_graded_day": len(short_any),
        "securities_with_a_security_day_ungraded_for_short_history_only": len(short_taken),
        "newly_held_securities_in_population": len(newly),
        "newly_held_securities_blank_for_their_first_window": len(newly_blank),
        "newly_held_securities_blank_for_their_first_window_of_which_began_trading_inside_the_run": len(set(newly_blank) & set(inrun)),
        "newly_held_securities_short_of_history_on_the_day_first_held": len(newly_short_at_first_held),
        "newly_held_securities_with_the_floor_met_on_the_day_first_held": len(newly_floor_met_at_first_held),
        "newly_held_securities_first_held_on_a_day_not_graded": len(newly_not_in_graded),
        "first_listed_partition": day0,
        "account_days_freed_rule_off": e_off["freed"], "account_days_freed_rule_on": e_on["freed"], "account_days_freed_floor_waived": e_wv["freed"],
        "account_days_blank_only_for_short_history": e_wv["freed"] - e_on["freed"],
        "blank_rule_off": e_off["blank"], "blank_rule_on": e_on["blank"], "blank_floor_waived": e_wv["blank"], "eligible": e_on["eligible"],
        "never_served_rule_on": e_on["never_served"], "never_served_floor_waived": e_wv["never_served"],
        "securities_that_began_trading_inside_the_run": len(inrun),
        "securities_that_began_trading_inside_the_run_ungraded_days_for_short_history_only": inrun_days,
        "securities_that_began_trading_inside_the_run_graded_days_short_of_the_floor_after_the_first_bar": inrun_cmp_lt,
        "securities_with_bars_beginning_after_the_fetch_start_and_on_or_before_the_first_graded_day_and_short_on_it": len(young_before_run),
        "fetch_first_bar_day": fetch_first.isoformat(),
    }
    assert short + repeat == taken
    json.dump(doc, open(out, "w"), indent=1)
    print(json.dumps(doc, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
