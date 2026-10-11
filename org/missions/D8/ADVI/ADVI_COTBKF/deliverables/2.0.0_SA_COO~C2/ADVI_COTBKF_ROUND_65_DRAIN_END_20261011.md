# L8 drain end -- ADVI_COTBKF round 65: the 207 outlier days classed; two price requests written and not sent; method_r29 selectable

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-11 ~11:07Z | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB65bm1-AC2 and CB65bm2-AC3)
**Cut on:** `1.0.0_SA_CTO~DELL2` round-65 analysis @1e9128413f. **Issued:** @c15e72c38f, 3 of 3 chains. **No served write, no send, no re-mint.**

| order | item | worker | state | issuer's own run at the drained base |
|---|---|---|---|---|
| CB-bm-1 | the 207 measured days above 100 percent, classed | ~94 | complete @6546e422d1, drained @80348d1900 | `OUTLIER-DAYS-RECORD measured_rows_positive_prior=107311 outliers=207 prior_under_1=55 prior_1_or_more=152 classes=5 class_sum=207 unexplained=0 threshold_rows=6` |
| CB-bm-2 | the two price requests, written, NOT sent | ~95 | complete @7be65db679, drained @9bb6681873 | `PRICE-REQUESTS-RECORD position_rows=21102041 unpriced_position_rows=15993996 legs=2 leg_rows_sum=15993996 unpriced_securities=4408 leg_securities_sum=4408 bloomberg_rules=15`; `PRICE-REQUESTS-STATUS yahoo_not_sent=True bloomberg_not_sent=True yahoo_csv_rows=3102 bloomberg_csv_rows=1306` |
| CB-bm-3 | `method_r29`: a cash tax withholding is an outflow with or without a withdrawal row (direct-act) | ~96 | complete @32e919d40a, drained @803e5f2c14 | `WITHHOLDING-FLOW-RECORD withholding_account_days=4115 no_withdrawal_account_days=71 no_withdrawal_measured_days=7 flow_rule_version=method_r29 tests_added=18 tests_changed=0`; suite: **`1 failed, 839 passed, 12 skipped`** (see below) |

## THE SUITE IS RED AT THE BASE (row D2-S113) -- CB65bm3-AC1 is NOT met at the drained base

The one failure is `test_cotbkf_no_account_ids`: it counts 76 CUSIPs in CB-bm-2's two security lists as account-id shapes
(`76 shape hits and 0 account-set hits in 2 files`; 538 files scanned; the pinned set holds 4,710 ids). No account id is in either
file. Worker ~96's branch read 840 passed because its base predated CB-bm-2's drain. **Issuer defect:** CB-bm-2 was drained on its
two criteria without a suite run. The repair is a round-66 cell. Every other test passes, including the 18 added for `method_r29`.

## Issuer defects on record in this round (five)

1. **CB-bm-3 granted one file for a change that needs six** (row D2-S111). Worker ~96 stopped correctly.
2. **AMENDMENT 1 still under-granted** (the valuation script; row D2-W96-S2): the grant was written from a report, not a census. The
   census was then taken: 51 hits, 14 files of 407 scanned, 8 scripts and 6 tests. AMENDMENT 2 @ccd8d1ce68.
3. **AMENDMENT 2 moved the code default to r29 ahead of the CTO's addendum.** The issuer held the drain and asked; CTO msg 4772: the
   default stays `method_r28`. AMENDMENT 3 @e3dd6c3e67. Read at the base: `CASH_LEG_DEFAULT = CASH_LEG_METHOD_R28`, the line identical
   to its pre-order text, and four of the five touched test files show an empty diff against the pre-order base.
4. **CB65bm2-AC2's invocation was corrupted by the issuer's own template** (row D2-W95-S1). The assignee repaired element and proof
   instance together on the issuer's ruling; the issuer then ran both invocations as the order now states them (above).
5. **The red suite** (above).

Also: the orders told workers to mint `D2-S<k>` row ids; the gate requires `D2-W<n>-S<k>` from a worker. Worker ~96's first row
commit (fd47dde9c0) changed trailing whitespace on 206 channel lines and was not merged; its content is re-filed as D2-S111.

## What the issuer checked itself, and what it did not

- Read every product diff before draining. CB-bm-3: 6 scripts, 70 lines; `rides_withdrawal` and the r25 to r28 reason strings are
  untouched; the r28 sites became membership tests against one named set (`ROUND28_REPAIR_LEGS`, `ROUND28_FLOW_RULES`).
- Read both request documents and the shape of both security lists (no account column; the security-day sums equal the record's).
- Scanned the outlier record for an account-id shape: 1 hit, which is the number 107311.
- **NOT re-derived:** the placing of the 207 days in classes (the worker hand-checked 31); the per-leg counts and unblank shares; the
  reach counts 4,115 / 71 / 7 (measured twice by worker sessions, same result).

## For L9

**CB65bm1-AC2 (the 207).** Five classes, 0 unexplained. 206 are a credit landing on a leftover balance after a close-out, kind
RESIDUAL_BASE: income 3 + 105, a fee rebate 97 (94 carry note text beginning "Fee Rebate"; 89 dated 2026-05-22 or 2026-06-09), a fee 1.
One is FORM: an in-kind contribution valued at a close the next-day sale contradicts by 6.72 times. By prior value: 55 under 1.00, 95
from 1.00 to under 100.00, 57 of 100.00 or more. 147 of the 207 are dated 2026-05-20 to 2026-06-10. **For the grade:** 56 days called
RESIDUAL_BASE sit on a prior value of 100.00 or more (income 35, rebate 21); the worker says whether that is "too small to mean
anything" is the CTO's threshold and does not rule it. The threshold table over all 107,311 rows is in the record.

**CB65bm2-AC3 (the requests).** Yahoo leg: 3,102 securities (124 with no symbol), 1,556,036 security-days, could unblank alone
1,257,183 of 1,559,722 blank-for-price account-days (80.60 percent). Bloomberg leg: 1,306 securities (1,242 with no symbol), 867,890
security-days, 119,078 alone (7.63 percent). 183,461 (11.76 percent) need both. All upper bounds. The Bloomberg document says plainly
that `integrations/bloomberg/READ_HERE.md` neither forbids nor establishes historical closes for fixed income by CUSIP back to 2013, and
is written as "find out whether it is served, then pull"; at 120,000 points a day the leg is at least 8 days. 210 Yahoo securities
share one of 103 symbols with another CUSIP. The blank-for-price denominator (1,559,722 of 1,669,040 account-days in the holdings
table) was not reconciled to the returns table's own NOT_MEASURABLE count.

## Carried and next

- **Carried item 4 is done:** the method row read back after IRPT_DASHBD's rewrite, row D2-S112 @74144c06ec.
- **Round 66, on the CTO's msg 4734:** the r28-versus-r29 comparison over all 3,325 days (measured under both with a different return;
  measured under one only; unchanged), and the repair of the scan. No re-mint order is cut before the comparison is read.
- **The default leg** moves by the CTO's addendum, after the comparison.
- **Neither request is sent.** `0.0.0_AB_MSTR~DELL2` carries each on the CTO's read of the two documents.

**Round-close check:** REFUSED until the two judgment criteria are graded.
