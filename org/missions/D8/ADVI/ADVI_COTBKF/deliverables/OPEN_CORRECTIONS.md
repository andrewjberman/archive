# OPEN_CORRECTIONS -- ADVI_COTBKF, revised round 72 2026-10-11T18:53:00Z by 0.9.0_WK_ADVI_COTBKF~122 (round 71 by ~117; compiled by 0.9.0_WK_ADVI_COTBKF~111)

The list is `OPEN_CORRECTIONS.json` beside this file. Served table: `method_r28`. Tree default: `method_r29`. Pin: 2026-10-09T11:52:52Z, sha256 `4aca4f1fa311712424df5daf91b68048ff362a88874033e53b31c8b706a362c7`.

List closes when (PRD line 282, ADDENDUM v0.7): "One re-serve carries all of them, once, when that list is closed."

Extent cells read `NOT_MEASURED` where no record holds the number. Counts below are as the records print them; where two records differ both are in the JSON `unreconciled`.

| id | state | measured account-days | other extent | closes when | owner |
|---|---|---|---|---|---|
| withholding-flow-and-return | OPEN | 2 | 42 flow cells on blank days; day files 43 by real change, up to 46 by bytes (reviewer: 47 rows over 46 dates, 44 real, 3 residue on zero); 3 silver objects | the one re-serve under its own pair, stating both day-file numbers | 2.0.0_SA_COO~C2 |
| unpriced-withholding-days | OPEN | NOT_MEASURED | 41 (counts of 41, 42, 45 not reconciled) | a ruling on pricing them, and a measurement | 1.0.0_SA_CTO~DELL2 |
| mis-scaled-price-series | OPEN | 470 | 8 series; never without 334 too few, 44 thin with a pair beyond 10 percent, 1,700 with no close (974,014 not-measurable account-days) | a ruling on which are corrected, with the dividend entry's ruling | 2.0.0_SA_COO~C2 |
| dividend-adjusted-fund-series | OPEN | 3,187 by the round-71 vendor test; 712 by the round-72 custodian check | Two instruments, both held. ROUND 71 (vendor against itself): 72 of 73 tested read adjusted of 270 fund series; 124 untested; 287,912 priced holding account-days; 60 measured days on a distribution date. ROUND 72 (custodian reinvestment price): of 270, 19 confirmed adjusted, 15 confirmed not, 236 nothing to test on; 261,182 priced holding account-days; 0 disagreements with round 71. Round-71 criterion graded MET (nine and the count as a count; one limb not met for 63 of 72); this round's record not yet graded at the time of this update. Ruling (CTO round-72 analysis lines 17-18): "The basis for a fund series is the unadjusted value the fund traded at on the day, and a series that is not that is a defect of the store, not a method." Where a corrected series would come from: NOT_MEASURED (record absent at the time of this update) | a ruling on the price basis, and a measurement of the 124 untested | 1.0.0_SA_CTO~DELL2 |
| spinoff-factor-2022-event | OPEN | 28 | evidence reads APPLY: 15 of 16 pairs within 2 percent with the factor, 0 of 16 without; 3,434 priced holding account-days over 448 dates; level enters on 1 of 28 | a PRD addendum owed by 1.0.0_SA_CTO~DELL2 (none yet; latest is v0.7), then the re-serve | 1.0.0_SA_CTO~DELL2 |
| method-version-label | OPEN | NOT_MEASURED | method row names method_version 3 | a ruling on the label | 1.0.0_SA_CTO~DELL2 |

Still unreconciled (JSON `unreconciled`): blank rows with a changed flow, 42 account-days (REMINT_FACTS.md) against 45 rows (issuer packet); the four counts of unpriced withholding days; the two dividend-adjusted instruments' reaches differ (3,187 against 712 measured account-days) because the confirmed set differs (72 against 19), and 53 series read adjusted by the vendor test cannot be read by the custodian check; the dividend-adjusted and mis-scaled entries count some of the same series (AMBFX, BALCX, OIEJX), and the mis-scaled entry still includes ticker T, the 2022-factor security.

## Tooling

Not a correction to the served table. The re-mint mode (REMINT_FAILURE_PATHS.json, round 71): 18 failure points, each with a test; its own output describes 8 and does not describe 10; 5 leave half a pair; not run against the bucket. Repair ordered by 1.0.0_SA_CTO~DELL2 (round-72 analysis section 2 item 3); in flight as CB-bt-3 at the time of this update. REMINT_REPAIR.json: NOT_MEASURED (record absent at the time of this update).

## Struck

`late-receipt-rule` is struck by 1.0.0_SA_CTO~DELL2 (round-71 analysis section 2 item 3, msg 5458): out of sample its constants read 72 of 77 one way and 37 of 85 the other. What stands: the round-69 ruling that a receipt arriving after an account's assets left is neither a return nor a contribution; how such a day is recognised is open, and no day is blanked on it.

Build gaps, not corrections to the served table (JSON `not_established`): the five report inputs that print NOT AVAILABLE in a clean checkout; the as-traded basis's price-basis census csv, unpinned.
