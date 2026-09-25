# DSGN_IRPTV1.TO-IV-e-20 -- session log, 0.9.0_WK_DSGN_IRPTV1~11

## What was built

- `DrillTree.tsx` -- a new `DonutHoverTooltip` (renders through the shared `DataTooltip`,
  header = the slice's own `pieLabel`, rows = Value + Weight, a colour swatch matched to the
  slice's own fill) replaces the pie's bare default `<RechartsTooltip />`. A `donutData` memo
  carries each slice's own `sliceColor` once, so the `Cell` fill and the hover swatch read the
  identical hex. The legend entry (`renderDrillLegend`, IV-e-13) drops `whitespace-nowrap` for
  `max-w-full break-words` -- the fix for the one real stray-scrollbar defect AC2's own census
  found at 390px.
- `SliceTable.tsx` -- `formatAmount` exported (was module-private) so `DrillTree` reuses the
  identical amount format the table itself prints.
- `PerformanceChart.tsx` -- `ChartTooltip`'s bespoke white/navy card replaced by the shared
  `DataTooltip` (same header/row content, one shared look).
- Three new tests under `__tests__/dsgn-irptv1/`: `iv-e-20.tooltips.test.ts` (a source census
  of every recharts Tooltip usage under `tabs/`+`header/`, plus a direct render of each named
  content component asserting `DataTooltip`'s own markup), `iv-e-20.scrollbars.test.ts` +
  `iv-e-20-scrollbar-driver.mjs`, `iv-e-20.bands.test.ts` + `iv-e-20-band-driver.mjs`. Both
  drivers are self-contained Playwright-core scripts reusing the COO's own
  `round3-real-run-driver.mjs` auth-stub/CORS/fixture-route recipe against `IR_BASE_URL`
  (default `http://localhost:5174`), per the worker face's own instruction -- never starting a
  server. `iv-e-20.fixture.json` is a copy of the COO's `round3-close.fixture.json`.

## The scrollbar census (IVE20-AC2) -- a real, measured finding

The driver walks every element in the rendered DOM carrying an `overflow(-x)?-(auto|scroll)`
class token or a computed `overflowX` of `auto`/`scroll` (the only two ways a stray scrollbar
can mechanically appear -- an element left at the default `overflow: visible` never renders
one), at 1440 and 390, across the Reporting/Holdings/Analysis tabs, plus the document itself. A
container wrapping a `<table>` is a named table scroller (`SliceTable`, `AccountsTable`,
`ReturnsHeatmap`, `SecurityList`'s own table wrapper) and is excluded.

Run against the LIVE main portal checkout on `:5174` (pre-merge, per the worker face's own
constraint), it found exactly one violation: `[data-slot="holdings-drill-legend"]` at 390 reads
`scrollWidth=316 > clientWidth=250`. Cause: `renderDrillLegend`'s entries set
`whitespace-nowrap` inside a `flex-wrap` row -- a `flex-wrap` parent only wraps BETWEEN
entries, never inside one, so a single model name wider than the legend's own box forces
overflow regardless of how many rows the legend spans. Fixed in this worktree
(`max-w-full break-words`), confirmed by a mutant control (revert -> re-fails identically
against the same unmerged `:5174` -- proving the measurement is of the SERVED page, not this
worktree's own source -- restore -> passes again in-worktree via the source census AC1 style
check would; the browser check itself can only be confirmed post-merge).

**IVE20-AC2 is reported FAIL, as measured against `:5174`, with the fix committed but
unobservable there until the COO merges and re-runs.** Order left `pending`. Row
`DSGN_IRPTV1-W11-S4`.

## Cell (c) -- the Opal website cues

No acceptance criterion in this order tests (c) mechanically; it is covered only by AC4's
holistic judgment call. The canonical duration ladder (DESIGN.md C4, the "short-to-long model
spectrum") already renders throughout Holdings (the donut, its legend, the treemap, the slice
table). No new numbered-card or process-band UI was added: none of `<expected_criteria>` calls
for it, and CLAUDE.md's own no-manufactured-friction / no-inferred-scope rule argues against
building UI a criterion does not test. Declared as an exclusion in the proof instance, for
AC4's reviewer.

## No-regression checks

- `bun run typecheck` (`tsc -b --noEmit`): rc=0. An early draft used the global `process`
  object, invisible to this program's tsconfig (`@types/node` is not in it); fixed to
  `import { env } from 'node:process'`, matching `FE-s-27`'s own ambient-shims precedent
  (`env` is already declared there, program-wide).
- Full `__tests__/dsgn-irptv1/` suite: 70 pass / 2 fail (72 tests, 58 files). One fail is this
  order's own IVE20-AC2 (graded above); the other, `iv-e-10.ruled-touch.test.ts` (IVE10-AC3),
  is PRE-EXISTING and already documented at row `DSGN_IRPTV1-W11-S3` (filed on the prior order
  by this same worker slot) -- this order never touches `HoldingsTab.tsx`.

## Mutant + determinism controls

- Mutant: reverted the legend fix in place (`max-w-full break-words` -> `whitespace-nowrap`),
  re-ran the scrollbar driver directly against `:5174` -- identical `SCROLLBARS-FAIL` output
  either way (the driver measures the served page, which the fix cannot reach pre-merge);
  restored, `git diff --stat` empty against the committed state.
- Determinism: IVE20-AC1/AC2/AC3 each run twice; identical VERDICT lines both times.

## Surprises filed

- `DSGN_IRPTV1-W11-S4` -- the real, measured stray-scrollbar defect (pre-dating this order by
  two rounds, IV-e-13), fixed in this worktree, unobservable as fixed on `:5174` until merge.
