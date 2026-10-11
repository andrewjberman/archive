#!/usr/bin/env python3
"""IB-pr-435 phase A: the securities behind OUTSIDE_ANCHOR ranked, and the CTO-ruled cash rule counted, on the same 85 partitions as IB-pr-429 / its
AMENDMENT 2.  Read only.  Imports the row typing (ib429_claims.row_types via ib429_claims_v035.typed_rows), the ordered claim rule (claim_v035) and the
serving counter (serve_v035) UNCHANGED; the partitions are the cache of ib433_fetch.py (outside the repo, AccountID already a 12-character one-way digest).

    python -I ib435_measure.py <cache_dir> <phaseA.pkl>      measure (the pickle holds counts and security identifiers only, no account key)
    python -I ib435_measure.py --control                     run only the planted cash-rule control

THE CASH RULE (CTO msg 5082): a cash-flagged priced row the anchor does not carry (row type cash_priced_outside_anchor) is cash ONLY WHERE the source's own
price for that row (Market Value / Units, the row filter Units > 0 and Market Value > 0 and a CUSIP) is EQUAL, within the tolerance 1e-4 relative, in the day's
partition and in the prior trading day's partition for the same account and CUSIP.  Otherwise the row is OUTSIDE_ANCHOR:
  equal               the prior trading day's partition holds a priced row of that account and CUSIP at an equal price
  differs             it holds priced row(s) of that account and CUSIP, none at an equal price
  not_comparable      it holds no priced row of that account and CUSIP (or the prior partition is not in hand)
A not-comparable row is NOT cash ("only where measured"): it is typed OUTSIDE_ANCHOR in the primary counts; the other treatment is also counted.
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
import ib429_claims_v035 as v35  # noqa: E402

EXPECTED_V035 = {"present": 76796, "UNGRADEABLE": 42967, "ACCT_OWN_DATE": 20138, "NOTHING_TO_GRADE": 13636, "ACCT_PRIOR_DATE": 55}
CLAIMS = ("UNGRADEABLE", "ACCT_PRIOR_DATE", "ACCT_OWN_DATE", "NOTHING_TO_GRADE")


def prior_index(rows):
    """{(account, cusip): [price, ...]} for the priced rows of one partition (the existing row filter)."""
    idx = collections.defaultdict(list)
    if rows is None:
        return idx
    for i, (c, p) in old.price_rows(rows["CUSIP"], rows["Market Value"], rows["Units"]).items():
        idx[(rows["AccountID"][i], c)].append(p)
    return idx


def cash_outcome(account, cusip, price, prev_idx):
    """equal | differs | not_comparable, for one cash-flagged priced row outside the anchor."""
    ps = prev_idx.get((account, cusip))
    if not ps:
        return "not_comparable"
    return "equal" if any(old.same(price, q) for q in ps) else "differs"


def reclassify(c, outcomes, not_comparable_is_cash=False):
    """The account-day's row-type counter with its cash_priced_outside_anchor rows re-typed by the rule: equal -> cash; differs -> outside_anchor;
    not_comparable -> outside_anchor (primary) or cash (the other treatment)."""
    c2 = collections.Counter(c)
    for o in outcomes:
        c2["cash_priced_outside_anchor"] -= 1
        if o == "equal" or (o == "not_comparable" and not_comparable_is_cash):
            c2["cash"] += 1
        else:
            c2["outside_anchor"] += 1
    return c2


# ---------------------------------------------------------------------------- the planted control (cash rule)

def control_cash_run():
    """Fixture: 3 trading days D1..D3, anchor carries S1 only.  Accounts (all hold S1 at the own close every day, which is graded OWN, and a cash-flagged
    priced row of NOANCHOR):
      X: NOANCHOR at 5.0 on D1, D2, D3            -> D2 equal, D3 equal         -> cash both days   (ACCT_OWN_DATE stays)
      Y: NOANCHOR at 5.0 on D1, at 6.0 on D2      -> D2 differs                 -> OUTSIDE_ANCHOR   (UNGRADEABLE)
      Z: NOANCHOR first held on D2 (absent D1)    -> D2 not comparable          -> OUTSIDE_ANCHOR primary, cash in the other treatment
      W: NOANCHOR on D2 only at 5.0 and on D3 at 5.0 + 1e-6 (inside the tolerance) -> D3 equal (not comparable on D2)
    Known by construction (counted by hand): D2 and D3 are the graded days; outcomes D2: X equal, Y differs, Z not_comparable, W not_comparable; D3: X equal,
    Y not_comparable (Y has no NOANCHOR row on D3: no row), Z not held, W equal."""
    anchors = {"D0": {"S1": 10.0}, "D1": {"S1": 11.0}, "D2": {"S1": 12.0}, "D3": {"S1": 13.0}}
    days = ["D1", "D2", "D3"]
    held = {  # (account, day) -> NOANCHOR price
        ("X", "D1"): 5.0, ("X", "D2"): 5.0, ("X", "D3"): 5.0,
        ("Y", "D1"): 5.0, ("Y", "D2"): 6.0,
        ("Z", "D2"): 5.0,
        ("W", "D2"): 5.0, ("W", "D3"): 5.0 + 1e-6,
    }
    out = collections.Counter()
    claims_primary, claims_other = collections.defaultdict(dict), collections.defaultdict(dict)
    parts = {}
    for i, d in enumerate(days):
        accts = ["X", "Y", "Z", "W"]
        rows = [(a, "S1", anchors[d]["S1"] * 10.0, 10.0, "false") for a in accts]
        rows += [(a, "NOANCHOR", p * 10.0, 10.0, "true") for (a, dd), p in sorted(held.items()) if dd == d]
        parts[d] = dict(AccountID=[r[0] for r in rows], CUSIP=[r[1] for r in rows], **{"Market Value": [r[2] for r in rows], "Units": [r[3] for r in rows]})
        if i == 0:
            continue   # D1 has no graded prior in the fixture; it is only the prior partition of D2
        p = days[i - 1]
        types = v35.typed_rows(parts[d]["CUSIP"], parts[d]["Market Value"], parts[d]["Units"], [r[4] for r in rows], anchors[d], anchors[p])
        idx = prior_index(parts[p])
        outcomes = collections.defaultdict(list)
        for k, (a, t) in enumerate(zip(parts[d]["AccountID"], types)):
            if t == "cash_priced_outside_anchor":
                o = cash_outcome(a, parts[d]["CUSIP"][k], parts[d]["Market Value"][k] / parts[d]["Units"][k], idx)
                outcomes[a].append(o)
                out["%s_%s" % (d, o)] += 1
        for a, c in old.account_day_records(parts[d]["AccountID"], types).items():
            claims_primary[a][d] = v35.claim_v035(reclassify(c, outcomes.get(a, [])))[0]
            claims_other[a][d] = v35.claim_v035(reclassify(c, outcomes.get(a, []), True))[0]
    return {
        "outcomes": dict(sorted(out.items())),
        "primary_D2": {a: claims_primary[a]["D2"] for a in "XYZW"}, "primary_D3": {a: claims_primary[a]["D3"] for a in "XYZW"},
        "not_comparable_as_cash_D2": {a: claims_other[a]["D2"] for a in "XYZW"},
    }


# Known BY CONSTRUCTION from the fixture above (counted by hand, not by the code).  D2 cash rows: X (prior 5.0, now 5.0) equal; Y (prior 5.0, now 6.0) differs;
# Z (absent D1) not_comparable; W (absent D1) not_comparable.  D3 cash rows: X equal; W (prior 5.0 on D2, now 5.0+1e-6, inside 1e-4 relative) equal.  Y and Z hold no row on D3.
# Claims, the anchor moves every day and S1 is held at the own close: a day with no outside_anchor row reads ACCT_OWN_DATE; one with reads UNGRADEABLE.
# Primary treatment: D2 X OWN, Y UNGRADEABLE, Z UNGRADEABLE, W UNGRADEABLE; D3 X OWN, Y OWN, Z OWN, W OWN.  Other treatment (not comparable stays cash): D2 Z and W OWN.
PLANTED_CASH = {
    "outcomes": {"D2_differs": 1, "D2_equal": 1, "D2_not_comparable": 2, "D3_equal": 2},
    "primary_D2": {"X": "ACCT_OWN_DATE", "Y": "UNGRADEABLE", "Z": "UNGRADEABLE", "W": "UNGRADEABLE"},
    "primary_D3": {"X": "ACCT_OWN_DATE", "Y": "ACCT_OWN_DATE", "Z": "ACCT_OWN_DATE", "W": "ACCT_OWN_DATE"},
    "not_comparable_as_cash_D2": {"X": "ACCT_OWN_DATE", "Y": "UNGRADEABLE", "Z": "ACCT_OWN_DATE", "W": "ACCT_OWN_DATE"},
}


# ---------------------------------------------------------------------------- the measurement

def main():
    if sys.argv[1:] == ["--control"]:
        r = control_cash_run()
        print(json.dumps(r, indent=1), "\nEQUAL:", r == PLANTED_CASH)
        return 0 if r == PLANTED_CASH else 1
    cache, out = Path(sys.argv[1]), Path(sys.argv[2])
    root = Path(__file__).resolve().parents[7]
    sys.path[:0] = [str(root / "lib"), str(root)]
    import trading_calendar as tc

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

    graded_days, outside_days = [], []
    claims_pre = collections.defaultdict(dict)       # the v0.35 claim (cash-flagged rows read as cash), the re-count's own
    claims_cash = collections.defaultdict(dict)      # under the cash rule, not-comparable NOT cash (primary)
    claims_cash_nc = collections.defaultdict(dict)   # under the cash rule, not-comparable stays cash (the other treatment)
    tally_pre, tally_cash, tally_cash_nc = collections.Counter(), collections.Counter(), collections.Counter()
    carried = collections.defaultdict(set)           # cusip -> {(account, day)}   pre-cash-rule OUTSIDE_ANCHOR rows
    carried_added = collections.defaultdict(set)     # cusip -> {(account, day)}   OUTSIDE_ANCHOR by the cash rule (differs or not comparable), not already carried
    carried_added_nc = collections.defaultdict(set)  # same, but only the rows whose price differs
    ad_cusips = collections.defaultdict(set)         # (account, day) -> cusips, pre-cash OUTSIDE_ANCHOR
    ad_cusips_cash = collections.defaultdict(set)    # (account, day) -> cusips, OUTSIDE_ANCHOR after the cash rule (primary)
    ad_other_kind = {}                               # (account, day) -> True if it holds a kind other than OUTSIDE_ANCHOR (pre-cash)
    ad_other_kind_cash = {}
    idents = collections.defaultdict(collections.Counter)   # cusip -> Counter of ticker/symbol values
    names = collections.defaultdict(collections.Counter)    # cusip -> Counter of asset names
    cash_ad = {}                                     # (account, day) -> outcomes list of its cash_priced_outside_anchor rows
    cash_rows = collections.Counter()
    multi_prior_rows = 0
    sixth = {"rows": 0, "account_days": set()}
    sixth_claim = collections.Counter()
    for i, d in enumerate(tdays):
        p = tc.prev_trading_day(dt.date.fromisoformat(d)).isoformat()
        s = load("src", d)
        A, B = anchor(d), anchor(p)
        if s in (None, "UNREAD") or A == "UNREAD" or B == "UNREAD":
            outside_days.append(d)
            continue
        if i == 0 or tdays[i - 1] != p:
            continue
        if A is None or B is None:
            A, B = (None, None)
        graded_days.append(d)
        sp = load("src", p)
        pidx = prior_index(sp if sp not in (None, "UNREAD") else None)
        types = v35.typed_rows(s["CUSIP"], s["Market Value"], s["Units"], s["Cash Equivalent"], A, B)
        accts = s["AccountID"]
        priced = old.price_rows(s["CUSIP"], s["Market Value"], s["Units"])
        outcomes = collections.defaultdict(list)
        cash_cusips = collections.defaultdict(list)
        sixth_acct = set()
        for k, t in enumerate(types):
            a = accts[k]
            if t == "outside_anchor":
                c = priced[k][0]
                carried[c].add((a, d))
                ad_cusips[(a, d)].add(c)
                ad_cusips_cash[(a, d)].add(c)
                tk = {str(x).strip() for x in (s["Ticker"][k], s["Symbol"][k]) if x not in (None, "") and str(x).strip() and str(x).strip().lower() != "none"}
                for x in tk:
                    idents[c][x] += 1
                nm = s["Asset Name"][k]
                if nm not in (None, ""):
                    names[c][str(nm).strip()] += 1
            elif t == "cash_priced_outside_anchor":
                c, price = priced[k]
                o = cash_outcome(a, c, price, pidx)
                if o == "differs" and len(pidx.get((a, c), [])) > 1:
                    multi_prior_rows += 1
                outcomes[a].append(o)
                cash_cusips[a].append((c, o))
                cash_rows[o] += 1
                tk = {str(x).strip() for x in (s["Ticker"][k], s["Symbol"][k]) if x not in (None, "") and str(x).strip() and str(x).strip().lower() != "none"}
                for x in tk:
                    idents[c][x] += 1
                nm = s["Asset Name"][k]
                if nm not in (None, ""):
                    names[c][str(nm).strip()] += 1
            elif t == "no_price":
                mn = old.num(s["Market Value"][k])
                if mn is not None and mn != 0:
                    sixth["rows"] += 1
                    sixth_acct.add(a)
        rec = old.account_day_records(accts, types)
        for a, c in rec.items():
            pre, kinds = v35.claim_v035(c)
            claims_pre[a][d] = pre
            tally_pre["present"] += 1
            tally_pre[pre] += 1
            oc = outcomes.get(a, [])
            c1, c2 = reclassify(c, oc), reclassify(c, oc, True)
            cl1, k1 = v35.claim_v035(c1)
            cl2, _ = v35.claim_v035(c2)
            claims_cash[a][d] = cl1
            claims_cash_nc[a][d] = cl2
            tally_cash["present"] += 1
            tally_cash[cl1] += 1
            tally_cash_nc["present"] += 1
            tally_cash_nc[cl2] += 1
            ad_other_kind[(a, d)] = any(kk != "OUTSIDE_ANCHOR" for kk in kinds)
            ad_other_kind_cash[(a, d)] = any(kk != "OUTSIDE_ANCHOR" for kk in k1)
            if a in sixth_acct:
                sixth["account_days"].add((a, d))
                sixth_claim[pre] += 1
            for cu, o in cash_cusips.get(a, []):
                if o != "equal":
                    ad_cusips_cash[(a, d)].add(cu)
                    if cu not in ad_cusips.get((a, d), ()):
                        carried_added[cu].add((a, d))
                    if o == "differs":
                        carried_added_nc[cu].add((a, d))
            if oc:
                cash_ad[(a, d)] = (pre, oc)
    assert tally_pre["present"] == sum(len(v) for v in claims_pre.values()) == sum(tally_pre[k] for k in CLAIMS)
    same = {k: tally_pre[k] for k in EXPECTED_V035} == EXPECTED_V035

    # --- the cash rule's account-days: the cash-flagged account-days (re-count: 31,307) and those that would move (19,809)
    cash_account_days = len(cash_ad)
    examined = [(k, v) for k, v in cash_ad.items() if v[0] != "UNGRADEABLE"]
    stays = sum(1 for k, (pre, oc) in examined if all(o == "equal" for o in oc))
    differs = sum(1 for k, (pre, oc) in examined if any(o == "differs" for o in oc))
    notcomp = sum(1 for k, (pre, oc) in examined if not any(o == "differs" for o in oc) and any(o == "not_comparable" for o in oc))
    all_ad = collections.Counter()
    for k, (pre, oc) in cash_ad.items():
        all_ad["differs" if "differs" in oc else "not_comparable" if "not_comparable" in oc else "equal"] += 1

    sv_pre = v35.serve_v035(claims_pre, graded_days)
    sv = v35.serve_v035(claims_cash, graded_days)
    sv_nc = v35.serve_v035(claims_cash_nc, graded_days)

    def serving(r):
        pa = [v for v in r["per_account"].values() if v[0]]
        return {"eligible": r["eligible"], "served": r["served"], "blank": r["blank"], "blank_by_reason": dict(r["blank_by_reason"]),
                "blank_share_percent": round(100.0 * r["blank"] / r["eligible"], 3),
                "accounts_with_eligible_days": len(pa), "accounts_never_served": sum(1 for e, s_ in pa if s_ == 0),
                "accounts_always_served": sum(1 for e, s_ in pa if s_ == e)}

    doc = {
        "graded_days": graded_days, "days_outside_the_85": outside_days,
        "same_account_days_read": same, "v035_totals": {k: tally_pre[k] for k in EXPECTED_V035}, "expected_v035_totals": EXPECTED_V035,
        "claims_pre": dict(tally_pre), "claims_cash_rule": dict(tally_cash), "claims_cash_rule_not_comparable_stays_cash": dict(tally_cash_nc),
        "serving_pre": serving(sv_pre), "serving_cash_rule": serving(sv), "serving_cash_rule_not_comparable_stays_cash": serving(sv_nc),
        "cash_account_days_all": cash_account_days, "cash_account_days_examined": len(examined),
        "cash_outcome_account_days": {"price_equal_both_days_stays_cash": stays, "price_differs_becomes_OUTSIDE_ANCHOR": differs, "not_comparable": notcomp},
        "cash_outcome_account_days_all_31k": dict(all_ad), "cash_rows_by_outcome": dict(cash_rows), "cash_rows_differs_with_several_prior_rows": multi_prior_rows,
        "sixth_reason": {"rows": sixth["rows"], "account_days": len(sixth["account_days"]), "account_days_by_claim": dict(sixth_claim)},
        "account_days_holding_an_outside_anchor_row": len(ad_cusips),
        "security_account_days_total": sum(len(v) for v in carried.values()),
        "added_by_the_cash_rule": {"security_account_days": sum(len(v) for v in carried_added.values()),
                                   "of_which_price_differs": sum(len(v) for v in carried_added_nc.values()),
                                   "securities_new_to_the_ranking": sum(1 for c in carried_added if c not in carried),
                                   "securities_touched": len(carried_added),
                                   "account_days_holding_an_outside_anchor_row_after": len(ad_cusips_cash)},
        "securities": {c: {"account_days": len(v), "tickers": [k for k, _ in idents[c].most_common()], "name": (names[c].most_common(1) or [("", 0)])[0][0]}
                       for c, v in carried.items()},
        "securities_added": {c: {"account_days": len(v), "tickers": [k for k, _ in idents[c].most_common()], "name": (names[c].most_common(1) or [("", 0)])[0][0]}
                             for c, v in carried_added.items()},
        # needed security-days: the day AND the prior trading day of every carried account-day (distinct dates per security)
        "needed_dates": {}, "needed_dates_added": {},
        # anonymous account-day structure: cusip sets per account-day (no account key, no date)
        "ad_structure_pre": collections.Counter((frozenset(v), ad_other_kind[k]) for k, v in ad_cusips.items()),
        "ad_structure_cash": collections.Counter((frozenset(v), ad_other_kind_cash[k]) for k, v in ad_cusips_cash.items()),
    }
    prev_of = {d: tc.prev_trading_day(dt.date.fromisoformat(d)).isoformat() for d in graded_days}
    for key, src in (("needed_dates", carried), ("needed_dates_added", carried_added)):
        for c, v in src.items():
            ds = {d for _, d in v}
            doc[key][c] = sorted(ds | {prev_of[d] for d in ds})
    doc["control_cash"] = {"planted": PLANTED_CASH, "read": control_cash_run()}
    pickle.dump(doc, open(out, "wb"))
    print("wrote", out, "days", len(graded_days), "same", same, doc["v035_totals"], "OA account-days", len(ad_cusips), "securities", len(carried),
          "cash examined", len(examined), doc["cash_outcome_account_days"], "all", cash_account_days)
    return 0


if __name__ == "__main__":
    sys.exit(main())
