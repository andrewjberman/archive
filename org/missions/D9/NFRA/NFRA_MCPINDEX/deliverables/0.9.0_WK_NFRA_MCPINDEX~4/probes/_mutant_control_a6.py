#!/usr/bin/env python3
"""Mutant control for MXA6-AC1's classify() (the UNCLASSIFIED-detection logic).

A NEW file, not an overwrite of probes/_mutant_control.py -- this slot's issuer named that path
as pinned by a prior cell's (MX-a-5's) proof_of_spec instance by hash, and this cell's classify()
matches by TOP SUBDIRECTORY under smartx/platform/silver/ (not by filename suffix like MX-a-5's, and
not by folder-prefix-equals-table like MX-a-4's) -- a third distinct discriminator shape, warranting
its own control rather than reuse.

Offline (no AWS call): imports classify() from mx_a_6.py and feeds it a synthetic objects list.

ENGAGED arm: plant one synthetic key under smartx/platform/silver/ whose top subdirectory matches
NEITHER a CANON_TABLES subdir NOR an EXCLUDED_SUBDIRS entry (e.g.
'smartx/platform/silver/zzz_synthetic_unmapped_table/date=2026-09-21/data.parquet'). Expect:
classify() returns it in `unclassified`, which ac1() would report as FAIL.

DISENGAGED arm: the same synthetic key removed, replaced by real canon + excluded-draft keys only.
Expect: no unclassified keys from the synthetic plant.

This SAME discriminating behavior was also observed LIVE, not just here: this cell's first AC1 run
against the real 757 live objects returned 0 unclassified (11 canon tables all matched by their
subdir; the 2 pre-naming-law draft objects all matched EXCLUDED_SUBDIRS) with no FAIL-then-fix
iteration needed. Both observations (offline synthetic plant, and the live natural all-classified
outcome) are recorded in the proof_of_spec instance's controls.mutant field.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mx_a_6 import classify, CANON_TABLES, EXCLUDED_SUBDIRS  # noqa: E402


def run():
    # Real, already-classified keys (positive control: must NOT be unclassified)
    base = [
        ("smartx/platform/silver/fact_model_aum_daily/date=2026-09-20/data.parquet", 81480,
         "2026-09-20T09:23:00Z"),
        ("smartx/platform/silver/allocation_positions/date=2026-07-14/data.parquet", 3050617,
         "2026-07-14T02:46:20Z"),  # a real EXCLUDED_SUBDIRS (draft) key
    ]
    synthetic = ("smartx/platform/silver/zzz_synthetic_unmapped_table/date=2026-09-21/data.parquet",
                 123, "2026-09-21T00:00:00Z")

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
    print(f"CANON_TABLES count={len(CANON_TABLES)} EXCLUDED_SUBDIRS count={len(EXCLUDED_SUBDIRS)} "
          f"(both imported live from mx_a_6.py, not restated)")
    ok = engaged_ok and disengaged_ok
    print(f"engaged_ok={engaged_ok} disengaged_ok={disengaged_ok}")
    print("RESULT: FIRED-AS-EXPECTED" if ok else "RESULT: CONTROL FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(run())
