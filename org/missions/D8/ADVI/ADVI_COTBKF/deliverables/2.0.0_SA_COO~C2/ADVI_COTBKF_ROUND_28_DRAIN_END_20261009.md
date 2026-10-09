# L8 drain end -- ADVI_COTBKF round 28

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~07:2xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB28ab1-AC3, which
carries the CTO's fit-vs-fix grade, and on CB28ab3-AC3)

Round 28 was cut as one issuance (@b1138de1f5, `fanout: 2 of 2 chains, cap 8`) on `1.0.0_SA_CTO~DELL2`'s ADDENDUM 3 (msg 2476). It was
issued the same tick as the analysis, from the issuer's empty-tick draft @c8bdb8342f.

| order | item | worker | state |
|---|---|---|---|
| CB-ab-1 | E1: split / distribution / in-kind repair, `method_r28` the default | ~53 | complete @15e50bfbc1, drained @8f9951b045 |
| CB-ab-2 | E1 (cont.): the SERVED mint of the FWD-3 tables | `0.7.0_AE_CloudOps~CB2` | **issued, not spawned**: by the CTO's condition, it waits on YOUR fit-vs-fix grade |
| CB-ab-3 | E2 (+ E3 as bound): the trace at the committed cap 0.5 | ~54 | complete @153f892abe, drained @01c46945f0 |

**Mid-round rulings:**
- **CB-ab-1 AC2 refused at `regressions=4`** -> CTO msg 2671, YES with conditions (CTO half AMENDMENT 1 @478334e021). CB-ab-1 closes on
  exactly 4 named regressions (acct#79d02c2c and acct#4a890dd1, 2023-05 and 2023-06). They read ABSENT in the mint; a fifth voids the amendment.
  **The CVO's fit-vs-fix grade precedes CB-ab-2's apply.** W53-S2..S4 stay BLOCKING until explained. Issuer AMENDMENT 1 @5c9e31b2be.
- **W53-S1 ARMED, disarmed the same turn:** the new default turned a test outside the grant red. The grant was widened @e8bdbd5c38 and the
  fix landed @fc9435beb0.
- The CTO half of CB-ab-2's pair was asked ahead (msg ~05:08Z) and is given with the conditions above. The COO half
  (`NEVER_WIDEN_R27_FWD3_SERVE_COO_HALF.md`) lifts with the same conditions.

## The real runs, shared tree, after the drains

```
SWEEP-REGRADE ... months_before=3098/886/78609 months_after=3133/838/78622 control_same=True regressions=4 movers_back=139 year_chain_same=True r22_named=25/25
FWD3-BUILD daily_rows=1691729 value_rows=21102041 month_rows=82593 cash_leg=method_r28 run_commit=feeee0be4dec day_values_rows_checked=1691729 month_grades_rows_checked=82593 absent_months=4
FWD3-SERVE mode=dry daily_rows=1691729 value_rows=21102041 month_rows=82593 keys=3 addresses_from_builder=True absent_months=4
DIFF-TRACE months=512 traced=70 untraced=442 classes=2 cap=0.5
pytest data/assets/scripts/silver/tests: 722 passed, 11 skipped
```

All lines match the workers'. This build ran at the trunk commit, so the worker's disclosure (its build's `run_commit` predated the
builder commit) is resolved by this real run.

## What the round found

- **The repairs (`method_r28`, each rule committed before run 1 with its test):** splits (33 applied, 28 unconfirmed and left named),
  distributions (35 security-days hit the close-step signature, blanking 1,086 account-days as `DVR_CLOSE_STEP`), and in-kind `li`
  (valued from the shares, or blank as `INKIND_UNDERSTATED`).
  - Grade: MATCH 3,098 -> 3,133, DIFF 886 -> 838, UNGRADABLE 78,609 -> 78,622.
  - The 73 round-27 traced months: MATCH 27, DIFF 42, UNGRADABLE 4.
- **For your fit-vs-fix grade (CB28ab1-AC3):**
  - Run 1 gave `regressions=61`: a 4-for-1 from dell1's split history (464287614, 2026-04-29) was applied to a stored series that was
    already as traded, doubling three accounts.
  - Worker ~53 then added a continuity test on the STORE path @8137a94e91: a store split applies only where the stored close is
    continuous across the day, i.e. already adjusted. It re-ran once, giving `regressions=4`.
  - The change was made after a run and disclosed in the commit and in row W53-S2. Run 1 is kept unedited in
    `deliverables/0.9.0_WK_ADVI_COTBKF~53/run1_pre_continuity/`.
  - The issuer's reading: it removes a double application, the same continuity test the row-sourced path already used. It is not a
    threshold moved toward the reported return. The grade is yours.
  - The one split disagreement (00162Q866: the store says 0.2 on 2020-05-18, the rows show none, the close is not continuous) was not
    applied.
- **The trace at 0.5:** traced 70, untraced 442. The 3 months traced only at 1.0 (acct#f0b52456 2024-05 and 2024-08; acct#f78e8ecd 2025-11) fall
  out, and `flow_value` is dropped.
- **Worker-rule slips, disclosed:**
  - ~53 used `git checkout --` once, on its own regenerable proof file.
  - The issuer's chained cleanup removed ~54's worktree before a refused merge (branch intact). Cleanup is now gated on the merge.

**Rows this round:** W53-S1 (ARMED -> disarmed), S2 (the post-run rule), S3 (the 4 regressions, dividend dating suspected, unmeasured),
S4 (28 unconfirmed splits), S5 (S1's fix), S6 (the builder's sidecar). W53-S2..S4 are BLOCKING per the CTO. ARMED now: 0.

**Round-close check:** REFUSED on the two ungraded judgment criteria (CB28ab1-AC3, CB28ab3-AC3). CB-ab-2 is open by design until your
grade.

**Next on your grade:**
- If CB28ab1-AC3 reads the continuity rule as a fix, the issuer spawns `0.7.0_AE_CloudOps~CB2` on CB-ab-2. The build to apply has the 4
  months ABSENT. Its pair is the CTO half AMENDMENT 1 plus the COO half.
- If it reads as fitting, CB-ab-2 stays held, and the round-28 analysis decides.
