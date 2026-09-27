# DSGN_IRPTV1.TO-IV-e-60.drill-and-bases -- session log (0.9.0_WK_DSGN_IRPTV1~38)

## What was wrong (window 9)

`iv-e-42.drill-bases.test.tsx` already built and tested UIR-31/32/33/34/36/47/49 once. Window 9 found
two of its own rules wrong for a real production shape:

1. **UIR-32/49 -- the breadcrumb dropped a solo account's own name.** `DrillTree.tsx`'s `Breadcrumbs`
   dropped ANY solo root's crumb ("All holdings" already names it) -- true for a generic
   scope/client wrapper, false for a single-account selection whose one root IS the account.
   `iv-e-42`'s own `SOLO_ACCOUNT` regression control asserted the DROPPED crumb as correct. Worse:
   an account with exactly one child reaches this state on the FIRST screen with ZERO clicks --
   `initialDrillRef` opens straight past the account onto its one child -- so "All holdings / Models"
   with no account name in it at all was reachable without any user action, exactly window 9's
   report.
2. **UIR-34 -- the one-child-no-pie check used the wrong denominator.** The branch checked
   `rows.length` (the STRUCTURAL child count) rather than `donutRows.length` (the rows the pie
   actually draws -- `rows.filter(r => r.amount !== null)`). A level with TWO structural children
   where only one carries a resolvable amount still drew a lone 100% wedge.

## Fix

- `DrillTree.tsx` Breadcrumbs: `path={roots.length === 1 && roots[0].kind !== 'account' ? path.filter(...) : path}`
  -- the root crumb is dropped only when the solo root is NOT itself an account.
- `DrillTree.tsx` pie suppression: `donutRows.length === 1 ? <SliceTable .../> : (...)` -- checks the
  DRAWN row count, never the structural one.
- `iv-e-42.drill-bases.test.tsx`: its SOLO_ACCOUNT control is REVERSED in place (now expects exactly
  1 crumb naming the account, matching the corrected rule) -- every other arm in that file is
  untouched and still passes.

## Test

New `iv-e-60.drill-bases.test.tsx`, one VERDICT line gating:
- UIR-32/49: the literal window-9 shape (solo account, zero clicks) now shows 2 crumbs, both
  carrying the account's masked tail; a REGRESSION CONTROL confirms a genuine common-wrapper root
  (BASE_SNAPSHOT's own shape) still drops the wrapper's own redundant crumb.
- UIR-31: `onAccountDrill` wiring regression (unchanged from IV-e-42).
- UIR-33/36/47: percentage bases in words (table header/hover, donut tooltip) and as a markup
  contract (`data-pct-base="parent"`) -- regression.
- UIR-34 (window 9): a level with two structural children but only one drawn (non-null amount) row
  shows no pie -- plus two positive controls (the plain one-structural-child case; a two-drawn-row
  level keeps its donut).

## Controls

- **Mutant** (two, applied together): reverted the Breadcrumbs fix back to `roots.length === 1` with
  no account-kind check, AND the pie-suppression check back to `rows.length === 1`. Re-ran IVE60-AC1
  -- 5 failures pushed: the 4 UIR-32/49 lines (crumb count wrong, account not named, model crumb
  missing/mismatched tail) plus the UIR-34 window-9 line (pie drawn for the two-structural/one-drawn
  level). Restored both lines (python edit); `git diff --stat` before commit showed exactly the 2
  intended hunks (14 insertions / 3 deletions in `DrillTree.tsx`). Re-ran clean: both `iv-e-60` and
  `iv-e-42` print their own `VERDICT: DRILL-BASES-OK`.
- **Determinism**: ran IVE60-AC1's exact invocation twice post-restore -- identical `VERDICT:
  DRILL-BASES-OK`, 1 pass / 0 fail, 1 expect() call, both runs.

## No-regression sweep

- Targeted: `fe-s-76/revision-mismatch-guard.test.ts`, `fe-s-7/drill.test.ts`,
  `iv-e-41.every-account.test.tsx`, `iv-e-43.one-colour.test.tsx`, `iv-e-59.slice-colours.test.ts`,
  plus `iv-e-42`/`iv-e-60` themselves and the rest of `fe-s-7/` -- 43+18 pass, 0 fail.
- Full suite (`__tests__/`, no path filter): 828 pass, 27 skip, 7 fail, 862 tests across 237 files.
  All 7 failures are PRE-EXISTING and outside this cell's grant: `fe-s-1/fixtures.test.ts` (smoke-map
  route coverage), `fe-s-1/source-bounds.test.ts` ('ycharts' forbidden token in
  `api/endpoints/investor-reporting.ts`), `fe-s-25/absent-vs-null.test.ts` (a `?? null` scan over
  `contracts/adapt.ts`), `fe-s-45/residuals.test.ts` (dev-server config-loader reach, environment-
  dependent), `fe-s-57/carry.test.ts` (`unprojected_grant` carry over two routes). None touch
  `tabs/holdings/{DrillTree,SliceTable,slices}.ts` or either drill-bases test file.

## Compiler tools

- `bun run typecheck` (`tsc -b --noEmit`, full portal): 0 errors.
- `bun run lint` (`eslint .`, full portal): 0 errors, 193 pre-existing warnings -- identical count to
  IV-e-59's own baseline. `DrillTree.tsx` carries the same 3 pre-existing
  `react-refresh/only-export-components` warnings on functions this cell did not touch
  (`renderInsideLabel`, `renderDrillLegend`, `modelSliceColor`); the new test file carries none.

## Declared exclusion

AC2 (UIR-31/32/33/34/36/47/49 read on the running page) is judgment-graded by 3.0.0_SA_CVO at L9 per
the task order; this worker's grant does not include a live portal DEV walk, so AC2 is recorded
UNVERIFIABLE-BY-INSTRUMENT, never self-graded.

## Surprises

None filed. This cell's own "Build" text named both regressions (the dropped account crumb and the
`rows.length` vs `donutRows.length` mismatch) and explicitly granted edit access to `iv-e-42`'s own
test file to reconcile its now-superseded control -- so reconciling that file was the task, not a
deviation from it. No premise failed, no path was elsewhere, no capability was missing.
