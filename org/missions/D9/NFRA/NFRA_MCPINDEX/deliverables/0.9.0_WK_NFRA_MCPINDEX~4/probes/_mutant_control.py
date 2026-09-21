#!/usr/bin/env python3
"""Mutant control for MXA5-AC1's classify() (the UNCLASSIFIED-detection logic).

Overwrites the prior cell's (MX-a-4's) copy of this file in the same shared deliverables/probes/
folder -- the established per-cell reuse pattern in this slot (MX-a-3 and MX-a-4 each wrote their
own `_mutant_control.py` importing from their own probe module; MX-a-4's proof_of_spec instance
already pins ITS OWN commit's bytes of this file by hash, so overwriting here does not alter that
prior record).

Offline (no AWS call): imports classify() from mx_a_5.py and feeds it a synthetic objects list.
mx_a_5.py's classify() matches by FILENAME SUFFIX (not folder prefix, unlike mx_a_4.py's) -- the
control below exercises that specific difference.

ENGAGED arm: plant one synthetic key under silver/eclipse/ whose filename matches NEITHER a
CANON_TABLES filename NOR an EXCLUDED suffix (e.g.
'silver/eclipse/2026-09-21/zzz_synthetic_unmapped_table.parquet'). Expect: classify() returns it
in `unclassified`, which ac1() would report as FAIL.

DISENGAGED arm: the same synthetic key removed. Expect: no unclassified keys from the synthetic
plant (the real live objects are not re-fetched here; this control tests classify()'s own
discriminating logic in isolation, not a live AC1 run).

This SAME discriminating behavior was also observed LIVE, not just here: this cell's first AC1
run matched every one of the 570 live objects (114 canon x 4 tables + 114 EXCLUDED sentinels, 0
unclassified) with no iteration needed -- so the live positive control is a clean PASS with no
FAIL-then-fix cycle (unlike MX-a-4's). Both observations (offline synthetic plant, and the live
natural all-classified outcome) are recorded in the proof_of_spec instance's controls.mutant field.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mx_a_5 import classify, CANON_TABLES, EXCLUDED_SUFFIXES  # noqa: E402


def run():
    # A real, already-classified key (positive control: must NOT be unclassified)
    base = [
        ("silver/eclipse/2026-09-20/portfolios_simple.parquet", 64437, "2026-09-20T12:33:15Z"),
        ("silver/eclipse/2026-09-20/_meta/silver_complete.json", 455, "2026-09-20T12:33:15Z"),
    ]
    synthetic = ("silver/eclipse/2026-09-21/zzz_synthetic_unmapped_table.parquet", 123,
                 "2026-09-21T00:00:00Z")

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
    print(f"CANON_TABLES count={len(CANON_TABLES)} EXCLUDED_SUFFIXES count={len(EXCLUDED_SUFFIXES)} "
          f"(both imported live from mx_a_5.py, not restated)")
    ok = engaged_ok and disengaged_ok
    print(f"engaged_ok={engaged_ok} disengaged_ok={disengaged_ok}")
    print("RESULT: FIRED-AS-EXPECTED" if ok else "RESULT: CONTROL FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(run())
