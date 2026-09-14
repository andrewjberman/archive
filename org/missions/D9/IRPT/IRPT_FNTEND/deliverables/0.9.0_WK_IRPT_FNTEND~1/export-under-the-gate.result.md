# IRPT_FNTEND.TO-FE-s-31 -- the export gates on the report, and says what the report is on every page (amendment 2)

Worker `0.9.0_WK_IRPT_FNTEND~1`. Worktree pair `/c/tmp/wk-irpt_fntend-5-1-fe-s-31`.

- The workspace branch carries amendment 2 @7a186aeb96.
- The portal branch carries the issuer's merges 364dc0d1 (DEV e85498be) and 7c5303fa (DEV ca8524a1: FE-s-34 and
  FE-s-32).
- Portal commits, all LOCAL (the portal is frozen): **1f7d84b2** (the cut), **02f9f938** (amendment 1),
  **51518c8e** (amendment 2).
- The proof instance, `IRPT_FNTEND.TO-FE-s-31.export-under-the-gate.proof_of_spec.json`, sits beside this file.

**Every mechanical criterion PASSES by output, and the proof validates with the eleven ids.** `<status>` is flipped
to complete in the same commit as this file.

## Amendment 2 -- W2-S12 / W3-S5 closed (rows W1-S58, W1-S62)

The patch measured under row W1-S62, applied to exactly the four granted regions of
`src/api/endpoints/investor-reporting.ts`:

| region | change |
|---|---|
| the interface | `submitExport(req): Promise<ExportReceipt>` |
| `LiveClient.submitExport` | takes the envelope's `data`, through `adaptExportReceipt`, not the `status` ack |
| `IR_FIXTURE_PLAN['submit-export']` | `{ contract: 'ExportReceipt', shape: 'one' }` |
| `FixtureAdapter.submitExport` | serves the receipt on submit-export's own route |

Consumers:

- **`export/submit.ts`.** `submitExport` returns `Promise<ExportReceipt>`, and `SubmitOutcome` carries `receipt`.
- **`export/ExportButton.tsx`.**
  - The receipt the submit returns goes straight to the flow.
  - The follow-up `export-receipt` read of the browser's own composed `bundleRef` is gone.
  - The unused `flowAcked` import is gone.

## Every test assertion changed

`__tests__/fe-s-16/mounted-states.test.ts`, W2-S12 only, each change cited `// W2-S12`:

1. **`statusFromWire` (`:79-87`) -- a helper, no assertion.**
   - It now returns `adaptStatusEnvelope(readWireInstance<StatusEnvelopeWire>(fileName))`. That is the ack, read
     from the status carrier through the adapter `parseIrEnvelope` applies to an envelope's `status`.
   - It used to return `FixtureAdapter.submitExport(...)` over the status fixture.
   - Imports added: `adaptStatusEnvelope` and `StatusEnvelopeWire`.
   - New helper `receiptFromSubmit`: what `submitExport` returns now.
2. **F16-AC2, "five wire-fixture states render on the mounted body" (the use at `:148`). ADDED:**
   - `expect(submittedFailed.jobState).toBe('failed')` -- the submit returns the RECEIPT;
   - `expect(failedStatus.publicReasonCode).toBe(failedAckCode)` -- the ack's code is the status wire's.

   Printed:
   `W2-S12 BOTH WAYS (F16-AC2): submitExport -> receipt EXP-FE16-1 jobState=failed; ack from the status carrier -> publicReasonCode=IR-EXPORT-RENDER-REJECTED (wire IR-EXPORT-RENDER-REJECTED)`.
3. **"a FAILED receipt preserves the submitted request" (the use at `:262`). ADDED:**
   - `expect(submittedFailed.exportRef).toBe(failed.exportRef)`.

   Printed: `W2-S12 BOTH WAYS (after failure): submitExport -> receipt EXP-FE16-1 jobState=failed (receipt read EXP-FE16-1); ack from the status carrier -> publicReasonCode=IR-EXPORT-RENDER-REJECTED`.
4. **No existing assertion in that file was modified or removed.**
   - F16-AC2's `data-reason-code="${failedStatus.publicReasonCode}"` check is textually unchanged. It now reads the
     ack's real code. With the round-1 helper under the receipt contract it would have read `undefined`, which was
     row W1-S62's measured failure.

`__tests__/fe-s-31/submit.test.ts` (this cell's own), for F31-AC8:

5. The arm is `test(...)`, no longer `test.failing(...)`. Its `expect(isReceipt).toBe(true)` is unchanged, and it
   now passes.
6. ADDED control: `expect(parsed.status?.producerState).toBe('QUEUED')`. The same envelope's ack is read from the
   parsed `status`.
7. Removed: the `BLOCKED:` console line.
8. F31-AC7's positive control now also prints the receipt in the outcome. No assertion changed.

## Criteria -- deciding runs, and which way the server was

`IRPT_FE_DEV_PORT` was exported on every run:
- 5237 while this worker's server was up (`vite.worktree.config.mjs`);
- 5237 again after it was killed and measured ECONNREFUSED;
- 5238, measured ECONNREFUSED, for the whole-suite run.

| id | deciding line | server |
|---|---|---|
| F31-AC1 | `rc=0` on 51518c8e | n/a |
| F31-AC2 | `EVERY PAGE CARRIES STATE, REASON AND business_date: 10 of 10 pages` | up (not read) |
| F31-AC3 | `ABSENT SCOPE COUNT RENDERS: unavailable, never 0` | up (not read) |
| F31-AC4 | `REPORT SCOPE AND BUNDLE SCOPE AGREE: yes (2 / 2 renders ...)` | up (not read) |
| F31-AC5 | `ONE PREDICATE: Preview and PrintEntry read state/availability` | up (not read) |
| F31-AC6 | `PRINT UNDER THE GATE, IN A BROWSER: 2 of 2` | **UP**, 5237 |
| F31-AC7 | `NO-ANSWER REPORT: EXPORT NOT SUBMITTED` | up (not read) |
| F31-AC8 | `SUBMIT RETURNS THE EXPORT RECEIPT: yes` (exportRef=EXP-1, jobState=ready) | up (not read) |
| F31-AC9 | `76 pass / 0 fail` across 21 files | **UP**; also **DOWN**: 74 pass / 2 skip / 0 fail |
| F31-AC10 | RECORDED for L9 (judgment) | captures from AC6's run |
| F31-AC11 | `PAGE 3 BUNDLE ROWS AGREE WITH THE REPORT: yes (3 / 3 renders)` | up (not read) |

**The whole InvestorReporting suite, once, with the patch applied:** `IRPT_FE_DEV_PORT=5238` (measured closed),
**523 pass / 13 skip / 0 fail across 94 files**. That includes fe-s-1's call log, which row W1-S62 had seen fail
under the in-region route. There was no failure outside the grant, so there is no BLOCKING row.

## The earlier amendments (still in force)

- **Page 3 (rulings H and J, row W1-S60).** The row is "Bundle envelope (not the report)", naming the report's state
  beside it, and both scope rows print one count. See F31-AC11.
- **Row W1-S61 re-run.** The committed frozen map, as committed, renders a 3-page READY document in the print route.
  Its header reads "2 account(s) in scope", above the A-0001/A-0002 table.
- **The vite override is `vite.worktree.config.mjs` (row W1-S59).** It wrote `<WS>/.scratch/vite-cache-fe-s-31`,
  and the main checkout's `node_modules/.vite` was untouched.

## Controls

- **AC5.** A bundle-envelope copy is refused.
- **AC4.** The round-4 rule reads 0 against a 2-account table.
- **AC2.** A READY report reads complete.
- **AC7.** PARTIAL issues 1 request, and the outcome carries the receipt.
- **AC11.** The READY scan fires on a READY report's page 3.
- **AC8.**
  - The ack survives in the parsed status (`producerState=QUEUED`).
  - The identical arm read "no" at 02f9f938, with the client reverted, and "yes" at 51518c8e.

## Rows (INVESTIGATION_v2.md)

No new row this pass. W1-S58 to W1-S62 stand as filed. W1-S58 and W1-S62 are answered by amendment 2 and closed in
portal 51518c8e. Their disposition is the adjudicator's.

## proof-of-spec-check

Run from `<WS>` with the eleven ids, on the instance before the commit (portal checkout @51518c8e).

**`VALID (rc=0)`**, 0 violations across 11 acceptance rows. Every limb ran in ENFORCE mode:

| limb | result |
|---|---|
| invocation alignment | 10/10 comparable rows match the amended order |
| count-bar | 0 contradicting counts |
| drives | F31-AC6 and F31-AC8 read clean, 0 seeded |
| surprises | 5/5 row ids resolve |

Every mechanical criterion passes by output, so `<status>` is flipped to complete in this commit.

The dev server was killed before the final report: 5237 read ECONNREFUSED.
