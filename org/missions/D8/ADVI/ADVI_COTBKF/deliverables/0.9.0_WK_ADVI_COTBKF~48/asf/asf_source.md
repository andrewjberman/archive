# ASF source (CB-z-1)

## The decision rule, fixed before the counts

SOURCED only if (a) a repo document that states a treatment names ASF, or (b) EVERY ASF row sits in the same account, on the same day, at the same signed Amount, beside a row of ONE other type whose treatment a source already states (drag: METHOD_DRAG; flow: METHOD_CHARGE_FLOWS, R25_CHARGE_FLOWS; income: METHOD_INCOME). One uncovered row makes the type NO-SOURCE; a treatment is never chosen for part of a type or from its effect on a grade. Otherwise NO-SOURCE, internal.

## The census

- rows: 6; accounts: 1 (B3S606537); trade dates 2019-01-18 to 2019-01-22
- signs: 3 credit, 3 debit, 0 zero; net Amount 0.00; gross |Amount| 5295.98
- Transaction_Description (the delivered field): 'ASF' x6
- CUSIP lines: CFNCASH x6
- note kinds (dates and tag removed): 'Fee Reversal' x3; 'Returned Payment' x3

## Each row and what it sits beside

| account | day | Amount | note kind | tag | other types at the same account, day and Amount | opposite ASF rows (same tag) |
|---|---|---|---|---|---|---|
| B3S606537 | 2019-01-18 | 251.48 | Fee Reversal | B3S606540 | ManAltF | 1 |
| B3S606537 | 2019-01-18 | 276.46 | Fee Reversal | B3S606539 | ManAltF | 1 |
| B3S606537 | 2019-01-18 | 2120.05 | Fee Reversal | B3S606541 | ManAltF | 1 |
| B3S606537 | 2019-01-22 | -2120.05 | Returned Payment | B3S606541 | none | 1 |
| B3S606537 | 2019-01-22 | -276.46 | Returned Payment | B3S606539 | none | 1 |
| B3S606537 | 2019-01-22 | -251.48 | Returned Payment | B3S606540 | none | 1 |

- rows beside a row of another type at the same Amount: 3 of 6; beside ONE type with a stated treatment: 3 of 6
- the other types seen: ManAltF (stated treatment: flow)
- rows with an opposite ASF row of the same tag: 6 of 6

## Documents

- the CRO's research (RESEARCH_20261008_COMMONWEALTH_TWR_METHOD.md): read; lines naming ASF: 0
- the delivered field: Transaction_Description is the three letters ASF on every row and names no fee; the notes read 'Fee Reversal' and 'Returned Payment' for a quarterly fee period and say nothing of the type's treatment

## The state

- state NO-SOURCE, treatment internal, source none-pair-covers-3of6 (3 of 6 rows covered).
- ASF stays INTERNAL (inside the return, no flow), carried with 6 rows. `method_r26` is `method_r25`.

ASF-SOURCE state=NO-SOURCE rows=6 treatment=internal source=none-pair-covers-3of6
