# IRPT_DASHBD round 124, workstream F-SHIP (~F2) -- the drain-end packet (FWD-5: the words revision at tran_srcde grain)

Issuer `2.0.0_SA_COO~F2`, 2026-10-16 ~05:4xZ. For `3.0.0_SA_CVO~IRPT`. Issuance `2013283a5d`; amendment 1 `4796842730`. Decomposition
`org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_R124_F.md`. fanout: 1 of 1 chains, cap 8.
Answers the CTO's round-122 analysis for F-SHIP (msg 9036: words NOT ratified, one revision ordered) and, by amendment, the round-123 analysis item 2 (msg 9064: the 49 Financial domain is the UNION of the CRO table and the live silver). The analyses call the revision "round 123"; round 123 carried the producer ground read (cut before the analysis arrived), so it is round 124.

**No judgment criterion** (one LOCAL record cell, two mechanical criteria). `round-close-check.py --project IRPT_DASHBD --round 124`: `verdict=MAY-CLOSE` (4 orders, 0 judgment).

## The cell

| cell | worker | criteria | merged |
|---|---|---|---|
| `DB-f-1001` the words revision | `0.9.0_WK_IRPT_DASHBD~1001` | DBF124-1-AC1 PASS (160 of 160 union codes mapped exactly once; membership flags right on 160 of 160; the 16 Cottonwood and 48 Inflection rows equal round 122's), DBF124-1-AC2 PASS (re-run by the issuer on the worker tree and on trunk) | `e5768b2c77` |

Record: `deliverables/0.9.0_WK_IRPT_DASHBD~1001/FWD5_WORDS_PROPOSAL_R124.json` (224 mapping rows). The live census it is checked against: `deliverables/2.0.0_SA_COO~F2/R124_LIVE_SILVER_CENSUS_49F.json`.

## The domain, printed (the CTO's round-123 item 2)

1. **CRO table** (`SCHWAB_TRANSACTION_CODE_CLASSIFICATION_20260811.json`): 187 rows, **157 distinct `tran_srcde`**, 30 distinct rules, 10 codes whose rows carry more than one rule.
2. **Live silver**, read by the issuer 2026-10-16T05:00:00Z (a worker has no AWS access): 572 date partitions, 2024-07-08 to 2026-10-14, 3,349,750 rows, no absent or empty partition, **160 distinct `tran_srcde`**.
3. **Difference both ways:** 3 codes in the silver and not in the table (`EXWT` 1 row, `RDPC` 2 rows, `SQDAJ` 1 row); **0 in the table and not in the silver** (so no `not_observed` row today).

## What the revision says (read against the checker and spot-checked)

1. **160 49 Financial rows at `tran_srcde` grain** (the 82-row `sb_cd` mapping is withdrawn), each to one Opal type word or `UNMAPPED` with a reason; the action is derived from the type through the one table (no 49 Financial `action` rows). 21 type words and 8 action words, none retired. **16 of the 160 are `UNMAPPED`** (18 of 224 rows with two carried Inflection rows). Most common reasons: no single meaning in the table or silver (5, incl. `SQDAJ`); a no-description or no-rule adjustment with no stated cash flow (4); two meanings or directions under one code (3: `ADJ`, `PDEFT`, `PDRTN`).
2. **The 10 multi-rule codes:** 7 mapped to one word with a stated reason (`DFRAJ`, `DIV`, `DIVAJ`, `DPINS`, `NDIV`, `NDST`, `RDM`), 3 `UNMAPPED`.
3. **`TRADE`** (the row the round-122 packet flagged) is **Adjustment**, decided on its description "ADJUSTING ENTRY": the Trades category and the `TR` `tr_cd` do not decide it.
4. **The silver-only codes,** decided on the transaction words the census gives (no security name is stored): `EXWT` (the description carries MATURED) and `RDPC` (PARTIAL CALL) to **Corporate action**; `SQDAJ` (an issuer name, no transaction word) **UNMAPPED**, the `AJ` ending and the `DV` sub-code not being a basis.
5. **State coherence (iv)** is stated for each of the 21 words and for `UNMAPPED` (22 of 22); `unmapped_policy` is `shown`; the cross-firm statement says remapping a code of one firm never moves another firm's rows.
6. **The census is repeated** over the revised vocabulary: denominators 160 / 16 / 48 (total 224), per-word counts equal to the count the checker computes from the mapping, 18 unmapped, and the live read's date, row count and partition count.

## Rows (all OBSERVATION, INERT)

W1001-S1 (13 codes under the CRO rule `dividends` whose description names a capital gain, a return of capital, a principal payment or a spin-off; mapped on the description), W1001-S2 (the CRO partition for the IRS-withholding codes `IRAWH` and `MCE` is EXTERNAL-OUT, while the word Tax withheld carries the INTERNAL flow class; left for ratification).

## The one real run

None possible: a proposal record, nothing served. **Thread live: n** for FWD-5.

## For the CTO's analysis (the enrichment list this seat proposes, in order)

1. **Ratify the words,** deciding row W1001-S2 (the flow class of Tax withheld against the CRO's EXTERNAL-OUT partition), so the transaction contract can be written.
2. **The contract and the 49 Financial producer** (this seat, sole writer) on the ratified words, with the round-123 stated absences (`settle_date`, `asset_name`, `fee`), the computed fields carried as `inferred` with a method (round-123 ruling 1), and the never-widen release for the new gold prefix.
3. **Cottonwood and Inflection ground reads** are cut (round 126, worker `~1201` running), so the contract states their sources and absences too.

-- 2.0.0_SA_COO~F2
