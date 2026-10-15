# IRPT_DASHBD round 123, workstream B-IN (Inflection) -- drain-end (issuer 2.0.0_SA_COO~I2, 2026-10-15 ~19:5xZ)

**One order (a LOCAL build), drained; no vendor call, nothing written to AWS, nothing deployed, no client data.** Issued @ba5fa73f5f (merged @13b4cd4c68), drained: `DB-i-10` (~310, merged @90862adf60). On the landed tree `DBI123-1-AC1`, `AC2` and `AC3` all PASS, and the proof instance reads VALID (rc 0). `round-close-check --project IRPT_DASHBD --round 123 --workstream B-IN` reads **MAY-CLOSE** (1 order, 0 judgment criteria). Push state: LOCAL on box/dell2, not read against origin. Cut on the CTO's round-118 ADDENDUM 4 and `~D2` msg 8574, not on a new analysis.

## What exists

`data/assets/scripts/gold/irpt_reporting/adapters/inflection_scope_feed_adapter.py` (183 lines, standard library only, no I/O) and its test file (22 tests, one a mutant). `adapt(feed_rows, account_map, trading_days, firm, method_version)` returns contract-0.4.0 rows, a list of ABSENT records and a manifest.

- Each non-trading calendar day's factor is multiplied into the next trading day's factor; the row carries `carried_days`. A trading day whose own row is ABSENT stays ABSENT, even beside returned weekend days.
- Rows carry `source` orion, `flow_claim` absent, null flows, and `source_account_id` Orion's integer id. An unmapped account writes no row and no source id; its days are ABSENT `UNMAPPED_ACCOUNT` and counted.
- A gross-of-fees feed row and an unsorted calendar are refused (`ValueError`).

## What the issuer read for itself

Re-ran all three criteria on the landed tree (PASS) and re-validated the proof instance. Read the 183-line module line by line against the eight rules. Before the cut the checker was fed a reference implementation (PASS) and six single-rule mutants (no compounding, leading days not skipped, unmapped dropped, claim removed, gap filled, a guessed source id): each FAILED. Scanned the changed files for identifier-length digit runs: none. **Not a grade.**

## Decisions inside this round (the issuer's; open to the CTO)

1. **ABSENT days are returned beside the rows, not written to the table:** the contract has no reason column and `market_value_eod` and `account_id` are non-nullable. If ABSENT rows are wanted in the table, `~D2`'s contract needs a reason column and a nullable value.
2. **`market_value_eod` is inferred** (the next calendar day's start value; the feed carries an end value only on its last day). The manifest says so. Whether Orion's `startValue` equals the prior day's end is NOT measured.
3. **Three reason classes are added by the module:** `NO_FEED_ROW`, `INCOMPLETE_WINDOW`, `NO_EOD_VALUE`. They are not in the feed's vocabulary and not in the contract's enums.
4. **`day_quality` MEASURED and `guard_state` GUARD_NOT_REACHED** are the nearest members for a vendor return the holdings guard never saw. The CVO grades the words at L9.
5. **`holdings_price_return_reason` is None** beside a null return (worker row `W310-S1`, ruled in seat row `D2-S93`): valid under the contract, no class invented.
6. The dimension's `account_id` is Orion's id as a string (round 108), so "mapped through `account_dim`" is membership in an injected map; the real map is read in the run wrapper.

## Rows

`W310-S1` (ARMED, my disarm: ruled by `D2-S93`), `W310-S2` (a repeated (account, day) feed row is read as the last one, silently), `W310-S3` (an empty feed gives an empty result), `W310-S4` (the manifest counts feed accounts only). S2 to S4 are INERT; **S2 is carried into round 124: the wrapper refuses and counts a repeated key before calling `adapt`.** `D2-S60`/`S61` stay on the feed landing.

## Next

Round 124 (the CTO's ADDENDUM 5, msg 8584): the run wrapper (silver reader, `adapt()`, the parquet), LOCAL, fixtures only, with the complete-day rule and a 238-to-365-day chain fixture. The first real-row run stays a later cell on the feed's silver (about the morning of 2026-10-16).

**Andrew:** nothing from this workstream.

-- 2.0.0_SA_COO~I2
