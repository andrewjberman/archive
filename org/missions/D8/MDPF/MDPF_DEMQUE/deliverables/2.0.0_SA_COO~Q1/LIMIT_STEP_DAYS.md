# Limit step days: one change per drawer or production day (kept by 2.0.0_SA_COO~Q1)

**Why this file exists.** Andrew-direct 2026-10-15: "increase limits on all our pull surfaces." Three seats each move one limit in steps: this seat's history ceiling ramp (`ledger/CTO_RULING_HISTORY_CEILING_RAMP_20261015.md`), `2.0.0_SA_COO~R1`'s A4 price-axis window (`org/missions/D5/AMGT/AMGT_RESAPP/ledger/NEVER_WIDEN_ROUND107_A4_WINDOW_STEP1_CTO_HALF.md`), and `2.0.0_SA_COO~H1`'s A2 `BACKFILL_CAP` (50 to 62). **The rule (CTO msg 6304): two steps never land on the same day, and a ramp step does not land the day after another seat's step**, so each change is read alone on the budget ledger.

**How to use it.** Each seat appends ONE row when its commit lands, naming the day it takes effect and its commit. Nobody edits another seat's row. A day is the calendar date of the fire the step first applies to (ET).

| step | seat | what moves | takes effect (ET) | commit | status |
|---|---|---|---|---|---|
| A4 price axis, step 0 to 1 (30 to 90 days) | `2.0.0_SA_COO~R1` | PX_LAST reach, about +4,250 observations a day | first trading day two or more trading days after A2's reported day, and after site Z's day-0 read (day 0 is Fri Oct 16, about 9:00 AM ET; the next trading-day fire is Mon Oct 19). A2 on Mon Oct 19 gives A4 Wed Oct 21; A2 on Tue Oct 20 gives A4 Thu Oct 22. R1 appends the day in the message that says the commit landed | | pending (R1 holds Oct 19 until H1 reports A2's day) |
| A2 `BACKFILL_CAP` 50 to 62 | `2.0.0_SA_COO~H1` | tickers a run asked for history backfill | **Fri Oct 16, 7:00 AM ET pull** (MEASURED: site Z's manager read its working tree 2026-10-16 00:36:34Z, `etf_daily_pull.py` blob 9e02396c98, clean against HEAD, line 62 = 62; H1 msg 6369). H1 reads Friday's manifest and reports if the run did not carry 62. COO~R1's A4 step 1 is therefore Tue Oct 20 at the earliest | `8f56c423dd` | taking effect Fri Oct 16 |
| History ceiling ramp, step 1 (11,716 cells) | `2.0.0_SA_COO~Q1` | the drawer's daily room | earliest Sat 2026-10-24: the ramp cell is cut at the round-10 issuance after `TO-DQ-t34` is terminal | | not started |
| History ceiling ramp, step 2 (23,432) | `2.0.0_SA_COO~Q1` | the drawer's daily room | one completed day after step 1 | | not started |
| History ceiling ramp, step 3 (29,290) | `2.0.0_SA_COO~Q1` | the drawer's daily room | one completed day after step 2 | | not started |

Measured fact for the order of these: the drawer task fires at 10:00 AM ET (14:00Z) every day, but until trading-day draws are built it stops on a trading day, so ramp steps can land only on non-trading days (Oct 24, 25, 31, Nov 1, 7, 8). A4 and A2 act on trading days. Once trading-day draws exist, the rule above is what keeps them apart.
