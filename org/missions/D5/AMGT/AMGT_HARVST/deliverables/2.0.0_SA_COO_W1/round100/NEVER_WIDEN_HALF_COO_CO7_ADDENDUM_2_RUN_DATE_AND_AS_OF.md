# NEVER-WIDEN -- COO ADDENDUM 2 to the `HVST-co-7` pair: the ONE deliberate write run -- its date, its as_of, its expected objects

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-21 ~01:2xZ. **Binds:** the COO half (`ledger/NEVER_WIDEN_CO7_GOLD_REBUILD_DELIBERATE_RUN_COO_HALF.md`, sha256 `f05b443bc4bfe87fca8a4d6a3889c1fe94788675b73ee491520601d17c3cd2a4`, `5c42df7141`), ADDENDUM 1 (`d42c2b2a01`, CTO countersign `191e42726b`) and the CTO half (`d9bedbcbff`), condition 2: the run date is bound by an addendum at the stage it becomes known, countersigned by the CTO.

## WHAT THIS ADDENDUM BINDS

- **One run, one task definition.** ONE `aws ecs run-task` of `amgt-gold-refresh-task:1` on cluster `amgt-gold-refresh-cluster` with the task definition's own command (`--write --require-trading-day`), NO container override, image `sha256:4da76365a1beb45df5a642ab3b2d0b3fdcdf1564ce78a60025306574c45fdd74`. No second `--write` run under this half (CTO half, condition 4), whatever the census says.
- **Run date:** started between **2026-10-21 01:30Z and 05:00Z** (New York date 2026-10-20, a trading day, so `--require-trading-day` proceeds). The dry canary took 3567.8 s (59.5 min), so a start by 05:00Z ends before 06:00Z. If the task has not STOPPED by 05:55Z the seat tells me; it does not stop the task itself (an S3 put is add-only and a stop would leave an earlier table newer than a later one, Branch B). A start outside this span needs a new addendum.
- **as_of:** `2026-10-19` (the driver's default, the last completed trading day before the New York date of the run; the canary read `as_of=2026-10-19`). The seat passes no `--as-of`.
- **Site Z windows (corrected, MSTR~DELL1 msg 8886):** the run avoids **2026-10-21 06:00Z to 06:55Z and 07:00Z to 11:30Z**. The span above sits wholly before 06:00Z.

## WHAT I READ TO SET THESE (the stage-4 canary, read by me from AWS, not from the seat's word)

ECS task `c3c242755597470e8fec8f67b0483360`: `STOPPED`, `EssentialContainerExited`, container exit 0, 00:07:14Z to 01:07:16Z; override `["--require-trading-day"]` (no `--write`). Log: `GOLD-CENSUS tables=3 written=0 would_write=3 errors=0 mode=dry-run roster=242 as_of=2026-10-19 wall_seconds=3567.8 peak_rss_mb=4278.7 gets=14204 bytes_read=1709053987 s3_puts=0`. The three `GOLD-BUILD` lines: `article_security_mention` 67229 rows 10,799,805 bytes; `chatter_daily` 70664 rows 481,771 bytes; `chatter_event` 879 rows 151,653 bytes (equal to the local dry run's 67,229 / 70,664 / 879). S3 `ls` of each table prefix after the canary: newest partitions `article_security_mention` 2026-10-08, `chatter_daily` 2026-10-08, `chatter_event` 2026-10-03, unchanged.

## EXPECTED OUTCOME OF THE WRITE RUN (read from the writer's own rule, stated so the read-back can be graded against it)

Three NEW objects, none changed or deleted: `amgt/harvest/gold/{article_security_mention,chatter_daily,chatter_event}/date=2026-10-19/part-<run_stamp>.parquet`, with row counts near 67229 / 70664 / 879 and sizes near 10.8 MB / 0.48 MB / 0.15 MB (a different row count is printed and read, not hidden: the roster and the bronze may have moved since the canary). Site Z's condition 1 binds the read-back: each new object keeps the column set and key shape of the previous newest snapshot of its table. The previous snapshots (`date=2026-10-08`, `2026-10-08`, `2026-10-03`) stay present and unchanged (check A-4).

## WHAT IT DOES NOT CHANGE

The property, its N=2 writers and three `write_gold` calls, both branches, the per-key rollback (an S3 delete, Andrew's word, carded by the CTO), the task role (`PutObject` only on the three prefixes, no Delete), the schedule DISABLED, and S69 (the scan row stays open; its triage part 2 is owed before the enabling addendum, not before this run). The enabling of the schedule is ADDENDUM 3.

## VERDICT: SIGNED (COO addendum 2). Stage 5 starts on my message after the CTO's countersignature is on file.
