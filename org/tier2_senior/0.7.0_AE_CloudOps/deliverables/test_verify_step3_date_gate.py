"""CONTROL B for verify_step3_served_category_views.py -- the date gate.

WHY THIS EXISTS. The instrument asserted SMA.aum == 22,794,766.25 UNCONDITIONALLY in
its first two commits. That figure is MARKET-VALUED -- opal_div_sma 18,783,379.81 +
opal_growth_sma 4,011,386.44, moving ~$170k-$250k PER TRADING DAY (measured by
0.4.0_DS_ClientPlatform~Z, 13879/13880/13881; the cross-instrument catch is
3.0.0_SA_CVO~Z's, 14264). So the ungated form FAILS A CORRECT BUILD at any as_of other
than 2026-08-27 -- which is exactly what Monday's scheduled fire produces.

MEASURED AGAINST THE PRE-FIX COMMIT b924645c54, on a correct 2026-08-31 build:
    [FAIL] global       SMA.aum == 22,794,766.25  ->  aum=22950112.08
    [FAIL] 49financial  SMA.aum == 22,794,766.25  ->  aum=22950112.08
    rc=1 REFUSE.
The fix is not "update the number" -- next week it is wrong again. It is the two-track
split: STRUCTURAL propositions scored at every date, LITERAL figures scored ONLY at
LITERAL_AS_OF and otherwise NA_BY_DATE, a third verdict that is never PASS and never
FAIL. An instrument that cannot check something must say so rather than guess.

CONTROL A (the negative control, run against the live plane) lives in the instrument's
own exercise: it must REFUSE the pre-reland artifact. This file is CONTROL B, its
mirror: a CORRECT build at a LATER as_of must be ACCEPTED. Guarding one direction
leaves the other open, and here the two failure modes are opposite -- an instrument
that cannot refuse a bad build, and one that cannot accept a good one.

Hermetic: stubs `_get_body`, touches no AWS.
Usage: python test_verify_step3_date_gate.py   (exit 0 = control holds)
"""
from __future__ import annotations

import importlib.util
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_TARGET = os.path.join(_HERE, "verify_step3_served_category_views.py")

_spec = importlib.util.spec_from_file_location("vs3", _TARGET)
vs3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vs3)

LATER_AS_OF = "2026-08-31"          # Monday's scheduled fire
MONDAY_SMA = 22_950_112.08          # market moved ~+155k -- CORRECT for that day
MONDAY_CLIENT = 268_100_004.11      # that day's OWN pre-extraction total


def fake_get_body(scope: str):
    """A CORRECT build at a later as_of: dollars extracted, reason gone, Direction B
    intact -- every proposition true, and not one literal equal to 08-27's."""
    key = f"platinum/mdpf/{scope}/category-views.json"
    if scope in vs3.SMA_BEARING:
        sma = {"aum": MONDAY_SMA}
        client = {"aum": MONDAY_CLIENT}
    else:
        sma = {"aum": 0.0, "absent_reason": f"{scope} has NO SMA category members"}
        client = {"aum": 1000.0}
    doc = {"as_of": LATER_AS_OF,
           "nodes": {"SMA": sma, "Client": client,
                     "Models": {"children": {"Primary": {
                         "members": [{"aum": float(i)} for i in range(1, 10)]}}}}}
    return doc, key, None


def main() -> int:
    vs3._get_body = fake_get_body
    rc, rows, indeterminate, controls = vs3.check()

    literal = [r for r in rows if r.get("track") == "LITERAL"]
    structural = [r for r in rows if r.get("track") != "LITERAL"]
    ok = True

    if not literal:
        print("XX no LITERAL rows emitted -- the two-track split is gone")
        ok = False
    elif not all(r["verdict"] == "NA_BY_DATE" for r in literal):
        print(f"XX LITERAL rows not all NA_BY_DATE: "
              f"{[(r['scope'], r['verdict']) for r in literal]}")
        ok = False
    else:
        print(f"OK: all {len(literal)} LITERAL row(s) -> NA_BY_DATE")

    bad = [r for r in structural if r["verdict"] != "PASS"]
    if bad:
        print(f"XX {len(bad)} STRUCTURAL row(s) did not PASS on a correct build: "
              f"{[(r['scope'], r['assertion']) for r in bad]}")
        ok = False
    else:
        print(f"OK: all {len(structural)} STRUCTURAL row(s) -> PASS")

    if not all(c["verdict"] == "NA_BY_DATE" for c in controls):
        print(f"XX conservation control not NA_BY_DATE: "
              f"{[(c['scope'], c['verdict']) for c in controls]}")
        ok = False
    else:
        print("OK: conservation control -> NA_BY_DATE (its target is date-scoped too)")

    if indeterminate:
        print(f"XX unexpected INDETERMINATE: {indeterminate}")
        ok = False

    if rc != 0:
        print(f"XX rc={rc}, expected 0 -- a CORRECT later build must be ACCEPTED")
        ok = False
    else:
        print("OK: rc=0 ACCEPT -- the literal does not fail a correct Monday build")

    print("\nCONTROL B: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
