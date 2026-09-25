# DSGN_IRPTV1.TO-IV-e-16 -- worker session log (0.9.0_WK_DSGN_IRPTV1~10)

Order: `org/missions/D13/DSGN/DSGN_IRPTV1/task-orders/DSGN_IRPTV1.TO-IV-e-16.export-and-tab-order.md`.
Portal commit: `669a60a0be50dc917c10cf8c05e9508b90ffd9d0` on branch `wk-DSGN_IRPTV1-10-portal` (LOCAL).

## What was built

- `portal/src/pages/InvestorReporting/index.tsx`: one page-level Export control in the header
  actions (`data-slot="export-button-control"`, wrapped in `data-slot="export-target"` carrying
  `data-export-tab` / `data-export-kind` / `data-export-revision`), mapped from the active tab via
  `EXPORT_KIND_BY_TAB` (`reporting -> performance`, `holdings -> null`, `analysis -> analysis`) and
  wired to `selectedScopeRef.revision`, through `export/ExportButton.tsx` (consumed unchanged). Two
  test-only seed props added (`initialActiveTab`, `initialSelectedScopeRef`), following this
  project's own established pattern (`ReportingTab.tsx`'s `initialReport`, `TabShell.tsx`'s
  `initialTab`) -- the live app never passes them.
- `portal/src/pages/InvestorReporting/tabs/TabShell.tsx`: `TABS` reordered to Performance, Holdings,
  Analysis (ids unchanged); added `onActiveTabChange` notifier (effect-driven; fires in the browser,
  not under `renderToStaticMarkup`).
- `portal/src/pages/InvestorReporting/tabs/reporting/ReportingTab.tsx`: the answer-bearing body's
  wrapper no longer carries `.ir-page`; the `render/print.css` import is removed (every child
  self-styles via the shared `Panel` component, confirmed by reading each file's own imports).
  `render/**` itself is untouched (verified by `git diff --numstat` against the base, empty).
- `portal/src/pages/InvestorReporting/__tests__/fe-s-5/controls.test.ts`: the disabled-per-tab-Export
  assertion (already failing at this worktree's base -- `PerformanceControls.tsx` retired that
  control in round-2's IV-e-6) re-scoped to assert the retirement plus Refresh's own control, citing
  CTO 100865 / PRD FWD-9, in the same commit as the rest of this cell's work.
- Three new tests under `__tests__/dsgn-irptv1/`: `iv-e-16.page-export.test.ts` (IVE16-AC1),
  `iv-e-16.tab-order.test.ts` (IVE16-AC2), `iv-e-16.screen-layout.test.ts` (IVE16-AC3).

## The gap (surprise row DSGN_IRPTV1-W10-S1)

IVE16-AC1's "zero per-tab Export buttons render on any tab" cannot be fully satisfied inside this
cell's `<paths>` grant: `tabs/analysis/AnalysisTab.tsx` still renders a permanently-disabled
`data-slot="export-button"` control (unconditional, every mount), and `AnalysisTab.tsx` is named in
neither the decomp's `IV-e-16` `writes` column nor this order's `<paths>`. Per the order's own
refusal clause, `iv-e-16.page-export.test.ts` checks the criterion exactly as written across all
three tabs; the header-level arms (exactly one control; it targets the active tab + revision) pass
on all three tabs, and the per-tab-absence arm passes on reporting and holdings but fails on
analysis. The test therefore reports `VERDICT: PAGE-EXPORT-FAIL`, and IVE16-AC1 is graded FAIL in
the proof instance rather than silently marked PASS. Filed in full at
`org/missions/D13/DSGN/DSGN_IRPTV1/surprise-channel/investigations/INVESTIGATION_v1.md` as
`DSGN_IRPTV1-W10-S1`.

## Naming-gate note

The first commit attempt was REFUSED by the naming gate for hand-typing the fixture filename
`fe-s-5/performance.49f-bd.json` (a firm token, `49f`) inside the new `iv-e-16.screen-layout.test.ts`
-- the exact defect surprise row `DSGN_IRPTV1-W3-S2` already documents for this project. Fixed by
switching to the generic, firm-token-free fixture `performanceReport.success.json` (the same one
`iv-e-6.performance-complete.test.ts`, already committed in this same directory, loads by name),
never by naming a lookup()/key()/address() call that has no implementation in this codebase.

## Verification

- `bun test` on each of the three new files individually, plus `fe-s-5/controls.test.ts`, plus the
  full `src/pages/InvestorReporting/__tests__` tree before/after this cell's edits (baseline 661
  pass / 86 fail / 27 skip; after, 664 pass / 86 fail / 27 skip -- the fail count is unchanged: one
  pre-existing failure fixed, one new intentional failure (IVE16-AC1) added).
- `bun run typecheck` (`tsc -b --noEmit`): rc=0, clean, both before committing and after restoring
  from the mutant-control edit.
- `eslint` on the 7 changed/added files: 0 errors, 2 pre-existing warnings in `ReportingTab.tsx`
  unrelated to this cell (react-refresh export-components rule, an unnecessary `useMemo` dep --
  both pre-dating this cell's touch).
- Mutant control (IVE16-AC3): reverted the wrapper's className to carry `ir-page` again; the test
  correctly reported `VERDICT: SCREEN-LAYOUT-FAIL`; restored from `.scratch/ReportingTab.tsx.bak`.
- Determinism: each of the three new tests run twice; byte-identical VERDICT lines both times.

Proof instance:
`org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~10/DSGN_IRPTV1.TO-IV-e-16.export-and-tab-order.proof_of_spec.json`.
