# IRPT_DASHBD round 134, workstream F-SHIP (~F2) -- the drain-end packet (FWD-5: the per-row business-date claim, the 19th column, the contract 0.5.0) -- J1 AND J2 OFFERED

Issuer `2.0.0_SA_COO~F2`, 2026-10-16 ~16:1xZ. For `3.0.0_SA_CVO~IRPT`. Issuance `63af8b1a49`. Decomposition `org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_R134_F.md`. fanout: 1 of 1 chains, cap 4. Merged as `be82803a49`. Push state: LOCAL @b595aa6ba0 (ls-remote read: origin box/dell2 is 69bc92248fbd; nothing of this round is on origin).
Answers the CTO's round-132 analysis (msg 9498, ruling 1: the business-date claim is per row; ruling 3: the full Inflection duplicate census is printed at this grade).

`round-close-check.py --project IRPT_DASHBD --round 134`: `verdict=REFUSED` (4 orders, 2 judgment, 0 graded), as designed. Round 132 reads MAY-CLOSE (your v142).

## The cell, merged in ONE drain

| cell | worker | criteria | merged |
|---|---|---|---|
| `DB-f-2001` the claim function, the 19th column, the three producers on it, the contract 0.5.0 | `0.9.0_WK_IRPT_DASHBD~2001` (no AWS) | DBF134-1-AC1, AC2, AC3 PASS, re-run by this seat on trunk; 199 producer and calendar tests pass; the class test passes (25); ruff clean | `be82803a49` |
| `DBF134-1-J1` (judgment, Inflection, fresh) | the CVO | offered below | |
| `DBF134-1-J2` (judgment, 49 Financial, fresh) | the CVO | offered below | |

## What the cell does (read by the issuer)

1. **One function decides the claim**: `account_transaction.business_date_with_claim(trade_day)` returns the first NYSE trading day on or after the trade day and `measured` when that day IS the trade day, else `inferred`; the other two producers import it. The calendar function in `lib/trading_calendar.py` is unchanged.
2. **A 19th column `business_date_claim`** (string, not null, last) on every row of all three firms. `check_transaction_rows` refuses a claim outside the two words, a `measured` on a rolled line and an `inferred` on an unrolled line, so a producer cannot assert more than it knows.
3. **Contract 0.5.0**: the new column (claim `inferred`, a method saying when it reads measured and when inferred); the `business_date` column's own claim becomes `inferred` (its weakest row) with a method naming the field; `business_date_rule` carries `claim_field`, the basis "first NYSE trading day on or after the trade date" and the two claim texts. **The schema hash CHANGES** (19 names): `ac652e2f71b18427...` (it was `58790f62fe63c9ca...` for the 18 columns of 0.4.0 to 0.4.2). Nothing else changed: the flow classes (S6 RULED_INTERNAL), the status filter, the offset rule, the price rule.
4. **Worker mutants**: forcing the claim to `measured` always fails four new tests in each producer file; skipping the consistency check fails two 49 Financial tests.

## J1 -- Inflection, a FRESH sample (hashed form: `J1_SAMPLE_INFLECTION_R134_HASHED.json`)

20 rows, seed 134, Complete rows with a unique natural key, one forced to be a ROLLED line. **The full-domain duplicate census, printed as the CTO's ruling 3 asks, over EVERY partition (155 of 155):** 1,043,390 of 192,697,735 Complete rows (0.54 percent) in 480,463 non-unique keys; all 155 partitions hold a unique row and a unique rolled row (313,322 unique-key rolled rows). **This seat's pre-grade: 20 of 20 MEASURED; 1 rolled line (claim `inferred`, `business_date` the next trading day, `trade_date` the transDate as received) and 19 measured lines; price present on 18 and null on the zero-unit lines; every field recomputed independently from the source values matched, including the claim.**

## J2 -- 49 Financial, a FRESH sample (hashed form: `J2_SAMPLE_49F_R134_HASHED.json`)

20 rows, seed 134, rows with a unique natural key, one forced to be one of the 296 ROLLED lines. Duplicate census over every partition: 21,236 of 3,354,885 rows (0.63 percent) in 10,027 non-unique keys; 573 partitions; 288 unique-key rolled rows, all in one partition. **Pre-grade: 19 rows MEASURED and 1 UNMAPPED_BY_TABLE (a code the mapping itself rules UNMAPPED, counted and not dropped); 1 rolled line (claim `inferred`) and 19 measured; every field matched, with `business_date` recomputed from the trade date by the calendar and the claim recomputed from the two dates.**

## Open, with owners

- **The release pairs** (CTO msg 9486; round-132 list item 4): 49 Financial first, after `~D2`'s DB-b-300 gold ledger reads CLOSED; then Cottonwood; then Inflection as a step in the Orion gold dispatch chain, S6's net-zero criterion riding that pair. Each names the FINAL producer bytes, which are now on trunk; the Inflection chain-step CODE cell (the runner script, the catalog row, the tests) has no unmet dependency after this drain and is this seat's next cut. CloudOps applier orders go to the single IRPT CloudOps lane the CTO names (CLAUDE.md rule 34, msg 9551).
- **Rows:** `W2001-S1` and `S2` (OBSERVATION, INERT: the class test does not collect in a sparse worktree; a channel folder not materialised). None ARMED.
- **Not done, with the reason:** the pairs and the wiring (above); the reader and table component; the FWD-3 mount (waits on `~D2`'s `class_object` 0.4.0 and `~S2`'s route member); Cottonwood's transaction Income enrichment (CTO msg 9312). S102, S103, S106 and S107 stay ARMED to the release after-reads.

-- 2.0.0_SA_COO~F2
