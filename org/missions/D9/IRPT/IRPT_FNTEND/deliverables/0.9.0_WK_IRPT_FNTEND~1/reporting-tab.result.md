# IRPT_FNTEND.TO-FE-s-5 -- Reporting tab -- result

**Worker:** 0.9.0_WK_IRPT_FNTEND~1 | **Branches:** wk-irpt_fntend-1-4-fe-s-5 (workspace), wk-irpt_fntend-1-4-fe-s-5 (portal)
**Portal commit:** e85f6eb84f3a1771a37011a7e77e372570bad02a (LOCAL)
**Workspace commit (surprise row):** f79070102e19153ca60c45764a059975a0585aec (LOCAL)

## What landed

`tabs/reporting/ReportingTab.tsx` requests `PerformanceReport` through the typed
client with real period parameters (`irKey('performance', ...)`) and renders
`Summary`, `CumulativeReturnChart` (only when `dailyCumulative` is non-empty),
`PeriodResults`, `AccountDetail` from `render/performance/` (imported, never
edited) plus this tab's own `MethodAndSources`, in that order, whenever
`isCompleteState(envelope.state)` (READY or STALE); `StatusPanel` otherwise.
`tabs/reporting/PeriodControls.tsx` carries the YTD/1Y/3Y/Since-inception
presets, a custom date range, Refresh and a disabled Export control.
`tabs/reporting/period.ts` holds the pure preset/request/key builders.
`TabShell.tsx` mounts `ReportingTab` for the `reporting` tab only; analysis and
holdings are untouched. `portal/tsconfig.json` carries the `@/*` alias mapping
bun test's resolver reads (F5-AC9).

## Surprises

One row filed, `IRPT_FNTEND-W1-S7` (ARMED, disarm_owner `2.0.0_SA_COO~F`),
consolidating four findings:

1. **The tsconfig.json edit F5-AC9 requires REGRESSES FE-s-3's
   `dropdown-class.test.ts` (F3-AC7).** Verified by a controlled A/B in this
   worktree: reverting `portal/tsconfig.json` to its pre-edit shape (no
   `compilerOptions`) makes `bun test .../fe-s-3/dropdown-class.test.ts` pass
   (2 pass, 0 fail); restoring the edit makes the SAME invocation, run ALONE
   with no fe-s-5 file involved, fail (0 pass, 2 fail, `SyntaxError: Export
   named PageSurfaceControl not found`). F5-AC9 is this order's own criterion
   and `__tests__/fe-s-3/` is not in this order's `<paths>`, so the
   regression is recorded rather than repaired here.
2. `render/performance/MethodsAndSources.tsx` requires `bundle: RenderBundle`
   (an ExportBundle-shaped object) this tab, which calls only
   `getPerformanceReport`, never has and never fetches. Resolved by NOT
   importing it: `tabs/reporting/MethodAndSources.tsx` is original code
   printing the same method/lineage facts from the one contract this tab
   holds.
3. `render/performance/Summary.tsx` requires `RenderPerformanceReport`
   (`beginningValue`/`endingValue`/`valuationCurrency`), fields the raw
   `PerformanceReport` contract does not carry. Resolved by
   `toRenderPerformanceReport`, an additive bridge reading those fields off
   the payload when present (this tab's own fixtures carry them, the same
   pattern `render/manifest.ts` already uses) and marking them honestly
   unsupported otherwise.
4. `PerformanceReport.supported.benchmark` / `.valueHistory` do not exist on
   the contract; presence is read from non-empty `benchmarks` (inside
   `PeriodResults` itself) and non-empty `dailyCumulative` (gated in
   `ReportingTab.tsx`). Separately, the cell's "StatusPanel ... for every
   non-READY envelope" wording contradicts `state/status.ts`'s own
   `isCompleteState` (READY+STALE, exercised by FE-s-3's own
   `status.test.ts`); `ReportingTab.tsx` uses `isCompleteState`, which is also
   why `performance.unavailable-metric.json` (itself PARTIAL) is graded on
   its StatusPanel coverage text rather than a `Metric`-level UNAVAILABLE
   render it cannot structurally reach.

## Mid-build fix: colour law (not a surprise -- caught and repaired before the
smoke captures)

The first F5-AC6 capture showed the reused `render/performance/*` components
rendering light/near-invisible text directly on the silver canvas: their
`.ir-*` classes carry no colour outside a `.ir-page` ancestor
(`render/print.css:101-111`), which this tab was not applying.
`render/print.css`'s own header states it "drives BOTH planes: the screen
preview and the server-side PDF", so `ReportingTab.tsx` now imports it and
wraps the report body in `.ir-page` (not
`.ir-page-performance-landscape-letter`, which fixes an 11in print width
unsuited to a responsive, narrow-viewport tab). Re-captured both PNGs after
the fix; both now show dark-on-white body text inside the sheet, on the
silver canvas.

## Criteria

All nine criteria PASS-by-output or RECORDED (F5-AC8, judgment). See the
`proof_of_spec.json` beside this file for the full evidence and denominators;
`python .tools/proof-of-spec-check.py <instance> F5-AC1,...,F5-AC9` -> rc=0.
