#!/usr/bin/env python3
"""IB-pr-442 step 2.  From the phase-1 pickle (the securities behind an OUTSIDE_ANCHOR row under the cash rule) and the transactions pickle (ib441_fetch_tx.py):
  (a) the type of each of those securities (the pair SEC Asset Type / Share Class Type the transactions table states for its CUSIP), and its class before any bar is read;
  (b) the priced fund trades inside the 85 graded days and each fund's ticker and type pair (IB-pr-441's rules, copied);
  (c) the ONE list of distinct tickers to ask the reader for: admitted-type securities with a ticker, plus the fund tickers.
Counts only leave this script; the pickle stays outside the repo.

    python -I ib442_prepare.py <phase1.pkl> <tx.pkl> <prep.pkl> <tickers.json>
"""
import collections
import json
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
root = HERE.parents[6]
sys.path[:0] = [str(root / "lib"), str(root)]
import datetime as dt  # noqa: E402

RIC = "Securities Issued by Registered Investment Companies or Business Development Companies"
ETS = "Exchange-Traded Equity Securities"
# the seven admitted pairs of PRD ADDENDUM v0.39 in the source's own strings; each is asserted to occur in the transactions table
ADMITTED = [(ETS, "Not Available"), (RIC, "ETF"), (RIC, "A"), (RIC, "No Load"), (RIC, "Other"), (RIC, "Retirement"), (RIC, "Inv")]
LEFT_INST, LEFT_NA = (RIC, "Inst"), (RIC, "Not Available")
NOT_FUND_CLASSES = ("ETF", "Not Available")


def pair_name(p):
    return "%s / %s" % p


def real_ticker(t, cusip):
    t = None if t is None else str(t).strip()
    if t and t.lower() != "none" and t.upper() != (cusip or "").strip().upper():
        return t
    return None


def iso(s):
    try:
        return dt.datetime.strptime(str(s).strip(), "%m/%d/%Y").date().isoformat()
    except Exception:
        return None


def sec_class(ticker, pairs):
    """The class of one outside-first-witness security BEFORE any bar is read.  Precedence: no ticker; then its type (none or more than one pair; Inst; RIC Not Available;
    another pair not admitted); then admitted (-> no_bar / admitted_type_with_bars once the reader has been asked)."""
    if ticker is None:
        return "no_ticker_to_ask_with", None
    if len(pairs) != 1:
        return "no_type_or_mixed", None
    (p,) = pairs
    if p == LEFT_INST:
        return "left_out_type_inst", p
    if p == LEFT_NA:
        return "left_out_type_ric_not_available", p
    if p in ADMITTED:
        return "admitted_type", p
    return "another_type_not_admitted", p


def main():
    p1p, txp, outp, tkp = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    P1 = pickle.load(open(p1p, "rb"))
    secs, graded = P1["secs"], P1["graded"]
    T = pickle.load(open(txp, "rb"))
    rows = T["rows"]
    present = collections.Counter((r["SEC Asset Type"], r["Share Class Type"]) for r in rows)
    for p in ADMITTED + [LEFT_INST, LEFT_NA]:
        assert present[p] > 0, "pair not found exactly as the source writes it: %r" % (p,)
    # --- the type of each security (all de-duplicated transaction rows of its CUSIP, any kind, any date)
    pairs_of = collections.defaultdict(set)
    for r in rows:
        c = (r["CUSIP"] or "").strip()
        if c in secs:
            pairs_of[c].add((r["SEC Asset Type"] or "<blank>", r["Share Class Type"] or "<blank>"))
    sec_ticker, sec_cls, sec_pair = {}, {}, {}
    for c, r in secs.items():
        real = [t for t in r["tickers"] if t.strip().upper() != c.strip().upper()]
        sec_ticker[c] = real[0] if real else None          # IB-pr-438's rule: the most frequent identifier the source states, not the CUSIP itself
        sec_cls[c], sec_pair[c] = sec_class(sec_ticker[c], pairs_of.get(c, set()))
    join = collections.Counter("found_no_row" if not pairs_of.get(c) else ("found_one_pair" if len(pairs_of[c]) == 1 else "found_more_than_one_pair") for c in secs)
    join_t = collections.Counter("found_no_row" if not pairs_of.get(c) else ("found_one_pair" if len(pairs_of[c]) == 1 else "found_more_than_one_pair") for c in secs if sec_ticker[c])
    other_pairs = collections.Counter(pair_name(sec_pair[c]) for c in secs if sec_cls[c] == "another_type_not_admitted")
    mixed_combos = collections.Counter(" + ".join(sorted(pair_name(p) for p in pairs_of[c])) for c in secs if sec_cls[c] == "no_type_or_mixed" and len(pairs_of.get(c, ())) > 1)
    # --- the priced fund trades (IB-pr-441's recognition rule, copied) inside the graded days
    trades, tick_by_cusip, pairs_all = [], collections.defaultdict(collections.Counter), collections.defaultdict(set)
    for r in rows:
        c = (r["CUSIP"] or "").strip()
        if c:
            pairs_all[c].add((r["SEC Asset Type"] or "<blank>", r["Share Class Type"] or "<blank>"))
    for r in rows:
        c = (r["CUSIP"] or "").strip()
        sa, sc = r["SEC Asset Type"], r["Share Class Type"]
        pr = r["Price"]
        if r["Transaction Type"] in ("Buy", "Sale") and pr is not None and pr == pr and pr > 0 and c and sa == RIC and sc not in NOT_FUND_CLASSES:
            tk = real_ticker(r["Ticker"], c) or real_ticker(r["Symbol"], c)
            if tk:
                tick_by_cusip[c][tk] += 1
            trades.append({"id": r["TransactionID"], "cusip": c, "ticker": None, "price": float(pr), "trade": iso(r["Trade Date"]), "kind": r["Transaction Type"], "sub": r["Transaction Sub Type"]})
    fund_ticker = {c: v.most_common(1)[0][0] for c, v in tick_by_cusip.items()}
    for t in trades:
        t["ticker"] = fund_ticker.get(t["cusip"])
    gset = set(graded)
    inside = [t for t in trades if t["trade"] in gset]
    fund_pair = {}
    for c in {t["cusip"] for t in inside}:
        ps = pairs_all[c]
        fund_pair[c] = pair_name(next(iter(ps))) if len(ps) == 1 else "MIXED"
    fund_tickers = sorted({t["ticker"] for t in inside if t["ticker"]})
    sec_tickers = sorted({sec_ticker[c] for c in secs if sec_cls[c] == "admitted_type"})
    distinct = sorted(set(sec_tickers) | set(fund_tickers))
    pickle.dump({"sec_ticker": sec_ticker, "sec_cls": sec_cls, "sec_pair": {c: (None if p is None else pair_name(p)) for c, p in sec_pair.items()}, "join": dict(join), "join_with_ticker": dict(join_t),
                 "other_pairs": dict(other_pairs), "mixed_combos": dict(mixed_combos), "trades": trades, "inside": inside, "fund_pair": fund_pair, "fund_ticker": fund_ticker,
                 "admitted": [pair_name(p) for p in ADMITTED], "tx_meta": {k: T[k] for k in ("partitions", "objects", "rows_read", "absent_cols")}, "tx_distinct_ids": len(rows)}, open(outp, "wb"))
    json.dump({"tickers": distinct}, open(tkp, "w"))
    cc = collections.Counter(sec_cls.values())
    print("securities", len(secs), "classes before any bar:", dict(cc))
    print("type join (all securities):", dict(join), " (with a ticker):", dict(join_t))
    print("other pairs not admitted:", dict(other_pairs))
    print("admitted-type securities with a ticker", cc["admitted_type"], "-> distinct tickers", len(sec_tickers))
    print("fund trades all dates", len(trades), "inside 85d", len(inside), "funds inside", len({t["cusip"] for t in inside}), "fund tickers", len(fund_tickers), "inside trades without ticker", sum(1 for t in inside if not t["ticker"]))
    print("overlap of the two ticker lists", len(set(sec_tickers) & set(fund_tickers)))
    print("DISTINCT TICKERS TO ASK", len(distinct), "calls of <=50:", -(-len(distinct) // 50))


if __name__ == "__main__":
    main()
