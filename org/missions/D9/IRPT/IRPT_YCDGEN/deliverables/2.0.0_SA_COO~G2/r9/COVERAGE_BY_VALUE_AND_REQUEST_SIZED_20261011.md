# IRPT_YCDGEN round 9, cells YCD-b-9 and YCD-c-9 -- coverage by value, and the data request sized (not sent)

**By:** `2.0.0_SA_COO~G2`, 2026-10-11, read-only, on the CTO's round-9 analysis @eeb799ce72 section 3 items 2 and 3.
Percentages, counts and ticker symbols only: no account, quantity, price or dollar figure is written. Record beside this file:
`COVERAGE_BY_VALUE_AND_REQUEST_SIZED_20261011.json` (the ordered list is its `sizing.ordered_list`).

## THE LIMIT THAT GOVERNS EVERY NUMBER BELOW

On the date read, **6122 of 10090 position rows carry NO value** in the positions file (`value` is null), and only **367 of the 826**
securities have a positive value. Every share below is a share of PRICED value. An unpriced position counts as zero, so the
253 securities with no symbol (183 fixed income, 50 cash equivalents, 12 annuities, 6 equities, 2 alternatives) read 0.00%
because none of them is priced there, not because they are small. True coverage of ALL held value is therefore unknown and is
LOWER than the covered figure wherever the unpriced positions are large.

## 1. Sources and date

As the coverage-by-count read (`r8/COVERAGE_COTTONWOOD_VS_HELD_STORE_20261011.md` @23a7a1f51c): positions of 2026-05-06
(columns `cusip`, `date`, `value`), the transactions cache (`Cusip`, `Symbol`, `Asset_Type`), and the store
`bbg/2026-10-09` (172 keys). 10090 rows, 826 distinct securities, 2 rows with a negative value.

## 2. Coverage by value (cell YCD-b-9)

| kind | securities | share of priced value |
|---|---|---|
| uncovered: other symbol | 381 | 47.12% |
| uncovered: 5-letter symbol ending X | 120 | 29.87% |
| covered | 72 | 23.01% |
| no symbol | 253 | 0.00% |

The store's 72 covered securities carry **23.01% of priced value** (8.7% by count).

### The uncovered that have a symbol, by asset type

| asset type (transactions cache) | securities | share of priced value |
|---|---|---|
| Mutual Fund | 113 | 24.53% |
| ETF | 133 | 17.26% |
| Equity | 217 | 12.04% |
| Cash | 1 | 10.96% |
| Mutual Fund (Closed End) | 28 | 6.87% |
| Cash Equivalent | 7 | 5.34% |
| Fixed Income | 1 | 0.00% |
| Alternative Investment | 1 | 0.00% |

### The 253 with no symbol, by asset type

| asset type | securities | share of priced value |
|---|---|---|
| Fixed Income | 183 | 0.00% |
| Annuity | 12 | 0.00% |
| Cash Equivalent | 50 | 0.00% |
| Equity | 6 | 0.00% |
| Alternative Investment | 2 | 0.00% |

## 3. The request, sized (cell YCD-c-9). NOT SENT.

Uncovered securities that have a symbol, ordered by value. Adding them in that order takes priced-value coverage from
23.01% to:

| target | securities to add |
|---|---|
| 50% | 4 |
| 60% | 5 |
| 70% | 8 |
| 75% | 10 |
| 80% | 14 |
| 85% | 23 |
| 90% | 46 |
| 100.00% (every security that has a symbol) | 501 |

The first 14 symbols, which reach 80%:

| rank | symbol | cumulative priced-value coverage |
|---|---|---|
| 1 | `CASH` | 33.97% |
| 2 | `PDBZX` | 41.88% |
| 3 | `MIEKX` | 48.53% |
| 4 | `FSMAX` | 55.11% |
| 5 | `FDRXX` | 60.45% |
| 6 | `PHYS` | 64.93% |
| 7 | `PULS` | 68.34% |
| 8 | `VEA` | 71.02% |
| 9 | `PSLV` | 73.19% |
| 10 | `IWD` | 75.06% |
| 11 | `IWF` | 76.84% |
| 12 | `VWIUX` | 78.52% |
| 13 | `MPC` | 79.57% |
| 14 | `SHYG` | 80.50% |

The full ordered list of 501 is in the record. Kinds the store's source may not describe: the store's 172 rows are single
stocks with 8 funds among them (8 rows carry a fund expense ratio), while the uncovered priced value is mostly mutual funds
(open and closed end), ETFs and cash. Whether the store's source can describe a mutual fund's country or sector at all is NOT
established here; if it cannot, those need another source Opal already holds, which is cell YCD-d-9's read.

## 4. Limits

- Priced value only (the governing limit above). One date, five months old, whole-firm union, not per-portfolio.
- A symbol match is assumed to be the same security; the store carries no CUSIP.
- The symbol source is the transactions cache; a held security never traded in it has no symbol there.
- Nothing is asked of Bloomberg: this is a list, not a request. Whoever cuts a request reads `integrations/bloomberg/READ_HERE.md` first.
