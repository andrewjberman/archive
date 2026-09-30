# SCHEMA_MX-s-15 -- Schwab `dim_transaction`, measured live 2026-09-30

Author: 0.9.0_WK_NFRA_MCPINDEX~19. Read-only S3 reads (`aws s3 ls`, one `aws s3 cp` per master to `.scratch/`).

## Key form (measured)

`s3://opal-data-assets/schwab/<master>/silver/dim_transaction/date=<YYYY-MM-DD>/data.parquet` -- the SAME form the
dims read. One object per date partition. The object name `{master}_dim_transaction.parquet` recorded at
`analysis-schwab.result.md:343` is NOT what is in S3 (the producer's own `dim_key()` at
`data/assets/scripts/silver/schwab_projections.py:93-96` builds `.../date=<date>/data.parquet`).

| master | date partitions listed | oldest | newest | newest object |
|---|---|---|---|---|
| 08242234 | 679 | 2024-01-16 | **2026-09-28** | `date=2026-09-28/data.parquet`, 59,293 bytes, 1,271 rows, written 2026-09-29 06:15:53 (local time) |
| 08335338 | 560 | 2024-07-08 | **2026-09-28** | `date=2026-09-28/data.parquet`, 107,339 bytes, 1,983 rows, written 2026-09-29 05:46:30 (local time) |

`date=2026-09-29/` is absent on 08242234 (empty listing, rc=1). The newest partition is 2026-09-28 on both masters.
`dim_position` has the same newest date on both masters (2026-09-28).

## Columns (measured, both masters' 2026-09-28 objects)

44 columns: the 39 pinned by `PROJECTIONS['dim_transaction']` (`schwab_projections.py:55-68`) followed by 5 provenance
columns (`_source_file`, `_source_as_of`, `_master_observed`, `_section`, `_schema_version`, all string).

Served by this cell (15 of 39 pinned; typed from the live Arrow schema):

| field | Arrow type | declared |
|---|---|---|
| account_id | string | `account_ref` (keyed alias; raw id never leaves) |
| business_date, trade_date, settlmnt_date | date32 | date |
| tr_cd, sb_cd, transaction_category, tran_srcde, debit_credit, cusip, ticker_symbol | string | string |
| quantity | decimal128(15,5) | decimal(15,5) units |
| price | decimal128(15,5) | decimal(15,5) USD per unit |
| gross_amount, net_amount | decimal128(15,2) | decimal(15,2) USD |

Not served (24 pinned + 5 provenance): `tran_date`, `transaction_source_code_description`,
`transaction_detail_description`, `industry_ticker_symbol`, `isin`, `sedol`, `tax_code`, `accrued_interest`, the fee and
withholding columns, `closing_price`, `factor`, and the provenance columns.

## Grain (measured)

The producer's own comment says it: "per-partition APPEND, NO row-unique key (refuted from bytes v1.2.1)"
(`schwab_projections.py:52-54`). Measured on both 2026-09-28 objects: no fully duplicated row (0 groups of 1,271 and
1,983), but the natural 4-column key (account_id, tr_cd, cusip, tran_srcde) repeats (32 and 34 duplicate groups, max 2).
A 10-column key (adding sb_cd, detail description, debit_credit, quantity, net_amount, gross_amount) was unique on
those two objects only. One partition does not prove a rule, so `DATASET_GRAINS["dim_transaction"] = None`: paging
refuses. Row `NFRA_MCPINDEX-Z-W19-S1`.

## Values observed at date=2026-09-28 (3,254 rows, both masters)

- tr_cd: TR (trades), FC (cash), IC. debit_credit: DEBIT, CREDIT, and LONG/SHORT on the IC rows.
- quantity, price, gross_amount: no negative value. net_amount: signed (TR/CREDIT negative, TR/DEBIT positive, FC and IC
  zero). The business meaning of the sign is this pass's observation on one date, so nothing is declared summable.
- trade_date, settlmnt_date: 0 nulls.
