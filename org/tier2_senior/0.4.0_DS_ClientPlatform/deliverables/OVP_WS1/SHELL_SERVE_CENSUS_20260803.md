# Shell-serve census (ADHOC Leg 1) + converter-lag resolution (Leg 2)

**archetype:** TRACE
**Author:** 0.4.0_DS_ClientPlatform -- 2026-08-03 ~23:35Z
**TO:** ADHOC.shell-serve-census-and-cot-converter-lag @337aea9aeb (CTO 232535Z b-ii + c)
**Method:** opal-data-cot bucket versioning = Enabled (checked first); serve moments =
platinum/firm/* object-version writes; partition selectability = first-version landing time;
near-empty = current-version rows < 10% of trailing-7-partition median (rows READ per
partition, never size-proxied). Machine output: scratchpad shell_serve_census_out.json.

## Leg 1 -- THE DAY-LIST

DENOMINATOR: 90 silver/allocations partitions (2026-04-22..2026-07-31; corpus birth
post-dates the 2024-11 serve-window floor, so the corpus IS the window). 222 platinum
serve-moment writes survive, 2026-07-19..2026-08-03. 26 near-empty partitions marked:
24 are 0-row (all landed by the 06-29 22:07 backfill batch -- weekend dates PLUS the
weekday 0-rows 06-22, 06-23, 06-26, 06-29, 06-30) + the two measured partials
(07-27 = 3 rows, 07-29 = 1 row).

**SHELL-CONSUMING SERVE MOMENTS (complete within surviving evidence): 4 serve days x
all 12 platinum/firm artifacts = 48 artifact-day pairs.**

| Serve day | Latest-snapshot at serve moment | Artifacts |
|---|---|---|
| 2026-07-28 | 07-27 partition (3 rows vs median 878) | all 12 (client_directory, clients-tab-slim, cumulative_chart, dashboard, header_metrics, leaderboard, mix_summary, partner_analytics_{annual,monthly,quarterly}, timeseries_chart, timeseries_overview) |
| 2026-07-29 | 07-27 partition (3 rows) | all 12 |
| 2026-07-30 | 07-29 partition (1 row) | all 12 |
| 2026-07-31 | 07-29 partition (1 row) | all 12 |

The exposure window CLOSED at the 08-01 publish (latest = the full 07-31 partition).
"Consumed" means: the near-empty partition was the LATEST-SNAPSHOT per the gold chain's
selection logic (A_00.accounts_dimension.py:13,:327 latest-snapshot enrichment;
A_01:29 latest-only) at that artifact-write moment -- CTO's exact census condition.
Which of the 12 artifacts carries an allocations-DERIVED value at what depth is the
impact assessment, explicitly NOT begun without the word.

**UNKNOWNs (reasons, never estimates):**
- Serve moments BEFORE 2026-07-19: no surviving platinum version history -- the June
  episode's serve moments (incl. the value-carrying 06-15..06-18 window and the weekday
  0-row cluster 06-22..06-30) are NOT reconstructable from S3 evidence. UNKNOWN.
- Partition 2026-07-09 carries 2 versions; prior-version row count not read (overwritten
  content; the documented cash_coverage $0.00 instance already records its consumption).
- Per-artifact allocation-derivation depth: out of census scope (impact assessment).

## Leg 2 -- CONVERTER LAG: NO DEFECT (diagnosis corrected, no fix deployed)

My 232021Z "silver converter lag" diagnosis was WRONG, and the census evidence corrects
it: the converter's own set-identity instrument reads frontier_date 2026-08-03, PASS
732/732 (backfill-status.json checked_at 05:00:10Z today); cottonwood fact_transactions
runs to date=2026-08-03. The 07-31 frontier on the SNAPSHOT tables (holdings/allocations)
is CORRECT: snapshot labels are business as-of dates (07-31 = Friday = the last business
as-of; the weekend snapshot pulls correctly produced nothing land-worthy -- allocations
bronze's newest label is 07-31), while period tables label by run date (08-03). I compared
a period-table label frontier against snapshot-table as-of frontiers -- the exact
apples-to-oranges my own registry label semantics distinguish. NO FIX DEPLOYED -- a "fix"
to a working converter would have been the false-outage class NEVER#1 exists to prevent.
Tonight's scheduled cycle (post the LAG=1 deploy @bf4c0aabbe) advances the snapshot
frontier to 08-03 in the ordinary course; that scheduled advance is the closure evidence.

## THE RESIDUAL (CTO 234054Z item 3 -- recorded, not built; routed to OVP WS-5)

The ingest guard's stated predicate is `has_data == 0` (cot_bronze_ingest.py REJECT
branch) -- a ZERO-ROW test. The actual failure shape is a 1-3-row PARTIAL, which passes
it. **LAG=1 (@bf4c0aabbe) removes the KNOWN PRODUCER of partials (BD's not-yet-completed
as-ofs); it does NOT make the guard able to see a partial** -- any other partial-producing
path (truncated transfer, partial vendor day, retry landing mid-write) walks through. An
existence test wearing a completeness test's name (the night's recurring class). The
completeness predicate design (row count vs the partition's own recent distribution, or
vs the roster's expected grain) is routed to OPAL_VENDORPROVENANCE WS-5 where
completeness rules live -- the blindness is not cot-specific. No alarm, no tonight-build
(moratorium).

## Compiler Tools (TO mandate)

| Run | Observed | Verdict |
|---|---|---|
| Phase 1: partition enumeration + selection-logic cites | 90 partitions versioned-enumerated, rows read; A_00:13,:327 + A_01:29 cited | PASS (denominator printed) |
| Phase 2: converter trace | mechanism DISCONFIRMED at instrument + evidence level (set-identity PASS; per-family label semantics) -- the "second mechanism" if_mismatch clause honored by NOT widening into a fix | PASS as no-defect |
| Phase 3: routing | this doc -> CTO cc COO on landing; Leg 2 closes on tonight's scheduled advance | executed |
