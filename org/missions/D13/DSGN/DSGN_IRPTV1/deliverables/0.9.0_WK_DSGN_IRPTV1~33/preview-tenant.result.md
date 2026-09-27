# DSGN_IRPTV1.TO-IV-e-53 -- session log, 0.9.0_WK_DSGN_IRPTV1~33

Cell `IV-e-53` (rows DSGN_IRPTV1-S20 / S22): the Export preview's own
`getPerformanceReport` request carried no `selected_tenant`, so the adapter
could not map the viewer's firm and answered UNAVAILABLE for every account --
no export could be made from the page.

## Build

Additive-only, following the exact seam IV-e-36 built for
`accountSelection`/`start`/`end`:

- `export/resolveBundle.ts` -- `ResolveBundleDeps` gains optional
  `selectedTenant`; both `getPerformanceReport` request shapes (the
  print-window path and the pre-IV-e-26 fallback) spread it in only when
  present.
- `export/Preview.tsx` -- `PreviewRequestState` gains optional
  `selectedTenant`; `runPreview` passes it straight to `resolveBundle`.
- `export/ExportButton.tsx` -- `ExportButtonProps` gains optional
  `selectedTenant`; `buildPreviewRequestState` and the component's own
  `request` useMemo thread it through.
- `index.tsx` -- maps `performanceExportOverride?.selectedTenant` (already
  carried by `ReportingTab`'s `PerformanceExportTarget` /
  `buildPerformanceExportTarget`, unedited -- out of this cell's grant) onto
  `ExportButton`'s new prop.
- `render/PrintEntry.tsx` -- reads an optional `?selected_tenant=` URL
  parameter with the same one-line, no-branching form every other optional
  fact on this route already uses, and passes it to `resolveBundle` when
  present; its absence never refuses a print (the three window facts keep
  their own `parsePrintWindow` rule, untouched).

No API edit: `PerformanceReportRequest`/`getPerformanceReport` already carry
`selectedTenant` -> `selected_tenant` (`api/endpoints/investor-reporting.ts`),
confirmed read-only.

## Verification

- `iv-e-53.preview-tenant.test.ts` (IVE53-AC1): recording-stub `bun test`,
  4 arms -- window path with tenant, fallback path with tenant, and the same
  two WITHOUT a tenant (control: no `selectedTenant` key at all). `VERDICT:
  PREVIEW-TENANT-OK`.
- `iv-e-53.tenant-thread.test.tsx` (IVE53-AC2): the real
  `resolveAccountFocus` -> `buildPerformanceExportTarget` -> `index.tsx`'s
  own mapping -> `buildPreviewRequestState` seam, plus the print URL ->
  `parsePrintWindow` + the same one-line `selected_tenant` read ->
  `resolveBundle` seam, with and without the tenant. `VERDICT:
  TENANT-THREAD-OK`.
- `bun run typecheck` (`tsc -b --noEmit`, full portal): 0 errors, both
  before and after every edit.
- `eslint` on the seven touched files: 0 errors; warnings are pre-existing
  patterns (`react-refresh/only-export-components` on files that already
  exported more than one component/function; one unused eslint-disable at
  `resolveBundle.ts:327` and one `set-state-in-effect` at `PrintEntry.tsx`,
  both confirmed present at HEAD before this cell's edit via
  `git show HEAD:<path> | eslint --stdin`).
- Mutant: removed the `...(selectedTenant ? { selectedTenant } : {})` spread
  from both `getPerformanceReport` request shapes in `resolveBundle.ts`;
  IVE53-AC1 failed exactly as expected (`selectedTenant=undefined, expected
  reg-e53` on both the window and fallback arms); restored the file via the
  same scripted transform run in reverse, confirmed `git diff` against the
  intended edit was empty, and re-ran both criteria clean.
- Determinism: both criteria re-run twice post-restore and against the
  final committed HEAD (97c08b21) -- identical VERDICT lines each time.

## Out-of-grant observation (not a surprise for this cell)

`git status --short` in the portal worktree showed 24 files under
`contracts/wire/` as modified (LF -> CRLF) after running `bun test` /
`tsc -b`, none of which I edited and none in this cell's `<paths>`. `git
diff` against every one of them is byte-empty (line-ending normalization
noise only, no content change) -- confirmed via `git diff --stat --
src/pages/InvestorReporting/contracts/wire/` returning nothing. Left
untouched and unstaged; the commit below stages only the seven files this
cell's grant names.
