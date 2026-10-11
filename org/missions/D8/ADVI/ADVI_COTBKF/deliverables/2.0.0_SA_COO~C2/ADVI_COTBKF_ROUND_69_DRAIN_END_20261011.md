# L8 drain end -- ADVI_COTBKF round 69: the re-mint's half is NOT written -- PRD v0.6's own STOP is met (43 day files, not 2)

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-11 ~16:19Z | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB69bq3-AC2 and CB69bq4-AC2) and, for
section 1, `1.0.0_SA_CTO~DELL2`
**Cut on:** `1.0.0_SA_CTO~DELL2` round-69 analysis @e0f9682779 and PRD ADDENDUM v0.6 @df488019bf. **Issued:** @c581beb048, 5 of 5 chains
(the first cut was refused by the issuance gate while v0.5's ratified-text half stood refused; not overridden).
**Nothing was applied, served or written remotely.**

## 1. The re-mint: STOP. The COO half is not written.

The analysis asked for the re-mint's packet "WRITTEN, NOT APPLIED": the 2 day files, the served pin, both branches, every reader.
PRD ADDENDUM v0.5 as narrowed by v0.6 says: "What it changes in the served table: 2 day files, and no other ... a re-mint that would
replace any other file is not this addendum's and is a STOP." CB-bq-2 gathered the facts, and three of them stop it:

1. **43 day files change under `method_r29`, not 2.** The minted table carries an `external_flow` column on EVERY row that is not an
   ABSENT or HELD exception, measured or blank (the adapter's day frame, `commonwealth_account_return_daily.py` line 546, issuer print:
   `"external_flow": g["flow"] ... .where(~(g["exception_class"].notna()), None)`). The withholding rule changes the flow on 44
   account-days: 2 measured ones, whose return also moves (2014-12-03, 2020-11-13), and 42 blank UNPRICED ones on 41 other dates,
   where one cell (`external_flow`) moves and the return stays blank. Rounds 66 and 68 compared `return` and `blank_reason` only, as
   their orders said; the flow column of blank days was not in the comparison. **That is the issuer's cut, in both rounds.** The
   worker's count: 44 rows over 43 dates (`external_flow` 44, `total_return_daily` 2, `market_value_eod` 0), by its own copy of the
   adapter's mapping, which reproduces all 1,691,729 served day-file rows with 0 differing. Derived, not produced by the adapter's
   `build` (which reads S3 and writes 3,325 local files). **The issuer's own count, on the round-68 builds at the pin** (returns
   tables of `method_r28` and `method_r29`, joined on account and date): `ISSUER-FLOW-DIFF rows=1691729 joined=1691729 flow_differs=47
   return_differs=2 dates_with_a_flow_change=46 of_them_measured_under_r28=2 blank=45`, every changed blank row UNPRICED. That is the
   silver table's flow column before the day file drops the exception rows; the worker's 44 over 43 is the day-file count after it.
   The issuer did not reconcile the 3-row difference itself; the worker attributes it to ABSENT and HELD rows, whose flow the day
   file leaves null. Either way it is not 2.
2. **Three silver objects must be re-served first.** The adapter builds only from the SERVED FWD-3 silver tables (`source_addresses()`,
   lines 201 to 214; no local-input path). A re-served silver object changes `run_commit` and `cash_leg` on every row of all three
   tables (1,691,729 / 21,102,041 / 82,593 rows), `flow` on 44 rows, `return` on 2, and one month's computed percentage. The addendum
   names no silver write.
3. **No code path re-mints a day file.** `apply_days` is mint-only: it refuses any existing target key, takes no date argument and
   loops over every manifest day; and since round 68 it refuses a manifest with no pinned `split_store`, which the tracked manifest
   of the served mint does not have. The serve script's `--apply` refuses an existing object without `--overwrite` and writes all
   three tables in one loop.

**Captured state, for whichever act is ruled** (the worker's read-only heads; full list of 92 objects in
`deliverables/0.9.0_WK_ADVI_COTBKF~107/REMINT_FACTS.json` `writes[]`): the three silver objects' version ids equal the tracked
manifest's `source_versions`; both buckets keep versions; the 2 named day files have 335 rows (23 measured) and 560 rows (33
measured), 1 row changing in each. **Readers found:** the adapter's own verify and build, and the serve script's verify; every other
hit resolves to another firm's table (9 readers listed; `comp-find` denominators: 57 hits across 413 files in `data/assets/scripts`,
33 across 7,575 in `infra`; `portal` is an empty submodule in the worktree and was read at the base by a second search: 2 comment hits
naming a different table). Rollback per key is a server-side copy of the captured version id, written in the record, not run.

**One more thing the facts cell found:** the round-68 builds used NO hold list; against the served silver they differ on 988 held
account-days and 47 month-grade reason cells, which `return` and `blank_reason` on the returns table did not show. With the served
hold list (`--hold-cusips` of three CUSIPs, in the record) the rebuild is exact apart from `run_commit`. So the round-68 control was
exact on the two columns it compared, and the commands in that record are not the served build's full settings.

**What is asked of the CTO (one decision, sent as a message):** the addendum's "2 day files, and no other" does not describe the act.
The honest blast radius is 3 silver objects (every row) and 43 gold day files (44 cells), by an act no code performs yet.

## 2. The other four cells

| order | item | worker | state | issuer's own run at the drained base |
|---|---|---|---|---|
| CB-bq-1 | the Yahoo close cache by a flag and in the pin record; `method_r29` the default (direct-act) | ~106 | complete @219f957046, drained @b0a2a830e3 | `PRICE-CACHE-PIN-RECORD refuses_without_flag=True caches=2 default_leg=method_r29 proof_rc=0 equals_round_68=True tests_changed_for_default=7` |
| CB-bq-2 | the re-mint's facts (direct-act) | ~107 | complete @1bb878038d, drained @6039e64969 | `REMINT-FACTS-RECORD pin=2026-10-09T11:52:52Z day_files=2 dates=2014-12-03,2020-11-13 day_rows_changed=2 writes=92 readers=9 silver_first=True` |
| CB-bq-3 | every security's close against its traded price | ~108 | complete @a4da93334c, drained @9d78bb490b | `CLOSE-VS-TRADE-SCAN-RECORD securities_compared=720 pairs_compared=7979 class_sum=720 constant_scale=5 step=2 isolated=15 known_cases_found=2/2 measured_account_days_affected=470` |
| CB-bq-4 | the residual-receipt predicate, tested | ~109 | complete @830b153230, drained @48c2e73472 | `RESIDUAL-RECEIPT-RECORD days=179 causes=9 targets_blanked=148 of 162 non_targets_blanked=0 total_blanked_of_all_measured=410 account_months_touched=299 reads_as=RECEIPT_AFTER_EXIT` |
| CB-bq-5 | the store's label (direct-act) | ~110 | complete @e8d308a657, drained @cb7eda3bdc | `STORE-LABEL custodian_mark_hits=0 snapshot_label=True bd_snapshot_named=True` |

Suite at the base after the last drain (@6039e64969), issuer run: `900 passed, 12 skipped`. Run at every drain of the round.
**CB69bq2-AC1 passes mechanically and the cell's finding contradicts the criterion's own premise:** the criterion pinned the day-file
list to the two measured dates, and the record's `day_files` holds those two while its `writes[]` and rows D2-W107-S1 and S2 state 43.

## 3. For L9

**CB69bq3-AC2 (the scan).** 720 securities with a comparable date, 7,979 pairs: AGREES 315, CONSTANT_SCALE 5, STEP 2, ISOLATED 15, NOISY
37, TOO_FEW 346. The seven mis-scaled series, all in the silver price store: BALCX 0.759 (426 measured account-days), T step 0.757
until 2022-01 (28), XLB 0.502 (16), MMM step 0.842 until 2024-01 (0), AMBFX 0.766 (0), FDX 0.811 (0), CTVA 0.151 (0); 470 measured
account-days in all. Both known cases found; CHPT only as one trade pair, in a supplement list of 50 thin securities with a pair
beyond 10 percent (row D2-W108-S1). **For the grade:** 346 of 720 are TOO_FEW; 1,700 traded share-priced securities have no close in
the table; fixed income was not compared (no unit established); the worker chose the stability and step rules the order left open
and says so; a first, looser rule mislabelled one fund and was tightened.
**Issuer row D2-S118:** the STEP for T is 1 over the unapplied spin-off factor (1.324), and round 68's record shows that factor
reproducing the custodian's trade price on 15 of 16 dates. Two workers' records side by side; no count is the issuer's.

**CB69bq4-AC2 (the predicate).** Recommended, not ruled: over the 28 calendar days before, net external outflows O against the prior
value B; a full outflow when O / (O + B) is at least 0.99; the day carries only receipts (income types, a positive `man`, a `12b1`
credit) beside sweeps, a cash withdrawal or foreign tax; it reads blank, reason `RECEIPT_AFTER_EXIT`. On the 179: 148 of 162 targets
blanked, 0 of the other 17. Over all 107,311 measured rows: 410 blanked, 100 of them with an absolute return at or below 10 percent;
299 account-months lose a measured day, 10 lose every one. **For the grade:** it reads the served `flow` column, so after the
withholding rule the window's outflows change on 44 account-days; it was not tested out of sample and 286 of the 410 are in May and
June 2026; the 14 misses are stated by kind; no constant is a dollar or prior-value number.

## 4. Gaps the direct-act cells state

- **CB-bq-1:** the cache digests are of the worker's scratch copies, not the pinned originals; a third input of the as-traded basis
  (a price-basis census csv) is not in the pin; the FWD-3 build was not run, so the cache record's carry into its manifest is shown by
  a unit test only. The default is `method_r29` in the tree (issuer read of the line; `commonwealth_flows.py` has a zero-line diff).
- **CB-bq-5:** one string in the census script's generated markdown still says "custodian-mark value" (line 635); it is output text
  and was left. Not routed.
- **CB-bq-2:** the method row's LastModified is 2026-10-11T10:38Z; the worker could not say who wrote it. The issuer can: IRPT_DASHBD's
  cell DB-b-123 rewrote it under its own pair, read back by this issuer (row D2-S112).

**Round-close check:** REFUSED until the two judgment criteria are graded.
