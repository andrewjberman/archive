"""RIV-we-1 AC1 -- a Bloomberg canonical row's report date is the vendor's claimed as-of date; the delivery day is kept apart.

build_bloomberg_rows(..., claimed_report_date=<date|None>) writes, in extra_attributes["bloomberg"]:
  source_report_date = the claim; delivered_on = the delivery day (the function's report_date); report_date_claim =
  "MEASURED" -- and with no claim, source_report_date = the trading day before delivery and report_date_claim = "INFERRED".
Pure: fixture rows, no S3. CTO ruling ADDENDUM 2 @9f0a957c00 (row ETFS_RIVALS-D1-S5).

Run from the repository root:  python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~V1/ws2/checks/we-1.AC1.py
Last line: `AC1 RESULT: PASS 0 failures` or `AC1 RESULT: FAIL <n> (<arms>)`.
"""
import datetime as dt
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 9))
sys.path[:0] = [ROOT, os.path.join(ROOT, "data", "etfs", "scripts")]

from rivalfunds import gold_canonical_shape as gcs  # noqa: E402

fails = []
BASE = [{"weights": 1.0, "position": 100.0, "sha256": "a" * 64, "id": "8035 JP Equity", "name": "TOKYO ELECTRON",
         "report_date": "2026-10-05", "requested_date": "2026-10-05"}]
DELIVERY = dt.date(2026, 10, 5)


def check(arm, ok, detail):
    print(("OK   " if ok else "FAIL ") + f"({arm}) {detail}", flush=True)
    if not ok:
        fails.append(arm)


def attrs(claim):
    try:
        out = gcs.build_bloomberg_rows([dict(r) for r in BASE], "CGIC", DELIVERY, "rev", "u",
                                       lambda sec, path=None: {"security_key": None, "reason": "fixture"}, None, "fixture",
                                       claimed_report_date=claim)
    except Exception as e:  # noqa: BLE001 -- the missing keyword at the base is the expected FAIL
        return {"error": f"{type(e).__name__}: {e}"}
    return json.loads(out[0]["extra_attributes"])["bloomberg"]


a = attrs(dt.date(2026, 10, 2))
check("a", a.get("source_report_date") == "2026-10-02" and a.get("delivered_on") == "2026-10-05"
      and a.get("report_date_claim") == "MEASURED", f"claim 10-02, delivered 10-05 -> {a}")

b = attrs(None)
check("b", b.get("source_report_date") == "2026-10-02" and b.get("delivered_on") == "2026-10-05"
      and b.get("report_date_claim") == "INFERRED", f"no claim, delivered Mon 10-05 -> prev trading day 10-02 -> {b}")

c = attrs(DELIVERY)
check("c", c.get("source_report_date") == "2026-10-05" and c.get("delivered_on") == "2026-10-05"
      and c.get("report_date_claim") == "MEASURED", f"control: claim equals delivery -> {c}")

print("AC1 RESULT: PASS 0 failures" if not fails else f"AC1 RESULT: FAIL {len(fails)} ({', '.join(fails)})")
