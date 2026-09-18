# LT-c-2 (round 2) -- the card names its own subject

**Worker:** `0.9.0_WK_LGIC_LGCTFM~1` | **Order:** `LGIC_LGCTFM.TO-LT-c-2-r2` | **Branch:**
`wk-lgic-lgctfm-2-3` | **Artifact commit:** `f3cfbabebb` | **Written:** 2026-09-18

## THE RESULT IN ONE LINE

`ANDREW_CARD.md` now names its run, its contract's content hash, the instrument that produced that
hash and the adjudication that confirmed its ranking -- and the ranking table and the RECOMMENDATION
line are byte-identical to what they were, which is the half of this cell that mattered most.

## ACCEPTANCE

| criterion | arm | verdict | deciding line |
|---|---|---|---|
| C2R2-AC1 | `c2-names-run` | **PASS** | `VERDICT: PASS-C2-CARD-NAMES-ITS-RUN-AND-HASH` (3 of 3 elements True) |
| C2R2-AC2 | `c2-frozen` | **PASS** (a GUARD) | `VERDICT: PASS-C2-RANKING-AND-RECOMMENDATION-UNCHANGED` (11 rows, both sha1s identical True) |
| C2R2-AC3 | `c2-pointer` | **PASS** | `VERDICT: PASS-C2-CARD-POINTS-AT-THE-ADJUDICATION` |
| C2R2-AC4 | judgment | RECORDED, no verdict | for `3.0.0_SA_CVO` at L9 |

`selftest-arms` ran FIRST, before any work: 28 arms, 10 positive-satisfiability,
`VERDICT: PASS-ARMS-DISCRIMINATE`. No arm was unsatisfiable by a correct edit, so no blocking row
was owed on that count.

## THE THREE NUMBERS, RE-DERIVED RATHER THAN COPIED

```
  git hash-object .../20260918T011619Z-8db9eb1/contract.json  -> 33204e29839de89af81fb293317cce3ccdf2266d
  NEGATIVE CONTROL, the other candidate run:
  git hash-object .../20260918T002711Z-caf0983/contract.json  -> 3ffedfed35c05a1820d594c85c2b416c0441aa0f
  CORROBORATION on a DIFFERENT instrument (not a re-run of the first):
  git rev-parse HEAD:.../20260918T011619Z-8db9eb1/contract.json -> 33204e29839de89af81fb293317cce3ccdf2266d
```

A hash that merely matches proves nothing without the second read. These differ, so the pin
discriminates between exactly the two runs row `S12` said a reader could not tell apart.

## THE GUARD, MEASURED BEFORE AND AFTER

```
  ranking table    11 rows  sha1 837b46cc6dde4912ab31de9d2ba664c5dc1284e6  ->  UNCHANGED
  recommendation            sha1 b5513d671f10da2bced39b311c9989cc1d1796df  ->  UNCHANGED
  non-ASCII        0 characters -> 0 characters
  diff             22 insertions, 0 deletions
```

**And the guard was made to fail on the real card, through its real CLI.** `c2-frozen` reads PASS at
the cut and can only be broken by this cell's own edit -- the shape that passes vacuously if the
arm's wiring never reaches the file, because a PASS on an unread object and a PASS on a correct
object are the same string. One ranking-table cell was altered (`| 1 | T-0001 |` ->
`| 1 | T-9999 |`), the arm run, and the bytes restored in the same process and verified byte-identical:

```
  BEFORE   VERDICT: PASS-C2-RANKING-AND-RECOMMENDATION-UNCHANGED
  MUTANT   VERDICT: FAIL-C2-RANKING-AND-RECOMMENDATION-UNCHANGED
  MUTANT   VERDICT: PASS-C2-CARD-NAMES-ITS-RUN-AND-HASH      (the two arms are independent)
  RESTORED byte-identical to pre-mutation: True
  AFTER    VERDICT: PASS-C2-RANKING-AND-RECOMMENDATION-UNCHANGED
```

**The silent way to break that guard had nothing to do with this cell's content.** The two pinned
sha1s are taken over lines that still carry their trailing CR on this CRLF checkout, so a
well-meaning LF rewrite of the file would have failed an arm on text it never touched. The splice
preserved the checkout's line endings byte for byte and refused on a MIXED file.

## THE RECOMMENDATION IS WRONG BY ONE AND STAYS AS WRITTEN

It says *"the two rows touching a live, client-facing surface"*; measured over 179 tensions the
answer is **1 of 179** (`T-0001`). Row `S6` set the condition that this correction reach the
decision-maker **beside** the card *"rather than as a silent rewrite"*, and it did, through
`1.0.0_SA_CTO`'s adjudication `662d53b793` under Andrew-direct. Rewriting it now would be the exact
act `S6` exists to prevent. The card gains a **pointer**: a section naming the adjudication, what it
decided, and the corrected claim stated as a count with its denominator and attributed to that
commit -- with the sentence above it untouched. That is more than the bare citation the order
required and less than a rewrite, and the instance declares the judgment as this cell's for the CVO
to weigh.

## ONE ROW FILED -- `LGIC_LGCTFM-W1-S22`

OBSERVATION, ARMED, `disarm_owner` `2.0.0_SA_COO~G`.

**The published reason for the two hashes is half the cause, and the recipe as written yields a third
number.** Four carriers (`R2_BASE.json`, `CARD_SUBJECT_PIN.md`, row `S19`, and `NUMBER_PINS_R2.json`
on all 16 pins) explain the gap between `33204e29...` and the plain sha1 `9c5cdb87...` as *"git
prefixes blob <len> and a NUL byte"*. Measured here:

```
  sha1( b'blob 790871' + NUL + CHECKOUT bytes )      -> d07bf29d245fd358fa15859b09a35aa8a3a2d5c3
  sha1( b'blob 765904' + NUL + CRLF->LF bytes )      -> 33204e29839de89af81fb293317cce3ccdf2266d
  checkout 790871 bytes, 24967 CRLF pairs; core.autocrlf=true
```

`git hash-object` runs the end-of-line filter **first**, so the published hash is the id of the
COMMITTED bytes while the plain sha1 is over the CHECKOUT bytes. **Every number in the record is
correct**; the stated MECHANISM is not, and the mechanism is the half a later seat re-derives from --
it would return `d07bf29d...`, which appears nowhere in the record, and read a mismatch where there
is none. That is the near-miss `S19` already records, one level down. The remedy is one clause per
carrier, and `NUMBER_PINS_R2.json` already carries it (*"confirmed equal to git rev-parse
HEAD:<path>, so the pin is the committed bytes"*). The card's own wording was written in that form.

## WHAT THIS CELL DID NOT DO

- It did not correct the RECOMMENDATION, touch the ranking table, the rule quote or the evidence
  section. Within the granted card it only ADDED.
- It did not repair the four carriers of the incomplete instrument explanation: three are outside
  this order's `<paths>` and the fourth is an append-only channel row. The finding is a row with a
  named disarm owner, and a worker judges a surprise's form, never its significance.
- It did not dispose of `S6`, `S12`, `S16` or `S19` -- those are `3.0.0_SA_CVO`'s. It performed the
  durable remedy `S19` itself named as owed to a later cell: *"the durable fix is a CELL whose
  `<paths>` names the card."*

## READING NOTE FOR THE NEXT SEAT

`INVESTIGATION_v1.md` carries **five** json fences: one list of 22 rows and **four single-row dicts**
holding `S10`, `S11`, `S12` and `S20`. A reader who parses only the list fence -- the correct target
for an append -- **will not find `S12` at all**, which this order required be read whole. Select the
append target by `isinstance(obj, list)`; census row ids over the whole file, and over every document
under the channel (the maximum lives in `INVESTIGATION_v1.md` at `S21`, but `ADJUDICATION_v1.md`
reaches `S20` and only a per-document walk shows that).

## PROOF

`org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~1/LGIC_LGCTFM.TO-LT-c-2-r2.card-names-its-subject.proof_of_spec.json`
-- `proof-of-spec-check.py` **rc=0, VALID**, with `--governing-order`. Surprises limb: 1 entry, 1
resolving channel row. **Negative control beside it:** the same instance with `C2R2-AC9` appended to
the id list reads `INVALID (rc=1)` on `coverage: criterion 'C2R2-AC9' ... has NO instance row`, so
the checker discriminates on this instance rather than passing everything.
