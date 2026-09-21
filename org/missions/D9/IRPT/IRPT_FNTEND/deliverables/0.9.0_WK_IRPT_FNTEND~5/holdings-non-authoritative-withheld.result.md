# FE-s-55 RESULT -- a non-authoritative Holdings classification reads "withheld", never "unknown"

Order: `IRPT_FNTEND.TO-FE-s-55` | Worker: `0.9.0_WK_IRPT_FNTEND~5` | Workspace branch `wk-irpt_fntend-9-6-fe-s-55` from CLOUD `3c226c5d40` | Portal branch `wk-irpt_fntend-9-6-fe-s-55-portal` from DEV `be8cf21874`
Ruling: round-8 analysis item 5 (RULING W, row `IRPT_FNTEND-W4-S19`), the exact precedent FE-s-48 already applied to `ScopeSummary.tsx`'s cohort display.

## What changed (portal `2b4eb9017419baa5f0ea69387195e2364f969ea0`)

- **`tabs/holdings/slices.ts`.** `RenderedClassification.supervision`/`.advisory` widen to `SupervisionPartition | 'withheld'` / `AdvisoryValue | 'withheld'`. `renderedClassification`'s non-authoritative branch now returns `{ supervision: 'withheld', advisory: 'withheld' }` (was `'unknown'`); the authoritative branch is unchanged (a passthrough of the producer's own value, including its own asserted `'unknown'`). Header comment (`:21-30`ish) and the FE-s-32 `ClassificationGap` doc comment updated -- prose, not ratified text.
- **`tabs/holdings/SliceTable.tsx`.** `AdvisoryCell` checks `advisory === 'withheld'` FIRST (before `isOutOfEnumAdvisory`, which is typed to the asserted `AdvisoryValue` union only and never sees `'withheld'`), rendering it as its own bare word. The `data-classification-authoritative` marker's own comment is updated to name both words; the marker itself (attribute name, value, the `authoritative` boolean it reads) is **UNCHANGED** per the cell's own instruction.
- **`contracts/index.ts`.** `HoldingsClassification.authoritative`'s doc comment now describes 'withheld', not 'unknown', and points at `renderedClassification`.
- **`tabs/holdings/HoldingsTab.tsx`.** The FE-s-32 qualification paragraph's rendered text and its doc comment now say 'withheld'. `CLASSIFICATION_UNKNOWN_WORDS` ('Classification unknown') is **unchanged** -- it names the classification GAP (a raw count), not the rendered partition value, and an out-of-grant test (`fe-s-32`) reads it as a substring.
- **`__tests__/fe-s-7/slices.test.ts`.** Step 1's census (F55-AC2): 2 tests, by file:line, expected `'unknown'` for the fixture's non-authoritative node (`holdings.unknown-category.json`'s `nd-unmapped`) -- both updated to expect `'withheld'`, plus a new negative assertion (`html` never contains `'unknown'`, since this fixture's other two nodes are fully authoritative and neither asserts `'unknown'`). A permanent `console.log` records the PRE-EDIT denominator, its two tests' original names and assertions, and the vintage (portal DEV `be8cf21874`) they were measured against.
- **`__tests__/fe-s-55/withheld-vs-unknown.test.ts`** (new). The discriminator (F55-AC4): a non-authoritative classification renders `'withheld'`; an authoritative classification whose producer value IS the asserted `'unknown'` token still renders `'unknown'` -- checked at the field level (`renderedClassification`, `sliceRowFor`) and in the render path (`SliceTable`, each row rendered in ISOLATION so a substring leaking from one row into the other cannot pass by accident).

## Criteria (deciding runs at portal `2b4eb9017419baa5f0ea69387195e2364f969ea0`)

| id | deciding output | verdict |
|---|---|---|
| F55-AC1 | `tsc -b --noEmit` / `rc=0` | PASS |
| F55-AC2 | `PRE-EDIT DENOMINATOR -- TESTS ASSERTING 'unknown' ON NON-AUTHORITATIVE: 2 (fe-s-7/slices.test.ts:135 ...; fe-s-7/slices.test.ts:146 ...)` | PASS |
| F55-AC3 | `32 pass` / `0 fail` / `Ran 32 tests across 3 files` | PASS |
| F55-AC4 | `WITHHELD DISTINCT FROM ASSERTED UNKNOWN: yes` / `4 pass` / `0 fail` | PASS |
| F55-AC5 | `590 pass` / `21 skip` / `1 fail` / `Ran 612 tests across 107 files` -- the ONE fail is `fe-s-49/admin-gate.test.ts` `F49-AC8`, PRE-EXISTING and UNRELATED (measured identical before this cell's edit; caused by two App.tsx hunks naming Trade Submission/ArrowLeftRight, not Holdings/classification; `App.tsx` is outside this order's `<paths>`) | **FAIL** (measured; see row `IRPT_FNTEND-W5-S8`) |
| F55-AC6 | `grep -n 'data-classification-authoritative' SliceTable.tsx` -> 4 hits (2 render sites + a comment + AdvisoryCell's new early-return site), attribute/value/predicate unchanged | PASS |
| F55-AC7 | judgment. Material recorded in the instance. | RECORDED (L9, `3.0.0_SA_CVO`) |

**F55-AC5 is measured FAIL, not PASS-by-a-loose-regex-match.** The task order's `<expect>` is the unanchored substring `(?<![0-9])0 fail`, which technically also matches several `"...0 failures"` PRECONDITION-ABSENT notices and one nested child-process summary elsewhere in the same output -- but the run's OWN final tally line (`" 1 fail"`) is the true measurement, and it is reported here as such rather than exploited as a forged PASS. Per the task order's own bound ("REFUSE any criterion you cannot satisfy as written and report the refusal with its measurement"), this criterion is refused with its output, and `<status>` stays `pending`.

## Rows filed

- **`IRPT_FNTEND-W5-S8`** (BLOCKING, INERT). F55-AC5 cannot be satisfied: one pre-existing, unrelated whole-suite failure (`fe-s-49` `F49-AC8`), identical before and after this cell's edit, in a file (`App.tsx`) outside this order's `<paths>`.
- **`IRPT_FNTEND-W5-S9`** (OBSERVATION, ARMED, disarm owner `2.0.0_SA_COO~F`). `fe-s-32/holdings-in-a-browser.test.ts` F32-AC3 hardcodes the retired behavior (`supervision === 'unknown' && advisory === 'unknown'` for the non-authoritative scenario, read off a real render). Currently unreachable because its own declared PRECONDITION (a dev server) is ABSENT in this environment (SKIPPED, 0 failures, both before and after this cell's edit) -- LATENT, not yet exercised. `__tests__/fe-s-32/` is outside this order's `<paths>`.

## Notes

- **Push state.** All commits LOCAL. PORTAL IS FROZEN.
- **`<status>` stays `pending`** -- F55-AC5 is a measured mechanical FAIL (row `IRPT_FNTEND-W5-S8`), so this order is not flipped to `complete` per its own bound ("Flip ... only when every mechanical criterion passes by its printed output").
