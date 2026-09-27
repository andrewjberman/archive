# DSGN_IRPTV1.TO-IV-e-64 -- session log, 0.9.0_WK_DSGN_IRPTV1~41

Cell `IV-e-64` (row DSGN_IRPTV1-S23): IV-e-53 threaded `selectedTenant` into
the Export PREVIEW; the SUBMIT still dropped it, so the one
`POST /api/scoped/investor-reporting/export` an internal viewer sent
answered 200 `state: UNAVAILABLE` / `public_reason_code: UNEXPECTED`
(backend BucketUnmapped) and nothing rendered.

## Build

Additive-only:

- `export/submit.ts` -- `buildSubmitRequest` (and `buildAnalysisSubmitRequest`
  beside it) gain an optional 7th-position `selectedTenant`; absent, no
  `selectedTenant` key, byte-identical to before this cell. `downloadRouteFor`
  gains an optional `selectedTenant` and appends `selected_tenant` to the
  route's query when given one AND the route does not already carry the key;
  otherwise the route is returned unchanged. New `receiptForFlow(receipt,
  selectedTenant?)` applies that same rule to the receipt `ExportButton`
  stores, returning the receipt UNCHANGED (`===`) when the rule does not
  change it.
- `export/ExportButton.tsx` -- `handleSubmit` passes its own `selectedTenant`
  prop (already carried since IV-e-53) into `buildSubmitRequest`, and wraps
  the submitted receipt in `receiptForFlow(outcome.receipt, selectedTenant)`
  before storing it in flow state.

**`ReceiptPanel.tsx` and `ExportModal.tsx` are NOT edited.** `ExportModal.tsx`
mounts `ReceiptPanel` and is OUT OF this cell's `<paths>` grant, so a new prop
threaded through it was not an available seam. `receiptForFlow` embeds the
augmented route directly into the `authorizedDownloadRoute` field of the
receipt object `ExportButton` already passes down unchanged through
`ExportModal` to `ReceiptPanel`, so `ReceiptPanel`'s existing
`downloadRouteFor(receipt)` call (one argument, unedited) renders the
augmented href with no component in between needing to know a tenant was
ever threaded.

No poll to thread: `submit.ts`'s own file header (pre-existing, "Round 1's
follow-up read of export-receipt ... is gone") and a source read confirm
`ExportButton`/`ReceiptPanel` make no `getExportReceipt`/`getJobStatus` call
anywhere in this flow -- the receipt IS the submit's own answer (W2-S12/
W3-S5). IVE64-AC1's stub's `getExportReceipt` throws if ever reached, and it
is not.

## Verification

- `iv-e-64.submit-tenant.test.tsx` (IVE64-AC1): a recording fake
  `InvestorReportingApi`, exercising the SAME functions
  `ExportButton.handleSubmit` calls (`buildSubmitRequest`, `submitUnderGate`,
  `receiptForFlow`, `downloadRouteFor`) in the same order. Arms: (a) one
  submit-export call carrying `selectedTenant`; (b) no other read of the
  export is ever reached; (c) the stored receipt's download href carries
  `selected_tenant=<tenant>` and keeps the fixture's own route as its prefix;
  (d) control -- the same flow with no selected tenant: no `selectedTenant`
  key on the request, receipt returned unchanged (`===`) by `receiptForFlow`,
  href unchanged from the fixture's own route. `VERDICT: SUBMIT-TENANT-OK`.
- `bun run typecheck` (`tsc -b --noEmit`, full portal): 0 errors.
- `eslint` on the three touched files: 0 errors; the 2 warnings
  (`react-refresh/only-export-components` on `ExportButton.tsx` and
  `ReceiptPanel.tsx`) are pre-existing -- both files already exported more
  than one component/function before this cell.
- No-regression sweep: `bun test src/pages/InvestorReporting/__tests__/`
  (fe-s-9, fe-s-16, fe-s-31, both iv-e-53 batteries) and the full
  `__tests__/dsgn-irptv1/` directory (113 pass / 0 fail, 551 expect() calls
  across 99 files) -- every sibling battery still green, including the
  fixture `fe-s-9/receipt.ready.json` assertion
  `downloadRouteFor(receipt) === receipt.authorizedDownloadRoute` (no
  selectedTenant argument -> unchanged, exactly as before).
- Mutant: replaced `buildSubmitRequest`'s `tenantField` computation with an
  unconditional `{}` (dropping the selectedTenant spread entirely) via a
  scripted in-place edit; IVE64-AC1 failed exactly as expected
  (`request.selectedTenant=undefined, expected reg-e64` and
  `submitted request selectedTenant=undefined, expected reg-e64`); restored
  the file from a pre-mutation backup, confirmed `git diff --stat` against
  the intended commit showed only the intended 43-insertion/4-deletion hunk,
  and re-ran IVE64-AC1 clean.
- Determinism: IVE64-AC1's exact invocation run 3x (pre-mutant, post-restore,
  post-commit) -- identical `VERDICT: SUBMIT-TENANT-OK`, 1 pass / 0 fail,
  1 expect() call every time.

## Out-of-grant observation (not a surprise for this cell)

`git status --porcelain` in the portal worktree showed ~24 files under
`contracts/wire/` as modified after running `bun test`/`tsc -b`, none of
which this cell edited or grants. `git diff` on each is byte-empty
(LF -> CRLF normalization noise only); left untouched and unstaged. The
commit above stages only the three files this cell's grant and test file
name. (The same condition was recorded independently by
`0.9.0_WK_DSGN_IRPTV1~33`'s own IV-e-53 session log.)

## Surprise channel

Row `DSGN_IRPTV1-S23` (the defect this cell closes) was already filed by
`2.0.0_SA_COO~D` before this task order issued, naming this exact TO as its
`disarm_owner`. No new row was needed: every premise in the cell text held,
every criterion was met within the stated `<paths>` grant, and the pre-filed
row above documents the world-state this cell's fix disarms.
