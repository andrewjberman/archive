# Black Diamond analysis record, round 5 (MX-a-8): refreshed against today's silver, naming the first tool

read_at: 2026-09-30

Worker `0.9.0_WK_NFRA_MCPINDEX~21`. Cell `MX-a-8` (FWD-4). Structure: MX-a-3's record
(`deliverables/0.9.0_WK_NFRA_MCPINDEX~4/analysis-blackdiamond.result.md`, read 2026-09-21), 9 sections. Every live fact
below carries its read time. Read verbs (all read-only, `.tools/aws` account 313476888478, us-east-1, boto3 from the
worker's scratch): `s3:ListObjectsV2` (paginated) and `s3:GetObject` of individual silver, forwardfill, bronze-fees and
log objects. No write to any bucket. Nothing under `data/cot/` was read or touched.
Bucket: `opal-data-bd`. Read times (UTC): listing 2026-09-30T08:50Z; per-object reads 2026-09-30T08:5xZ-09:05Z.
Legend: MEASURED = read from the object or listing today; CODE = read from repo source at this worktree's HEAD
(CLOUD @3ce0240861); INFERRED = a reading, not a measurement.

## Live prefixes

`s3://opal-data-bd/silver/` read 2026-09-30T08:50Z: **8,061 objects, 2,862,883,282 bytes** (2026-09-21 read: 8,022 objects,
2,847,180,993 bytes). Denominator of the table below: the 9 canonical tables of MX-a-3, which sit in 6 prefixes plus 3
single files. Dated-partition counts and ranges read 2026-09-30T09:02Z.

| table | key shape (MEASURED) | objects | bytes | dated partitions | oldest .. newest partition |
|---|---|---|---|---|---|
| transactions | `silver/transactions/YYYY-MM-DD.parquet` (+ `_README.txt`) | 1,915 | 595,303,680 | 1,914 | 2020-03-06 .. 2026-09-30 |
| allocations | `silver/allocations/YYYY-MM-DD.parquet` | 133 | 146,016,045 | 133 | 2026-01-16 .. 2026-09-25 |
| realized | `silver/realized/YYYY-MM-DD.parquet` (+ `bd_realized_agg.parquet`, `bd_realized_compact.parquet`) | 1,345 | 81,614,142 | 1,343 | 2021-01-04 .. 2026-09-30 |
| unrealized | `silver/unrealized/YYYY-MM-DD.parquet` (+ `unrealized_gain_loss.parquet`) | 75 | 159,734,895 | 74 | 2026-03-27 .. 2026-09-25 |
| fees | `silver/fees/YYYY-MM-DD.parquet` | 1,992 | 207,875,577 | 1,992 | 2020-03-06 .. 2026-09-28 |
| canonical_prices, plus the prefix's daily files | `silver/prices/canonical_prices.parquet`; `silver/prices/YYYY-MM-DD.parquet`; `silver/prices/backfill_telemetry.json` | 164 (prefix) | 155,064,391 (prefix); canonical_prices alone 108,579,247 | 162 daily | 2026-02-22 .. 2026-09-30 |
| bd_assets_dim | `silver/bd_assets_dim.parquet` | 1 | 977,664 | n/a | lastmod 2026-09-29T22:11Z |
| historical_prices | `silver/historical_prices.parquet` | 1 | 39,576,144 | n/a | lastmod 2026-09-29T14:13Z |
| interpolated_prices | `silver/interpolated_prices.parquet` | 1 | 37,864,731 | n/a | lastmod 2026-09-30T00:16Z |

Everything else under `silver/` is EXCLUDED from any tool (named, with the reason, in Read fence): the non-canonical
entries today (legacy monoliths frozen Jan-Feb 2026, two dated backups, `silver/assets/` 1,890 objects newest partition
2026-06-18, `silver/transactions_enriched/` 519 objects newest 2026-04-20, `silver/bd_assets.parquet` 2026-04-14,
control-plane manifests and `.bak` sidecars, `interpolated_prices_summary.json`, `bd_transactions_metadata.json`).
Non-`silver/` top-level prefixes of the bucket (MEASURED 08:5xZ, 31 prefixes): `GOOD_RUN_2026-01-21_1015AM/`,
`_rollback/`, `ajb_workspace/`, `backfill_v2/`, `blackdiamond/`, `bronze/`, `canonical/`, `code/`, `config/`, `debug/`,
`diagnostics/`, `forwardfill_v2/`, `gldrst/`, `gold/`, `investor-reporting/`, `lambda-deploy/`, `lambda-layers/`,
`lambda-packages/`, `logs/`, `platinum/`, `qa-scratch/`, `runs/`, `schwab/`, `scripts/`, `silver/`, `smartx/`,
`ssm-output/`, `status/`, `temp/`, `tmp/`, `v4_output/`. None is in any fence; `schwab/` and `smartx/` belong to other
properties.

Producer per leg (what wrote the bytes that are there today):

| leg | writer of silver | input | last writes (MEASURED today) | how well the producer is known |
|---|---|---|---|---|
| transactions, allocations, realized, unrealized | `data/black_diamond/scripts/silver/merge-daily-incremental.py` (the `bd-silver-merge` Lambda / SSM merge step), header lines 1-75 (CODE) | `forwardfill_v2/{transactions,allocations,realized,unrealized}/*_DAILY_*.xlsx` | silver partitions last-modified 2026-09-30T00:10Z-00:15Z (transactions, realized); allocations and unrealized 2026-09-27T00:14Z / 2026-09-28T21:40Z; `silver/incremental_manifest.json` `last_updated` 2026-09-30T00:15:11Z | silver writer: CODE + timing. The writer of `forwardfill_v2/*` is named by the completion marker itself: `forwardfill_v2/transactions/_complete/2026-09-24.json` (read 08:5xZ) says `"producer": "cot_bronze_ingest.py"`, `"basis": "land_time_measured"`, landed 2026-09-30T00:05:25Z. That script lives under `data/cot/`, which this cell may not read, so its firm behaviour is UNREAD. |
| the four Playwright download documents (`opal-bd-{transaction,allocation,realized,unrealized}-download`) | none | vendor UI login | per `deliverables/0.9.0_WK_NFRA_MCPINDEX~17/ANNOUNCE_MX-s-14.md` (repo record, not re-read live by me): download failed at login in 70 of 70 dated logs, then stripped to merge-only and published 2026-09-29T08:25-08:27Z (unrealized v3, realized v3, transaction v3; allocation re-cut NOT published, served Default 3 / Latest 4). Logs `logs/*-download-2026-09-29.log` exist for all four (listing read 08:5xZ). | DEAD as a vendor download; alive only as the merge wrapper. Feeds nothing new. |
| fees | `convert_fees_to_silver.py` (CODE, docstring lines 1-20: bronze/fees xlsx to `silver/fees/YYYY-MM-DD.parquet` by Trade Date) | `bronze/fees/Fees_OpalCapital_Daily_<from>_to_<to>.xlsx`, a rolling 15-day window | newest bronze object `Fees_OpalCapital_Daily_2026-09-15_to_2026-09-29.xlsx`, 6,555,580 bytes, landed 2026-09-29T22:20Z; newest silver partitions last-modified 2026-09-29T22:21Z | **WRITER UNATTRIBUTED (row Z-W21-S3).** The scheduled Playwright fees document (`bd-fees-pipeline-trigger`, `cron(15 22 ? * MON-FRI *)`, per `ANNOUNCE_MX-s-10.md` lines 100-118) has its newest log on 2026-09-25 (`logs/fees-download-2026-09-25.log`, read 08:5xZ: `TimeoutError ... bd3.bdreporting.com`, `Download exit code: 1`, `SKIP: silver conversion skipped`). Yet the bronze object lands at 22:20Z every weekday after it (09-18, 09-21 .. 09-25, 09-28, 09-29 all read) and silver follows at 22:21Z. Something other than that document's logged path writes it. INFERRED only: the BD REST vehicle (`org/critical_paths/change_management/20260714T1124Z_d1a-bd-rest-vehicle-a_deploy_completion.md` names `Fees_OpalCapital_Daily` in its tenancy probe); not verified here. |
| bd_assets_dim | `build_bd_assets_dim.py` (CODE) | `silver/bd_assets.parquet` | `built_at` column 2026-09-29T22:11:39Z, object lastmod 2026-09-29T22:11Z | writer/trigger not re-read this cell |
| canonical_prices, historical_prices, interpolated_prices | `bd_price_update.py`, `fetch_historical_prices_yfinance.py`, `build_interpolated_prices.py` (CODE, names only) | prices | lastmods 2026-09-30T04:03Z, 2026-09-29T14:13Z, 2026-09-30T00:16Z | trigger not re-read this cell |

## Grain

Each line: table, grain, source of the statement. Measured today from the newest non-empty partition read 2026-09-30.

| table | grain | source |
|---|---|---|
| fees | one row per fee/transaction line per `trade_date`; **the partition filename date equals `trade_date`** (min = max in every one of the 10 newest partitions read 08:5xZ, e.g. `2026-09-28.parquet`: 1,856 rows, 34 columns, 358 distinct `account_id`). A `transaction_id` can appear twice inside one partition when the same account sits under two `relationship_id` values: 43 ids repeated of 1,856 rows on 2026-09-28, the two rows differ ONLY in `relationship_id` (0 full-row duplicates). 0 `transaction_id` overlaps across the 5 partitions 09-22, 09-23, 09-24, 09-25, 09-28. | MEASURED (objects); CODE `convert_fees_to_silver.py:1-20` |
| transactions | `silver/transactions/<date>.parquet` is the **export/ingest date, not the trade date**: `2026-09-30.parquet` holds 7,643 rows with `trade_date` 2026-09-24..2026-09-28; `2026-09-25.parquet` holds 7,637 rows with `trade_date` 2026-07-31..2026-09-25. Partitions overlap; dedup on `transaction_id` is applied by the reader. 74 columns. | MEASURED; CODE `merge-daily-incremental.py:479-507` |
| realized | sliding window per partition: `2026-09-30.parquet` = 10,242 rows, `trade_date` 2026-09-16..2026-09-28 (2026-09-29: 10,915 rows, 09-15..09-25). 15 columns: `open_date, trade_date, unit_cost, account_number, account_id, asset_name, asset_id, symbol, ticker, cusip, ...`. **No proceeds, units or gain column** (MEASURED column list), so a realized-gain figure cannot be computed from this table. | MEASURED |
| allocations | one row per account per `as_of_date` weekly snapshot; `2026-09-25.parquet` 7,257 rows, `as_of_date` = 2026-09-25 (min = max), 94 columns incl. `account_market_value`, `portfolio_group_market_value`, advisor split fields, fee schedule | MEASURED |
| unrealized | one row per open holding per account per weekly snapshot; `2026-09-25.parquet` 111,527 rows, columns `open_date, market_value, unit_cost, account_id, asset_id, asset_name, symbol, ticker, cusip, ...` | MEASURED |
| bd_assets_dim | one row per `asset_id`: 12,146 rows, 22 columns (`cusip, symbol, ticker, asset_class, opal_asset_class, first_seen_trade_date, last_seen_trade_date, txn_count, built_at`, ...) | MEASURED |
| canonical_prices | one row per (`asset_name`/`ticker`, `date`): 12,504,187 rows, columns `date, asset_name, ticker, price, source` | MEASURED |
| historical_prices | (`ticker`, `date`) close: 5,851,369 rows, columns `date, ticker, close, fetch_date, source` | MEASURED |
| interpolated_prices | (`asset_name`, `date`): 4,579,070 rows, columns `asset_name, date, price, data_quality, num_observations` | MEASURED |

## Freshness

Freshness field and newest value per table, read 2026-09-30T08:50Z-09:05Z. "Today" is Wed 2026-09-30 ~09:05Z; T-1 = Tue
2026-09-29 (trading calendar: Mon 09-28 and Tue 09-29 are both trading days).

| table | freshness field | newest value | state today |
|---|---|---|---|
| fees | `trade_date` (= partition date) | **2026-09-28** (last partition; written 2026-09-29T22:21Z) | LIVE daily. Newest `trade_date` is one calendar day before the run that wrote it (single observation of that pattern: run 09-29T22:21Z, newest 09-28); the 09-29 partition is expected from tonight's 22:2xZ run. Writer unattributed (Live prefixes, row Z-W21-S3). |
| transactions | max `trade_date` across the newest non-empty partitions | partition file 2026-09-30; max `trade_date` **2026-09-28** | LIVE but thin: the input workbooks for 09-28 and 09-29 are 4,356 and 4,355 bytes (empty) and the partitions 09-27, 09-28, 09-29 have 0 rows; the newest real rows are trade_date 09-28 in the 09-30 partition. |
| realized | max `trade_date` | partition 2026-09-30; max `trade_date` **2026-09-28** | LIVE daily (sliding window) |
| allocations | `as_of_date` | **2026-09-25** (landed 2026-09-27T00:14Z) | LIVE weekly: since 2026-07-01 the partition gaps are 11 of 20 at 7 days, the rest 1 day. A Friday snapshot is 5 days old on Wednesday by design. |
| unrealized | snapshot date | **2026-09-25** | LIVE weekly, the same cadence (11 of 20 gaps at 7 days since 07-01) |
| bd_assets_dim | `built_at` | **2026-09-29T22:11:39Z**; but `last_seen_trade_date` max is **2026-04-13** and `first_seen_trade_date` max 2026-04-10 | REBUILT (the 2026-09-21 read said last built 2026-04-14, STALE; that part is superseded) but its per-asset transaction aggregates stop at 2026-04-13 |
| canonical_prices | `date` max | **2026-09-30** (11,080 rows on the max date; lastmod 2026-09-30T04:03Z) | LIVE |
| historical_prices | `date` max | **2026-09-28** | LIVE (T-2 at the read) |
| interpolated_prices | `date` max | **2026-09-28** | LIVE (T-2 at the read) |
| `silver/assets/` (excluded) | partition date | 2026-06-18 | STALE, 104 days |
| `silver/transactions_enriched/` (excluded) | partition date | 2026-04-20 | DEAD (superseded by inline cusip enrichment, CODE `merge-daily-incremental.py:509-511`) |
| the 5 vendor-download documents (fees, transaction, allocation, realized, unrealized) | n/a | fees: newest log 2026-09-25, a login failure; the other four: logs dated 2026-09-29 exist (contents not read) | DEAD as downloads per the MX-s-14 record (see Live prefixes) |

No stale or dead leg feeds the first tool. The fees leg is live; its ONE open provenance fact (the writer) is a filed
row, not a staleness.

## Scope rule

**There is no key segment in `opal-data-bd/silver/` that separates firms.** Every key read today has the shape
`silver/<table>/<date>.parquet` or `silver/<table>.parquet` (key shapes MEASURED on all 6 dated prefixes: 1-3 shapes each,
none carries a firm or master token). What the world offers instead, in order of strength:

1. **The bucket.** `infra/logic/registry/scopes.json` (CODE, this worktree's HEAD) lists the spelling `opal-data-bd` as a
   graded ALIAS of firm `49financial`'s bucket (`opal-data-49financial`); `49financial.pipeline_trees` names
   `data/black_diamond/` with `separated_from: ["cottonwood"]`. Cottonwood's Black Diamond data is a different tree
   (`data/cot/`) and a different bucket (`opal-data-cottonwood`, master `z09`). So this bucket holds one firm's BD data.
2. **The row-level marker.** Black Diamond account ids carry the firm-instance prefix: the `scopes.json` row `z09` says
   Cottonwood's accounts carry `z09` and "49 Financial's Black Diamond ids carry z08, zero overlap". MEASURED today on
   `account_id`: fees 2026-09-28 1,856 of 1,856 `z08`; the 60 newest fees partitions (2026-07-31..2026-09-28) 47,464 of
   47,464 `z08`; transactions 2026-09-30 7,643 of 7,643; realized 2026-09-30 10,242 of 10,242; allocations 2026-09-25
   7,257 of 7,257; unrealized 2026-09-25 111,527 of 111,527. Zero `z09` rows in every object read (the full history of
   fees and the other tables was NOT scanned).
3. The `bd` token is NOT a scope token for naming: `scopes.json` marks `bd` as refused in every naming slot.

**The scope rule the first tool binds:** the tool takes `scope` as an explicit argument (C3); `scope` must be the firm key
`49financial` (validated against `scopes.json`, class FIRM); **a principal resolves only its own firm** (its identity's
firm, never a caller-chosen value) and the call is refused when the principal's firm is not `49financial`; a
`cottonwood`, `inflection`, `demo`, `global` or master-shaped value is refused, never translated. **The first tool never
reads across firms**: it reads exactly one prefix of one firm's bucket, and as a second fence it asserts every returned
`account_id` starts with `z08` and refuses the WHOLE answer (fail closed) if one does not. Because no key segment carries
the firm, the firm binding is held by (a) the read role's single-prefix fence and (b) the `z08` assertion, not by a key
segment. This is recorded as row Z-W21-S2.

## Never-sum

Each rule with its reason class. Rules 1-4 bind the first tool's answer; the rest bind later tools.

1. **Fee columns are summed only after de-duplicating on `transaction_id`** (same account under two `relationship_id`
   values produces two rows with identical amounts: 43 of 1,856 ids on 2026-09-28). Reason: double count (non-additive rows).
2. **`basis_points`, `flat_fee`, `fee_schedule_*`, `units`, `market_value` and `income` are never summed and never presented
   as fees.** `flat_fee` and `basis_points` are schedule parameters present on 1,856 of 1,856 rows, `market_value` is the
   trade value, `income` is dividends or interest (52,507.19 on 2026-09-28), not a fee. Reason: non-additive field.
   (`account_fee` is nonzero on 11 of 1,856 rows and `transaction_fee` on 486 of 1,856 on 2026-09-28: MEASURED.)
3. **Never sum across firms or masters**: `49financial` only; never combined with Cottonwood's Black Diamond tree or any
   Schwab master. Reason: cross-firm (`scopes.json` `separated_from`).
4. **A range answer states its dates and never fills an absent partition with zero**: the partition for a date that has no
   object (today: 2026-09-29) is `NO_PARTITION`, not 0 fees. Reason: cross-date, C4.
5. Snapshot tables (allocations, unrealized) are never summed across `as_of_date`; `portfolio_group_market_value` repeats
   on every account row of a group and is never summed across accounts. Reason: cross-date and non-additive.
6. Transactions and realized are never summed across partitions without de-duplicating on the business key (windows
   overlap: transactions 09-25 and 09-30 partitions share trade dates). Reason: cross-date.
7. Prices are never summed; realized and unrealized are never combined unlabeled. Reason: non-additive, different basis.
8. AUA is never derived from summed flows (README warning carried from MX-a-3). Reason: wrong basis.

## Common questions

Numbered; source = reasoning from the tables' columns and the README's documented pages (as in MX-a-3); **none is measured
user demand** (no query log or usage telemetry exists for this pre-launch tool set). The list keeps MX-a-3's 10 classes,
re-stated against today's columns; the route of each is in Question to tool.

1. What fees were charged to account X (or relationship Y) on date D, or across a range? Table `fees`; fields `trade_date, account_id, relationship_id, transaction_fee, account_fee`. **FIRST TOOL.**
2. What is account X's market value at the latest allocation snapshot, and what is its fee schedule? Table `allocations`; `account_id, account_market_value, account_fee_schedule, basis_points, as_of_date`.
3. What does account X hold now? Table `unrealized`; `account_id, asset_name, ticker, cusip, market_value, unit_cost`.
4. Which assets did account X sell in a period? Table `realized`; `account_id, trade_date, asset_name, unit_cost`. (Not a gain figure: the table has no proceeds column.)
5. What transactions hit account X in a date range? Table `transactions`; `account_id, trade_date, transaction_type, asset_name, units, market_value`.
6. What is asset A (by cusip or ticker): class, classification? Table `bd_assets_dim`; `cusip, ticker, asset_class, opal_asset_class`.
7. What was the price of asset A on date D? Table `canonical_prices`; `date, ticker, asset_name, price, source`.
8. Who is the advisor, architect, consultant or implementor of account X and what are their splits? Table `allocations`; the `*_split_pct` fields.
9. How fresh is each Black Diamond table? The freshness field of each table (Freshness section).
10. What were NNA flows by category (NMNC, NMEC_NA, NMEC_SA, OUTFLOW)? Needs per-client sequential state over the full transaction history; `silver/transactions/` carries no `is_nna*`/`nna_category` column (MEASURED column list, 74 columns).

## Question to tool

**The first tool: ONE question class, ONE tool.**

- Question class: **question 1, fees by account or relationship for a trade date or date range.** Why this one: it is
  fresh (newest 2026-09-28, daily, 1,992 partitions), answerable from ONE prefix (`silver/fees/`), has a clean grain
  (partition date = `trade_date`), and is a question a fee-billing or advisor user plausibly asks (reasoning, not measured
  demand). The alternatives were weaker today: transactions is thin (empty inputs 09-28 and 09-29) and its partitions
  overlap; realized has no gain column; allocations and unrealized are weekly and cross-row-state heavy.
- Tool name: **`blackdiamond_list_fees`**. C3 check: `{system}_{function}[_{qualifier}]`; `system` = `blackdiamond`, a key of
  `infra/logic/registry/systems.json` (49 keys read; VENDOR class); `function` = `list`, a base-form verb; qualifier =
  `fees`; scope is an argument, not in the name.
  **The order asked for a name starting `bd_`. That cannot be C3-valid:** `bd` is not one of the 49 `systems.json` keys and
  `scopes.json` records `bd` as a token refused in every naming slot ("the vendor is blackdiamond, the firm is
  49financial"). A `bd_*` name would be refused by MX-n-1's validator at registration. The name chosen is the C3-valid one;
  the conflict is filed as row Z-W21-S1. If the issuer rules `bd_` anyway, only the name string in MX-t-13 changes; every
  other fact below is unchanged.
- Arguments (for the builder): `scope` (required, must resolve to `49financial` for the principal); `date_from`, `date_to`
  (`trade_date`; both default to the newest partition; span capped at 31 days); optional `account_id` (must start `z08`),
  optional `relationship_id`; row cap 200 with a `truncated` flag.
- Answer (C4 envelope): scope `49financial`; `as_of` = newest `trade_date` returned; `complete`/`truncated`; source dataset
  `opal-data-bd/silver/fees`; `partitions_read` and `partitions_absent` (dates with no object, reported as `NO_PARTITION`).
  Rows carry `transaction_id, trade_date, account_id, account_name, relationship_id, asset_name, cusip, transaction_fee,
  account_fee, income, fee_schedule_type, fee_schedule_rate_type`. Totals: `transaction_fee` and `account_fee` only,
  per `trade_date`, after de-duplication on `transaction_id`.
- Route of every other question (every common question is assigned):

| # | question | route | reason |
|---|---|---|---|
| 1 | fees | `blackdiamond_list_fees` | the first tool |
| 2 | account market value and fee schedule | a later tool, `blackdiamond_get_allocation` | weekly snapshot, repeated group-level values (never-sum 5) need tool-side handling; not in this fence |
| 3 | current holdings | typed query (C6) once `unrealized` is declared to it | single-table filter, no cross-row state |
| 4 | what was sold | typed query | single-table filter; no gain column, so no gain tool is possible from silver |
| 5 | transactions in a range | a later tool, `blackdiamond_list_transactions` | overlapping partitions and reader-side dedup (never-sum 6) need tool-side handling; held until the leg's input is non-empty |
| 6 | asset lookup | typed query | single-table point lookup; note `last_seen_trade_date` stops 2026-04-13 |
| 7 | price on a date | typed query | single-table point lookup |
| 8 | advisor attribution and splits | typed query | single-table filter on `allocations` |
| 9 | freshness | `opal_discover` (cross-property, reserved `opal` system), not a BD tool | not a property question |
| 10 | NNA flows by category | a later tool, `blackdiamond_classify_nna` | per-client sequential state over full history; no NNA columns in silver |

## Read fence

The first tool, `blackdiamond_list_fees`, reads **exactly one prefix and nothing wider**:

- `s3://opal-data-bd/silver/fees/` (objects `silver/fees/YYYY-MM-DD.parquet`; 1,992 objects today; the prefix holds no other
  key shape, MEASURED 08:5xZ).

For MX-t-13's read role: `s3:GetObject` on `arn:aws:s3:::opal-data-bd/silver/fees/*`; `s3:ListBucket` on
`arn:aws:s3:::opal-data-bd` with condition `s3:prefix` = `silver/fees/*` only. Nothing else in the bucket: no `bronze/`,
no `forwardfill_v2/`, no other `silver/` table, no `logs/`.

Excluded, with the reason (every table outside the first tool's fence, today's read):

- `silver/transactions/`, `silver/allocations/`, `silver/realized/`, `silver/unrealized/`, `silver/bd_assets_dim.parquet`,
  `silver/prices/canonical_prices.parquet`, `silver/historical_prices.parquet`, `silver/interpolated_prices.parquet`:
  live tables whose questions route to a later tool or the typed query (table above); a later tool's cell adds its own prefix.
- `silver/prices/YYYY-MM-DD.parquet` (162 files): the gold-trigger artifact, rows already in `canonical_prices`.
- `silver/assets/`, `silver/transactions_enriched/`, `silver/bd_assets.parquet`, `silver/bd_allocations.parquet`,
  `silver/bd_aua_timeseries.parquet`, `silver/bd_nna_daily.parquet`, `silver/bd_nna_by_architect.parquet`,
  `silver/bd_canonical_timeline.parquet`, `silver/aua_validation_log.parquet`, `silver/daily_aua.parquet`,
  `silver/daily_aua_firm.parquet`, `silver/daily_flows.parquet`, `silver/daily_positions.parquet`,
  `silver/nna_timeseries.parquet`, `silver/historical_dividends.parquet`, `silver/historical_prices_20260213.parquet`,
  `silver/historical_prices_final.parquet`, `silver/bd_transactions_backup_2026-01-20.parquet`,
  `silver/bd_transactions_backup_2026-01-28.parquet`: stale or legacy (newest 2026-06-18 and older), superseded, or backups.
- `silver/incremental_*manifest.json*`, `silver/bd_transactions_metadata.json`, `silver/interpolated_prices_summary.json`,
  `silver/prices/backfill_telemetry.json`: control-plane files, not data tables.
- Every non-`silver/` prefix of the bucket (31 listed in Live prefixes), including `schwab/` and `smartx/` which belong to
  other properties, and `platinum/`, served tier, which is a different grant class.
- Finding, not a fence line: the LGIC builder address for this property is `opal-data-assets/blackdiamond/49financial/...`
  per MX-a-3 (R19 migration gap, unchanged); the fence above targets the LIVE location.

## No-data

Black Diamond HAS live silver data today (8,061 objects, 2,862,883,282 bytes under `silver/`), so the "no data, propose no
tool" branch does not bind and one tool is proposed. Within the property: `silver/fees/` has no partition for 2026-09-29
(arrives with tonight's run); `silver/transactions/` holds 0-row partitions for 2026-09-27, 2026-09-28 and 2026-09-29;
allocations and unrealized have no partition between weekly snapshots (2026-09-26 through 2026-09-30 today). The tool renders
each of these as `NO_PARTITION` or a stated empty partition with its date, never as zero fees (never-sum 4, C4).

## Surprise rows filed by this cell

`NFRA_MCPINDEX-Z-W21-S1` (the `bd_` name cannot be C3-valid), `-S2` (no firm key segment exists in this bucket), `-S3` (the
fees writer is unattributed while the scheduled document's last log is a login failure).
