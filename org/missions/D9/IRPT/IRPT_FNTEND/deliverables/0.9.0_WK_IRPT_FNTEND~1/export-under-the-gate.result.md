# IRPT_FNTEND.TO-FE-s-31 -- the export gates on the report, and says what the report is on every page

Worker `0.9.0_WK_IRPT_FNTEND~1`. Worktree pair `/c/tmp/wk-irpt_fntend-5-1-fe-s-31`: the workspace base is CLOUD
@a2060c08b5, and the portal worktree (`.../portal`) is based on DEV @fd91bea1. Portal commit **1f7d84b2**, LOCAL
(the portal is frozen). The proof instance, `IRPT_FNTEND.TO-FE-s-31.export-under-the-gate.proof_of_spec.json`, sits
beside this file.

**The order stays OPEN: F31-AC8 FAILs.** It is blocked by the grant (BLOCKING row IRPT_FNTEND-W1-S58), and its
`<status>` is not flipped.

## What changed (portal 1f7d84b2)

- `render/Page.tsx`
  - `PageSheet` takes a **required** `reportState` band. The band shows the REPORT's state, its reason
    (`code -- text`, or "No reason stated") and its `business_date` (FE-s-30's `businessDateOf`: the status's
    date, else the document's, naming which).
  - `isCompleteState` decides the presentation. A report that is not complete carries "Qualified -- not a
    complete report" and a 2px accent rule on every page.
  - It also exports the shared `reportStateChrome` / `noAnswerWords` / `renderedReportOf`.
- `render/PrintEntry.tsx`, `export/Preview.tsx`
  - Both call `isAnswerBearing(report.availability)` over the RESOLVED REPORT, never over the composed bundle's
    own READY envelope.
  - A no-answer report produces no document, and the refusal is displayed.
  - Preview's `runPreview` is unchanged. Its new optional `onResolved` hands the report to ExportButton.
- `render/performance/PerformanceDocument.tsx`
  - `reportState` is passed on all 4 pages.
  - Ruling J: `scopeCountOf`. An empty account list is never printed as a count, and two scopes that name
    different sets print "unavailable".
- `render/analysis/AnalysisDocument.tsx`: `reportState` on all 3 pages.
- `export/submit.ts`
  - `exportGateFor` + `submitUnderGate`: a closed gate issues no request.
  - `submitExport` stays typed to the ack (W1-S58).
- `export/ExportButton.tsx`
  - The gate reads the preview's resolved report.
  - While the gate is closed the modal gets no `onSubmit`, and the reason is displayed.
- `__tests__/fe-s-31/`: `every-page.test.ts` (AC2-AC5), `print-in-a-browser.test.ts` + `print-driver.mjs` (AC6),
  `submit.test.ts` (AC7; AC8 as `test.failing`), `_scenarios.ts`, `ambient-shims.d.ts`,
  `vite.worktree.config.mjs`.

## Criteria -- deciding runs, and which way the server was

Every `bun test` run exported `IRPT_FE_DEV_PORT`. It pointed at 5237 (this worker's server) while the server was
up, and at 5237 after that port was measured ECONNREFUSED while it was down. Before the server existed, runs used
5238, also measured closed.

| id | deciding line | server |
|---|---|---|
| F31-AC1 | `rc=0` | n/a |
| F31-AC2 | `EVERY PAGE CARRIES STATE, REASON AND business_date: 10 of 10 pages` | up (not read) |
| F31-AC3 | `ABSENT SCOPE COUNT RENDERS: unavailable, never 0` | up (not read) |
| F31-AC4 | `REPORT SCOPE AND BUNDLE SCOPE AGREE: yes (2 / 2 renders: header count = account table)` | up (not read) |
| F31-AC5 | `ONE PREDICATE: Preview and PrintEntry read state/availability` | up (not read) |
| F31-AC6 | `PRINT UNDER THE GATE, IN A BROWSER: 2 of 2` | **UP**, 5237 |
| F31-AC7 | `NO-ANSWER REPORT: EXPORT NOT SUBMITTED` (4 / 4 states, 0 requests; PARTIAL control 1 request) | up (not read) |
| F31-AC8 | `SUBMIT RETURNS THE EXPORT RECEIPT: no` -> **FAIL** (W1-S58) | up (not read) |
| F31-AC9 | `74 pass / 0 fail` across 21 files | **UP**, 5237; also DOWN: 73 pass / 1 skip / 0 fail |
| F31-AC10 | RECORDED for L9 (judgment) | captures from AC6 |

- Baseline before any edit: the portal typechecked (rc=0), and fe-s-4/8/9/16 read 65 pass / 0 fail across 18
  files.
- No test in those four suites asserts the old chrome or the old gate, so there was no row to file for that.

## The dev server and the worktree-local cache

- **The launch:**
  `bun run dev --port 5237 --strictPort --config src/pages/InvestorReporting/__tests__/fe-s-31/vite.worktree.config.mjs`.
- **The override worked.** Vite wrote `<WS>/.scratch/vite-cache-fe-s-31/deps` at 02:00:57 local, and the main
  checkout's `node_modules/.vite/deps` kept its 00:56:58 mtime.
- **Why `.mjs` and not the `.ts` the amendment names (row W1-S59).** With the `.ts` present, `tsc -b --noEmit`
  failed rc=2 on two files nobody edited: the vite typings pulled `NodeJS.Timeout` into the app program.
- The server was killed before this report: 5237 read ECONNREFUSED.

## Controls

- **AC5.** A PrintEntry copy gated on `bundle.availability` is refused.
- **AC4.** The round-4 header rule on the same bundle reads "0 account(s) in scope", which disagrees with the
  2-account table.
- **AC2.** A READY report reads complete, with no qualifier, on 3 / 3 pages.
- **AC7.** A PARTIAL report opens the gate and issues exactly 1 request.

## Rows (INVESTIGATION_v2.md; W1 plane max was S57 across v1 + v2 at mint)

- **IRPT_FNTEND-W1-S58 -- BLOCKING, INERT.** F31-AC8 cannot be satisfied in the grant. `LiveClient.submitExport`
  (`api/endpoints/investor-reporting.ts`, not in `<paths>`) takes the `status` half and drops the receipt.
- **IRPT_FNTEND-W1-S59 -- OBSERVATION, INERT.** The amendment's `.ts` override file breaks `tsc -b`, so the same
  override ships as `.mjs`.
- **IRPT_FNTEND-W1-S60 -- OBSERVATION, INERT.** Page 3 (`MethodsAndSources.tsx`, outside the grant) still prints
  the composed bundle's "Bundle availability READY" and an empty bundle-scope line.
- **IRPT_FNTEND-W1-S61 -- OBSERVATION, INERT.** The committed frozen map carries no status, so the gated print
  route refuses it. C-S68's disarm needs a capture with a status carrier.

## For the issuer to amend

1. **W2-S12 / W3-S5 need `src/api/endpoints/investor-reporting.ts` in a grant.** `LiveClient.submitExport`
   (and the interface type) must take `data`. Then F31-AC8's `test.failing` turns red and is promoted to `test`.
2. **The BOUNDS launch line names `vite.worktree.config.ts`.** It should name the `.mjs`, or place the `.ts`
   outside `src/`.
3. **`MethodsAndSources.tsx`'s bundle rows (W1-S60)** are the remaining half of ruling J on page 3.

## proof-of-spec-check

Run from `<WS>` on the instance before the commit, with checker vintage 9e6ed6c236.

**`VALID (rc=0)`**, 0 violations across 10 acceptance rows. Every limb ran in ENFORCE mode:

| limb | result |
|---|---|
| invocation alignment | 9/9 comparable rows match the order |
| count-bar | 0 contradicting counts |
| drives | F31-AC6 read clean, 0 seeded |
| surprises | 4/4 row ids resolve |

A VALID instance is not a met order. F31-AC8 is FAIL, so `<status>` is NOT flipped to complete.
