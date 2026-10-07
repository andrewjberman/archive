# CLASS_DAILY_LOCAL_RUN -- IRPT_DASHBD.TO-DB-b-33 (counts only)

Local run of `account_class_daily.py` (method_version 1). S3 reads only; nothing written to S3. Record: `CLASS_DAILY_LOCAL_RUN.json`.

| Quantity | Count |
|---|---|
| trading days | 5 (2026-09-29 .. 2026-10-05) |
| accounts in the sample | 61 (the C-NAMES example plus 60 drawn, seeded, from a population of 7597) |
| sampled accounts the producer emits rows for | 52 (the other 9 carry a zero custodian value on 2026-10-01 and no producer row) |
| account-days with class rows | 260 |
| MEASURED account-days (classes sum to the account) | 254 |
| not measurable: ACCOUNT_RETURN_NOT_MEASURABLE | 1 |
| not measurable: CLASS_VALUES_DO_NOT_SUM_TO_ACCOUNT | 5 |
| class rows | 992 |
| class rows: cash | 257 |
| class rows: fixed_income | 240 |
| class rows: equity | 240 |
| class rows: structured | 220 |
| class rows: alternatives | 0 |
| class rows: commodities | 5 |
| class rows: unclassified | 30 |
| distinct holdings seen | 78 |
| holdings named by the module | 33 |
| holdings `unclassified` (not named by the module) | 45 |
| holdings that are cash positions | 0 |
| trade legs (TR) in the window for the sampled accounts | 220 |
| in-kind legs (IC) in the window for the sampled accounts | 0 (the in-kind path is exercised offline only) |

Largest gap between the class sum and the producer's own daily return over the 254 measured account-days: 2.116e-16 (criterion limit 1e-9).
