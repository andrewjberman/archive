# IRPT_FNTEND.TO-FE-s-31 -- the export gates on the report, and says what the report is on every page (amended)

Worker `0.9.0_WK_IRPT_FNTEND~1`. Worktree pair `/c/tmp/wk-irpt_fntend-5-1-fe-s-31`: the workspace branch carries the
amendment @261a0c923f; the portal branch carries the issuer's merge 364dc0d1 (portal DEV e85498be). Portal commits
**1f7d84b2** (the cut) and **02f9f938** (the amendment), both LOCAL; the portal is frozen. The proof instance,
`IRPT_FNTEND.TO-FE-s-31.export-under-the-gate.proof_of_spec.json`, sits beside this file.

**The order stays OPEN: F31-AC8 FAILs, refused as written.** The amendment granted the client file; the fix was made
and measured, and it returns the receipt. It also turns F31-AC1 red in a test outside the grant, so it is not
shipped. See row IRPT_FNTEND-W1-S62 and the section "W2-S12" below. The order's `<status>` is not flipped.

## What changed

Cut, portal 1f7d84b2:

- **`render/Page.tsx`.** `PageSheet` takes a REQUIRED `reportState` band: the report's state, its reason and its
  `business_date` (FE-s-30's `businessDateOf`). A report that is not complete carries "Qualified -- not a complete
  report" on every page.
- **`render/PrintEntry.tsx`, `export/Preview.tsx`.** Both call `isAnswerBearing(report.availability)` over the
  resolved REPORT. A no-answer report produces no document, and the refusal is displayed.
- **`render/performance/PerformanceDocument.tsx`.** Ruling J's header count: an empty list is never printed as a
  count.
- **`render/analysis/AnalysisDocument.tsx`.** The band on all 3 pages.
- **`export/submit.ts`, `export/ExportButton.tsx`.** `exportGateFor` + `submitUnderGate`: a no-answer report
  issues no submit request, and the control withholds submit and says why.

Amendment, portal 02f9f938:

- **`render/performance/MethodsAndSources.tsx` (rulings H and J on page 3, row W1-S60).**
  - "Bundle availability" is now "Bundle envelope (not the report)". It reads *"the export bundle's own envelope
    reads READY -- a statement about the bundle object, NOT the report's state. The report is Partial (Report
    availability, above)."*
  - The value stays on the page, because fe-s-4's fields battery requires every scalar leaf of the bundle.
  - Report scope and Bundle scope print ONE count (`scopeCountOf`), and an absent list prints "Account count
    unavailable".
- **`render/Page.tsx`.** `scopeCountOf` moved here from PerformanceDocument, so the header and page 3 share it
  without an import cycle.
- **`__tests__/fe-s-31/`.**
  - F31-AC11 is added.
  - The row W1-S61 re-run is added to the browser test, outside AC6's denominator.
  - The driver now reads page 3's rows.
  - The AC8 arm stays `test.failing`.
  - `stripTags` now leaves a space where each tag was. AC11's READY control caught it gluing a label to its value
    and hiding READY from the scan.
- **`export/submit.ts`.** The header now states the W1-S62 measurement.
- **`api/endpoints/investor-reporting.ts`.** Changed, measured, reverted: **0 diff lines**.

## Criteria -- deciding runs, and which way the server was

Every `bun test` run exported `IRPT_FE_DEV_PORT=5237`. While the server was up, that was this worker's own server,
launched through `vite.worktree.config.mjs`. While it was down, 5237 had been measured ECONNREFUSED first.

| id | deciding line | server |
|---|---|---|
| F31-AC1 | `rc=0` on 02f9f938 | n/a |
| F31-AC2 | `EVERY PAGE CARRIES STATE, REASON AND business_date: 10 of 10 pages` | up (not read) |
| F31-AC3 | `ABSENT SCOPE COUNT RENDERS: unavailable, never 0` | up (not read) |
| F31-AC4 | `REPORT SCOPE AND BUNDLE SCOPE AGREE: yes (2 / 2 renders: header count = account table)` | up (not read) |
| F31-AC5 | `ONE PREDICATE: Preview and PrintEntry read state/availability` | up (not read) |
| F31-AC6 | `PRINT UNDER THE GATE, IN A BROWSER: 2 of 2` | **UP**, 5237 |
| F31-AC7 | `NO-ANSWER REPORT: EXPORT NOT SUBMITTED` | up (not read) |
| F31-AC8 | `SUBMIT RETURNS THE EXPORT RECEIPT: no` -> **FAIL** (W1-S58, W1-S62) | up (not read) |
| F31-AC9 | `76 pass / 0 fail` across 21 files | **UP**; also **DOWN**: 74 pass / 2 skip / 0 fail |
| F31-AC10 | RECORDED for L9 (judgment) | captures from AC6's run |
| F31-AC11 | `PAGE 3 BUNDLE ROWS AGREE WITH THE REPORT: yes (3 / 3 renders)` | up (not read) |

## Row W1-S61 re-run: does the frozen print now render? YES

The committed frozen map was served EXACTLY AS COMMITTED through the print route in Edge. It now carries FE-s-33's
READY status, and the print route renders a **3-page document**. Every page carries:

- the band, reading "Report state: Ready";
- the complete presentation, with no qualifier;
- business date 2026-09-09, from the status;
- reason `REQUESTED_WINDOW_ANSWERED`;
- the header "2 account(s) in scope", above the table of A-0001 and A-0002.

The last point is C-S68's disarm reading. The capture is `fe-s-31_print_frozen-as-committed_1440.png`.

## W2-S12 / W3-S5 -- the granted fix, measured, and why it is not shipped (row W1-S62)

**What was applied.** The three regions the amendment names:

- the interface, returning `Promise<ExportReceipt>`;
- `LiveClient.submitExport`, now taking `data` through `adaptExportReceipt`;
- `FixtureAdapter.submitExport`.

**The in-region FixtureAdapter route.** `IR_FIXTURE_PLAN['submit-export']` (`:1178`) names `StatusEnvelope`, and that
line is outside the three regions. So the only in-region way to serve a receipt is `serve('export-receipt')`.

**Result with the fix applied:**

- F31-AC8: `SUBMIT RETURNS THE EXPORT RECEIPT: yes`.
- `tsc -b --noEmit`: rc=2 at `__tests__/fe-s-16/mounted-states.test.ts(82,3)`, TS2740. `statusFromWire` is typed
  `Promise<StatusEnvelope>`, returns `adapter.submitExport(...)` over a STATUS wire fixture, and uses the result as
  the ack at `:148` and `:262`.
- Runtime failures:
  - fe-s-16 F16-AC2 (`:201`), with `data-reason-code="undefined"`;
  - fe-s-1's call log (`:137`), with `export-receipt` in submit-export's slot.

**For it to land,** a grant must also cover:

1. `__tests__/fe-s-16/mounted-states.test.ts:79-87`, plus its uses at `:148` and `:262`;
2. `IR_FIXTURE_PLAN['submit-export']` (`investor-reporting.ts:1178`), so FixtureAdapter serves its own route.

The measured patch:

```diff
@@ interface InvestorReportingApi
-  submitExport(req: SubmitExportRequest): Promise<StatusEnvelope>
+  submitExport(req: SubmitExportRequest): Promise<ExportReceipt>
@@ LiveClient.submitExport
-  submitExport(req: SubmitExportRequest): Promise<StatusEnvelope> {
+  submitExport(req: SubmitExportRequest): Promise<ExportReceipt> {
-    return this.send<StatusEnvelopeWire, StatusEnvelope>(
+    return this.send<ExportReceiptWire, ExportReceipt>(
       'submit-export',
       { body },
-      adaptStatusEnvelope,
+      adaptExportReceipt,
       req.scopeFingerprint,
       req.revision,
-      'status',
     )
@@ FixtureAdapter.submitExport
-  submitExport(req: SubmitExportRequest): Promise<StatusEnvelope> {
-    return this.serve('submit-export', req.scopeFingerprint, req.revision)
+  submitExport(req: SubmitExportRequest): Promise<ExportReceipt> {
+    return this.serve('export-receipt', ...)   // or serve('submit-export') once :1178 names ExportReceipt
```

`export/submit.ts`'s wrapper then returns `Promise<ExportReceipt>`. `ExportButton` sets the receipt from the submit
directly and drops the `export-receipt` follow-up. The AC8 arm becomes an ordinary `test`.

## Controls

- **AC5.** A PrintEntry copy gated on `bundle.availability` is refused.
- **AC4.** The round-4 rule on the same bundle reads 0 against a 2-account table.
- **AC2.** A READY report reads complete on 3 / 3 pages.
- **AC7.** A PARTIAL report opens the gate and issues 1 request.
- **AC11.** A READY report's page 3 is found by the same READY scan. Its first run read "no", which exposed the
  gluing defect in `stripTags`; that was fixed before the deciding run.
- **Live change.** The client fix was applied, measured and reverted.

## Rows (INVESTIGATION_v2.md)

- **W1-S58 -- BLOCKING, INERT.** `LiveClient.submitExport` drops the receipt.
- **W1-S59 -- OBSERVATION, INERT.** The `.ts` vite override breaks `tsc -b`, so it ships as `.mjs`, which is now
  the name the amended bound uses.
- **W1-S60 -- OBSERVATION, INERT.** Page 3's bundle rows. Granted by the amendment and fixed; see F31-AC11.
- **W1-S61 -- OBSERVATION, INERT.** The frozen print was refused. After FE-s-33 it renders; see the re-run above.
- **W1-S62 -- BLOCKING, INERT (new, W1 plane max was S61 at mint).** The granted W2-S12 fix breaks F31-AC1 and
  F31-AC9 outside the grant.

## For the issuer to amend

1. **Grant `__tests__/fe-s-16/mounted-states.test.ts`** (`statusFromWire`, `:79-87`, and its uses at `:148` and
   `:262`) **and `investor-reporting.ts:1178`** (`IR_FIXTURE_PLAN['submit-export']`, FE-s-34's region), with the
   three regions already granted. The patch above then lands with AC1, AC8 and AC9 all green.

## proof-of-spec-check

Run from `<WS>` with the eleven ids, on the instance before the commit (portal checkout @02f9f938).

**`VALID (rc=0)`**, 0 violations across 11 acceptance rows. Every limb ran in ENFORCE mode:

| limb | result |
|---|---|
| invocation alignment | 10/10 comparable rows match the amended order |
| count-bar | 0 contradicting counts |
| drives | F31-AC6 read clean, 0 seeded |
| surprises | 5/5 row ids resolve |

A VALID instance is not a met order. F31-AC8 is FAIL, so `<status>` is NOT flipped to complete.

The dev server was killed before the final report: 5237 read ECONNREFUSED.
