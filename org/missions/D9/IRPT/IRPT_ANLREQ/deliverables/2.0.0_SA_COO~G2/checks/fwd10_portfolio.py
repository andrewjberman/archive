"""IRPT_ANLREQ round 60 (issuer 2.0.0_SA_COO~G2): the issuer's independent recomputation of the PORTFOLIO row of FWD-10's comparison section.
READ ONLY on the repository; reads public Yahoo history through yfinance (the estate's second price tier). Run from the repository root.

    python fwd10_portfolio.py --holdings <Ticker,Dollars,...csv> --start YYYY-MM-DD --end YYYY-MM-DD [--pdf <saved PDF>]

It buys the holdings' dollars at the window START close (units = dollars / price), holds them (buy-and-hold, no rebalance), values the sum at
every trading day to END, rebases to 100 and prints the periodic total returns with the same arithmetic as fwd10_read.py (1m 3m ytd 1y 3y 5y
10y; a period longer than the window reads n/a). With --pdf it reports, for each number, whether it appears in the comparison pages' text.
The resident prices through the estate, yfinance and ycharts tiers, so a difference in the second decimal can be a price-source difference: a
number is a FAIL only when it differs by more than TOL percentage points (0.10) or is absent from the page. Prints numbers only. ASCII output.
"""
import argparse
import csv
import re
import sys

import fwd10_read as fr

TOL = 0.10


def prices(tickers, start, end):
    import yfinance
    frame = yfinance.download(sorted(tickers), start=start, end=fr.shift(end, -1), auto_adjust=True, progress=False, group_by="column")
    close = frame["Close"]
    out = {}
    for t in tickers:
        col = close[t] if t in close else close
        out[t] = [(d.strftime("%Y-%m-%d"), float(v)) for d, v in col.dropna().items()]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--holdings", required=True)
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--pdf")
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.holdings, encoding="utf-8")))
    dollars = {r["Ticker"].strip().upper(): float(r["Dollars"]) for r in rows}
    total = sum(dollars.values())
    print("HOLDINGS %s total %.2f weights %s" % (len(dollars), total, {k: round(v / total * 100, 2) for k, v in dollars.items()}))
    px = prices(list(dollars), a.start, a.end)
    days = sorted(set.intersection(*[{d for d, _ in v} for v in px.values()]))
    days = [d for d in days if a.start <= d <= a.end]
    if not days:
        print("NO COMMON TRADING DAYS in the window")
        sys.exit(1)
    first = days[0]
    print("WINDOW %s .. %s, %d common trading days, first used %s" % (a.start, a.end, len(days), first))
    units = {t: dollars[t] / dict(px[t])[first] for t in dollars}
    path = [(d, sum(units[t] * dict(px[t])[d] for t in dollars)) for d in days]
    base = path[0][1]
    path = [(d, v / base * 100.0) for d, v in path]
    print("PORTFOLIO last level %.4f cumulative %.4f %%" % (path[-1][1], path[-1][1] - 100.0))
    text = ""
    if a.pdf:
        pages = fr.pdf_pages(a.pdf)
        nospace = [re.sub(r"\s+", "", t) for t in pages]
        sect = [i for i, t in enumerate(nospace) if "Comparison:periodictotalreturns" in t]
        text = re.sub(r"\s+", "", " ".join(pages[i] for i in sect))
        print("SECTION pages %s" % [i + 1 for i in sect])
    for k in fr.KEYS:
        v = fr.total_return(path, k)
        if v is None:
            print("  %-4s n/a (period longer than the window)" % k)
            continue
        shown = ["%.2f" % v, "%.1f" % v]
        hit = any(s in text or s.replace("-", "−") in text for s in shown) if a.pdf else None
        print("  %-4s %9.4f %%   on page: %s" % (k, v, "n/a" if hit is None else ("YES" if hit else "NOT-ON-PAGE")))
    print("DONE (portfolio row only; tolerance %.2f pt for price-source differences; the risk table and allocation are read by eye)" % TOL)


if __name__ == "__main__":
    sys.path.insert(0, ".")
    main()
