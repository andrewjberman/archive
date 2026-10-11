#!/usr/bin/env python3
"""IB-pr-443 step 2.  Read only; counts and public-security dated values only.  Gathers, for the five one-day-off security-days of IB-pr-441, the two
witnesses' series, the custodian's mark, the priced trades and the distribution rows of the SAME security, and writes them to <gather.json>
(outside the repo).  No account column, quantity or amount is read into the output: the transactions rows are reduced to (kind, trade date, settle date, price).

    python -I ib443_gather.py <parts_cache> <tx.pkl> <yahoo_cache> <ib441.json> <gather.json>

"""
import collections
import datetime as dt
import json
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
root = HERE.parents[6]
sys.path[:0] = [str(root / "lib"), str(root), str(root / "data/assets/scripts/silver"), str(root / "data/assets/scripts/analysis")]
import trading_calendar as tc  # noqa: E402

CUSIP = {"MEIIX": "552983694", "MISIX": "92647K309", "PZA": "46138E537", "SHM": "78468R739"}
EPOCH = dt.date(1970, 1, 1)
RIC = "Securities Issued by Registered Investment Companies or Business Development Companies"


def iso(s):
    try:
        return dt.datetime.strptime(str(s).strip(), "%m/%d/%Y").date().isoformat()
    except Exception:
        return None


def main():
    parts, txp, ycache, ib441, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]), Path(sys.argv[5])
    import commonwealth_daily_valuation as dv
    five = [(d["ticker"], d["date"], d["type"]) for d in json.load(open(ib441))["one_day_off_detail"]]
    ax = [d.isoformat() for d in tc.trading_days_between(dt.date(2026, 6, 15), dt.date(2026, 10, 9))]
    # ---- the first witness (anchor closing_price by CUSIP) and the custodian's mark, per CUSIP per day
    anchor, mark, anc_rows, meta = collections.defaultdict(dict), collections.defaultdict(dict), collections.defaultdict(dict), {}
    for d in ax:
        a = pickle.load(open(parts / ("anc_%s.pkl" % d), "rb")) if (parts / ("anc_%s.pkl" % d)).exists() else "UNREAD"
        if a not in (None, "UNREAD"):
            meta[d] = a["_meta"]
            by = collections.defaultdict(list)
            for c, p in zip(a["cusip"], a["closing_price"]):
                if (c or "").strip() and p is not None and float(p) > 0:
                    by[c.strip()].append(float(p))
            for c, v in by.items():
                anchor[c][d] = v[-1]                         # IB-pr-441's rule: the last row of the day
                anc_rows[c][d] = len(v), len(set(v))
        s = pickle.load(open(parts / ("src_%s.pkl" % d), "rb")) if (parts / ("src_%s.pkl" % d)).exists() else "UNREAD"
        if s not in (None, "UNREAD"):
            cnt = collections.defaultdict(collections.Counter)
            for c, mv, u in zip(s["CUSIP"], s["Market Value"], s["Units"]):
                try:
                    mv, u = float(mv), float(u)
                except Exception:
                    continue
                if (c or "").strip() and mv > 0 and u > 0:
                    cnt[c.strip()][round(mv / u, 4)] += 1
            for c, k in cnt.items():
                mark[c][d] = {"most_common_mark": k.most_common(1)[0][0], "rows_at_it": k.most_common(1)[0][1], "rows": sum(k.values()), "distinct_marks": len(k)}
    # ---- the second witness
    reader = {}
    for tk in CUSIP:
        s, _ = dv.read_yahoo_close(ycache, tk)
        reader[tk] = None if s is None else {(EPOCH + dt.timedelta(days=int(k))).isoformat(): float(v) for k, v in s.items()}
    # ---- the transactions of the four securities, reduced
    T = pickle.load(open(txp, "rb"))["rows"]
    tx = collections.defaultdict(list)
    for r in T:
        c = (r["CUSIP"] or "").strip()
        if c in CUSIP.values():
            tx[c].append({"kind": r["Transaction Type"], "sub": r["Transaction Sub Type"], "trade": iso(r["Trade Date"]), "settle": iso(r["Settle Date"]),
                          "price": None if r["Price"] is None or r["Price"] != r["Price"] else float(r["Price"])})
    G = {"axis": ax, "five": five, "anchor": {c: anchor[c] for c in CUSIP.values()}, "mark": {c: mark[c] for c in CUSIP.values()},
         "anc_rows": {c: anc_rows[c] for c in CUSIP.values()}, "anchor_meta": meta, "reader": reader, "tx": dict(tx),
         "yahoo_none_reason": {tk: (reader[tk] is None) for tk in CUSIP}}
    json.dump(G, open(out, "w"))
    print("axis", len(ax), "first", ax[0], "last", ax[-1], "five", five)
    for tk, c in CUSIP.items():
        print(tk, c, "anchor days", len(anchor[c]), "mark days", len(mark[c]), "reader days", len(reader[tk] or {}), "tx rows", len(tx[c]),
              "anchor duplicate-row days", sum(1 for d, (n, k) in anc_rows[c].items() if n > 1), "of which differing", sum(1 for d, (n, k) in anc_rows[c].items() if k > 1))


if __name__ == "__main__":
    main()
