# IRPT_DASHBD round 114, workstream B-IN (Inflection) -- drain-end (issuer 2.0.0_SA_COO~I2, 2026-10-15 ~02:0xZ)

**Two orders, both drained; nothing served moved, nothing written to AWS, nothing deployed; counts, hashes and words only in the repo; the cache, the variant table and every input stay in the private folder `C:/dev/_irpt_private_evidence_20261009/`.** Issued @35e0b887eb (merged @1cb46e909b), check amended @6ec9d07ede. Drained: `DB-i-1` (~301, @f28c6cba29) and `DB-i-2` (~302, @f60a82b77e). On the landed tree `DBI114-1-AC1` and `DBI114-2-AC1` PASS and both proof instances read VALID. `round-close-check --project IRPT_DASHBD --round 114` reads **MAY-CLOSE** for these two orders (the verdict line counts seven orders in round 114 across the other workstreams; the five others are not complete and sit outside it). 0 judgment criteria: nothing here is for the CVO to grade by eye. Push state: LOCAL on box/dell2, not read against origin.

## What the cells found

- **`DB-i-1` (the QTD tie-out under three value bases):** the control holds, 0 of 320 households differ from round 109's quarter-to-date gaps (same not-comparable set, every gap within 0.01 bp). Compared / not comparable, then households in the bins under 5 bp, 5 to 25, 25 to 100, 100 or more: `all` 287 / 33, 16, 87, 175, 9; `active_only` 287 / 33, 16, 87, 175, 9 (identical, because no account-day in the quarter carries non-zero value on an inactive row); `ex_cash` 285 / 35, 19, 82, 162, 22. Under `ex_cash` 34 households move down a bin, but 2 more become not comparable and the 100 bp or more bin grows from 9 to 22. **No basis closes the gap:** 184 of 287 households (64 percent) sit 25 bp or more from Orion's client return under the round-109 basis, and `ex_cash` does not change that picture in any direction the CTO could call better. The residual cause is not diagnosed by this round.
- **`DB-i-2` (the two missing days):** 2026-07-01 and 2026-09-28 are both trading days. Orion silver `fact_positions`, `fact_performance` and `fact_transactions` have NO partition for either day; `fact_assets` has both. Bronze `positions`, `performance` and `transactions` hold no file for either day, bronze `assets` holds one per day. So the silver hole has no bronze source to convert: the pull did not land those feeds on those two days. Each gap is two calendar days wide (06-30 to 07-02 and 09-27 to 09-29). A no-flow bridge would touch 787 valued accounts on the day before 07-01, of which 56 had an external flow in the gap, and 792 before 09-28, of which 12 did. The silver producer is `infra/aws/lambda/opal-assets/opal-assets-silver-orion/mirror_conversion.py`; its live EventBridge rule `opal-assets-silver-orion-sweep-daily` is ENABLED at `cron(0 16 * * ? *)` (every calendar day). The repo gives no cause for the missing pulls.

## What this seat read for itself

I re-ran each criterion in its worker's tree (both PASS), re-validated both proof instances with the worktree's own checker (both VALID), and merged each branch through `safe-merge.sh` (row gate on the merged index: 0 violations, 5 and 4 paths). `DBI114-1-AC1` recounts every variant's bins from the private table and the control household by household; `DBI114-2-AC1` re-LISTs the Orion silver prefix and every table's partitions fresh. I did not open any client value. **Not a grade.**

## Issuer errors this round (mine, disclosed)

1. The check's write-token scan refused the one LOCAL parquet write the order requires (row `W301-S1`); amended @6ec9d07ede, the scan now bars AWS writes and any `s3://` literal outside the two granted prefixes.
2. The order said "sorted trading days in the cache"; the cache is calendar-daily and lacks the two NYSE trading days (row `W301-S2`); the NYSE trading-day axis stands, the control is unaffected.
3. My own test harness for the check deleted worker ~301's private folder while the worker had finished; the worker re-ran its committed script, and the regenerated table hashes identical to the recorded one.

## Rows held (owners named)

`W301-S1` and `W301-S2` ruled above. `W302-S1` (the reader has no common-prefix listing, so the worker used its client after the grant check) and `W302-S3` (`lib/trading_calendar` answered from its hardcoded NYSE fallback because `pandas_market_calendars` is absent on dell2; the answer for these two dates matches the weekday rule and the holiday list) are INERT observations. **`W302-S2` is ARMED with this seat as disarm owner and I cannot disarm it:** the feed gap sits in the Orion pull and the silver sweep, neither in this workstream's write surface. It goes to the CTO in the drain-end message for an owner.

## What goes to the CTO

The CTO's round-109 ruling reserved the tolerance for himself on this read. The read is now in: under no tested basis do most households fall within 25 bp of Orion, and the longer windows cannot be compared until the two days are resolved. The question this round hands up is not a number but a route: (a) is the residual QTD gap a method difference to explain (gross against net of fees, valuation timing, how Orion's factor treats flows), to be decomposed next round on a sample of households; (b) who owns the Orion pull that skipped 2026-07-01 and 2026-09-28, and may it be re-pulled (a WORLD act under a never-widen pair) or must the windows spanning them print as unavailable; (c) whether a no-flow bridge across a single missing day is an admissible method for the 12 or 56 accounts that had a flow in the gap. A proposed enrichment list is in the slug's reach; the next cells are the CTO's to name.

## What this does to the FWD outcomes

Inputs to `FWD-2` (account-level returns for Inflection). It is not met, and the account pages stay "Account-level returns are not available for this firm yet." The household return from Orion's client factor stays as sourced in contract 0.5.0.

## Open

**Andrew:** nothing from this workstream. **This seat:** the next B-IN cut waits on the CTO's round-114 B-IN analysis.

-- 2.0.0_SA_COO~I2
