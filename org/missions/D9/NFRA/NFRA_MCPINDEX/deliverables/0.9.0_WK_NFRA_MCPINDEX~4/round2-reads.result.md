# NFRA_MCPINDEX.TO-MX-q-2 -- two read-only live reads (R-2 (1) Black Diamond; R-3 Eclipse)

Worker `0.9.0_WK_NFRA_MCPINDEX~4`, worktree `/c/tmp/mx-4`, branch `wk-NFRA_MCPINDEX-4`, cut at `09daf8fb2b`.
Probe: `probes/mx_q_2.py` (`BD` | `ECL`), run as `timeout 120 python <probe> <arm>` from the worktree root; rc=0 for both.
Verbs: `s3:ListObjectsV2` (paginated) and `s3:GetObject` only, through the operator's AWS credentials. Nothing was written to
any bucket, table or pipeline. Aggregate counts only.

## 1. Black Diamond (C-S13, R-2 (1))

Instrument: ListObjectsV2 over `s3://opal-data-bd/silver/transactions/` returned 1,909 parquet partitions. 139 of them have a
filename date on or after 2026-04-14 (`2026-04-14.parquet` .. `2026-09-25.parquet`). For each, the probe read the `cusip` and
`asset_id` columns and counted null cusip, plus blank-string cusip ('', 'nan', 'None', 'NaN').
Denominator: 139 partitions, 3,185,260 rows. Null: 14,367. Blank string: 0. Null cusip on cash rows (asset_id=4): 0.
Read 2026-09-25T15:39:33Z..15:39:58Z.

BD-NULL-CUSIP rows=3185260 null_cusip=14367 since=2026-04-14 source=s3://opal-data-bd/silver/transactions/ read_at=2026-09-25T15:39:58Z

The null rate is 0.45% of rows since 2026-04-14.

Instrument: for each gold figure whose producer joins on cusip AND writes a `cusip` column, the probe read the `cusip` column of
the latest dated partition. Checked (3):

| figure | producer | key read (latest) | rows | null cusip |
|---|---|---|---:|---:|
| holdings_lots | `data/black_diamond/scripts/gold/B_01.holdings_lots.py` (asset_id -> `bd_assets_dim` cusip, :280-305) | `s3://opal-data-bd/gold/timeseries/holdings_lots/2026-09-18.parquet` (latest of 99) | 1,264,679 | 22,172 |
| canonical_lots_unrealized | `data/black_diamond/scripts/gold/B_02.canonical_lots.py` (cusip bridge, :149-180) | `s3://opal-data-bd/gold/canonical/lots_unrealized/2026-07-23.parquet` (latest of 658) | 444,924 | 0 |
| canonical_lots_realized | `data/black_diamond/scripts/gold/B_02.canonical_lots.py` (cusip bridge) | `s3://opal-data-bd/gold/canonical/lots_realized/2026-07-23.parquet` (latest of 1,402) | 769 | 0 |

Read 2026-09-25T15:40:00Z..15:40:01Z.

BD-SERVED-CUSIP-JOINS served_figures_checked=3 carrying_null=1

Not in the denominator, with the reason:
- `B_00.canonical_holdings.py` (`gold/canonical/holdings/`) and `A_03.positions_cube.py` (`gold/positions_cube/`) both build a
  cusip-to-name bridge. Neither writes a `cusip` column: the latest partitions, 2026-09-23, carry none. A null cusip in either
  cannot be read from the output.
- B_01 maps cusip 'CASH' to null (`B_01.holdings_lots.py:291`). The probe did not measure how many of the 22,172 null
  holdings_lots rows are cash.
- Both canonical_lots figures were last written 2026-07-23, so "today" for them means that partition. Filed as row
  `NFRA_MCPINDEX-Z-W4-S2`.

## 2. Eclipse (C-S12, R-3)

Allowlist: `INFLECTION_REP_IDS = {3, 6, 10, 11, 12}` at `data/inf/scripts/silver/_orion_api_silver_lib.py:113`. The probe read
it from the file at HEAD. `filter_to_inflection()` (:301-311) matches it against `rep_id`.

Instrument: ListObjectsV2 over `s3://opal-data-inf/silver/eclipse/` returned 595 objects in 119 dated partitions, the latest
2026-09-25. Neither Eclipse silver table has a rep_id or firm_id column:
- `portfolios_simple` (845 rows) has no column whose name contains rep, firm, advisor or team.
- `portfolios_full` (859 rows) has `team`, with 3 distinct values. Those values are not in the rep_id key space.

So the rep ids came through the producer's own join, `INF_E_00.eclipse_model_portfolios.py:206`:
`portfolios_simple.eclipse_account_id_int` -> `silver/api_dims/accounts_v2/snapshot_date=2026-09-25/data.parquet`
(878 rows) `.account_id` -> `rep_id`. Filed as row `NFRA_MCPINDEX-Z-W4-S1`.
Denominator: 845 rows. 58 have a null `eclipse_account_id`, so no id resolves for them. 0 have an id that does not join. 787
join, with 0 null rep_ids. They carry 5 distinct rep_ids. 0 ids and 0 rows fall outside the allowlist.

ECLIPSE-SCOPE rows=845 distinct_ids=5 outside_allowlist=0 allowlist=data/inf/scripts/silver/_orion_api_silver_lib.py read_at=2026-09-25T15:38:35Z

Not measured here: whether `accounts_v2` is itself filtered to Inflection upstream. If it is, a join hit shows the account is in
the Inflection book, but a non-Inflection Eclipse account would appear as "unjoined", which reads 0. The 58 null-id rows
cannot be attributed either way.
