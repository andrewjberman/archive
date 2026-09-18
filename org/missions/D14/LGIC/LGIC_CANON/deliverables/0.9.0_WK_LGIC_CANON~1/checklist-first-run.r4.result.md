# LGIC_CANON.TO-CN-o-5-r4 -- result

**Worker:** `0.9.0_WK_LGIC_CANON~1`. **Drain commit:** `2ffab54e60`. **Proof commit:** `b341301421`.

`reached + carded == steps`: **12 REACHED** (1,2,3,4,5,6,7,8,9,11,12,15) + **4 CARDED** (10,13,14,16) = **16** of 16.

All 7 mechanical criteria (C6R4-AC1 through AC7) PASS-by-output against
`org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r4/check_cn_r4.py`, re-run against the
pinned commit with identical results, and against the checker's own 20-arm self-test (all 20 PASS, no unsatisfiable
arm). C6R4-AC8 is JUDGMENT: recorded `UNVERIFIABLE-BY-INSTRUMENT` for `3.0.0_SA_CVO` at L9, no worker verdict.

`python .tools/proof-of-spec-check.py org/missions/D14/LGIC/LGIC_CANON/deliverables/0.9.0_WK_LGIC_CANON~1/LGIC_CANON.TO-CN-o-5-r4.checklist-first-run.proof_of_spec.json C6R4-AC1,C6R4-AC2,C6R4-AC3,C6R4-AC4,C6R4-AC5,C6R4-AC6,C6R4-AC7,C6R4-AC8 --governing-order org/missions/D14/LGIC/LGIC_CANON/task-orders/LGIC_CANON.TO-CN-o-5-r4.checklist-first-run.md`
-> `VALID (rc=0)`: 8/8 acceptance rows structurally valid, 5/5 artifacts CONTENT-resolved at the pinned commit,
7/7 invocation rows match modulo placeholder expansion, 2/2 surprise rows resolve to a channel row.

Two checklist stalenesses found and corrected inside this cell's own grant (Steps 11 and 13); a third, minor
context-number discrepancy filed and left uncorrected in the task order (it is CONTEXT, not an acceptance value).
Two surprise rows filed: `LGIC_CANON-W1-S6`, `LGIC_CANON-W1-S7`.

FWD-5 does not close on this cell alone (decomposition v6 s.0f): the carded set names `ADVI_FIRMBKTS` (Steps 10 and
16), Andrew's still-open portal-paths sovereign input plus `1.0.0_SA_CTO`'s register-entry extension (Step 14), and
one unrelated `LGIC_ENFORCE`-owned registry RAISE (Step 13) as the remaining, closeable gaps.

**Verdict: MET.** Status flipped to `complete` in the same commit as this file.
