# IRPT_DASHBD round 124, workstream B-IN (Inflection) -- drain-end (issuer 2.0.0_SA_COO~I2, 2026-10-15 ~20:4xZ)

**One order (a LOCAL build), drained; no vendor call, nothing written to AWS, nothing deployed, no client data.** Issued @e705822f21 and amended @a48b6b1364 before the merge (merged @057e7995b6), drained: `DB-i-11` (~311, merged @6c7b7ccb56). **On the worker's tree (built on 0.4.0) `DBI124-1-AC1`, `AC2` and `AC3` PASS, the adapter's 25 tests pass and the proof instance reads VALID (rc 0). On the LANDED tree only AC1 passes: AC2 and AC3 FAIL, and 2 of 38 tests fail (the adapter's contract-column test and the wrapper's schema-hash test), because contract 0.4.1 landed (`~D2` msg 8635, @969e41a3e7 and @ef1c8ccaf2) after the cut and these checks read the contract file at HEAD.** The wrapper is correct for the contract it was ordered against (0.4.0, ABSENT beside the rows, as ADDENDUM 6 item 1 ruled for a contract not yet landed); it is stale against 0.4.1. Push state: LOCAL on box/dell2, not read against origin. Cut on the CTO's round-118 ADDENDA 5 and 6 and the round-123 analysis (msg 8610), not on a new analysis.

## What exists

`data/assets/scripts/gold/irpt_reporting/adapters/inflection_scope_feed_run.py` (138 lines) and its test file (13 tests, one a mutant). `run(silver, dim_frame, trading_days, firm, method_version, out_dir)` takes feed silver partitions (frames) and the dimension frame and writes, under one directory: `date=<business_date>/data.parquet` (the contract's 22 fields, whose hash equals `schema_hash_with_optional`, plus the proposed string column `market_value_eod_claim`), `absent/data.parquet` and `run_record.json`.

- A repeated (account, day) key is refused with its count and nothing is written. An incomplete calendar day (an unknown status, a RETURNED row without a factor, an ABSENT row without a reason class) is dropped before the adapter and counted.
- The run record states `contract_version` 0.4.0 and `absent_placement` BESIDE_TABLE (0.4.1 has not landed), the proposed reason classes present, and the manifest's `reason_class_status` marking `NO_FEED_ROW`, `INCOMPLETE_WINDOW` and `NO_EOD_VALUE` as proposed.
- The adapter was edited (round-123 analysis items 2 and 3): rows carry `market_value_eod_claim` (`inferred` or `measured`); ABSENT records carry `row_status` ABSENT; an `UNMAPPED_ACCOUNT` record has `account_id` null and `source_account_id` set.
- The 299-calendar-day Monday-to-Friday fixture (inside the 238-to-365-day gap round 122 named): the chained rows equal the product of the source's factors to 1e-12 and `carried_days` sums to 299. **The fixture's "source" is the product of its own daily factors; a comparison against a real Orion period return belongs to the first real-row run.**

## What changed under the round: contract 0.4.1 (`~D2` msg 8635)

0.4.1 keeps the 19 columns and adds the optional `row_status` (PRESENT / ABSENT) and `reason_class` (eight classes, including the three this module proposed). Against it the merged module is stale in these places: (1) an Orion PRESENT row must carry `return_basis` `VENDOR_REPORTED` (the module writes `TWR`; `~D2`'s row `W221-S3`, ARMED, my disarm); (2) ABSENT records go INTO the table with `row_status` ABSENT and `reason_class`, with `market_value_eod` and the flows nullable, and an unmapped row has a null `account_id` and a required `source_account_id`; (3) the schema hash over the contract's now 24 fields differs, so the wrapper's 22-field hash check and the `BESIDE_TABLE` placement no longer hold; (4) `market_value_eod_claim` is not in 0.4.1, so it stays a proposed column beside the contract. The precedence `~D2` states for a day with two reasons is UNMAPPED_ACCOUNT, the feed's own class, NO_FEED_ROW, INCOMPLETE_WINDOW, NO_EOD_VALUE.

## What the issuer read for itself

Re-ran the three criteria and the adapter's tests in the worker's tree (PASS), re-ran them on the landed tree (AC1 PASS, AC2 and AC3 FAIL on the 0.4.1 move above, nothing else), re-validated the proof instance, read the 138-line wrapper against the five rules. Before the cut the checker was fed a reference wrapper over a patched reference adapter (PASS) and thirteen single-rule mutants (FAIL each). **Not a grade.**

## Rows (mine to rule or carry)

`W311-S1` (ARMED, my disarm). **The complete-day drop can remove a trading day silently:** the adapter takes its domain from the kept rows, so when an incomplete day is the first or last calendar day of the feed, its trading day gets neither a row nor an ABSENT record, and an interior drop turns the prior day's end value into `NO_EOD_VALUE`. The run record counts the dropped days but does not list the trading days left unaccounted. **Nothing is served from this output and no real run has happened, so the hazard is not live.** It stays ARMED, with its disarm named: the wrapper's record reports the dropped days and the trading days with neither a row nor an ABSENT record, and that count reads 0 or is explained on the first real-row run.

`W311-S2` to `S6` (INERT): the repeated-key count is keys, not extra rows; the run record's account counts omit an account whose every row was dropped; duplicate or non-canonical dimension keys collapse silently; the silver partition key is not checked against the rows; a rerun into the same `out_dir` leaves stale partitions.

## Proposed round-125 batch (the CTO's to rule)

One cell, the module's move to contract 0.4.1: Orion PRESENT rows `VENDOR_REPORTED` with `row_status` PRESENT (disarms `W221-S3`); ABSENT records written into the table in the 0.4.1 shape with the precedence above (the `absent/` file and `BESIDE_TABLE` retire); the wrapper's schema-hash check re-pointed at the 24 fields; the run record's `contract_version` read from the contract file, not typed. With it, the wrapper repair, ahead of the first real-row run: list the dropped days and the unaccounted trading days in the run record (S1); refuse a duplicate or non-canonical dimension key and a partition key that disagrees with its rows (S4, S5); refuse a non-empty `out_dir` (S6); count accounts before the drop (S3); state the repeated-key count rule (S2). The real-row run itself stays a later cell on the feed's silver.

## Issuer errors this round (mine, disclosed)

1. I wrote the order's criteria as bullets, not `<criterion>` tags; the issuance gate refused it and I recut it.
2. The CTO's round-123 analysis arrived after I had written the checker. I folded its three items into the same unmerged issuance (a48b6b1364) and re-fed the checker (the nine first mutants plus four new) before the merge.

**Andrew:** nothing from this workstream.

-- 2.0.0_SA_COO~I2
