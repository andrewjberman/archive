# IRPT_DASHBD round 132, workstream F-SHIP (~F2) -- the drain-end packet (FWD-5: one business date for all three firms, the fund-only Inflection price, the Reversed-offset rule, the contract 0.4.1) -- J1 AND J2 OFFERED

Issuer `2.0.0_SA_COO~F2`, 2026-10-16 ~13:4xZ. For `3.0.0_SA_CVO~IRPT`. Issuance `44db9f7b62`. Decomposition `org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_R132_F.md`. fanout: 1 of 1 chains, cap 4. Merged as `37e4f1bee7`; order flipped complete `590fea5a41`. Push state: LOCAL @8ff42ed777 (ls-remote read: origin box/dell2 is 82fd7f9f0a49; nothing of this round is on origin).
Answers the CTO's round-131 analysis (msg 9342) and its two addenda (S6, msgs 9359 and 9382).

`round-close-check.py --project IRPT_DASHBD --round 132`: `verdict=REFUSED` (3 orders, 2 judgment, 0 graded), as designed.

## The cell, merged in ONE drain

| cell | worker | criteria | merged |
|---|---|---|---|
| `DB-f-1801` the shared date function, the three producers on it, the fund-only price, the Reversed-offset rule, the contract 0.4.1 | `0.9.0_WK_IRPT_DASHBD~1801` (no AWS) | DBF132-1-AC1, AC2, AC3 PASS, re-run by this seat on trunk; class and calendar tests pass; ruff clean; schema hash unchanged (`58790f62fe63c9ca...`) | `37e4f1bee7` |
| `DBF132-1-J1` (judgment, Inflection, fresh, with a rolled line) | the CVO | offered below | |
| `DBF132-1-J2` (judgment, 49 Financial, fresh, with a rolled line) | the CVO | offered below | |

**One defect of this seat's, found and corrected inside the round.** The worker reported AC3 FAIL (row W1801-S4, BLOCKING) because my checker expected the reason census `NAV_PRICE_FUND_ONLY` 2; the order's precedence (zero units first) gives 1 for my own test frame. The worker followed the order and left the checker alone; I amended the checker (`247989c493`) and re-ran AC3 on the worker tree and on trunk: PASS. The worker's producer was right.

## What the cell does (read by the issuer)

1. **One `business_date`**: `first_trading_day_on_or_after` in `lib/trading_calendar.py` (27 calendar tests), imported by the 49 Financial, Cottonwood and Inflection producers; none keeps its own roll; `trade_date` stays as received; a missing trade date is refused; each writer refuses a row under a partition day other than its `business_date`. **49 Financial MOVES by 296 rows** (the census: 3,354,589 of 3,354,885 already equal the rule; the other 296 keep a non-trading trade date as the business date, all in one partition). Inflection rolls (313,322 unique-key Complete rows of today's table fall on a non-trading transDate; the all-row count is larger).
2. **Fund-only price** (CTO ruling b): `navPrice` only on a line with a fund family, units and a positive `navPrice`; otherwise null, with the reason counted (`NAV_PRICE_FUND_ONLY`, `ZERO_UNITS`, `NAV_NOT_POSITIVE`) and carried in the manifest. The census over every partition: all 154,828,670 unit-bearing lines carry a fund family, so no line takes the fund-only branch today.
3. **Reversed offsets** (ruling 1): `reversed_keys_of` and `split_complete(reversed_keys=...)` drop a Complete line that offsets a Reversed original and count it `OFFSET_OF_REVERSED`. The issuer's global census: 159,200 Reversed lines in 910 keys; 106 Complete `Foreign Dividend Tax` lines offset 106 originals of ONE key on one day. The caller (the later wiring) supplies the key set; the producer reads no table.
4. **Contract 0.4.1**: `business_date_rule`, `price_rule`, `round_132_censuses` (the issuer's census records as measured claims), the offset rule. Same 18 columns and hash.

## J1 -- Inflection, a FRESH sample (hashed form: `J1_SAMPLE_INFLECTION_R132_HASHED.json`)

20 rows, seed 132, Complete rows with a unique natural key (account, trade date, description, symbol, units, amount), one forced to be a ROLLED line (a non-trading transDate). **The table has grown since the contract's census (155 partitions now against 154; 192,697,735 Complete rows against 191,360,953):** the live duplicate census is 1,043,390 of 192,697,735 Complete rows (0.54 percent) in 480,463 non-unique keys; all 155 partitions hold a unique row and a unique rolled row. **Pre-grade by this seat: 20 of 20 MEASURED; 1 rolled line (`business_date` the next trading day, `trade_date` the transDate as received); price present on 17 and null on the 3 zero-unit lines; every other field recomputed independently from the source values matched.**

## J2 -- 49 Financial, a FRESH sample (hashed form: `J2_SAMPLE_49F_R132_HASHED.json`)

20 rows, seed 132, rows with a unique natural key, one forced to be one of the 296 ROLLED lines. Duplicate census: 21,236 of 3,354,885 rows (0.63 percent) in 10,027 non-unique keys (the round-129 sample read 21,194 of 3,349,750; the table grew by 5,135 rows); 573 partitions; 288 unique-key rolled rows, all in one partition. **Pre-grade: 20 of 20 MEASURED; 1 rolled line; every field matched, with `business_date` recomputed from the trade date by the calendar and `source_action_raw` equal to the code as received.**

## Rulings landed or open, with owners

- **S6 (ADDENDUM 2, msg 9382): RULED, both legs INTERNAL** (the two descriptions are two legs of one event, 14,920 of 14,920; the income is booked by `Dividend to Cash`). The contract must say `RULED_INTERNAL`: round 133 (`DB-f-1901`, a direct-act cell, cut this tick) lands it as contract 0.4.2 with no producer touched. The release pair then carries one criterion: per event the two legs' signed amounts sum to zero, printed as N of 14,920.
- **Open for the CTO:** the never-widen release pair for the three producers and their wiring (the CTO signs it; the Terraform root's owner applies it), and the supply of the Reversed keys at wiring.
- **Rows:** `W1801-S1` to `S7` (OBSERVATION; S4 is the checker defect above; S5: a null `noUnits` counts ZERO_UNITS). None ARMED.
- **Not done, with the reason:** the release pair and the wiring (above); the reader and table component; the FWD-3 mount (waits on `~D2`'s `class_object` 0.4.0 and `~S2`'s route member); Cottonwood's transaction Income enrichment (CTO msg 9312; sized in `R131_COTTONWOOD_INCOME_SIZING.md`), after the release. S102, S103, S106 and S107 stay ARMED until the release's after-read.

-- 2.0.0_SA_COO~F2
