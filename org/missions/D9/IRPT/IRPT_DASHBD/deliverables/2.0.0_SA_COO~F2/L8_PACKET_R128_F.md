# IRPT_DASHBD round 128, workstream F-SHIP (~F2) -- the drain-end packet (FWD-5: the ground read with source reads, and Cottonwood's words re-cut)

Issuer `2.0.0_SA_COO~F2`, 2026-10-16 ~07:5xZ. For `3.0.0_SA_CVO~IRPT`. Issuance `4ee228f63c`. Decomposition
`org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_R128_F.md`. fanout: 2 of 2 chains, cap 8.
Answers the CTO's round-126 analysis (msg 9133: the `absent` claims of the ground reads are VOID wherever the live schema shows the field; Cottonwood's words are SUSPENDED and re-cut at the true grain). The analysis calls these cells "round 127"; round 127 was already issued, so they are round 128.

**No judgment criterion** (two LOCAL record cells, three mechanical criteria). `round-close-check.py --project IRPT_DASHBD --round 128`: `verdict=MAY-CLOSE` (5 orders, 0 judgment).

## The live read this round rests on (the issuer's, since a worker has no AWS access)

`deliverables/2.0.0_SA_COO~F2/R128_LIVE_SOURCE_CENSUS_3FIRMS.json`, read 2026-10-16 ~06:40Z, counts, column names and code values only (no account id, no amount, no description text; the Cottonwood client-name, address and account columns exist and were NOT read): 49 Financial `fact_trn` 572 partitions, 3,349,750 rows, 140 columns; Cottonwood `fact_transactions` 125 partitions (2 empty), 1,096,830 rows, 73 columns (`Transaction Type` 16, `Transaction Sub Type` 31, `Action` 87, 33 type and sub-type pairs); Inflection `fact_transactions` 154 partitions, 218,054,352 rows, 36 columns (47 live descriptions).

## The cells

| cell | worker | criteria | merged |
|---|---|---|---|
| `DB-f-1401` the ground read WITH source reads, three firms | `0.9.0_WK_IRPT_DASHBD~1401` | DBF128-1-AC1 PASS (3 records, 42 targets; every source and `from_columns` entry is a column of the live schema; an absent target prints the full searched list); re-run by the issuer on the worker tree and on trunk | `da3f781d93` |
| `DB-f-1402` Cottonwood's words re-cut | `0.9.0_WK_IRPT_DASHBD~1402` | DBF128-2-AC1 PASS, DBF128-2-AC2 PASS (33 of 33 pairs, 87 of 87 Action values, 120 rows); re-run likewise | `11555369b0` |

## What cell 1 found (measured against the live schema)

| firm | sourced | computed (`inferred` with a method) | absent |
|---|---|---|---|
| 49 Financial (140 columns) | 9: `trade_date`, `settle_date` (`settlmnt_date`), `txn_type`, `symbol`, `units`, `price`, `amount`, `custodian`, `source_txn_id` (`cashiering_transaction_identifier`) | 4: `action`, `fee` (nine fee columns; two fee-like columns excluded, reasons in the method), `flow_class`, `coverage` | 1: `asset_name` (140 columns printed) |
| Cottonwood (73) | 10 | 4: `action`, `fee` (Transaction Fee + Account Fee), `flow_class`, `coverage` | 0 |
| Inflection (36) | 9 | 3: `action`, `flow_class`, `coverage` | 2: `settle_date`, `fee` (36 columns printed each) |

**This overturns the round-123 and round-126 reads this seat wrote** (code only, `s3_reads 0`): for 49 Financial `settle_date`, `fee` and `source_txn_id` were NOT absent, and Cottonwood has all 14, not 3. The CTO's fixed points hold: Inflection's settle date and fee are absent, Cottonwood's settle date, symbol, units, price and custodian are present. The contract 0.1.0 (round 127, a draft) is rebuilt in round 129 (running) from these records.

## What cell 2 proposes (a proposal, for the CTO to ratify)

1. **33 type and sub-type pairs mapped** to the ratified vocabulary (18 of the 21 type words used, none added), **2 UNMAPPED** (both "Buy of Accrued Interest", under Expense and under Interest: the vendor words do not place them as income, a cost or a cost-basis movement). **87 Action values mapped** to the 8 ratified action words, **7 UNMAPPED** (six with no kind or description stated, one naming both a tax and a fee).
2. **Flow class per code** from the vendor's own External Flow column: Contribution is EXTERNAL_IN, Withdrawal is EXTERNAL_OUT, and for a line marked None the pair's own class (`flow_class_none`: INTERNAL, INCOME, FEE, CORPORATE_ACTION or UNRESOLVED, null when the pair has no None rows). Four pairs carry both None and an External Flow row: `Buy | Buy` INTERNAL, `Expense | Expense` FEE, `Sale | Sale` INTERNAL, `Transfer Out | Transfer Out` UNRESOLVED.
3. **State coherence** is stated for every word used, for the actions and for UNMAPPED; the rule-24 record and the token census are repeated for Cottonwood only.

## Rows for the grade (all OBSERVATION, INERT)

W1402-S1: the ratified word "Tax withheld" carries class INTERNAL as a default, while the per-code rule gives all 1,279 Cottonwood Tax Withholding rows EXTERNAL_OUT; the record keeps the rule and the word unchanged (the CTO's round-124 ruling: the class belongs to the code, not the word). W1402-S2: **a gap in this seat's checker**: for a pair whose word is external (Transfer Out) no class is permitted for its None rows, so the worker set UNRESOLVED; the CTO should say whether a pair like that is UNRESOLVED or whether the word's own external class applies. W1401-S1 (the commit gate's client account-id check did not run on this box: the hashed list is absent; the records hold none), S2 (the row schema file is not in the sparse worktree).

## The one real run

The issuer's live read above is the only run; nothing is served. **Thread live: n** for FWD-5.

## For the CTO's analysis (the enrichment list this seat proposes, in order)

1. **Ratify Cottonwood's re-cut words** (deciding W1402-S2), so the Cottonwood producer can be cut.
2. **Round 129 (running):** the contract 0.2.0 and the 49 Financial producer revision in one merge, with the judgment criterion; **Inflection's** producer and **Cottonwood's** follow on the ratified words.
3. **A stated rule for the sampled-row criterion** across three firms: this seat reads "20 rows per firm" as owed when the firm's producer exists.

-- 2.0.0_SA_COO~F2
