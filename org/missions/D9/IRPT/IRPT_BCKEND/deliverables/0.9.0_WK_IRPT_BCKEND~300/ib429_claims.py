#!/usr/bin/env python3
"""IB-pr-429: the per account-day date-basis claim (OWN_DATE / PRIOR_CLOSE / NOT_GRADED), the serving rule as written (CTO msg 4825) and the
alternative (AMENDMENT 1, CTO msg 4833), counted.  Copied from and extending IB-pr-427's ib427_by_account.py (deliverables/0.9.0_WK_IRPT_BCKEND~286/,
untouched).  Read only; the S3 reads were done by ib429_fetch.py into a cache OUTSIDE the repo, where AccountID is already a 12-character one-way digest.

    python -I ib429_claims.py <cache_dir> <out.json>        measure and write the output (counts only)
    python -I ib429_claims.py --control                      run only the planted control and print it

COPIED UNCHANGED FROM IB-pr-427 / IB-pr-425:
  * price of a source row = Market Value / Units, rows with Units > 0 and Market Value > 0 and a CUSIP only;
  * the anchor is the Schwab silver closing_price by CUSIP (an own-date close);
  * a security MOVED on D when anchor close(D) differs from anchor close(prior trading day) by more than the tolerance (1e-4 relative);
  * a moved row is `prior` if its price is at the prior trading day's anchor close, else `own` if at D's close, else `neither`;
  * 2026-06-09 (no prior partition) is outside the graded days; trading days from lib/trading_calendar.py.
ADDED: the account-DAY is the unit.  Each priced-or-not row of an account-day is typed once (see row_types); the account-day is claimed once.
"""
from __future__ import annotations

import collections
import datetime as dt
import json
import pickle
import statistics
import sys
from pathlib import Path

TOL = 1e-4


def same(a, b):
    return abs(a - b) <= TOL * max(abs(a), abs(b), 1e-9)


# ---------------------------------------------------------------------------- the instrument (pure functions: the control runs them)

def price_rows(cusips, mvs, units):
    """{row_index: (cusip, price)} -- the existing row filter."""
    out = {}
    for i, (c, mv, u) in enumerate(zip(cusips, mvs, units)):
        try:
            mv, u = float(mv), float(u)
        except (TypeError, ValueError):
            continue
        if c and c.strip() and u > 0 and mv > 0:
            out[i] = (c.strip(), mv / u)
    return out


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def is_cash(flag):
    return str(flag).strip().lower() == "true"


def row_types(cusips, mvs, units, cash_flags, own, prev):
    """One type per row: own | prior | neither (a MOVED priced row, graded as in IB-pr-427), or a not-graded kind:
       did_not_move   a priced row whose security the anchor carries on D and on the prior trading day, and did not move;
       outside_anchor a priced row the anchor does not carry on D or on the prior trading day (and not flagged cash-equivalent);
       cash           a row the source flags Cash Equivalent = true and that is not a graded moved row (priced or not);
       no_cusip       (not cash-flagged) Units > 0 and Market Value > 0 but no CUSIP: a valued row the instrument cannot match to the anchor;
       negative_position  (not cash-flagged) Units < 0 and Market Value < 0: a valued (short) row the instrument's Units > 0 filter leaves out;
       no_price       any other row the instrument does not price and that is not cash-flagged (null or zero Units / Market Value).
    no_cusip and negative_position are kinds the face did not list ("any other reason you meet, each named").
    Returns a list parallel to the rows."""
    priced = price_rows(cusips, mvs, units)
    out = []
    for i in range(len(cusips)):
        t = None
        if i in priced:
            k, x = priced[i]
            if k in own and k in prev:
                if same(own[k], prev[k]):
                    t = "did_not_move"
                elif same(x, prev[k]):
                    t = "prior"
                elif same(x, own[k]):
                    t = "own"
                else:
                    t = "neither"
        if t in (None, "did_not_move") and is_cash(cash_flags[i]):
            t = "cash_priced_outside_anchor" if (t is None and i in priced) else "cash"
        elif t is None:
            if i in priced:
                t = "outside_anchor"
            else:
                u, m = num(units[i]), num(mvs[i])
                t = ("negative_position" if (u is not None and m is not None and u < 0 and m < 0) else
                     "no_cusip" if (u is not None and m is not None and u > 0 and m > 0) else "no_price")
        out.append(t)
    return out


def account_day_records(accounts, types):
    """account -> collections.Counter of row types."""
    rec = collections.defaultdict(collections.Counter)
    for a, t in zip(accounts, types):
        rec[a][t] += 1
    return rec


def claim(c):
    """The claim rule.  Applied literally to the CTO's words: any neither row -> NOT_GRADED (reason neither_row); else any prior row -> PRIOR_CLOSE;
    else any own row (all moved priced rows at the own close) -> OWN_DATE; else NOT_GRADED (reason no_moved_security).
    An account-day holding both own and prior rows and no neither row is PRIOR_CLOSE.  Returns (claim, reason or None)."""
    if c["neither"]:
        return "NOT_GRADED", "neither_row"
    if c["prior"]:
        return "PRIOR_CLOSE", None
    if c["own"]:
        return "OWN_DATE", None
    return "NOT_GRADED", "no_moved_security"


def ng_split(c):
    """AMENDMENT 1: a NOT_GRADED account-day is `ungradeable` if it holds at least one priced security the instrument cannot grade, else `nothing_to_grade`.
    Ungradeable kinds, in the order the class is named when several are held: neither_row (a moved row at neither close), outside_anchor (a priced
    security the anchor does not carry), no_cusip, negative_position (the last two are valued rows the instrument cannot price; see row_types).  A day
    holding both kinds is ungradeable, under the first kind that applies.  Returns (side, holdings class, side_if_only_the_face's_two_kinds_count)."""
    strict = "ungradeable" if (c["neither"] or c["outside_anchor"]) else "nothing_to_grade"
    for key in ("neither", "outside_anchor", "no_cusip", "negative_position"):
        if c[key]:
            return "ungradeable", {"neither": "neither_row"}.get(key, key), strict
    parts = [name for name, key in (("cash", "cash"), ("did_not_move", "did_not_move"), ("no_priced_row", "no_price"))
             if (c[key] + (c["cash_priced_outside_anchor"] if key == "cash" else 0)) > 0]
    cls = {("cash",): "cash_only", ("did_not_move",): "did_not_move", ("no_priced_row",): "no_priced_row"}.get(tuple(parts))
    return "nothing_to_grade", cls or "_and_".join(parts), strict


def serve(claims, days, alt=1):
    """claims: {account: {day: (claim, side or None)}}; days: ordered graded days.  An account-day D is ELIGIBLE when the account has a claim on D
    and on the prior graded day (the day before D in `days`; days[0] has no graded prior day and is not eligible).  Rule as written: served when
    both read OWN_DATE.  Alternative: good = OWN_DATE or nothing_to_grade; served when both good.  claims values are (claim, side, strict_side); `alt` picks
    the side the alternative reads (1 = the side as classed, 2 = the two kinds the face names only).  Returns the counts of each."""
    res = {}
    for name in ("as_written", "alternative"):
        res[name] = {"eligible": 0, "served": 0, "blank": 0, "blank_by_reason": collections.Counter(), "per_account": {}}
    for a, byday in claims.items():
        for name in res:
            res[name]["per_account"][a] = [0, 0]   # eligible, served
        for i in range(1, len(days)):
            d, p = days[i], days[i - 1]
            if d not in byday or p not in byday:
                continue
            cd, sd = byday[d][0], byday[d][alt]
            cp, sp = byday[p][0], byday[p][alt]
            for name in res:
                r = res[name]
                if name == "as_written":
                    gd, gp = cd == "OWN_DATE", cp == "OWN_DATE"
                    why = ("today_PRIOR_CLOSE" if cd == "PRIOR_CLOSE" else "today_NOT_GRADED" if cd == "NOT_GRADED" else
                           "yesterday_PRIOR_CLOSE" if cp == "PRIOR_CLOSE" else "yesterday_NOT_GRADED")
                else:
                    gd, gp = cd == "OWN_DATE" or sd == "nothing_to_grade", cp == "OWN_DATE" or sp == "nothing_to_grade"
                    why = ("today_PRIOR_CLOSE" if cd == "PRIOR_CLOSE" else "today_ungradeable" if not gd else
                           "yesterday_PRIOR_CLOSE" if cp == "PRIOR_CLOSE" else "yesterday_ungradeable")
                r["eligible"] += 1
                r["per_account"][a][0] += 1
                if gd and gp:
                    r["served"] += 1
                    r["per_account"][a][1] += 1
                else:
                    r["blank"] += 1
                    r["blank_by_reason"][why] += 1
    return res


def summarize_serving(r):
    pa = [v for v in r["per_account"].values() if v[0]]
    never = sum(1 for e, s in pa if s == 0)
    always = sum(1 for e, s in pa if s == e)
    out = {"eligible": r["eligible"], "served": r["served"], "blank": r["blank"],
           "blank_by_reason": dict(r["blank_by_reason"]),
           "blank_share_percent": round(100.0 * r["blank"] / r["eligible"], 3) if r["eligible"] else None,
           "accounts": {"with_eligible_days": len(pa), "never_served": never, "always_served": always,
                        "sometimes_served": len(pa) - never - always}}
    return out


def share_buckets(r):
    def b(sh):
        return ("zero" if sh == 0 else "above_0_to_50" if sh < 50 else "50_to_90" if sh < 90 else "90_to_below_100" if sh < 100 else "100")
    order = ["zero", "above_0_to_50", "50_to_90", "90_to_below_100", "100"]
    c = collections.Counter(b(100.0 * s / e) for e, s in r["per_account"].values() if e)
    return {k: c[k] for k in order}


# ---------------------------------------------------------------------------- the planted control

def control_run():
    """Fixture: 4 trading days D1..D4, 4 accounts, 2 moving securities S1 S2 and one that does not move (FLAT); the anchor does not carry NOANCHOR.
      A: holds S1 S2 at the own close every day                                     -> OWN_DATE x4
      B: S1 S2 at the own close D1, at the PRIOR close D2 (planted), own D3, D4     -> OWN_DATE, PRIOR_CLOSE, OWN_DATE, OWN_DATE
      C: D1 one cash-equivalent row only; D2 cash + FLAT (did not move); D3 S1 at neither close (planted neither row); D4 NOANCHOR (priced, outside the anchor)
                                                                                    -> NOT_GRADED x4 (nothing_to_grade, nothing_to_grade, ungradeable, ungradeable)
      E: D1 a valued row with no CUSIP; D2 a negative (short) position; D3 and D4 a row with a CUSIP and null Units and Market Value
                                                                                    -> NOT_GRADED x4 (ungradeable no_cusip, ungradeable negative_position, nothing_to_grade x2)
    Runs the same row_types / claim / ng_split / serve functions as the measurement."""
    days = ["D1", "D2", "D3", "D4"]
    anchors = {"D0": {"S1": 10.0, "S2": 20.0, "FLAT": 50.0}}
    for n, d in enumerate(days, start=1):
        anchors[d] = {"S1": 10.0 + n, "S2": 20.0 + 2 * n, "FLAT": 50.0}
    prev_of = {d: ("D0" if i == 0 else days[i - 1]) for i, d in enumerate(days)}
    claims = {a: {} for a in "ABCE"}
    tally = collections.Counter()
    for d in days:
        own, prev = anchors[d], anchors[prev_of[d]]
        rows = []   # (account, cusip, market value, units, cash flag)
        for a in "AB":
            lag = (a == "B" and d == "D2")
            for s in ("S1", "S2"):
                rows.append((a, s, (prev if lag else own)[s] * 10.0, 10.0, "false"))
        if d == "D1":
            rows.append(("C", None, 100.0, 0.0, "true"))                      # cash row: no CUSIP, no units
            rows.append(("E", None, 300.0, 10.0, "false"))                    # valued, no CUSIP
        elif d == "D2":
            rows.append(("C", None, 100.0, 0.0, "true"))
            rows.append(("C", "FLAT", 500.0, 10.0, "false"))                  # did not move
            rows.append(("E", "S1", -400.0, -10.0, "false"))                  # negative (short) position
        elif d == "D3":
            rows.append(("C", "S1", own["S1"] * 1.07 * 10.0, 10.0, "false"))  # moved, at neither close
            rows.append(("E", "S2", None, None, "false"))                     # CUSIP, null Units and Market Value
        else:
            rows.append(("C", "NOANCHOR", 50.0, 10.0, "false"))               # priced, the anchor does not carry it
            rows.append(("E", "S2", None, None, "false"))
        types = row_types([r[1] for r in rows], [r[2] for r in rows], [r[3] for r in rows], [r[4] for r in rows], own, prev)
        for a, rec in account_day_records([r[0] for r in rows], types).items():
            cl, why = claim(rec)
            side, cls, strict = ng_split(rec) if cl == "NOT_GRADED" else (None, None, None)
            claims[a][d] = (cl, side, strict)
            tally[cl] += 1
            if cl == "NOT_GRADED":
                tally["reason:" + why] += 1
                tally["%s:%s" % (side, cls)] += 1
    res, res_s = serve(claims, days), serve(claims, days, alt=2)
    sa, sb, ss = summarize_serving(res["as_written"]), summarize_serving(res["alternative"]), summarize_serving(res_s["alternative"])

    def acc(x):
        return [x["accounts"]["never_served"], x["accounts"]["always_served"], x["accounts"]["sometimes_served"]]
    read = {
        "OWN_DATE": tally["OWN_DATE"], "PRIOR_CLOSE": tally["PRIOR_CLOSE"], "NOT_GRADED": tally["NOT_GRADED"],
        "NG_no_moved_security": tally["reason:no_moved_security"], "NG_neither_row": tally["reason:neither_row"],
        "nothing_to_grade_cash_only": tally["nothing_to_grade:cash_only"],
        "nothing_to_grade_cash_and_did_not_move": tally["nothing_to_grade:cash_and_did_not_move"],
        "nothing_to_grade_no_priced_row": tally["nothing_to_grade:no_priced_row"],
        "ungradeable_neither_row": tally["ungradeable:neither_row"], "ungradeable_outside_anchor": tally["ungradeable:outside_anchor"],
        "ungradeable_no_cusip": tally["ungradeable:no_cusip"], "ungradeable_negative_position": tally["ungradeable:negative_position"],
        "served": sa["served"], "blank": sa["blank"], "blank_by_reason": sa["blank_by_reason"], "accounts_never_always_sometimes": acc(sa),
        "alt_served": sb["served"], "alt_blank": sb["blank"], "alt_blank_by_reason": sb["blank_by_reason"], "alt_accounts_never_always_sometimes": acc(sb),
        "alt_two_kinds_only_served": ss["served"], "alt_two_kinds_only_blank": ss["blank"], "alt_two_kinds_only_blank_by_reason": ss["blank_by_reason"],
        "alt_two_kinds_only_accounts_never_always_sometimes": acc(ss),
    }
    return read


# Known BY CONSTRUCTION from the fixture's description above (counted by hand, not by the code): 16 account-days; A 4 own; B 3 own + 1 prior;
# C 4 not graded (3 no_moved_security: cash_only, cash_and_did_not_move, outside_anchor; 1 neither_row); E 4 not graded, all no_moved_security
# (no_cusip, negative_position ungradeable; no_priced_row x2 nothing_to_grade).  Eligible D2..D4 x 4 accounts = 12.
# As written: A served 3 (D2 D3 D4); B served D4 only (D2 today prior, D3 yesterday prior); C and E none -> served 4, blank 8 = today_PRIOR_CLOSE 1 (B D2),
# yesterday_PRIOR_CLOSE 1 (B D3), today_NOT_GRADED 6 (C and E, D2 D3 D4).  Accounts: C and E never (2), A always (1), B sometimes (1).
# Alternative (good = own or nothing_to_grade): A 3; B 1 (D4); C 1 (D2: D1 and D2 both nothing_to_grade); E 1 (D4: D3 and D4 nothing_to_grade) -> served 6, blank 6
# = today_PRIOR_CLOSE 1, yesterday_PRIOR_CLOSE 1, today_ungradeable 3 (C D3, C D4, E D2), yesterday_ungradeable 1 (E D3).  Accounts: never 0, always 1 (A),
# sometimes 3 (B, C, E).
# Alternative on the two ungradeable kinds the face names only (no_cusip and negative_position count as nothing_to_grade): E good every day, served D2 D3 D4 (3)
# -> served 8, blank 4 = today_PRIOR_CLOSE 1, yesterday_PRIOR_CLOSE 1, today_ungradeable 2 (C D3 D4).  Accounts: never 0, always 2 (A, E), sometimes 2 (B, C).
PLANTED = {
    "OWN_DATE": 7, "PRIOR_CLOSE": 1, "NOT_GRADED": 8,
    "NG_no_moved_security": 7, "NG_neither_row": 1,
    "nothing_to_grade_cash_only": 1, "nothing_to_grade_cash_and_did_not_move": 1, "nothing_to_grade_no_priced_row": 2,
    "ungradeable_neither_row": 1, "ungradeable_outside_anchor": 1, "ungradeable_no_cusip": 1, "ungradeable_negative_position": 1,
    "served": 4, "blank": 8,
    "blank_by_reason": {"today_PRIOR_CLOSE": 1, "yesterday_PRIOR_CLOSE": 1, "today_NOT_GRADED": 6},
    "accounts_never_always_sometimes": [2, 1, 1],
    "alt_served": 6, "alt_blank": 6,
    "alt_blank_by_reason": {"today_PRIOR_CLOSE": 1, "yesterday_PRIOR_CLOSE": 1, "today_ungradeable": 3, "yesterday_ungradeable": 1},
    "alt_accounts_never_always_sometimes": [0, 1, 3],
    "alt_two_kinds_only_served": 8, "alt_two_kinds_only_blank": 4,
    "alt_two_kinds_only_blank_by_reason": {"today_PRIOR_CLOSE": 1, "yesterday_PRIOR_CLOSE": 1, "today_ungradeable": 2},
    "alt_two_kinds_only_accounts_never_always_sometimes": [0, 2, 2],
}


def control():
    return {"planted": PLANTED, "read": control_run(),
            "fixture": "4 trading days, 4 accounts, 2 moving securities and one that does not move; B is at the prior close on D2 (planted prior-close day); "
                       "C holds cash only on D1, cash + an unmoved security on D2, a moved row at neither close on D3 (planted neither row) and a priced security "
                       "outside the anchor on D4; E holds a valued row with no CUSIP on D1, a negative position on D2 and a row with null Units and Market Value on D3 and D4"}


# ---------------------------------------------------------------------------- the measurement

def main():
    if sys.argv[1:] == ["--control"]:
        c = control()
        print(json.dumps(c, indent=1), "\nEQUAL:", c["planted"] == c["read"])
        return 0 if c["planted"] == c["read"] else 1
    cache, out = Path(sys.argv[1]), Path(sys.argv[2])
    root = Path(__file__).resolve().parents[7]
    sys.path[:0] = [str(root / "lib"), str(root), str(root / "data/assets/scripts/gold/irpt_holdings_performance")]
    import trading_calendar as tc
    import holdings_performance as hp
    decl = json.load(open(root / "data/assets/scripts/gold/irpt_holdings_performance/sources.json", encoding="utf-8"))
    src = decl["blackdiamond_z09"]
    prefix_resolved = hp.resolved_prefix(src, "positions_prefix", hp.firm_scope(src))
    anchor_prefix = decl["schwab_08335338"]["positions_prefix"]

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

    acct_all = set()
    graded_days, ungradeable = [], []
    claims = collections.defaultdict(dict)       # account -> day -> (claim, side, side if only the two kinds the face names count)
    cday = collections.Counter()                  # account-day tallies
    present_by_day = {}
    rows_tot = collections.Counter()
    hold = collections.defaultdict(collections.Counter)      # account -> component flags over its days (for the no-moved-row accounts)
    acct_moved_any = set()
    ng_reason_by_ng_class = collections.Counter()
    sens_cash_outside = 0                         # nothing_to_grade account-days that hold a cash-flagged priced row outside the anchor
    comp_ad = collections.Counter()               # NOT_GRADED account-days: component flags
    first_day_accounts = set(load("src", tdays[0])["AccountID"])   # accounts present in the ungraded first partition (2026-06-09)
    for i, d in enumerate(tdays):
        p = tc.prev_trading_day(dt.date.fromisoformat(d)).isoformat()
        s = load("src", d)
        A, B = anchor(d), anchor(p)
        if s in (None, "UNREAD") or A in (None, "UNREAD") or B in (None, "UNREAD"):
            ungradeable.append(d)
            continue
        if i == 0 or tdays[i - 1] != p:
            present_by_day[d] = None
            continue  # FIRST_DAY_NO_PRIOR: outside the totals
        graded_days.append(d)
        types = row_types(s["CUSIP"], s["Market Value"], s["Units"], s["Cash Equivalent"], A, B)
        rec = account_day_records(s["AccountID"], types)
        acct_all.update(rec)
        present_by_day[d] = set(rec)
        for t in types:
            if t in ("own", "prior", "neither"):
                rows_tot[t] += 1
                rows_tot["moved"] += 1
        for a, c in rec.items():
            cl, why = claim(c)
            side, cls, strict = (None, None, None)
            cday["present"] += 1
            cday[cl] += 1
            if c["own"] + c["prior"] + c["neither"]:
                acct_moved_any.add(a)
            if c["own"] and c["prior"]:
                cday["mix:own_and_prior"] += 1
            if c["neither"] and (c["own"] or c["prior"]):
                cday["mix:neither_with_own_or_prior"] += 1
            if cl == "NOT_GRADED":
                cday["reason:" + why] += 1
                side, cls, strict = ng_split(c)
                cday["two_kinds_only:" + strict] += 1
                cday["split:%s:%s" % (side, cls)] += 1
                ng_reason_by_ng_class["%s|%s" % (why, side)] += 1
                if side == "nothing_to_grade" and c["cash_priced_outside_anchor"]:
                    sens_cash_outside += 1
                for key in ("cash", "did_not_move", "no_price", "outside_anchor", "no_cusip", "negative_position", "cash_priced_outside_anchor", "neither"):
                    if c[key]:
                        comp_ad[("%s:%s" % (why, key))] += 1
            claims[a][d] = (cl, side, strict)
            for key in ("cash", "did_not_move", "no_price", "outside_anchor", "no_cusip", "negative_position", "cash_priced_outside_anchor"):
                if c[key]:
                    hold[a][key] += 1

    # ---- consistency: every account-day has exactly one claim
    assert cday["present"] == sum(len(v) for v in claims.values()) == cday["OWN_DATE"] + cday["PRIOR_CLOSE"] + cday["NOT_GRADED"]

    # ---- the serving rules
    res, res_s = serve(claims, graded_days), serve(claims, graded_days, alt=2)
    sa, sb, ss = summarize_serving(res["as_written"]), summarize_serving(res["alternative"]), summarize_serving(res_s["alternative"])
    d0 = graded_days[0]
    newly = sum(1 for _ in present_by_day[d0])           # account-days on the first graded day
    first_with_prior = len(present_by_day[d0] & first_day_accounts)
    # eligible account-days = present today AND present on the prior graded day (the first graded day has no graded prior day)
    not_eligible_new = 0
    for j in range(1, len(graded_days)):
        not_eligible_new += len(present_by_day[graded_days[j]] - present_by_day[graded_days[j - 1]])
    alt_first = {"eligible": sa["eligible"] + first_with_prior, "blank": sa["blank"] + first_with_prior,
                 "blank_share_percent": round(100.0 * (sa["blank"] + first_with_prior) / (sa["eligible"] + first_with_prior), 3)}
    first_day = {
        "first_graded_day": d0, "its_prior_partition": first_graded_prior(tdays, d0),
        "treatment": "The prior partition of the first graded day (2026-06-09) is ungraded, so no claim exists for it.  The %d account-days of %s are NOT eligible "
                     "and are outside the serving counts (they are still claimed and counted in account_days).  Eligible account-days are those present today and "
                     "on the prior GRADED day." % (newly, d0),
        "first_day_account_days_present_also_on_the_prior_partition": first_with_prior,
        "if_instead_counted_eligible_and_blank_as_yesterday_NOT_GRADED": alt_first,
        "account_days_after_the_first_day_not_eligible_because_the_account_was_absent_the_prior_day": not_eligible_new,
    }

    # ---- NOT_GRADED breakdown
    ng_total = cday["NOT_GRADED"]
    split = {"nothing_to_grade": {"account_days": 0, "by_holdings_class": {}}, "ungradeable": {"account_days": 0, "by_holdings_class": {}}}
    for k, v in cday.items():
        if k.startswith("split:"):
            _, side, cls = k.split(":")
            split[side]["account_days"] += v
            split[side]["by_holdings_class"][cls] = v
    for side in split:
        split[side]["by_holdings_class"] = dict(sorted(split[side]["by_holdings_class"].items(), key=lambda kv: -kv[1]))
    reasons = {"no_moved_security": cday["reason:no_moved_security"], "neither_row": cday["reason:neither_row"]}
    cross = {}
    for k, v in ng_reason_by_ng_class.items():
        w, side = k.split("|")
        cross.setdefault(w, {})[side] = v
    holdings_breakdown = {
        "reason_by_side": cross,
        "ng_account_days_holding_each_kind_of_row": {
            "note": "an account-day can hold several kinds, so these do not sum to the NOT_GRADED total; each counts the NOT_GRADED account-days of that reason that hold at least one row of the kind",
            **{w: {key: comp_ad[w + ":" + key] for key in ("cash", "did_not_move", "no_price", "outside_anchor", "no_cusip", "negative_position", "cash_priced_outside_anchor", "neither")}
               for w in ("no_moved_security", "neither_row")}},
        "kinds_defined": {
            "cash": "row flagged Cash Equivalent = true that is not a graded moved row (priced or not)",
            "did_not_move": "priced row, security carried by the anchor on D and the prior trading day, did not move",
            "outside_anchor": "priced row, security not carried by the anchor on D or on the prior trading day, not flagged cash-equivalent",
            "no_cusip": "valued row (Units > 0 and Market Value > 0) with no CUSIP, not flagged cash-equivalent: the instrument cannot match it to the anchor.  A kind the face did not list; counted as ungradeable",
            "negative_position": "valued row with Units < 0 and Market Value < 0, not flagged cash-equivalent: the instrument's Units > 0 filter leaves it out.  A kind the face did not list; counted as ungradeable",
            "no_price": "any other row the instrument does not price (null or zero Units / Market Value), not flagged cash-equivalent",
            "cash_priced_outside_anchor": "a cash-equivalent-flagged row that is priced and outside the anchor; counted as cash (nothing to grade)",
        },
        "sensitivity_nothing_to_grade_account_days_that_hold_a_cash_flagged_priced_row_outside_the_anchor": sens_cash_outside,
    }
    never_moved = [a for a in acct_all if a not in acct_moved_any]
    nm = collections.Counter()
    for a in never_moved:
        h = hold[a]
        parts = [n for n, k in (("cash", "cash"), ("did_not_move", "did_not_move"), ("no_priced_row", "no_price")) if (h[k] + (h["cash_priced_outside_anchor"] if k == "cash" else 0)) > 0]
        cls = ("holds_outside_anchor_on_some_day" if h["outside_anchor"] else "holds_no_cusip_valued_row_on_some_day" if h["no_cusip"] else
               "holds_negative_position_on_some_day" if h["negative_position"] else "_and_".join(parts) if parts else "none")
        nm[cls] += 1
    accounts_never_moved = {
        "accounts": len(never_moved),
        "basis": "accounts with no moved priced row on any graded day (IB-pr-427's no_moved_rows).  Each is classed once over its 85 days: if on any day it held a priced security "
                 "outside the anchor -> holds_outside_anchor_on_some_day; else a valued row with no CUSIP -> holds_no_cusip_valued_row_on_some_day; else a negative position -> "
                 "holds_negative_position_on_some_day; else the set of kinds it held on any day (cash, did_not_move, no_priced_row).",
        "by_holdings": dict(sorted(nm.items(), key=lambda kv: -kv[1])),
    }
    # accounts whose every present day is NOT_GRADED
    all_ng = sum(1 for a in acct_all if all(v[0] == "NOT_GRADED" for v in claims[a].values()))
    all_ng_ungr = sum(1 for a in acct_all if all(v[0] == "NOT_GRADED" and v[1] == "ungradeable" for v in claims[a].values()))
    all_ng_nothing = sum(1 for a in acct_all if all(v[0] == "NOT_GRADED" and v[1] == "nothing_to_grade" for v in claims[a].values()))

    # ---- timing of the inputs (object timestamps; times and counts only)
    timing = []
    for d in graded_days:
        sm, am = load("src", d)["_meta"], load("anc", d)["_meta"]
        timing.append({"date": d, "source_objects": sm["objects"], "source_last_modified_utc": sm["last_modified_utc"],
                       "anchor_objects": am["objects"], "anchor_last_modified_utc": am["last_modified_utc"]})

    def tm(x):
        return dt.datetime.fromisoformat(x)
    for x in timing:
        x["anchor_minus_source_minutes"] = round((tm(x["anchor_last_modified_utc"]) - tm(x["source_last_modified_utc"])).total_seconds() / 60.0, 1)
        x["last_to_land"] = "anchor" if x["anchor_minus_source_minutes"] > 0 else "source"
        x["source_hhmm_utc"] = tm(x["source_last_modified_utc"]).strftime("%H:%M")
        x["anchor_hhmm_utc"] = tm(x["anchor_last_modified_utc"]).strftime("%H:%M")
        x["source_day_offset"] = (tm(x["source_last_modified_utc"]).date() - dt.date.fromisoformat(x["date"])).days
        x["anchor_day_offset"] = (tm(x["anchor_last_modified_utc"]).date() - dt.date.fromisoformat(x["date"])).days

    doc_timing = {"recent_days": timing[-8:], "all_graded_days": {
        "days": len(timing), "anchor_landed_last": sum(1 for x in timing if x["last_to_land"] == "anchor"),
        "source_landed_last": sum(1 for x in timing if x["last_to_land"] == "source"),
        "anchor_minus_source_minutes": {"min": min(x["anchor_minus_source_minutes"] for x in timing),
                                        "median": statistics.median(x["anchor_minus_source_minutes"] for x in timing),
                                        "max": max(x["anchor_minus_source_minutes"] for x in timing)}}}

    rec8 = timing[-8:]
    s_t = sorted(x["source_hhmm_utc"] for x in rec8)
    a_t = sorted(x["anchor_hhmm_utc"] for x in rec8)
    miss_cash = [d for d in graded_days if "Cash Equivalent" in load("src", d).get("_absent_columns", [])]
    src_when = ("last-modified %s UTC on the calendar day after D, on each of the last %d trading days (%s to %s); one object per partition; "
                "over all %d graded days the source partition was the later of the two on %d"
                % (s_t[0] if s_t[0] == s_t[-1] else s_t[0] + " to " + s_t[-1], len(rec8), rec8[0]["date"], rec8[-1]["date"], len(timing), doc_timing["all_graded_days"]["source_landed_last"]))
    anc_when = ("last-modified %s UTC on the calendar day after D, on each of the last %d trading days; about %.0f minutes before the Cottonwood partition "
                "(median over %d graded days %.0f)" % (a_t[0] if a_t[0] == a_t[-1] else a_t[0] + " to " + a_t[-1], len(rec8), -statistics.median(x["anchor_minus_source_minutes"] for x in rec8),
                                                       len(timing), -doc_timing["all_graded_days"]["anchor_minus_source_minutes"]["median"]))
    needs = [
        {"need": "The account's holdings partition for day D: CUSIP, Market Value, Units, AccountID (the claim), plus the Cash Equivalent flag (the NOT_GRADED split; present on %d of %d partitions read)"
                 % (len(listed) - len(miss_cash), len(listed)),
         "where_from": "s3://%s/<blackdiamond_z09 positions_prefix, resolved by holdings_performance.resolved_prefix>date=D/ (Cottonwood silver positions)" % src["bucket"],
         "by_when": src_when + ".  THE LAST INPUT TO LAND."},
        {"need": "The anchor's own-date close for day D, by CUSIP (closing_price), to decide which securities moved and what the own close is",
         "where_from": "s3://%s/%sdate=D/ (Schwab silver dim_position, closing_price by cusip)" % (src["bucket"], anchor_prefix),
         "by_when": anc_when},
        {"need": "The anchor's close for the prior trading day p, by CUSIP, to decide which securities moved and what the prior close is",
         "where_from": "the same anchor prefix, date=p",
         "by_when": "already in place: it landed the morning after p, a full cycle before D's inputs"},
        {"need": "The account's holdings partition for the prior trading day p, to know whether the account was present (eligibility for the serving rule)",
         "where_from": "the same Cottonwood prefix, date=p",
         "by_when": "already in place: it landed the morning after p"},
        {"need": "The trading calendar, to name the prior trading day p",
         "where_from": "lib/trading_calendar.py (NYSE closures table 2010-2027 in the repo; pandas_market_calendars when installed)",
         "by_when": "no landing time: a static table, covers every date to 2027-12-31"},
        {"need": "The claim stamped for the same account on the prior trading day p (the serving rule reads yesterday's claim)",
         "where_from": "the instrument's own output for day p, stored by the gold; none exists for 2026-06-09, the first partition",
         "by_when": "stamped one cycle earlier, so it exists whenever the run for p completed; a missed day leaves the next day without a prior claim"},
    ]
    doc_timing["note"] = ("Object LastModified from list_objects_v2, times only.  A LastModified is the last write of the object, so a later rewrite of an old day "
                          "shows the rewrite time; the recent days are the least affected.")

    doc = {
        "source": {"bucket": src["bucket"], "entry": "blackdiamond_z09", "prefix_template": src["positions_prefix"] + "date=YYYY-MM-DD/",
                   "prefix_resolved_by": "holdings_performance.resolved_prefix(blackdiamond_z09, positions_prefix, firm_scope) -> %d characters, same as the gold script" % len(prefix_resolved),
                   "anchor": "%s%s (closing_price by cusip; the Schwab own-date close)" % (anchor_prefix, "date=YYYY-MM-DD/"),
                   "price": "Market Value / Units, rows with Units > 0 and Market Value > 0 and a CUSIP",
                   "account_key": "AccountID, replaced at read time by a one-way digest; used only to group rows, never written"},
        "tolerance": {"kind": "relative", "value": TOL, "rule": "abs(a-b) <= 1e-4 * max(abs(a), abs(b), 1e-9)", "taken_from": "IB-pr-425 s252_all_partitions.py same()"},
        "days": len(graded_days),
        "range_graded": [graded_days[0], graded_days[-1]],
        "days_ungradeable": ungradeable,
        "accounts": len(acct_all),
        "claim_rule": "One claim per account-day, by the first row that applies: (1) the account-day holds at least one moved priced row at NEITHER close -> NOT_GRADED "
                      "(reason neither_row), whatever else it holds; (2) else at least one moved priced row at the PRIOR close -> PRIOR_CLOSE (an account-day holding "
                      "both own and prior rows and no neither row is PRIOR_CLOSE); (3) else at least one moved priced row and all of them at the own close -> OWN_DATE; "
                      "(4) else no moved priced row -> NOT_GRADED (reason no_moved_security).  A moved row is a priced row whose security moved on D (anchor close(D) vs "
                      "close(prior trading day), 1e-4 relative); it is own / prior / neither as in IB-pr-427.  Nothing is dropped: every account present in a graded-day "
                      "partition has a claim.",
        "account_days": {"present": cday["present"], "OWN_DATE": cday["OWN_DATE"], "PRIOR_CLOSE": cday["PRIOR_CLOSE"], "NOT_GRADED": ng_total},
        "mixed_account_days": {"own_and_prior_rows_both_held": cday["mix:own_and_prior"],
                               "neither_row_held_with_own_or_prior_rows": cday["mix:neither_with_own_or_prior"],
                               "treatment": "own and prior both held, no neither row -> PRIOR_CLOSE; a neither row with any own or prior rows -> NOT_GRADED (neither_row); "
                                            "the two counts overlap when an account-day holds all three (it is NOT_GRADED)"},
        "not_graded_by_reason": reasons,
        "not_graded_split_rule": "AMENDMENT 1.  A NOT_GRADED account-day is `ungradeable` when it holds at least one priced security the instrument cannot grade: a priced "
                                 "security the anchor does not carry (outside_anchor), a moved row at neither close (neither_row), or a valued row the instrument cannot price "
                                 "(no_cusip: Units > 0 and Market Value > 0 and no CUSIP; negative_position: Units < 0 and Market Value < 0) -- the last two are kinds "
                                 "the face did not list, named here because such a row could sit on the wrong date; otherwise `nothing_to_grade`.  An account-day holding "
                                 "both kinds is ungradeable, named by the first kind that applies in the order neither_row, outside_anchor, no_cusip, negative_position "
                                 "(the kinds held are all counted in not_graded_holdings_breakdown).  nothing_to_grade classes name the kinds held (cash = Cash "
                                 "Equivalent flag, did_not_move, no_priced_row); an account-day holding more than one kind carries the joined name.",
        "not_graded_split_two_kinds_only": {
            "note": "the same split if only the two ungradeable kinds the face names (outside_anchor, neither_row) count; no_cusip and negative_position rows then count as nothing to grade",
            "nothing_to_grade": cday["two_kinds_only:nothing_to_grade"], "ungradeable": cday["two_kinds_only:ungradeable"]},
        "not_graded_split": split,
        "not_graded_holdings_breakdown": holdings_breakdown,
        "accounts_never_graded_on_a_moved_security": accounts_never_moved,
        "accounts_with_every_present_day_NOT_GRADED": {"all": all_ng, "every_day_ungradeable": all_ng_ungr, "every_day_nothing_to_grade": all_ng_nothing},
        "rows_moved": dict(rows_tot),
        "serving_rule": dict(sa, description="AS WRITTEN (CTO msg 4825): eligible = present today and on the prior graded day; served when today and the prior trading day both "
                                          "read OWN_DATE; blank otherwise, with the reason taken in the order today_PRIOR_CLOSE, today_NOT_GRADED, yesterday_PRIOR_CLOSE, "
                                          "yesterday_NOT_GRADED (the first that applies).",
                             first_day_treatment=first_day,
                             per_account_served_share_distribution={"basis": "per account, 100 * served / eligible account-days, over accounts with eligible days",
                                                                    "accounts": share_buckets(res["as_written"])}),
        "serving_rule_alternative_two_kinds_only": dict(ss, description="NOT THE RULE IN FORCE.  The alternative above, counting as ungradeable only the two kinds the face names "
                                                                 "(outside_anchor, neither_row); a valued row with no CUSIP or a negative position counts as nothing to grade.  A sensitivity."),
        "serving_rule_alternative": dict(sb, description="NOT THE RULE IN FORCE (CTO's ruling of msg 4825 is HELD, msg 4833).  The alternative the CTO describes: an account-day is "
                                                      "good when it reads OWN_DATE or is nothing_to_grade; a return is served when today and the prior trading day are both good.  "
                                                      "Same eligible set.  Blank reasons in the order today_PRIOR_CLOSE, today_ungradeable, yesterday_PRIOR_CLOSE, yesterday_ungradeable.",
                                         per_account_served_share_distribution={"basis": "as the rule as written", "accounts": share_buckets(res["alternative"])}),
        "instrument_input_timing": doc_timing,
        "instrument_daily_needs": needs,
        "binding_need": "The Cottonwood holdings partition for day D (need 1).  It lands about two hours after the anchor's close for D, which lands the same morning; "
                        "the prior-day inputs and the calendar are already in place.  A claim for D can be stamped no earlier than that partition.",
        "control": control(),
    }
    # reconciliation with IB-pr-427 (read from its committed JSON)
    old = json.load(open(root / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~286/IB125-1_lag_by_account.json", encoding="utf-8"))
    o = old["rows"]
    doc["reconciliation_with_IB_pr_427"] = {
        "ib_pr_427_rows": o, "this_cell_rows": dict(rows_tot),
        "moved_rows_equal": o["moved"] == rows_tot["moved"], "prior_rows_equal": o["prior"] == rows_tot["prior"], "neither_rows_equal": o["neither"] == rows_tot["neither"],
        "own_rows_equal": o["own"] == rows_tot["own"],
        "days_equal": old["days_graded"] == len(graded_days), "accounts_read_equal": old["accounts"]["read"] == len(acct_all),
        "ib_pr_427_accounts_with_no_moved_rows": old["accounts"]["no_moved_rows"], "this_cell_accounts_with_no_moved_row_on_any_day": len(never_moved),
    }
    out.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    print("wrote", out, "days", len(graded_days), "accounts", len(acct_all), dict(cday))
    return 0


def first_graded_prior(tdays, d0):
    return tdays[tdays.index(d0) - 1]


if __name__ == "__main__":
    sys.exit(main())
