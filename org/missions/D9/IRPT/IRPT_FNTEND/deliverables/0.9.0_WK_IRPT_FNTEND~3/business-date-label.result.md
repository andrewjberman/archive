# IRPT_FNTEND.TO-FE-s-34 -- business-date label: result

Worker: `0.9.0_WK_IRPT_FNTEND~3`. Worktree pair `/c/tmp/wk-irpt_fntend-5-3-fe-s-34` (CLOUD 0a74710f33) and its `portal/`
(DEV c2eb8eb4). Portal commit `944499a9b4f1e7b00572b80727c0daec32ca2e1b`, **LOCAL** on branch `wk-irpt_fntend-5-3-fe-s-34`.
Proof instance: `IRPT_FNTEND.TO-FE-s-34.business-date-label.proof_of_spec.json` (in this folder).

**The order is still OPEN.** F34-AC6 fails on two assertions outside the grant (row IRPT_FNTEND-W3-S19), so `<status>` was
not flipped.

## What changed

- **Ruling K.** `formatSourceAge` in `state/status.ts` now reads **`Business date age: <figure>`**, where the figure is `under 1m`,
  `Nm`, `Nh` or `Nd`. It used to read `Updated ... ago`. The figure and the branch boundaries are unchanged; only the words changed.
- **Ruling O.** `tabs/analysis/StageDisplay.tsx` and `tabs/analysis/VariantSelector.tsx` now call
  `formatSourceAgeForState(envelope.state, envelope.sourceAsOf)`, the path `StatusPanel` takes. Zero `formatSourceAge(` call
  sites remain outside `state/status.ts`.
- New test `__tests__/fe-s-34/label.test.ts` covers F34-AC2..AC5. `bun-test-clock.d.ts` declares `setSystemTime` (type-only).

## Criteria (deciding runs at portal 944499a9)

| id | verdict | deciding line |
|---|---|---|
| F34-AC1 | PASS | `rc=0` |
| F34-AC2 | PASS | `formatSourceAge( CALL SITES OUTSIDE state/status.ts: 0 (across 215 files)` |
| F34-AC3 | PASS | `ANALYSIS PANELS AGE THE BUSINESS DATE: 2 of 2` |
| F34-AC4 | PASS | `THE LABEL NAMES THE BUSINESS DATE: yes` |
| F34-AC5 | PASS | `"UPDATED" ON A BUSINESS-DATE AGE: 0 (source 0 + render 0 + pure 0)` |
| F34-AC6 | **FAIL** | ` 59 pass` / ` 2 fail` -- fe-s-21 `source-age.test.ts:166`, fe-s-25 `source-age-field.test.ts:65` |
| F34-AC7 | RECORDED (judgment, L9) | labels recorded in the instance; no verdict |

Negative control: the same test file run against the unmodified source printed `2`, `0 of 2`, `no` and `50`, and failed 4 of 4.

## Rows filed

- **IRPT_FNTEND-W3-S19** -- BLOCKING, ARMED (disarm `2.0.0_SA_COO~F`). Under the grant, F34-AC5 and F34-AC6 cannot both pass. Two
  out-of-grant tests assert that the age starts with `'Updated '`.
- **IRPT_FNTEND-W3-S20** -- OBSERVATION, INERT. On a reading, the two panels already aged `business_date`, so the reroute changed
  the wording for an absent or null date, not which field is aged.
- **IRPT_FNTEND-W3-S21** -- OBSERVATION, ARMED (disarm `2.0.0_SA_COO~F`). On the no-status fixture path the panels age
  `availability.sourceAsOf`, an instant, and the new label calls that a business date.

## For the issuer to amend

1. Grant the two test files, or seat the change elsewhere: replace `startsWith('Updated ')` in
   `__tests__/fe-s-21/source-age.test.ts:166` and `__tests__/fe-s-25/source-age-field.test.ts:65` with a check that does not
   spell the label. F34-AC6 then re-runs.
2. Route row W3-S21 for a ruling. The no-status envelope (`state/status.ts:222`) is outside this order's grant.
