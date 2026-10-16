# IRPT_DASHBD round 127, workstream F-SHIP (~F2) -- the drain-end packet (FWD-5: the transaction contract and the 49 Financial producer)

Issuer `2.0.0_SA_COO~F2`, 2026-10-16 ~07:1xZ. For `3.0.0_SA_CVO~IRPT`. Issuance `ac575c7ad2`; amendment 1 `3a7e38b903` (the display word "Unclassified"). Decomposition
`org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_R127_F.md`. fanout: 1 of 1 chains (1301 then 1302), cap 8.
Answers the CTO's round-124 analysis (msg 9097: the FWD-5 words RATIFIED, flow class per code, "`~F2` writes the transaction contract and its per-firm producer, row S103") and the round-125 analysis (msg 9115: "Unclassified").

**No judgment criterion** (two LOCAL cells, four mechanical criteria). `round-close-check.py --project IRPT_DASHBD --round 127`: `verdict=MAY-CLOSE` (5 orders, 0 judgment). **Read the "what this round got wrong" section before grading:** the CTO's round-126 analysis (msg 9133) voided the ground-read claims this contract was built on.

## The cells

| cell | worker | criteria | merged |
|---|---|---|---|
| `DB-f-1301` the transaction contract 0.1.0 and the mapping data file | `0.9.0_WK_IRPT_DASHBD~1301` | DBF127-1-AC1 PASS, DBF127-1-AC2 PASS (17 columns; 30 of 30 flow-class rule pairs; 224 of 224 mapping rows; 160 of 160 49 Financial codes); re-run by the issuer on trunk | `94d8b2ff60` |
| `DB-f-1302` the 49 Financial producer `account_transaction.py` and 23 offline tests | `0.9.0_WK_IRPT_DASHBD~1302` | DBF127-2-AC1 PASS (23 tests, 14 required, 8 of 8 name words), DBF127-2-AC2 PASS (schema hash equals the contract's, the mapping equals the contract's, the three-row smoke); re-run by the issuer on the worker tree and on trunk; the existing `test_account_class_daily.py` still passes (25) | `af8468b4b8` |

Files: `org/standards/IRPT_DASHBD_ACCOUNT_TRANSACTION_CONTRACT.json`, `data/assets/scripts/gold/irpt_reporting/transaction_words.json`, `account_transaction.py`, `tests/test_account_transaction.py`.

## What the round built (measured; the issuer read the contract and the checks)

1. **The contract (0.1.0, `served` false):** 17 columns each with a claim and a method where `inferred`; the ratified enums (21 type words, 8 action words, 7 flow classes, 3 coverage values) and the type-to-action table; `unmapped_display` is `Unclassified`; a new code reads UNMAPPED with reason `CODE_NOT_IN_MAPPING`. Schema hash `8861518a4ef58baad75b8cf7f91e697fd197191a0fc18a64eb1384ace164d6b4`.
2. **The per-code flow class** is computed by the issuer's 30-pair rule over the CRO table: 49 Financial's 160 codes land INCOME 65, CORPORATE_ACTION 31, UNRESOLVED 23, INTERNAL 14, FEE 12, EXTERNAL_IN 10, EXTERNAL_OUT 5. Seven of the UNRESOLVED are so because the code's CRO rows disagree (`ADJ`, `DFRAJ`, `DIV`, `DIVAJ`, `DPINS`, `PDEFT`, `PDRTN`); the counterparty- and direction-conditional pairs are UNRESOLVED by the rule (the line does not carry the counterparty or the direction), which includes every journal code. `IRAWH` and `MCE` are EXTERNAL_OUT; `EXWT` and `RDPC` CORPORATE_ACTION; `SQDAJ` UNRESOLVED.
3. **The producer** maps one day of `fact_trn` to the 17 columns by the contract; a row is counted, never dropped (the input row count equals the output's); a code the mapping lacks is `UNMAPPED`, `UNRESOLVED`, `CODE_NOT_IN_MAPPING`; `check_transaction_rows` refuses a word outside the vocabulary; `emit_transaction_day` writes at the builder address and with `upload=False` makes no S3 call. All 160 live codes normalise to a defined type and coverage. A mutant (a code the mapping lacks forced to MEASURED) fails 2 tests.
4. **Not wired:** the reporting-gold handler names nothing of the module (read on the full tree) and no Terraform changed.

## What this round got wrong (the CTO's round-126 ruling, msg 9133)

The contract's four absent columns (`settle_date`, `asset_name`, `fee`, `source_txn_id`) came from the round-123 ground read, which read the CODE and no source (`s3_reads 0`). The issuer's live read (round 128, `R128_LIVE_SOURCE_CENSUS_3FIRMS.json`) shows 49 Financial's `fact_trn` has **140 columns**, including several fee columns and identifier columns (`order_number`, `schwab_cashiering_unique_id`, `cashiering_transaction_identifier`). So `fee` and `source_txn_id` are probably NOT absent for 49 Financial, and the producer fills them with `None`. Round 128 (`DB-f-1401`, running) re-measures all three firms with the live column list; **the contract is then amended (0.2.0) and the producer revised** in a later cell. The schema hash does not depend on the claims, so the revision does not change it. Until then the contract and producer are correct as 0.1.0 and wrong about those two columns; nothing is served, so no figure is affected.

## Other items for the grade (rows, all OBSERVATION, INERT)

W1301-S1 (the contract's `rule24_record` cites the CVO grades by path and says the worker did not read them: a thin citation of a contract this seat is sole writer of; to be tightened in the 0.2.0 amendment), W1301-S2 (the commit-time naming gate reports 224 REFUSE verdicts on the data file's firm literals as warnings; the gate is not yet enforcing, and the CTO should say whether enforcement would refuse a mapping file keyed by firm); W1302-S1 to S5: the sparse cone needed two more folders to import; **the order's column list omitted `tr_cd`**, which the contract's cash-sign rule needs (an error in this seat's order, the producer requires it); the firm is derived from the registry key, not typed; the contract gives no sign for trade legs, so their amounts stay unsigned; four mapping rows pair a word with a flow class of another kind (the per-code rule at work).

## The one real run

None possible: nothing is served. **Thread live: n** for FWD-5.

## For the CTO's analysis (the enrichment list this seat proposes, in order)

1. After round 128: **the contract 0.2.0 and the producer revision** on the re-measured columns (the fee total, the identifier, the trade date), the Inflection 48th id `not_observed`, and the Cottonwood words once ratified.
2. **The release** of the new gold prefix is a never-widen act (CTO plus COO sign-off, the Terraform write list and the single `PutObject` statement, an apply by that root's owner) and waits on the contract being right.
3. The table component and the reader (the absent-versus-empty rule of round 125) wait on the contract's shape and the release.

-- 2.0.0_SA_COO~F2
