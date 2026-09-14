# IRPT_FNTEND.TO-FE-s-39 -- the adapter never substitutes a value the document did not state

Worker `0.9.0_WK_IRPT_FNTEND~3`, slot ~3, round 6 wave B. Workspace worktree `C:/tmp/wk-irpt_fntend-6-3-fe-s-39`,
branch `wk-irpt_fntend-6-3-fe-s-39`. Two runs:
- the first on workspace 1f5d387e17 / portal 741bb54b;
- this one, under AMENDMENT 1, on workspace 0294183b65 / portal 20545436. That portal commit is the first run's
  794d4899 plus the FE-s-38 sync (DEV f55538e7).

**Verdict:** all nine mechanical criteria pass by output on the current tree:
- F39-AC8's run ends **7 pass / 0 fail**.
- The whole suite (F39-AC9) reads **532 pass / 14 skip / 0 fail** of 546.
- F39-AC10 is a judgment row, recorded with no verdict.

## Commits (LOCAL; portal frozen)

- portal `794d4899a164f0f42f5cc08453572199b37b134f`: the first run's code (RULINGS V and W), 7 files.
- portal `45d5c1de5b36a38214af302ce6a43716c0811fdd`: AMENDMENT 1's two tests, 2 files, +51 / -13.
- workspace: this file, the proof instance, row W3-S32 and the `<status>` flip, in one commit. The first run's
  commit 36c34b9017 carried the first instance and rows W3-S27..S31.

## AMENDMENT 1 -- the two tests, each for ONE purpose

1. **`__tests__/fe-s-34/no-status.test.ts`, F34-AC9 path 1 NULL (the VIEW plane) only. RULING V.**
   - The arm now expects an absence wording other than `SOURCE_DATE_MALFORMED`.
   - Path 2 NULL (the WIRE plane) is unchanged and still requires `SOURCE_DATE_MALFORMED`.
   - Both ways, printed on every run: path 1 NULL reads `Ready -- Source time unknown`. RULING V's rule accepts
     it and the removed rule rejects it. RULING V's rule rejects `Source date malformed`.
   - Mutant m4 reverts the view-null rule in adapt.ts. The arm then reads `Ready -- Source date malformed`,
     which is rejected, `0 of 2`, 1 fail.
2. **`__tests__/fe-s-32/holdings-in-a-browser.test.ts`, `CLAIM_READERS.classification`. RULING W.**
   - The reader accepts a partition, or an out-of-enum token followed by ` (<ADVISORY_OUT_OF_ENUM_WORDS>)`.
   - It rejects an out-of-enum token without the flag. Each flagged row proves this on its own token: `the same
     token unflagged "ADVISORY" -> rejected`.
   - Mutant m5 removes the flag words from SliceTable. F32-AC5 then reads NOT FOUND on observed and target,
     `4 of 6`, 1 fail.
   - The `ADVISORY` list itself is unchanged.
   - The flag's words are imported from `tabs/holdings/slices.ts`, one name added to the file's existing import,
     so they are never re-typed. That is the only other line changed (row W3-S32).
   - `holdings-no-answer.json` is untouched.

## Where each null rule is decided (one rule per plane, no second copy)

| plane | what null means | decided in | reads on the panel |
|---|---|---|---|
| WIRE (a status's `source_dates.business_date`, or a wire document's clocks) | a producer defect | `contracts/adapt.ts` `readingFromValue`: null -> fact `NULL`. Unchanged. | `Source date malformed` (F39-AC3; fe-s-34 path 2 NULL) |
| VIEW (a view document's `sourceTimestamps.businessAsOf`) | "no clock", the `SourceTimestamps` contract's own definition | `contracts/adapt.ts` `carryDocumentReading`: a view null goes to the same `readingFromValue` as `undefined`, i.e. fact `ABSENT` | `No source age yet` on a no-answer state (F39-AC2), `Source time unknown` on an answer-bearing one (fe-s-34 path 1 NULL) |

## The advisory (RULING W, row W2-S29)

- An in-enum token is renamed through `ADVISORY_FOR_WIRE`, as before.
- An out-of-enum token becomes `{ outOfEnum: token }` (`contracts/index.ts` `OutOfEnumAdvisory`).
- `SliceTable.tsx` shows that token verbatim beside `(not a contract advisory value -- shown as sent)`, with
  `data-advisory-out-of-enum="true"`.
- The Directory use site is unchanged (row W3-S29).

## Criteria (deciding runs, on the portal tree that is HEAD 45d5c1de)

| id | status | deciding line | denominator |
|---|---|---|---|
| F39-AC1 | PASS | `rc=0` | 1 of 1 typecheck |
| F39-AC2 | PASS | `VIEW DOCUMENT WITH A NULL businessAsOf -> ABSENCE NAMED, NOT MALFORMED: 3 of 3` | 3 of 3 nulls; 5 pass / 0 fail |
| F39-AC3 | PASS | `WIRE NULL business_date STILL READS MALFORMED: yes` | 2 of 2 wire arms |
| F39-AC4 | PASS | `businessDateOf PROVENANCE KEYS ON producerState: 2 of 2` | 2 of 2 |
| F39-AC5 | PASS | `F21 GRADES THE DOCUMENT'S BUSINESS DATE, NOT AN INSTANT: yes` | 5 of 5 states; 8 pass / 0 fail |
| F39-AC6 | PASS | `OUT-OF-ENUM ADVISORY ON A READY ANSWER -> VERBATIM AND FLAGGED: 3 of 3` | 3 of 3 rows |
| F39-AC7 | PASS | `IN-ENUM ADVISORY UNCHANGED: yes` | 3 of 3 tokens x 3 cells |
| F39-AC8 | PASS | `HOLDINGS UNDER THE GATE, IN A BROWSER: 4 of 4`; `CLAIMED FIELD PRESENT IN THE RENDERED DOM: 6 of 6`; **7 pass / 0 fail**, rc=0 | 4 of 4 scenarios at 390 and 1440, own server on 5263 |
| F39-AC9 | PASS | `532 pass / 14 skip / 0 fail`, `Ran 546 tests across 96 files`, rc=0 | 546 tests, 96 files; +1 file vs the first run is fe-s-38/isolation.test.ts (the sync) |
| F39-AC10 | RECORDED (judgment) | see the proof instance | graded at L9 by 3.0.0_SA_CVO |

F39-AC9 runs on a closed port, so fe-s-32's five browser tests SKIP by name under ruling C. F32-AC5 is exercised
only by F39-AC8.

## Controls

- **Mutants.**
  - m1 and m2 are the first run's, at 794d4899: F39-AC2 and F39-AC6 each read `0 of 3`.
  - m4 is this run's: the view-null rule reverted, run against fe-s-34. It reads `0 of 2`, 1 fail.
  - m5 is this run's: the flag removed from the cell, run against fe-s-32. It reads `4 of 6`, 1 fail.
  - Each mutated file was restored from a byte copy and read clean against HEAD. FIRED-AS-EXPECTED.
- **Determinism.** F39-AC8 ran twice on identical bytes, before m5 and after m5's restore. Both read 4 of 4,
  6 of 6, 7 pass / 0 fail. STABLE.

## Servers

- 5263 measured closed (curl rc=7).
- Launched `bun run dev --port 5263 --strictPort` from `<WS>/portal`. No override config: FE-s-38 has drained, and
  vite's cache is `portal/.vite`, inside the worktree.
- vite 7.3.5 ready. The probe read HTTP 200, and the fe-s-27 helper read the server as serving THIS worktree
  (`/@fs/.../package.json` byte-identical).
- Killed after the runs (taskkill PIDs 27064 and 29308). 5263 measured closed again.
- Every `bun test` exported `IRPT_FE_DEV_PORT`: 5263 while the server was up, 5273 (measured closed) otherwise.

## Rows (INVESTIGATION_v2.md)

- IRPT_FNTEND-W3-S27 / -S28: BLOCKING, ARMED (disarm owner 2.0.0_SA_COO~F), filed by the first run. AMENDMENT 1
  granted both tests and this run amended them. The rows are not edited; their disposition is the disarm owner's.
- IRPT_FNTEND-W3-S29, -S30, -S31: OBSERVATION, INERT (first run).
- IRPT_FNTEND-W3-S32 (this run): OBSERVATION, INERT. The one import line added in fe-s-32 beside the reader.
