# COTTONWOOD_VALUE_RULE24 -- return_basis and method_version for Cottonwood's positions-based returns (IRPT_DASHBD TO-DB-b-114)

Machine record: `COTTONWOOD_VALUE_RULE24.json` beside this file. Authored by 0.9.0_WK_IRPT_DASHBD~89.

**Conclusion: EXISTING_VALUES_SUFFICE. Stamp: return_basis = `TWR`, method_version = `3`.** No value is added.

## The question on the producer's axes
- `return_basis` = which arithmetic produced total_return_daily. Cottonwood's form, (value - flow) / prior value - 1, is the producer's form. TWR.
- Valuation rebuilt from positions, as-traded close, net of fees = which method produced the value. These belong to `method_version`
  (row 3, `positions_based`) and to the entry's own fields `valuation_source`, `price_basis`, `fee_treatment`.

## Postulates
- MECE: the return of a row is produced in 2 ways across the producer and adapter (form computed -> TWR; no number -> NOT_MEASURABLE);
  HOLDINGS_INCOME_FALLBACK is never emitted. Subtraction leaves nothing on the arithmetic axis.
- Same grain: return_basis is account-day; method_version is a per-source fact. A valuation value on return_basis would mix grains.
- Intent coherence: one intent per axis; a combined value would collapse two axes (the defect contract line 166 names).
- State coherence: re-stamping moves return_basis and method_version only; day_quality, guard_state, history_scope, fee and income
  columns and dim row 3's inherited fields do not move. A new return_basis value would move every enum reader and leave method_version unmoved.

## Token census
comp-find word-boundary, corpus=all, 68,382 files scanned (7 ephemeral-floor and 4,272 binary not searched). TWR 2,421 hits / 760 files;
HOLDINGS_INCOME_FALLBACK 48 / 27; NOT_MEASURABLE 10,604 / 309; method_version 1,409 / 496; candidates POSITIONS_BASED_TWR,
AS_TRADED_TWR, POSITIONS_TWR 0 / 0. (The runs overlapped this worker's own scratch, since deleted: at most 2 files and 2 hits.)

## Strongest case against
The contract calls TWR "the C-METHOD form", whose V is the custodian equity; and dim row 3 as written does not itself state as-traded
close or net of fees, and inherits an income basis measured for the custodian channel only. Answer: the contract names the arithmetic and
V is method_version's; the gap is in row 3's text (a METHOD_ROWS edit under its own record), not a missing value. Not established here:
whether a dim row 3 partition exists, the flow timing of the 107,316 rows, and whether row 3's inherited income basis is true for Cottonwood.

## Manifest text at HEAD
`build_manifest` (producer line 1842) writes `method_version` from `method_version_of(src)` (line 1849): 3 for the Cottonwood entry
(sources.json line 125), and `method_text` (line 1826) gives the custodian sentence only for `custodian_reported`, so the entry gets the
generic branch (line 1836). It does not write custodian text or 2. The mint must pass `src=` the `_commonwealth_delivery` entry
(adapter lines 393 and 552) with a frame whose method_version is 3 (adapter lines 326 and 380), return_basis TWR on measured days and
NOT_MEASURABLE on blank days. If new: none.
