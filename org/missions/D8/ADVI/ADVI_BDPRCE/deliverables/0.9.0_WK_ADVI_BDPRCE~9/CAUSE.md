# BP-b-5 -- why six daily price files are missing, and why the served client objects run a day behind

Record: `CAUSE.json` (same folder). Read-only; nothing was re-run, invoked, written or edited on AWS or in the product tree.

## What ran and what did not on the six dates

The six dates are 2026-09-21, 09-22, 09-28, 09-29, 10-05 and 10-06. All are Monday or Tuesday run dates. The chain starts every day at 00:00Z, and the runner did run on all six. On each of those dates the day's transaction file was first written as an empty file (header only, zero data rows, about 4,356 bytes). Every other run date in the window had rows at first landing. The same is true of the earlier Monday and Tuesday run dates from 2026-09-14 to 10-13, and it is the signature that matters here.

The runner writes a "bronze complete" sentinel only when every table is complete. The runner code that was live until 2026-10-07 withheld the sentinel on the empty transaction file, and it still printed "OK: bronze sentinel emitted". S3 has no sentinel object for any of the six dates. No sentinel means the S3 event never reaches the silver-merge Lambda, so the price Lambda `bd-price-update` is never invoked and no `silver/prices/<date>.parquet` is written.

For 2026-10-05 and 2026-10-06 the logs are still inside the 14-day retention. Neither the silver-merge Lambda nor the price Lambda logged anything on those days, so their class is NO_RUN. For 2026-09-21, 09-22, 09-28 and 09-29 the logs have already expired (the oldest readable event is 2026-09-30), so the class is NOT_DETERMINED. The S3 evidence has the same signature for all six. The transaction file was re-landed with rows three days later, but nothing rewrites the sentinel for a past run date.

Schedule is not the cause. The start job fires every day, and the runner's own daily rule is disabled, so it is not the trigger either.

## Why the served client objects are a day behind

The producer is `D_02.advisor_client_detail.py`, which runs in the gold chain. It sets `data_as_of` to the newest date in its input, `gold/timeseries/account_performance.parquet` (D_02 lines 2874 and 2937). That input's newest date is 2026-10-09, with no rows for the weekend of 10-10 and 10-11. Those weekend rows are present in earlier weekends. The code has no T-1 rule, so the one-trading-day lag is not by design as documented. It is the input's frontier. Where that frontier stops upstream is not established by this cell.

Of 3,510 served client objects, 3,267 carry 2026-10-09 and 243 are older. The 243 were not regenerated in the latest run, and their bodies have no closed or inactive field, so their status is not known from the bodies.

## Defect or not

The missing daily files are a defect in the pre-2026-10-07 runner: it withheld the sentinel on a valid empty window and then reported success. The deployed code has been fixed since 2026-10-07 (commit `3709ae40d6`). Sentinels for 2026-10-12 and 2026-10-13 are present again. The six gaps are not repaired.

The one-day lag is not a documented design rule. The producer is faithful to its input, so the defect, if any, sits upstream, in the ledger that feeds `account_performance`.

## The fix a later cell would make (named, not made)

A later cell would backfill the six run dates. It would re-emit the sentinels, or run the silver merge for those dates, then check that `bd-price-update` writes the six daily files. It would also trace why the account ledger stops at 2026-10-09, and decide whether the producer should carry an explicit as-of basis. Each of those is a write, so none is done here.
