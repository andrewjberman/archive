# IRPT_FNTEND.TO-FE-s-9 -- export options, modals, preview, receipt -- result

Worker: `0.9.0_WK_IRPT_FNTEND~1`. Branches: workspace
`wk-irpt_fntend-1-5-fe-s-9` (HEAD at TO start `e31ad6b8a1`); portal
`wk-irpt_fntend-1-5-fe-s-9` (HEAD at TO start `5b959f63`, committed to
`5d5f366d` in this session).

## What was built

- `portal/src/pages/InvestorReporting/export/resolveBundle.ts` -- resolves the
  counterpart's `ExportBundle` (report REFERENCES only) into the render
  package's `RenderBundle`, cache-first through an in-memory `ReportCache`,
  fetching through the typed client only what the cache lacks;
  `MissingPayloadError` (reused from `render/manifest.ts` unmodified) names
  the revision it could not obtain.
- `export/submit.ts` -- pure: `submitExport`, `buildSubmitRequest` /
  `buildAnalysisSubmitRequest` (the analysis export's bound `inputRevision` /
  `configuration` / `artifactHash`), `envelopeFromReceipt`, `downloadRouteFor`.
- `export/ExportModal.tsx` -- the dark-Panel modal: branding (Opal / Advisor /
  Co-branded, the latter two gated on an approved logo asset), the narrative
  toggle, account detail, optional sections. `ScopeForExport` is this
  module's own additive extension of `ResolvedScope` -- the real FE-s-1
  contract carries `approvedAssets` on `ExportBundle`, not on `ResolvedScope`
  as the cell text names it (surprise row `IRPT_FNTEND-W1-S8`).
- `export/AppliedBranding.tsx` -- `appliedBrandingLabel`: reads what was
  APPLIED from the preview bundle, not what was requested; 'Opal' whenever no
  logo asset is present.
- `export/Preview.tsx` -- `PreviewRequestState`, `applyOptions` (same
  `sourceRevision`, bumped `exportRevision` on any options change),
  `runPreview` (the ONE `previewExportBundle` call plus `resolveBundle`), and
  the `Preview` component.
- `export/ExportButton.tsx` -- the button + modal-open state, and
  `ExportAnchorSlot`: finds the disabled Export control by its existing
  `data-action`/`data-slot` name, hides it, and portals the real button into
  the same parent -- `tabs/reporting/PeriodControls.tsx` and
  `tabs/analysis/AnalysisTab.tsx` stay outside this order's grant, unedited.
- `export/ReceiptPanel.tsx` -- `StatusPanel` (imported) driven by
  `envelopeFromReceipt`, plus the download link on `jobState: 'ready'` only.
- `render/manifest.ts` -- package-level `RenderOptions` (the contract's four
  fields plus `includeNarrative`, default false); `assertSupported` now
  tolerates a bundle with no `reportKind` yet (pre-resolution) while still
  refusing a PRESENT-but-wrong one, so a bundle "implementing the contract as
  written" reaches `resolveBundle` instead of being refused.
- `render/performance/PerformanceDocument.tsx` -- the inline placeholder
  `PeriodInContext` retired; the REAL `PeriodInContextPage` (FE-s-8) now
  mounts, gated on `narrativePacket !== null && renderOptions.includeNarrative`.
- `render/PrintEntry.tsx` -- `?kind=` / `?narrative=1` query params; calls
  `assertSupported` then `resolveBundle` before rendering.
- `index.tsx` -- mounts two `ExportAnchorSlot`s (reporting/analysis).
- Six fixtures under `fixtures/fe-s-9/`, two smoke maps under
  `fixtures/smoke/`, six test files under `__tests__/fe-s-9/`.
- `__tests__/fe-s-3/dropdown-class.test.ts` -- the FE-s-5-drain amendment:
  drops the now-intercepting `mock.module` workarounds, asserts the real
  markup, prints `CLASS:`.

## One surprise, recorded once as `IRPT_FNTEND-W1-S8`

The cell text names `ResolvedScope.approvedAssets`; the real FE-s-1 contract
carries `approvedAssets` on `ExportBundle`, and `ResolvedScope` has no such
field. Resolved with an additive extension (`ScopeForExport`), the same
pattern `render/manifest.ts` already uses for `RenderPerformanceReport`.

A SECOND effect of this order's own required amendment is recorded in the
SAME row's evidence rather than as a second row: gating
`PerformanceDocument`'s narrative page on `includeNarrative` (required by
this order) turns `__tests__/fe-s-4/analysis-no-narrative.test.ts`'s existing
POSITIVE CONTROL (outside this order's `<paths>`) from pass to fail --
measured: 3 pass, 1 fail, `expect(hits).toBe(1)` now reads `Received: 0`.
`hazard_standing: ARMED`, `disarm_owner: 2.0.0_SA_COO~F`.

## Verification

- `bun run typecheck` (incremental): rc=0. Forced clean rebuild
  (`./node_modules/.bin/tsc -b --noEmit --force`): rc=0.
- `bun test src/pages/InvestorReporting/__tests__/fe-s-9`: 18 pass, 0 fail, 59
  `expect()` calls across 6 files (default/branding/no-refetch/receipt/
  resolve/narrative-wired).
- `bun test src/pages/InvestorReporting/__tests__/fe-s-3`: 18 pass, 0 fail
  (F9-AC11; `CLASS:` line printed by `dropdown-class.test.ts`).
- Full `bun test src/pages/InvestorReporting`: 202 tests, 200 pass, 1 skip
  (pre-existing, unrelated), 1 fail (the FE-s-4 positive control named above,
  recorded at row `IRPT_FNTEND-W1-S8`).
- Mutation control: `PerformanceDocument.tsx`'s `showNarrative` forced to
  `packet !== null` (dropping the `includeNarrative` check);
  `narrative-wired.test.ts`'s `includeNarrative: false` case failed as
  expected (`Expected: false, Received: true`); reverted from a pre-mutation
  copy, confirmed byte-identical (`diff`: no output), full fe-s-9 suite
  re-passed 18/18.
- `node scripts/ui-smoke.mjs investor-reporting ... --click Export` at 1440px
  and 390px: both rc=0, `LOC: /investor-reporting` (landed), `FIXTURES: 5
  declared; 5 matched >=1 URL`, both PNGs saved.

## Commits

- Portal repo: `5d5f366d` (26 files, 2516 insertions, 94 deletions) on branch
  `wk-irpt_fntend-1-5-fe-s-9`, LOCAL (not pushed).
- Workspace repo: this instance, this result file, both PNGs, the surprise
  row and the task order's `<status>` flip, committed together, LOCAL (not
  pushed).
