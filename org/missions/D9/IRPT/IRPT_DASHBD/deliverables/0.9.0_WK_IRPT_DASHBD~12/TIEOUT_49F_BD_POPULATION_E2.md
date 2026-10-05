# E2 tie-out, 49 Financial served total return vs Black Diamond -- counts only

**Cell:** IRPT_DASHBD.TO-DB-b-26 (round 17, outcome FWD-8) | **Worker:** 0.9.0_WK_IRPT_DASHBD~12 | **Vendor calls:** 0
**Record:** `TIEOUT_49F_BD_POPULATION_E2.json` (per-segment rows) | **Script:** `tieout_e2.py` | **Tolerance:** 0.35 pp

## Inputs

| input | value |
|---|---|
| plan | `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~6/BD_POPULATION_PLAN_E3.json` (5,252 accounts, 9,082 segments) |
| Black Diamond side | `s3://opal-data-assets/blackdiamond/49financial/bronze/reporting_performance/pull=20261004/`, 5,252 of 5,252 objects read |
| served series | `s3://opal-data-49financial/irpt/49financial/gold/account_return_daily/date=<day>/data.parquet`, 563 partitions, 6,869 accounts, column `total_return_daily`, linked geometrically over each segment's days |

The re-linked served return equals the plan's own `opal_twr` on 9,082 of 9,082 segments.

## Counts

| | segments |
|---|---|
| planned | 9,082 |
| graded | 9,078 |
| not gradable | 4 (all BD_NO_VALUE: BD returned no time-weighted return, `daysHeld 0`) |
| within 0.35 pp | 2,103 |
| outside 0.35 pp | 6,975 |

| outside, by reason | segments |
|---|---|
| FLOW_TIMING | 150 |
| MISSING_PRICE | 2 |
| INCOME_DATE | 568 |
| COVERAGE_DAYS | 5 |
| UNEXPLAINED | 6,250 |

Reasons are assigned only on named evidence (the row's `evidence`): COVERAGE_DAYS on a day-count difference of 2 or more; MISSING_PRICE on served days flagged `holdings_price_return_reason`; FLOW_TIMING when a re-link under the START or MID flow convention lands within tolerance; INCOME_DATE when the link with income removed lands within tolerance. FLOW_TIMING and INCOME_DATE are necessary-not-sufficient readings.

## What the counts say

- Day coverage does not dominate, unlike round 1. BD `daysHeld` equals Opal's linked days on 5,678 segments, is exactly 1 more on 3,395 (all 3,395 contain 2025-01-09, a market closure BD counts), and differs by 2 or more on 5.
- 4,905 of the 6,250 UNEXPLAINED segments land within 0.35 pp once BD's own reported fees are netted from Opal's link (BD's request is NetOfFees; the served series carries no fee). Fees are not in the closed reason set, so they remain UNEXPLAINED with an OBSERVATION BD_FEES clause. 1,345 UNEXPLAINED segments are not accounted for by that observation.
- Surprise row `IRPT_DASHBD-W12-S1`.
