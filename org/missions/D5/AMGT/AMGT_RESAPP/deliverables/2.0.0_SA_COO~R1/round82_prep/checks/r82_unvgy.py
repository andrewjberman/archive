"""AMGT_RESAPP round-82 PREP -- the served no-forecast reason for a block whose forecast gaps are all per-period (UNVGY US).

  python r82_unvgy.py --crit AC1 [--where local|deployed]

AC1: GET /security/UNVGY_US_Equity/thesis -> the served `forecast_reason`:
  U1 the route answers 200 and a forecast_reason is served;
  U2 it no longer carries the false "pulled before C-MODEL-FORECASTS" text (UNVGY's stamp DOES carry bestdata.json);
  U3 it names the period-end-date absence (the per-period reason the block stores: "no BEST_PERIOD_END_DATE for this period").
Verdict: R82 UNVGY AC1 SERVED: YES|NO (exit 0|1). At the base (live aAkcp2l1, 2026-10-09) it reads NO.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r82_call import caller, find, say  # noqa: E402

FALSE_TEXT = "pulled before C-MODEL-FORECASTS"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1"])
    ap.add_argument("--where", choices=("local", "deployed"), default="local")
    a = ap.parse_args()
    get = caller(a.where)
    code, body = get("/security/UNVGY_US_Equity/thesis")
    reason = find(body, "forecast_reason")
    print("   forecast_reason: %r" % (reason,))
    r = [say(code == 200 and isinstance(reason, str) and reason != "", "U1 /thesis answered %s with a forecast_reason" % (code,)),
         say(isinstance(reason, str) and FALSE_TEXT not in reason, "U2 the reason no longer says '%s'" % FALSE_TEXT),
         say(isinstance(reason, str) and "period end date" in reason.replace("_", " ").lower().replace("period-end", "period end"),
             "U3 the reason names the period-end-date absence")]
    ok = all(r)
    print("R82 UNVGY AC1 SERVED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
