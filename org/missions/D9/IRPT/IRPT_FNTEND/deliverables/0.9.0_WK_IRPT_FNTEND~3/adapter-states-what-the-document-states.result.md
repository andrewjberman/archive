# IRPT_FNTEND.TO-FE-s-39 -- the adapter never substitutes a value the document did not state

Worker `0.9.0_WK_IRPT_FNTEND~3`, slot ~3, round 6 wave B. Workspace worktree `C:/tmp/wk-irpt_fntend-6-3-fe-s-39`,
branch `wk-irpt_fntend-6-3-fe-s-39`, base 1f5d387e17. Portal worktree on the same branch name, base 741bb54b.

**Verdict:** the order stays **open**. Nine mechanical criteria: eight pass by output, and F39-AC9 fails because
one test outside the grant goes red (row W3-S27). F39-AC8's anchor line prints, but the same run exits rc=1 on
F32-AC5 (row W3-S28). F39-AC10 is a judgment row, recorded with no verdict.

## Commits (LOCAL; portal frozen)

- portal `794d4899a164f0f42f5cc08453572199b37b134f` on `wk-irpt_fntend-6-3-fe-s-39`, 7 files, +597 / -24.
- workspace: this result file, the proof instance and 5 surprise rows in `INVESTIGATION_v2.md`, in one commit.
  The order's `<status>` stays `pending`.

## Where each null rule is decided (one rule per plane, no second copy)

| plane | what null means | decided in | reads on the panel |
|---|---|---|---|
| WIRE (a status's `source_dates.business_date`, or a wire document's clocks) | a producer defect | `contracts/adapt.ts` `readingFromValue`: null -> fact `NULL`. Unchanged. Reached through `readSourceDate` and `wireEnvelope`. | `Source date malformed` (`state/status.ts` `formatSourceAgeForState`, unchanged) |
| VIEW (a view document's `sourceTimestamps.businessAsOf`) | "no clock", the `SourceTimestamps` contract's own definition | `contracts/adapt.ts` `carryDocumentReading`: hands a view null to the same `readingFromValue` as `undefined`, i.e. fact `ABSENT` | the absence: `No source age yet` on a no-answer state, `Source time unknown` on an answer-bearing one |

The builder is not copied. Only the view plane's input changes, at the one place a view document gets its reading.
F39-AC3 shows the wire half unchanged. F39-AC2's "both ways" line shows the wire rule would still name the same
null malformed.

## The advisory (RULING W, row W2-S29)

- `contracts/index.ts`: `OutOfEnumAdvisory { outOfEnum: string }` and `AdvisoryValue = AdvisoryPartition | OutOfEnumAdvisory`.
  `HoldingsClassification.advisory` is now `AdvisoryValue`. Nothing else in the file changed.
- `contracts/adapt.ts`, the Holdings use site: `advisoryFromWire`. An in-enum token is renamed through
  `ADVISORY_FOR_WIRE`, unchanged. An out-of-enum token becomes `{ outOfEnum: token }`. An absent token takes the
  field's explicit unknown. `ADVISORY_FOR_WIRE` is typed to its partition members.
- The Directory use site (`:558` at 741bb54b) is **not** changed. See row W3-S29.
- `tabs/holdings/slices.ts` + `SliceTable.tsx`: `isOutOfEnumAdvisory` reads the flag from the value's shape. The
  cell shows the token verbatim beside `(not a contract advisory value -- shown as sent)`, with
  `data-advisory-out-of-enum="true"`. An in-enum cell is byte-identical to before (F39-AC7).

## Criteria (deciding output lines; portal@794d4899)

| id | status | deciding line | denominator |
|---|---|---|---|
| F39-AC1 | PASS | `rc=0` | 1 of 1 typecheck |
| F39-AC2 | PASS | `VIEW DOCUMENT WITH A NULL businessAsOf -> ABSENCE NAMED, NOT MALFORMED: 3 of 3` | 3 of 3 nulls, of 4 view documents in fe-s-3-loading.json |
| F39-AC3 | PASS | `WIRE NULL business_date STILL READS MALFORMED: yes` | 2 of 2 wire arms |
| F39-AC4 | PASS | `businessDateOf PROVENANCE KEYS ON producerState: 2 of 2` | 2 of 2 |
| F39-AC5 | PASS | `F21 GRADES THE DOCUMENT'S BUSINESS DATE, NOT AN INSTANT: yes` | 5 of 5 answer-bearing states (2d, not the instant's 1d); 8 of 8 tests |
| F39-AC6 | PASS | `OUT-OF-ENUM ADVISORY ON A READY ANSWER -> VERBATIM AND FLAGGED: 3 of 3` | 3 of 3 rows; reader control 0 of 3 |
| F39-AC7 | PASS | `IN-ENUM ADVISORY UNCHANGED: yes` | 3 of 3 tokens x 3 cells, byte for byte |
| F39-AC8 | PASS (anchor), run rc=1 | `HOLDINGS UNDER THE GATE, IN A BROWSER: 4 of 4`; same run `6 pass / 1 fail` (F32-AC5, `CLAIMED FIELD PRESENT IN THE RENDERED DOM: 4 of 6`) | 4 of 4 scenarios at 390 and 1440 on this worker's server on 5263 |
| F39-AC9 | **FAIL** | `527 pass / 13 skip / 1 fail`, 541 tests across 95 files, rc=1 | baseline at 741bb54b: 523 / 13 / 0 of 536 across 94 |
| F39-AC10 | RECORDED (judgment) | see the proof instance | graded at L9 by 3.0.0_SA_CVO |

### The red tests (all outside the grant; none edited)

1. `__tests__/fe-s-34/no-status.test.ts` F34-AC9, "path 1 NULL". It serves a view document whose `businessAsOf`
   is null and requires `Source date malformed`, which is exactly what RULING V removes. It now reads
   `Ready -- Source time unknown` (0 of 2). Path 2 (wire) still reads malformed. **Row W3-S27, BLOCKING, ARMED.**
2. `__tests__/fe-s-32/holdings-in-a-browser.test.ts` F32-AC5. Its classification reader accepts only
   `advised/residual/unknown`, so the verbatim `ADVISORY` reads NOT FOUND on the observed and target captures.
   It is visible only with a dev server up; on a closed port it skips under ruling C, so F39-AC9 cannot see it.
   **Row W3-S28, BLOCKING, ARMED.**

## Controls

- Mutant m1 (view null rule reverted): F39-AC2 `0 of 3`, 1 fail. Mutant m2 (advisory rule reverted): F39-AC6
  `0 of 3`, 1 fail. The other arms stay green under each. Restored from a byte copy, and adapt.ts is clean
  against HEAD. FIRED-AS-EXPECTED.
- Determinism: two runs at HEAD differ only on the wall-clock line. STABLE.

## Dev server (F39-AC8)

Port 5263, measured closed first (`PROBE UNREACHABLE ECONNREFUSED`). Launched with
`bun run dev --port 5263 --strictPort --config src/pages/InvestorReporting/__tests__/fe-s-39/vite.worktree.config.mjs`,
which loads the portal config at runtime and merges only `cacheDir` = `<WS>/.scratch/vite-cache-fe-s-39`. Vite 7.3.5
reported ready, and the cache directory appeared under `.scratch/`. The probe read `HTTP 200`. The server was killed
after the run (taskkill, PIDs 28064 and 28416), and 5263 measured closed again. Every `bun test` exported
`IRPT_FE_DEV_PORT`: 5263 while the server was up, 5273 (measured closed) otherwise.

## Rows filed (INVESTIGATION_v2.md)

- IRPT_FNTEND-W3-S27 -- BLOCKING, ARMED (disarm 2.0.0_SA_COO~F): fe-s-34 F34-AC9 turned red by RULING V.
- IRPT_FNTEND-W3-S28 -- BLOCKING, ARMED (disarm 2.0.0_SA_COO~F): fe-s-32 F32-AC5 turned red by RULING W.
- IRPT_FNTEND-W3-S29 -- OBSERVATION, INERT: the Directory cohort use site is unchanged.
- IRPT_FNTEND-W3-S30 -- OBSERVATION, INERT: validate.ts:448 pins advisory to three values.
- IRPT_FNTEND-W3-S31 -- OBSERVATION, INERT: F39-AC8's run writes 9 files into `~2`'s deliverables folder, unstaged.
