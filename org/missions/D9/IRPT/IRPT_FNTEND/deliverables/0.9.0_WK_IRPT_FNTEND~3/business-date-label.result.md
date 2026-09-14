# IRPT_FNTEND.TO-FE-s-34 -- business-date label: result

Worker: `0.9.0_WK_IRPT_FNTEND~3`. Worktree pair `/c/tmp/wk-irpt_fntend-5-3-fe-s-34`, on the order as amended at `1df5ac405f`,
and its `portal/`. All portal commits are **LOCAL** on branch `wk-irpt_fntend-5-3-fe-s-34`:

- `944499a9` -- ruling K (the label) and ruling O (the reroute), plus `__tests__/fe-s-34/label.test.ts`.
- `f7b2d986` -- amendment 1: the two `startsWith('Updated ')` checks.
- `fa9cbee2` -- amendment 2, ruling R: the no-status path ages the document's own business date, never an instant.

The portal branch also carries the issuer's sync merge `c18a2aab` of DEV `e85498be`.

**The order is OPEN (`<status>pending</status>`).** F34-AC6 has one failure, `__tests__/fe-s-3/status.test.ts:121`. That file is
outside the grant, and the line asserts exactly the instant hand-through that ruling R ends (row W3-S24).

## Amendment 2 (ruling R): what changed

- **`contracts/adapt.ts`**
  - `wireEnvelope` already built the document's business-date reading from `businessAsOf` and then dropped it. It now puts that
    reading on `availability.sourceDate`.
  - `carryAvailabilityFromStatus` keeps the document's own reading when no status arrives. When a status does arrive, the
    status's reading still wins, as before.
- **`state/status.ts`, `envelopeFromAvailability`**
  - The no-status branch changed from `sourceDate === undefined ? sourceAsOf : sourceDate` to `sourceDate ?? ABSENT_SOURCE_DATE`.
  - The panel is now handed a business-date reading or the stated absence. It is never handed an instant.
- **fe-s-25 claims moved (only these):**
  - The `source-age-field.test.ts:128` regex pinned the instant fallback. It is replaced by a behavioural no-status check that
    cites ruling R and is shown both ways.
  - That check prints the F34-AC10 line only when it holds.
  - Every other assertion in the folder is as written.
- **New test:** `__tests__/fe-s-34/no-status.test.ts`, for F34-AC8 and F34-AC9.

## Criteria (deciding runs on the portal `fa9cbee2` bytes)

| id | verdict | deciding line |
|---|---|---|
| F34-AC1 | PASS | `rc=0` |
| F34-AC2 | PASS | `formatSourceAge( CALL SITES OUTSIDE state/status.ts: 0 (across 217 files)` |
| F34-AC3 | PASS | `ANALYSIS PANELS AGE THE BUSINESS DATE: 2 of 2` |
| F34-AC4 | PASS | `THE LABEL NAMES THE BUSINESS DATE: yes` |
| F34-AC5 | PASS | `"UPDATED" ON A BUSINESS-DATE AGE: 0 (source 0 + render 0 + pure 0)` |
| F34-AC6 | **FAIL** | ` 84 pass` / ` 2 skip` / ` 1 fail` -- `fe-s-3/status.test.ts:121` (row W3-S24) |
| F34-AC7 | RECORDED (judgment, L9) | no verdict |
| F34-AC8 | PASS | `NO-STATUS DOCUMENT, INSTANT AND BUSINESS DATE DIFFER -> BOTH PANELS AGE THE BUSINESS DATE: 2 of 2` |
| F34-AC9 | PASS | `NO-STATUS DOCUMENT WITHOUT A BUSINESS DATE -> ABSENCE NAMED, NO AGE: 2 of 2` |
| F34-AC10 | PASS | `NO-STATUS ENVELOPE CARRIES THE DOCUMENT'S BUSINESS-DATE READING, NOT THE INSTANT: yes` |

F34-AC6 ran with `IRPT_FE_DEV_PORT=54034`, a port measured closed on `localhost`, `127.0.0.1` and `[::1]`. Its 2 skips are FE-s-30's
dev-server tests, which skip when their precondition is absent.

**Before the ruling-R edit:** F34-AC8 read `0 of 2`, F34-AC9 read `0 of 2`, and the F34-AC10 check printed its "DOES NOT CARRY" line.

**Whole InvestorReporting suite:** 509 / 6 / 0 before, 510 pass / 6 skip / 1 fail after, the one failure being W3-S24's line.

## Rows

| row | class, hazard | status |
|---|---|---|
| W3-S19 | BLOCKING | Resolved by amendment 1 (`f7b2d986`). |
| W3-S20 | OBSERVATION, INERT | Unchanged. |
| W3-S21 | OBSERVATION, ARMED | Answered by ruling R, implemented at `fa9cbee2`. |
| W3-S22 | OBSERVATION, INERT | Not this amendment's. |
| **W3-S23** (new) | OBSERVATION, ARMED | See below. |
| **W3-S24** (new) | BLOCKING, ARMED | See below. |
| **W3-S25** (new) | OBSERVATION, INERT | See below. |

- **W3-S23.** F34-AC8's named *availability* instant cannot exist on a no-status v1 document, because only a status writes it.
  - The criterion's dates belong to the fe-s-6 VIEW fixture, which ruling R's adapter remedy never reaches.
  - That fixture now names an absence instead of ageing its instant.
  - F34-AC8 is graded on the committed no-status Holdings body, using the document's own instant.
- **W3-S24.** `fe-s-3/status.test.ts:121` asserts the instant is handed through, which ruling R ends; the file is outside the grant.
- **W3-S25.** FE-s-30's `businessDateOf` now reports `from:'status'` for a no-status document's own reading. Measured; no current
  render path reaches it.

## For the issuer

1. Grant `__tests__/fe-s-3/status.test.ts:121` for one purpose: assert the ABSENT reading (or that no instant is handed), citing
   ruling R. F34-AC6 then re-runs.
2. Route W3-S23 and W3-S25, which sit in files outside the grant: the FixtureAdapter or the view fixtures, and FE-s-30's
   `businessDateOf`.
