# The late-receipt rule, out of sample (round 70, TO-CB-br-4)

Worker 0.9.0_WK_ADVI_COTBKF~114. A measurement; no code changed; no recommendation is made. The record is `RESIDUAL_RECEIPT_OUT_OF_SAMPLE.json`. No account id, amount, quantity or per-account return appears in either file.

## 1. Reproduced (served table, rule as recorded in round 69)

410 of 107,311 measured days blanked; 148 of 162 target days; 0 of the other 17.

## 2. Hold-out by account

Split fixed before any outcome: half A = accounts whose sha256 (UTF-8 of the account id string) hex digest ends in an even digit, half B = odd. No account is in both.

| Half | Accounts (with a measured day) | Measured rows | Target days | Other outlier days |
|---|---|---|---|---|
| A | 744 (520) | 58,183 | 85 | 13 |
| B | 789 (534) | 49,128 | 77 | 4 |

Selection rules, written before any result was read (in the JSON): look-back = smallest grid point (14, 21, 24, 28, 30, 60, 90, 180) whose fitting-half target count equals the maximum, "singled out" only if the previous grid point is 2 or more target days lower; share = the lower end of the last step (0.999, 0.995, 0.99, 0.95, 0.90, 0.80) whose added days are more than half targets, "singled out" only if the step into it yields 0.60 or more and the next step 0.40 or less.

Half A, target days blanked (total blanked) at share 0.99 by look-back: 14 days 67 (168); 21 days 74 (192); 24 days 76 (198); 28 days 76 (202); 30 days 76 (203); 60 days 76 (211); 90 days 76 (216, 1 other outlier); 180 days 76 (228, 1 other outlier). At 24 days by share: 0.999 37 (128); 0.995 67 (181); 0.99 76 (198); 0.95 80 (219); 0.90 81 (226); 0.80 81 (239). Step yields: 0.57, 0.53, 0.19, 0.14, 0.00. **Chosen: 24 days (singled out), share 0.99 (not singled out: range 0.995 to 0.99).**

Half B, same tables: 14 days 61 (168); 21 days 71 (192); 24 days 72 (201); 28 days 72 (208); 30 days 72 (211); 60 days 72 (220); 90 days 72 (229); 180 days 72 (246). At 24 days by share: 0.999 40 (126); 0.995 69 (194); 0.99 72 (201); 0.95 74 (221); 0.90 76 (232); 0.80 76 (245). Step yields: 0.43, 0.43, 0.10, 0.18, 0.00. **Chosen: 24 days (not singled out: 21 gives 71; range 21 to 180), share 0.999 (no step is mostly targets; not singled out: range 0.999 to 0.995).**

Neither half chose 28 days and 0.99 together; the halves chose the same look-back and different shares (the ranges meet at 0.995).

| Fit on | Tested on | Target days blanked | Other outlier days blanked | Total blanked |
|---|---|---|---|---|
| A (24, 0.99) | B | 72 of 77 (missed 5) | 0 of 4 | 201 of 49,128 |
| B (24, 0.999) | A | 37 of 85 (missed 48) | 0 of 13 | 128 of 58,183 |
| in sample, 28 and 0.99 | A | 76 of 85 | 0 of 13 | 202 |
| in sample, 28 and 0.99 | B | 72 of 77 | 0 of 4 | 208 |
| in sample, 28 and 0.99 | all | 148 of 162 | 0 of 17 | 410 |

At the range end 0.995 (24 days) half B's choice would blank 67 of 85 targets on A (181 total); half A's range end would blank 69 of 77 on B (194 total). The abs(return) by prior-value tables for the test halves are in the JSON.

## 3. On method_r29 flows

Build used: method_r29 at the served pin WITH the served hold list (`.scratch/w107/fwd3_hold_method_r29`); control `fwd3_hold_method_r28`. The r28 hold build gives 410 and the same 410 days as the served table (988 held-row flows differ from the served table; value and return are identical). Under r29 flows: 411 blanked. Only under r28: 0 days. Only under r29: 1 day (2020-11-30). The flow differs on 47 account-days between r28 and r29, 44 of them in the outflow term the rule reads; of the 44, 1 sits inside any measured receipt day's 28-day window, and it belongs to the one day that changes. At half A's constants (24, 0.99) and its range end (24, 0.995) the same day flips (399 to 400; 375 to 376); at half B's (24, 0.999) nothing changes (254 both). The two measured days whose return changes (2014-12-03, 2020-11-13) carry no receipt row and are blanked under neither method.

## 4. The 410 by class of receipt

| Class | Days | Days with abs return 0.10 or less | Account-months losing a measured day | Losing every measured day |
|---|---|---|---|---|
| dividend (dv, dvlt, dvst, DVX) | 163 | 29 | 106 | 3 |
| interest (int, INTX) | 2 | 2 | 2 | 0 |
| reinvested distribution (dvr, DVRX) | 19 | 19 | 19 | 0 |
| other income (roy, ileu, ac) | 0 | 0 | 0 | 0 |
| fee refund (positive man) | 108 | 1 | 108 | 0 |
| 12b1 credit | 2 | 0 | 2 | 0 |
| more than one class | 116 | 49 | 113 | 9 |
| **All** | **410** | **100** | **299 distinct** | **10 distinct** |

An account-month counts in every class in which it loses a day (rows sum to 350 and 12). The 116 "more than one class" days are 70 dividend with interest and reinvested (the cancels), 43 interest with reinvested, 1 dividend with interest, 1 dividend with other income, 1 dividend with a fee refund.

The 10 account-months that lose every measured day: 8 had a single measured day (7 "more than one class", 1 dividend); the other two had 3 and 4 measured days, each with dividend days and "more than one class" days.

## 5. What a blank costs (chain breaks)

Blank day = a table row with null return, any reason. Account-months with all rows measured today that would gain a blank under the rule: **63**; account-years: **17**. Already with a measured day and a blank day today: 2,015 account-months, 1,568 account-years. Not counting a FIRST_DAY row as a blank: 68 and 22 added; 1,727 and 1,467 already.

## Not established

See `not_established` in the JSON (10 lines): one partition only and the same period in both halves; the round-68 classing taken as given; constants depend on the stated selection rules; receipt flag not re-derived; one r29 build; 47 against 44 flow-changed days; no return recomputed; the quiet days not judged.
