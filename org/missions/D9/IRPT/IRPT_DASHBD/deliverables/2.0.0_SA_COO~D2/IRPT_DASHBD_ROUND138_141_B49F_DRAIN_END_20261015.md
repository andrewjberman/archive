# IRPT_DASHBD rounds 138, 139, 140 and 141, workstream B-49F + contract -- drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-15 ~21:1xZ)

**Four rounds, all drained: round 138 (`DB-b-271`, the households claim and counts of the report-build handler), round 139 (`DB-b-272`, the apply of the signed report-build pair revision 2, its dry run and the 65-day backfill, by the AE applier `0.7.0_AE_CloudOps~DB2`), round 140 (`DB-b-273`, contract 0.4.1) and round 141 (`DB-b-274`, the chain cap of the handler). Counts, hashes and words only.** Merged: `DB-b-271` @f25b913caf, `DB-b-272` @40376ff34b, `DB-b-273` @754702eb15 (with my one-sentence rule-text fix @ef1c8ccaf2), `DB-b-274` @24b4b16305. Not pushed. `round-close-check` for rounds 138 to 141: complete, no JUDGMENT criterion, MAY-CLOSE. Every criterion was run by me in the worker's or applier's tree and again on the LANDED tree: PASS (`DB138-1-AC1..AC3`, `DBC139-1-AC1`, `DBC139-2-AC1`, `DBC139-3-AC1` with fresh live reads, `DB140-1-AC1..AC3`, `DB141-1-AC1..AC3`).

## Round 139 -- the report-build function is deployed and the filled report values are written (WORLD)

`irpt-cot-reporting-gold-lambda` (python3.12, 1,024 MB, timeout 900 s, no reserved concurrency, the native layer version 1 with pyarrow 14.0.2), its two roles, log group and a schedule created DISABLED: one `safe-apply`, plan exactly 7 add / 0 change / 0 destroy, a post-apply plan with no changes, `CodeSha256` equal to the packet's build hash. **The dry run** (`{day 2026-10-14, dry_run true}`): 200, 407 MB in 21.6 s, 287,600 rows for 223 households, the three source-absent days (2026-08-19, 2026-09-24, 2026-09-25) stated with the sentence "3 trading days not reported by the source", the held claim and the counts, **nothing written**: the layer's pyarrow loaded and read the Black Diamond partitions on python3.12. **The backfill**, after the applier held on a defect (below): 65 explicit `{day}` events in 8 batches, all 200, none chained, at most 509 MB, longest 23.7 s, **65 objects**, none skipped; I read the prefix myself: exactly the printed list of trading days from 2026-07-10 to 2026-10-14 less the three absent days, none of those three written, five sampled objects carry `households_as_of` 2026-10-14 and `households_claim` held in their schema. The question-3 counts the CTO asked for: 1,335 accounts dropped by the membership in all (63 of 65 days) and at most 225 households with no rows (early July). The ledger `irpt-dashbd-cottonwood-reporting-gold-20261015` has its five legs closed and stays OPEN. **The schedule is DISABLED and stays so until the CTO's word.** The receipt to `1.0.0_SA_CTO~DELL1` went through the MSTR relay with "NOT a page render".

## Round 141 and the defect the applier found (row `IRPT_DASHBD-D2-S95`, ARMED, disarm owner this seat)

The packet said one event chains at most 10 days. The handler's `chain_next` recomputes the owed days on every hop, so the cap held for the list and not the chain: one `{}` event would have run 68 invocations. The applier simulated it and held before any write; the CTO ruled explicit day events (2026-10-14 first, so nothing is owed afterwards) and a build cell. Round 141 gives every chain a budget (`chain_left`, 0 to 9) carried in the self-invoke payload, refused before any call when bad, for the empty, explicit-day and scheduled entries alike; the probe drives a whole chain. **The deployed function still holds the earlier code**: a code-update pair (a `safe-apply` of a 0/1/0 plan, never `update-function-code`) is owed before the schedule can be enabled.

## Round 138 -- the households claim

Each filled day's one object carries `households_as_of` and `households_claim: held` in its parquet schema metadata (columns unchanged); a built day states four keys (the claim, the date, `accounts_dropped`, `households_no_rows`); ids never reach the output. 42 handler tests, one earlier exact-count assertion moved by the extra GET (worker row `W220-S1`).

## Round 140 -- contract 0.4.1 (for your L9)

`org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json`: row status (`PRESENT`, `ABSENT`), an eight-value `reason_class` (the feed's four, `UNMAPPED_ACCOUNT`, and `NO_FEED_ROW`, `INCOMPLETE_WINDOW`, `NO_EOD_VALUE`) resolved by one precedence, `account_id` nullable only for `UNMAPPED_ACCOUNT` (then `source_account_id` is required), market value and flows nullable on an ABSENT row, `VENDOR_REPORTED` for Orion rows, `source_requires`, the rule-24 record with a word-boundary token census the checker recounts exactly; the 19 columns and `schema_hash` unmoved. **One decision for you:** the rulings call the vendor mark `return_method`; the contract already has `return_basis` ("which arithmetic produced the number"), so `VENDOR_REPORTED` joins that enum and no second column exists (rule 24 postulate iii); the record says so. 31 new tests; 64 earlier contract-reading tests pass.

## Direct acts and rows

The round-131 probes are re-pointed (a 0.3.0 manifest in the fixture) and `DB131-1-AC1..AC3` read PASS on the guarded handler; row `IRPT_DASHBD-D2-S94` disarms `D2-S92`, citing the DB135 test that spans 2026-06-22 and 2026-07-10 and shows every pre-floor window as NOT_SPANNED. **Rows for your disposition:** `W219-S1` (resolved by my Amendment 1 to `DB-b-270`, a worker row cannot graduate), `W221-S1` (resolved by my rule-text fix @ef1c8ccaf2), `W221-S2`, `W221-S3` (ARMED, disarm owner `2.0.0_SA_COO~I2`: the Scope adapter writes TWR on Orion rows against `source_requires`). The 49 Financial disclosure-template read (`DB-b-205`) found no disclosure page in Andrew's named file; one call for Andrew is with the CTO.

## Rows held (owners named)

`S95` (ARMED, this seat, until the code-update pair); `W221-S3` (ARMED, `2.0.0_SA_COO~I2`); `W209-S3` (ARMED, CTO); `D2-S72` (2.0.0_SA_COO~B1, no reply); `W182-S1`, `W401-S1` (0.0.0_AB_MSTR); `D2-S64` (2.0.0_SA_COO~F2). No ARMED row has a dark owner as far as this seat can read.

## What is next, and what goes to the CTO

Round 142 (`DB-b-275`, contract 0.4.2: `market_value_eod_claim`, in flight with worker `~223`). The code-update pair for the chain cap, then the schedule-enable word. Tomorrow's first fire of the landing schedule (about 12:15Z) is read by me.

## What this does to the FWD outcomes

`FWD-1` (Cottonwood thread): the filled report values exist in the cloud for 65 trading days; no served reader opens the prefix yet. Grading is the CTO's at L10.

-- 2.0.0_SA_COO~D2
