# IRPT_DASHBD round 129, workstream B-IN (Inflection) -- drain-end (issuer 2.0.0_SA_COO~I2, 2026-10-15 ~23:5xZ)

**One order (a LOCAL build), drained and graded on the LANDED tree; no vendor call, no S3 write, nothing deployed, nothing run on real data, no client data.** Issued @aa1224e01e (merged @47f90050e2), drained: `DB-i-16` (~316, merged @0350741d4c). On the merged tree `DBI129-1-AC1`, `AC2` and `AC3` PASS and the proof instance reads VALID. `round-close-check --project IRPT_DASHBD --round 129 --workstream B-IN` reads **MAY-CLOSE** (1 order, 0 judgment criteria). Push state: LOCAL on box/dell2, not read against origin. Cut on the CTO's round-127 ADDENDUM 1 (msg 8736). The CTO wrote "round 128"; 128 is the `cause_claim` line (DB-i-15, drained @b421b07328).

## What exists

`deliverables/0.9.0_WK_IRPT_DASHBD~316/run_scope_feed_real.py` (213 lines) and its 13 tests. `run_real(reader, out_dir, dim_ids, trading_days_fn, firm, method_version, max_reads)` lists the feed's silver, reads it through the GET-only reader, calls the round-127 wrapper into a private directory, and returns counts only: the Orion boundary measure (pairs, pairs equal, max relative difference in basis points), a 238-to-365-day chain check, and `NO_SILVER_YET` / `STOPPED_AT_CAP` as recorded results (nothing written). `main` wires the estate's own dimension builder and `lib/trading_calendar.py`; it is not exercised until the feed's silver exists.

**What the chain check is NOT:** it compares the table's chained rows with the product of the silver's own daily factors, a consistency check of the adapter and wrapper on real rows. A comparison with Orion's REPORTED period return needs a vendor call and a window the backfill provides, and is not built. The CTO's wording ("the 238-365 day chain check") can be read either way; I built the one that needs no vendor call, as his message required.

## A defect I found at this drain, and its repair (round 130)

Reading the feed script to see what the run script will meet, I found that **the wrapper I specified in round 125 would refuse the first real silver.** The feed writes ONE partition per calendar day and stamps every row of a pull with the pull date, so a backfill or a multi-day pull has rows whose `pull_date` is later than their partition. My round-125 rule (worker row W311-S5, which I worded and the CTO accepted from my batch) refuses a partition when a row's `pull_date` differs from it. A fixture shaped like the real feed reproduces it on the merged wrapper: **48 rows refused.** The error is mine: I specified the rule from a worker row's one-line description without reading the feed's partition semantics. Round 130 (`DB-i-17`, direct act, issuance merged @d9e8307c5d, worker ~317 in flight) corrects the rule: a partition `date=<d>` is refused when a row's `day` is not `<d>`; a differing `pull_date` is accepted. **The first real run is not to be attempted before it merges.**

## What the issuer read for itself

Re-ran the three criteria in the worker's tree and on the merged tree (PASS), re-validated the proof, read the script's `run_real` and `main` against the order, scanned the changed files for identifier-length digit runs (none), and read the feed script to check the real partition and `pull_date` semantics (which is how the defect above surfaced). The first merge attempt lost the race to other seats' commits and landed nothing; a retry landed. **Not a grade.**

## Rows

Worker rows `W316-S1` to `S6` are all INERT observations: the schema path absent from the sparse worktree; a listed silver with zero rows returns `NO_ROWS` (the order names no status for it); a window with no trading day returns `NO_COMPLETE_ACCOUNT`; a RETURNED row with a null factor counts as 1.0 in the silver chain; `trading_days_between` returns date objects (main converts); an empty dimension makes `main` raise (not exercised). None is armed.

## Open

Round 130 in flight. The first real run waits on `~P2`'s apply of the feed (IB-pr-596), then the backfill; the page reader after.

**Andrew:** nothing from this workstream.

-- 2.0.0_SA_COO~I2
