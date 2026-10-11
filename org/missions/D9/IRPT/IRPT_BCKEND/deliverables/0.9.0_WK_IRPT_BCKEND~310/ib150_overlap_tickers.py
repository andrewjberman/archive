#!/usr/bin/env python3
"""IB-pr-454 step: the securities BOTH witnesses carry (held on one or more of the 85 graded days, carried by the anchor with a positive close on one or more of
them, with a ticker that is not the CUSIP itself: IB-pr-439's definition, which counted 894), their types from the transactions table, and the ONE list of distinct
tickers to ask the reader for: the 303 of IB-pr-452 (outside the first witness, nine pairs) plus the overlap securities of the nine pairs.  Counted BEFORE any fetch.
Read only; counts only leave this script; the lists stay outside the repo.

    python -I ib150_overlap_tickers.py <partition_cache> <phase1.pkl> <prep.pkl> <tx.pkl> <tickers_452.json> <out_tickers.json> <out_overlap.pkl> <meta.json>
"""
import collections
import json
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
sys.path[:0] = [str(ROOT / "lib"), str(ROOT), str(ROOT / "data/assets/scripts/gold/irpt_reporting")]
import date_basis_grading as m  # noqa: E402


def main():
    cache, p1f, prepf, txf, t452f, out_t, out_o, meta_f = sys.argv[1:9]
    cache = Path(cache)
    P1 = pickle.load(open(p1f, "rb"))
    graded = P1["graded"]
    held_idents = collections.defaultdict(collections.Counter)
    carried = set()
    for d in graded:
        s = pickle.load(open(cache / ("src_%s.pkl" % d), "rb"))
        a = pickle.load(open(cache / ("anc_%s.pkl" % d), "rb"))
        for c, tk, sy in zip(s["CUSIP"], s["Ticker"], s["Symbol"]):
            c = (c or "").strip()
            if not c:
                continue
            held_idents[c]["__held__"] += 1
            for x in (tk, sy):
                x = None if x is None else str(x).strip()
                if x and x.lower() != "none" and x.upper() != c.upper():
                    held_idents[c][x] += 1
        if a is not None:
            for c, p in zip(a["cusip"], a["closing_price"]):
                c = (c or "").strip()
                if c and p is not None and float(p) > 0:
                    carried.add(c)
    T = pickle.load(open(txf, "rb"))
    pairs_of = collections.defaultdict(set)
    for r in T["rows"]:
        c = (r["CUSIP"] or "").strip()
        if c:
            pairs_of[c].add((r["SEC Asset Type"] or "<blank>", r["Share Class Type"] or "<blank>"))
    overlap = {}
    for c in carried & set(held_idents):
        real = [(k, n) for k, n in held_idents[c].items() if k != "__held__"]
        if not real:
            continue
        tk = sorted(real, key=lambda kv: (-kv[1], kv[0]))[0][0]
        overlap[c] = {"ticker": tk, "pairs": sorted(pairs_of.get(c, set()))}
    adm = {c: v for c, v in overlap.items() if m.second_witness_admits(v["pairs"])}
    t452 = list(json.load(open(t452f))["tickers"])
    combined = sorted(set(t452) | {v["ticker"] for v in adm.values()})
    meta = {"held_on_the_85_days": len(held_idents), "carried_by_the_anchor": len(carried & set(held_idents)), "overlap_with_a_ticker": len(overlap),
            "overlap_of_the_nine_pairs": len(adm), "overlap_of_the_nine_pairs_distinct_tickers": len({v["ticker"] for v in adm.values()}),
            "tickers_of_ib_pr_452": len(t452), "in_both_lists": len(set(t452) & {v["ticker"] for v in adm.values()}),
            "distinct_tickers_to_ask": len(combined), "calls_of_at_most_50": -(-len(combined) // 50), "over_1500": len(combined) > 1500}
    json.dump({"tickers": combined}, open(out_t, "w"))
    pickle.dump({"overlap_nine": adm, "overlap_all": overlap}, open(out_o, "wb"))
    json.dump(meta, open(meta_f, "w"))
    print(meta)


if __name__ == "__main__":
    main()
