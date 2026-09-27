# DSGN_IRPTV1.TO-IV-e-67 -- session log, 0.9.0_WK_DSGN_IRPTV1~41

Cell `IV-e-67` (row DSGN_IRPTV1-S26): window 18's served async export answer
was a data-less `200 QUEUED` body -- `contract_version`, `operation`,
`firm_id`, `unprojected_grant`, `status` only, `data` absent, export id in
`status.operation.revision` (ruling R2, CTO 102138, backend @75156f2b18).
`envelope.ts`'s `parseIrEnvelope` refused any `data`-less body unconditionally
(`EnvelopeMismatch('data')`), so the page never saw a receipt and never polled.

## Build

- `contracts/envelope.ts` -- new `IR_DATA_OPTIONAL_WHILE_LOADING = ['submit-export',
  'export-receipt']`. The `data`-presence check now reads `!('data' in body) &&
  !dataOptionalHere`, where `dataOptionalHere` requires the operation be one of
  the two named AND a well-formed `status` (already validated above by the
  existing `requirePublicStatus` call) whose adapted `state` is `'LOADING'`
  (`STATE_FOR_WIRE`'s collapse of wire `QUEUED`/`RUNNING`). Every other
  data-less body -- a different operation, no status, or any other stated
  state -- still throws `EnvelopeMismatch('data', operation)`, unchanged. When
  the exemption fires, the per-operation adapter is not called at all (nothing
  to adapt) and `adaptedData` stays `null`; `carryAvailabilityFromStatus`/
  `carryUnprojectedGrant` already return `null` unchanged for a null view, so
  the parsed envelope reads `{data: null, status: <adapted>, state: 'LOADING',
  refused: false}`.
- `api/endpoints/investor-reporting.ts` -- `LiveClient.submitExport`
  (interface + implementation) no longer delegates to the shared `send()`
  (which returns only `parsed.data` OR only `parsed.status`, never both, and
  is out of this cell's grant): it inlines the same
  route/build/transport/parse/telemetry/refusal sequence `send()` runs, and
  when `parsed.data !== null` returns it exactly as before (FE-s-31,
  unchanged). When `parsed.data === null` (the exemption fired), it reads the
  export id off the **untouched wire payload** -- `payload.data`/`payload.status`,
  never the adapted view -- through `interpretSubmitExportAnswer`
  (`export/submit.ts`, built and tested at IV-e-26 but uncalled until this
  cell), returning `{exportId, receipt: null}`. The interface's return type
  widens to `Promise<ExportReceipt | {exportId: string; receipt: null}>`
  (a union superset -- every existing implementer, typed or structural, still
  satisfies it). `FixtureAdapter.submitExport` and `getExportReceipt` are
  unedited.
- `export/submit.ts` -- `SubmitOutcome` gains a queued arm (`{submitted: true;
  receipt: null; exportId: string}`); `submitUnderGate` discriminates the new
  shape from a real `ExportReceipt` by `'exportId' in answer` (the view type
  carries no such member). New `pollExportReceipt(api, request, onReceipt,
  options?)` reads `getExportReceipt` in a loop, calling `onReceipt` with
  EVERY read (queued/running included) and stopping at a terminal `jobState`
  (ready/failed/expired) or `maxAttempts`; default interval 1500ms / 40
  attempts, both overridable (a test passes small values).
- `export/ExportButton.tsx` -- `handleSubmit`'s `.then()` branches on
  `outcome.receipt === null`: when true, starts `pollExportReceipt` with an
  `ExportReceiptRequest` built from the same tenant/scope/revision/selectedTenant
  the submit used and the polled `exportId`, storing every read through the
  EXISTING `receiptForFlow`/`flowReceipt` path -- `ReceiptPanel`'s unedited
  `envelopeFromReceipt` already renders queued/running/ready/failed/expired
  from a bare receipt, so no change was needed there. `ReceiptPanel.tsx` is
  NOT edited by this cell.
- No backend change, no route added, matching the cell text.

## Verification

- `iv-e-67.queued-export-poll.test.tsx` (IVE67-AC1): a `recordingTransport` +
  real `LiveClient` (no server, no browser -- `fe-s-31/submit.test.ts`'s own
  discipline) proves (a) the literal W18 data-less QUEUED body is accepted
  and yields the `exr_` id (both through `client.submitExport` directly and
  through `submitUnderGate`'s unwrap); (d-ii) the same shape with `state:
  READY` is refused `EnvelopeMismatch('data')`, through both the client and
  `parseIrEnvelope` directly (control); (d-i) a submit answered WITH `data`
  still returns the receipt whole, carrying no `exportId` member (control).
  `pollExportReceipt`, fed real parsed `export-receipt` envelopes through the
  same parser, proves (b) three reads (queued/running/ready) all carrying
  `selectedTenant`, stopping at READY with a tenant-carrying download link
  (`receiptForFlow` + `downloadRouteFor`, byte-identical calls to what
  `ExportButton`/`ReceiptPanel` make), and (c) two reads (queued/failed)
  stopping at FAILED. A source-inspection check (the same instrument
  `fe-s-31`/`iv-e-64` use) confirms `ExportButton.tsx` itself calls
  `pollExportReceipt(...)` on the queued outcome. `VERDICT:
  QUEUED-EXPORT-POLL-OK`; 1 pass / 0 fail, 1 expect() call.
- `bun run typecheck` (`tsc -b --noEmit`, full portal): 0 errors (see ripple
  note below for what this required).
- No-regression sweep: `bun test` on `fe-s-31/submit.test.ts`,
  `fe-s-75/parse-control.test.ts`, both `iv-e-26.*` files, `fe-s-1/adapter.test.ts`,
  the full `fe-s-9/` and `fe-s-16/mounted-states.test.ts`, `fe-s-35/no-identity.test.ts`,
  `iv-e-64.submit-tenant.test.tsx`, `iv-e-53.tenant-thread.test.tsx`,
  `iv-e-53.preview-tenant.test.ts`, `iv-e-36.preview-account-scope.test.ts`,
  `iv-e-26.print-url.test.ts`, and the full `fe-s-13/` folder -- 90+ pass,
  0 fail across all of the above, byte-identical console output to before this
  cell's edits (re-ran fe-s-31 and iv-e-64 again after the ripple fix below).

## Ripple this cell's own widening required (row DSGN_IRPTV1-W41-S1)

Widening `SubmitOutcome` with a `submitted: true, receipt: null` arm merges,
under a bare `if (outcome.submitted)` check, with the pre-existing `submitted:
true, receipt: ExportReceipt` arm (TypeScript narrows on the checked
discriminant only) -- so `.receipt` reads TypeScript as `ExportReceipt | null`
everywhere `SubmitOutcome` is consumed, not only at the one pinned test the
REPORT note anticipated. `bun run typecheck` caught two: `fe-s-31/submit.test.ts:102`
and `iv-e-64.submit-tenant.test.tsx:147,175`. Each gained a one-line
`&& outcome.receipt` guard beside its existing `outcome.submitted` check --
no assertion's meaning changed (neither fake ever answers the queued shape),
and both files' `bun test` output is byte-identical before and after. Filed
as `DSGN_IRPTV1-W41-S1` (OBSERVATION, INERT, disarmed same-turn by the fix
itself).

## Out-of-grant observation (not a surprise for this cell)

Same condition IV-e-64's own session log recorded: `git status --porcelain`
shows ~24 files under `contracts/wire/` as modified (CRLF/LF normalization
noise only -- every `git diff` on them is byte-empty); left untouched and
unstaged. The commit for this cell stages only the seven files its grant and
build actually touch.
