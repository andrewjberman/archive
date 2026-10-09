"""AMGT_RESAPP round-82 PREP -- a per-day price series on the timeline route (DSGN round-58 R6 ask 1).

  python r82_timeline.py --crit AC1 [--where local|deployed]

AC1: GET /security/AMD_US_Equity/timeline -> the range body:
  T1 the route answers 200 with its chatter `series` (denominator printed);
  T2 it carries `price_series`: a non-empty list of {date, close} with ISO dates strictly ascending and numeric closes,
     read from the STORED Bloomberg PX_LAST history (bloomberg/harvest/bronze/price_history_px_last/, keyed by the
     Bloomberg ticker 'AMD US'), never fetched from a vendor;
  T3 every price date falls inside the body's own window (floor_date .. the last chatter day) and the body names its
     price source (a `price_series_source` naming price_history_px_last).
Verdict: R82 TIMELINE AC1 SERVED: YES|NO (exit 0|1). At the base (live aAkcp2l1, 2026-10-09) it reads NO (no price_series key).
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r82_call import caller, say  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1"])
    ap.add_argument("--where", choices=("local", "deployed"), default="local")
    a = ap.parse_args()
    get = caller(a.where)
    code, body = get("/security/AMD_US_Equity/timeline")
    series = (body or {}).get("series") or []
    prices = (body or {}).get("price_series")
    r1 = say(code == 200 and len(series) > 0, "T1 /timeline answered %s with %d chatter days" % (code, len(series)))
    ok2 = isinstance(prices, list) and len(prices) > 0
    if ok2:
        dates = [p.get("date") for p in prices]
        ok2 = all(isinstance(d, str) and len(d) == 10 for d in dates) and dates == sorted(set(dates)) and \
            all(isinstance(p.get("close"), (int, float)) and not isinstance(p.get("close"), bool) for p in prices)
    r2 = say(ok2, "T2 price_series: %s" % ("%d points, %s .. %s" % (len(prices), prices[0].get("date"), prices[-1].get("date"))
                                            if isinstance(prices, list) and prices else repr(prices)))
    floor = str((body or {}).get("floor_date") or "")
    last = max((str(s.get("day") or s.get("date") or "") for s in series), default="")
    inside = isinstance(prices, list) and bool(prices) and all(floor <= p.get("date", "") <= (last or "9999") for p in prices)
    source = str((body or {}).get("price_series_source") or "")
    r3 = say(inside and "price_history_px_last" in source,
             "T3 prices inside %s..%s and source named: %r" % (floor, last, source[:90]))
    ok = r1 and r2 and r3
    print("R82 TIMELINE AC1 SERVED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
