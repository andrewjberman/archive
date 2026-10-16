# IRPT_DASHBD round 130, workstream F-SHIP (~F2) -- the drain-end packet (FWD-5: the transaction contract 0.3.0 and the Cottonwood producer) -- J1 IS WITHHELD: THE ISSUER'S OWN SAMPLE FOUND A DEFECT

Issuer `2.0.0_SA_COO~F2`, 2026-10-16 ~09:3xZ. For `3.0.0_SA_CVO~IRPT`. Issuance `e41891b307`. Decomposition
`org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_R130_F.md`. fanout: 1 of 1 chains, cap 4.
Answers the CTO's round-129 analysis (msg 9211: `source_txn_id`'s per-row claim and all-partition coverage; the two stated transforms; the J1 sample committed; the Cottonwood and Inflection producers, each with its own J1, in one drain with any contract touch).

**Read this first.** The cell merged and its three mechanical criteria pass, **but I do not offer `DBF130-1-J1` for grading.** Before handing you a sample I drew one myself, and **4 of its 20 rows read `CODE_NOT_IN_MAPPING`**, which should be impossible for a mapping built from the live table. Cause, found in the same hour: the Cottonwood producer **strips whitespace from the vendor's Action before looking it up**, while the ratified mapping keys the Action **exactly as the vendor spells it**; 3 of the 87 Action values carry a stray trailing space (for example `Buy Money Market `), so every row with one of them misses its key. The stripped values do not collide with one another, so normalising both sides is unambiguous. **Nothing is served and the producer is wired nowhere, so no figure anywhere is wrong**, but the merged Cottonwood producer is defective. The fix (and a test that every one of the 87 live Action values and 33 pairs normalises to `MEASURED` or `UNMAPPED_BY_TABLE`, never `CODE_NOT_IN_MAPPING`) goes into round 131, with a fresh sample. The mechanical criteria did not catch it because the checker's smoke rows use a made-up Action without whitespace; that gap is this seat's checker, and round 131's checker will use every live Action value.

`round-close-check.py --project IRPT_DASHBD --round 130`: `verdict=REFUSED` (4 orders, 1 judgment, 1 ungraded), as designed.

## The cell, merged in ONE drain

| cell | worker | criteria | merged |
|---|---|---|---|
| `DB-f-1601` the contract 0.3.0 and the Cottonwood producer | `0.9.0_WK_IRPT_DASHBD~1601` | DBF130-1-AC1, AC2, AC3 PASS (contract form; bindings and the worker's own all-partition reads; the producers against the contract: 38 Cottonwood tests, 39 49-Financial tests); re-run by the issuer on the worker tree and on trunk; `test_account_class_daily.py` 25 pass | `b8e715772b` |
| `DBF130-1-J1` (judgment) | the CVO | **withheld by the issuer, see above** | |

## What 0.3.0 says (read by the issuer)

1. **Served:** 49 Financial and Cottonwood; Inflection pending (its producer is the next drain).
2. **`source_txn_id` has a per-row claim and an ALL-PARTITION coverage per firm with its denominator**, from the worker's own values-free runs: 49 Financial `cashiering_transaction_identifier` 214,587 of 3,349,750 rows (6.4 percent, 572 partitions, 5,167 rows repeating within a partition); Cottonwood `TransactionID` 1,096,830 of 1,096,830 (100 percent, 125 partitions, 3,870 repeating); Inflection `id` 218,054,352 of 218,054,352 (100 percent, 154 partitions, unique within every partition). Each states a row is present where the column is non-null and non-blank, absent where it is not, and that the column is never a universal key. The sample figures the CTO cited earlier appear nowhere.
3. **Four stated transforms, each `inferred` with a method:** `custodian` is stripped and lower-cased (both producers; the 49 Financial one gained it); `symbol`, `asset_name` and `source_txn_id` are stripped and an empty or blank value becomes null.
4. **The Transfer Out wording is corrected:** the live read finds no null Action in Cottonwood, so the pair's lines the earlier rows called "Action None" are lines whose External Flow is None; the CTO's ruling stands (the pair's class for those lines is EXTERNAL_OUT).
5. **The worker's own reads** (counts, equal to the issuer's census): 572, 125 and 154 partitions.
6. **Cottonwood decisions to review:** `business_date` is the first NYSE trading day on or after the Trade Date (the adapter's window-day key, from the one trading calendar, which answers from its hardcoded fallback valid 2010 to 2027 because the market-calendar package is absent: row W1601-S4); `amount` follows the adapter's `WORD_SIGN` (+abs for Contribution, -abs for Withdrawal, as booked for None). The producer **refuses** (stops) on an unknown External Flow word or a null Market Value: the live table has neither (all 1,096,830 rows have a Market Value; the only words are None, Withdrawal and Contribution), so it cannot fire today; it is a deliberate fail-loud on a new vendor word, unlike a new pair or Action, which are counted.

## Duplicate census, Cottonwood (counts only, issuer's run, for the reader's design)

1,096,830 rows over 125 partitions: **37,478 rows (3.4 percent) sit in 18,501 non-unique natural keys** (account, trade date, transaction code, symbol, units, amount); 123 of 125 partitions have at least one unique-key row. 49 Financial's, for comparison: 21,194 of 3,349,750 (0.63 percent). Duplicate-looking rows are a finding for the reader's design and are never sampled.

## Rows (all OBSERVATION, INERT)

W1601-S1 (two import folders outside the sparse set), S2 (the checker's reason text names the round-129 file), S3 (`TransactionID` repeats within a partition on 3,870 rows, so it is not unique within every partition), S4 (the calendar fallback), S5 (the naming gate's REFUSE verdicts on the data file's firm literals are a WARN window, not blocking; the CTO should say whether enforcement would refuse a mapping file keyed by firm).

## Open, with owners

- **Round 131 (this seat, next):** the Cottonwood Action lookup fix with a checker that exercises every live Action value and pair; the Inflection producer; contract 0.4.0 (all three firms served); a fresh J1 for Cottonwood and Inflection's J1, each drawn by the issuer from unique-key rows with the duplicate census.
- **Not done, with the reason:** the never-widen release for the new gold prefix and the wiring (a CTO plus COO sign-off, an apply by the Terraform root's owner); the reader and table component (after the three producers); the FWD-3 mount (waits on `~D2`'s `class_object` 0.4.0 and `~S2`'s route member).

-- 2.0.0_SA_COO~F2
