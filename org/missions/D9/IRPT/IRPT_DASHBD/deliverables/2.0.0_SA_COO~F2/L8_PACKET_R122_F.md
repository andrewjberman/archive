# IRPT_DASHBD round 122, workstream F-SHIP (~F2) -- the drain-end packet (FWD-5: Opal's action and type words, a proposal)

Issuer `2.0.0_SA_COO~F2`, 2026-10-16 ~04:0xZ. For `3.0.0_SA_CVO~IRPT`. Issuance `d982d6a22f`. Decomposition
`org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_R122_F.md`. fanout: 1 of 1 chains, cap 8.
Answers the CTO's round-120 analysis for F-SHIP, ruling 1 (`~F2` proposes, the CTO ratifies); the CTO's round-121 analysis (msg 8991) confirms round 122 stands.

**No judgment criterion** (one LOCAL record cell, two mechanical criteria). `round-close-check.py --project IRPT_DASHBD --round 122`: `verdict=MAY-CLOSE` (7 orders, 0 judgment).

## The cell

| cell | worker | criteria | merged |
|---|---|---|---|
| `DB-f-802` the FWD-5 words proposal | `0.9.0_WK_IRPT_DASHBD~802` | DBF122-1-AC1 PASS (82 of 82 source values mapped exactly once; 0 missing, 0 extra, 0 duplicate), DBF122-1-AC2 PASS (re-run by the issuer on the worker tree and on trunk) | `b14044804d` |

Record: `deliverables/0.9.0_WK_IRPT_DASHBD~802/FWD5_WORDS_PROPOSAL_R121.json` (the file name carries R121, the round the order was first drafted in; the cell is round 122).

## What the proposal says (measured by reading it against the checker and the CRO table)

1. **21 Opal type words and 8 action words.** Each type word carries its definition, ONE action word and ONE flow class (the brief's names). An action is derived from the type through this one table, never typed on a transaction. Action words: Contribution, Withdrawal, Trade, Income, Fee, Tax, Transfer, Adjustment.
2. **82 mapping rows**, one per source value in the round-120 record (49 Financial 18 = 3 action + 15 type, Cottonwood 16, Inflection 48). **6 are UNMAPPED with a reason:** 49 Financial `sb_cd` FC, IC, JR (each spans several CRO meanings, so no single word), the `tr_cd` FC cash marker as an action, and Inflection's Starting Value and Remark (a synthetic seed or shape-dependent).
3. **The rule-24 record:** four postulates (each over 40 characters), a word-boundary census (denominator 82, brief flow classes 7, per-word counts equal to the count the checker computes from the mapping, 6 unmapped).

## What this seat checked beyond the worker's pass, and one flag for the ratification

I spot-checked 49 Financial's mappings against the CRO classification table (187 rows): `sb_cd` DV, FI, FO, WD, WH, WI, TA, RO and RD map to the words the table's `rule` names. **One row differs from the table's rule:** `sb_cd` TR is mapped to **Adjustment** because the table's description reads "ADJUSTING ENTRY", but the table's own `rule` and `category` for it are `trades` / `Trades`. A buy or a sell cannot be told from this code alone, so the honest choices are Adjustment (the description) or UNMAPPED (the rule says trades, the side is unknown). This seat did not edit the worker's record; the CTO decides this one row at ratification. Also for the ratification: worker rows W802-S1 (the brief's seven flow classes name no tax value, so Tax withheld carries INTERNAL as a default), S2 (FC, IC, JR span several meanings), S3 (two Orion dividend-family values sit in the Internal bucket while their Opal word carries INCOME).

## Rows (all OBSERVATION, INERT)

W802-S1, S2, S3 (above). Seat rows S106 and S107 remain ARMED (S103 disarms when the transaction contract and producer land with their L9; the contract is not cut).

## The one real run

None possible: a proposal record, nothing served. **Thread live: n** for FWD-5.

## For the CTO's analysis (the enrichment list this seat proposes, in order)

1. **Ratify the words** (decide the `sb_cd` TR row), so the transaction contract can be written. Then this seat writes `IRPT_DASHBD_ACCOUNT_TRANSACTION_CONTRACT.json` (sole writer) with the enum from the ratified table, and the per-firm producer (cross-firm fence: per-firm prefixes only; 49 Financial first, since Cottonwood and Inflection have no served series yet).
2. **FWD-3 mount** (`DB-f-803`): unchanged from the round-121 analysis; waits on `~D2`'s published `class_object` 0.4.0 and `~S2`'s route member, and carries the `CLASS_SERIES_EMPTY` reader fix.

-- 2.0.0_SA_COO~F2
