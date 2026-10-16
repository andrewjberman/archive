# IRPT_DASHBD round 131, workstream B-IN (Inflection) -- drain-end (issuer 2.0.0_SA_COO~I2, 2026-10-16 ~02:0xZ)

**One order (a LOCAL build: one new test file), drained and graded on the LANDED tree; no vendor call, no S3 write, nothing deployed, no client data.** Issued @8f19caad87 (merged @231823bb48), amended once on its branch @4e13c27d91 (the CTO's round-130 analysis, msg 8823), drained: `DB-i-18` (~318, merged @0f19a69518). On the merged tree `DBI131-1-AC1`, `AC2` and `AC3` PASS, the round-130 criteria still PASS, and 73 tests pass across the adapter, wrapper and new feed-shape test files (35 + 29 + 9). The proof instance reads VALID. `round-close-check --project IRPT_DASHBD --round 131 --workstream B-IN` reads **MAY-CLOSE** (1 order, 0 judgment criteria). Push state: LOCAL on box/dell2, not read against origin. The merge lost the lock to another seat's back-to-back drains for about 40 minutes; a one-second retry loop landed it.

## What exists

`data/assets/scripts/gold/irpt_reporting/tests/test_inflection_scope_feed_real_shape.py` (9 tests, one a mutant). Every feed frame in it is produced by the FEED'S OWN `run()` over the feed's own offline fakes (its schema and day partitioning), never hand-shaped: a backfill window, a single-day pull, a day the feed skipped (built from three feed runs, row `W318-S1`), the wrapper and the round-129 run script on those partitions, the pull-date regression (a later `pull_date` is accepted; a row whose `day` is not its partition is refused with a count and nothing written), and a mutant that puts the round-125 rule back (it refuses the feed's own partitions). This is the CTO's fixture rule (msg 8779) as a criterion.

## The two additions from the round-130 analysis (msg 8823)

1. **The chain is graded on a multi-day series.** The feed-writer fixture now runs the feed's own `run()` over 10 calendar days (8 trading days) with one account carrying a series point on every calendar day: the wrapper writes a PRESENT row on all 8 trading days, `carried_days` sums to 10, and the chained rows equal the product of the silver's own factors to 1e-12. Graded by my checker (AC1) and by a test in the file. (As before, this is a consistency check against the silver's factors, not against Orion's reported period return.)
2. **The dimension input is recorded and the PRESENT count explained.** The file defines `DIM_IDS` (the five fixture accounts, as strings). On the 3-day ended-series fixture the silver holds 2 RETURNED rows but the wrapper writes 1 PRESENT: the other RETURNED row (7001 on its only series day) has a next-day row that is ABSENT `SERIES_ENDED_AT_SOURCE` and carries no end value, so it reads ABSENT `NO_EOD_VALUE`; the PRESENT one (7004 on the pull day) carries the window's end value. The CVO's 2 matches the RETURNED count. A dimension without account 7004 reads 0 PRESENT (its rows become `UNMAPPED_ACCOUNT`).

## What the issuer read for itself

Re-ran the three round-131 criteria and the three round-130 criteria on the merged tree (PASS), the three test files (73 passed), the proof and `round-close-check`, and scanned the changed files for identifier-length digit runs (none). No defect was found in the wrapper or the run script. **Not a grade.**

## Rows

`W318-S1` (one feed run cannot skip a middle day for a failed household, because the household's failure skips every day its accounts are held on), `S2` (no `org/surprise_channel/` folder in the sparse worktree), `S3` (the wrapper's module docstring still names a pull-date refusal the code no longer makes; with `W317-S1`, one docstring line for the next wrapper order) and `S4` (the amendment applied): all INERT, none armed.

## Open

The first real run waits on `~P2`'s apply of the feed (IB-pr-596), then the backfill; the page reader after. Contract 0.4.2's own L9 is the CVO's.

**Andrew:** nothing from this workstream.

-- 2.0.0_SA_COO~I2
