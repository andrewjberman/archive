"""IRPT_ANLREQ round 60 (issuer 2.0.0_SA_COO~G2): the issuer's independent recomputation of a typed ETF comparable's row in FWD-10's comparison
section (run 7M). READ ONLY on the repository; reads public Yahoo history through yfinance. Run from the repository root with a python that can
import pypdf and yfinance (not `-I`).

    python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/fwd10_etf_row.py --ticker VNQ --start YYYY-MM-DD --end YYYY-MM-DD [--pdf <saved PDF>]

Uses this file's own arithmetic, never the code under test: the periodic total returns over the common window (the daily close path, rebased to
100 at START; same rule as fwd10_read.py), and the risk figures by the conventions the 7K read recovered on the models and verified on the
portfolio: the last 2 years on month-end levels (24 returns); std dev = sample std of monthly returns x sqrt 12; Sharpe and Sortino from monthly
excess returns over BIL (Sortino's downside deviation about zero excess); beta = regression of raw monthly returns on SPY's; alpha = annualised mean
excess return less beta x SPY's mean excess return. The maximum drawdown convention is not stated on the page, so both the daily-path and the
month-end value are printed. With --pdf each number is reported YES or NOT-ON-PAGE against the text of the comparison pages. A difference in the
second decimal can be a price-source difference (the resident reads the estate tier first): the tolerance is 0.10 pt. Prints numbers only. ASCII.
"""
import argparse
import math
import re

import fwd10_read as fr


def closes(ticker, start, end):
    import yfinance
    frame = yfinance.download(ticker, start=start, end=fr.shift(end, -1), auto_adjust=True, progress=False, group_by="column")
    col = frame["Close"]
    col = col[ticker] if ticker in getattr(col, "columns", []) else col
    return [(d.strftime("%Y-%m-%d"), float(v)) for d, v in col.dropna().items()]


def month_ends(series):
    out = {}
    for d, v in series:
        out[d[:7]] = (d, v)
    return [out[k] for k in sorted(out)]


def monthly_returns(series, last_day, months=24):
    me = month_ends(series)
    me = [x for x in me if x[0] <= last_day]
    me = me[-(months + 1):]
    return [me[i][1] / me[i - 1][1] - 1.0 for i in range(1, len(me))]


def mean(xs):
    return sum(xs) / len(xs)


def sstd(xs):
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def max_drawdown(path):
    peak, worst = path[0], 0.0
    for v in path:
        peak = max(peak, v)
        worst = min(worst, v / peak - 1.0)
    return worst * 100.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--pdf")
    a = ap.parse_args()
    t = a.ticker.upper()
    px = closes(t, fr.shift(a.end, 12 * 3), a.end)
    spy = closes("SPY", fr.shift(a.end, 12 * 3), a.end)
    bil = closes("BIL", fr.shift(a.end, 12 * 3), a.end)
    path = fr.rebase_cut(px, a.start, a.end)
    print("%s common-window days %d, first %s last %s" % (t, len(path), path[0][0], path[-1][0]))
    found = []
    for k in fr.KEYS:
        v = fr.total_return(path, k)
        found.append((k, v))
        print("  return %-4s %s" % (k, "n/a" if v is None else "%.4f" % v))
    last = path[-1][0]
    r, rs, rb = monthly_returns(px, last), monthly_returns(spy, last), monthly_returns(bil, last)
    n = min(len(r), len(rs), len(rb))
    r, rs, rb = r[-n:], rs[-n:], rb[-n:]
    ex = [x - y for x, y in zip(r, rb)]
    exs = [x - y for x, y in zip(rs, rb)]
    sd = sstd(r) * math.sqrt(12) * 100.0
    sharpe = mean(ex) / sstd(ex) * math.sqrt(12)
    down = math.sqrt(sum(min(x, 0.0) ** 2 for x in ex) / len(ex))
    sortino = mean(ex) * 12 / (down * math.sqrt(12))
    mr, ms = mean(r), mean(rs)
    beta = sum((x - mr) * (y - ms) for x, y in zip(r, rs)) / sum((y - ms) ** 2 for y in rs)
    alpha = (mean(ex) - beta * mean(exs)) * 12 * 100.0
    dd_daily = max_drawdown([v for _, v in path])
    dd_month = max_drawdown([v for _, v in month_ends(path)])
    stats = [("std dev", sd), ("Sharpe", sharpe), ("Sortino", sortino), ("beta", beta), ("alpha", alpha), ("max drawdown daily", dd_daily),
             ("max drawdown month-end", dd_month)]
    print("RISK over %d monthly returns ending %s" % (n, last))
    for name, v in stats:
        print("  %-24s %.4f" % (name, v))
    if a.pdf:
        pages = fr.pdf_pages(a.pdf)
        sect = [i for i, tx in enumerate(pages) if "Comparison" in tx]
        text = re.sub(r"\s+", "", " ".join(pages[i] for i in sect))
        print("SECTION pages %s" % [i + 1 for i in sect])
        for name, v in found + stats:
            if v is None:
                continue
            shown = ["%.2f" % v, "%.1f" % v, "%.3f" % v]
            hit = any(s in text or s.replace("-", "−") in text for s in shown)
            print("  on page %-24s %s" % (name, "YES" if hit else "NOT-ON-PAGE"))
    print("DONE (tolerance 0.10 pt; allocation is read by eye: 100 percent in the ETF's class from etf-classifications)")


if __name__ == "__main__":
    main()
