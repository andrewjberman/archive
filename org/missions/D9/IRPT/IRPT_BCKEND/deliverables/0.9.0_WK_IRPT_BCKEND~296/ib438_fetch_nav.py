#!/usr/bin/env python3
"""IB-pr-438: ONE PASS over Yahoo Finance through the existing reader (fetch_yahoo in data/assets/scripts/silver/commonwealth_price_basis_census.py, not edited).
Every ticker is asked exactly once, at most 50 a call, a pause between calls, no parallel call.  A ticker whose cache file exists is NEVER asked again
(a ticker that returned nothing leaves a none_reason marker, which the reader's cache honours).  Each call is logged (ticker count, bars returned) to <calls.json>.

    python -I ib438_fetch_nav.py <tickers.json> <yahoo_cache> <calls.json>
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
root = HERE.parents[6]
sys.path[:0] = [str(root / "lib"), str(root), str(root / "data/assets/scripts/silver"), str(root / "data/assets/scripts/analysis")]
import commonwealth_price_basis_census as cen  # noqa: E402

START, END = "2026-06-08", "2026-10-10"
PAUSE = 8.0


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    cache, log = Path(sys.argv[2]), Path(sys.argv[3])
    tickers = list(spec["tickers"]) + [spec["control"]]
    assert len(set(tickers)) == len(tickers)
    calls = json.load(open(log)) if log.exists() else []
    done = {t for c in calls for t in c["ticker_list"]}
    todo = [t for t in tickers if t not in done]
    print("distinct tickers", len(tickers), "already asked", len(done), "to ask", len(todo), flush=True)
    for lo in range(0, len(todo), 50):
        batch = todo[lo:lo + 50]
        data, reasons, n = cen.fetch_yahoo(batch, START, END, cache)
        got = sum(1 for t in batch if data.get(t) is not None)
        limited = sum(1 for t in batch if reasons.get(t) == "rate_limited")
        calls.append({"call": len(calls) + 1, "tickers": len(batch), "ticker_list": batch, "with_bars": got, "no_bars": len(batch) - got,
                      "rate_limited_not_read": limited, "reader_calls": n})
        json.dump(calls, open(log, "w"))
        print("call", len(calls), "tickers", len(batch), "with bars", got, "rate_limited", limited, flush=True)
        if limited:
            print("RATE-LIMITED: stop; nothing repeated", flush=True)
            break
        if lo + 50 < len(todo):
            time.sleep(PAUSE)


if __name__ == "__main__":
    main()
