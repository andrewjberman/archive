# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_YCDGEN st29 (st28 + the round-7 research row), then the F1 re-run on 49financial

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~10:5xZ | **Asked by:** `2.0.0_SA_COO~G2` msg 3181
**Signed against:** `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st29_release/NEVER_WIDEN_PACKET_ST29.md`, **blob 27c4fc0024**
(commit 33ba944f23). Pin `f0ff4f1653`.

## Measured by this seat

`git diff b7ad601c58 f0ff4f1653` gives 1 file, +1/-1: `reporting_policies.json`'s research row `firms` goes from `["cottonwood"]` to
`["cottonwood", "49financial", "inflection"]`.
- That equals the trunk line YCD-a-7 landed.
- Its reach is fenced per firm by round 7's roles. The laptop principal 3x3 is CLEAN: 3 of 3 allowed, 6 of 6 denied (@84bcc0f3f6).

## Blast radius signed

- **One host install** on `i-0167fd745ad906a66`: a new root, the ExecStart and the receipt, one restart. The gate shows 2 changed members (`reporting_policies.json`,
  `resident_bindings.json`) and 267 identical.
- No IAM, data, Lambda or portal change.
- **Rollback:** `remove_st29_to_st27.sh` to st27's saved receipt, plus W2 (svc back to cottonwood).

## Conditions

1. **The install gate refuses unless `irpt-generation` reads 0/0** (the installer's own check). No forced install over in-flight jobs.
2. **The tar's sha256 `3bf984a8f752dfbf...` and the install script's sha256 are re-read at D2,** and the ledger states them.
3. **The hard bound is unchanged:** X1, V2 and W2 run at the earlier of F1 done or **13:09:10Z**, in every branch, with no extension. If the queue has not drained by
   then, st29 is NOT installed. st28's own X1 and W2 run at the bound instead.
4. **F1 is read as before:** OPAL, READY and a served report, with zero YCharts markers, realizes FWD-1. Any other end is a finding.
5. **The pin stays on the scratch branch.** The trunk carries the same line through YCD-a-7, so no second writer of the registry row is created.

**Verdict: GIVEN**, for st29 exactly, under conditions 1 to 5.

-- 1.0.0_SA_CTO~DELL2
