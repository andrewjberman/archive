# FE-s-48 RESULT -- a cohort value the panel declines to assert reads "withheld", never "unknown"

Order: `IRPT_FNTEND.TO-FE-s-48` | Worker: `0.9.0_WK_IRPT_FNTEND~4` | Workspace branch `wk-irpt_fntend-8-4-fe-s-48` from CLOUD `e2d9f703e9` | Portal branch `wk-irpt_fntend-8-4-fe-s-48` from DEV `1f3ce9f0`
Ruling: `1.0.0_SA_CTO` round-7 analysis (msg 96865, item 6), on `3.0.0_SA_CVO`'s F42-AC10 qualification (grade record C-S93).

## What changed

**Portal `a06252ee`: `src/pages/InvestorReporting/header/ScopeSummary.tsx`.** Text only, 4 insertions and 2 deletions.

```diff
@@ -9,7 +9,9 @@
  * fact nobody asserted is the defect the flag exists to prevent -- so those
- * axes are shown as 'unknown' text with no affordance.
+ * axes are shown as 'withheld' text with no affordance. FE-s-48 (`1.0.0_SA_CTO`,
+ * round-7 analysis item 6): a value the panel declines to assert is withheld,
+ * not unknown. An asserted UNKNOWN token keeps rendering as 'unknown'.
@@ -115,7 +117,7 @@
         {withheld.length > 0 ? (
-          <Fact label="Cohort (not asserted)" value={withheld.map((c) => `${c.axis}: unknown`).join(', ')} />
+          <Fact label="Cohort (not asserted)" value={withheld.map((c) => `${c.axis}: withheld`).join(', ')} />
         ) : null}
```

- The assertable path is untouched: the buttons, the out-of-enum flag, and a producer's own UNKNOWN token.
- No class, colour, element or label moves. F48-AC4 finds 1 of 111 code lines changed, and it is the withheld fact.

**Portal `e5c92f0c`: `src/pages/InvestorReporting/__tests__/fe-s-48/withheld.test.ts`** (new). It grades F48-AC2 to AC5.
- **Rendering.** ScopeSummary is rendered in memory with `renderToStaticMarkup`, with no server.
- **Reads.** Every file the test inspects is a committed blob or a `git grep <rev>` over the committed tree (RULING AC).
- **The one working-copy read.** The test checks that the imported ScopeSummary.tsx equals its HEAD blob, and grades no render unless it does.

## Criteria (deciding runs at portal `e5c92f0c`, `IRPT_FE_DEV_PORT=5265`, measured closed)

| id | deciding output | verdict |
|---|---|---|
| F48-AC1 | `tsc -b --noEmit` / `rc=0` | PASS |
| F48-AC2 | `NON-AUTHORITATIVE COHORT READS WITHHELD ON EVERY AXIS: 5 of 5` (3 fixture axes + 2 wire axes; the reader reads 0 of 3 on DEV 1f3ce9f0's fact) | PASS |
| F48-AC3 | `IN-ENUM AUTHORITATIVE ADVISORY UNCHANGED: 3 of 3` (the cohort block is byte-identical to DEV 1f3ce9f0; UNKNOWN still reads `advisory: unknown`) | PASS |
| F48-AC4 | `BEFORE (DEV 1f3ce9f0): THE WITHHELD FACT READ unknown: yes` / `AFTER (HEAD): THE WITHHELD FACT READS withheld: yes` | PASS |
| F48-AC5 | `EVERY RENDER OF A WITHHELD COHORT VALUE READS withheld: 1 of 1` (59 files, 58 subtracted with reasons, 0 unclassified; the same census at DEV 1f3ce9f0 reads 0 of 1) | PASS |
| F48-AC6 | `564 pass` / `18 skip` / `0 fail` / `Ran 582 tests across 103 files` / `rc=0` | PASS |
| F48-AC7 | judgment. The material is recorded in the instance. | RECORDED (L9, 3.0.0_SA_CVO) |

## The render census (F48-AC5), by subtraction

**The domain.** `git grep -l -i -w -e CohortFact -e cohorts -e authoritative HEAD -- src`, outside `__tests__/`. That is 59 files; 8 more under `__tests__/` are excluded.

**Subtracted, 58 files:**
- **13 files outside the page.** Each names neither `CohortFact` nor `InvestorReporting`.
- **34 fixture JSON files.** They are data.
- **5 files that hold no CohortFact.** Their `authoritative` belongs to another fact:
  - `contracts/wire/HoldingsSnapshot.ts`;
  - `tabs/analysis/composer.ts`;
  - `tabs/holdings/HoldingsTab.tsx`, `SliceTable.tsx` and `slices.ts`.
- **6 holders with no markup.** Each carries its stated role:
  - `contracts/index.ts` declares the type;
  - `contracts/adapt.ts` produces CohortFacts;
  - `contracts/validate.ts` checks them;
  - `contracts/wire/DirectoryEntry.ts` declares the wire cohort;
  - `header/search.ts` carries the entry;
  - `fixtures/index.ts` is the registry. `NAMED_NEGATIVES` is named by 0 other non-test files.

**Remaining:** 1 render site, `header/ScopeSummary.tsx`, and it reads `withheld`.

## Rows filed (all OBSERVATION, INERT)

- **`IRPT_FNTEND-W4-S18`.** The order cites `contracts/validate.ts:164-171` for the cohort check. At DEV 1f3ce9f0 those lines are the termination and access checks, and the cohort check is at `:178-192`.
- **`IRPT_FNTEND-W4-S19`.** Holdings renders a non-authoritative classification's partitions as `unknown` (`slices.ts:100-102`), following the contract's own rule (`contracts/index.ts:708`). That is the same shape one surface over. It is not a CohortFact and not in this grant, so it is placed for the ruling's owner.
- **`IRPT_FNTEND-W4-S20`.** `fixtures/index.ts:77` still says the unknown-cohort fixture's "unknown renders as unknown". The header now renders it `withheld`. Fixtures are not in this grant.

## Notes

- **The issuer's probe, re-run.** The whole suite reads 0 fail with the change and the new test: 564 pass and 18 skip of 582. F41-AC5's control did not time out on this run.
- **A mechanics note.** The new test file needed one explicit `git add` before the pathspec commit, because git will not commit an untracked path by pathspec alone.
- **Push state.** All commits are LOCAL. PORTAL IS FROZEN.
