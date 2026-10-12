#!/usr/bin/env python3
"""IB-pr-445 measure.  READ ONLY; counts only: no account key, balance, quantity or single account's holding is written.  Nothing is re-graded in the product.

    python -I ib445_measure.py --control
    python -I ib445_measure.py <prep441.pkl> <phase1.pkl> <prep442.pkl> <yahoo_cache> <calls.json> <tickers_meta.json> <ib138_2.json> <out.json>

THE GUARD (the CTO's ruling, msg 5549): the second witness (the reader's unadjusted Close) does not grade a security-day on which its own bar for t equals its own
bar for the prior trading day (relative 1e-4).  The first witness (the anchor) grades every security it carries, as today.

TABLE 1 (ib441_measure's classifier, copied by import): the securities both witnesses carry, per type, five exclusive columns per security-day:
  not_graded_under_the_guard (the reader's bar for t equals its bar for the prior trading day), else equal / one_day_off / neither / no_bar as in IB-pr-441.
SIZING (ib442_measure's row grade, account-day order, sizing claim and serving counter, imported UNCHANGED): the rows of securities outside the first witness; a
row whose reader bar for t equals the reader bar for the prior trading day gets no grade and blocks its account-day, exactly as a row with no bar.
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
import ib442_prepare as prep  # noqa: E402
import ib429_claims_v035 as v35  # noqa: E402

EPOCH = dt.date(1970, 1, 1)
GUARD = "not_graded_under_the_guard"
COLS5 = ("equal", "one_day_off", "neither", "no_bar", GUARD)
CLAIMS = m442.CLAIMS
OUTC = m442.OUTC
same, cent = m441.same, m441.cent
EXPECTED_441 = {"securities": 894, "security_days": 64536, "equal": 63720, "one_day_off": 5, "neither": 499, "no_bar": 312}
EXPECTED_442 = {"UNGRADEABLE": 37592, "ACCT_PRIOR_DATE": 107, "ACCT_OWN_DATE": 25498, "NOTHING_TO_GRADE": 13599, "present": 76796,
                "eligible": 75796, "served": 37667, "blank": 38129, "blank_share_percent": 50.305, "accounts_never_served": 357, "freed": 5666}
EXPECTED_CASH = {"UNGRADEABLE": 43310, "ACCT_PRIOR_DATE": 55, "ACCT_OWN_DATE": 19832, "NOTHING_TO_GRADE": 13599, "present": 76796}

GUARD_RULE = ("For a security and a trading day t: if the reader's (Yahoo Finance unadjusted Close) bar for t equals its bar for the prior trading day within the instrument's "
              "relative tolerance 1e-4 (|a-b| <= 1e-4 * max(|a|,|b|)), the second witness gives NO grade for that security on day t, whatever the first witness says; a security-day "
              "with no grade from any witness is ungradeable, as a security with no bar is today. The guard applies to the second witness only; the first witness (the Schwab "
              "anchor) grades every security it carries, as today. A day on which the reader has no bar for t, or none for the prior trading day, is not an unmoved bar.")


# ------------------------------------------------------------------ the guarded classifiers (the ones the real run and the control both use)
def label_day(reader, anchor, tdays, i, guard_eq):
    """-> (label, direction, label_without_the_guard).  Table 1's day label under the guard; guard_eq None = the guard switched off."""
    lab, dr = m441.classify_day(reader, anchor, tdays, i)
    if guard_eq is not None and lab != "no_bar" and i > 0:
        r, p = reader.get(tdays[i]), reader.get(tdays[i - 1])
        if r is not None and p is not None and guard_eq(r, p):
            return GUARD, None, lab
    return lab, dr, lab


def grade_row(mark, nd, npp, guard_eq):
    """-> the row outcome of ib442_measure.classify, or GUARD when the reader's bar for the day equals its bar for the prior trading day."""
    if nd is not None and npp is not None and guard_eq is not None and guard_eq(nd, npp):
        return GUARD
    return m442.classify(mark, nd, npp)


def day_outcome(outs):
    """ib442_measure.day_outcome with a guard-ungraded row counted as a row no witness may grade."""
    return m442.day_outcome(["no_bar_for_the_day_or_prior" if o == GUARD else o for o in outs])


# ------------------------------------------------------------------ the control
def control_run():
    """One security over five graded days (d1..d5, prior day d0) whose reader bar repeats on day 3, run through label_day / grade_row / day_outcome, the functions the
    real run uses.  Security U: anchor = reader (the anchor also sat still on day 3).  Security V: the anchor MOVES on day 3 while the reader repeats day 2's bar (the
    dangerous direction): without the guard it reads one_day_off (prior), with it not graded."""
    td = ["d0", "d1", "d2", "d3", "d4", "d5"]
    rdr = {"d0": 9.0, "d1": 10.0, "d2": 11.0, "d3": 11.0, "d4": 13.0, "d5": 14.0}
    anc_u = dict(rdr)
    anc_v = {"d0": 9.0, "d1": 10.0, "d2": 11.0, "d3": 12.0, "d4": 13.0, "d5": 14.0}
    lab_u = [label_day(rdr, anc_u, td, i, same)[0] for i in range(1, 6)]
    lab_u_off = [label_day(rdr, anc_u, td, i, None)[0] for i in range(1, 6)]
    lab_v = [label_day(rdr, anc_v, td, i, same)[0] for i in range(1, 6)]
    lab_v_off = [label_day(rdr, anc_v, td, i, None)[0] for i in range(1, 6)]
    nav = {"S": {"d%d" % i: rdr["d%d" % i] for i in range(6)}}

    def acct_day(k):                                  # an account-day holding S with the custodian's mark at the day's bar
        outs = [grade_row(rdr["d%d" % k], nav["S"]["d%d" % k], nav["S"]["d%d" % (k - 1)], same)]
        return day_outcome(outs), outs[0]
    oc3, row3 = acct_day(3)
    oc2, row2 = acct_day(2)
    oc4, row4 = acct_day(4)
    return {"day_labels_of_the_planted_security_under_the_guard": lab_u,
            "day_labels_with_the_guard_off": lab_u_off,
            "day_labels_when_the_anchor_moves_on_day_3_under_the_guard": lab_v,
            "day_labels_when_the_anchor_moves_on_day_3_with_the_guard_off": lab_v_off,
            "unmoved_bar_is_not_graded": lab_u[2] == GUARD and lab_v[2] == GUARD,
            "moved_bar_is_graded": all(lab_u[k] == "equal" for k in (0, 1, 3, 4)) and all(lab_v[k] != GUARD for k in (0, 1, 3, 4)),
            "account_day_holding_it_on_day_3": {"row": row3, "outcome": oc3, "freed": oc3 == OUTC[3]},
            "account_day_holding_it_on_day_2": {"row": row2, "outcome": oc2, "freed": oc2 == OUTC[3]},
            "account_day_holding_it_on_day_4": {"row": row4, "outcome": oc4, "freed": oc4 == OUTC[3]},
            "account_day_on_the_unmoved_day_is_not_freed": oc3 != OUTC[3] and oc3 == OUTC[0]}


PLANTED = {"day_labels_of_the_planted_security_under_the_guard": ["equal", "equal", GUARD, "equal", "equal"],
           "day_labels_with_the_guard_off": ["equal", "equal", "equal", "equal", "equal"],
           "day_labels_when_the_anchor_moves_on_day_3_under_the_guard": ["equal", "equal", GUARD, "equal", "equal"],
           "day_labels_when_the_anchor_moves_on_day_3_with_the_guard_off": ["equal", "equal", "one_day_off", "equal", "equal"],
           "unmoved_bar_is_not_graded": True, "moved_bar_is_graded": True,
           "account_day_holding_it_on_day_3": {"row": GUARD, "outcome": OUTC[0], "freed": False},
           "account_day_holding_it_on_day_2": {"row": "equals_day_only", "outcome": OUTC[3], "freed": True},
           "account_day_holding_it_on_day_4": {"row": "equals_day_only", "outcome": OUTC[3], "freed": True},
           "account_day_on_the_unmoved_day_is_not_freed": True}


# ------------------------------------------------------------------ main
def main():
    if sys.argv[1:] == ["--control"]:
        r = control_run()
        print(json.dumps(r, indent=1), "\nEQUAL:", r == PLANTED)
        return 0 if r == PLANTED else 1
    p441f, p1f, p442f, ycache, calls_f, meta_f, ib138f, out = [Path(x) for x in sys.argv[1:9]]
    root = HERE.parents[6]
    sys.path[:0] = [str(root / "lib"), str(root), str(root / "data/assets/scripts/silver"), str(root / "data/assets/scripts/analysis")]
    import commonwealth_daily_valuation as dv
    A = pickle.load(open(p441f, "rb"))
    P = pickle.load(open(p1f, "rb"))
    R = pickle.load(open(p442f, "rb"))
    calls = json.load(open(calls_f))
    meta = json.load(open(meta_f))
    ib138 = json.load(open(ib138f, encoding="utf-8"))

    def day_iso(n):
        return (EPOCH + dt.timedelta(days=int(n))).isoformat()
    sers = {}

    def series(t):                       # {int day: close}, or None when the ticker returned nothing
        if t not in sers:
            s, _ = dv.read_yahoo_close(ycache, t)
            sers[t] = None if s is None else {int(k): float(v) for k, v in s.items()}
        return sers[t]

    def bars_iso(t):
        s = series(t) if t else None
        return {day_iso(k): v for k, v in s.items()} if s else {}

    # ============================================================ TABLE 1 under the guard (and with the guard off, and to the cent)
    ax, graded, anchor = A["axis"], A["graded"], A["anchor"]
    gi = [ax.index(d) for d in graded]
    sec_ticker, types_of = A["sec_ticker"], A["types_of"]
    variants = {"off": None, "rel": same, "cent": cent}
    tab = {v: collections.defaultdict(lambda: {"securities": 0, "security_days": 0, **{k: 0 for k in COLS5}, "equal_on_days_the_close_moved": 0}) for v in variants}
    was = collections.defaultdict(collections.Counter)          # type -> former column of the days the guard (relative) un-graded
    detail = {"off": [], "rel": []}
    dir_rel_only, dir_cent_only = collections.Counter(), collections.Counter()    # type -> security-days un-graded by one reading and not by the other
    sec_unmoved = collections.defaultdict(lambda: [0, 0, None, None])   # cusip -> [days with both bars, unmoved days, ticker, type]
    type_of_sec = {}
    for c in sorted(sec_ticker):
        k, _ = m441.type_key(set(types_of.get(c, {})))
        type_of_sec[c] = k
        tk = sec_ticker[c]
        bars = bars_iso(tk)
        a_c = {d: anchor[d].get(c) for d in ax}
        for v in variants:
            tab[v][k]["securities"] += 1
        sec_unmoved[c][2:] = [tk, k]
        for i in gi:
            d = ax[i]
            if a_c[d] is None:
                continue
            if bars.get(d) is not None and bars.get(ax[i - 1]) is not None:
                sec_unmoved[c][0] += 1
                sec_unmoved[c][1] += 1 if same(bars[d], bars[ax[i - 1]]) else 0
            g_flag = {}
            for v, geq in variants.items():
                lab, dr, before = label_day(bars, a_c, ax, i, geq)
                g_flag[v] = lab == GUARD
                r = tab[v][k]
                r["security_days"] += 1
                r[lab] += 1
                if lab == "equal" and a_c[ax[i - 1]] is not None and not same(a_c[d], a_c[ax[i - 1]]):
                    r["equal_on_days_the_close_moved"] += 1
                if v == "rel" and lab == GUARD:
                    was[k][before] += 1
                if v in detail and lab == "one_day_off":
                    detail[v].append({"type": k, "ticker": tk, "date": d, "direction": dr,
                                      "reader_bars_prior_day_next": [bars.get(ax[i - 1]), bars.get(d), bars.get(ax[i + 1]) if i + 1 < len(ax) else None],
                                      "anchor_closes_prior_day_next": [a_c[ax[i - 1]], a_c[d], a_c[ax[i + 1]] if i + 1 < len(ax) else None]})
            if g_flag["rel"] and not g_flag["cent"]:
                dir_rel_only[k] += 1
            elif g_flag["cent"] and not g_flag["rel"]:
                dir_cent_only[k] += 1

    def tot(t, cols):
        return {k: sum(r[k] for r in t.values()) for k in cols}
    cols_all = ("securities", "security_days") + COLS5 + ("equal_on_days_the_close_moved",)
    off_t, rel_t, cent_t = ({k: dict(v) for k, v in sorted(tab[x].items())} for x in ("off", "rel", "cent"))
    off_tot = tot(off_t, cols_all)
    reproduces = all(off_tot[k] == v for k, v in EXPECTED_441.items()) and off_tot[GUARD] == 0
    ib138_t = ib138["overlap_by_type"]
    per_type_equal = sorted(ib138_t) == sorted(off_t) and all(
        all(off_t[k][c] == ib138_t[k][c] for c in ("securities", "security_days", "equal", "one_day_off", "neither", "no_bar", "equal_on_days_the_close_moved")) for k in off_t)
    over = {}
    for k, r in rel_t.items():
        o = off_t[k]
        over[k] = {**r, "guard_off": {c: o[c] for c in ("equal", "one_day_off", "neither", "no_bar")},
                   "neither_remaining": r["neither"], "guard_moved_neither": r["neither"] != o["neither"],
                   "not_graded_by_the_column_it_had_without_the_guard": {c: was[k].get(c, 0) for c in ("equal", "one_day_off", "neither")}}
    empty = sorted(k for k, r in rel_t.items() if r["one_day_off"] == 0 and r["equal"] > 0)
    empty_off = sorted(k for k, r in off_t.items() if r["one_day_off"] == 0 and r["equal"] > 0)
    rel_tot, cent_tot = tot(rel_t, cols_all), tot(cent_t, cols_all)
    five_off = sorted(detail["off"], key=lambda x: (x["date"], x["ticker"]))
    five = []
    for e in five_off:
        c = next(c for c in sec_ticker if sec_ticker[c] == e["ticker"])
        i = ax.index(e["date"])
        bars = bars_iso(e["ticker"])
        a_c = {d: anchor[d].get(c) for d in ax}
        lab, _, before = label_day(bars, a_c, ax, i, same)
        five.append({"ticker": e["ticker"], "date": e["date"], "type": e["type"], "direction_without_the_guard": e["direction"], "under_the_guard": lab,
                     "reader_bars_prior_day_next": e["reader_bars_prior_day_next"], "anchor_closes_prior_day_next": e["anchor_closes_prior_day_next"],
                     "label_without_the_guard": before})
    five_is_ib441 = sorted((e["ticker"], e["date"]) for e in five) == sorted((x["ticker"], x["date"]) for x in ib138["one_day_off_detail"])
    cent_net = {k: cent_t[k][GUARD] - rel_t[k][GUARD] for k in rel_t if cent_t[k][GUARD] != rel_t[k][GUARD]}
    moved_empty = sorted(k for k in empty if rel_t[k]["equal_on_days_the_close_moved"] > 0)
    over_half_overlap = sorted(({"ticker": tk, "type": ty, "days_with_both_bars": n, "days_unmoved": u} for c, (n, u, tk, ty) in sec_unmoved.items() if n and u * 2 > n),
                               key=lambda x: (-x["days_unmoved"] / x["days_with_both_bars"], x["ticker"]))
    table1_block = {"overlap_by_type_under_the_guard": over, "types_with_an_empty_one_day_off_column_under_the_guard": empty,
                    "types_with_an_empty_one_day_off_column_with_the_guard_off": empty_off,
                    "types_with_an_empty_one_day_off_column_under_the_guard_and_days_equal_on_which_the_close_moved": moved_empty,
                    "totals_under_the_guard": rel_tot, "totals_with_the_guard_off": off_tot,
                    "the_five_earlier_one_day_off_security_days": five,
                    "the_five_are_those_of_ib_pr_441": bool(five_is_ib441),
                    "one_day_off_remaining_under_the_guard": sorted(detail["rel"], key=lambda x: (x["date"], x["ticker"])),
                    "overlap_securities_ungraded_on_more_than_half_their_days": over_half_overlap}

    # ============================================================ SIZINGS
    graded_p, prev_of, ad, secs = P["graded"], P["prev_of"], P["ad"], P["secs"]
    sec_t2, sec_cls0 = R["sec_ticker"], dict(R["sec_cls"])

    def classes(include_inst):
        cls = {}
        for c, k in sec_cls0.items():
            if include_inst and k == "left_out_type_inst":
                k = "admitted_type"
            cls[c] = k if k != "admitted_type" else ("admitted_type_with_bars" if series(sec_t2[c]) else "no_bar")
        return cls

    def day_int(iso):
        return (dt.date.fromisoformat(iso) - EPOCH).days

    def sizing(include_inst, guard_eq):
        cls = classes(include_inst)
        nav = {c: series(sec_t2[c]) for c in secs if sec_t2[c] and cls[c] == "admitted_type_with_bars"}
        row_out, oc_counts, freed_clean, prior_clean = collections.Counter(), collections.Counter(), 0, 0
        new_claims = {}
        rows_by_sec, guard_rows_by_sec = collections.Counter(), collections.Counter()
        dirn = collections.Counter()
        for (a, d), r in ad.items():
            dd, pp = day_int(d), day_int(prev_of[d])
            outs = []
            for cu, price in r["rows"]:
                if cls[cu] != "admitted_type_with_bars":
                    o = "no_bar_for_the_day_or_prior"
                else:
                    o = grade_row(price, nav[cu].get(dd), nav[cu].get(pp), guard_eq)
                    if nav[cu].get(dd) is not None and nav[cu].get(pp) is not None:
                        f_r, f_c = same(nav[cu][dd], nav[cu][pp]), cent(nav[cu][dd], nav[cu][pp])
                        dirn["relative_only" if f_r and not f_c else ("cent_only" if f_c and not f_r else "both_or_neither")] += 1
                    rows_by_sec[cu] += 1
                    if o == GUARD:
                        guard_rows_by_sec[cu] += 1
                outs.append(o)
                row_out[o] += 1
            oc = day_outcome(outs)
            oc_counts[oc] += 1
            other = any(k != "OUTSIDE_ANCHOR" for k in r["kinds"]) or r["sixth"]
            if oc == OUTC[3] and not other:
                freed_clean += 1
            if oc == OUTC[2] and not other:
                prior_clean += 1
            nc = m442.new_claim(r["c1"], [("no_bar_for_the_day_or_prior" if o == GUARD else o) for o in outs], r["kinds"], r["sixth"], oc)
            if nc is not None:
                new_claims[(a, d)] = nc
        claims = {a: dict(v) for a, v in P["claims_cash"].items()}
        for (a, d), nc in new_claims.items():
            claims[a][d] = nc
        tally = collections.Counter(v for byday in claims.values() for v in byday.values())
        sv = v35.serve_v035(claims, graded_p)
        pa = [v for v in sv["per_account"].values() if v[0]]
        res = {"account_days": {"present": sum(tally.values()), **{k: tally.get(k, 0) for k in CLAIMS}},
               "serving_rule": {"eligible": sv["eligible"], "served": sv["served"], "blank": sv["blank"], "blank_share_percent": round(100.0 * sv["blank"] / sv["eligible"], 3),
                                "accounts_never_served": sum(1 for e, s_ in pa if s_ == 0)},
               "freed_and_holding_no_other_ungradeable_kind": freed_clean,
               "account_day_outcomes": {k: oc_counts[k] for k in OUTC}, "at_prior_day_only_and_holding_no_other_ungradeable_kind": prior_clean,
               "row_outcomes": dict(row_out), "account_days_holding_such_a_security": len(ad), "_flagged_by_one_reading_only": dict(dirn)}
        return res, cls, nav, rows_by_sec, guard_rows_by_sec

    s1, cls7, nav7, rows7, _ = sizing(False, None)
    s2, _, _, rows7g, guard7 = sizing(False, same)
    s3, cls8, nav8, rows8g, guard8 = sizing(True, same)
    s2c, _, _, _, guard7c = sizing(False, cent)
    s3c, _, _, _, guard8c = sizing(True, cent)
    ec = P["tally_cash"]
    same_days = {k: ec.get(k, 0) for k in CLAIMS} == {k: EXPECTED_CASH[k] for k in CLAIMS} and ec["present"] == EXPECTED_CASH["present"] and bool(P["same_cash"])
    reproduces_442 = (all(s1["account_days"][k] == EXPECTED_442[k] for k in CLAIMS + ("present",)) and
                      all(s1["serving_rule"][k] == EXPECTED_442[k] for k in ("eligible", "served", "blank", "blank_share_percent", "accounts_never_served")) and
                      s1["freed_and_holding_no_other_ungradeable_kind"] == EXPECTED_442["freed"])

    # ---- what the guard costs in the seven admitted types
    cent_dir = collections.Counter()

    def day_stats(cls, nav, only):
        """85-day basis: per security with bars (class admitted_type_with_bars and `only(c)`), the days on which both the day's and the prior day's bar exist and the days they are equal."""
        res = {}
        for c in secs:
            if cls[c] != "admitted_type_with_bars" or not only(c):
                continue
            n = u = uc = 0
            for d in graded_p:
                a_, b_ = nav[c].get(day_int(d)), nav[c].get(day_int(prev_of[d]))
                if a_ is not None and b_ is not None:
                    n += 1
                    u += 1 if same(a_, b_) else 0
                    uc += 1 if cent(a_, b_) else 0
                    cent_dir["rel_only"] += 1 if same(a_, b_) and not cent(a_, b_) else 0
                    cent_dir["cent_only"] += 1 if cent(a_, b_) and not same(a_, b_) else 0
            res[c] = (n, u, uc)
        return res
    seven_ds = day_stats(cls7, nav7, lambda c: True)
    pair_of = R["sec_pair"]
    held_days = collections.defaultdict(set)
    for (a, d), r in ad.items():
        for cu, _ in r["rows"]:
            if cls7[cu] == "admitted_type_with_bars":
                held_days[cu].add(d)
    sec_days_not_graded = sum(u for n, u, uc in seven_ds.values())
    sec_days_not_graded_cent = sum(uc for n, u, uc in seven_ds.values())
    held_not_graded = 0
    for c in held_days:
        for d in held_days[c]:
            a_, b_ = nav7[c].get(day_int(d)), nav7[c].get(day_int(prev_of[d]))
            if a_ is not None and b_ is not None and same(a_, b_):
                held_not_graded += 1
    carry = sorted(((guard7[c], c) for c in guard7), key=lambda x: (-x[0], sec_t2[x[1]]))
    most = [{"ticker": sec_t2[c], "type": pair_of[c], "row_days_not_graded": n, "rows_of_this_security": rows7g[c], "days_unmoved_of_days_with_both_bars": "%d of %d" % (seven_ds[c][1], seven_ds[c][0])}
            for n, c in carry[:10]]
    over_half = sorted(({"ticker": sec_t2[c], "type": pair_of[c], "days_with_both_bars": n, "days_unmoved": u, "row_days_not_graded": guard7.get(c, 0)} for c, (n, u, uc) in seven_ds.items() if n and u * 2 > n),
                       key=lambda x: (-x["days_unmoved"] / x["days_with_both_bars"], x["ticker"]))
    row_days_not_graded = sum(guard7.values())
    cost = {"row_days_not_graded": row_days_not_graded,
            "row_days_of_admitted_type_securities_outside_the_first_witness": sum(rows7g.values()),
            "security_days_not_graded": sec_days_not_graded,
            "security_days_not_graded_basis": "over the 85 graded days: security-days of the %d admitted-type securities outside the first witness that have bars, on which the reader has a bar for the day and for the prior trading day and the two are equal (relative 1e-4); %d security-days are such days in all" % (
                len(seven_ds), sum(n for n, u, uc in seven_ds.values())),
            "security_days_not_graded_on_days_an_account_holds_it": held_not_graded,
            "securities_with_a_row_not_graded": len(guard7),
            "account_days_no_longer_freed": s1["freed_and_holding_no_other_ungradeable_kind"] - s2["freed_and_holding_no_other_ungradeable_kind"],
            "account_days_no_longer_freed_all_kinds": s1["account_day_outcomes"][OUTC[3]] - s2["account_day_outcomes"][OUTC[3]],
            "securities_carrying_most": most,
            "securities_ungraded_on_more_than_half_their_days": over_half,
            "securities_ungraded_on_more_than_half_their_days_basis": "days_unmoved of days_with_both_bars over the 85 graded days; the type pair is the source's own"}
    # ---- the institutional class under the guard
    inst_secs = [c for c in secs if sec_cls0[c] == "left_out_type_inst"]
    inst_bars = [c for c in inst_secs if cls8[c] == "admitted_type_with_bars"]
    inst_rows = sum(rows8g[c] for c in inst_secs if c in rows8g)
    inst_guard = sum(guard8.get(c, 0) for c in inst_secs)
    seven_cent_dir = dict(cent_dir)
    inst_ds = day_stats(cls8, nav8, lambda c: sec_cls0[c] == "left_out_type_inst")
    inst_over_half = sorted(({"ticker": sec_t2[c], "type": pair_of[c], "days_with_both_bars": n, "days_unmoved": u} for c, (n, u, uc) in inst_ds.items() if n and u * 2 > n),
                            key=lambda x: (-x["days_unmoved"] / x["days_with_both_bars"], x["ticker"]))
    inst_no_bar_rows = sum(1 for (a, d), r in ad.items() for cu, _ in r["rows"] if cu in inst_secs and cls8[cu] != "admitted_type_with_bars")
    inst_block = {"pair": "%s / Inst" % prep.RIC, "securities_outside_the_first_witness": len(inst_secs), "securities_with_bars": len(inst_bars),
                  "securities_whose_ticker_returned_nothing": len(inst_secs) - len(inst_bars),
                  "row_days": inst_rows + inst_no_bar_rows, "row_days_with_no_bar": inst_no_bar_rows, "row_days_with_a_bar": inst_rows,
                  "row_days_graded": inst_rows - inst_guard, "row_days_the_guard_leaves_ungraded": inst_guard,
                  "row_days_graded_basis": "a row of an institutional-class security outside the first witness is graded when the reader has a bar for the day and for the prior trading day and the two are not equal; it is then equals_day_only, equals_prior_day_only or equals_neither",
                  "security_days_not_graded": sum(u for n, u, uc in inst_ds.values()), "security_days_with_both_bars": sum(n for n, u, uc in inst_ds.values()),
                  "securities_ungraded_on_more_than_half_their_days": inst_over_half,
                  "account_days_freed_by_adding_it": s3["freed_and_holding_no_other_ungradeable_kind"] - s2["freed_and_holding_no_other_ungradeable_kind"]}
    # ---- the to-the-cent variant
    cent_block = {"meaning": "the guard's equality read to the cent (both bars rounded to 2 decimals, equal) instead of relative 1e-4; the sizing's mark-to-bar tolerance is unchanged",
                  "table1_security_days_not_graded_relative": rel_tot[GUARD], "table1_security_days_not_graded_to_the_cent": cent_tot[GUARD],
                  "table1_net_security_days_cent_less_relative": cent_tot[GUARD] - rel_tot[GUARD],
                  "table1_security_days_ungraded_by_the_relative_reading_and_not_by_the_cent": sum(dir_rel_only.values()),
                  "table1_security_days_ungraded_by_the_cent_reading_and_not_by_the_relative": sum(dir_cent_only.values()),
                  "table1_net_by_type_cent_less_relative": cent_net,
                  "table1_one_day_off_to_the_cent_under_the_guard": cent_tot["one_day_off"],
                  "seven_types_outside_the_first_witness": {
                      "security_days_not_graded_relative": sec_days_not_graded, "security_days_not_graded_to_the_cent": sec_days_not_graded_cent,
                      "net_security_days_cent_less_relative": sec_days_not_graded_cent - sec_days_not_graded,
                      "security_days_ungraded_by_the_relative_reading_and_not_by_the_cent": seven_cent_dir.get("rel_only", 0),
                      "security_days_ungraded_by_the_cent_reading_and_not_by_the_relative": seven_cent_dir.get("cent_only", 0),
                      "row_days_not_graded_relative": row_days_not_graded, "row_days_not_graded_to_the_cent": sum(guard7c.values()),
                      "net_row_days_cent_less_relative": sum(guard7c.values()) - row_days_not_graded,
                      "row_days_flagged_by_the_relative_reading_only": s2["_flagged_by_one_reading_only"].get("relative_only", 0),
                      "row_days_flagged_by_the_cent_reading_only": s2["_flagged_by_one_reading_only"].get("cent_only", 0),
                      "freed_and_holding_no_other_ungradeable_kind_to_the_cent": s2c["freed_and_holding_no_other_ungradeable_kind"],
                      "blank_share_percent_to_the_cent": s2c["serving_rule"]["blank_share_percent"]},
                  "seven_types_and_inst_under_the_guard_to_the_cent": {
                      "freed_and_holding_no_other_ungradeable_kind": s3c["freed_and_holding_no_other_ungradeable_kind"],
                      "blank_share_percent": s3c["serving_rule"]["blank_share_percent"], "accounts_never_served": s3c["serving_rule"]["accounts_never_served"]}}
    # ---- fetch record and control
    ticks = [t for c_ in calls for t in c_["ticker_list"]]
    fetch = {"calls": [{"call": c_["call"], "tickers": c_["tickers"], "with_bars": c_["with_bars"], "no_bars": c_["no_bars"], "rate_limited_not_read": c_["rate_limited_not_read"]} for c_ in calls],
             "call_count": len(calls), "distinct_tickers_asked": sum(c_["tickers"] for c_ in calls),
             "tickers_asked_more_than_once": len([t for t, n in collections.Counter(ticks).items() if n > 1]),
             "tickers_with_bars": sum(c_["with_bars"] for c_ in calls), "tickers_with_no_bars": sum(c_["no_bars"] for c_ in calls),
             "counted_before_fetching": meta, "window": "2026-06-05 to 2026-10-13 (end exclusive 2026-10-14)", "pause_between_calls_seconds": 8, "reader_internal_pause_seconds": 6, "parallel_calls": 0,
             "reader": "fetch_yahoo (data/assets/scripts/silver/commonwealth_price_basis_census.py) / read_yahoo_close (data/assets/scripts/silver/commonwealth_daily_valuation.py), neither edited; unadjusted Close"}
    ctl = control_run()
    assumed = ("A SIZING, not a stamp: IF every account-day that holds, outside the first witness, only securities graded by the second witness at the day's close took the claim its rows give "
               "(IB-pr-442's rule, imported unchanged: ACCT_OWN_DATE unless an anchor-graded row says ACCT_PRIOR_DATE; prior-day-only rows read ACCT_PRIOR_DATE), with the one added rule that a "
               "security-day on which the reader's own bar equals its bar for the prior trading day gets no grade and blocks its account-day, the claim counts and the serving rule would read as below; "
               "every other account-day keeps the claim it has under the cash rule in force, and nothing is re-graded or admitted in the product.")
    for s_ in (s1, s2, s3, s2c, s3c):
        s_.pop("_flagged_by_one_reading_only", None)
    doc = {
        "same_account_days_read": bool(same_days),
        "same_account_days_read_basis": "this run's totals under the cash rule: %s; IB-pr-442's: UNGRADEABLE 43,310; ACCT_PRIOR_DATE 55; ACCT_OWN_DATE 19,832; NOTHING_TO_GRADE 13,599; present 76,796" % dict(ec),
        "guard_rule_in_words": GUARD_RULE + " Read to the cent (both bars rounded to 2 decimals) instead: the overlap table un-grades %d security-days (relative 1e-4: %d; %d un-graded only by the cent reading, %d only by the relative one), and the seven types outside the first witness %d security-days (relative: %d; %d only by the cent reading, %d only by the relative one)." % (
            cent_tot[GUARD], rel_tot[GUARD], sum(dir_cent_only.values()), sum(dir_rel_only.values()), sec_days_not_graded_cent, sec_days_not_graded,
            seven_cent_dir.get("cent_only", 0), seven_cent_dir.get("rel_only", 0)),
        "guard_off_reproduces_ib_pr_441": {"reproduces": bool(reproduces), "per_type_equal_to_ib138_2_table_1": bool(per_type_equal), "totals_with_the_guard_off": off_tot,
                                           "expected": EXPECTED_441, "expected_source": "IB-pr-441's Table 1 (IB138-2_type_overlap_and_fund_check.json, deliverables/0.9.0_WK_IRPT_BCKEND~299)"},
        "seven_types_no_guard_reproduces_ib_pr_442": {"reproduces": bool(reproduces_442), "expected": EXPECTED_442, "read": {"account_days": s1["account_days"], "serving_rule": s1["serving_rule"],
                                                                                                                            "freed_and_holding_no_other_ungradeable_kind": s1["freed_and_holding_no_other_ungradeable_kind"]}},
        **table1_block,
        "to_the_cent_variant": cent_block,
        "sizings": {"seven_types_no_guard": s1, "seven_types_under_the_guard": s2, "seven_types_and_inst_under_the_guard": s3},
        "what_is_assumed": assumed,
        "guard_cost_in_the_seven_types": cost,
        "inst_under_the_guard": inst_block,
        "fetch": fetch,
        "control": {"planted": PLANTED, "read": ctl,
                    "what_it_is": "one security over five graded days whose reader bar repeats on day 3 (plus a variant where the anchor moves on day 3, the dangerous direction), run through the same label_day / grade_row / day_outcome functions as the real run; an account-day holding it on day 3 is not freed, on days 2 and 4 it is"},
        "claims_regraded_in_product": False, "other_sources_asked": 0, "classes_admitted_by_this_cell": 0,
    }
    if not same_days:
        doc["source_difference_explained"] = "the totals under the cash rule differ from IB-pr-442's: see same_account_days_read_basis"
    cost2 = cost
    out.write_text(json.dumps(doc, indent=1, default=str), encoding="utf-8")
    print("wrote", out, "control equal", ctl == PLANTED, "guard-off reproduces", reproduces, per_type_equal, "442 reproduces", reproduces_442, "same days", same_days)
    print("table1 guard-off", off_tot)
    print("table1 under guard", rel_tot)
    for n_, s_ in (("no_guard", s1), ("guard", s2), ("guard+inst", s3)):
        print(n_, s_["account_days"], s_["serving_rule"], s_["freed_and_holding_no_other_ungradeable_kind"])
    print("cost", {k: cost2[k] for k in ("row_days_not_graded", "security_days_not_graded", "account_days_no_longer_freed")})
    return 0


if __name__ == "__main__":
    sys.exit(main())
