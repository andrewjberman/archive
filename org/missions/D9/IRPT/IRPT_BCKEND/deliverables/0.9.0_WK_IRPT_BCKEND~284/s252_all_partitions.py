#!/usr/bin/env python3
"""IB-pr-425: row S252 measured on EVERY trading-day partition of the blackdiamond_z09 holdings source, graded against the Schwab
own-date anchor.  Copied from and extending org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_P/partition_close_anchor_sweep.py
(the originals are untouched).  Read-only; the S3 reads were done by s252_fetch.py into a cache OUTSIDE the repo.

    python -I s252_all_partitions.py <cache_dir> <src_dates.json> <out.json>     measure and write the output
    python -I s252_all_partitions.py --control                                    run only the planted control and print it

WHAT IS COPIED FROM THE EXISTING INSTRUMENT, UNCHANGED
  * price of a source row = Market Value / Units, rows with Units > 0 and Market Value > 0 and a CUSIP only (PRD v0.19 ruling 4);
  * the anchor is the Schwab silver closing_price by CUSIP (an own-date close);
  * a security MOVED on D when anchor close(D) differs from anchor close(prior trading day) by more than the tolerance;
  * TOLERANCE: same(a, b) <= 1e-4 relative, i.e. abs(a-b) <= 1e-4 * max(abs(a), abs(b), 1e-9);
  * trading days come from lib/trading_calendar.py.

WHAT IS EXTENDED
  * the existing instrument keeps ONE price per CUSIP (the last row read wins).  A CUSIP is held in many accounts and 9 of 1,151
    CUSIPs on 2026-09-24 carry more than one distinct row price, so "last wins" makes the answer depend on row order.  Here a
    security-day is decided from ALL its priced rows, by a fixed precedence:
        prior_close  if ANY priced row of the security is at the prior trading day's anchor close,
        else own_close  if ANY row is at D's anchor close,
        else neither.
    own_close + prior_close + neither == moved by construction.  Also reported per day, because the precedence is a choice:
    prior_close_every_row (securities whose EVERY priced row is at the prior close: the lower bound), mixed_own_and_prior
    (securities with rows at both), rows_prior and rows_priced_moved.
  * per-security accumulation: days_lagged (days the security is in prior_close), days_moved, days_lagged_every_row.
  * a diagnostic for "neither" securities (two-back close, or a small gap to the own close).
  * a planted-fixture control that runs the same grade_day / accumulate path.
"""
from __future__ import annotations

import collections
import datetime as dt
import json
import pickle
import re
import statistics
import sys
from pathlib import Path

TOL = 1e-4


def same(a, b):
    return abs(a - b) <= TOL * max(abs(a), abs(b), 1e-9)


# ---------------------------------------------------------------------------- the instrument (pure functions: tested by the control)

def price_rows(cusips, mvs, units):
    """{cusip: [row prices]} -- the existing instrument's row filter, but every row kept."""
    out = collections.defaultdict(list)
    for c, mv, u in zip(cusips, mvs, units):
        try:
            mv, u = float(mv), float(u)
        except (TypeError, ValueError):
            continue
        if c and c.strip() and u > 0 and mv > 0:
            out[c.strip()].append(mv / u)
    return out


def grade_day(rows, own, prev, back):
    """rows {cusip: [prices]}; own/prev/back {cusip: anchor close} on D, P, PP.
    Returns (counts, per-security dict {cusip: (state, n_rows, n_prior_rows)}, neither list of diagnostics)."""
    per = {}
    neither_diag = []
    for k, prices in rows.items():
        if k not in own or k not in prev or same(own[k], prev[k]):
            continue  # not priced in the anchor on both days, or did not move: cannot tell an own close from a prior one
        n_own = sum(1 for x in prices if same(x, own[k]))
        n_prior = sum(1 for x in prices if same(x, prev[k]))
        if n_prior:
            state = "prior"
        elif n_own:
            state = "own"
        else:
            state = "neither"
            gaps = [abs(x - own[k]) / own[k] for x in prices]
            neither_diag.append({
                "security": k, "rows": len(prices),
                "two_back": bool(k in back and any(same(x, back[k]) for x in prices)),
                "min_rel_gap_to_own": min(gaps)})
        per[k] = (state, len(prices), n_prior, n_own)
    c = collections.Counter(v[0] for v in per.values())
    counts = {
        "moved": len(per), "own_close": c["own"], "prior_close": c["prior"], "neither": c["neither"],
        "prior_close_every_row": sum(1 for v in per.values() if v[0] == "prior" and v[2] == v[1]),
        "mixed_own_and_prior": sum(1 for v in per.values() if v[0] == "prior" and v[3] > 0),
        "rows_priced_moved": sum(v[1] for v in per.values()),
        "rows_prior": sum(v[2] for v in per.values()),
    }
    return counts, per, neither_diag


def accumulate(day_pers):
    """day_pers: iterable of per-security dicts from grade_day for the GRADED days -> {cusip: [days_lagged, days_moved, every_row]}."""
    acc = collections.defaultdict(lambda: [0, 0, 0])
    for per in day_pers:
        for k, (state, n, n_prior, n_own) in per.items():
            acc[k][1] += 1
            if state == "prior":
                acc[k][0] += 1
                if n_prior == n:
                    acc[k][2] += 1
    return {k: v for k, v in acc.items() if v[0]}


# ---------------------------------------------------------------------------- class of a security, from the fields the source carries

_MF = re.compile(r"^[A-Z]{4}X$")
_BOND = re.compile(r"\b(BOND|BONDS|NOTE|NOTES|TREAS|TREASURY|BILL|BILLS|DEBENTURE|MUNI|MUNICIPAL|CD)\b|\d+(\.\d+)?%|\bDUE\b", re.I)
_ETF = re.compile(r"\b(ETF|ETN|ETP)\b|\bTRUST SERIES\b|\bSPDR GOLD\b|\bISHARES\b", re.I)
_EQ = re.compile(r"\b(COM|CL [A-Z]|CAP STK|ORD|ADR|SHS|INC|CORP|CO|LTD|PLC|HLDGS|HOLDINGS|SUB VTG|N V|S A|LP|NEW)\b", re.I)


def classify(symbol, name, cash_any, er_any):
    """fund | ETF | equity | bond | cash | other, from Cash Equivalent, Expense Ratio, Symbol and Asset Name (the source names no class)."""
    sym, nm = (symbol or "").strip().upper(), (name or "")
    if cash_any:
        return "cash"
    if _ETF.search(nm):
        return "ETF"
    if er_any:
        return "fund" if _MF.match(sym) else "ETF"
    if _BOND.search(nm):
        return "bond"
    if _EQ.search(nm):
        return "equity"
    return "other"


# ---------------------------------------------------------------------------- the planted control

def control():
    """A synthetic fixture: 3 trading days D1 < D2 < D3 (dates are labels only), 8 securities, ONE planted lagged security
    (lagged on D2 and D3, own on D1).  The clean copy is the same fixture with the planted security at its own close every day.
    Decoys that must NOT be reported: a security that did not move (own == prior), a security at neither close, and a security
    present in the source but absent from the anchor."""
    anchors = {  # day -> {cusip: close}
        "D0": {"S1": 10.0, "S2": 20.0, "S3": 30.0, "S4": 40.0, "S5": 50.0, "S6": 60.0, "PLANT0001": 100.0},
        "D1": {"S1": 11.0, "S2": 21.0, "S3": 31.0, "S4": 41.0, "S5": 50.0, "S6": 61.0, "PLANT0001": 101.0},
        "D2": {"S1": 12.0, "S2": 22.0, "S3": 32.0, "S4": 42.0, "S5": 50.0, "S6": 62.0, "PLANT0001": 102.0},
        "D3": {"S1": 13.0, "S2": 23.0, "S3": 33.0, "S4": 43.0, "S5": 50.0, "S6": 63.0, "PLANT0001": 103.0},
    }
    prev_of = {"D1": "D0", "D2": "D1", "D3": "D2"}

    def source(day, lagged_security):
        a, p = anchors[day], anchors[prev_of[day]]
        rows = {k: [a[k]] for k in a}                       # every security at D's own close ...
        rows["S4"] = [a["S4"] * 1.07]                        # ... except a decoy at neither close
        rows["NOANCHOR"] = [5.0]                             # a decoy the anchor does not carry
        if lagged_security and day in lagged_security:
            rows["PLANT0001"] = [p["PLANT0001"]]            # the planted one, at the PRIOR close
        return rows

    def run(lag_days):
        pers = []
        for d in ("D1", "D2", "D3"):
            c, per, _ = grade_day(source(d, lag_days), anchors[d], anchors[prev_of[d]], anchors.get(prev_of.get(prev_of[d], ""), {}))
            assert c["own_close"] + c["prior_close"] + c["neither"] == c["moved"]
            pers.append(per)
        return sorted(accumulate(pers))

    reported = run({"D2", "D3"})
    clean = run(set())
    return {"planted": "PLANT0001", "reported": reported, "clean_fixture_reported": clean,
            "fixture": "3 trading days, 7 anchor securities + 1 source-only decoy; PLANT0001 lagged on D2 and D3; decoys: S5 did not move, "
                       "S4 at neither close, NOANCHOR absent from the anchor"}


# ---------------------------------------------------------------------------- the measurement

def main():
    if sys.argv[1:] == ["--control"]:
        print(json.dumps(control(), indent=1))
        return 0
    cache, srcdates, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    root = Path(__file__).resolve().parents[7]
    sys.path[:0] = [str(root / "lib"), str(root), str(root / "data/assets/scripts/gold/irpt_holdings_performance")]
    import trading_calendar as tc
    import holdings_performance as hp
    decl = json.load(open(root / "data/assets/scripts/gold/irpt_holdings_performance/sources.json", encoding="utf-8"))
    src = decl["blackdiamond_z09"]
    prefix_resolved = hp.resolved_prefix(src, "positions_prefix", hp.firm_scope(src))
    anchor_prefix = decl["schwab_08335338"]["positions_prefix"]

    listed = json.load(open(srcdates, encoding="utf-8"))
    tdays = [d for d in listed if tc.is_trading_day(d)]
    non_trading = [d for d in listed if d not in tdays]
    expected = [d.isoformat() for d in tc.trading_days_between(listed[0], listed[-1])]
    missing = [d for d in expected if d not in listed]

    def load(kind, day):
        f = cache / ("%s_%s.pkl" % (kind, day))
        return pickle.load(open(f, "rb")) if f.exists() else "UNREAD"

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

    days, pers, meta = [], [], {}
    lag_dates = collections.defaultdict(list)
    neither_two_back = neither_small_gap = neither_total = 0
    neither_secs = collections.Counter()
    for i, d in enumerate(tdays):
        row = {"date": d, "state": None, "reason": "", "moved": None, "own_close": None, "prior_close": None, "neither": None}
        dd = dt.date.fromisoformat(d)
        p = tc.prev_trading_day(dd).isoformat()
        pp = tc.prev_trading_day(dt.date.fromisoformat(p)).isoformat()
        s = load("src", d)
        A, B, PP = anchor(d), anchor(p), anchor(pp)
        if s in (None, "UNREAD"):
            row.update(state="UNGRADEABLE", reason="source partition %s" % ("empty or absent" if s is None else "not read into the cache"))
        elif A in (None, "UNREAD") or B in (None, "UNREAD"):
            row.update(state="UNGRADEABLE", reason="anchor partition missing for %s" % (d if A in (None, "UNREAD") else p))
        else:
            rows = price_rows(s["CUSIP"], s["Market Value"], s["Units"])
            for c, sy, nm, ce, er in zip(s["CUSIP"], s["Symbol"], s["Asset Name"], s["Cash Equivalent"], s["Expense Ratio"]):
                if c and c.strip():
                    m = meta.setdefault(c.strip(), [sy, nm, False, False])
                    m[2] = m[2] or str(ce).strip().lower() == "true"
                    m[3] = m[3] or er is not None
            counts, per, nd = grade_day(rows, A, B, PP if PP not in (None, "UNREAD") else {})
            if i == 0 or tdays[i - 1] != p:
                # no prior trading-day partition in the source: the face's FIRST_DAY_NO_PRIOR (counts shown in the reason, not in the totals)
                row.update(state="FIRST_DAY_NO_PRIOR", reason=(
                    "no source partition for the prior trading day %s; for information only (not in the totals): moved %d, own %d, "
                    "prior %d, neither %d" % (p, counts["moved"], counts["own_close"], counts["prior_close"], counts["neither"])))
            else:
                row.update(state="GRADED", **counts)
                pers.append(per)
                for k, v in per.items():
                    if v[0] == "prior":
                        lag_dates[k].append(d)
                for x in nd:
                    neither_total += 1
                    neither_two_back += x["two_back"]
                    neither_small_gap += (not x["two_back"]) and x["min_rel_gap_to_own"] <= 0.005
                    neither_secs[x["security"]] += 1
        days.append(row)

    acc = accumulate(pers)
    lag = []
    for k, (n_lag, n_mov, n_every) in acc.items():
        sy, nm, ce, er = meta.get(k, ["", "", False, False])
        lag.append({"security": k, "class": classify(sy, nm, ce, er), "days_lagged": n_lag, "days_moved": n_mov,
                    "days_lagged_every_row": n_every, "first_lagged": min(lag_dates[k]), "last_lagged": max(lag_dates[k]), "symbol": sy, "name": (nm or "").encode("ascii", "replace").decode().replace("?", " ").strip()})
    lag.sort(key=lambda r: (-r["days_lagged"], r["security"]))
    by_class = dict(sorted(collections.Counter(r["class"] for r in lag).items()))
    graded = [d for d in days if d["state"] == "GRADED"]
    shares = [100.0 * d["prior_close"] / d["moved"] for d in graded if d["moved"]]
    strict = [100.0 * d["prior_close_every_row"] / d["moved"] for d in graded if d["moved"]]
    neither_class = collections.Counter(classify(*meta.get(k, ["", "", False, False])[:2], meta.get(k, ["", "", False, False])[2], meta.get(k, ["", "", False, False])[3]) for k in neither_secs)

    doc = {
        "source": {"bucket": src["bucket"], "prefix_template": src["positions_prefix"] + "date=YYYY-MM-DD/",
                   "prefix_resolved_by": "holdings_performance.resolved_prefix(blackdiamond_z09, positions_prefix, firm_scope) -> %d characters, same as the gold script" % len(prefix_resolved),
                   "anchor": "%s%s (closing_price by cusip; the Schwab own-date close)" % (anchor_prefix, "date=YYYY-MM-DD/"),
                   "price": "Market Value / Units, rows with Units > 0 and Market Value > 0 and a CUSIP; every row kept",
                   "security_key": "CUSIP (rows without a CUSIP are not graded: the existing instrument's join key)"},
        "tolerance": {"kind": "relative", "value": TOL, "rule": "abs(a-b) <= 1e-4 * max(abs(a), abs(b), 1e-9)", "taken_from": "partition_close_anchor_sweep.py same()"},
        "security_day_rule": "prior_close if ANY priced row of the security is at the prior trading day's anchor close, else own_close if any row is at the day's anchor close, else neither",
        "partitions_listed": len(listed),
        "trading_day_partitions_listed": len(tdays),
        "non_trading_dates_listed": non_trading,
        "trading_days_in_range_missing_from_prefix": missing,
        "range": [listed[0], listed[-1]],
        "calendar": tc.calendar_source(),
        "days": days,
        "lagged_securities": lag,
        "lagged_by_class": by_class,
        "summary": {
            "graded_days": len(graded),
            "share_prior_close_pct": {"min": round(min(shares), 3), "median": round(statistics.median(shares), 3), "max": round(max(shares), 3),
                                      "days_above_1pct": sum(1 for x in shares if x > 1.0)},
            "share_prior_close_every_row_pct": {"min": round(min(strict), 3), "median": round(statistics.median(strict), 3), "max": round(max(strict), 3),
                                                "days_above_1pct": sum(1 for x in strict if x > 1.0)},
            "lagged_security_days": sum(d["prior_close"] for d in graded),
            "lagged_securities": len(lag),
            "lagged_every_row_security_days": sum(d["prior_close_every_row"] for d in graded),
            "securities_with_any_lag_every_row": sum(1 for r in lag if r["days_lagged_every_row"]),
            "stability": {
                "securities_lagged_10_or_more_days": sum(1 for r in lag if r["days_lagged"] >= 10),
                "classes_of_those": dict(sorted(collections.Counter(r["class"] for r in lag if r["days_lagged"] >= 10).items())),
                "securities_lagged_under_10_days": sum(1 for r in lag if r["days_lagged"] < 10),
                "securities_lagged_on_half_or_more_of_their_moved_days": sum(1 for r in lag if 2 * r["days_lagged"] >= r["days_moved"]),
                "four_days_with_most_prior_close": [[d["date"], d["prior_close"], d["moved"]] for d in sorted(graded, key=lambda x: -x["prior_close"])[:4]],
                "lagged_security_days_on_those_four": sum(sorted((d["prior_close"] for d in graded), reverse=True)[:4]),
                "days_with_zero_prior_close": sum(1 for d in graded if d["prior_close"] == 0),
            },
            "neither": {"security_days": neither_total, "distinct_securities": len(neither_secs), "equal_two_back_close": neither_two_back,
                        "within_0.5pct_of_own_close_not_two_back": neither_small_gap, "by_class": dict(neither_class),
                        "top_by_days": neither_secs.most_common(8)},
        },
        "control": control(),
    }
    out.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    print("wrote", out, "days", len(days), "graded", len(graded), "lagged securities", len(lag), by_class)
    return 0


if __name__ == "__main__":
    sys.exit(main())
