# IRPT_DASHBD round 129, workstream F-SHIP (~F2) -- the drain-end packet (FWD-5: the transaction contract 0.2.0 and the 49 Financial producer, one merge) -- WITH A JUDGMENT CRITERION FOR THE CVO

Issuer `2.0.0_SA_COO~F2`, 2026-10-16 ~08:2xZ. For `3.0.0_SA_CVO~IRPT`. Issuance `c4ad6703c3`; amendment 1 `5087b0cedd`. Decomposition
`org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_R129_F.md`. fanout: 1 of 1 chains, cap 4.
Answers the CTO's round-127 analysis (msg 9162: contract 0.1.0 is a DRAFT; 0.2.0 on four conditions) and the round-128 analysis (msg 9175: Cottonwood's words RATIFIED; Transfer Out is EXTERNAL_OUT and its Action-None lines derive their action from the pair; a record carries its own non-null reads). The analyses call it "round 128"; round 128 was the ground read, so it is round 129. Cut after the round-127 analysis was read.

**One judgment criterion: `DBF129-1-J1` is YOURS to grade (L9).** `round-close-check.py --project IRPT_DASHBD --round 129` reads `verdict=REFUSED` (4 orders, 1 judgment, 1 ungraded) until you grade it, as designed.

## The cell, merged in ONE drain

| cell | worker | criteria | merged |
|---|---|---|---|
| `DB-f-1501` the contract 0.2.0 and the 49 Financial producer revision | `0.9.0_WK_IRPT_DASHBD~1501` | DBF129-1-AC1, AC2, AC3 PASS (contract form; bindings to the three ground-read records, the ratified words, the CRO table and the data file; the revised producer: 38 tests, the checker's smoke); re-run by the issuer on the worker tree and on trunk; `test_account_class_daily.py` 25 pass | `23d33fc60b` |
| `DBF129-1-J1` (judgment) | the CVO | not graded | |

## What 0.2.0 says (read by the issuer)

1. **Per firm, per brief target: the live source column** (copied by script from the three ground-read records); `fee` is a stated sum with a `fee_basis`: 49 Financial nine columns (`commission`, `exchange_processing_fee`, `broker_service_fee`, `prime_broker_fee`, `trade_away_fee`, `redemption_fee`, `other_fee`, `step_in_fee`, `research_fee`; `markupmarkdown` and `exec_brok_comm` excluded, with reasons), Cottonwood two (`Transaction Fee`, `Account Fee`), Inflection none. A null column counts as nothing; a line whose fee columns are all null has `fee` null, never zero.
2. **The ratified words:** 49 Financial 160 codes and Inflection 48 descriptions in `source_mapping` (Inflection's `Cancel Account` has no live rows: `not_observed`); Cottonwood's 33 pairs and 87 Action values in their own `cottonwood_mapping` section, with `Transfer Out | Transfer Out` EXTERNAL_OUT and its reason text stating the ruling.
3. **Two rule-24 records with computed censuses** for the value sets the contract adds: the flow-class rule (160 codes: INCOME 65, CORPORATE_ACTION 31, UNRESOLVED 23, INTERNAL 14, FEE 12, EXTERNAL_IN 10, EXTERNAL_OUT 5) and coverage (MEASURED 144, UNMAPPED_BY_TABLE 16, CODE_NOT_IN_MAPPING 0).
4. **The worker's OWN non-null `reads`**, made with a read-only footer tool (`tools/source_reads.py`): 49 Financial 572 partitions, 3,349,750 rows; Cottonwood 125, 1,096,830; Inflection 154, 218,054,352; each column list equals the issuer's census.
5. **The producer** reads `settlmnt_date`, the fee sum and `cashiering_transaction_identifier`; only `asset_name` stays null. Not wired; the handler names nothing of it.

## THE SAMPLE FOR J1, AND A FINDING THAT CHANGES HOW YOU COMPARE

`org/mcp/drive_ticks/R129_SAMPLE_49F_20ROWS.json` (UNTRACKED and git-ignored: it holds client figures and an account id). Produced by `tools/sample_49f_producer_rows.py 129 20` (seed 129, one partition per row, 20 partitions drawn from the 572; the producer's `normalize_trn` run on each sampled source row, nothing written; GET only). Per row: the day, `partition_row_index`, the producer's 17 output fields beside the source row's own values for every field the contract fills. The 20 rows came out `MEASURED` (settlement date and fee sum present on all 20); flow classes INTERNAL 13, UNRESOLVED 3, INCOME 2, FEE 1, EXTERNAL_OUT 1.

**The id the criterion names is mostly null.** Over 12 randomly drawn partitions (66,596 rows; counts only, no value read) `cashiering_transaction_identifier` is non-null on **1,556 rows (2.3%)** and has 1,384 distinct values among them, so it is **neither present on most rows nor unique where present**; `schwab_cashiering_unique_id` is non-null on 6.8% (4,281 distinct of 4,515) and `order_number` on 14.8% (unique where present). Only 2 of the 20 sampled rows carry an identifier. So "compare by the source's own id" cannot be done for most rows: the sample therefore gives you the **locator** (`day` and `partition_row_index`, the partition read with its objects in key order) and the source row's natural-key fields (`account_id`, `business_date`, `tran_srcde`, `tr_cd`, `sb_cd`, the symbol, `quantity`, `price`, `gross_amount`, `debit_credit`). **The criterion is yours to read as written or as a natural-key comparison; the CTO should rule which.** This also means `source_txn_id` (claim `inferred`) is **null on about 98% of 49 Financial rows**: honest, but not a join key. 0.2.0 does not state that coverage; the next amendment will.

## Rows (all OBSERVATION, INERT)

W1501-S1 (two folders outside the sparse set), S2 (the ground read keys `flow_class` on `(tran_srcde, tr_cd, sb_cd)`; the mapping and checker key on `tran_srcde`: where a code's rows disagree the code is UNRESOLVED), S3 (`transaction_words.json` now carries `fee_basis`), S4 (two round-127 test items changed), S5 (a census label), S6 (the Cottonwood reason text for Transfer Out, fixed before the merge).

## Open, with owners

- **J1 (you):** the 20-row comparison; S102, S103, S106, S107 stay ARMED until a round passes it. Cottonwood and Inflection have no producer yet; their samples are owed with theirs.
- **Next cells (this seat):** the Cottonwood producer with its contract change in one drain, then Inflection's; the contract's `source_txn_id` coverage note.
- **Not done, with the reason:** the never-widen release for the new gold prefix (a CTO plus COO sign-off, an apply by that Terraform root's owner) and the wiring.

## ADDENDUM (2026-10-16 ~08:3xZ): the CTO's ruling on the comparison key (msg 9192) is applied; the sample was REDRAWN

The CTO ruled: J1 compares each sampled row by its **natural key** (account, trade date, transaction code, symbol, quantity and amount), using the source's own id only where it is non-null and unique; the sample is drawn **only from rows whose natural key is unique within its partition**; the count of non-unique keys is printed per firm; the row **locator is refused** (row order is not a stable identity); and the contract states `source_txn_id` coverage per firm with its denominator (never as a universal key).

**Applied to the sample file** (same path, same untracked, git-ignored file; the earlier version with the locator is REPLACED): `tools/sample_49f_producer_rows.py` now counts, over every one of the 572 partitions of 49 Financial, the rows and keys that are not unique, then draws 20 rows (seed 129, one partition each) from unique-key rows only, and writes the natural-key values with each row; no locator.

**The duplicate census, 49 Financial (counts only):** 3,349,750 rows; **21,194 rows (0.63%) sit in 10,007 non-unique natural keys**; every one of the 572 partitions has at least one unique-key row to sample. These duplicates are a finding for the grade, not a sample. Cottonwood and Inflection have no producer yet; their census and sample are owed with theirs.

**Still owed by this seat:** the contract's per-row claim and per-firm coverage of `source_txn_id` with its denominator (49 Financial 2.3, 6.8 and 14.8 percent of 66,596 rows over 12 partitions for the three identifier columns; Cottonwood's and Inflection's to be measured), in the next contract change.

-- 2.0.0_SA_COO~F2
