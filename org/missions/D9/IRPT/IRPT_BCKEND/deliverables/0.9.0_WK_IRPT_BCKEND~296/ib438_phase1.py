#!/usr/bin/env python3
"""IB-pr-438 phase 1: the securities behind OUTSIDE_ANCHOR under the cash rule in force, and the anonymous account-day structure.  Read only.
Same source partitions (the cache of ib433_fetch.py, outside the repo, AccountID already a 12-character one-way digest), same price rule, tolerance,
trading-day axis, row typing, ordered claim rule and cash rule as IB-pr-435 / IB-pr-436 (their modules imported UNCHANGED).

    python -I ib438_phase1.py <partition_cache> <phase1.pkl> <tickers.json>

The pickle (outside the repo) holds the account-day structure under a one-way digest; no output of the repo ever carries it.
"""
from __future__ import annotations

import collections
import datetime as dt
import json
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
sys.path.insert(0, str(D / "0.9.0_WK_IRPT_BCKEND~293"))    # ib435_measure (merged); it imports ib429_claims / ib429_claims_v035 from the same folder
import ib429_claims as old  # noqa: E402
import ib429_claims_v035 as v35  # noqa: E402
import ib435_measure as m435  # noqa: E402

FUNDS = {"31635V679": "FLCOX", "552985863": "MFEIX", "149498107": "CEMIX", "316146315": "FSGGX", "315911743": "FSMAX", "316146356": "FXNAX",
         "31635V729": "FSPGX", "13161T401": "CDSIX", "30254T643": "FPNIX"}
CONTROL_CUSIP = "922908769"
CONTROL_TICKER = "VTI"
EXPECTED_CASH = {"present": 76796, "UNGRADEABLE": 43310, "ACCT_PRIOR_DATE": 55, "ACCT_OWN_DATE": 19832, "NOTHING_TO_GRADE": 13599}


def main():
    cache, out, tout = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    root = HERE.parents[6]
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

    graded, prev_of, landing = [], {}, {}
    tally_pre, tally_cash = collections.Counter(), collections.Counter()
    claims_pre = collections.defaultdict(dict)
    claims_cash = collections.defaultdict(dict)
    ad = {}                                   # (account digest, day) -> dict(rows=[(cusip, price)], c1=dict, kinds=[...], sixth=bool)
    idents = collections.defaultdict(collections.Counter)
    names = collections.defaultdict(collections.Counter)
    carried_pre = collections.defaultdict(set)    # cusip -> {(account, day)}  pre-cash-rule OUTSIDE_ANCHOR rows
    fund_day_rows = collections.defaultdict(list)
    ctl_anchor = {}
    row_counts = collections.Counter()
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
        ctl_anchor[d] = None if A is None else A.get(CONTROL_CUSIP)
        sp = load("src", p)
        pidx = m435.prior_index(sp if sp not in (None, "UNREAD") else None)
        types = v35.typed_rows(s["CUSIP"], s["Market Value"], s["Units"], s["Cash Equivalent"], A, B)
        accts = s["AccountID"]
        priced = old.price_rows(s["CUSIP"], s["Market Value"], s["Units"])
        outcomes = collections.defaultdict(list)
        out_rows = collections.defaultdict(list)       # account -> [(cusip, price)]  outside_anchor (pre-cash)
        cash_rows = collections.defaultdict(list)      # account -> [(cusip, price, outcome)]
        sixth_acct = set()
        for k, t in enumerate(types):
            a = accts[k]
            if k in priced and priced[k][0] in FUNDS:
                fund_day_rows[(FUNDS[priced[k][0]], d)].append(priced[k][1])
            if t in ("outside_anchor", "cash_priced_outside_anchor"):
                c = priced[k][0]
                tk = {str(x).strip() for x in (s["Ticker"][k], s["Symbol"][k]) if x not in (None, "") and str(x).strip() and str(x).strip().lower() != "none"}
                for x in tk:
                    idents[c][x] += 1
                nm = s["Asset Name"][k]
                if nm not in (None, ""):
                    names[c][str(nm).strip()] += 1
            if t == "outside_anchor":
                out_rows[a].append(priced[k])
                carried_pre[priced[k][0]].add((a, d))
            elif t == "cash_priced_outside_anchor":
                c, price = priced[k]
                o = m435.cash_outcome(a, c, price, pidx)
                outcomes[a].append(o)
                cash_rows[a].append((c, price, o))
            elif t == "no_price":
                mn = old.num(s["Market Value"][k])
                if mn is not None and mn != 0:
                    sixth_acct.add(a)
        rec = old.account_day_records(accts, types)
        for a, c in rec.items():
            pre, _kinds = v35.claim_v035(c)
            claims_pre[a][d] = pre
            tally_pre["present"] += 1
            tally_pre[pre] += 1
            c1 = m435.reclassify(c, outcomes.get(a, []))
            cl1, k1 = v35.claim_v035(c1)
            claims_cash[a][d] = cl1
            tally_cash["present"] += 1
            tally_cash[cl1] += 1
            rows_cash = list(out_rows.get(a, [])) + [(cu, pr) for cu, pr, o in cash_rows.get(a, []) if o != "equal"]
            if rows_cash:
                ad[(a, d)] = {"rows": rows_cash, "c1": dict(c1), "kinds": k1, "sixth": a in sixth_acct, "claim": cl1}
                row_counts["rows"] += len(rows_cash)
    same_pre = {k: tally_pre[k] for k in m435.EXPECTED_V035} == m435.EXPECTED_V035
    same_cash = {k: tally_cash[k] for k in EXPECTED_CASH} == EXPECTED_CASH
    sv_cash = v35.serve_v035(claims_cash, graded)

    # securities behind an OUTSIDE_ANCHOR row under the cash rule
    carried = collections.defaultdict(set)
    for (a, d), r in ad.items():
        for cu, _pr in r["rows"]:
            carried[cu].add((a, d))
    secs = {}
    for c, v in carried.items():
        tks = [k for k, _ in sorted(idents[c].items(), key=lambda kv: (-kv[1], kv[0]))]
        nm = (names[c].most_common(1) or [("", 0)])[0][0]
        secs[c] = {"tickers": tks, "name": nm, "account_days": len(v), "in_pre_cash": c in carried_pre}
    doc = {"graded": graded, "prev_of": prev_of, "landing": landing, "tally_pre": dict(tally_pre), "tally_cash": dict(tally_cash),
           "same_pre": same_pre, "same_cash": same_cash, "claims_cash": {a: dict(v) for a, v in claims_cash.items()}, "ad": ad,
           "secs": secs, "fund_day_rows": dict(fund_day_rows), "ctl_anchor": ctl_anchor, "serve_cash": {"eligible": sv_cash["eligible"], "served": sv_cash["served"],
           "blank": sv_cash["blank"], "never": sum(1 for e, s_ in sv_cash["per_account"].values() if e and s_ == 0)},
           "pre_cash_securities": len(carried_pre), "pre_cash_account_days": len({k for v in carried_pre.values() for k in v})}
    pickle.dump(doc, open(out, "wb"))

    def is_cusip_as_ticker(c, tk):
        return tk.strip().upper() == c.strip().upper()
    asked = {}
    for c, r in secs.items():
        real = [t for t in r["tickers"] if not is_cusip_as_ticker(c, t)]
        if real:
            asked.setdefault(real[0], []).append(c)
    json.dump({"tickers": sorted(asked), "control": CONTROL_TICKER}, open(tout, "w"))
    print("graded", len(graded), "same_pre", same_pre, "same_cash", same_cash, doc["tally_cash"], "securities", len(secs), "pre-cash", len(carried_pre),
          "account-days with an outside row", len(ad), "pre-cash", doc["pre_cash_account_days"], "distinct tickers to ask", len(asked), "serve", doc["serve_cash"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
