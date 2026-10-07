# Commonwealth transactions: exact repeats in the applied silver table (ADVI_COTBKF CB-h-1)

Measured by `data/assets/scripts/analysis/commonwealth_tx_repeats.py` on the applied silver transactions table (data date 2026-06-23),
read-only, key = the 20 vendor columns (the 5 lineage columns, such as `source_record`, are not part of the key):

`TX-REPEATS rows=1416497 exact_repeat_rows=1360 distinct=1415137 key=20_vendor_columns`

- The table holds 1,416,497 rows. 1,360 of them repeat an earlier row on all 20 vendor columns; 1,415,137 rows are distinct.
- The measured 1,360 equals the figure the early row W2-S1 gave for the records "identical in all 20 vendor columns". The 1,415,137 that row
  said silver would keep is the number of distinct rows here, not the applied row count.

## Why the applied table holds them (cited, not re-derived)

The ratified PRD keeps every delivered record. `org/missions/D8/ADVI/ADVI_COTBKF/prd/ADVI_COTBKF_PRD.md` line 114 (C-SILVER: "holding EVERY row of
the file: two identical lines are two rows") and lines 204-206 (v0.4 addendum item 1: "C-SILVER clarified: every delivered row is kept. Without
a transaction id, two identical lines may be two real events ... rebuilt with all 1,416,497 records"). The writer agrees:
`data/assets/scripts/silver/commonwealth_transactions.py` lines 13-15 ("nothing is de-duplicated").

So a repeat is two real records kept by design, not a write that skipped a drop.
