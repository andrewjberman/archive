#!/usr/bin/env python3
"""IB-pr-445 step: the ONE list of distinct tickers to ask the reader for, counted BEFORE any fetch.

  (a) the first ticker of each security BOTH witnesses carry (ib441_prepare's prep pickle: sec_ticker);
  (b) the ticker of each security OUTSIDE the first witness whose type is one of the seven admitted pairs, or the institutional pair
      (ib442_prepare's prep pickle: sec_cls 'admitted_type' / 'left_out_type_inst').
No fund-trade list: this cell reads no trade.  Counts only.

    python -I ib445_tickers.py <prep441.pkl> <prep442.pkl> <tickers.json> <meta.json>
"""
import json
import pickle
import sys


def main():
    p441, p442, tk, meta = sys.argv[1:5]
    A = pickle.load(open(p441, "rb"))
    B = pickle.load(open(p442, "rb"))
    overlap = set(A["sec_ticker"].values())
    adm = {B["sec_ticker"][c] for c, k in B["sec_cls"].items() if k == "admitted_type" and B["sec_ticker"][c]}
    inst = {B["sec_ticker"][c] for c, k in B["sec_cls"].items() if k == "left_out_type_inst" and B["sec_ticker"][c]}
    distinct = sorted(overlap | adm | inst)
    json.dump({"tickers": distinct}, open(tk, "w"))
    m = {"overlap_securities": len(A["sec_ticker"]), "overlap_tickers": len(overlap), "outside_admitted_tickers": len(adm), "outside_inst_tickers": len(inst),
         "outside_admitted_also_in_overlap": len(adm & overlap), "outside_inst_also_in_overlap": len(inst & overlap), "distinct": len(distinct),
         "calls_of_at_most_50": -(-len(distinct) // 50), "over_1500": len(distinct) > 1500}
    json.dump(m, open(meta, "w"))
    print(m)
    return 0


if __name__ == "__main__":
    sys.exit(main())
