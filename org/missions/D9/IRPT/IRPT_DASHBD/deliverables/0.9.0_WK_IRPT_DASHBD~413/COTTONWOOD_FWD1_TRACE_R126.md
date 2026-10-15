# Cottonwood FWD-1 trace, round 126, cell DB-c-21 (read only)

Worker 0.9.0_WK_IRPT_DASHBD~413. Record: COTTONWOOD_FWD1_TRACE_R126.json (same folder). Reads by UTC 2026-10-15T14:31Z to 14:32Z.

## Silver (Black Diamond, Cottonwood)

- fact_holdings: 94 date= partitions, newest 2026-10-14.
- fact_allocations: 145 date= partitions, newest 2026-10-14.
- Bucket and prefixes come from the account_dim producer's silver_locations(); the function needs a day argument, so the read passed the placeholder 2000-01-03 and kept the prefix.

## Gold (Cottonwood)

- holdings_performance_daily: newest 2026-10-14, 1001 rows, 1001 distinct accounts (column account_id).
- account_dim: newest 2026-10-14, 1004 rows, 226 households, 37 accounts without a household.
- Crosswalk (account_id, stripped string): overlap 1001, only in holdings 0, only in account_dim 3.
- Account forms match in both tables (account_id, str().strip()).

## Reporting gold (the build)

- The scheduled handler (reporting-gold/handler.py) takes its firm from the first custody entry of sources.json. That file holds one custody entry, and its registry master resolves to a firm other than cottonwood. No cottonwood key exists in it.
- The handler's filled-report households call is the built-in firm adapter (FirmAdapter), which reads that firm's household crosswalk. It never calls the Cottonwood reader.
- The schedule (reporting-gold/schedule.tf) fires only this handler; it has no Cottonwood event.
- The Cottonwood reader, called read-only through the same newest-partition rule, returns 226 households from the 2026-10-14 partition. That is the reader's own behaviour, not the build's.
- The build writes no Cottonwood filled report. Output prefix null, object count 0.
- Absent kinds for Cottonwood: account_activity_daily, account_lot_realized, account_lot_unrealized_daily, account_class_daily (NO_SOURCE_YET).

## Hop verdicts

1. silver_to_gold_holdings: HOLDS. Both newest partitions are 2026-10-14; the row-level tie to silver was not compared.
2. silver_to_gold_account_dim: HOLDS. Both silver inputs and the gold account_dim land 2026-10-14; account_dim holds 3 accounts beyond the holdings set.
3. gold_to_reporting_gold_households: BREAKS. The Cottonwood account_dim is not the households source of the scheduled build; the build's households come from another firm's crosswalk. scheduled_for_cottonwood = false.
4. reporting_gold_output: BREAKS. The scheduled build writes no Cottonwood filled report; the output is absent by construction.

## Method notes

- Two runs of the same read-only script were made. The first run missed the partition date in the reader's key (a parse bug, fixed); the reads block counts both runs: 10 LIST calls, 6 GET calls, 0 writes, 0 invokes.
- Scheduling state was read from the Terraform files only, not from the live scheduler.
- No account or household id appears in this note or the record.
