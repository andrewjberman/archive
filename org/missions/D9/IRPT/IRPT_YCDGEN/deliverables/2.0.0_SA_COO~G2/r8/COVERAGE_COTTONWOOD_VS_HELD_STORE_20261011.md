# IRPT_YCDGEN round 8 -- coverage read: the securities Cottonwood's accounts hold against the held-characteristics store

**By:** `2.0.0_SA_COO~G2`, 2026-10-11 ~07:5xZ, read-only, on `1.0.0_SA_CTO~DELL2` ADDENDUM 8.3 @7f3b2e983a item 1. Counts and
symbol SHAPES only; no account, quantity, price, value, symbol or CUSIP is written. Record beside this file:
`COVERAGE_COTTONWOOD_VS_HELD_STORE_20261011.json`.

## Sources (paths from `2.0.0_SA_COO~C2`, msgs 4405 and 4415; two columns read from each)

| what | where | columns read |
|---|---|---|
| Cottonwood positions | `.scratch/advi_cotbkf/fwd3_serve_r34/account_day_value.parquet` (local copy of the served silver table; 21,102,041 rows) | `cusip`, `date` |
| CUSIP to symbol | `.scratch/advi_cotbkf/tx_cache/trade_year=*/*.parquet` (14 files, 1,416,497 rows; Cottonwood's silver transactions) | `Cusip`, `Symbol` |
| the store | `s3://opal-data-etfs/bbg/2026-10-09/characteristics.parquet` (172 rows, key `<TICKER> US Equity`) | `security`, `CNTRY_OF_DOMICILE`, `GICS_SECTOR_NAME` |

## Denominator

The positions file tapers after 2026-06-01 (30 distinct CUSIPs on its last date, 2026-06-22). The fullest recent date is
**2026-05-06: 826 distinct CUSIPs** over 10,090 rows. That date is the denominator. It is five months old.

## Result

| step | securities | of |
|---|---|---|
| Cottonwood securities held on 2026-05-06 | **826** | |
| ... with a symbol in the transactions cache | 573 | 826 |
| ... with NO symbol there (9-character CUSIPs; asset type not read) | 253 | 826 |
| ... whose symbol is a store key | **72** | 826 (8.7%); 573 (12.6%) |
| ... of those, with `CNTRY_OF_DOMICILE` | 72 | 72 |
| ... of those, with `GICS_SECTOR_NAME` | 71 | 72 |
| store keys Cottonwood holds / does not hold | 72 / 100 | 172 |

`bond_maturity` and the other 69 no-rule inputs have no store column at all (held-store read part 1).

## "Not covered" or "covered under another symbol"? Symbol shapes on both sides

| shape | store keys (172) | Cottonwood, matched (72) | Cottonwood, with a symbol but unmatched (501) |
|---|---|---|---|
| 1 letter | 4 | 4 | 4 |
| 2 letters | 21 | 12 | 24 |
| 3 letters | 69 | 32 | 213 |
| 4 letters | 53 | 23 | 127 |
| 5 letters | 23 | 1 | 131 |
| other | 2 | 0 | 2 |

Both sides use the same plain-letter ticker form, and the 72 matches span every length, so the unmatched are NOT a symbology
mismatch: they are securities the store has no row for. Of the 501 unmatched, **120 are five-letter symbols ending in X**, the
form of a mutual-fund ticker; the store's 23 five-letter keys matched 1.

## Reading

For Cottonwood's real holdings the store covers 72 of 826 securities by count (weights were not read). An Overview for a
Cottonwood portfolio would state "not covered" for most held securities on the 85 rule-fed sections, and those sections
compute over the covered share only. The list to ask the Bloomberg queue for is 754 securities: 501 with a symbol and 253
that first need one.

## Limits

- Counts of securities, not of dollars: a portfolio's covered WEIGHT may be far higher or lower than 8.7%.
- One date, five months old; the symbol source is the transactions cache, which holds no symbol for 253 of the 826.
- A security matched by symbol is assumed to be the same security; no CUSIP is in the store to confirm it.
- Whole-firm union, not per-portfolio coverage.
