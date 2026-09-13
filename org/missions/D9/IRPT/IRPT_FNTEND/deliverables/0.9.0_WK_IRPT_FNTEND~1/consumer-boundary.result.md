# IRPT_FNTEND.TO-FE-s-25 -- the consumer boundary: a distinction the contract makes must survive arrival

**Worker:** `0.9.0_WK_IRPT_FNTEND~1` (slot ~1)
**Branch:** `wk-irpt_fntend-4-1-fe-s-25` (workspace and portal), cut from CLOUD @`f3b42b1e0b` / DEV @`237a9027`
**Portal commits:** `abd470c7` (pass 1) and `fbc5699c` (pass 2) -- LOCAL. Portal is frozen: no push, no gitlink bump.
**Grant:** widened by the issuer @`913706a898` with `tabs/StatusPanel.tsx` and a ruling on row `W1-S49`:
*display the producer's state; do NOT add a view state.*
**Order status:** `complete`, flipped in the same commit as this file, after `proof-of-spec-check` returned rc=0.
All 11 mechanical criteria pass by output. `F25-AC12` is a judgment criterion and carries a record with no verdict.

---

## THE RESULT IN ONE PARAGRAPH

Pass 1 refused `F25-AC6` at 7 of 9 because QUEUED and RUNNING rendered identically, and both honest remedies
needed a path outside the grant (row `W1-S49`). The issuer widened the grant and ruled for **displaying** the
producer's state. Re-grounding that premise before writing the fix exposed **my own pass-1 defect** (row
`W1-S50`). My panel tests had graded `tabEnvelopeFromStatus`, a builder with **zero production callers**. Every
tab builds its panel from `envelopeFromAvailability(<document>.availability)`, so the pass-1 fixes did not reach
the page a reader actually sees. Pass 2 moves both producer facts, the three-way source-date fact and the
producer's state, onto that path. It retires the builder and re-drives every panel test from a v1 response body
through the real parser. On that path all four rows now hold. `F25-AC6` reads **9 of 9 with the reason code held
constant**.

---

## WHAT A READER OF THE PAGE CAN NOW TELL APART -- one entry per row

"Before" is the tab path at `237a9027`: response → `parseIrEnvelope` → `carryAvailabilityFromStatus` →
`<document>.availability` → `envelopeFromAvailability` → `StatusPanel`. "Now" is the same path at `fbc5699c`.
Every "now" below was measured on that path. None was measured on a test-only builder.

### `W1-S43` -- ABSENT vs NULL (`F25-AC2`, `F25-AC3`)

| no-answer state | `business_date` ABSENT | `business_date: null` |
|---|---|---|
| QUEUED, RUNNING, UNAVAILABLE, FAILED -- **before** | identical: both read the availability instant | identical |
| QUEUED, RUNNING, UNAVAILABLE, FAILED -- **now** | `No source age yet` | `Source date malformed` |

**A reader can now tell a job that has no source date yet from a producer that broke the contract.** The fact
is taken on the wire object and travels on the document's `availability.sourceDate` to the panel. A consumer
holding only the view document can read it (`ABSENT` vs `NULL`). The pattern is enforced as well as the
instance. A scan of `contracts/` and `state/` checks the 35 fields that may be absent but never null, which is
309 declared schema properties minus the required ones minus the null-admitting ones. It finds **0** `?? null`
coalesces on them. The positive control fires 2 of 2 and the negative control 0.

### `W1-S42` -- the age reads the field the clause governs (`F25-AC4`, `F25-AC5`)

A READY response carrying the REQUIRED `business_date` renders its age from **that date**. On an injected clock
that is `Updated 2d ago`, asserted equal to the age of `business_date` itself. Before, the same slot read the
availability **instant**: the status's `as_of`, or, when the status sent none, the document's own timestamp.
**A reader now sees the age of the date the contract governs, and a READY that lost its date still reads
`Source time unknown`**, rather than quietly borrowing the document's instant. Field agreement is structural.
The spelling is declared once, the adapter reads it, the status rules read it, and `envelopeFromAvailability`,
the builder every tab calls, hands the reading to the panel. The behavioural arm uses three different dates on
the tab path. On all 5 answer-bearing states it renders `Updated 2d ago` where `as_of` would give
`Updated 7d ago`.

### `W1-S41` -- two different nines (`F25-AC6`, `F25-AC7`)

Nine responses, identical except `state`, with the reason code held at `STATE_REPORTED`:

| producer state | what a reader sees |
|---|---|
| QUEUED | `Loading \| Queued -- not started yet \| No source age yet \| STATE_REPORTED` |
| RUNNING | `Loading \| Running -- in progress \| No source age yet \| STATE_REPORTED` |
| *(no response yet -- `EMPTY_ENVELOPE`)* | `Loading \| No source age yet` |
| the other seven | their own label, unchanged, **no producer note** (0 of 7) |

**A reader can now tell a queued job from a running one, and both from a browser still waiting for an
answer**, from the words on the page. Before, all three read `Loading`. There are 36 of 36 distinguishable
pairs. The words appear **only** where the view label is shared by more than one producer state. That set is
derived from the adapter's own mapping and today is exactly LOADING. Nothing is invented where the label already
says it. Per the ruling, **no view state was added**. `ENVELOPE_STATES`, `STATE_FOR_WIRE` and every label are
unchanged, and `fe-s-3/` is untouched; its deliberate denominator of 9 still passes. Both planes are printed with
their own denominators and the full mapping (AC7): producer 9, view 9, 8 reached, `RETRYABLE` unreached, one
collapse.

### `W1-S26` -- the generator (`F25-AC8`, `F25-AC9`)

Developer-facing, and unchanged in pass 2. Regenerating `StatusEnvelope` emits **7 of 7** properties, and the
committed file equals the render. A construct the generator cannot render now **refuses with its coordinate
named** instead of emitting a legal-looking `unknown`. All 11 document schemas, plus `responses.ts` and
`index.ts`, regenerate byte-identically.

---

## THE UNSCOPED CHECK THE BOUNDS REQUIRE -- every `StatusPanel` consumer

**Census:** the files under `src/pages/InvestorReporting/` that mention `StatusPanel` number **24**, the same as the
issuer's count, measured independently:
- **9 test files** (per-file results below)
- **1 fixture generator** (`__tests__/fe-s-18/gen-fixtures.ts`), which has no tests and was not run as main
- **14 source files**
  - `tabs/StatusPanel.tsx` itself
  - **3 that import and render it:** `tabs/reporting/ReportingTab.tsx`, `tabs/holdings/HoldingsTab.tsx`, `export/ReceiptPanel.tsx`
  - **10 that mention it without importing:** `contracts/index.ts`, `export/ExportModal.tsx`, `export/submit.ts`,
    `index.tsx`, `state/status.ts`, `tabs/TabShell.tsx`, `tabs/analysis/AnalysisTab.tsx`,
    `tabs/analysis/VariantSelector.tsx`, `tabs/holdings/HoldingsSummary.tsx`, `tabs/reporting/PeriodControls.tsx`

The consumers' reach is transitive, since a test rendering a tab renders the panel. So **every test file under
`__tests__/` was run, one at a time**: 80 of 80, with none NOT-RUN. The first run was at the pre-change commit
`237a9027` (the four pass-1 source files temporarily restored to their blobs, then restored and byte-compared).
The second was at `fbc5699c`.

| the 9 direct test files | at `237a9027` | at `fbc5699c` |
|---|---|---|
| `fe-s-21/source-age.test.ts` | 8 pass / 0 fail | 8 / 0 -- same |
| `fe-s-10/tabs-mounted.test.ts` | 5 / 0 | 5 / 0 -- same |
| `fe-s-11/colour-law.test.ts` | 4 / 0 | 4 / 0 -- same |
| `fe-s-3/source-bounds.test.ts` | 3 / 0 | 3 / 0 -- same |
| `fe-s-5/states.test.ts` | 6 / 0 | 6 / 0 -- same |
| `fe-s-18/manifest.test.ts` | 4 / **1** | 4 / **1** -- same (baseline) |
| `fe-s-25/absent-vs-null.test.ts` | did not exist | 3 / 0 |
| `fe-s-25/source-age-field.test.ts` | did not exist | 3 / 0 |
| `fe-s-25/state-planes.test.ts` | did not exist | 2 / 0 |

**All 80 files:** 452 pass / 7 fail / 1 skip at `237a9027`, and 464 pass / 3 fail / 1 skip at `fbc5699c`. **Four
files changed result, all in fe-s-25**, going from not existing at baseline to passing. The other 76 are identical.
**No test newly fails, so none asserted the old panel text, and no row is owed on that ground.**

**Baseline results, not attributed to this change**, identical at both commits:
- `fe-s-18/manifest.test.ts` -- F18-AC3 declares its own failure in its name.
- `fe-s-19/mounted-from-wire.test.ts` -- F19-AC4 and F19-AC5 **need a dev server**: their declared precondition
  is a vite dev server on port 5181, which is not up in this worktree.
- `fe-s-2/app-diff.test.ts` -- 1 skip, `SKIPPED: .scratch/app.diff absent`. This is an absent-artifact gate,
  not a server.

---

## THINGS THE L9 GRADER SHOULD WEIGH (`F25-AC12`, recorded, no verdict)

1. **A contract question placed, not decided.** The panel can only show what `Availability` carries, so
   `Availability` gained two **optional** members (`producerState`, `sourceDate`). They are additive and every
   out-of-grant constructor still typechecks. But `Availability` is a view-contract member all ten contracts
   carry, and the ruling's rationale was "touches one file and no contract". Row `W1-S50` places the question
   with the issuer.
2. **On the tab path, the age of a status-bearing payload now comes from `business_date`**, even when the status
   or the document carries an instant. AC5 asks for exactly this, and it changes behaviour.
3. **`tabEnvelopeFromStatus` is retired.** It was my own pass-1 addition and had no production caller. Leaving a
   builder that reads live but serves nothing is the trap that misled my own pass-1 tests.
4. **No distinction was invented.** `Source date malformed` renders only for a null the wire sent. The age
   renders only from a date the wire sent. The producer-state words render only where the label is shared, and
   only for a token among the producer's nine.

---

## ROWS

- `IRPT_FNTEND-W1-S49` -- BLOCKING, INERT. F25-AC6 could not reach 9 of 9 inside the original grant. The issuer
  resolved it by widening the grant @`913706a898`.
- `IRPT_FNTEND-W1-S50` -- OBSERVATION, INERT. My own pass-1 defect: its tests graded a builder no tab calls.
  Displaying the producer state therefore had to ride `Availability`. Fixed in this round.
