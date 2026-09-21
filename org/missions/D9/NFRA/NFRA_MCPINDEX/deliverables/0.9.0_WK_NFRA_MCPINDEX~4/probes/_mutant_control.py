#!/usr/bin/env python3
"""Mutant control for MXA4-AC1's classify() (the UNCLASSIFIED-detection logic).

Offline (no AWS call): imports classify() from mx_a_4.py and feeds it a synthetic
objects list.

ENGAGED arm: plant one synthetic key under silver/ that matches NEITHER a CANON_TABLES
prefix NOR an EXCLUDED entry (e.g. 'silver/zzz_synthetic_unmapped_table/2026-09-21.parquet').
Expect: classify() returns it in `unclassified`, which ac1() would report as FAIL.

DISENGAGED arm: the same synthetic key removed (an empty extra list). Expect: no
unclassified keys from the synthetic plant (the real live objects are not re-fetched here;
this control tests classify()'s own discriminating logic in isolation, not a live AC1 run).

This SAME discriminating behavior was also observed LIVE, not just here: the first AC1 run
this cell made (before EXCLUDED gained the 'silver/historical_prices.parquet' entry) returned
`VERDICT: FAIL-MXA4-AC1 unclassified keys present` with exactly that key listed; adding the
entry made AC1 return PASS on the next run, with no other line changing. Both observations
(offline synthetic plant, and the live natural occurrence) are recorded in the proof_of_spec
instance's controls.mutant field.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mx_a_4 import classify, CANON_TABLES, EXCLUDED  # noqa: E402


def run():
    # A real, already-classified key (positive control: must NOT be unclassified)
    base = [
        ("silver/api_dims/positions_mv/snapshot_date=2026-09-20/data.parquet", 1000, "2026-09-20T00:00:00Z"),
    ]
    synthetic = ("silver/zzz_synthetic_unmapped_table/2026-09-21.parquet", 123, "2026-09-21T00:00:00Z")

    # ENGAGED: synthetic key present
    _, _, _, unclassified_engaged = classify(base + [synthetic])
    engaged_ok = synthetic[0] in unclassified_engaged

    # DISENGAGED: synthetic key absent
    _, _, _, unclassified_disengaged = classify(base)
    disengaged_ok = len(unclassified_disengaged) == 0

    print(f"ENGAGED (synthetic key planted): unclassified={unclassified_engaged} "
          f"-> {'CORRECTLY FLAGGED' if engaged_ok else 'FAIL: NOT FLAGGED'}")
    print(f"DISENGAGED (synthetic key absent): unclassified={unclassified_disengaged} "
          f"-> {'CORRECTLY CLEAN' if disengaged_ok else 'FAIL: FALSE POSITIVE'}")
    print(f"CANON_TABLES count={len(CANON_TABLES)} EXCLUDED count={len(EXCLUDED)} "
          f"(both imported live from mx_a_4.py, not restated)")
    ok = engaged_ok and disengaged_ok
    print(f"engaged_ok={engaged_ok} disengaged_ok={disengaged_ok}")
    print("RESULT: FIRED-AS-EXPECTED" if ok else "RESULT: CONTROL FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(run())
