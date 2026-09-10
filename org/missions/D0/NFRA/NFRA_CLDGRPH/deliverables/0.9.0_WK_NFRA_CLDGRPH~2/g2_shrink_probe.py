#!/usr/bin/env python3
"""g2_shrink_probe -- THE ROUND'S LESSON, MADE FALSIFIABLE.

NFRA_CLDGRPH.TO-CG-G-3 / CG-s-34, criterion G3-AC4. Slot 0.9.0_WK_NFRA_CLDGRPH~2.

THE SENTENCE THIS REPLACES (ROUND_ANALYSIS.round6.md s.7): "A producer that reads back its own
output is silently idempotent under a FIXED emission and silently WRONG under a SHRINKING one --
which is exactly what a nightly with stable counts cannot surface." Everybody agrees with that
sentence, which is the problem with it. This probe turns it into a check somebody can run: given
two successive emissions and one flag -- whether the producer drops its own prior output on read
-- it reports whether a shrink would be MASKED by the archive read, and it says so in numbers.

WHAT IT IS AND IS NOT. It is a one-shot instrument in a deliverables folder, run by a human or by
a criterion, WIRED TO NOTHING: no schedule, no alarm, no SNS, no freshness checker, no monitor
(the standing moratorium, and this order's BOUNDS say so explicitly). It reads no artifact, makes
no AWS call and runs nothing -- the populations below are RECONSTRUCTED IN PROCESS from numbers
the record already measured, and every one of them is cited where it is built.

THE MODEL, stated so it can be disagreed with rather than trusted:
    artifact(cycle N) = dedup( archive_read(cycle N-1's artifact) UNION emission(cycle N) )
    archive_read drops this producer's own edge type only if drop_prior_on_read is set.
Dedup is by the triple identity the producer actually uses -- (source, edge_type, target) -- which
is why a FIXED emission collapses to itself and leaves no trace, and why a SHRINKING one does not.

Usage: python g2_shrink_probe.py     (exit 0 when the probe and its controls behave as predicted)
"""
from __future__ import annotations

import sys

# ---------------------------------------------------------------------------------------------
# THE POPULATIONS, reconstructed from the record. GRAIN: one STORED_IN edge triple.
# COVERAGE: the whole STORED_IN population of one cycle's artifact, denominator 191 firm-relative
# keys. ENVIRONMENT of the baseline numbers: NOT this process -- they were measured on the cloud
# artifact published 2026-09-10T02:15:44Z (row NFRA_CLDGRPH-W2-S71: 955 emitted, 191 distinct
# sources, 5 distinct targets, per-key distribution 5 for all 191; 137 of the 191 keys carry their
# own bucket in props; 54 carry none) and graded in ROUND_ANALYSIS.round6.md s.2 (955 -> 137,
# per-key {5: 191} -> {1: 137}). This process only rebuilds sets of that size and shape.
# ---------------------------------------------------------------------------------------------
KEYS = ["s3:gold/key-%03d" % i for i in range(191)]
BUCKETS = ["opal-data-bd", "opal-data-inf", "opal-data-cot", "opal-data-mdpf", "opal-data-demo"]
# 137 of the 191 keys carry a bucket in their own props; the remaining 54 carry none.
OWN_BUCKET = {k: BUCKETS[i % len(BUCKETS)] for i, k in enumerate(KEYS[:137])}

FANOUT_EMISSION = {(k, "STORED_IN", b) for k in KEYS for b in BUCKETS}          # 191 x 5 = 955
ONE_PER_KEY_EMISSION = {(k, "STORED_IN", b) for k, b in OWN_BUCKET.items()}     # 137


def archive_read(prior_artifact: set, drop_prior_on_read: bool, own_type: str = "STORED_IN") -> set:
    """What arrives back in this run's edge list from the snapshot the derive archived."""
    if not drop_prior_on_read:
        return set(prior_artifact)
    return {e for e in prior_artifact if e[1] != own_type}


def probe(label: str, prior_artifact: set, emission: set, drop_prior_on_read: bool) -> dict:
    """Given two successive emissions, report whether a shrink is MASKED by the archive read."""
    carried = archive_read(prior_artifact, drop_prior_on_read)
    artifact = carried | emission                       # the dedup: a set union on the triple
    stale = artifact - emission                         # asserted by the artifact, not by this run
    shrank = len(emission) < len(prior_artifact)
    masked = shrank and len(stale) > 0
    return {
        "label": label,
        "prior": len(prior_artifact),
        "emitted": len(emission),
        "carried_in_from_the_archive": len(carried),
        "artifact": len(artifact),
        "stale_edges_the_artifact_asserts": len(stale),
        "shrank": shrank,
        "masked": masked,
        "artifact_equals_prior": len(artifact) == len(prior_artifact),
        "drop_prior_on_read": drop_prior_on_read,
    }


def show(r: dict) -> None:
    print("  %s" % r["label"])
    print("    prior artifact %d -> this emission %d | carried in from the archive %d | "
          "artifact after dedup %d | stale edges the artifact asserts and this run did not emit %d"
          % (r["prior"], r["emitted"], r["carried_in_from_the_archive"], r["artifact"],
             r["stale_edges_the_artifact_asserts"]))
    print("    emission shrank: %s | drop-on-read: %s | artifact count equals the prior cycle's: %s"
          % (r["shrank"], r["drop_prior_on_read"], r["artifact_equals_prior"]))
    print("    MASKED: %s" % r["masked"])


def main() -> int:
    print("G2 SHRINK PROBE -- a producer that reads back its own output, as a check rather than a "
          "sentence")
    print("  MODEL: artifact(N) = dedup( archive_read(artifact(N-1)) UNION emission(N) ), dedup by "
          "the (source, edge_type, target) triple. INSTRUMENT COVERAGE: the whole reconstructed "
          "STORED_IN population, denominator 191 firm-relative keys x 5 candidate buckets = 955 "
          "possible triples; 137 of the 191 keys answer from their own props and 54 answer with "
          "nothing. GRAIN: one edge triple. ENVIRONMENT: in-process reconstruction from the "
          "record's measured numbers -- NO artifact read, NO AWS call, NO run.")
    print("")

    # ---- ARM 1: the round's own shrink, with the archive read as it was BEFORE cycle 4 ----
    print("ARM 1 -- POSITIVE CASE, the round's own numbers (fan-out cycle followed by the "
          "one-edge-per-key cycle, no drop on read):")
    a1 = probe("955 -> 137, drop_prior_on_read=False", FANOUT_EMISSION, ONE_PER_KEY_EMISSION, False)
    show(a1)
    print("")

    # ---- ARM 2: a FIXED emission, which is what every night before the shrink looked like ----
    print("ARM 2 -- NEGATIVE CASE, a fixed emission (the same triples emitted twice, no drop on "
          "read) -- the nightly that ran for months and showed nothing:")
    a2 = probe("955 -> 955, drop_prior_on_read=False", FANOUT_EMISSION, set(FANOUT_EMISSION), False)
    show(a2)
    print("")

    # ---- CONTROLS ----
    print("CONTROLS -- a probe that cannot answer both ways is a constant wearing a "
          "measurement's clothes, and a clean negative can also be a DEAD ARM:")
    c1 = probe("955 -> 137, drop_prior_on_read=True (the cycle-4 remedy)",
               FANOUT_EMISSION, ONE_PER_KEY_EMISSION, True)
    show(c1)
    c2 = probe("137 -> 137, drop_prior_on_read=False (fixed emission at the post-fix size)",
               ONE_PER_KEY_EMISSION, set(ONE_PER_KEY_EMISSION), False)
    show(c2)

    ctrl = {
        "positive_arm_returns_true": a1["masked"] is True,
        "negative_arm_returns_false": a2["masked"] is False,
        "remedy_arm_flips_the_answer_on_the_same_numbers": c1["masked"] is False and c1["artifact"] == 137,
        "negative_arm_is_not_a_dead_arm": a2["carried_in_from_the_archive"] == 955 and a2["artifact"] == 955,
        "second_negative_at_a_different_size": c2["masked"] is False,
        "the_masking_is_invisible_by_count": a1["artifact_equals_prior"] is True,
    }
    print("")
    print("  CONTROL LEDGER (each is a prediction made before the arm ran):")
    for k, v in ctrl.items():
        print("    %-52s %s" % (k, v))
    print("    ^ the fourth line is the one that matters most: ARM 2 returns false WHILE 955 edges "
          "really did arrive from the archive, so the false is a measured negative and not an arm "
          "that never carried anything.")
    fired = all(ctrl.values())

    print("")
    print("WHAT ARM 1 MEANS IN ONE LINE: the run emitted 137 and the artifact asserts %d, of which "
          "%d are last night's; a consumer counting edges sees %d and cannot tell this cycle from "
          "the one before it. THAT is silently wrong under a shrinking emission."
          % (a1["artifact"], a1["stale_edges_the_artifact_asserts"], a1["artifact"]))
    print("WHAT ARM 2 MEANS: 955 edges arrived from the archive and every one of them was re-emitted "
          "this cycle, so the union is the emission and nothing is stale. Silently IDEMPOTENT -- "
          "correct output, and no evidence at all that a carry-forward exists.")
    print("")
    print("SUMMARY")
    print("SHRINK_MASKED=true on (955 -> 137) -- %d stale edge(s) of %d in the artifact, %d of %d "
          "emitted this cycle" % (a1["stale_edges_the_artifact_asserts"], a1["artifact"],
                                  a1["emitted"], a1["artifact"]))
    print("SHRINK_MASKED=false on the fixed-emission pair (955 -> 955) -- 955 of 955 carried in and "
          "955 of 955 re-emitted, 0 stale")
    print("PROBE_CONTROL=%s (%d of %d controls hold)"
          % ("FIRED" if fired else "NOT-FIRED", sum(1 for v in ctrl.values() if v), len(ctrl)))
    print("WIRED_TO=nothing -- one-shot, no schedule, no alarm, no notification (BOUNDS of "
          "TO-CG-G-3 and the standing monitoring moratorium)")
    return 0 if fired and a1["masked"] and not a2["masked"] else 1


if __name__ == "__main__":
    sys.exit(main())
