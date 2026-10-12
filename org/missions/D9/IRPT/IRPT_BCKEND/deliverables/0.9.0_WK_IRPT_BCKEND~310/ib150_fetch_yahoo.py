#!/usr/bin/env python3
"""IB-pr-454: ONE PASS over Yahoo Finance through the existing reader (fetch_yahoo in data/assets/scripts/silver/commonwealth_price_basis_census.py, not edited).
Copied from ib441_fetch_yahoo.py (~308, unchanged logic); only the start date moves back by EARLIER_TRADING_DAYS trading days before the first graded day 2026-06-10, so
every candidate window has its bars.  Every ticker is asked exactly once, at most 50 a call, a pause between calls, no parallel call.  A ticker whose call was logged is
never asked again.  Each call is logged to <calls.json>.

    python -I ib150_fetch_yahoo.py <tickers.json> <yahoo_cache> <calls.json>
"""
import datetime as dt
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
root = HERE.parents[6]
sys.path[:0] = [str(root / "lib"), str(root), str(root / "data/assets/scripts/silver"), str(root / "data/assets/scripts/analysis")]
import commonwealth_price_basis_census as cen  # noqa: E402
import trading_calendar as tc  # noqa: E402

FIRST_GRADED = dt.date(2026, 6, 10)
EARLIER_TRADING_DAYS = 90
END = "2026-10-14"      # end exclusive: the last bar asked for is 2026-10-13
PAUSE = 8.0


def start_date():
    d = FIRST_GRADED
    for _ in range(EARLIER_TRADING_DAYS):
        d = tc.prev_trading_day(d)
    return d.isoformat()


def main():
    tickers = list(json.load(open(sys.argv[1], encoding="utf-8"))["tickers"])
    cache, log = Path(sys.argv[2]), Path(sys.argv[3])
    assert len(set(tickers)) == len(tickers)
    assert len(tickers) <= 1500, "STOP: above 1,500 distinct tickers"
    start = start_date()
    calls = json.load(open(log)) if log.exists() else []
    done = {t for c in calls for t in c["ticker_list"]}
    todo = [t for t in tickers if t not in done]
    print("start", start, "end (exclusive)", END, "distinct tickers", len(tickers), "already asked", len(done), "to ask", len(todo), flush=True)
    for lo in range(0, len(todo), 50):
        batch = todo[lo:lo + 50]
        data, reasons, n = cen.fetch_yahoo(batch, start, END, cache)
        got = sum(1 for t in batch if data.get(t) is not None)
        limited = sum(1 for t in batch if reasons.get(t) == "rate_limited")
        calls.append({"call": len(calls) + 1, "tickers": len(batch), "ticker_list": batch, "with_bars": got, "no_bars": len(batch) - got,
                      "rate_limited_not_read": limited, "reader_calls": n, "start": start, "end_exclusive": END})
        json.dump(calls, open(log, "w"))
        print("call", len(calls), "tickers", len(batch), "with bars", got, "rate_limited", limited, flush=True)
        if limited:
            print("RATE-LIMITED: stop; nothing repeated", flush=True)
            break
        if lo + 50 < len(todo):
            time.sleep(PAUSE)


if __name__ == "__main__":
    main()
