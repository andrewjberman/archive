# RIGHT_GAP_E2 -- the shape of the right-half gap for the E2 set (counts and statistics only)

Measured by 0.9.0_WK_IRPT_DASHBD~30 for TO-DB-b-51. Zero vendor calls; S3 reads of the served gold only.

- E2 population: 1528 accounts (right.tied false, recompose.within true). Control population: 2220 left-half ties.
- Signed gap (pp), right half: median 0.567, p10 0.374, p90 0.764; share positive 0.947.
- Length scaling: Pearson corr of gap with right-half calendar days = -0.145 (n 1528; median 630 days).

| component | corr with gap | n |
|---|---|---|
| external_flow | -0.009 | 1528 |
| income_received | -0.009 | 1528 |
| market_value_eod | -0.009 | 1528 |
| day_quality | -0.014 | 1528 |
| carried_days | -0.144 | 1528 |
| fee_amount | undefined (constant across the population (zero variance)) | 1528 |

- Top driver: carried_days (corr -0.144).
- Control (carried_days over the 2220 left-half ties, n with statistic 2220): corr -0.042; rule |control| < |top|/2; signature_absent = True.
- day_quality values seen in the series for these accounts: {"FLOW_UNRECONCILED": 1184, "LARGE_FLOW": 19086, "MEASURED": 1216546, "NOT_MEASURABLE": 10203}; clean = MEASURED.
- Statistic definitions are in RIGHT_GAP_E2.json `statistic`.
