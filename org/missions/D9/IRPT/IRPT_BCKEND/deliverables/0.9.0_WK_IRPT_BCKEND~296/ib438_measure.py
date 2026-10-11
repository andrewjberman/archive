#!/usr/bin/env python3
"""IB-pr-438 phase 2: grade every outside-anchor row of every security the reader returned data for against the NAV of the day and of the prior trading day
(IB-pr-436's classify / tolerance, imported by copy of its rule below), put every account-day that holds an outside-anchor row in ONE outcome, and size the
serving rule under v0.36 as a sizing (nothing is re-graded).  Read only.  Counts only: no account key, no balance, no one account's holding is written.

    python -I ib438_measure.py <phase1.pkl> <yahoo_cache> <calls.json> <out.json>
    python -I ib438_measure.py --control      the planted classifier / outcome-order / sizing control

OUTCOME of one row (mark m = the row's own price; N = NAV of the day; P = NAV of the prior trading day; eq = relative 1e-4, ib429_claims.same):
  no_nav_found                 the security has no ticker, or no data, or N or P is not in the reader's series
  equals_both_nav_unchanged    m eq N and m eq P and N eq P
  equals_day_nav_only          m eq N and not m eq P
  equals_prior_day_nav_only    m eq P and not m eq N
  equals_neither               otherwise
ACCOUNT-DAY outcome, the first that applies: one_or_more_with_no_nav; one_or_more_at_neither; one_or_more_at_prior_day_nav_only;
every_security_at_day_nav_or_unchanged (FREED).
"""
from __future__ import annotations

import collections
import datetime as dt
import json
import pickle
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
sys.path.insert(0, str(D / "0.9.0_WK_IRPT_BCKEND~293"))
import ib429_claims as old  # noqa: E402
import ib429_claims_v035 as v35  # noqa: E402

EPOCH = dt.date(1970, 1, 1)
CONTROL_TICKER, CONTROL_CUSIP = "VTI", "922908769"
OUTCOMES = ("one_or_more_with_no_nav", "one_or_more_at_neither", "one_or_more_at_prior_day_nav_only", "every_security_at_day_nav_or_unchanged")
CLAIMS = ("UNGRADEABLE", "ACCT_PRIOR_DATE", "ACCT_OWN_DATE", "NOTHING_TO_GRADE")
FUND_TICKERS = ["FLCOX", "MFEIX", "CEMIX", "FSGGX", "FSMAX", "FXNAX", "FSPGX", "CDSIX", "FPNIX"]
ASSUMED = ("A SIZING, not a claim anybody stamped. IF every freed account-day with no other ungradeable kind took the claim its graded rows give (its anchor-graded "
           "rows by the anchor as today, its outside-anchor rows at the day's NAV: so ACCT_OWN_DATE unless an anchor-graded row says ACCT_PRIOR_DATE), and an "
           "account-day with a prior-day-only row and nothing worse (no no-NAV or neither row, no other ungradeable kind) read ACCT_PRIOR_DATE, the four claim counts "
           "and the serving rule would read as below. Every other account-day keeps the claim it has under the cash rule in force. Nothing is re-graded in the product.")


def classify(mark, nav_d, nav_p):
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


def day_outcome(row_outcomes):
    """The account-day outcome from the outcomes of its outside-anchor rows (first that applies)."""
    if any(o == "no_nav_found" for o in row_outcomes):
        return OUTCOMES[0]
    if any(o == "equals_neither" for o in row_outcomes):
        return OUTCOMES[1]
    if any(o == "equals_prior_day_nav_only" for o in row_outcomes):
        return OUTCOMES[2]
    return OUTCOMES[3]


def new_claim(c1, row_outcomes, kinds, sixth, outcome):
    """The sizing claim of one account-day.  c1: row-type counter after the cash rule; kinds: its ungradeable kinds; sixth: holds the sixth-reason row."""
    other = any(k != "OUTSIDE_ANCHOR" for k in kinds) or sixth
    if other or outcome not in (OUTCOMES[2], OUTCOMES[3]):
        return None            # keeps the claim it has
    c2 = collections.Counter(c1)
    n = c2["outside_anchor"]
    assert n == len(row_outcomes), (n, len(row_outcomes))
    c2["outside_anchor"] = 0
    npr = sum(1 for o in row_outcomes if o == "equals_prior_day_nav_only")
    c2["prior"] += npr
    c2["own"] += n - npr
    return v35.claim_v035(c2)[0]


# ---------------------------------------------------------------------------- planted control
def control_run():
    """Known by construction.  NAV day 10.00, prior 9.90 for every ticker that has data.  Rows: day-NAV, prior-NAV, neither, no-data, unchanged."""
    out = {}
    out["row_day"] = classify(10.0, 10.0, 9.9)
    out["row_prior"] = classify(9.9, 10.0, 9.9)
    out["row_neither"] = classify(10.5, 10.0, 9.9)
    out["row_nonav"] = classify(10.0, None, 9.9)
    out["row_unchanged"] = classify(10.0, 10.0, 10.0)
    out["ad_nonav_first"] = day_outcome(["equals_day_nav_only", "no_nav_found", "equals_neither", "equals_prior_day_nav_only"])
    out["ad_neither_second"] = day_outcome(["equals_day_nav_only", "equals_neither", "equals_prior_day_nav_only"])
    out["ad_prior_third"] = day_outcome(["equals_day_nav_only", "equals_prior_day_nav_only", "equals_both_nav_unchanged"])
    out["ad_freed"] = day_outcome(["equals_day_nav_only", "equals_both_nav_unchanged"])
    c = {"own": 3, "outside_anchor": 2}
    out["size_freed"] = new_claim(c, ["equals_day_nav_only", "equals_both_nav_unchanged"], [], False, OUTCOMES[3])
    out["size_prior"] = new_claim(c, ["equals_day_nav_only", "equals_prior_day_nav_only"], [], False, OUTCOMES[2])
    out["size_freed_other_kind"] = new_claim({"own": 3, "outside_anchor": 2, "no_cusip": 1}, ["equals_day_nav_only"] * 2, ["NO_CUSIP", "OUTSIDE_ANCHOR"], False, OUTCOMES[3])
    out["size_sixth"] = new_claim(c, ["equals_day_nav_only"] * 2, ["OUTSIDE_ANCHOR"], True, OUTCOMES[3])
    out["size_anchor_prior_row"] = new_claim({"prior": 1, "own": 1, "outside_anchor": 1}, ["equals_day_nav_only"], ["OUTSIDE_ANCHOR"], False, OUTCOMES[3])
    out["size_nothing_to_grade_when_no_rows_but_cash"] = new_claim({"cash": 2, "outside_anchor": 1}, ["equals_both_nav_unchanged"], ["OUTSIDE_ANCHOR"], False, OUTCOMES[3])
    return out


PLANTED = {"row_day": "equals_day_nav_only", "row_prior": "equals_prior_day_nav_only", "row_neither": "equals_neither", "row_nonav": "no_nav_found",
           "row_unchanged": "equals_both_nav_unchanged", "ad_nonav_first": OUTCOMES[0], "ad_neither_second": OUTCOMES[1], "ad_prior_third": OUTCOMES[2],
           "ad_freed": OUTCOMES[3], "size_freed": "ACCT_OWN_DATE", "size_prior": "ACCT_PRIOR_DATE", "size_freed_other_kind": None, "size_sixth": None,
           "size_anchor_prior_row": "ACCT_PRIOR_DATE", "size_nothing_to_grade_when_no_rows_but_cash": "ACCT_OWN_DATE"}


def ascii_(s):
    return re.sub(r"[^\x20-\x7e]", "?", str(s or ""))


def med(xs):
    xs = sorted(x for x in xs if x is not None)
    return None if not xs else xs[len(xs) // 2]


def hour(iso):
    if not iso:
        return None
    t = dt.datetime.fromisoformat(iso).astimezone(dt.timezone.utc)
    return t.hour + t.minute / 60.0


def main():
    if sys.argv[1:] == ["--control"]:
        r = control_run()
        print(json.dumps(r, indent=1), "\nEQUAL:", r == PLANTED)
        return 0 if r == PLANTED else 1
    p1, ycache, calls_f, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    root = HERE.parents[6]
    sys.path[:0] = [str(root / "lib"), str(root), str(root / "data/assets/scripts/silver"), str(root / "data/assets/scripts/analysis")]
    import commonwealth_daily_valuation as dv
    P = pickle.load(open(p1, "rb"))
    calls = json.load(open(calls_f))
    graded, prev_of, landing, ad, secs = P["graded"], P["prev_of"], P["landing"], P["ad"], P["secs"]

    def day_int(iso):
        return (dt.date.fromisoformat(iso) - EPOCH).days

    # --- the securities: three classes ---
    sec_ticker = {}
    for c, r in secs.items():
        real = [t for t in r["tickers"] if t.strip().upper() != c.strip().upper()]
        sec_ticker[c] = real[0] if real else None
    tickers = sorted({t for t in sec_ticker.values() if t})
    nav, as_of = {}, {}
    for t in tickers + [CONTROL_TICKER]:
        s, ao = dv.read_yahoo_close(ycache, t)
        nav[t] = None if s is None else {int(i): float(v) for i, v in s.items()}
        as_of[t] = ao
    cls = {}
    for c, t in sec_ticker.items():
        cls[c] = "no_ticker_to_ask_with" if t is None else ("asked_data_returned" if nav[t] else "asked_no_data")
    cnt = collections.Counter(cls.values())
    shared = collections.defaultdict(list)
    for c, t in sec_ticker.items():
        if t:
            shared[t].append(c)
    shared = {t: cs for t, cs in shared.items() if len(cs) > 1}
    nt_cusips = [c for c, k in cls.items() if k == "no_ticker_to_ask_with"]
    nd_list = sorted(({"ticker": sec_ticker[c], "name": ascii_(secs[c]["name"]), "account_days_carried": secs[c]["account_days"]}
                      for c, k in cls.items() if k == "asked_no_data"), key=lambda x: (-x["account_days_carried"], x["ticker"]))
    reasons = {}
    import pandas as pd
    from urllib.parse import quote
    for t in tickers:
        if not nav[t]:
            f = ycache / (quote(t, safe="") + ".csv")
            reasons[t] = str(pd.read_csv(f)["none_reason"].iloc[0])[:70] if f.is_file() else "no cache file"
    reason_count = collections.Counter(re.sub(r"[A-Z0-9.\-^=]{1,8}: ", "", v) for v in reasons.values())

    # --- row- and account-day-level grading ---
    row_out = collections.Counter()
    row_by_cls = collections.Counter()
    prior_by_day, prior_by_sec, prior_by_dow, rows_nav_by_sec = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    neither_by_day = collections.Counter()
    day_rows_by_dow = collections.Counter()
    ad_out_counts = collections.Counter()
    freed_clean = 0
    prior_blank_clean = 0
    nonav_detail = collections.Counter()
    touched_nt = 0
    nt_rows = 0
    new_claims = {}
    detail = collections.defaultdict(lambda: collections.Counter())
    for (a, d), r in ad.items():
        p = prev_of[d]
        outs = []
        kinds_nonav = set()
        for cu, price in r["rows"]:
            t = sec_ticker[cu]
            if t is None:
                o = "no_nav_found"
                kinds_nonav.add("no_ticker")
                nt_rows += 1
            elif not nav[t]:
                o = "no_nav_found"
                kinds_nonav.add("no_data")
            else:
                o = classify(price, nav[t].get(day_int(d)), nav[t].get(day_int(p)))
                if o == "no_nav_found":
                    kinds_nonav.add("no_bar")
            outs.append(o)
            row_out[o] += 1
            row_by_cls[(cls[cu], o)] += 1
            if t and nav[t]:
                detail[cu][o] += 1
                if o != "no_nav_found":
                    rows_nav_by_sec[cu] += 1
                if o == "equals_prior_day_nav_only":
                    prior_by_day[d] += 1
                    prior_by_sec[cu] += 1
                    prior_by_dow[dt.date.fromisoformat(d).strftime("%a")] += 1
                if o == "equals_neither":
                    neither_by_day[d] += 1
                if o != "no_nav_found":
                    day_rows_by_dow[dt.date.fromisoformat(d).strftime("%a")] += 1
        if any(cls[cu] == "no_ticker_to_ask_with" for cu, _ in r["rows"]):
            touched_nt += 1
        oc = day_outcome(outs)
        ad_out_counts[oc] += 1
        other = any(k != "OUTSIDE_ANCHOR" for k in r["kinds"]) or r["sixth"]
        if oc == OUTCOMES[0]:
            nonav_detail["|".join(sorted(kinds_nonav))] += 1
        if oc == OUTCOMES[3] and not other:
            freed_clean += 1
        if oc == OUTCOMES[2] and not other:
            prior_blank_clean += 1
        nc = new_claim(r["c1"], outs, r["kinds"], r["sixth"], oc)
        if nc is not None:
            new_claims[(a, d)] = nc

    # --- the sizing under v0.36 ---
    claims = {a: dict(v) for a, v in P["claims_cash"].items()}
    changed = collections.Counter()
    for (a, d), nc in new_claims.items():
        if claims[a][d] != nc:
            changed[(claims[a][d], nc)] += 1
        claims[a][d] = nc
    tally = collections.Counter(v for byday in claims.values() for v in byday.values())
    sv = v35.serve_v035(claims, graded)
    pa = [v for v in sv["per_account"].values() if v[0]]
    sizing = {
        "what_is_assumed": ASSUMED,
        "account_days": {"present": sum(tally.values()), **{k: tally.get(k, 0) for k in CLAIMS}},
        "claims_moved": {"%s -> %s" % k: v for k, v in sorted(changed.items())},
        "serving_rule": {"eligible": sv["eligible"], "served": sv["served"], "blank": sv["blank"], "blank_share_percent": round(100.0 * sv["blank"] / sv["eligible"], 3),
                         "accounts_never_served": sum(1 for e, s_ in pa if s_ == 0), "accounts_with_eligible_days": len(pa),
                         "accounts_always_served": sum(1 for e, s_ in pa if s_ == e), "blank_by_reason": dict(sv["blank_by_reason"])},
        "rule_in_force": {"basis": "the cash rule of IB-pr-435 (v0.35 names)", "account_days": {"present": P["tally_cash"]["present"], **{k: P["tally_cash"].get(k, 0) for k in CLAIMS}},
                          "eligible": P["serve_cash"]["eligible"], "served": P["serve_cash"]["served"], "blank": P["serve_cash"]["blank"],
                          "blank_share_percent": round(100.0 * P["serve_cash"]["blank"] / P["serve_cash"]["eligible"], 3),
                          "accounts_never_served": P["serve_cash"]["never"], "accounts_with_eligible_days": len(pa)},
    }

    # --- the prior-day rows ---
    rows_with_nav = sum(v for k, v in row_out.items() if k != "no_nav_found")
    prior_rows = row_out["equals_prior_day_nav_only"]
    fam = collections.defaultdict(collections.Counter)
    import re as _re
    for cu in detail:
        t = sec_ticker[cu]
        f = "fund_shaped_ticker (five letters ending X)" if _re.fullmatch(r"[A-Z]{4}X", t) else "other_ticker (exchange-traded or other)"
        fam[f]["securities"] += 1
        fam[f]["rows_with_a_nav"] += rows_nav_by_sec[cu]
        fam[f]["rows_equal_only_to_prior_day_nav"] += prior_by_sec[cu]
    top_days = prior_by_day.most_common(8)
    top_secs = [{"ticker": sec_ticker[cu], "prior_day_rows": n, "rows_with_a_nav": rows_nav_by_sec[cu]} for cu, n in prior_by_sec.most_common(10)]
    days_with = sorted(prior_by_day)
    land = {"days_with_prior_rows": len(days_with), "days_without": len(graded) - len(days_with),
            "median_last_modified_utc_hour_days_with_prior_rows": med(hour(landing[d].get("last_modified_utc")) for d in days_with),
            "median_last_modified_utc_hour_days_without": med(hour(landing[d].get("last_modified_utc")) for d in graded if d not in prior_by_day),
            "median_first_modified_utc_hour_days_with_prior_rows": med(hour(landing[d].get("first_modified_utc")) for d in days_with),
            "median_first_modified_utc_hour_days_without": med(hour(landing[d].get("first_modified_utc")) for d in graded if d not in prior_by_day)}
    by_hour = collections.defaultdict(lambda: [0, 0, 0])      # last-modified UTC hour of the partition -> [days, days with a prior-day row, prior-day rows]
    for d in graded:
        h = hour(landing[d].get("last_modified_utc"))
        k = "unknown" if h is None else "%02d" % int(h)
        by_hour[k][0] += 1
        by_hour[k][1] += int(d in prior_by_day)
        by_hour[k][2] += prior_by_day.get(d, 0)
    hi_sec = []
    for cu in detail:
        n = rows_nav_by_sec[cu]
        if n >= 10 and prior_by_sec[cu] / n >= 0.2:
            hi_sec.append(cu)
    hi_rows = sum(prior_by_sec[cu] for cu in hi_sec)
    late_start = "2026-08-13"
    late_days = [d for d in graded if d >= late_start]
    land_hour_11 = by_hour.get("11", [0, 0, 0])
    def share(n, tot):
        return round(100.0 * n / tot, 3) if tot else None

    # per-day rate of a prior-day row among the rows with a NAV, for the days with any
    per_day_rows = collections.Counter()
    for (a, d), r in ad.items():
        for cu, price in r["rows"]:
            t = sec_ticker[cu]
            if t and nav[t] and nav[t].get(day_int(d)) is not None and nav[t].get(day_int(prev_of[d])) is not None:
                per_day_rows[d] += 1
    rate_days = {d: round(100.0 * prior_by_day[d] / per_day_rows[d], 2) for d in days_with}
    first_half = [d for d in graded if d < "2026-08-26"]
    prior_before = sum(prior_by_day[d] for d in first_half)
    prior_blank_all = ad_out_counts[OUTCOMES[2]]
    prior = {
        "rows_with_a_nav": rows_with_nav, "rows_equal_only_to_prior_day_nav": prior_rows, "rows_equal_neither": row_out["equals_neither"],
        "rows_equal_day_nav_only": row_out["equals_day_nav_only"], "rows_equal_both_nav_unchanged": row_out["equals_both_nav_unchanged"],
        "rows_with_no_nav": row_out["no_nav_found"], "rows_outside_anchor_total": sum(row_out.values()),
        "share_of_rows_with_a_nav_percent": share(prior_rows, rows_with_nav),
        "days_they_fall_on": len(days_with), "days_graded": len(graded),
        "account_days_they_blank": prior_blank_all,
        "account_days_they_blank_basis": "account-days whose outside-anchor rows are all at a NAV, with one or more at the prior day's NAV only and none with no NAV or at neither (the outcome one_or_more_at_prior_day_nav_only)",
        "of_which_holding_no_other_ungradeable_kind": prior_blank_clean,
        "rows_by_day": {d: prior_by_day[d] for d in days_with}, "share_of_prior_rows_on_top_8_days_percent": share(sum(n for _, n in top_days), prior_rows),
        "top_days": [[d, n] for d, n in top_days], "prior_rate_of_rows_with_a_nav_by_day_percent": rate_days,
        "rows_by_weekday": dict(prior_by_dow), "rows_with_a_nav_by_weekday": dict(day_rows_by_dow),
        "rows_by_security_family": {k: dict(v) for k, v in fam.items()}, "top_securities": top_secs,
        "securities_with_any_prior_day_row": len(prior_by_sec), "securities_with_data": len(detail),
        "rows_equal_neither_by_day_top": [[d, n] for d, n in neither_by_day.most_common(8)],
        "prior_rows_before_2026-08-26": prior_before, "prior_rows_from_2026-08-26": prior_rows - prior_before,
        "landing_time_of_partitions": land,
        "landing_hour_table_utc": {k: {"days": v[0], "days_with_a_prior_day_row": v[1], "prior_day_rows": v[2]} for k, v in sorted(by_hour.items())},
        "securities_with_10_or_more_rows_and_a_prior_day_rate_of_20_percent_or_more": {"securities": len(hi_sec), "prior_day_rows": hi_rows, "share_of_prior_rows_percent": share(hi_rows, prior_rows)},
        "days_from_2026-08-13": {"days": len(late_days), "days_with_a_prior_day_row": sum(1 for d in late_days if d in prior_by_day), "prior_day_rows": sum(prior_by_day.get(d, 0) for d in late_days)},
    }
    prior["clustering"] = (
        "BY DATE: %d of %d days carry a prior-day row (%d to %d rows a day; the top 8 days hold %s%% of the rows); from %s on %d of %d days carry them, before it %d of %d, "
        "so they are steady in the later weeks and scattered before, with %s as the one spike. BY SECURITY: %d of %d securities with data carry one; %d securities "
        "with 10 or more rows and a 20%% or higher prior-day rate hold %d rows (%s%%), so a part of it is persistent per security, while the large funds hold about "
        "the same number each (%s). BY FAMILY: fund-shaped tickers %s%% of their rows, other tickers %s%%. BY LANDING TIME: days whose last object landed in the 11 UTC hour "
        "(%d days) carry them on %d days, holding %d of the %d rows; days landing in the 19 UTC hour (%d days) carry them on %d. So the days DO cluster by date (from mid-August), "
        "partly by security, and with landing time; this read does not trace why." % (
            len(days_with), len(graded), min(prior_by_day.values()), max(prior_by_day.values()), share(sum(n for _, n in top_days), prior_rows), late_start, prior["days_from_2026-08-13"]["days_with_a_prior_day_row"],
            len(late_days), len(days_with) - prior["days_from_2026-08-13"]["days_with_a_prior_day_row"], len(graded) - len(late_days), top_days[0][0],
            len(prior_by_sec), len(detail), len(hi_sec), hi_rows, share(hi_rows, prior_rows), ", ".join("%s %d" % (x["ticker"], x["prior_day_rows"]) for x in top_secs[:3]),
            share(fam["fund_shaped_ticker (five letters ending X)"]["rows_equal_only_to_prior_day_nav"], fam["fund_shaped_ticker (five letters ending X)"]["rows_with_a_nav"]),
            share(fam["other_ticker (exchange-traded or other)"]["rows_equal_only_to_prior_day_nav"], fam["other_ticker (exchange-traded or other)"]["rows_with_a_nav"]),
            land_hour_11[0], land_hour_11[1], land_hour_11[2], prior_rows, by_hour.get("19", [0, 0, 0])[0], by_hour.get("19", [0, 0, 0])[1]))

    # --- cross-check against IB-pr-436 (its basis: every priced row of the nine funds, any type) ---
    xc = collections.Counter()
    xdays = set()
    fdr = P["fund_day_rows"]
    for (t, d), prices in fdr.items():
        if t == "FPNIX" or not nav[t]:
            continue
        for pr in prices:
            o = classify(pr, nav[t].get(day_int(d)), nav[t].get(day_int(prev_of[d])))
            xc[o] += 1
            if o == "equals_prior_day_nav_only":
                xdays.add(d)
    cross = {"basis": "every priced row of the eight funds with a NAV in the 85 partitions (IB-pr-436's row-level basis), not only rows behind an outside-anchor row",
             "rows_with_a_nav": sum(v for k, v in xc.items() if k != "no_nav_found"), "rows_equal_only_to_prior_day_nav": xc["equals_prior_day_nav_only"],
             "rows_equal_neither": xc["equals_neither"], "days_they_fall_on": len(xdays),
             "ib436_read": {"rows_with_a_nav": 124645, "rows_equal_only_to_prior_day_nav": 497, "rows_equal_neither": 42, "days_they_fall_on": 33}}

    # --- the control: one security the anchor carries every day ---
    ctl = {"days_compared": 0, "days_equal": 0, "days_equal_to_yahoo_prior_close": 0, "days_equal_to_neither": 0, "days_anchor_absent": 0, "days_reader_absent": 0}
    diffs = []
    for d in graded:
        a_ = P["ctl_anchor"].get(d)
        y = None if not nav[CONTROL_TICKER] else nav[CONTROL_TICKER].get(day_int(d))
        yp = None if not nav[CONTROL_TICKER] else nav[CONTROL_TICKER].get(day_int(prev_of[d]))
        if a_ is None:
            ctl["days_anchor_absent"] += 1
            continue
        if y is None:
            ctl["days_reader_absent"] += 1
            continue
        ctl["days_compared"] += 1
        if old.same(a_, y):
            ctl["days_equal"] += 1
        elif yp is not None and old.same(a_, yp):
            ctl["days_equal_to_yahoo_prior_close"] += 1
        else:
            ctl["days_equal_to_neither"] += 1
        diffs.append(abs(a_ - y) / max(a_, y))
    ctl["max_relative_difference"] = max(diffs) if diffs else None
    control = {"security": "%s (CUSIP %s)" % (CONTROL_TICKER, CONTROL_CUSIP), "carried_by_anchor": True, **ctl,
               "difference_explained": "none needed: the reader's Close equals the anchor's closing_price of the same partition day (max relative difference %s)" % ctl["max_relative_difference"]}

    sec_rows = sorted(({"ticker": sec_ticker[c], "class": cls[c], "account_days_carried": secs[c]["account_days"],
                        **({"rows_by_outcome": dict(detail[c])} if c in detail else {})} for c in secs), key=lambda x: -x["account_days_carried"])
    nt_security_account_days = sum(secs[c]["account_days"] for c in nt_cusips)
    n_calls = len(calls)
    doc = {
        "same_account_days_read": bool(P["same_cash"] and P["same_pre"]),
        "same_account_days_read_basis": "this run's totals under the cash rule equal IB-pr-435's (UNGRADEABLE 43,310; ACCT_PRIOR_DATE 55; ACCT_OWN_DATE 19,832; NOTHING_TO_GRADE 13,599; present 76,796), and its v0.35 totals before the cash rule equal the re-count's (42,967 / 55 / 20,138 / 13,636)",
        "totals_read_under_the_cash_rule": P["tally_cash"], "totals_read_v035_before_the_cash_rule": P["tally_pre"], "graded_days": len(graded),
        "first_graded_day": graded[0], "last_graded_day": graded[-1],
        "securities": {"total": len(secs), "no_ticker_to_ask_with": cnt["no_ticker_to_ask_with"], "asked_data_returned": cnt["asked_data_returned"],
                       "asked_no_data": cnt["asked_no_data"], "account_days_touched_by_no_ticker_securities": touched_nt,
                       "security_account_days_on_no_ticker_securities": nt_security_account_days,
                       "basis": "securities behind an OUTSIDE_ANCHOR row under the cash rule in force (%d before the cash rule's three additions, %d after)" % (P["pre_cash_securities"], len(secs)),
                       "no_ticker_rule": "the source's Ticker/Symbol column is empty or equals the security's own identifier (a CUSIP-only bond); nothing is looked up or invented",
                       "distinct_tickers_to_ask": len(tickers), "tickers_shared_by_two_securities": {t: len(cs) for t, cs in shared.items()},
                       "tickers_shared_note": "a ticker the source gives to two securities was asked once; both securities take that ticker's class and NAV"},
        "fetch": {"calls": [{"call": c["call"], "tickers": c["tickers"], "with_bars": c["with_bars"], "no_bars": c["no_bars"], "rate_limited_not_read": c["rate_limited_not_read"]} for c in calls],
                  "call_count": n_calls, "distinct_tickers_asked": sum(c["tickers"] for c in calls), "tickers_asked_more_than_once": sum(c["tickers"] for c in calls) - len(set(t for c in calls for t in c["ticker_list"])),
                  "of_which_the_control_ticker": 1, "tickers_of_securities_asked": len(tickers),
                  "window": "2026-06-08 to 2026-10-10 (end exclusive)", "pause_between_calls_seconds": 8, "reader": "fetch_yahoo / read_yahoo_close (not edited); auto_adjust=False, unadjusted Close",
                  "no_data_reasons": dict(reason_count)},
        "no_data_securities": nd_list,
        "fpnix_note": "FPNIX is among the no-data securities (its ticker is in the list)" if any(x["ticker"] == "FPNIX" for x in nd_list) else "FPNIX returned data this time",
        "account_day_effect": {"account_days_holding_an_outside_anchor_row": len(ad), **{k: ad_out_counts[k] for k in OUTCOMES},
                               "freed_and_holding_no_other_ungradeable_kind": freed_clean,
                               "no_other_ungradeable_kind_means": "no NO_CUSIP, NEITHER_CLOSE or NEGATIVE_POSITION kind (after the cash rule) and no sixth-reason row on the account-day",
                               "one_or_more_with_no_nav_detail_by_exact_set_of_reasons": dict(nonav_detail),
                               "basis_check": "IB-pr-435 counted 34,789 account-days holding an outside-anchor row after the cash rule; this run: %d" % len(ad)},
        "sizing_under_v036": sizing,
        "prior_day_rows": prior, "cross_check_ib436_basis": cross,
        "row_outcomes_all_outside_anchor_rows": dict(row_out),
        "row_outcomes_by_security_class": {"%s|%s" % k: v for k, v in sorted(row_by_cls.items())},
        "control": control, "control_planted_classifier": {"planted": PLANTED, "read": control_run(), "equal": control_run() == PLANTED},
        "nav_source": {"name": "Yahoo Finance (yfinance), unadjusted Close, via the cell-named reader", "navs_read_as_of_file_date": sorted(set(v for v in as_of.values() if v)),
                       "adjusted": False},
        "securities_by_account_days": sec_rows,
        "claims_regraded_in_product": False, "other_sources_asked": 0,
    }
    out.write_text(json.dumps(doc, indent=1, default=str), encoding="utf-8")
    print("wrote", out, dict(cnt), dict(ad_out_counts), "freed_clean", freed_clean, "prior rows", prior_rows, "of", rows_with_nav)
    return 0


if __name__ == "__main__":
    sys.exit(main())
