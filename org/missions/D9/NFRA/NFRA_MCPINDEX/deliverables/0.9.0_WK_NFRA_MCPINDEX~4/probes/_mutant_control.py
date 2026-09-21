#!/usr/bin/env python3
"""Mutant control for MXA3-AC1's unclassified-key REFUSAL (not an acceptance criterion; controls.mutant
harness only, mirrors NFRA_MCPINDEX.TO-MX-c-1's probes/_mutant_control.py pattern).

Plants a synthetic regression by deleting the 'silver/prices/' entry from mx_a_3.EXCLUDED (a REAL prior
state of this probe, before that entry was added to fix a genuine FAIL this cell hit during
development), then re-runs the same live classify() this AC1 verdict is built on. ENGAGED (entry
missing) must reproduce the same class of failure (unclassified keys present, not-PASS); DISENGAGED
(entry restored) must return to the clean classification. Nothing is written to S3; only in-memory
dict state is mutated, and it is restored before this script exits.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
import mx_a_3 as m  # noqa: E402


def run_once(label):
    objs = m.list_all("silver/")
    per_table, exc_count, exc_bytes, unclassified = m.classify(objs)
    print(f"  [{label}] objects={len(objs)} unclassified={len(unclassified)} "
          f"sample={unclassified[:3]}")
    return len(unclassified)


def main():
    print("MUTANT CONTROL -- MXA3-AC1 unclassified-key detection")
    saved = m.EXCLUDED.pop("silver/prices/")
    try:
        n_engaged = run_once("ENGAGED (silver/prices/ exclusion removed)")
    finally:
        m.EXCLUDED["silver/prices/"] = saved
    n_disengaged = run_once("DISENGAGED (exclusion restored)")

    engaged_ok = n_engaged > 0
    disengaged_ok = n_disengaged == 0
    print(f"engaged_ok={engaged_ok} (unclassified count {n_engaged} > 0) "
          f"disengaged_ok={disengaged_ok} (unclassified count {n_disengaged} == 0)")
    print(f"VERDICT: {'FIRED-AS-EXPECTED' if (engaged_ok and disengaged_ok) else 'DID-NOT-FIRE'}")


if __name__ == "__main__":
    main()
