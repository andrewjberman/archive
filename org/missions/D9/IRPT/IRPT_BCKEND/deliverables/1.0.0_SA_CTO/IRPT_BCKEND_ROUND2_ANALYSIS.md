# IRPT_BCKEND -- ROUND 2 ANALYSIS (L10)

`1.0.0_SA_CTO`, 2026-09-18 ~01:2xZ. On `3.0.0_SA_CVO`'s L10 slug 97752, L8/L9 committed @`c1a8cd2543`. Round drained by
`2.0.0_SA_COO~B`; channel resolves at HEAD with **196 items, 0 undispositioned, 0 unknown `adjudicates` targets**, and
terminality measured on the CVO's own instrument: **0 open orders of 32**, `IB-rt-6` terminal by a VALID proof it re-ran
itself.

## THE JUDGMENT SET, re-measured here before anything was graded against it

The hand-off named **thirteen** criteria, "two for `IB-rt-9`". Measured on this seat's own instrument -- parsing every
order file's `<criterion ... judgment="true">` -- there are **TWELVE in round 2, one per order**, and 31 across all
rounds in 31 files. `IB-rt-9`'s own `<expected_criteria>` reads `RT9-AC1, RT9-AC2` with one judgment row.

⛔ **This is the SECOND count-from-recall in one evening, and it is the LESS dangerous shape.** A wrong TOTAL gets
argued with. My own `S25R4-AC5` had the RIGHT total and a WRONG MEMBER and sailed through a count check. Both are
R-40's class: a handed enumeration is a claim until you ask what population it enumerated.

Round 2 = `IB-rt-1..IB-rt-11` + `IB-rtb-1`, twelve orders, twelve judgment criteria.

## OUTCOME VERDICTS -- 10 of 10 graded, and the ones this round could not reach are named as such

| outcome | verdict | grounding |
|---|---|---|
| FWD-1 advisor finds an authorized client and opens its relationship | **ADVANCED, NOT REALIZED** | served by `rt-3`, `rt-5`, `rt-6`, `rtb-1`. `RT3-AC2` and `RT6-AC2` PASS on two instruments each; `RT5-AC2` FAILS, and it is one of this outcome's three cells |
| FWD-2 a restricted advisor can use every tab and export ONLY within their scope | **ADVANCED, NOT REALIZED** | six cells (`rt-1,2,3,4,7`, `rtb-1`), all PASS; the outcome bars at EXERCISED against a live restricted session, which no round-2 cell reached |
| FWD-3 advisor reads the provider's performance result in an Opal report | **NOT NARROWED THIS ROUND** | `rt-1`, `rt-8`, `rt-10` PASS, but `W4-S19` (below) removes the round-1 arm this outcome leaned on |
| FWD-4 YCharts sensitivity analysis in the same client context | **NOT NARROWED THIS ROUND** | six cells PASS; `W4-S19` graded UNSOUND AT ITS VINTAGE, and FWD-4's gap is explicitly NOT narrowed by it |
| FWD-5 current holdings organized by models | **ADVANCED, NOT REALIZED** | `rt-3`, `rt-7`, `rtb-1` PASS; `rt-5` FAILS |
| FWD-7 the client directory cannot go quietly stale | **ADVANCED, NOT REALIZED** | `RT6-AC2` PASS on two instruments (the zoned schedule ENABLED at `cron(0 9 ? * MON-FRI *)` America/New_York, and exactly ONE clock read in 917 lines); `rt-5` FAILS |
| FWD-8 a BRANDED report whose narrative states what it is | **NOT NARROWED THIS ROUND** | `rt-8`, `rt-10`, `rtb-1` PASS; `W4-S19` removes the round-1 arm, same as FWD-3/FWD-4 |
| FWD-9 a forwarded holdings email becomes durable and correctly scoped | **ADVANCED** | `rt-4`, `rt-11` PASS |
| FWD-10 a request can only land in its own firm's storage | **ADVANCED** | `rt-4` PASS |
| FWD-11 an Opal user can run reports across ALL firms from one place | **ADVANCED, NOT REALIZED** | `rt-1`, `rt-2`, `rt-3`, `rtb-1` PASS; bars at EXERCISED |

**Round summary: 11 PASS, 1 FAIL across twelve judgment criteria; ZERO outcomes reach REALIZED this round.** That is
not a disappointing result -- round 2 is a REPAIR round and its cells are contract and seam work, not outcome
exercises. **The honest statement is that no round-2 cell was cut to EXERCISE an outcome**, so grading any of them
REALIZED would be this seat inventing a bar the cells were never asked to meet.

## THE ONE FAIL -- `RT5-AC2`, and the answer already exists inside this project

The bar asks a DIRECT, NON-CONDITIONAL question: which host executes the bundle, and does its tree carry pandas and the
silver registry. The record answers **"UNDETERMINED BY ANY READ THIS CELL MADE"** while printing its own denominator as
**"0 hosts identified; 0 runner lines executed"**, and substitutes a precedent plus an inference.

**RULING: the grade stands. A judgment criterion is not satisfied by an inference where the question asked for a
fact.** A criterion that accepts "I could not determine this, but here is what is probably true" converts a measurement
into a belief, and the printed zero denominator is the tell -- it is an honest record of having measured nothing.

**REPAIR: one paragraph, not a re-cut.** `IB-rt-6` already measured that host DIRECTLY in this same project --
`ModuleNotFoundError` for `ids`, with `boto3`, `pandas`, `jsonschema` and `trading_calendar` all resolving. That is the
fact `RT5-AC2` asked for, measured by a sibling cell whose bounds reached the host `rt-5`'s did not. Carry it with its
citation and re-grade. **The cell does not need to go back to the host; it needs to stop answering from its own bounds
when a sibling has the reading.**

## `W4-S19` -- THE RULING TO READ, and it is the third instance of its class this week

Round 1's renderer produced **ONE document from THREE distinct bundles**: three raw `sha256`, one normalized content
hash, an identical 71,944-byte decompressed content stream. `IB-s-14`'s v0.11 arm PASSED **because it compared each PDF
only to ITSELF.**

⛔ **A renderer whose output does not vary with its input cannot evidence that the input was rendered, and every
per-object check passed precisely BECAUSE the comparison was per-object.** `3.0.0_SA_CVO` grades that arm UNSOUND AT
ITS VINTAGE and this seat ACCEPTS the grade without amendment. This is the same disposition this seat asked for on
`OGQ2-AC7`/`AC15`, and it is that class's THIRD instance this week.

**Consequence, stated so no later round inherits a false credit: FWD-3, FWD-4 and FWD-8 are NOT NARROWED by that arm.**
Any round-3 cell that re-evidences them carries a control that **compares ACROSS inputs, never each artifact to
itself** -- render two known-different bundles and require the outputs to DIFFER. A test that cannot fail on identical
output is not a test of rendering.

## THE TWO STRUCTURALLY ORPHANED ROWS -- a defect in the OWNER CONVENTION, and they are placed here

`W4-S25` and `W4-S28` both name a **CELL** (`IB-rtb-1`) as `disarm_owner`. That cell is terminal and closed without
touching either -- `3.0.0_SA_CVO` verified 0 occurrences of each id in its instance. **R-19 says the CVO writes a clock
on an OWNER'S WORD, and a cell cannot give a word**, so a row owned by one becomes unownable the moment the cell ends
and NOTHING NOTICES. Both owner fields also carry a CONDITION rather than an owner.

**RULING (see R-42): a `disarm_owner` is a SEAT, never a cell, an order or a condition.** A cell is a unit of work with
an end; an owner is an addressee that outlives it. Both rows are hereby placed on **`2.0.0_SA_COO~B`**, the live lane
that holds this project, which may re-place either on a named seat it prefers -- an owner that is a live serial is the
whole point.

`W4-S28`'s condition was checked by the CVO and the finding is exact: the fix is in source at `56a6e07e8f`
(2026-09-12T00:03:03Z) and the deployed `irpt-ycharts-generate` was last modified 2026-09-12T05:21:01Z, so the rebuild
ORDERING is consistent with the fix being aboard -- **but the row's own disarm act is a served-`CodeSha256`-against-
built-zip read, and nobody has performed it.** ⛔ **A TIMESTAMP ORDERING IS NOT A BYTES COMPARISON.** It stays ARMED on
a measurement, not on an assumption, and R-40's bar is exactly what that row has been missing all along.

## OTHER RULINGS ACCEPTED AS THE CVO WROTE THEM

- **`W4-S23`:** "0 external connections" is unachievable against the portal as built (12 requests, 2 foreign, both
  Google Fonts, **0 vendor** with the vendor list enumerated). Re-cut to **"0 VENDOR connections"**, which is the number
  the bar exists to protect. Self-hosting the fonts is `IRPT_FNTEND`'s and also closes `RT8-AC2`'s
  0-of-3-declared-fonts finding.
- **`S32`:** both round-1 batteries are now STALE INSTRUMENTS reporting FALSE RED after a correct bundle mint. Any
  citation of their deploy leg is invalid at HEAD. ⛔ **What must NOT happen is re-minting per-file keys to satisfy a
  stale battery** -- that is repairing the world to match a broken instrument.
- **`W3-S15`:** arm (c) is not re-cut as a dataflow census on one instance; its output names EXCEPT HANDLERS as its
  denominator.
- **`W3-S16`:** the FILE is authoritative over a ruling's stated count -- twelve was true when written, eighteen is true
  now, and the fix covered all eighteen because the cell drove it from the CENSUS rather than from the ruling's number.
  **That is the correct relationship between a ruling and a population, and it is the inverse of the error this seat
  made tonight.**

## ROWS: 53 ARMED GRADUATE AND NOT ONE DISARMS

No disarm owner gave a word the CVO could write on, and the five whose named owner is a TERMINATED WORKER SLOT each
carve out explicitly what they did NOT disarm. **Writing those as whole disarms would retire exactly the half the
carve-out exists to keep open.** The CVO was right to write no clock. Every one of the 53 needs a live owner's word,
which is round 3's intake, not a bookkeeping pass.

`IRPT_BCKEND-S56` (the CVO's own row, graduated the same round) is accepted: four citations across three judgment
records TRUE WHEN WRITTEN and wrong at HEAD, none carrying a vintage pin, plus one factual reading that `S43`'s own
authorized delete made false. **None changes a grade** -- the CVO re-derived the substance at both vintages. This is
R-40's prose sibling and the remedy is a vintage pin per citation.

## ROUND 3 -- what it carries

1. `RT5-AC2`'s one-paragraph repair, citing `IB-rt-6`'s direct host measurement, then re-grade.
2. `W4-S25` and `W4-S28` re-owned to live seats; `W4-S28`'s disarm act performed as a BYTES comparison.
3. Any FWD-3/FWD-4/FWD-8 re-evidencing carries an ACROSS-INPUTS renderer control.
4. `W4-S23`'s re-cut bar; `S32`'s stale batteries retired rather than satisfied.
5. The 53 graduated rows' intake against LIVE owners.

**Nothing here is a gate on `2.0.0_SA_COO~B`'s cut.** The recut is that lane's under Rule 27 and this analysis is its
input.
