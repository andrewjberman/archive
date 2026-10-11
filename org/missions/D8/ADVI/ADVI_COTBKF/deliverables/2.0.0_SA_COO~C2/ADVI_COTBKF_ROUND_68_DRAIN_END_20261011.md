# L8 drain end -- ADVI_COTBKF round 68: the chain from a clean checkout, the pin in the mint, the spin-off read, r29 at the served instant's pin, the outlier days by cause

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-11 ~15:04Z | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB68bp3-AC2, CB68bp4-AC2, CB68bp5-AC2)
**Cut on:** `1.0.0_SA_CTO~DELL2` round-68 analysis @b3a272fffc. **Issued:** @f325600fbf, 5 cells (4 at once; CB-bp-4 after its two
dependencies drained). **Nothing served moved. No re-mint, no vendor call, nothing written remotely.**

| order | item | worker | state | issuer's own run at the drained base |
|---|---|---|---|---|
| CB-bp-1 | the regrade completes from a clean checkout; the price input is reproducible (direct-act) | ~101 | complete @10f1765052, drained @1051a1eba0 | `CLEAN-CHAIN-RECORD rc=0 extra_flags=0 report_inputs=5 price_input=DROPPED price_input_equal=True tables_equal_to_proof_a=True` |
| CB-bp-2 | the mint adapter carries the split-store pin; `--apply` refuses without it (direct-act) | ~102 | complete @0f2e7cd1c1, drained @50171dcbde | `ARD-PIN-CARRIED split_store_mentions=21 apply_refusal=True verify_token=True`; the REAL verify of today's table: `ARD-COTTONWOOD-VERIFY days=3325 match=3325/3325 sidecar=match method_row=match manifests=3325/3325 split_store=absent` |
| CB-bp-3 | the four spin-off events against the custodian's own price; a claim per event | ~103 | complete @e584d0b1ea, drained @a8fe2b856b | `SPINOFF-CLAIMS-RECORD events=4 ... claims=UNAPPLIED_NO_HELD_DATE,UNAPPLIED_NO_HELD_DATE,UNAPPLIED_NO_HELD_DATE,UNAPPLIED_NO_HELD_DATE dates_compared=0,0,0,0` |
| CB-bp-4 | `method_r29` against the served table at the served instant's pin | ~104 | complete @c7e18a16ac, drained @b3e47e0d68 | `R28-VS-R29-AT-PIN-RECORD as_of=2026-10-09T11:52:52Z listed=32 control_rows=1691729 control_differing=0 rows_union=1691729 class_sum=1691729 changed_account_days=2 changed_dates=2 spinoff_events_in_store_at_pin=0` |
| CB-bp-5 | the 179 measured days above 10 percent on a base of 100.00 or more, by cause | ~105 | complete @3b90849ca5, drained @9aaa549183 | `OUTLIERS-ON-A-REAL-BASE-RECORD days=179 above_100pct=57 from_10_to_100pct=122 classes=9 class_sum=179 unclassed=0 read_row_by_row=77 placed_by_rule=102` |

Suite at the base after the last drain (@b3e47e0d68), issuer run: `889 passed, 12 skipped`. The suite was run at every drain of the round.

## What the issuer checked itself, and what it did not

- Read every product diff before draining (the valuation and regrade changes of CB-bp-1; the adapter's +47/-1 of CB-bp-2).
- Ran each record's criterion at the base; ran the adapter's REAL `--verify-served` against the stamped manifest of the table served
  today (3,325 of 3,325; the new token reads `absent`, which is right: that table was minted before the pin existed).
- Read the custodian-mark store's local cache: 564,563 rows, days 2026-06-08 to 2026-10-06, one source label `bd_snapshot`.
- Read `CHANGED_DATES_AT_PIN.csv`: 2 rows, 2014-12-03 and 2020-11-13, no account column.
- **NOT re-run or re-derived:** the four build runs of CB-bp-4 (the worker's, 494 s to 571 s each) and its class counts; the two clean
  regrade runs of CB-bp-1; every comparison inside CB-bp-3; the placing of the 179 days.

## For L9

**CB68bp4-AC2 (the list at the pin).** The control is exact: `method_r28` at `as_of=2026-10-09T11:52:52Z` equals the served table on
1,691,729 of 1,691,729 rows. `method_r29` at the same pin differs from the SERVED table on 2 account-days, both measured under both,
both a withholding day with no withdrawal row; 0 other days, 0 other accounts, 0 of 82,593 month verdicts, 0 ABSENT changes. The two
dates are round 66's. Both regrade logs print one identical pin line (listed=32) and equal price tables. The worker ran all four
steps itself from the clean worktree and reused nothing. **For the grade:** the served build ran at code commit 728d223ddc and these
runs at 21055cff57; only the control covers that difference. 41 of the 71 withholding days carry a changed flow but are blank under
both rules: they would change under r29 if priced later and are not in this list. One check of the worker's printed five ABSENT
`account|month` keys into its own session output; it says they reached no file.

**CB68bp3-AC2 (the spin-off claims).** All four are `UNAPPLIED_NO_HELD_DATE`: the store the code calls the custodian's mark starts
2026-06-08, after every event. Three things for the grade, as the worker states them:
- **Whether that print is the custodian's own** rests on the code's comment; its label says it is the portfolio system's report of the
  holding.
- **A second candidate, kept separate and deciding nothing:** the price implied by the custodian's own trade rows. On it the claims
  would read APPLY (16 dates), DO_NOT_APPLY (4), APPLY (4), APPLY (1). Whether the ruling's "the custodian's own price" admits a
  price derived by division from a trade row is the CTO's.
- **Row D2-W103-S2 corrects round 67:** the "independent" price step that round's record cited equals the vendor's step divided by the
  factor to four digits; it is the with-factor table's own step, not a second source. The events remain real by the custodian's
  cost-adjustment rows.

**CB68bp5-AC2 (the outlier days).** Nine causes, 0 unclassed: income paid after the holdings left 119 (FORM); a fee refund credited
after the assets left 43 (FORM); a real price move 10 (TRUE_RETURN); a withholding taking the whole balance 2 (FORM, the `method_r29`
case); a fee debit on cash 1 (TRUE_RETURN); a fee owed elsewhere taken as a drag 1 (FORM); a 12b1 credit 1 (FORM); a sale against a
split-adjusted close 1 (PRICE); an in-kind contribution on a mis-scaled close 1 (PRICE). 77 days read row by row, 102 placed by rules
derived from them. **For the grade:**
- The worker DISAGREES with round 65 on the kind of one day (PRICE, not FORM): one security's whole close series sits about 6.6 times
  below its traded price on all four trades checked. Whether other securities carry that scale defect was not scanned.
- Its observation for the threshold, not a ruling: a prior value of 100.00 does not separate the classes; the account's own
  prior-30-row outflow of 100 times the base does (152 of 152 such days are in the two exit classes; 0 of the other 27).
- Whether income paid after an exit and a fee refund are FLOWS is a policy call it did not make; "FORM" here means the form's present
  treatment produces a return that is not a market return, not that a fix is agreed.
- Round-65 matching is by count only: that record carried no day keys.

## Rows and gaps of the round

- **D2-W101-S1:** the as-traded basis also reads an untracked Yahoo Close cache (3,580 files) from a fixed path with no flag. A truly
  empty checkout still stops there; both CB-bp-1 and CB-bp-4 ran with a copy of the pinned directory. So "from a clean checkout"
  holds for tracked code and flags, NOT for that cache.
- **All five report inputs are NOT AVAILABLE lines**, none rebuilt (each is a full multi-arm regrade). The tables are unaffected.
- **D2-W103-S1, D2-W103-S2:** above.
- **Issuer note on CB-bp-2:** the pin is carried from a LOCAL FWD-3 manifest given by path, while the mint reads its tables from the
  served objects. Nothing in the adapter ties that manifest to those objects; the manifest carries the tables' content hashes, so a
  check is possible. Not cut. `build` itself was not run (it needs S3); the carry is tested through its helper.
- **Merge refusals:** two `safe-merge` runs were refused while another lane's merge held the shared tree; retried, not overridden.

## Where this leaves the re-mint

- **At the served instant's pin:** the withholding rule's list is 2 account-days on 2 dates, stated against the served table; the 30
  drift days do not exist at this pin (they belong to the grown store); the four spin-off events are not in the store.
- **Not decided here, the CTO's:** the default leg; the pin a re-mint uses; whether the trade-price candidate may decide a spin-off
  claim; the leftover-balance rule; the treatment of income and fee refunds after an exit. No re-mint order is cut.

**Round-close check:** REFUSED until the three judgment criteria are graded.
