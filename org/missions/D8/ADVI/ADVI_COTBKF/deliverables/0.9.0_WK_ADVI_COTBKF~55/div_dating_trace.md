# Dividend-dating trace of the 4 regressed months (CB-ac-2)

Read-only. Rule: see the module docstring of commonwealth_div_dating_trace.py (committed before this run). Ex-date sources: (1) EXDATES_ADVI_COTBKF_20261009.csv (39 rows, 0 refused for ex after pay); (2) dell1's price store s3://opal-data-assets/yahoo/global/silver/price_history/ (32 CUSIP partitions listed). G = 26 days (largest pay - ex gap in source 1).

## B3S728504 2023-05

- reported 0.10; r26 computed 0.141810 (MATCH); r28 computed 0.181286 (DIFF); regression_pp (r28 - r26) = 0.039475

| CUSIP | pay date | ex-date | ex source | amount | candidate | r26 value pay day | r28 value pay day | r28/r26 |
|---|---|---|---|---|---|---|---|---|
| 808524102 | 2023-03-27 |  | NONE | 75.66 | no | 10837.79 | 26320.47 | 2.4286 |
| 808524839 | 2023-04-10 |  | NONE | 17.30 | no | 11035.27 | 26946.55 | 2.4419 |
| 808524839 | 2023-05-05 |  | NONE | 15.32 | yes | 11085.71 | 27063.87 | 2.4413 |
| 808524839 | 2023-06-07 |  | NONE | 16.71 | yes | 11309.97 | 27749.95 | 2.4536 |
| 808524102 | 2023-06-26 |  | NONE | 79.02 | yes | 11486.75 | 28101.43 | 2.4464 |
| 808524839 | 2023-07-10 |  | NONE | 17.77 | no | 11571.09 | 28454.03 | 2.4591 |

Day values in the month (both methods valued): 22 days; r28/r26 ratio min 2.4365 max 2.4495; first day 2023-05-01 r26 11090.99 r28 27134.81; last day 2023-05-31 r26 11137.50 r28 27248.32.

Candidates (could change month under a lag <= 26 days): 3, sum 111.05; r28 value on the last valued day before the month (2023-04-28) 27199.01; bound_pp = 0.408287.

Ex-dated month: NOT COMPUTED -- no source holds the ex-date of 808524102, 808524839.

**Class: untraced:ex-date no source holds for 808524102,808524839 (checked: EXDATES_ADVI_COTBKF_20261009.csv 39 rows, dell1 store listing 32 CUSIPs, bound_pp 0.408287 >= regression_pp 0.039475)**

## B3S728504 2023-06

- reported 4.81; r26 computed 4.834446 (MATCH); r28 computed 5.239873 (DIFF); regression_pp (r28 - r26) = 0.405427

| CUSIP | pay date | ex-date | ex source | amount | candidate | r26 value pay day | r28 value pay day | r28/r26 |
|---|---|---|---|---|---|---|---|---|
| 808524839 | 2023-05-05 |  | NONE | 15.32 | no | 11085.71 | 27063.87 | 2.4413 |
| 808524839 | 2023-06-07 |  | NONE | 16.71 | yes | 11309.97 | 27749.95 | 2.4536 |
| 808524102 | 2023-06-26 |  | NONE | 79.02 | yes | 11486.75 | 28101.43 | 2.4464 |
| 808524839 | 2023-07-10 |  | NONE | 17.77 | yes | 11571.09 | 28454.03 | 2.4591 |
| 808524839 | 2023-08-07 |  | NONE | 16.48 | no | 11770.86 | 29018.27 | 2.4653 |

Day values in the month (both methods valued): 21 days; r28/r26 ratio min 2.4464 max 2.4641; first day 2023-06-01 r26 11207.79 r28 27451.71; last day 2023-06-30 r26 11675.94 r28 28676.10.

Candidates (could change month under a lag <= 26 days): 3, sum 113.50; r28 value on the last valued day before the month (2023-05-31) 27248.32; bound_pp = 0.416539.

Ex-dated month: NOT COMPUTED -- no source holds the ex-date of 808524102, 808524839.

**Class: untraced:ex-date no source holds for 808524102,808524839 (checked: EXDATES_ADVI_COTBKF_20261009.csv 39 rows, dell1 store listing 32 CUSIPs, bound_pp 0.416539 >= regression_pp 0.405427)**

## B3S728506 2023-05

- reported 0.11; r26 computed 0.149265 (MATCH); r28 computed 0.189425 (DIFF); regression_pp (r28 - r26) = 0.040160

| CUSIP | pay date | ex-date | ex source | amount | candidate | r26 value pay day | r28 value pay day | r28/r26 |
|---|---|---|---|---|---|---|---|---|
| 808524102 | 2023-03-27 |  | NONE | 87.38 | no | 12351.51 | 30124.63 | 2.4389 |
| 808524839 | 2023-04-10 |  | NONE | 19.32 | no | 12578.37 | 30845.47 | 2.4523 |
| 808524839 | 2023-05-05 |  | NONE | 17.11 | yes | 12635.96 | 30980.24 | 2.4518 |
| 808524839 | 2023-06-07 |  | NONE | 18.67 | yes | 12896.16 | 31775.68 | 2.4640 |
| 808524102 | 2023-06-26 |  | NONE | 91.27 | yes | 13099.55 | 32180.03 | 2.4566 |
| 808524839 | 2023-07-10 |  | NONE | 19.84 | no | 13198.19 | 32589.98 | 2.4693 |

Day values in the month (both methods valued): 22 days; r28/r26 ratio min 2.4469 max 2.4599; first day 2023-05-01 r26 12643.57 r28 31064.62; last day 2023-05-31 r26 12696.93 r28 31195.62.

Candidates (could change month under a lag <= 26 days): 3, sum 127.05; r28 value on the last valued day before the month (2023-04-28) 31136.64; bound_pp = 0.408040.

Ex-dated month: NOT COMPUTED -- no source holds the ex-date of 808524102, 808524839.

**Class: untraced:ex-date no source holds for 808524102,808524839 (checked: EXDATES_ADVI_COTBKF_20261009.csv 39 rows, dell1 store listing 32 CUSIPs, bound_pp 0.408040 >= regression_pp 0.040160)**

## B3S728506 2023-06

- reported 4.86; r26 computed 4.894278 (MATCH); r28 computed 5.285287 (DIFF); regression_pp (r28 - r26) = 0.391010

| CUSIP | pay date | ex-date | ex source | amount | candidate | r26 value pay day | r28 value pay day | r28/r26 |
|---|---|---|---|---|---|---|---|---|
| 808524839 | 2023-05-05 |  | NONE | 17.11 | no | 12635.96 | 30980.24 | 2.4518 |
| 808524839 | 2023-06-07 |  | NONE | 18.67 | yes | 12896.16 | 31775.68 | 2.4640 |
| 808524102 | 2023-06-26 |  | NONE | 91.27 | yes | 13099.55 | 32180.03 | 2.4566 |
| 808524839 | 2023-07-10 |  | NONE | 19.84 | yes | 13198.19 | 32589.98 | 2.4693 |
| 808524839 | 2023-08-07 |  | NONE | 18.41 | no | 13428.25 | 33240.98 | 2.4755 |

Day values in the month (both methods valued): 21 days; r28/r26 ratio min 2.4566 max 2.4744; first day 2023-06-01 r26 12777.82 r28 31429.95; last day 2023-06-30 r26 13318.35 r28 32844.40.

Candidates (could change month under a lag <= 26 days): 3, sum 129.78; r28 value on the last valued day before the month (2023-05-31) 31195.62; bound_pp = 0.416020.

Ex-dated month: NOT COMPUTED -- no source holds the ex-date of 808524102, 808524839.

**Class: untraced:ex-date no source holds for 808524102,808524839 (checked: EXDATES_ADVI_COTBKF_20261009.csv 39 rows, dell1 store listing 32 CUSIPs, bound_pp 0.416020 >= regression_pp 0.391010)**

DIV-TRACE months=4 dividend_dating=0 other=0 untraced=4
