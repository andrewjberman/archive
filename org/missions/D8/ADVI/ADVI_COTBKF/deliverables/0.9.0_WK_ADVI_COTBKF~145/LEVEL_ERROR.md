# CB-by-3 (round 77, amended): the no-snapshot branch read, then the level error sized where a served reader exists

Worker 0.9.0_WK_ADVI_COTBKF~145. Records: `NO_SNAPSHOT_BRANCH.json` (item A), `LEVEL_ERROR.json` (item B). Tickers, prices, counts and proportions only; no account id or account value.

## Result

No served figure built from an affected close was found. No surprise row was filed (`rows_filed` is empty in both records). `served_readers_from_cell_1` is 0 (the census's 0 plus none from item A); `sized` and `unsized` are empty, which is the complete result.

## Item A: what was read

| Question | Answer | Read from |
|---|---|---|
| Snapshot branch | price = market_value / units, `source` 'bd_snapshot'; writes `gold/canonical/holdings/{date}.parquet` only for dates in `silver/holdings/`; returns before the store is loaded | B_00.canonical_holdings.py:1115-1121, :127-139, :142-221 |
| No-snapshot branch | units x the store's close by asset_name for the date (cash and par names at 1.0); `source` 'bd'; writes the same key layout for every unsealed positions_cube date; cannot run while a snapshot exists; no delete anywhere in the file | B_00:1123-1503, :703-723, :877, :917-924 |
| First snapshot date | 2026-06-08 | live listing of `s3://opal-data-cot/silver/holdings/`: 87 keys seen, complete, first 2026-06-08, last 2026-10-09 |
| Partitions before it | 47, 2026-04-22 to 2026-06-07 (consecutive days), all still exist, all last written 2026-06-09T20:58:26Z-29Z | live listing of `gold/canonical/holdings/`: 134 keys seen, complete; 47 before 2026-06-08, 87 from it, matching the 87 snapshot dates |
| Which branch built them | the no-snapshot branch: the one partition read (2026-06-03) has 8164 of 8164 rows `source` 'bd' | one get-object of that key |
| Can the page be asked for a date | No. The page's calls take a period (monthly, quarterly, annual) and no date; no request was made | cottonwood/index.tsx:116-121; advisor-intelligence.ts:379-421 |
| Does it show those dates | By code yes, as part of its period series: C_03 reads every partition and sums market_value with no filter on source; D_00b reads that output; both are live steps | C_03:199-226, :283-289; D_00b:1195-1202, :1259; ssm.tf:391, :395 |

The 15 funds held on 2026-06-03 (the one partition read): 7 of 15 (ABNFX, FCNTX, GFFFX, MEIIX, NFFFX, SGIIX, VEIRX), matched by asset name through the local bridge because the partition's ticker column is empty. The other 8 are not established as held (3 have a bridge name and no row; 5 have no bridge name).

### One price read: FCNTX on 2026-06-03

| Served holdings | Store close | Unadjusted close | Served / store | Served / unadjusted |
|---|---|---|---|---|
| 26.35 | 26.35 | 26.350000 | 1.0000 | 1.0000 |

The other six held funds on that date show the same three prices (ratios 1.0000). Across the 47-day window, the store's close over the unadjusted close for all 15 funds: min 0.9845, median 1.0000, max 1.0061 over 480 fund-days; none below 0.98. The close is not affected on these dates.

### The three readers the census left not established

| Reader | The one read that would settle it |
|---|---|
| C_05 -> D_00/D_02 tax panels | head `gold/views/client_tax_liability.parquet` and list `gold/timeseries/holdings_lots/` in opal-data-cot |
| IRPT holdings-performance, Cottonwood channel | get-schedule for the two ENABLED schedules (schedule.tf:88-91, :192-195); the source in each Target.Input |
| IRPT performance route, Cottonwood tenant | get-function `irpt-performance-adapter` and the route or portal call that opens it for the Cottonwood tenant |

## Item B

`served_readers_from_cell_1` = 0. `level_by_fund` (served close over unadjusted close on common days, 15 funds): medians run from 0.5647 (PRILX) to 0.9179 (DFLVX); the three lowest are PRILX 0.5647, GFFFX 0.5865, AGTHX 0.5912. The ratio rises toward 1.0 by 2026 (median 1.0 for 12 of 15).

### In the minted, unread table (read by nothing released; NOT a served figure)

| Measure | Value |
|---|---|
| Accounts in the table / holding one of the 15 funds at a value | 1,528 / 407 |
| Account-days valued / holding one of the 15 funds at a value | 1,396,834 / 259,357 |
| Date range of those account-days | 2020-07-06 to 2026-06-08 |
| Funds' share of the account's valued total: median | 0.2276 |
| Share of those account-days above 5 / 25 / 50 percent | 96.3 / 43.1 / 9.9 percent |

## Not established

46 of the 47 pre-snapshot partitions were not read (grant: one partition's rows), so "held on any such date" is at least 7 and at most 15 of 15. The store's close in the window comes from the local cache read 2026-10-08, not the bucket object as it stood on 2026-06-09 (the served price equals it on the date read). The served portal artifacts were not read; the page's use of the early dates is from code. The deployed gold code was not compared with HEAD.

## AWS reads made (all read-only, this firm's bucket opal-data-cot, via `.tools/aws`)

1. `s3api list-objects-v2`, prefix `silver/holdings/` (87 keys).
2. `s3api list-objects-v2`, prefix `gold/canonical/holdings/` (134 keys).
3. `s3api get-object`, `gold/canonical/holdings/2026-06-03.parquet` (to this worktree's gitignored scratch).

Plus two served-graph queries (`comp-find --corpus aws`, nodes S3_BUCKET and LAMBDA). Nothing was written, deleted or served; no other firm's data was opened.
