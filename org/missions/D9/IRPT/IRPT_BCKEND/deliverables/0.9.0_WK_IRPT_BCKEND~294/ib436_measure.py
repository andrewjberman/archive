#!/usr/bin/env python3
"""IB-pr-436: nine mutual funds by 85 trading days -- the custodian's MARK of each fund-day against an independent daily NAV (Yahoo, unadjusted Close).
Read only.  Same source partitions (the cache of ib433_fetch.py, outside the repo, AccountID already a 12-character one-way digest), same price rule
(Market Value / Units, the existing row filter), same tolerance (1e-4 relative), same trading-day axis (lib/trading_calendar.py), same row typing and ordered
claim rule (ib429_claims / ib429_claims_v035 imported UNCHANGED; the cash rule is ib435_measure's own functions, imported UNCHANGED).

    python -I ib436_measure.py <partition_cache> <yahoo_cache> <out.json>      measure and write the counts (no account key is ever written)
    python -I ib436_measure.py --control                                       run only the planted classifier control

OUTCOME of one fund-day (mark m = the fund-day's chosen mark; N = the NAV of the day; P = the NAV of the prior trading day; eq = relative 1e-4):
  no_nav_found                 N or P is not in the reader's series (both are needed to say which one the mark equals)
  equals_both_nav_unchanged    m eq N and m eq P and N eq P  (the NAV did not move; the mark cannot say which day)
  equals_day_nav_only          m eq N and not m eq P
  equals_prior_day_nav_only    m eq P and not m eq N
  equals_neither               otherwise (including m eq N and m eq P with N not eq P: the tolerance cannot tell them apart; counted and reported)
MANY MARKS: the rows of one fund-day are clustered by eq (single linkage on the sorted prices); the mark is the median of the cluster holding the MOST rows;
a tie goes to the LOWER mark.  fund_days_with_more_than_one_mark counts the fund-days with two or more clusters.
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
sys.path.insert(0, str(HERE.parent / "0.9.0_WK_IRPT_BCKEND~288"))    # ib429_claims / ib429_claims_v035: the merged copies, read, not written (byte-identical to the ~293 branch)
import ib429_claims as old  # noqa: E402
import ib429_claims_v035 as v35  # noqa: E402
import ib435_measure as m435  # noqa: E402

FUNDS = ["FLCOX", "MFEIX", "CEMIX", "FSGGX", "FSMAX", "FXNAX", "FSPGX", "CDSIX", "FPNIX"]
CUSIP = {"FLCOX": "31635V679", "MFEIX": "552985863", "CEMIX": "149498107", "FSGGX": "316146315", "FSMAX": "315911743",
         "FXNAX": "316146356", "FSPGX": "31635V729", "CDSIX": "13161T401", "FPNIX": "30254T643"}   # IB-pr-435's ranking, rows 1-9
OF_CUSIP = {v: k for k, v in CUSIP.items()}
PARTS = ("equals_day_nav_only", "equals_prior_day_nav_only", "equals_both_nav_unchanged", "equals_neither", "no_nav_found")
BY_DAY_KEY = {"equals_day_nav_only": "day", "equals_prior_day_nav_only": "prior", "equals_both_nav_unchanged": "both", "equals_neither": "neither", "no_nav_found": "none"}
EXPECTED_V035 = m435.EXPECTED_V035
ONE_CENT = 0.01
CONTROL_TICKER = "VTI"
EPOCH = dt.date(1970, 1, 1)


def classify(mark, nav_d, nav_p):
    """One of PARTS.  mark, nav_d, nav_p are floats or None (None NAV -> no_nav_found)."""
    if nav_d is None or nav_p is None:
        return "no_nav_found"
    e_d, e_p, e_n = old.same(mark, nav_d), old.same(mark, nav_p), old.same(nav_d, nav_p)
    if e_d and e_p and e_n:
        return "equals_both_nav_unchanged"
    if e_d and not e_p:
        return "equals_day_nav_only"
    if e_p and not e_d:
        return "equals_prior_day_nav_only"
    return "equals_neither"


def choose_mark(prices):
    """-> (mark, number of clusters, tie).  Clusters: sorted prices, a price joins the running cluster when it is eq the cluster's first price (single linkage on the
    previous price).  The cluster with the most rows wins; a tie goes to the lower mark."""
    ps = sorted(prices)
    clusters = []
    for p in ps:
        if clusters and old.same(clusters[-1][-1], p):
            clusters[-1].append(p)
        else:
            clusters.append([p])
    best = max(len(c) for c in clusters)
    top = [c for c in clusters if len(c) == best]
    c = top[0]    # clusters are in ascending price order: the lower mark
    s = sorted(c)
    med = s[len(s) // 2] if len(s) % 2 else 0.5 * (s[len(s) // 2 - 1] + s[len(s) // 2])
    return med, len(clusters), len(top) > 1


def within_one_cent(mark, nav_d, nav_p):
    return any(n is not None and abs(mark - n) <= ONE_CENT + 1e-9 for n in (nav_d, nav_p))


# ---------------------------------------------------------------------------- the planted control (classifier + mark rule)

def control_run():
    """Fixture: NAV day 10.00, NAV prior 9.90 unless stated.  Known by construction (by hand)."""
    r = {
        "day": classify(10.00, 10.00, 9.90),
        "prior": classify(9.90, 10.00, 9.90),
        "both_unchanged": classify(10.00, 10.00, 10.00),
        "neither": classify(10.50, 10.00, 9.90),
        "no_day_nav": classify(10.00, None, 9.90),
        "no_prior_nav": classify(10.00, 10.00, None),
        "inside_tolerance": classify(10.00 + 5e-4, 10.00, 9.90),      # 5e-5 relative: equal to the day NAV
        "just_outside_tolerance": classify(10.00 + 2e-3, 10.00, 9.90),  # 2e-4 relative: not equal
        "mark_majority": choose_mark([10.0, 10.0, 10.0, 9.9, 9.9]),
        "mark_tie_lower": choose_mark([10.0, 10.0, 9.9, 9.9]),
        "mark_one_cluster": choose_mark([10.0, 10.0 + 1e-5, 10.0 - 1e-5]),
        "one_cent": (within_one_cent(10.005, 10.00, 9.90), within_one_cent(10.05, 10.00, 9.90)),
    }
    return r


PLANTED = {
    "day": "equals_day_nav_only", "prior": "equals_prior_day_nav_only", "both_unchanged": "equals_both_nav_unchanged", "neither": "equals_neither",
    "no_day_nav": "no_nav_found", "no_prior_nav": "no_nav_found", "inside_tolerance": "equals_day_nav_only", "just_outside_tolerance": "equals_neither",
    "mark_majority": (10.0, 2, False), "mark_tie_lower": (9.9, 2, True), "mark_one_cluster": (10.0, 1, False), "one_cent": (True, False),
}


# ---------------------------------------------------------------------------- the measurement

def day_int(iso):
    return (dt.date.fromisoformat(iso) - EPOCH).days


def main():
    if sys.argv[1:] == ["--control"]:
        r = control_run()
        print(json.dumps(r, indent=1), "\nEQUAL:", r == PLANTED)
        return 0 if r == PLANTED else 1
    cache, ycache, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    root = HERE.parents[6]
    sys.path[:0] = [str(root / "lib"), str(root), str(root / "data/assets/scripts/silver"), str(root / "data/assets/scripts/analysis")]
    import trading_calendar as tc
    import commonwealth_daily_valuation as dv

    # --- the NAV series (the reader's own function; unadjusted Close) ---
    nav = {}
    for t in FUNDS + [CONTROL_TICKER]:
        s, as_of = dv.read_yahoo_close(ycache, t)
        nav[t] = (None if s is None else {int(i): float(v) for i, v in s.items()}, as_of)

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

    graded, tally_pre = [], collections.Counter()
    fund_day_rows = collections.defaultdict(list)       # (ticker, day) -> [mark of each priced row]
    # account-day structure (no key kept beyond the loop): per account-day the outside-anchor cusip set, the fund rows' marks, the other-kind flag
    ad_effect = []      # one record per account-day with an outside-anchor row, after the cash rule: (set of cusips, [(ticker, mark)], other_kind, day)
    ad_effect_pre = []  # same on the pre-cash-rule typing
    landing = {}
    prev_of = {}
    for i, d in enumerate(tdays):
        p = tc.prev_trading_day(dt.date.fromisoformat(d)).isoformat()
        s = load("src", d)
        A, B = anchor(d), anchor(p)
        if s in (None, "UNREAD") or A == "UNREAD" or B == "UNREAD":
            continue
        if i == 0 or tdays[i - 1] != p:
            continue
        if A is None or B is None:
            A, B = (None, None)
        graded.append(d)
        prev_of[d] = p
        landing[d] = s.get("_meta", {})
        sp = load("src", p)
        pidx = m435.prior_index(sp if sp not in (None, "UNREAD") else None)
        types = v35.typed_rows(s["CUSIP"], s["Market Value"], s["Units"], s["Cash Equivalent"], A, B)
        accts = s["AccountID"]
        priced = old.price_rows(s["CUSIP"], s["Market Value"], s["Units"])
        outcomes = collections.defaultdict(list)
        out_rows = collections.defaultdict(list)       # account -> [(cusip, price)] outside-anchor rows (pre-cash typing)
        cash_rows = collections.defaultdict(list)      # account -> [(cusip, price, outcome)]
        for k, t in enumerate(types):
            a = accts[k]
            if k in priced and priced[k][0] in OF_CUSIP:
                fund_day_rows[(OF_CUSIP[priced[k][0]], d)].append(priced[k][1])
            if t == "outside_anchor":
                out_rows[a].append(priced[k])
            elif t == "cash_priced_outside_anchor":
                c, price = priced[k]
                o = m435.cash_outcome(a, c, price, pidx)
                outcomes[a].append(o)
                cash_rows[a].append((c, price, o))
        rec = old.account_day_records(accts, types)
        for a, c in rec.items():
            pre, kinds = v35.claim_v035(c)
            tally_pre["present"] += 1
            tally_pre[pre] += 1
            c1 = m435.reclassify(c, outcomes.get(a, []))
            _cl1, k1 = v35.claim_v035(c1)
            other_pre = any(kk != "OUTSIDE_ANCHOR" for kk in kinds)
            other_cash = any(kk != "OUTSIDE_ANCHOR" for kk in k1)
            rows_pre = list(out_rows.get(a, []))
            rows_cash = rows_pre + [(cu, pr) for cu, pr, o in cash_rows.get(a, []) if o != "equal"]
            if rows_pre:
                ad_effect_pre.append((frozenset(cu for cu, _ in rows_pre), [(OF_CUSIP[cu], pr) for cu, pr in rows_pre if cu in OF_CUSIP], other_pre, d))
            if rows_cash:
                ad_effect.append((frozenset(cu for cu, _ in rows_cash), [(OF_CUSIP[cu], pr) for cu, pr in rows_cash if cu in OF_CUSIP], other_cash, d))
    same_read = {k: tally_pre[k] for k in EXPECTED_V035} == EXPECTED_V035

    # --- NAVs the fund-days need ---
    def nav_on(t, iso):
        s = nav[t][0]
        return None if s is None else s.get(day_int(iso))

    funds_out, by_day = [], {d: {"day": 0, "prior": 0, "both": 0, "neither": 0, "none": 0} for d in graded}
    fd_outcome, fd_info = {}, {}      # (ticker, day) -> outcome ; -> (mark, nav_d, nav_p)
    ties = 0
    prior_by_dow = collections.Counter()
    day_by_dow = collections.Counter()
    for t in FUNDS:
        row = {"ticker": t, "cusip": CUSIP[t], "fund_days_with_a_mark": 0, "fund_days_with_more_than_one_mark": 0, "fund_days_mark_tie": 0}
        row.update(dict.fromkeys(PARTS, 0))
        row["equals_neither_within_one_cent"] = 0
        row["equals_neither_within_one_cent_of_either_nav"] = 0
        needed, found = set(), set()
        for d in graded:
            prices = fund_day_rows.get((t, d))
            if not prices:
                continue
            mark, ncl, tie = choose_mark(prices)
            row["fund_days_with_a_mark"] += 1
            row["fund_days_with_more_than_one_mark"] += int(ncl > 1)
            row["fund_days_mark_tie"] += int(tie)
            p = prev_of[d]
            nd, npr = nav_on(t, d), nav_on(t, p)
            needed.update((d, p))
            for x, v in ((d, nd), (p, npr)):
                if v is not None:
                    found.add(x)
            o = classify(mark, nd, npr)
            fd_outcome[(t, d)] = o
            fd_info[(t, d)] = (mark, nd, npr)
            row[o] += 1
            by_day[d][BY_DAY_KEY[o]] += 1
            if o == "equals_neither" and within_one_cent(mark, nd, npr):
                row["equals_neither_within_one_cent"] += 1
            dow = dt.date.fromisoformat(d).strftime("%a")
            if o == "equals_prior_day_nav_only":
                prior_by_dow[dow] += 1
            if o == "equals_day_nav_only":
                day_by_dow[dow] += 1
        row["equals_neither_within_one_cent_of_either_nav"] = row["equals_neither_within_one_cent"]
        row["nav_days_needed"] = len(needed)
        row["nav_days_found"] = len(found)
        ties += row["fund_days_mark_tie"]
        funds_out.append(row)
    totals = {k: sum(r[k] for r in funds_out) for k in PARTS}

    # --- row-level (each priced row of a fund-day against the two NAVs): shows whether the accounts agree inside a fund-day ---
    row_level = collections.Counter()
    rl_fund = collections.defaultdict(collections.Counter)
    rl_day = collections.defaultdict(collections.Counter)      # day -> Counter of the row outcomes (rows of the eight funds with a NAV)
    rl_prior_fund_day = collections.Counter()
    for (t, d), prices in fund_day_rows.items():
        if t not in FUNDS:
            continue
        nd, npr = nav_on(t, d), nav_on(t, prev_of[d])
        for pr in prices:
            o = classify(pr, nd, npr)
            row_level[o] += 1
            rl_fund[t][o] += 1
            rl_day[d][o] += 1
            if o == "equals_prior_day_nav_only":
                rl_prior_fund_day[(t, d)] += 1

    # --- the account-day effect (an upper bound; nothing re-graded).  Row-level: each fund row of the account-day against its own NAVs. ---
    def effect(recs):
        e = {"account_days_whose_only_outside_anchor_rows_are_these_funds": 0, "every_mark_equals_day_nav_or_both": 0,
             "one_or_more_equals_prior_day_only": 0, "one_or_more_neither_or_no_nav": 0, "of_those_holding_no_other_ungradeable_kind": 0}
        for cus, frows, other, d in recs:
            if not cus or any(c not in OF_CUSIP for c in cus):
                continue
            e["account_days_whose_only_outside_anchor_rows_are_these_funds"] += 1
            outs = [classify(pr, nav_on(tk, d), nav_on(tk, prev_of[d])) for tk, pr in frows]
            if any(o in ("equals_neither", "no_nav_found") for o in outs):
                e["one_or_more_neither_or_no_nav"] += 1
            elif any(o == "equals_prior_day_nav_only" for o in outs):
                e["one_or_more_equals_prior_day_only"] += 1
            else:
                e["every_mark_equals_day_nav_or_both"] += 1
                if not other:
                    e["of_those_holding_no_other_ungradeable_kind"] += 1
        return e

    eff, eff_pre = effect(ad_effect), effect(ad_effect_pre)
    # the same, with the funds whose NAV could not be found (FPNIX) set aside: what the answer is where a NAV was found
    def effect_found(recs):
        e = {"account_days": 0, "every_mark_equals_day_nav_or_both": 0, "one_or_more_equals_prior_day_only": 0, "one_or_more_neither_or_no_nav": 0, "no_other_kind_in_first": 0}
        for cus, frows, other, d in recs:
            if not cus or any(c not in OF_CUSIP for c in cus) or any(OF_CUSIP[c] == "FPNIX" for c in cus):
                continue
            e["account_days"] += 1
            outs = [classify(pr, nav_on(tk, d), nav_on(tk, prev_of[d])) for tk, pr in frows]
            if any(o in ("equals_neither", "no_nav_found") for o in outs):
                e["one_or_more_neither_or_no_nav"] += 1
            elif any(o == "equals_prior_day_nav_only" for o in outs):
                e["one_or_more_equals_prior_day_only"] += 1
            else:
                e["every_mark_equals_day_nav_or_both"] += 1
                e["no_other_kind_in_first"] += int(not other)
        return e

    eff_found = effect_found(ad_effect)

    # --- the control: a security the anchor carries on every day ---
    ctl_cusip = "922908769"      # VTI, chosen from the anchor-carried, held-every-day set (see the read file)
    ctl = {"days_compared": 0, "days_equal": 0, "days_equal_to_yahoo_prior_close": 0, "days_equal_to_neither": 0, "days_anchor_absent": 0, "days_reader_absent": 0}
    ctl_diff_rel = []
    ctl_neither = []
    for d in graded:
        A = anchor(d)
        a = None if A in (None, "UNREAD") else A.get(ctl_cusip)
        y, yp = nav_on(CONTROL_TICKER, d), nav_on(CONTROL_TICKER, prev_of[d])
        if a is None:
            ctl["days_anchor_absent"] += 1
            continue
        if y is None:
            ctl["days_reader_absent"] += 1
            continue
        ctl["days_compared"] += 1
        if old.same(a, y):
            ctl["days_equal"] += 1
        elif yp is not None and old.same(a, yp):
            ctl["days_equal_to_yahoo_prior_close"] += 1
        else:
            ctl["days_equal_to_neither"] += 1
            ctl_neither.append((d, a, y))
        ctl_diff_rel.append(abs(a - y) / max(a, y))
    ctl["max_relative_difference"] = max(ctl_diff_rel) if ctl_diff_rel else None
    ctl["neither_days_max_relative_difference_to_same_day"] = max([abs(a - y) / max(a, y) for _, a, y in ctl_neither], default=0.0)

    # --- the existing ADVI_COTBKF cache, read only: what it already held for the nine (checked against the reader's own series) ---
    held = {}
    import subprocess   # the MAIN checkout is the parent of this worktree's common git dir (derived, not typed)
    common = subprocess.run(["git", "-C", str(root), "rev-parse", "--path-format=absolute", "--git-common-dir"], capture_output=True, text=True, check=True).stdout.strip()
    main_census = Path(common).parent / ".scratch" / "advi_cotbkf" / "yahoo_census"
    for t in FUNDS:
        s, as_of = dv.read_yahoo_close(main_census, t)
        if s is None:
            f = main_census / (t + ".csv")
            held[t] = "none_reason marker" if f.is_file() else "no file"
            continue
        mine = nav[t][0] or {}
        common = [x for x in mine if x in s.index]
        held[t] = {"rows": int(len(s)), "first": (EPOCH + dt.timedelta(days=int(s.index.min()))).isoformat(), "last": (EPOCH + dt.timedelta(days=int(s.index.max()))).isoformat(),
                   "file_date": as_of, "dates_in_common_with_this_fetch": len(common), "of_which_equal_close": sum(1 for x in common if old.same(float(s[x]), mine[x]))}

    # --- internal evidence on the date question: landing time of the partition against the day/prior split ---
    dayrec = []
    for d in graded:
        b = by_day[d]
        m = landing.get(d, {})
        dayrec.append((d, b["day"], b["prior"], b["both"], b["neither"], b["none"], m.get("first_modified_utc"), m.get("last_modified_utc")))
    prior_rows_by_day = {d: rl_day[d]["equals_prior_day_nav_only"] for d in graded if rl_day[d]["equals_prior_day_nav_only"]}
    neither_rows_by_day = {d: rl_day[d]["equals_neither"] for d in graded if rl_day[d]["equals_neither"]}
    rows_with_nav_by_day = {d: sum(v for k, v in rl_day[d].items() if k != "no_nav_found") for d in graded}

    def hour(iso):
        return None if not iso else dt.datetime.fromisoformat(iso).astimezone(dt.timezone.utc).hour + dt.datetime.fromisoformat(iso).astimezone(dt.timezone.utc).minute / 60.0

    def med(xs):
        xs = sorted(x for x in xs if x is not None)
        return None if not xs else xs[len(xs) // 2]
    land = {"days_with_prior_rows": len(prior_rows_by_day), "days_without": len(graded) - len(prior_rows_by_day),
            "median_last_modified_utc_hour_days_with_prior_rows": med(hour(landing[d].get("last_modified_utc")) for d in prior_rows_by_day),
            "median_last_modified_utc_hour_days_without": med(hour(landing[d].get("last_modified_utc")) for d in graded if d not in prior_rows_by_day),
            "median_first_modified_utc_hour_days_with_prior_rows": med(hour(landing[d].get("first_modified_utc")) for d in prior_rows_by_day),
            "median_first_modified_utc_hour_days_without": med(hour(landing[d].get("first_modified_utc")) for d in graded if d not in prior_rows_by_day)}
    prior_fd = sorted(rl_prior_fund_day.items(), key=lambda kv: -kv[1])

    doc = {
        "same_account_days_read": same_read, "v035_totals_read": {k: tally_pre[k] for k in EXPECTED_V035}, "graded_days": len(graded),
        "first_graded_day": graded[0], "last_graded_day": graded[-1],
        "funds": funds_out, "totals": totals,
        "many_marks_rule": choose_mark.__doc__.strip().split("\n")[0] + " fund_days_mark_tie counts the fund-days where two clusters tied for the most rows.",
        "fund_days_mark_ties": ties,
        "tolerance": "relative 1e-4: abs(a - b) <= 1e-4 * max(abs(a), abs(b)) (the instrument's own, ib429_claims.same); the one-cent count is reported beside, not used for the five outcomes",
        "tolerance_works_for_cent_quoted_navs": "yes: a one-cent NAV step on a NAV of about 10 is 1e-3 relative, ten times the tolerance, so a day-to-day move of one cent is told apart; a move smaller than the tolerance is the unchanged case",
        "nav_source": {"name": "Yahoo Finance (yfinance.download, auto_adjust=False), one call for the nine funds and the control", "read_by": "fetch_yahoo(tickers, start, end, cache_dir) in data/assets/scripts/silver/commonwealth_price_basis_census.py; read_yahoo_close(cache_dir, ticker) in data/assets/scripts/silver/commonwealth_daily_valuation.py (unadjusted Close)",
                       "adjusted": False, "first_date": "2026-06-08", "last_date": "2026-10-09", "requested_window": "2026-06-08 to 2026-10-10 (end exclusive)",
                       "navs_read_as_of_file_date": {t: nav[t][1] for t in FUNDS + [CONTROL_TICKER]}, "cache_already_held": held},
        "row_level_outcomes": dict(row_level),
        "row_level_outcomes_by_fund": {t: dict(c) for t, c in rl_fund.items()},
        "row_level_prior_rows_by_day": prior_rows_by_day, "row_level_neither_rows_by_day": neither_rows_by_day, "row_level_rows_with_a_nav_by_day": rows_with_nav_by_day,
        "row_level_prior_fund_days": len(rl_prior_fund_day), "row_level_prior_rows_top_fund_days": [[t, d, n] for (t, d), n in prior_fd[:10]],
        "landing_time_of_partitions": land,
        "by_day": {d: by_day[d] for d in graded},
        "prior_day_outcomes_by_weekday": dict(prior_by_dow), "day_nav_outcomes_by_weekday": dict(day_by_dow),
        "control": {"security": "%s (CUSIP %s)" % (CONTROL_TICKER, ctl_cusip), "carried_by_anchor": True, **ctl},
        "account_day_effect": eff, "account_day_effect_basis": "the cash rule of IB-pr-435 applied (the primary treatment in force); each fund row of the account-day graded by its own mark",
        "account_day_effect_before_the_cash_rule": eff_pre,
        "account_day_effect_funds_with_a_nav_only": eff_found,
        "claims_regraded": False,
    }
    out.write_text(json.dumps(doc, indent=1, default=str), encoding="utf-8")
    print("wrote", out, "graded", len(graded), "same_read", same_read, totals, "ties", ties)
    return 0


if __name__ == "__main__":
    sys.exit(main())
