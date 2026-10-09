"""RIV-wf-1 AC1 -- the holdings calendar classifies a capture by its claim against the PREVIOUS capture's claim, and a
Bloomberg canonical row's `delivered_on` is the capture's requested date. CTO ruling ADDENDUM 4 (msg 2128; row D1-S7).

(a) gold_holdings_coverage.classify(expected, actual, periodic, prev_actual=...): claim newer than the previous -> "new";
    equal -> "repeat"; older -> "regressed". CGIC's real sequence (requested 10-05 claims 10-02 after a 09-30 claim;
    requested 10-06 claims 10-05) reads "new" both days.
(b) "regressed" is one of the module's STATUSES.
(c) control: with no previous claim (the first capture), today's rule stands: a claim equal to the expected day is "new".
(d) gold_canonical_shape.build_bloomberg_rows(..., requested_date=<date>) writes delivered_on = the requested date.
Pure: no S3.

Run from the repository root:  python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~V1/ws2/checks/wf-1.AC1.py
Last line: `AC1 RESULT: PASS 0 failures` or `AC1 RESULT: FAIL <n> (<arms>)`.
"""
import datetime as dt
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 9))
sys.path[:0] = [ROOT, os.path.join(ROOT, "data", "etfs", "scripts")]

from rivalfunds import gold_canonical_shape as gcs  # noqa: E402
from rivalfunds import gold_holdings_coverage as cov  # noqa: E402

D = dt.date.fromisoformat
fails = []


def check(arm, ok, detail):
    print(("OK   " if ok else "FAIL ") + f"({arm}) {detail}", flush=True)
    if not ok:
        fails.append(arm)


def cls(expected, actual, prev):
    try:
        return cov.classify(D(expected), D(actual), False, prev_actual=D(prev) if prev else None)[0]
    except Exception as e:  # noqa: BLE001 -- the missing keyword at the base is the expected FAIL
        return f"{type(e).__name__}: {e}"


got = [cls("2026-10-05", "2026-10-02", "2026-09-30"), cls("2026-10-06", "2026-10-05", "2026-10-02"),
       cls("2026-10-07", "2026-10-05", "2026-10-05"), cls("2026-10-08", "2026-10-02", "2026-10-05")]
check("a", got == ["new", "new", "repeat", "regressed"], f"CGIC lagged x2, planted equal, planted older -> {got}")
check("b", "regressed" in getattr(cov, "STATUSES", ()), f"STATUSES {getattr(cov, 'STATUSES', None)}")
first = cls("2026-10-02", "2026-10-02", None)
check("c", first == "new", f"control: first capture, claim = expected day -> {first}")

try:
    out = gcs.build_bloomberg_rows([{"weights": 1.0, "position": 1.0, "sha256": "a" * 64, "id": "8035 JP Equity"}], "CGIC",
                                   D("2026-10-05"), "rev", "u", lambda sec, path=None: {"security_key": None, "reason": "fixture"},
                                   None, "fixture", claimed_report_date=D("2026-10-05"), requested_date=D("2026-10-06"))
    b = json.loads(out[0]["extra_attributes"])["bloomberg"]
except Exception as e:  # noqa: BLE001
    b = {"error": f"{type(e).__name__}: {e}"}
check("d", b.get("delivered_on") == "2026-10-06" and b.get("source_report_date") == "2026-10-05",
      f"partition 10-05, requested 10-06 -> {b}")

print("AC1 RESULT: PASS 0 failures" if not fails else f"AC1 RESULT: FAIL {len(fails)} ({', '.join(fails)})")
