# IRPT_FNTEND.TO-FE-s-34 -- business-date label: result

Worker: `0.9.0_WK_IRPT_FNTEND~3`. Worktree pair `/c/tmp/wk-irpt_fntend-5-3-fe-s-34` (CLOUD 0a74710f33, amended order at
12eef1910c) and its `portal/` (DEV c2eb8eb4). Both portal commits are **LOCAL** on branch `wk-irpt_fntend-5-3-fe-s-34`:

- `944499a9b4f1e7b00572b80727c0daec32ca2e1b` -- the relabel and the reroute, plus `__tests__/fe-s-34/`.
- `f7b2d98657089f7a2251ca808487c524651a1333` -- the amendment: the two `startsWith('Updated ')` checks, and nothing else.

Proof instance: `IRPT_FNTEND.TO-FE-s-34.business-date-label.proof_of_spec.json` (in this folder). **Every mechanical criterion
passes by output, so the order's `<status>` is flipped to `complete`.**

## What changed

- **Ruling K.** `formatSourceAge` in `state/status.ts` now reads **`Business date age: <figure>`**, where the figure is `under 1m`,
  `Nm`, `Nh` or `Nd`. It used to read `Updated ... ago`. The figure and the branch boundaries are unchanged.
- **Ruling O.** `StageDisplay.tsx` and `VariantSelector.tsx` now call
  `formatSourceAgeForState(envelope.state, envelope.sourceAsOf)`, the path `StatusPanel` takes. Zero `formatSourceAge(` call
  sites remain outside `state/status.ts`.
- **Amendment 12eef1910c (on row W3-S19).** Two checks were replaced; each cites ruling K and prints itself both ways:
  - `fe-s-21/source-age.test.ts:166`: `pure.startsWith('Updated ')` became equality with `formatSourceAge(AS_OF, now)`. The
    comparison uses `AS_OF`, the date this file's `pure` is actually computed from (row W3-S22).
  - `fe-s-25/source-age-field.test.ts:65`: the check became equality with `formatSourceAge(BUSINESS_DATE, now)`.

  Every other assertion in both files is as written.

## Criteria (deciding runs on the amended tree)

| id | verdict | deciding line |
|---|---|---|
| F34-AC1 | PASS | `rc=0` |
| F34-AC2 | PASS | `formatSourceAge( CALL SITES OUTSIDE state/status.ts: 0 (across 215 files)` |
| F34-AC3 | PASS | `ANALYSIS PANELS AGE THE BUSINESS DATE: 2 of 2` |
| F34-AC4 | PASS | `THE LABEL NAMES THE BUSINESS DATE: yes` |
| F34-AC5 | PASS | `"UPDATED" ON A BUSINESS-DATE AGE: 0 (source 0 + render 0 + pure 0)` |
| F34-AC6 | PASS | ` 61 pass` / ` 0 fail` / `Ran 61 tests across 14 files.` |
| F34-AC7 | RECORDED (judgment, L9) | labels recorded in the instance; no verdict |

Before the amendment, F34-AC6 ran 59 passing tests and two failures (F21-AC3 and F25-AC4). That run is kept in the row's
`status_reason`.

## Rows

- **IRPT_FNTEND-W3-S19** -- BLOCKING, ARMED. **Resolved** by amendment 12eef1910c, which granted the two checks. They were replaced
  at `f7b2d986`, and F34-AC6 now runs 61 of 61.
- **IRPT_FNTEND-W3-S20** -- OBSERVATION, INERT. On a reading, the two panels already aged `business_date`, so the reroute changed
  the wording for an absent or null date.
- **IRPT_FNTEND-W3-S21** -- OBSERVATION, ARMED. On the no-status fixture path the panels age an instant under the business-date
  label. Still open; the issuer routed it to 1.0.0_SA_CTO.
- **IRPT_FNTEND-W3-S22** -- OBSERVATION, INERT (new). fe-s-21's `pure` is computed from `as_of`, so "the same date" for its
  amended check is `AS_OF`, not the business date.
