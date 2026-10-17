#!/usr/bin/env python
"""OG-ev-5: assemble W/FEES_TRACE.json from the host's per-date counts (FEES_TRACE_COUNTS.json) and lib/trading_calendar.py. No value is typed here that a record does not hold.
The stretch is the CVO's (row Z-S355): the 30 consecutive dates 2026-08-17 to 2026-09-15; the counts below are checked to agree (109 source rows).
usage: python ev5_build.py   (repository root of the worktree that holds FEES_TRACE_COUNTS.json)"""
from __future__ import annotations

import datetime as dt
import io
import json
import statistics
import sys

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
FROM, TO = "2026-08-17", "2026-09-15"
CVO_ROWS = 109                      # row Z-S355: "reads 109 partition rows firm-wide"

sys.path.insert(0, ".")
import lib.trading_calendar as tc  # noqa: E402

doc = json.load(io.open(W + "FEES_TRACE_COUNTS.json", encoding="utf-8"))
rows = doc["partitions"]
assert not doc.get("stopped_on_memory") and doc.get("account_resolved")
by = {r[0]: r for r in rows}
days = (dt.date.fromisoformat(TO) - dt.date.fromisoformat(FROM)).days + 1
inside = [r for r in rows if FROM <= r[0] <= TO]
outside = [r for r in rows if not (FROM <= r[0] <= TO)]
src_in, acc_in = sum(r[1] for r in inside), sum(r[3] for r in inside)
src_med, acc_med = statistics.median([r[1] for r in outside]), statistics.median([r[3] for r in outside])
expected = [d.isoformat() for d in tc.trading_days_between(FROM, TO)]
on_trading = [d for d in expected if d in by]
non_trading = [r for r in inside if r[0] not in set(expected)]


def near(rows_in, med):
    return med > 0 and rows_in < 0.25 * med * days


verdict = "source" if near(src_in, src_med) else ("account" if near(acc_in, acc_med) else "neither")
if src_med == 0 and acc_med == 0:
    verdict = "not_determined"
body = {
    "read_at": doc["read_at"],
    "window": doc["window"],
    "stretch": {"from": FROM, "to": TO, "days": days},
    "source": {"rows_in_stretch": src_in, "median_rows_per_day_outside": src_med, "partitions_in_stretch": len(on_trading), "partitions_expected_in_stretch": len(expected)},
    "account": {"rows_in_stretch": acc_in, "median_rows_per_day_outside": acc_med},
    "verdict": verdict,
    "stretch_basis": "the CVO's stretch (row Z-S355: %d partition rows, 2026-08-17 to 2026-09-15); this trace's source count for it is %d: %s" % (
        CVO_ROWS, src_in, "agree" if src_in == CVO_ROWS else "DISAGREE"),
    "source_ratio_to_median_times_days": round(src_in / (src_med * days), 3) if src_med else None,
    "account_ratio_to_median_times_days": round(acc_in / (acc_med * days), 3) if acc_med else None,
    "account_median_is_zero_so_not_assessable": acc_med == 0,
    "partitions_total_in_stretch": len(inside),
    "partitions_on_non_trading_days_in_stretch": len(non_trading),
    "rows_on_non_trading_days_in_stretch": sum(r[1] for r in non_trading),
    "partitions_missing_on_trading_days_in_stretch": [d for d in expected if d not in by],
    "partitions_in_window": len(rows),
    "account_nonzero_fee_amounts_in_window": sum(r[4] for r in rows),
    "source_rows_outside_stretch_mean_per_day": round(statistics.mean([r[1] for r in outside]), 1),
    "memory_basis": "fresh_process",
}
io.open(W + "FEES_TRACE.json", "w", encoding="utf-8", newline=chr(10)).write(json.dumps({"body": body}, indent=1) + chr(10))
print(json.dumps({k: body[k] for k in ("stretch", "source", "account", "verdict", "stretch_basis", "source_ratio_to_median_times_days", "partitions_total_in_stretch",
                                       "partitions_on_non_trading_days_in_stretch", "partitions_missing_on_trading_days_in_stretch")}, indent=1))
