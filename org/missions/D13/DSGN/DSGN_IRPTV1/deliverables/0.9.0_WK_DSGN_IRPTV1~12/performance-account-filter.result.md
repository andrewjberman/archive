# DSGN_IRPTV1.TO-IV-e-21 -- session log, 0.9.0_WK_DSGN_IRPTV1~12

## What was built

- `ReportingTab.tsx` -- one import (`AccountFilter` from `../holdings/AccountFilter`) and
  one mount line (`<AccountFilter scope={scope ?? null} />`), placed after the
  `FirmAttribution` row and immediately before `<PerformanceHeadline report={report} />`,
  outside both `<details>` disclosures ("Report details" and "Monthly returns and
  accounts"). `AccountFilter.tsx` itself is untouched (READ ONLY per the worker face): it
  already falls back to `HeaderSelectionContext` when its own props are absent, the same
  pattern `HoldingsTab.tsx` already uses for the same component.
- Two new tests under `__tests__/dsgn-irptv1/` (neither existed before this order):
  `iv-e-21.performance-filter.test.ts` (IVE21-AC1) and `iv-e-21.at-rest.test.ts`
  (IVE21-AC2). Both reuse the fixture + construction pattern
  `iv-e-10.holdings-filter.test.ts` and `iv-e-18.census.test.ts` already established
  (`resolvedScope.success.json` / `directoryEntry.success.json`, a `HeaderSelectionContext.
  Provider` carrying a real accepted two-account selection, `handleAccountFilterChange`
  exercised directly).

## Placement decision

The cell text names "above the Performance headline"; Holdings mounts the same component
after its own headline-equivalent (`HoldingsSummary`) and before its main picture
(`DrillTree`). Performance has no equivalent "main picture" slot before the headline, so
the filter is mounted directly before `PerformanceHeadline` (after the firm-attribution
row, which is chrome, not a headline or disclosure) -- literally above the headline, as
instructed, and outside both `<details>` blocks that bracket it above and below.

## No-regression checks

- `dsgn-irptv1/iv-e-18.census.test.ts`, `iv-e-18.retained.test.ts`, `iv-e-19.at-rest.test.ts`,
  `iv-e-19.opens.test.ts`, `iv-e-19.design-clause.test.ts`: all pass, unchanged VERDICT
  lines, before and after this order's edit.
- `fe-s-10/parity.test.ts`, `fe-s-5/fields.test.ts`: pass (2 and 4 sub-tests respectively).
- `fe-s-33/fixtures-reach.test.ts`, `fe-s-54/stated-state-wins.test.ts`,
  `fe-s-57/carry.test.ts`: pre-existing failures, module-load-time (a `StatusSchema.allOf`
  shape TypeError) or `EnvelopeMismatch`-class, unrelated to `ReportingTab.tsx`/
  `AccountFilter.tsx` and already part of the documented round-3 baseline (row
  DSGN_IRPTV1-S14: "IR suite ... 742 pass / 82 fail, the only round-3 residual fe-s-5/
  states" -- this order touches neither file class).

## Mutant + determinism controls

- Mutant: removed the new mount line + comment from `ReportingTab.tsx` (python edit, in
  place); both IVE21-AC1 and IVE21-AC2 failed with the expected leaked/absent-filter arms
  (`filter-count=0`, `filter-idx=-1`). File restored byte-for-byte from a saved copy
  (`.scratch/ReportingTab.tsx.good`); `git diff --stat` afterward showed only the intended
  6-line addition (identical to the pre-mutation diff), and both tests re-ran clean.
- Determinism: both tests run twice in a row post-restore, identical VERDICT lines both
  times (`PERF-FILTER-OK`, `FILTER-AT-REST-OK`).

## Surprises filed

- None. The pre-existing test failures found during the no-regression sweep are already
  covered by the round-3 close row (`DSGN_IRPTV1-S14`, 82 pre-existing failures measured at
  the drain) and touch no file this order edits.
