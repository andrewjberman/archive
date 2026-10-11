#!/usr/bin/env python3
"""IB-pr-441 step 2: from the cached source / anchor partitions and the transactions pickle, build (a) the securities both witnesses carry, each with its type, and
(b) the priced fund trades; and the distinct tickers to ask Yahoo Finance for, ONE list for both tables.  Counts only leave this script; the pickle stays outside the repo.

    python -I ib441_prepare.py <parts_cache> <tx.pkl> <prep.pkl> <tickers.json>
"""
import collections
import datetime as dt
import json
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
root = HERE.parents[6]
sys.path[:0] = [str(root / "lib"), str(root)]
import trading_calendar as tc  # noqa: E402

FIRST, LAST = "2026-06-10", "2026-10-09"
RIC = "Securities Issued by Registered Investment Companies or Business Development Companies"
NOT_FUND_CLASSES = ("ETF", "Not Available")


def iso(s):
    try:
        return dt.datetime.strptime(str(s).strip(), "%m/%d/%Y").date().isoformat()
    except Exception:
        return None


def real_ticker(t, cusip):
    t = None if t is None else str(t).strip()
    if t and t.lower() != "none" and t.upper() != (cusip or "").strip().upper():
        return t
    return None


def main():
    cache, txp, outp, tkp = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    # trading-day axis: calendar trading days 2026-06-09 .. 2026-10-12 (one before the first graded day, one after the last)
    ax = [d.isoformat() for d in tc.trading_days_between(dt.date(2026, 6, 9), dt.date(2026, 10, 12))]
    graded = [d for d in ax if FIRST <= d <= LAST]

    def load(kind, day):
        f = cache / ("%s_%s.pkl" % (kind, day))
        return pickle.load(open(f, "rb")) if f.exists() else "UNREAD"
    anchor, src_days_missing, anc_days_missing = {}, [], []
    held, tick_of, anc_any = set(), collections.defaultdict(set), set()
    for d in ax:
        a = load("anc", d)
        if a in (None, "UNREAD"):
            anc_days_missing.append(d)
            anchor[d] = {}
        else:
            anchor[d] = {(c or "").strip(): float(p) for c, p in zip(a["cusip"], a["closing_price"]) if (c or "").strip() and p is not None and float(p) > 0}
        if d in graded:
            s = load("src", d)
            if s in (None, "UNREAD"):
                src_days_missing.append(d)
                continue
            for c, t1, t2 in zip(s["CUSIP"], s["Ticker"], s["Symbol"]):
                c = (c or "").strip()
                if not c:
                    continue
                held.add(c)
                for x in (t1, t2):
                    r = real_ticker(x, c)
                    if r:
                        tick_of[c].add(r)
            anc_any |= set(anchor[d])
    both = {c for c in held if c in anc_any}
    both_t = {c for c in both if tick_of.get(c)}
    sec_ticker = {c: sorted(tick_of[c])[0] for c in both_t}

    # ---- transactions: the type of each security, the priced fund trades
    T = pickle.load(open(txp, "rb"))
    rows = T["rows"]
    types_of = collections.defaultdict(collections.Counter)
    for r in rows:
        c = (r["CUSIP"] or "").strip()
        if c in both_t:
            types_of[c][(r["SEC Asset Type"] or "<blank>", r["Share Class Type"] or "<blank>")] += 1
    trades, tick_by_cusip = [], collections.defaultdict(collections.Counter)
    for r in rows:
        c = (r["CUSIP"] or "").strip()
        sa, sc = r["SEC Asset Type"], r["Share Class Type"]
        pr = r["Price"]
        if r["Transaction Type"] in ("Buy", "Sale") and pr is not None and pr == pr and pr > 0 and c and sa == RIC and sc not in NOT_FUND_CLASSES:
            tk = real_ticker(r["Ticker"], c) or real_ticker(r["Symbol"], c)
            if tk:
                tick_by_cusip[c][tk] += 1
            trades.append({"id": r["TransactionID"], "cusip": c, "ticker": tk, "price": float(pr), "trade": iso(r["Trade Date"]), "settle": iso(r["Settle Date"]),
                           "type": r["Transaction Type"], "sub": r["Transaction Sub Type"]})
    fund_ticker = {c: v.most_common(1)[0][0] for c, v in tick_by_cusip.items()}
    for t in trades:
        t["ticker"] = fund_ticker.get(t["cusip"])
    # the trades this cell compares: trade date inside the 85 graded days (the reader's window is fixed at 2026-06-05..2026-10-13)
    inside = [t for t in trades if t["trade"] in set(graded)]
    inside_ticker = {t["ticker"] for t in inside if t["ticker"]}
    sec_tickers = set(sec_ticker.values())
    distinct = sorted(sec_tickers | inside_ticker)
    P = {"axis": ax, "graded": graded, "anchor": anchor, "sec_ticker": sec_ticker, "types_of": {c: dict(v) for c, v in types_of.items()}, "trades": trades,
         "inside": inside, "src_days_missing": src_days_missing, "anc_days_missing": anc_days_missing, "held": len(held), "both": len(both), "both_t": len(both_t),
         "tx_meta": {k: T[k] for k in ("partitions", "objects", "rows_read", "absent_cols")}, "tx_distinct_ids": len(rows)}
    pickle.dump(P, open(outp, "wb"))
    json.dump({"tickers": distinct}, open(tkp, "w"))
    print("axis", len(ax), "graded", len(graded), "missing src", src_days_missing, "missing anc", anc_days_missing)
    print("held", len(held), "both", len(both), "both with ticker", len(both_t), "distinct sec tickers", len(sec_tickers))
    print("fund trades (all dates)", len(trades), "inside 85d", len(inside), "fund tickers inside", len(inside_ticker), "overlap with sec tickers", len(sec_tickers & inside_ticker))
    print("distinct to ask", len(distinct), "over 1500:", len(distinct) > 1500)
    print("funds (cusip) inside", len({t["cusip"] for t in inside}), "no ticker trades", sum(1 for t in inside if not t["ticker"]), "fund-dates inside", len({(t["cusip"], t["trade"]) for t in inside}), "fund-dates all", len({(t["cusip"], t["trade"]) for t in trades}))


if __name__ == "__main__":
    main()
