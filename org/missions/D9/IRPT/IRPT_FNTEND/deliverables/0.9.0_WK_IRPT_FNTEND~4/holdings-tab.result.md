# IRPT_FNTEND.TO-FE-s-7 -- Holdings tab -- session log

Worker: `0.9.0_WK_IRPT_FNTEND~4`. Worktree: `/c/tmp/wk-irpt_fntend-4-1-fe-s-7` (branch
`wk-irpt_fntend-4-1-fe-s-7`), portal worktree same branch name in the portal repo.

## What was built

- `portal/src/pages/InvestorReporting/tabs/holdings/slices.ts` -- pure rules (basis
  labels, classification, denominator validity, tree navigation, drill destinations,
  revision-bound drill refusal, slice-row construction, model coverage).
- `HoldingsSummary.tsx`, `SliceTable.tsx`, `DrillTree.tsx`, `HoldingsTab.tsx`.
- Eight fixtures under `fixtures/fe-s-7/` and two smoke maps under `fixtures/smoke/`.
- `__tests__/fe-s-7/slices.test.ts`, `drill.test.ts`, `source-bounds.test.ts` (32 tests,
  0 fail, 156 `expect()` calls) and a type-only `ambient-shims.d.ts` (`Matchers.toBeCloseTo`).

## Two surprises filed

`IRPT_FNTEND-W4-S1` -- `TabShell.tsx`'s holdings body mount fills with `StatusPanel` only
today and is out of this cell's grant / explicitly not-editable, so "mounted in TabShell's
holdings body" cannot be performed here. `IRPT_FNTEND-W4-S2` -- `CategoryViewTree.tsx` is
hard-wired to the AUM-domain `MdpfCategoryViewsResult` contract and cannot carry this
cell's basis/denominator/signed-amount/classification rules; used only for a coarse
top-level overview via an adapter, with every substantive rule implemented directly.

Both are visible empirically in the F7-AC5/AC6 PNGs: the Holdings tab, once clicked,
renders only the generic `StatusPanel` state, never this cell's own component tree.

## Controls

Mutant: flipped `isInvalidDenominator`'s boundary (`<= 0` -> `>= 0`); 2 of 18
`slices.test.ts` tests failed exactly as predicted (the denominator-validity checks),
the other 16 stayed green; restored and re-verified 18/18 pass. Determinism: two
back-to-back runs of all three test files differ in only the wall-clock timing line.

## Commits (both LOCAL on branch `wk-irpt_fntend-4-1-fe-s-7`, never pushed)

- portal repo: `3b434bd8c76db8ca66b51468ea242ab431373d5e` -- FE-s-7 component tree,
  fixtures, tests.
- workspace repo: `efb0946ef82c70a80aa4467a63db2e45d9e1c934` -- two surprise-channel rows.
