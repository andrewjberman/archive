# DSGN_IRPTV1.TO-IV-e-6 (performance-complete) -- result

Worker: `0.9.0_WK_DSGN_IRPTV1~5`. Portal branch `wk-DSGN_IRPTV1-5-portal`, commit
`04f1aa21b0efb597e3fa0790541cc2e594d85c37` (LOCAL, carries IV-e-1's a380bcb5, IV-e-2's
4a55727e/42337b2469 first). Workspace branch `wk-DSGN_IRPTV1-5`.

## What changed

Four new components under `tabs/reporting/`, one existing file's footer popover widened, one
ruled block touch:

**(a) `PerformanceControls.tsx`.** Same base props as `PeriodControls` (`period`,
`onPresetChange`, `onCustomRangeChange`, `onRefresh`, `requestedDates`, `actualDates`) plus one
additive `feeBasis` prop. Presets render only the four `period.ts` actually declares (YTD, 1Y,
3Y, SI -- measured: `PeriodPresetId = 'YTD' | '1Y' | '3Y' | 'SI'`, no QTD id anywhere; never
invented). NET/GROSS renders as a LABEL, never a toggle -- measured against
`api/endpoints/investor-reporting.ts`'s `getPerformanceReport`/`PerformanceReportRequest`: the
built query is `{ start, end, selected_tenant }`, no fee-basis parameter anywhere. No Export
button (FWD-9 is round 3's page-level Export).

**(b) `PerformanceChart.tsx`.** Full-width `AreaChart` over `dailyCumulative`, gradient fill +
`ReferenceArea` shading + hover tooltip -- the TECHNIQUE read from `ModelPortfolios.tsx`'s AUA
Trend Analysis panel (`:2099`/`:2114`/`:2164`), not its literal colours (that panel is an
inverted-band `Panel`; this tab's panels are the white `variant="nested"` surface every other
component here uses, so the chart draws `render/brand.ts`'s own navy/hairline constants).
Empty `dailyCumulative` renders `PanelEmpty` (C12), never an empty axis. No benchmark overlay
invented (`benchmarks[]` carries period returns only today).

**(c) `ReturnsHeatmap.tsx`.** An ORIGINAL component, NOT an import/wrap of
`components/BenchmarkHeatmap.tsx` -- that file's data shape (`BenchmarkModelData[]`, a fixed
10-period ladder) and its own internal net-cost-from-gross proration are incompatible with
`PerformanceReport` and this cell's own "spread never computed" rule (CALL 3). Reuses its
VISUAL PATTERN only (periods across, portfolio/benchmark/spread rows), the same resolution
`SecurityList.tsx` already set for `slices.ts`. Filed as row `DSGN_IRPTV1-W5-S3`. Spread = the
server-stated `benchmarks[0].spread`, applied to the ONE period it answers (the answered-window
period); every other spread cell "not supplied".

**(d) `AccountsTable.tsx`.** One row per `accountDetail` entry. NAME HONESTY: measured against
`contracts/adapt.ts`'s `adaptPerformanceReport` (read-only) that the CURRENT adapter sets
`displayName = accountId` and `maskedDiscriminator = null` unconditionally -- a naive read
would print an id disguised as a name. `accountName()` checks `maskedDiscriminator` presence
and `displayName !== accountId` before trusting `displayName`, else "not supplied". Filed as
row `DSGN_IRPTV1-W5-S4`. `covered` renders as a word ("Covered" / "Not covered -- <reason>"),
never `true`/`false`; an uncovered id not already represented in `accountDetail` gets its own
row too (none in the success fixture -- `uncoveredAccountIds` is empty and the adapter derives
it FROM `accountDetail`'s own flags, so every uncovered account is already a row).

**(e) `PerformanceHeadline.tsx` footer.** `MethodAndSources.tsx`'s rows (method, basis,
currency, producer, source coordinate + revision, report revision, entitlement revision,
schema, ingested, generated) absorbed into the EXISTING `HelperTip` popover (that file read,
not edited); the footer's always-visible LINE now reads `method -- basis -- currency --
source`.

**(f) `ReportingTab.tsx` (T4).** `<PeriodControls>` -> `<PerformanceControls>` (+ `feeBasis`
prop); `<CumulativeReturnChart>` -> `<PerformanceChart report={report} />`; `<PeriodResults>`
-> `<ReturnsHeatmap report={report} />`; `<AccountDetail>` -> `<AccountsTable report={report}
/>`; `<MethodAndSources report={report} />` removed. Imports adjusted (5 removed: PeriodControls,
CumulativeReturnChart, PeriodResults, AccountDetail, MethodAndSources; 4 added: the new
components). Hop-11 catch line and the `<AnswerStatus .../>` mount untouched.

## IVE6-AC1 -- PERFORMANCE-COMPLETE

`bun test .../iv-e-6.performance-complete.test.ts` -- PASS. `HEATMAP: 3 periods, portfolio
3/3, benchmark 1/3, spread 3 x "not supplied"` / `ACCOUNTS: 2 rows, 0 uncovered rows, 0 ids
printed, 0 true/false` / `CHART: 3 points` / `CONTROLS: presets=["YTD","1Y","3Y","SI"]
QTD-absent=true BASIS: label` / `VERDICT: PERFORMANCE-COMPLETE`.

Mutant control: `AccountsTable.tsx`'s `accountName()` replaced with a bare `row.accountId`
return -- re-ran, test failed (no VERDICT line). File restored, `git diff` clean afterward.

## IVE6-AC2 -- SPREAD-AND-CONTROLS-OK

`bun test .../iv-e-6.spread-and-controls.test.ts` -- PASS. `ARM A: no spread supplied -> all 3
cells "not supplied": true; no computed diff found: true` / `ARM B: planted spread 0.011 on
period "YTD" -> cell reads "1.10%" (expected "1.10%"): true` / `CONTROLS: preset calls=1
arg=YTD refresh calls=1` / `VERDICT: SPREAD-AND-CONTROLS-OK`.

This codebase's `bun test` React plane is `renderToStaticMarkup`-only -- no fireEvent/DOM
simulation (measured, `__tests__/fe-s-9/branding.test.ts`'s own header). The controls arm calls
`PerformanceControls(props)` directly (a plain JS function call, no DOM) and walks the returned
React element tree to the button carrying `data-preset="YTD"` / `data-action="refresh"`, then
invokes each one's own `onClick` prop -- the SAME function a real click would call.

Mutant control: `ReturnsHeatmap.tsx`'s spread cell replaced with a computed
portfolio-minus-benchmark difference for every period -- re-ran, test failed (ARM A's
not-supplied/no-computed-diff check failed, no VERDICT line). File restored, `git diff` clean
afterward.

## IVE6-AC3 -- RULED-BLOCK-ONLY

`git show <base>:ReportingTab.tsx` located the import region end at base line 87 and the ruled
block `<PeriodControls>`..`<MethodAndSources report={report} />` at base lines 200-233.
`git diff -U0 <base> -- ReportingTab.tsx`: 7 hunks at base lines `64, 76, 78, 80, 200, 206,
220`, all inside the import region `[1,88]` or the ruled block `[200,234]`. Hop-11 catch line
and the `<AnswerStatus .../>` mount confirmed byte-present. `render/**`,
`PeriodControls.tsx`, `AnswerStatus.tsx`, `MethodAndSources.tsx` numstat empty (0 lines
changed, all four). `VERDICT: RULED-BLOCK-ONLY`.

`bun run typecheck` (`tsc -b --noEmit`): rc=0, 0 errors, run before AND after the
`ReportingTab.tsx` touch and again after the full commit.

## IVE6-AC4 -- RECORD, no verdict (judgment, CVO at L9)

- `iv-e-6.performance.html` (11840 bytes): `renderToStaticMarkup` over all five components
  (`PerformanceControls`, `PerformanceHeadline`, `PerformanceChart`, `ReturnsHeatmap`,
  `AccountsTable`), concatenated, over `fixtures/performanceReport.success.json`. Contains
  `YTD` (preset + heatmap column + headline tile), `Basis: net` (footer line), `Coastal Ridge
  Trust` (account name, printed verbatim since it differs from its own accountId), `Spread`
  (heatmap row label). Confirmed `acct-1001` (an accountId) never appears verbatim anywhere in
  the markup.

No smoke PNG offered for this criterion: IV-e-2's committed fixture
(`dsgn-irptv1-cottonwood.json`) has no route reachable that serves a `performance-report`
response from a click-free `ui-smoke.mjs` run (the criterion's own text is conditional -- "if
IV-e-2's fixture renders it" -- and it does not), and this order's grant names only the
`bun test` fixture set (`performanceReport.success.json`, `performance.*.json`,
`fixtures/wire/`), not `scripts/ui-smoke.mjs`'s grammar. The static markup is the substantive
AC4 artifact.

## Surprise rows filed

`DSGN_IRPTV1-W5-S3` (OBSERVATION, INERT) -- `components/BenchmarkHeatmap.tsx`'s data shape and
internal net-cost computation are incompatible with `PerformanceReport` and this cell's "never
compute a spread" rule; `ReturnsHeatmap.tsx` reuses its visual pattern only, never imports it.

`DSGN_IRPTV1-W5-S4` (OBSERVATION, INERT) -- `contracts/adapt.ts`'s `adaptPerformanceReport` sets
`accountDetail[].displayName = accountId` unconditionally (measured, out of grant to fix);
`AccountsTable.tsx`'s own `displayName !== accountId` check is the working detector.
