# RELEASE_LOCAL_RUN -- IRPT_DASHBD.TO-DB-b-34 (counts only)

Local runs only: S3 reads, DynamoDB `GetItem` on `etf-classifications`, nothing written to S3. The record is `RELEASE_LOCAL_RUN.json`
(built by `build_release_record.py`); the 61-account re-run is `class_share_61_driver.py`.

## A. The extended handler against the unextended one (`handler.py --local`, 2026-10-05, the round-21 sample's first 20 accounts)

The unextended side is the BASE handler AND the BASE source declaration: `git show 954983d543:infra/aws/lambda/investor-reporting/reporting-gold/handler.py`
and `git show 954983d543:data/assets/scripts/gold/irpt_reporting/sources.json` (amendment 1 @e765698322: the before side used the base
declaration, not the declaration at this branch, so the equality below also covers the trade-leg tokens moved into `sources.json`). The
base declaration was written to the working path only for the duration of that one run and restored byte-for-byte after (its sha256
matched `git show 954983d543:` at the time of the run). The extended side used the handler and the declaration at this branch. Both ran
the same day over the same 20 accounts; the sha256 values below are the re-run's and equal the first run's.

| Quantity | Count |
|---|---|
| accounts requested | 20 |
| `account_return_daily` rows, unextended handler | 19 |
| `account_return_daily` rows, extended handler | 19 |
| sha256 of the returns parquet, unextended | `11453fc79610d5830f58f77cc835ea1127e2533f67ae0fb985de729c677ae2e1` |
| sha256 of the returns parquet, extended | `11453fc79610d5830f58f77cc835ea1127e2533f67ae0fb985de729c677ae2e1` |
| returns table byte-identical (DELTA) | 0 bytes |
| `account_class_daily` account-days emitted | 19 |
| MEASURED account-days (classes sum to the account) | 18 |
| `CLASS_VALUES_DO_NOT_SUM_TO_ACCOUNT` account-days | 1 |
| class rows | 76 |
| class rows: cash / fixed_income / equity / structured / unclassified | 19 / 19 / 19 / 17 / 2 |
| largest gap between the class sum and the account return, 18 measured account-days | 1.56e-16 (limit 1e-9) |
| unclassified share of value | 0.0720 percent (the denominator is the summed class market value of the 19 account-days and 76 class rows; the dollar figure is in the JSON) |

## B. The round-21 sample's 61 accounts, 2026-09-29 .. 2026-10-05, classes from the table and from the module on the same positions

The same positions, cash lines and trade legs were classified twice: once through the `etf-classifications` table (one `GetItem` per
distinct identifier) and once through the old module dictionary. The module pass reproduces round 21's record exactly (992 class rows,
30 of them `unclassified`), so the two columns differ only by the class source.

| Quantity | Module (round 21) | Table (this cell) |
|---|---|---|
| distinct holdings | 78 | 78 |
| holdings with a class among the six | 33 | 69 |
| holdings not in the source (`unclassified`) | 45 | 9 |
| table values outside the six | n/a | 0 |
| cash positions | 0 | 0 |
| `GetItem` reads | n/a | 78 (one per distinct identifier) |
| class rows | 992 | 982 |
| class rows `unclassified` | 30 | 20 |
| MEASURED account-days | 254 | 254 |
| largest identity gap over the measured account-days | 2.12e-16 | 2.12e-16 |
| unclassified share of value on 2026-10-05, 61 accounts | 1.804 percent | 0.153 percent |

The recorded "about 16 percent" (row IRPT_DASHBD-W18-S2) is the share across every account on `dim_position` 2026-10-01 under the
module. On this 61-account sample the same module gives 1.804 percent on 2026-10-05, so the sample understates the module's all-account
share by a factor of about nine; the table's all-account share is not measured by this cell and is the after-read's job (criterion 3).
