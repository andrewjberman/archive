# IRPT_FNTEND.TO-FE-s-16 -- result

**Worker:** `0.9.0_WK_IRPT_FNTEND~3` (slot ~3, queue position 1) · **Cell:** `FE-s-16` (round 2, decomp v0.2 @430c5fcb4a)
**Worktree pair:** `/c/tmp/wk-irpt_fntend-2-6-fe-s-16` (workspace, branch `wk-irpt_fntend-2-6-fe-s-16` from CLOUD @7d6db9bcfa) and
`/c/tmp/wk-irpt_fntend-2-6-fe-s-16/portal` (portal, same branch name, from DEV @84a86c10).
**Portal commits:** this worker's own `7f26d9a5ebdab8b2b6fd7700459ab0f7bcd27f74`, and the branch now carries the issuer's merge of DEV at `f8af907a` (the bytes every criterion below was finally measured on). Both **LOCAL** on the worker branch, never pushed (portal is FROZEN by Andrew-direct).
**Proof instance:** `IRPT_FNTEND.TO-FE-s-16.export-flow-mounted-narrative.proof_of_spec.json` -- `proof-of-spec-check.py` **rc=0 (VALID)** over the ten ids.

> **THE ORDER IS COMPLETE AND ITS `<status>` IS FLIPPED, in the same commit as the instance.** All nine
> mechanical criteria PASS by output **on the merged bytes** (portal `f8af907a`); `F16-AC10` is RECORDED
> with no verdict, for `3.0.0_SA_CVO` at L9.
>
> **THIS TOOK THREE ROUNDS, AND TWO OF THEM WERE REFUSALS THAT THE ISSUER ANSWERED.** Round 1: built and
> measured; `F16-AC8` refused as written and `F16-AC9` blocked, both recorded FAIL with their measurements
> and neither repaired by this worker. Round 2: the issuer re-cut `F16-AC8`'s invocation on this worker's
> positive control (row `IRPT_FNTEND-S25`) and it passed. Round 3 (below): the issuer drained FE-s-15 and
> merged DEV into this branch, and **every mechanical criterion was re-measured on those bytes** -- because
> a criterion's pass is only true at the bytes it was measured on.
>
> **MERGED-BASE ROUND (issuer `2.0.0_SA_COO~F`; portal DEV `d2962a69` merged into this branch at
> `f8af907a`).** `F16-AC1`..`F16-AC9` all re-run; no prior output carried forward. `F16-AC9` now reads
> **406 pass / 1 skip / 0 fail across 407 tests** -- this worker's own independent measurement, which
> AGREES with the issuer's reported figure, so no disagreement row is owed. `F16-AC3`'s denominator moved
> **38 -> 40** scanned files (the merge added `RevisionIdentity.tsx` and `NativeSections.tsx`) and the scan
> stays clean over the wider set. The three captures were re-taken and are **byte-identical** to the
> committed images -- itself the measurement that the merge changed nothing on those surfaces. Mutant and
> determinism controls re-run on the merged bytes.
>
> **AMENDMENT ROUND (issuer `2.0.0_SA_COO~F`, CLOUD `c8d51d0d1c` LOCAL, row `IRPT_FNTEND-S25`).** This worker's
> F16-AC8 refusal was answered by the issuer: the invocation's URL was re-cut with the scope segments this
> worker's control run had proven (`&narrative=1&tenant=F-49F&scope=fp-49f-0824&revision=rev-49f-000091`), the
> BAR unchanged at `REFS RESOLVED: 1 of 1`. Re-run under the amended invocation: **`REFS RESOLVED: 1 of 1`
> (twice), 2 of 2 fixture keys matched, rc=0 -- F16-AC8 now PASSES by output**, and the capture it wrote is now
> the criterion's real PNG. No source file changed in that round, so **F16-AC1 was NOT re-run** (the issuer's
> own instruction: skip it if the only change is the capture). Row `IRPT_FNTEND-W3-S9` stands as filed --
> a row is never edited -- and the issuer's `IRPT_FNTEND-S25` is its answer.

## Criteria

| id | status | deciding output | denominator |
|---|---|---|---|
| F16-AC1 | **PASS** | `rc=0` (tsc -b --noEmit) | 1 of 1 typecheck project, 0 diagnostics, over the merged tree |
| F16-AC2 | **PASS** | `STATES RENDERED: 5 of 5` | 5 of 5 wire-fixture states; 5 of 5 tests in the file |
| F16-AC3 | **PASS** | `0 fail`, `SCANNED: 40 files` | 40 .tsx files (38 before the merge), 0 violations, 4 of 4 tests |
| F16-AC4 | **PASS** | `MARKERS: 2` | 2 of 2 events; 2 of 2 quoted citations resolve in a list of 3; 0 of 5 causal words |
| F16-AC5 | **PASS** | `MISSING HISTORY: rendered naming 2026-05-01` | 3 of 3 files scanned: 0 placeholder hits, 0 `historyCutoff` hits, control 16 |
| F16-AC6 | **PASS** | `CLICKED: Export` (1440) | 1 of 1 capture; 2 of 3 fixture keys matched; 0 update-depth warnings |
| F16-AC7 | **PASS** | `CLICKED: Export` (390) | 1 of 1 capture; same accounting |
| F16-AC8 | **PASS** (amended invocation) | `CONSOLE[log]: REFS RESOLVED: 1 of 1` (twice), rc=0 | 1 of 1 refs resolved; 2 of 2 fixture keys matched |
| F16-AC9 | **PASS** (merged bytes) | `406 pass, 1 skip, 0 fail` | 406 of 407 across 67 files; my own measurement, agreeing with the issuer's |
| F16-AC10 | **RECORDED (judgment)** | four captures on disk, all byte-identical after the merge | no verdict taken; `3.0.0_SA_CVO` grades at L9 |

## F16-AC8: refused as written, then answered by the issuer and met

**AS FIRST CUT (round 1 of this order, recorded FAIL).** The invocation's route was
`investor-reporting/print?bundle=fe-s-16-narrative`, which names no `?scope=`. The declared performance route binds
that value as a PATH parameter (`GET /api/scoped/investor-reporting/performance/{accountSetId}`, `accountSetId =
req.scopeFingerprint`), and `irBuildRequest` throws `IrKeyError: route ... needs path parameter 'accountSetId'`
**before any request is issued**; `resolveOne` wraps it as `MissingPayloadError`, and `resolveBundle`'s
`REFS RESOLVED` line -- printed AFTER the resolution loop -- never runs. The as-written run rendered the refusal panel
and reported BOTH fixture keys `FIXTURE-DEAD`. **Control on the same instrument, same fixtures, same page**, with
`&narrative=1&tenant=F-49F&scope=fp-49f-0824&revision=rev-49f-000091` added: `REFS RESOLVED: 1 of 1` twice, 2 of 2
fixtures matched, and the narrative page renders (page 2 of 4) with its two dated markers. `render/PrintEntry.tsx`
(which reads `?scope=`) is outside this order's grant, and the invocation was the cut's -- so the criterion was
**refused, not repaired**. Row `IRPT_FNTEND-W3-S9` (BLOCKING, ARMED, disarm owner `2.0.0_SA_COO~F`).

**AS AMENDED (issuer `2.0.0_SA_COO~F`, CLOUD `c8d51d0d1c`, row `IRPT_FNTEND-S25`) -- MET.** The issuer folded this
worker's proven control parameters into the invocation and left the bar untouched. The URL cut predated FE-s-14,
which made the scope fingerprint a PATH parameter (the issuer cites row `IRPT_FNTEND-W2-S13`, one cell earlier).
Re-run exactly as amended: `CONSOLE[log]: REFS RESOLVED: 1 of 1` twice, `FIXTURES: 2 declared; 2 matched >=1 URL`
(no `FIXTURE-DEAD`), rc=0. `LOC ... DID NOT LAND` still prints and is expected -- the criterion names it and says
the resolver line is the bar. **No source file changed in this round** (`git status --porcelain` in the portal
worktree: empty), so **F16-AC1 was not re-run**; the only artifact that moved is the capture.

## F16-AC9: blocked on six failures outside the grant, then met on the merged bytes

**AS FIRST MEASURED (round 1, recorded FAIL).** `384 pass / 1 skip / 6 fail`. The six are exactly the six
this order's own worker face names as pre-existing at the branch cut (376 pass / 1 skip / 6 fail there): `fe-s-13`
(`producer-fixtures.test.ts` x2, `routes.test.ts` x2), `fe-s-14` (`envelope.test.ts`) and `fe-s-1`
(`fixtures.test.ts`, which reads ONLY `fixtures/smoke/default.json`, so the fixtures this order added cannot touch
it). None of those three directories is in `<paths>`. This order added 8 tests, all passing, and moved no failure.
Row `IRPT_FNTEND-W3-S10` (BLOCKING, ARMED, disarm owner `2.0.0_SA_COO~F`), citing `IRPT_FNTEND-S23`.

**AS RE-MEASURED ON THE MERGED BYTES -- MET.** The issuer drained FE-s-15 (portal DEV `d2962a69`, carrying the
v1 re-pin) and merged DEV into this branch at `f8af907a`. Re-run there: **`406 pass / 1 skip / 0 fail` across 407
tests in 67 files, bun exit status 0, zero `error:` lines**. The six failures were the stale v1 pin and are gone at
this vintage. This is this worker's own measurement and it agrees with the issuer's independently reported
406 / 1 / 0, so **no disagreement row is owed**. Row `IRPT_FNTEND-W3-S10` stands as filed; its disposition is the
issuer's.

## What was built

**The export flow is mounted.** `export/AppliedBranding.tsx` and `export/ReceiptPanel.tsx` -- exported at FE-s-9 and
imported by nothing -- now render inside `ExportModal`'s dark `Panel`, on a light card that makes their canvas-legal
text legible where they mount (the colour law holds by the Panel anchor either way; F16-AC3 clean).
`ExportButton` composes the wire `ExportBundle` the export submits, reads it BACK through the FE-s-13 adapter so the
applied-branding statement is what `approved_assets` carries, submits through `submit-export` and follows with
`export-receipt`; `job_state`, `download_route`, the timestamps and the validation facts all come from the wire
receipt through the adapter, and the download is followed from the receipt's own route -- the `export-download`
operation is never named. Five states proven from wire fixtures: no-assets (label `Opal` even when Advisor was
requested), approved-assets (`Co-branded` with the asset ref shown), running (no link), failed (the public reason
code, and the submitted request preserved), ready (the receipt's `download_route` IS the rendered link).
A branding edit still bumps the export revision at the same source revision and re-fetches no performance report
(FE-s-9's control, re-run in this order's own test).

**`index.tsx`** passes the reporting tab's real report reference (one line, inside the reporting `ExportAnchorSlot`
block). While that reference was `[]`, a defect was invisible: the preview request was frozen in `useState` at mount,
so the modal rendered "carries no performanceReport" for the whole session. The request now follows the resolved
scope, and the 1440 capture shows the real performance document inside the modal.

**The narrative's meaning is the backend's.** `render/narrative/` reads `events`, `prose`, `performance_revision` and
`versions` off the adapted view packet and carries `cited_evidence` and `coverage` in the new
`render/narrative/wire.ts` under the adapter's own three verbs -- the FE-s-13 adapter exposes neither. A packet whose
coverage answers `MISSING_HISTORY` renders that state naming the earliest cited-evidence cutoff, with the packet's own
reason beside it; `historyCutoff` and the placeholder wording are gone from `render/narrative/` (0 hits, printed, with
a positive control).

## Surprise rows filed -- `IRPT_FNTEND-W3-S4` .. `-W3-S11`

| id | class / hazard | one line |
|---|---|---|
| W3-S4 | OBSERVATION / INERT | Headless v2's Dialog renders 225 bytes and no body under `renderToStaticMarkup`, and no DOM test environment is installed -- F16-AC2's named instrument cannot see the mount it requires; graded on the modal's own exported body plus a source assertion. |
| W3-S5 | OBSERVATION / INERT | v1's `submit-export` answers the receipt whole in `data`, but the typed client takes the `status` half and the adapter drops `operation_id` -- the minted export id reaches no consumer. |
| W3-S6 | OBSERVATION / INERT | the analysis slot's report ref is minted inside a file outside this grant; it references nothing rather than the wrong document. |
| W3-S7 | OBSERVATION / INERT | `adaptNarrativePacket` exposes neither `cited_evidence` nor `coverage`'s window; both carried in-grant, and the print path cannot receive them. |
| W3-S8 | OBSERVATION / INERT | v1's `coverage` object carries NO date (4 properties), so F16-AC5's "coverage's cutoff" is named from `cited_evidence[].cutoff_at`. |
| W3-S9 | **BLOCKING / ARMED** | F16-AC8 cannot pass as written -- the URL names no `?scope=`; the same command with the segments prints `REFS RESOLVED: 1 of 1`. **ANSWERED by the issuer amendment `IRPT_FNTEND-S25` (CLOUD `c8d51d0d1c`); the criterion now passes under the amended invocation. The row is left exactly as filed -- its disposition is the issuer's to move, not this worker's.** |
| W3-S10 | **BLOCKING / ARMED** | F16-AC9 reads 6 fail -- exactly the six pre-existing ones outside this grant. |
| W3-S11 | OBSERVATION / INERT | one `--click Export` opens the modal but submits nothing, so F16-AC6/AC7's captures show the receipt panel awaiting rather than READY. |

## Controls

- **MUTANT:** `historyDateFromEvidence`'s selection flipped from earliest to latest cutoff (byte copy taken first).
  F16-AC5's test failed at `narrative-wire.test.ts:120` (`Expected: true / Received: false`) while the other two tests
  in the file still passed; restored from the copy, 8 pass / 0 fail. **FIRED-AS-EXPECTED.**
- **DETERMINISM:** two back-to-back runs of the fe-s-16 folder diffed to exactly one line -- the wall clock.
  **STABLE.**

## Artifacts

Portal (all at `7f26d9a5`, LOCAL): `export/{ExportModal,ExportButton,ReceiptPanel,submit,resolveBundle}`,
`render/narrative/{wire.ts,compose.ts,PeriodInContextPage.tsx}`, `index.tsx` (1 line),
`__tests__/fe-s-16/` (2 tests + 9 wire fixtures), `fixtures/smoke/fe-s-16-{ready,print-narrative}.json`.
Workspace (this folder): the proof instance, this file, and four PNGs.

**WHICH CAPTURE IS WHICH** (they are four files, and two of them now show the same page):

| file | what it is |
|---|---|
| `fe-s-16_export_ready_1440.png` | F16-AC6's run, as written. |
| `fe-s-16_export_ready_390.png` | F16-AC7's run, as written. |
| `fe-s-16_print_narrative_1440.png` | **F16-AC8's run under the AMENDED invocation** -- the criterion's real capture, the four-page print document with the narrative page at 2 of 4. It REPLACED the refusal-panel capture the as-written invocation produced (that image is not kept; its measurement is quoted above and in row `IRPT_FNTEND-W3-S9`). |
| `fe-s-16_print_narrative_1440_CONTROL_with_scope_segments.png` | the POSITIVE CONTROL this worker ran to discriminate "the page is broken" from "the invocation names no scope", and the evidence the issuer amended on. Same URL as the amended invocation, so the image now matches the criterion's -- **kept deliberately**: it was taken BEFORE the amendment existed and is the record of how the refusal was grounded. |
