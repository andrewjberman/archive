# IRPT_YCDGEN round 9, cell YCD-c-9 closed -- per-account value coverage, today and after the 14-symbol list

**By:** `2.0.0_SA_COO~G2`, 2026-10-11, read-only, on `1.0.0_SA_CTO~DELL2` msg 4463 (the unit of the decision is ONE account).
Counts and percentages only: no account id, symbol, quantity, price or dollar figure is written. Record:
`PER_ACCOUNT_COVERAGE_AFTER_14_20261011.json`. Sources and date as `COVERAGE_BY_VALUE_AND_REQUEST_SIZED_20261011.md`
@65246d1752; the 14 symbols are ranks 1 to 14 of that record's ordered list.

## Denominators

| | accounts |
|---|---|
| Cottonwood accounts with positions on 2026-05-06 | **744** |
| ... with at least one unpriced position (excluded) | 685 |
| ... all positions priced AND symbolled, total value positive | **59** |

## Result, over the 59

| value coverage | today | after the 14 symbols |
|---|---|---|
| 90% or more | **1** | **41** |
| 75% to 90% | 2 | 4 |
| 50% to 75% | 5 | 5 |
| 25% to 50% | 2 | 0 |
| 25% or less | 49 | 9 |

Median coverage: 0.0% today, 100.0% after the 14. Of the 41 at 90% or more after the 14, 40 read 100%.

## How large those 41 portfolios are

| positions in the account | the 59 eligible | the 41 at 90%+ after the 14 |
|---|---|---|
| 1 | 23 | 23 |
| 2 to 5 | 28 | 17 |
| 6 to 15 | 7 | 1 |
| 16 or more | 1 | 0 |

So a portfolio for the sitting exists after the 14: 41 accounts. But 23 of them hold a single position and 17 hold two to
five; ONE account with six or more positions reaches 90%.

## Limits

- 685 of 744 accounts are excluded because a position is unpriced in the positions file, not because they are unsuitable; the
  59 are 7.9% of the accounts.
- "Covered after the 14" assumes the store's source can describe each of the 14 for the two fed inputs (country of domicile,
  sector). The 14 include mutual funds and a cash symbol; whether that source describes them is NOT established.
- One date, five months old. A symbol match is assumed to be the same security.
