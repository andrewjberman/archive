# IRPT_FNTEND.TO-FE-s-6 -- the Analysis tab -- result

Worker: `0.9.0_WK_IRPT_FNTEND~3`. Branches: workspace `wk-irpt_fntend-3-1-fe-s-6`
(HEAD at TO start `9a71ef7626`); portal `wk-irpt_fntend-3-1-fe-s-6` (HEAD at TO
start `65a37017`, committed to `488b0c31` in this session).

## What was built

- `portal/src/pages/InvestorReporting/tabs/analysis/parity.ts` -- widens
  `ReportSection` (contracts carry no `parity` field) with an optional
  `parity?: { passed, reason }`, `isSupported`/`isModeled`/`unsupportedReason`.
- `portal/src/pages/InvestorReporting/tabs/analysis/correction.ts` --
  `deriveInputRevision` (`corrections.length + 1`, since `AnalysisRequest`
  carries no `inputRevision` field), `submitCorrection` (calls the typed
  client, then returns a NEW request built by spreading -- never mutates the
  one passed in).
- Six panels: `VariantSelector.tsx`, `RequestList.tsx`, `InputReview.tsx`,
  `StageDisplay.tsx`, `NativeSections.tsx`, `VendorPdfPreview.tsx`.
- `AnalysisTab.tsx` -- the orchestrator: does its own `listAnalysisRequests` /
  `getAnalysisReport` fetching (TabShell's selection store carries only a
  `TabEnvelope` per slice, never the analysis payload), composes the six
  panels, and a permanently disabled Export control.
- Six fixtures under `fixtures/fe-s-6/` and three smoke maps under
  `fixtures/smoke/`.
- Five files under `__tests__/fe-s-6/` (`_load.ts` + four test files):
  `variants`, `correction`, `sections`, `source-bounds`.

## Two premise gaps, recorded as `IRPT_FNTEND-W3-S1` and `-S2`

1. **`IRPT_FNTEND-W3-S1` (ARMED, disarm owner `2.0.0_SA_COO~F`).** The order's
   own text ("Tab ... mounted in TabShell's analysis body") and its RECORD
   FACE preflight ("The tab mounts into TabShell's existing `analysis` body by
   export name") both assume a mount point that does not exist at this
   worktree's HEAD: `TabShell.tsx` renders `<StatusPanel tabId={activeTab}
   envelope={envelope} />` unconditionally for every tab, and its own
   docstring says so ("tabs/reporting/, tabs/analysis/, tabs/holdings/ are
   later cells"). `TabShell.tsx` is not in this order's `<paths>` and is
   listed in BOUNDS as "IMPORTED, never edited", so this worker cannot wire
   it in. Measured directly: both `ui-smoke` captures (F6-AC6/F6-AC7) show the
   tab strip with ANALYSIS active and a bare `StatusPanel` below it -- no
   `VariantSelector`/`RequestList`/`InputReview`/`StageDisplay`/
   `NativeSections`/`VendorPdfPreview`/Export control anywhere; the tool's own
   `FIXTURE-DEAD` line names `analysis-report` as declared but never matched,
   confirming no live code path calls `getAnalysisReport`. F6-AC6/F6-AC7 still
   PASS mechanically (`rc=0`, the named invocation ran, `LOC` recorded);
   F6-AC8's L9 judgment is recorded against what the PNGs actually show, with
   the correction-view/modeled-label content the criterion names cited from
   the passing F6-AC3/F6-AC4 unit-render output instead. The same gap sits
   under FE-s-5 (Reporting) and FE-s-7 (Holdings) -- neither sibling holds
   `TabShell.tsx` either.
2. **`IRPT_FNTEND-W3-S2` (INERT).** The order's ACT text names
   `AnalysisRequest.inputRevision` and `section.parity.passed` as if reading
   existing contract fields; `contracts/index.ts` (FE-s-1, out of `<paths>`)
   carries neither. Resolved additively inside this order's `<paths>` (see
   `correction.ts` / `parity.ts` above) rather than by editing the shared
   contracts file.

Filed at `org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v1.md`,
rows `IRPT_FNTEND-W3-S1` (ARMED) and `IRPT_FNTEND-W3-S2` (INERT).

## Verification

- `bun run typecheck`: rc=0.
- `bun test src/pages/InvestorReporting/__tests__/fe-s-6/`: 19 tests across 4
  files (+1 shared loader), 19 pass, 0 fail, 78 `expect()` calls --
  `variants` (4 pass), `correction` (5 pass), `sections` (6 pass),
  `source-bounds` (4 pass).
- Full `bun test src/pages/InvestorReporting`: 132 tests across 26 files, 131
  pass, 1 skip, 0 fail, 760 `expect()` calls -- no regression against the
  other seventeen fe-s-1..fe-s-4/fe-s-8 files.
- Mutation control: `parity.ts`'s `isSupported` inverted
  (`!== true` instead of `=== true`); `sections.test.ts` failed as expected (3
  pass, 3 fail); reverted via Edit and confirmed byte-identical to the
  committed blob (`git diff --stat`: no content change); re-ran 6/6.
- `node scripts/ui-smoke.mjs investor-reporting ... --click Analysis`: rc=0
  both at 1440 (`fe-s-6_analysis_ready_1440.png`, 4/5 fixtures matched) and at
  390 (`fe-s-6_analysis_correction_390.png`, 4/4 fixtures matched). Both
  captures show `StatusPanel`'s generic envelope rather than this cell's
  component tree, per the `IRPT_FNTEND-W3-S1` gap above.
- `.tools/surprise-row-gate.py` on the investigation file (staged): 2 new
  row(s) of 22 total, all step-7/step-10 fields present, OK.
- `.tools/proof-of-spec-check.py` on this instance (staged): `VALID (rc=0)`,
  0 violations, 8/8 acceptance rows aligned to cell `FE-s-6`.

## Commits

- Portal repo: `488b0c31` (23 files, 2360 insertions) on branch
  `wk-irpt_fntend-3-1-fe-s-6`, LOCAL (not pushed).
- Workspace repo: this instance, this result file, both PNGs, the two
  surprise rows and the task order's `<status>` flip, committed together,
  LOCAL (not pushed).
