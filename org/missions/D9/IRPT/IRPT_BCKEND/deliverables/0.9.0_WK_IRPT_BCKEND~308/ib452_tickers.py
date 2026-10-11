#!/usr/bin/env python3
"""IB-pr-452 step: the ONE list of distinct tickers to ask the reader for, counted BEFORE any fetch.

Only the securities OUTSIDE the first witness (behind an OUTSIDE_ANCHOR row under the cash rule) whose type is one of the NINE admitted pairs
(ib442_prepare's prep pickle: sec_cls 'admitted_type' = the seven of PRD v0.39, 'left_out_type_inst', 'left_out_type_ric_not_available') and that have a ticker.
No overlap table, no fund trade: this cell reads neither.  Counts only.

    python -I ib452_tickers.py <prep442.pkl> <tickers.json> <meta.json>
"""
import collections
import json
import pickle
import sys

NINE_CLASSES = ("admitted_type", "left_out_type_inst", "left_out_type_ric_not_available")
FIVE = ["ADLYX", "BISOX", "EIBLX", "GPPIX", "OLCYX"]


def main():
    prep, tk, meta = sys.argv[1:4]
    B = pickle.load(open(prep, "rb"))
    by_cls = collections.defaultdict(set)
    for c, k in B["sec_cls"].items():
        if k in NINE_CLASSES and B["sec_ticker"][c]:
            by_cls[k].add(B["sec_ticker"][c])
    distinct = sorted(set().union(*by_cls.values()))
    json.dump({"tickers": distinct}, open(tk, "w"))
    m = {"securities_outside_the_first_witness": len(B["sec_cls"]),
         "tickers_by_class": {k: len(by_cls[k]) for k in NINE_CLASSES},
         "distinct": len(distinct), "calls_of_at_most_50": -(-len(distinct) // 50), "over_1500": len(distinct) > 1500,
         "the_five_are_among_them": [t for t in FIVE if t in distinct]}
    json.dump(m, open(meta, "w"))
    print(m)
    return 0


if __name__ == "__main__":
    sys.exit(main())
