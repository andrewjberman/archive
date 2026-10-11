#!/usr/bin/env python3
"""IB-pr-429 AMENDMENT 2: the date-basis claim re-counted under PRD ADDENDUM v0.35's ORDERED rule, beside IB-pr-429's own rule, on the same 85 partitions.
Read only.  Starts from ib429_claims.py (same folder, untouched): the row typing (row_types), the old claim (claim, ng_split) and the old serving
counter (serve) are IMPORTED and run in the same pass, so each account-day holds both claims and the moves are cross-counted from the same rows.
The partitions are read by ib429_fetch.py into a cache OUTSIDE the repo, where AccountID is already a 12-character one-way digest.

    python -I ib429_claims_v035.py <cache_dir> <out.json>      measure and write the output (counts only)
    python -I ib429_claims_v035.py --control                   run only the planted control and print it

THE RULE (ADDENDUM v0.35), decided in this order, the first that applies is the claim:
  1 UNGRADEABLE      the account-day holds one or more priced securities the instrument cannot place at a close, whatever its other rows read;
                     it carries the list of EVERY kind present: ANCHOR_NOT_LANDED, OUTSIDE_ANCHOR, NO_CUSIP, NEITHER_CLOSE, NEGATIVE_POSITION
  2 ACCT_PRIOR_DATE       no row ungradeable, one or more gradeable moved securities at the prior trading day's close
  3 ACCT_OWN_DATE         no row ungradeable, every gradeable moved security at its own date's close
  4 NOTHING_TO_GRADE nothing whose value depends on the date basis
KEPT UNCHANGED from IB-pr-429: source, anchor, price rule, tolerance, trading-day axis, digest, the row-kind definitions of row_types.
Serving: eligible = present today and on the prior graded day; served when today and the prior day each read ACCT_OWN_DATE or NOTHING_TO_GRADE; blank
otherwise, the reason the first of today_UNGRADEABLE, today_ACCT_PRIOR_DATE, yesterday_UNGRADEABLE, yesterday_ACCT_PRIOR_DATE.
"""
from __future__ import annotations

import collections
import datetime as dt
import json
import pickle
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ib429_claims as old  # noqa: E402

KINDS = ("ANCHOR_NOT_LANDED", "OUTSIDE_ANCHOR", "NO_CUSIP", "NEITHER_CLOSE", "NEGATIVE_POSITION")
KIND_OF_TYPE = {"anchor_not_landed": "ANCHOR_NOT_LANDED", "outside_anchor": "OUTSIDE_ANCHOR", "no_cusip": "NO_CUSIP", "neither": "NEITHER_CLOSE",
                "negative_position": "NEGATIVE_POSITION"}
OLD_FILE = {"present": 76796, "OWN_DATE": 45247, "PRIOR_CLOSE": 425, "ungradeable": 17488, "nothing_to_grade": 13636}


def typed_rows(cusips, mvs, units, cash_flags, own, prev):
    """Row types of IB-pr-429 (row_types), with one addition: when the anchor close for D or for the prior trading day is not in hand (own or prev is None)
    every non-cash priced row is `anchor_not_landed` instead of outside_anchor.  Nothing else changes."""
    if own is None or prev is None:
        return ["anchor_not_landed" if t == "outside_anchor" else t for t in old.row_types(cusips, mvs, units, cash_flags, {}, {})]
    return old.row_types(cusips, mvs, units, cash_flags, own, prev)


def kinds_of(c):
    """The sorted list of every ungradeable kind an account-day holds, from its row-type counter."""
    return sorted(KIND_OF_TYPE[t] for t in KIND_OF_TYPE if c[t])


def claim_v035(c):
    """(claim, kinds).  The ordered rule."""
    k = kinds_of(c)
    if k:
        return "UNGRADEABLE", k
    if c["prior"]:
        return "ACCT_PRIOR_DATE", []
    if c["own"]:
        return "ACCT_OWN_DATE", []
    return "NOTHING_TO_GRADE", []


def old_class(c):
    """IB-pr-429's claim and, for NOT_GRADED, its AMENDMENT 1 side -> one of OWN, PRIOR, NG_ungradeable, NG_nothing."""
    cl, _ = old.claim(c)
    if cl == "NOT_GRADED":
        side, _cls, _strict = old.ng_split(c)
        return "NG_ungradeable" if side == "ungradeable" else "NG_nothing"
    return {"OWN_DATE": "OWN", "PRIOR_CLOSE": "PRIOR"}[cl]


EXPECTED = {"OWN": {"ACCT_OWN_DATE", "UNGRADEABLE"}, "PRIOR": {"ACCT_PRIOR_DATE", "UNGRADEABLE"}, "NG_ungradeable": {"UNGRADEABLE"}, "NG_nothing": {"NOTHING_TO_GRADE"}}
GOOD = ("ACCT_OWN_DATE", "NOTHING_TO_GRADE")


def serve_v035(claims, days):
    """claims: {account: {day: claim}}.  Same eligibility as IB-pr-429.  Returns counts and per-account [eligible, served]."""
    r = {"eligible": 0, "served": 0, "blank": 0, "blank_by_reason": collections.Counter(), "per_account": {}}
    for a, byday in claims.items():
        r["per_account"][a] = [0, 0]
        for i in range(1, len(days)):
            d, p = days[i], days[i - 1]
            if d not in byday or p not in byday:
                continue
            cd, cp = byday[d], byday[p]
            r["eligible"] += 1
            r["per_account"][a][0] += 1
            if cd in GOOD and cp in GOOD:
                r["served"] += 1
                r["per_account"][a][1] += 1
            else:
                r["blank"] += 1
                r["blank_by_reason"][("today_" + cd) if cd not in GOOD else ("yesterday_" + cp)] += 1
    return r


# ---------------------------------------------------------------------------- the planted control

def control_run():
    """Fixture: 4 trading days D1..D4, six accounts, two moving securities S1 S2, one that does not move (FLAT); the anchor does not carry NOANCHOR.
      A: S1 S2 at the own close every day                                              new: OWN x4
      B: own D1, PRIOR close D2, own D3, D4                                            new: OWN, ACCT_PRIOR_DATE, OWN, OWN
      C: D1 cash only; D2 cash + FLAT; D3 S1 at neither close; D4 NOANCHOR priced      new: NOTHING, NOTHING, UNGRADEABLE [NEITHER_CLOSE], UNGRADEABLE [OUTSIDE_ANCHOR]
      E: D1 valued row no CUSIP; D2 negative position; D3 and D4 a row with null Units and Market Value
                                                                                       new: UNGRADEABLE [NO_CUSIP], UNGRADEABLE [NEGATIVE_POSITION], NOTHING x2
      F: D1 S1 S2 own + NOANCHOR priced row                      (IB-pr-429 read OWN_DATE)   new: UNGRADEABLE [OUTSIDE_ANCHOR]
         D2 S1 own + valued no-CUSIP row + negative position     (IB-pr-429 read OWN_DATE)   new: UNGRADEABLE [NEGATIVE_POSITION, NO_CUSIP]  (two kinds)
         D3 S1 at the PRIOR close + NOANCHOR priced row          (IB-pr-429 read PRIOR_CLOSE) new: UNGRADEABLE [OUTSIDE_ANCHOR]
         D4 S1 own only                                                                  new: ACCT_OWN_DATE
      H: S1 own every day; on D1 also a cash-flagged priced row outside the anchor        new: OWN x4 (primary treatment: that row is cash)
    Plus one separate call: a day whose anchor is not in hand reads its priced row as ANCHOR_NOT_LANDED."""
    days = ["D1", "D2", "D3", "D4"]
    anchors = {"D0": {"S1": 10.0, "S2": 20.0, "FLAT": 50.0}}
    for n, d in enumerate(days, start=1):
        anchors[d] = {"S1": 10.0 + n, "S2": 20.0 + 2 * n, "FLAT": 50.0}
    prev_of = {d: ("D0" if i == 0 else days[i - 1]) for i, d in enumerate(days)}
    new_claims = {a: {} for a in "ABCEFH"}
    old_claims = {a: {} for a in "ABCEFH"}
    new_kinds = {}
    cross = collections.Counter()
    sens_cash = 0
    for d in days:
        own, prev = anchors[d], anchors[prev_of[d]]
        rows = []   # (account, cusip, market value, units, cash flag)
        for a in "AB":
            lag = (a == "B" and d == "D2")
            for s in ("S1", "S2"):
                rows.append((a, s, (prev if lag else own)[s] * 10.0, 10.0, "false"))
        rows.append(("H", "S1", own["S1"] * 10.0, 10.0, "false"))
        if d == "D1":
            rows += [("C", None, 100.0, 0.0, "true"), ("E", None, 300.0, 10.0, "false"), ("H", "NOANCHOR", 50.0, 10.0, "true"),
                     ("F", "S1", own["S1"] * 10.0, 10.0, "false"), ("F", "S2", own["S2"] * 10.0, 10.0, "false"), ("F", "NOANCHOR", 50.0, 10.0, "false")]
        elif d == "D2":
            rows += [("C", None, 100.0, 0.0, "true"), ("C", "FLAT", 500.0, 10.0, "false"), ("E", "S1", -400.0, -10.0, "false"),
                     ("F", "S1", own["S1"] * 10.0, 10.0, "false"), ("F", None, 300.0, 10.0, "false"), ("F", "S2", -400.0, -10.0, "false")]
        elif d == "D3":
            rows += [("C", "S1", own["S1"] * 1.07 * 10.0, 10.0, "false"), ("E", "S2", None, None, "false"),
                     ("F", "S1", prev["S1"] * 10.0, 10.0, "false"), ("F", "NOANCHOR", 50.0, 10.0, "false")]
        else:
            rows += [("C", "NOANCHOR", 50.0, 10.0, "false"), ("E", "S2", None, None, "false"), ("F", "S1", own["S1"] * 10.0, 10.0, "false")]
        types = typed_rows([r[1] for r in rows], [r[2] for r in rows], [r[3] for r in rows], [r[4] for r in rows], own, prev)
        for a, rec in old.account_day_records([r[0] for r in rows], types).items():
            cl, kinds = claim_v035(rec)
            oc = old_class(rec)
            new_claims[a][d] = cl
            new_kinds[(a, d)] = kinds
            old_claims[a][d] = old.claim(rec)[0]
            cross[(oc, cl)] += 1
            if rec["cash_priced_outside_anchor"] and cl != "UNGRADEABLE":
                sens_cash += 1
    sv = serve_v035(new_claims, days)
    pa = [v for v in sv["per_account"].values() if v[0]]
    tally = collections.Counter(c for byday in new_claims.values() for c in byday.values())
    kind_days = collections.Counter(k for kk in new_kinds.values() for k in kk)
    # the separate ANCHOR_NOT_LANDED call: an anchor that is not in hand
    anl = typed_rows(["S1"], [100.0], [10.0], ["false"], None, anchors["D0"])
    anl_claim = claim_v035(old.account_day_records(["x"], anl)["x"])
    read = {
        "ACCT_OWN_DATE": tally["ACCT_OWN_DATE"], "ACCT_PRIOR_DATE": tally["ACCT_PRIOR_DATE"], "UNGRADEABLE": tally["UNGRADEABLE"], "NOTHING_TO_GRADE": tally["NOTHING_TO_GRADE"],
        "kind_account_days": {k: kind_days[k] for k in KINDS},
        "days_with_more_than_one_kind": sum(1 for kk in new_kinds.values() if len(kk) > 1),
        "OWN_DATE_to_UNGRADEABLE": cross[("OWN", "UNGRADEABLE")], "PRIOR_to_UNGRADEABLE": cross[("PRIOR", "UNGRADEABLE")],
        "not_graded_ungradeable_kept": cross[("NG_ungradeable", "UNGRADEABLE")], "not_graded_nothing_to_grade_kept": cross[("NG_nothing", "NOTHING_TO_GRADE")],
        "any_other_move": sum(v for (o, n), v in cross.items() if n not in EXPECTED[o]),
        "cash_flagged_priced_outside_anchor_would_move": sens_cash,
        "served": sv["served"], "blank": sv["blank"], "blank_by_reason": dict(sv["blank_by_reason"]),
        "accounts_never_always_sometimes": [sum(1 for e, s in pa if s == 0), sum(1 for e, s in pa if s == e), sum(1 for e, s in pa if 0 < s < e)],
        "own_rows_with_an_ungradeable_priced_row_reads_UNGRADEABLE": (old_claims["F"]["D1"] == "OWN_DATE" and new_claims["F"]["D1"] == "UNGRADEABLE"
                                                                       and old_claims["F"]["D2"] == "OWN_DATE" and new_claims["F"]["D2"] == "UNGRADEABLE"),
        "day_with_two_kinds_lists_both": new_kinds[("F", "D2")] == ["NEGATIVE_POSITION", "NO_CUSIP"],
        "anchor_absent_day_reads_ANCHOR_NOT_LANDED": anl_claim == ("UNGRADEABLE", ["ANCHOR_NOT_LANDED"]),
    }
    return read


# Known BY CONSTRUCTION from the fixture's description above, counted by hand (not by the code): 24 account-days.
# ACCT_OWN_DATE 12 (A 4, B 3, F D4, H 4); ACCT_PRIOR_DATE 1 (B D2); UNGRADEABLE 7 (C D3 D4, E D1 D2, F D1 D2 D3); NOTHING_TO_GRADE 4 (C D1 D2, E D3 D4).
# Kinds' account-days: OUTSIDE_ANCHOR 3 (C D4, F D1, F D3), NO_CUSIP 2 (E D1, F D2), NEITHER_CLOSE 1 (C D3), NEGATIVE_POSITION 2 (E D2, F D2), ANCHOR_NOT_LANDED 0;
# one day with two kinds (F D2).  Moves against IB-pr-429: OWN->UNGRADEABLE 2 (F D1, F D2), PRIOR->UNGRADEABLE 1 (F D3), NOT_GRADED ungradeable kept 4
# (C D3 D4, E D1 D2), NOT_GRADED nothing kept 4 (C D1 D2, E D3 D4), no other move.  Cash-flagged priced outside the anchor: H D1 (stays ACCT_OWN_DATE) -> would move 1.
# Serving: eligible 18 (D2..D4 x 6).  Good = OWN or NOTHING.  A 3 served; B 1 (D4: D2 prior, D3 follows prior); C 1 (D2); E 1 (D4); F 0; H 3 -> served 9, blank 9
# = today_ACCT_PRIOR_DATE 1 (B D2), yesterday_ACCT_PRIOR_DATE 1 (B D3), today_UNGRADEABLE 5 (C D3 D4, E D2, F D2 D3), yesterday_UNGRADEABLE 2 (E D3, F D4).
# Accounts: never 1 (F), always 2 (A, H), sometimes 3 (B, C, E).
PLANTED = {
    "ACCT_OWN_DATE": 12, "ACCT_PRIOR_DATE": 1, "UNGRADEABLE": 7, "NOTHING_TO_GRADE": 4,
    "kind_account_days": {"ANCHOR_NOT_LANDED": 0, "OUTSIDE_ANCHOR": 3, "NO_CUSIP": 2, "NEITHER_CLOSE": 1, "NEGATIVE_POSITION": 2},
    "days_with_more_than_one_kind": 1,
    "OWN_DATE_to_UNGRADEABLE": 2, "PRIOR_to_UNGRADEABLE": 1, "not_graded_ungradeable_kept": 4, "not_graded_nothing_to_grade_kept": 4, "any_other_move": 0,
    "cash_flagged_priced_outside_anchor_would_move": 1,
    "served": 9, "blank": 9,
    "blank_by_reason": {"today_ACCT_PRIOR_DATE": 1, "yesterday_ACCT_PRIOR_DATE": 1, "today_UNGRADEABLE": 5, "yesterday_UNGRADEABLE": 2},
    "accounts_never_always_sometimes": [1, 2, 3],
    "own_rows_with_an_ungradeable_priced_row_reads_UNGRADEABLE": True,
    "day_with_two_kinds_lists_both": True,
    "anchor_absent_day_reads_ANCHOR_NOT_LANDED": True,
}
FIXTURE = ("4 trading days, six accounts, 2 moving securities and one that does not move.  A own every day.  B is at the prior close on D2.  C: cash only D1, cash + an "
           "unmoved security D2, a moved row at neither close D3, a priced security outside the anchor D4.  E: a valued row with no CUSIP D1, a negative position D2, a row "
           "with null Units and Market Value D3 and D4.  F (new): D1 own rows + a priced security outside the anchor; D2 an own row + a valued row with no CUSIP + a negative "
           "position (two kinds in one account-day); D3 a prior-close row + a priced security outside the anchor; D4 an own row.  H (new): own rows every day and, on D1, a "
           "cash-flagged priced row outside the anchor.  One separate call: a day whose anchor is not in hand.")


def control():
    return {"planted": PLANTED, "read": control_run(), "fixture": FIXTURE}


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
    graded_days, ungradeable_days, anchor_not_landed_days = [], [], []
    claims_new = collections.defaultdict(dict)      # account -> day -> new claim
    claims_old = collections.defaultdict(dict)      # account -> day -> (claim, side, strict) as IB-pr-429 (for old.serve)
    new_tally, old_tally = collections.Counter(), collections.Counter()
    cross = collections.Counter()
    kind_days = collections.Counter()
    combos = collections.Counter()
    multi, no_kind = 0, 0
    sens_cash_total, sens_cash_would_move = 0, 0
    rows_tot = collections.Counter()
    sixth = {"rows": 0, "account_days": 0, "by_sign": collections.Counter(), "account_days_claim": collections.Counter()}
    for i, d in enumerate(tdays):
        p = tc.prev_trading_day(dt.date.fromisoformat(d)).isoformat()
        s = load("src", d)
        A, B = anchor(d), anchor(p)
        if s in (None, "UNREAD") or A == "UNREAD" or B == "UNREAD":
            ungradeable_days.append(d)
            continue
        if i == 0 or tdays[i - 1] != p:
            continue  # FIRST_DAY_NO_PRIOR: outside the totals
        if A is None or B is None:
            anchor_not_landed_days.append(d)
            A, B = (None, None)
        graded_days.append(d)
        types = typed_rows(s["CUSIP"], s["Market Value"], s["Units"], s["Cash Equivalent"], A, B)
        rec = old.account_day_records(s["AccountID"], types)
        acct_all.update(rec)
        for t in types:
            if t in ("own", "prior", "neither"):
                rows_tot[t] += 1
                rows_tot["moved"] += 1
        # sixth-reason probe: a non-cash row with a non-zero Market Value that no kind and no price covers (Units null, zero, or of the opposite sign)
        sixth_acct = set()
        for a, t, u, m in zip(s["AccountID"], types, s["Units"], s["Market Value"]):
            if t == "no_price":
                un, mn = old.num(u), old.num(m)
                if mn is not None and mn != 0:
                    sixth["rows"] += 1
                    sixth["by_sign"]["units_%s_mv_%s" % ("null" if un is None else "zero" if un == 0 else "pos" if un > 0 else "neg", "pos" if mn > 0 else "neg")] += 1
                    sixth_acct.add(a)
        for a, c in rec.items():
            cl, kinds = claim_v035(c)
            oc = old_class(c)
            ocl, _ = old.claim(c)
            oside = old.ng_split(c) if ocl == "NOT_GRADED" else (None, None, None)
            claims_old[a][d] = (ocl, oside[0], oside[2])
            claims_new[a][d] = cl
            new_tally["present"] += 1
            new_tally[cl] += 1
            old_tally["present"] += 1
            old_tally[oc] += 1
            cross[(oc, cl)] += 1
            if cl == "UNGRADEABLE":
                for k in kinds:
                    kind_days[k] += 1
                if len(kinds) > 1:
                    multi += 1
                if not kinds:
                    no_kind += 1
                combos["+".join(kinds) if kinds else "NONE"] += 1
            if c["cash_priced_outside_anchor"]:
                sens_cash_total += 1
                if cl != "UNGRADEABLE":
                    sens_cash_would_move += 1
            if a in sixth_acct:
                sixth["account_days"] += 1
                sixth["account_days_claim"][cl] += 1
    assert new_tally["present"] == sum(len(v) for v in claims_new.values()) == sum(new_tally[k] for k in ("UNGRADEABLE", "ACCT_PRIOR_DATE", "ACCT_OWN_DATE", "NOTHING_TO_GRADE"))

    # ---- IB-pr-429's totals, from THIS run's old logic, against its file
    old_ung, old_nothing = old_tally["NG_ungradeable"], old_tally["NG_nothing"]
    this_old = {"present": old_tally["present"], "OWN_DATE": old_tally["OWN"], "PRIOR_CLOSE": old_tally["PRIOR"], "ungradeable": old_ung, "nothing_to_grade": old_nothing}
    same = this_old == OLD_FILE
    any_other = sum(v for (o, n), v in cross.items() if n not in EXPECTED[o])
    moves = {"same_account_days_read": same,
             "OWN_DATE_to_UNGRADEABLE": cross[("OWN", "UNGRADEABLE")], "PRIOR_to_UNGRADEABLE": cross[("PRIOR", "UNGRADEABLE")],
             "not_graded_ungradeable_kept": cross[("NG_ungradeable", "UNGRADEABLE")], "not_graded_nothing_to_grade_kept": cross[("NG_nothing", "NOTHING_TO_GRADE")],
             "any_other_move": any_other}
    cross_table = {"%s->%s" % k: v for k, v in sorted(cross.items())}

    # ---- the serving rule, new and old (old alternative = v0.34's rule), same pass
    sv = serve_v035(claims_new, graded_days)
    pa = [v for v in sv["per_account"].values() if v[0]]
    never = sum(1 for e, s_ in pa if s_ == 0)
    always = sum(1 for e, s_ in pa if s_ == e)
    old_sv = old.serve(claims_old, graded_days)
    o_alt, o_wr = old.summarize_serving(old_sv["alternative"]), old.summarize_serving(old_sv["as_written"])
    d0 = graded_days[0]
    first_day = {"first_graded_day": d0, "its_prior_partition": old.first_graded_prior(tdays, d0),
                 "treatment": "As IB-pr-429: the prior partition of the first graded day (%s) is ungraded, so no claim exists for it.  The account-days of %s are claimed "
                              "and counted in account_days, but are NOT eligible and are outside the serving counts.  Eligible account-days are those present today and on the "
                              "prior GRADED day." % (tdays[tdays.index(d0) - 1], d0)}
    # ---- timing from the objects' LastModified (times only), this run
    landed_after = 0
    old_doc = json.load(open(root / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~288/IB127-1_account_day_claims.json", encoding="utf-8"))
    for d in graded_days:
        sm, am = load("src", d)["_meta"], load("anc", d)["_meta"]
        if dt.datetime.fromisoformat(am["last_modified_utc"]) > dt.datetime.fromisoformat(sm["last_modified_utc"]):
            landed_after += 1
    anchor_timing = {"graded_days": len(graded_days), "anchor_landed_after_the_cottonwood_partition": landed_after,
                     "cottonwood_partition_landed_after_the_anchor": len(graded_days) - landed_after,
                     "ib_pr_429_file_said_anchor_landed_last_on": old_doc["instrument_input_timing"]["all_graded_days"]["anchor_landed_last"],
                     "note": "from object LastModified (list_objects_v2), latest object per partition, this run; counts only.  A later rewrite of an old day shows the rewrite "
                             "time.  Not turned into claims."}

    doc = {
        "source": {"bucket": src["bucket"], "entry": "blackdiamond_z09", "prefix_template": src["positions_prefix"] + "date=YYYY-MM-DD/",
                   "prefix_resolved_by": "holdings_performance.resolved_prefix(blackdiamond_z09, positions_prefix, firm_scope) -> %d characters, same as the gold script" % len(prefix_resolved),
                   "anchor": "%s%s (closing_price by cusip; the Schwab own-date close)" % (anchor_prefix, "date=YYYY-MM-DD/"),
                   "price": "Market Value / Units, rows with Units > 0 and Market Value > 0 and a CUSIP",
                   "account_key": "AccountID, replaced at read time by a one-way digest; used only to group rows, never written"},
        "tolerance": {"kind": "relative", "value": old.TOL, "rule": "abs(a-b) <= 1e-4 * max(abs(a), abs(b), 1e-9)"},
        "rule": "PRD ADDENDUM v0.35, ordered, the first that applies: (1) UNGRADEABLE: one or more priced securities the instrument cannot place at a close, whatever the "
                "other rows read, with the list of every kind present from ANCHOR_NOT_LANDED, OUTSIDE_ANCHOR, NO_CUSIP, NEITHER_CLOSE, NEGATIVE_POSITION; (2) ACCT_PRIOR_DATE; "
                "(3) ACCT_OWN_DATE; (4) NOTHING_TO_GRADE.  Row kinds as IB-pr-429's row_types: OUTSIDE_ANCHOR = outside_anchor, NO_CUSIP = no_cusip, NEITHER_CLOSE = a moved "
                "priced row at neither close, NEGATIVE_POSITION = negative_position; ANCHOR_NOT_LANDED = the anchor's close for the day or the prior trading day is absent "
                "from the anchor at read time.",
        "days": len(graded_days), "range_graded": [graded_days[0], graded_days[-1]], "days_ungradeable_outside_the_85": ungradeable_days,
        "accounts": len(acct_all),
        "account_days": {"present": new_tally["present"], "UNGRADEABLE": new_tally["UNGRADEABLE"], "ACCT_PRIOR_DATE": new_tally["ACCT_PRIOR_DATE"],
                         "ACCT_OWN_DATE": new_tally["ACCT_OWN_DATE"], "NOTHING_TO_GRADE": new_tally["NOTHING_TO_GRADE"]},
        "ib_pr_429_rule_this_run": this_old,
        "ib_pr_429_file": OLD_FILE,
        "moves_against_IB_pr_429": moves,
        "claim_cross_count_old_class_to_new_claim": cross_table,
        "ungradeable_kinds": {
            "account_days_holding_each_kind": {k: kind_days[k] for k in KINDS},
            "days_with_more_than_one_kind": multi,
            "ungradeable_days_with_no_kind": no_kind,
            "kind_combinations": dict(sorted(combos.items(), key=lambda kv: -kv[1])),
            "anchor_not_landed_days_now": len(anchor_not_landed_days),
            "anchor_not_landed_note": "the days of the 85 whose own or prior-day anchor partition is absent from the anchor at read time; the days are listed by count only",
            "anchor_landing_order": anchor_timing},
        "cash_flagged_priced_outside_anchor": {
            "treatment": "primary: as IB-pr-429, a cash-flagged priced row outside the anchor is cash (nothing to grade), not OUTSIDE_ANCHOR.  The addendum does not say; the CTO rules it.",
            "account_days": sens_cash_total,
            "would_move_if_ungradeable": sens_cash_would_move,
            "would_move_note": "account-days holding such a row whose claim is not already UNGRADEABLE; they would change claim to UNGRADEABLE"},
        "serving_rule": {"eligible": sv["eligible"], "served": sv["served"], "blank": sv["blank"], "blank_by_reason": dict(sv["blank_by_reason"]),
                         "blank_share_percent": round(100.0 * sv["blank"] / sv["eligible"], 3),
                         "accounts": {"with_eligible_days": len(pa), "never_served": never, "always_served": always, "sometimes_served": len(pa) - never - always},
                         "first_day_treatment": first_day,
                         "blank_reason_order": "today_UNGRADEABLE, today_ACCT_PRIOR_DATE, yesterday_UNGRADEABLE, yesterday_ACCT_PRIOR_DATE (the first that applies)",
                         "good_claims": "ACCT_OWN_DATE or NOTHING_TO_GRADE, today and the prior trading day"},
        "v0_34_rule_same_pass": {"note": "IB-pr-429's alternative (good = OWN_DATE or nothing_to_grade), run on the same rows; the v0.34 floor was 25.0 percent of 75,796 and 169 of 999",
                                 "alternative": o_alt, "as_written": o_wr},
        "sixth_reason_rows": {
            "rows": sixth["rows"], "account_days": sixth["account_days"], "account_days_by_new_claim": dict(sixth["account_days_claim"]),
            "rows_by_sign_of_units_and_market_value": dict(sixth["by_sign"]),
            "description": "non-cash rows with a non-zero Market Value that the instrument does not price (Units null, zero or of the opposite sign to Market Value) and that "
                           "are neither a NO_CUSIP row (Units > 0, Market Value > 0, no CUSIP) nor a NEGATIVE_POSITION row (both negative).  Such a row has no price, so rule 4 "
                           "reads it as 'rows with no price'; it is counted here, not fitted to one of the five kinds and not made a kind.",
            "treatment_in_the_counts": "the row adds no kind and moves no claim: its account-day reads by its other rows (see account_days_by_new_claim)"},
        "rows_moved": dict(rows_tot),
        "control": control(),
    }
    out.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    print("wrote", out, "days", len(graded_days), "accounts", len(acct_all), dict(new_tally), moves)
    return 0


if __name__ == "__main__":
    sys.exit(main())
