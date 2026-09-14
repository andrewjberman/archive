# IRPT_FNTEND.TO-FE-s-34 -- business-date label: result

Worker: `0.9.0_WK_IRPT_FNTEND~3`. Worktree pair `/c/tmp/wk-irpt_fntend-5-3-fe-s-34` and its `portal/`, branch
`wk-irpt_fntend-5-3-fe-s-34`, on the order as amended at `7fd807ab76` (amendment 3; 1.0.0_SA_CTO confirms it is within ruling R).

**COMPLETE.** All eleven criteria are met: ten mechanical criteria pass by output, and F34-AC7 is recorded for L9. The proof
instance (`IRPT_FNTEND.TO-FE-s-34.business-date-label.proof_of_spec.json`, in this folder) reads VALID.

## Portal commits (all LOCAL)

| commit | what it carries |
|---|---|
| `944499a9` | Ruling K (the label `Business date age: <figure>`) and ruling O (StageDisplay and VariantSelector route through `formatSourceAgeForState`). |
| `f7b2d986` | Amendment 1: the two `'Updated '` prefix checks. |
| `fa9cbee2` | Amendment 2, ruling R on the v1 path. |
| `c6ee044e` | Amendment 3, ruling R on the view-fixture path. |

The branch also carries the issuer's sync merge `c18a2aab` of portal DEV `e85498be`.

## Amendment 3: what changed

- **`contracts/adapt.ts` -- new `carryDocumentReading`.**
  - A view-shaped document's availability gains `readingFromValue(sourceTimestamps.businessAsOf)`. That is the wire path's own
    rule; there is no second copy.
  - A document that already has a reading keeps it.
- **`src/api/endpoints/investor-reporting.ts` -- `FixtureAdapter.serve`, VIEW branch only.**
  - The branch's expression `: loaded` became `: carryDocumentReading(loaded)`.
  - The one name was added to the existing `contracts/adapt` import list.
  - No other region was touched; FE-s-31 holds `submitExport`.
- **`state/availability.ts` -- `businessDateOf`.**
  - It now reports `from:'status'` only when `availability.producerState` is present, and `from:'document'` otherwise.
  - Nothing else in the file moved.

## Every test assertion changed by this order

Each assertion was changed for one purpose, cites its ruling beside it, and prints itself both ways.

| # | assertion | was | now | commit |
|---|---|---|---|---|
| 1 | `__tests__/fe-s-21/source-age.test.ts:166` (amendment 1, ruling K) | `pure.startsWith('Updated ')` | `isRealAge(pure)`, i.e. equality with `formatSourceAge(AS_OF, now)` -- AS_OF being the date this file's `pure` is aged from (row W3-S22) | `f7b2d986`; now line 176, marker 166 |
| 2 | `__tests__/fe-s-25/source-age-field.test.ts:65` (amendment 1, ruling K) | `expect(pure.startsWith('Updated ')).toBe(true)` | `expect(isBusinessDateAge(pure)).toBe(true)`, i.e. equality with `formatSourceAge(BUSINESS_DATE, now)` | `f7b2d986`; now line 77, marker 70 |
| 3 | `__tests__/fe-s-25/source-age-field.test.ts:128` (amendment 2, ruling R) | a regex pinning `sourceDate === undefined ? availability.sourceAsOf : availability.sourceDate` | a behavioural check: a no-status v1 body, through `parseIrEnvelope` and `envelopeFromAvailability`, hands over the document's own reading; it prints the F34-AC10 line only when that holds | `fa9cbee2`; now line 162, marker 133 |
| 4 | `__tests__/fe-s-3/status.test.ts:121` (amendment 3, ruling R, row W3-S24) | `expect(built.sourceAsOf).toBe('2026-09-10T10:00:00Z')` | `expect(isAbsentReading(built.sourceAsOf)).toBe(true)`, the ABSENT reading | `c6ee044e`; now line 132, marker 121 |
| 5 | `__tests__/fe-s-6/correction.test.ts:94` (amendment 3, ruling R, row W3-S23) | `expect(original).toEqual(rawFixture)` | `expect(original).toEqual(asServed)`, where `asServed = carryDocumentReading(rawFixture)` | `c6ee044e`; now line 108, marker 95 |

Notes on the table:
- **#5, why it qualified.** It pinned the served view document as byte-equal to the raw fixture, whose availability carried only
  the instant. Amendment 3 supersedes that shape. The assertion's job is unchanged: the object loaded before the submit was not
  mutated by it.
- **#5, a fix made before the commit.** Its both-ways log line first used `Bun.deepEquals`, and typecheck read rc=2. It now uses
  a local JSON-equality helper. Only the log line changed; the expect did not.
- **What was not touched:** no other assertion in `__tests__/fe-s-3/`, `fe-s-6/`, `fe-s-21/` or `fe-s-25/`, and nothing in
  `__tests__/fe-s-22/`, `fe-s-26/`, `fe-s-31/` or `fe-s-32/`.

My own folder `__tests__/fe-s-34/` (`label.test.ts`, `no-status.test.ts`, `bun-test-clock.d.ts`) is the order's own test code.

## Criteria (deciding runs on the portal `c6ee044e` bytes)

| id | verdict | deciding line |
|---|---|---|
| F34-AC1 | PASS | `rc=0` |
| F34-AC2 | PASS | `formatSourceAge( CALL SITES OUTSIDE state/status.ts: 0 (across 217 files)` |
| F34-AC3 | PASS | `ANALYSIS PANELS AGE THE BUSINESS DATE: 2 of 2` |
| F34-AC4 | PASS | `THE LABEL NAMES THE BUSINESS DATE: yes` |
| F34-AC5 | PASS | `"UPDATED" ON A BUSINESS-DATE AGE: 0 (source 0 + render 0 + pure 0)` |
| F34-AC6 | PASS | ` 86 pass` / ` 2 skip` / ` 0 fail`, `Ran 88 tests across 19 files.` |
| F34-AC7 | RECORDED (judgment, L9) | no verdict |
| F34-AC8 | PASS | `NO-STATUS DOCUMENT, INSTANT AND BUSINESS DATE DIFFER -> BOTH PANELS AGE THE BUSINESS DATE: 2 of 2` |
| F34-AC9 | PASS | `NO-STATUS DOCUMENT WITHOUT A BUSINESS DATE -> ABSENCE NAMED, NO AGE: 2 of 2` |
| F34-AC10 | PASS | `NO-STATUS ENVELOPE CARRIES THE DOCUMENT'S BUSINESS-DATE READING, NOT THE INSTANT: yes` |
| F34-AC11 | PASS | `NO-STATUS BUSINESS DATE PROVENANCE -> document: 2 of 2` |

Notes on the criteria:
- **F34-AC6** ran with `IRPT_FE_DEV_PORT=54034`, a port measured closed on `localhost`, `127.0.0.1` and `[::1]`. Its 2 skips are
  FE-s-30's dev-server tests, which skip when their precondition is absent.
- **F34-AC11 control:** a status-carried date still reports `from:"status"`.
- **Whole InvestorReporting suite:** 512 pass / 6 skip / 0 fail across 90 files.
- **Before the amendment-3 source edit:** F34-AC8 read `0 of 2`, F34-AC9 read `0 of 2`, and F34-AC11 read `1 of 2`.

## Rows

| row | class, hazard | status |
|---|---|---|
| W3-S19 | BLOCKING | Resolved by amendment 1. |
| W3-S20 | OBSERVATION, INERT | Unchanged. |
| W3-S21 | OBSERVATION, ARMED | Answered by ruling R on both paths. |
| W3-S22 | OBSERVATION, INERT | In no amendment. |
| W3-S23 | OBSERVATION, ARMED | Resolved by amendment 3. |
| W3-S24 | BLOCKING, ARMED | Resolved by amendment 3. |
| W3-S25 | OBSERVATION, INERT | Resolved by amendment 3. |
| **W3-S26** (new) | OBSERVATION, INERT | See below. |

- **W3-S26.** The one reading rule reads a view document's null `businessAsOf` as NULL, shown as "Source date malformed". The view
  contract means "no clock" by that null. It affects 3 of 134 view documents, all in `smoke/fe-s-3-loading.json`; no test fails.
