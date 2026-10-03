"""DB11-1-AC2 -- PRD v0.7 ruling 27: the fix admits exactly row W1-S17's measured set and moves income only, never return.

Reads deliverables/0.9.0_WK_IRPT_DASHBD~6/SHORT_DIV_DEBIT_R11.json:
  {"span": ["2026-01-02", "2026-10-01"], "partitions_scanned": 188,
   "newly_admitted_div_debit_rows": 38, "newly_admitted_amount_abs": 822.51,
   "admitted_with_nonnegative_share_quantity": 0, "zero_share_div_debit_rows_excluded": 1,
   "account_days_compared": <int > 0>, "return_delta_nonzero_account_days": 0, "income_delta_nonzero_account_days": <int > 0>}
Grades every field above as written (the amount within 0.01). The span and counts are W1-S17's own measurement
(188 fact_trn partitions, 38 DIV debits with negative shares, 822.51 absolute, 1 zero-share row).
Usage: python <this file> <repo_root>
"""
import json
import sys
from pathlib import Path

REC = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~6/SHORT_DIV_DEBIT_R11.json"


def fail(msg):
    print("FAIL: " + msg)
    print("DB11-1-AC2 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    p = root / REC
    if not p.is_file():
        fail("no record at %s" % REC)
    r = json.loads(p.read_text(encoding="utf-8"))
    want = {"span": ["2026-01-02", "2026-10-01"], "partitions_scanned": 188, "newly_admitted_div_debit_rows": 38,
            "admitted_with_nonnegative_share_quantity": 0, "zero_share_div_debit_rows_excluded": 1,
            "return_delta_nonzero_account_days": 0}
    for k, v in want.items():
        if r.get(k) != v:
            fail("%s is %r, not %r" % (k, r.get(k), v))
    try:
        amt = float(r.get("newly_admitted_amount_abs"))
    except (TypeError, ValueError):
        fail("newly_admitted_amount_abs is not a number")
    if abs(amt - 822.51) > 0.01:
        fail("newly_admitted_amount_abs is %s, not 822.51" % amt)
    for k in ("account_days_compared", "income_delta_nonzero_account_days"):
        v = r.get(k)
        if not isinstance(v, int) or isinstance(v, bool) or v <= 0:
            fail("%s is %r, not a positive int" % (k, v))
    print("OK: 38 short DIV debits admitted (822.51), 0 with non-negative shares, 1 zero-share row excluded; return DELTA=0 on "
          "%d account-days, income moved on %d" % (r["account_days_compared"], r["income_delta_nonzero_account_days"]))
    print("DB11-1-AC2 PASS")


if __name__ == "__main__":
    main()
