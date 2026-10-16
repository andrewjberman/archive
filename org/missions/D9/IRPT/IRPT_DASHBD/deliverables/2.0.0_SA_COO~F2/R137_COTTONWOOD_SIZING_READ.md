# The Cottonwood sizing read for the transaction stage: the landing function `irpt-cot-account-return-daily-lambda` (read by 2.0.0_SA_COO~F2, 2026-10-16 ~22:5xZ)

Read-only (live GETs, the function's log group, and the producer run OFFLINE on one real day with nothing written). It answers the CTO's three questions of msg 9962 (call 6c9a, submission `XADJ_6C9A_COTTONWOOD_TRANSACTION_HOST_SUBMISSION_20261016.md` @7b7c3a6664; cells wait on XA-20261016T224156Z-3c21). Counts and timings only; no figure, no account id.

## (a) Does the landing function's role read the Black Diamond transaction silver? YES: no new read grant

The role `irpt-cot-account-return-daily-execution-role`, one inline policy `irpt-cot-account-return-daily-execution-policy`, five statements (read from the live policy):

| statement | effect | what it grants |
|---|---|---|
| `ListSilverTablePrefixesOnly` | Allow | `s3:ListBucket` on `opal-data-assets`, `s3:prefix` like `blackdiamond/cottonwood/silver/fact_allocations/*` and `.../fact_transactions/*` |
| `ReadTwoBlackDiamondSilverTablesOnly` | Allow | `s3:GetObject` on `opal-data-assets/blackdiamond/cottonwood/silver/fact_transactions/*` and `.../fact_allocations/*` |
| `WriteTheOneAccountReturnDailyGoldPrefixOnly` | Allow | `s3:PutObject` on `opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/*` |
| `ListTheOneAccountReturnDailyGoldPrefixOnly` | Allow | `s3:ListBucket` on `opal-data-cottonwood`, `s3:prefix` like `irpt/cottonwood/gold/account_return_daily/*` |
| `OwnLogStreamOnly` | Allow | `logs:PutLogEvents`, `logs:CreateLogStream` on its own log group |

So the transaction stage's INPUT (the day's `fact_transactions` partition) is already listed and readable. The adapter the function runs (`cottonwood_bd_account_return_daily.py`) reads exactly these two tables, which confirms the earlier inference. **The one grant the stage needs is a WRITE:** `s3:PutObject` on `arn:aws:s3:::opal-data-cottonwood/irpt/cottonwood/gold/account_transaction/*` (the address is `opal_naming.address("irpt", "cottonwood", "gold", "account_transaction", ...)` output). No list grant on the new prefix is needed (the writer only puts). **A choice for the cell, the CTO's if he wants it:** the existing write statement is NAMED `WriteTheOneAccountReturnDailyGoldPrefixOnly`; adding a second resource to a statement whose sid says "One" is a misnomer, and a renamed sid reads as new to the issuer's checker. REC: a NEW statement `WriteTheAccountTransactionGoldPrefixOnly` with that one resource (the plan would be expected to read 0 add / 2 change / 0 destroy as for 49 Financial, the policy being one inline policy whose document changes plus the function's code; the root was not read here).

## (b) Memory and duration of the last scheduled fires (REPORT lines)

The function: 1,024 MB, timeout 900 s, ephemeral 512 MB, the one native layer, no environment. Schedule `irpt-cot-account-return-daily-daily` ENABLED, `cron(15 8 ? * MON-FRI *)` America/New_York (12:15Z in October). Last SCHEDULED fire read: **2026-10-16T12:15:59Z, duration 10,674 ms, Max Memory Used 331 MB of 1,024.** The other REPORT lines of the last eight days (31) are DB-b-308's hand events (a rewrite and backfill run on the 16th from 19:47Z): the first of them (19:47Z) shows a 900,000 ms duration, the limit, consistent with the DB-b-308 STOP at Act 3 that IB2 recorded (I read the REPORT line, not that record's text), then rewrites of 65 to 493 s with Max Memory Used 639 to 642 MB. A scheduled fire is one owed day (about 11 s); a long-history rewrite is a different event.

## (c) The producer offline on one real day

`account_transaction_cottonwood.normalize_trn` on the newest silver partition (`date=2026-10-16`; 126 partitions exist; the partitions are DAILY slices, not snapshots: sampled days hold 8,512 to 14,138 rows, the earliest in March holds 0): **8,512 rows read in 0.3 s (one object), 8,512 rows out in 2.8 s, the process resident memory 199 MB (129 MB before the read, so +70 MB for the stage)**; no row refused. At that rate a 25-day range is about 25 times 3.1 s, roughly 80 s.

## What this says about the three hosts

- **Option 1 (the landing function): fits.** Read grant none; write grant one; memory 331 MB used by the scheduled fire plus about 70 MB for the stage against 1,024 MB; time 11 s plus about 3 s against 900 s. The margin is two orders of magnitude, unlike the 49 Financial function (whose filled stage alone runs to several minutes). The stage would be the LAST stage of the fire, as in the 49 Financial handler.
- **Option 2 (the filled-report function): not recommended** (the CTO's own ruling), and this read adds a reason: it does not hold the transaction input (its role was not read for it).
- **Option 3 (a new function): not needed** on this evidence.

## Not established

The landing function's Terraform root (`account-return-daily`) was not read for how its policy document is built (the statement choice above); the real function's handler was not run; the cold-start and the `fact_transactions` read inside Lambda (network) are not measured here (the local read took 0.3 s). The sizing is one day and the day-range arithmetic; the apply's own dry run would be the first in-Lambda measure.

-- 2.0.0_SA_COO~F2
