# IRPT_DASHBD round 125, workstream B-IN (Inflection) -- drain-end (issuer 2.0.0_SA_COO~I2, 2026-10-15 ~21:3xZ)

**One order (a LOCAL build), drained and graded on the LANDED tree; no vendor call, nothing written to AWS, nothing deployed, no client data.** Issued @4b660d8288 (merged @3dde628d6e), drained: `DB-i-12` (~312, merged @7a8a2f681f). On the merged tree `DBI125-1-AC1`, `AC2` and `AC3` PASS, and 93 tests pass across the adapter, wrapper and contract-041 test files (the worker reported 35 + 27). The worker's proof instance reads VALID. `round-close-check --project IRPT_DASHBD --round 125 --workstream B-IN` reads **MAY-CLOSE** (1 order, 0 judgment criteria). Push state: LOCAL on box/dell2, not read against origin. Cut on the CTO's round-124 analysis (msg 8654). **This is what round 124 was owed: the module green on trunk against contract 0.4.1.**

## What exists

The adapter (235 lines) and the run wrapper (173 lines) on contract 0.4.1, with their tests.

- Orion PRESENT rows carry `return_basis` `VENDOR_REPORTED` and `row_status` PRESENT, as 0.4.1's `source_requires` demands. ABSENT rows are written INTO the table in the 0.4.1 shape with the contract's precedence (UNMAPPED_ACCOUNT with a null `account_id` and a set `source_account_id`; the `absent/` file and `BESIDE_TABLE` retired). The three "proposed" marks are gone.
- The wrapper reads its field list and `contract_version` from the contract file. It refuses, with a count and nothing written, a duplicate or non-canonical dimension key, a partition whose rows name another pull date, a non-empty output directory and a repeated key. It passes the adapter the full domain and account set, so a dropped first or last calendar day leaves each account ABSENT (`NO_FEED_ROW` or `UNMAPPED_ACCOUNT`) and `trading_days_unaccounted` reads 0 on both edge-day fixtures; the run record lists the dropped days.
- The end-of-day claim: `claim_placement` reads `RUN_RECORD` (the contract does not declare `market_value_eod_claim`) and the record carries the inferred and measured counts. The wrapper switches the claim into the table by reading the contract when 0.4.2 declares it.

## What the issuer read for itself

Re-ran the three criteria in the worker's tree (PASS), merged through `safe-merge.sh`, re-ran them on the merged tree (PASS) and the three test files (93 passed), read the wrapper's `run()` line by line against the eight rules, and scanned the changed files for identifier-length digit runs (none). **Not a grade.**

## One conflict to rule (the CTO's msg 8674 against contract 0.4.1)

The B-49F round-138-to-141 analysis rules that `VENDOR_REPORTED` leaves `return_basis`: Orion rows carry `TWR` and `source` orion, in contract 0.4.2, and says "in round 125 write TWR". **Round 125 had already landed green when that message arrived, and contract 0.4.1 is still the file at HEAD: its `source_requires` demands `VENDOR_REPORTED` on an Orion present row, so writing `TWR` now would turn trunk red (the 0.4.1 validator and my checker would refuse it).** The module is correct for the contract that exists. Proposal: round 126 flips PRESENT rows to `TWR` (and takes the claim into the table) when 0.4.2 lands; until then nothing runs the module, so nothing served is wrong. `~D2`'s row `W221-S3` (the TWR / VENDOR_REPORTED mismatch) therefore stays ARMED, not disarmed, because its premise reverses with 0.4.2.

## Rows

Seat row `D2-S97` disarms `W311-S1` (edge trading days no longer vanish; measured by the r125 checker and its two edge-day fixtures). Worker rows `W312-S1` to `S4` are INERT: the dropped-row count is computed but has no run-record key; an `out_dir` that is a regular file is refused with count 1; a None or NaN dimension key counts as not canonical; the `accounts` parameter's ids are counted from feed rows only.

## Issuer notes

1. The round-124 checker (`checks/r124/`) no longer passes on the 0.4.1 shapes; round 124's order graded the module against 0.4.0 and is superseded by `checks/r125/`. Disclosed in the worker's instance.
2. The first real-row run and the series-ended cause read (open call dell2-20261015T211904Z-4255) are still uncut.

**Andrew:** nothing from this workstream.

-- 2.0.0_SA_COO~I2
