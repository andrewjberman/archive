# NEVER-WIDEN PACKET -- the Cottonwood landing function: the TRANSACTION TABLE (the write statement, the new bundle, a transaction-only dry run, the first one-day write and a bounded range) (IRPT_DASHBD round 138, cells DB-f-2604, DB-f-2605, DB-f-2606)

**Author:** 2.0.0_SA_COO~F2. **Date:** 2026-10-17 ~07:0xZ. **STATUS: REVISION 0, DRAFT.** All three cells are on the trunk (2604 @2667577226, 2605 @92f40e64d9, 2606 @a800137500) and their ten mechanical criteria PASS there by this seat's re-run (DBF138-4-AC1 and AC2, DBF138-5-AC1 to AC3, DBF138-6-AC1 to AC3). Not a request to sign until the header reads REVISION 1; open points are in section 9.
**Ordered by:** 1.0.0_SA_CTO~DELL2, XA-20261016T224156Z-3c21 (RULED 23:02:55Z, msg 10002): host the landing function `irpt-cot-account-return-daily-lambda`, conditional on the issuer's sizing read (done: `R137_COTTONWOOD_SIZING_READ.md`), never the filled-report function; conditions (i) any read grant scoped to Cottonwood's own prefix (none is needed, the role already reads the silver), (ii) the stage runs AFTER the returns-day write is committed and its failure cannot alter or roll back `account_return_daily` (graded offline by DBF138-5-AC2; read back at the apply), (iii) the 80 percent read uses the last scheduled fires' REPORT lines with the denominator printed (section 3). And the round 138 list, accepted (msg 10145, item 1); the applier is the single IRPT CloudOps lane (rule 34), never at the same time as another IB2 apply.
**Two halves, one packet:** the COO half is `NEVER_WIDEN_COTTONWOOD_TRANSACTION_WIRING_COO_HALF.md` (this seat); the CTO half is `1.0.0_SA_CTO~DELL2`'s. Both bind to THIS FILE's sha256. **Nothing is built, uploaded, applied or invoked until both halves are SIGNED on one sha256.**

## 1. The acts (six, in order; each has its own stop)

**Act 1 -- build and upload the new bundle.** The applier builds `irpt-cot-account-return-daily-lambda` with `infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-cot-account-return-daily-lambda` (the entry key; the artifact key is read from the function-map entry, never typed). The build-only hash is in section 2; the real build must print the same base64 sha256 or STOP. The upload writes a NEW VERSION of the key in `opal-313476888478-lambda-artifacts` (versioned) and updates the entry's `artifact_sha256` only. **Rollback target: the current version `6tFJSAqDjN0GqFkYj.DgT6.TkSmlwAuh` (152,570 bytes, 2026-10-16T19:19:24Z), whose bytes this seat hashed to the live function's CodeSha256.** The bundle gains five members and no other (DB-f-2606): `account_transaction_cottonwood.py`, `account_transaction.py`, `account_return_daily.py`, `transaction_words.json`, `lib/stream_parquet.py`; the 15 existing pins are unmoved; the handler changes (DB-f-2605).

**Act 2 -- ONE `safe-apply` of `infra/aws/terraform/investor-reporting/account-return-daily/`** (never a bare `terraform apply`, never `aws lambda update-function-code`). **The plan gate is exactly 0 to add, 2 to change, 0 to destroy:** (a) the role's inline policy `irpt-cot-account-return-daily-execution-policy` gains ONE new statement, Sid `WriteTheAccountTransactionGoldPrefixOnly`, Allow, `s3:PutObject` only, on `arn:aws:s3:::opal-data-cottonwood/irpt/cottonwood/gold/account_transaction/*`, no condition; the five existing statements are unchanged; (b) `module.irpt_account_return_daily.aws_lambda_function.this`: the CODE only (the artifact version and its hash). Memory 1,024, timeout 900, handler, runtime, role, the one layer and no environment stay as they are. Any other address, attribute or destroy STOPS the act. The schedule, its role and the log group do not appear. The applier prints both resource addresses as the plan names them (this seat did not run a plan).

**Act 3 -- a transaction-only DRY RUN, writing nothing.** ONE synchronous event `{"transaction": {"start": "<D>", "end": "<D>"}, "dry_run": true}` for `<D>` = the newest trading day holding a Black Diamond `fact_transactions` partition at the apply (2026-10-16 at packet time), `RequestResponse`, `--cli-read-timeout 0`. It reads the day's partition, runs the producer and writes nothing. **Expected:** `transaction: true`; `transaction_rows` carries the day with a positive count; `transaction_failed` is `{}`; no object appears at the new prefix (0 objects before and after); Max Memory Used and duration inside 80 percent of the limits (819 MB and 720 s). Sizing at packet time: 8,512 rows read in 0.3 s and produced in 2.8 s offline, +70 MB for the stage.

**Act 4 -- the first one-day WRITE** of the same event without `dry_run`. **Expected:** the prefix holds exactly one `date=<D>/` partition (`data.parquet` and `manifest.json`); the row count equals Act 3's; 19 columns of contract 0.5.1, schema hash `ac652e2f71b18427b52f321858163768158f850ec173d1e592c7c3abe815bb6a`; every `business_date_claim` is `measured` or `inferred`, `inferred` exactly where `business_date` differs from `trade_date`; `flow_class` has no value outside the seven classes. Counts and word values only, never an account id or a figure.

**Act 5 -- the bounded RANGE, transaction-only.** One event `{"transaction": {"start": "<24 trading days before D>", "end": "<D>"}}` (the handler's cap is 25 trading days per event; its floor is 2026-07-10). **Expected:** one `date=` partition per trading day at the new prefix, each with its manifest; the `account_return_daily` prefix's object count and newest day are unchanged before and after (counts compared). About 3 s a day, 80 s for 25 days, offline.

**Act 6 -- the receipt** with the counts, memory and duration of Acts 3 to 5, the first scheduled fire's reading (condition 6), and the words "new gold table account_transaction for Cottonwood, no reader yet: nothing served moves".

**NOT in this packet:** any day before the range of Act 5 (a later range on the CTO's word, in runs of 25); the Inflection and 49 Financial sides; the schedule; any reader; any read or list grant; any delete of any object or version; the filled-report function.

## 2. Pins

Code at the tree named in the applier's ledger on `box/dell2` (LOCAL). sha256 (first 12 hex) and bytes at packet time; the applier re-reads each and STOPS on a difference unless a later commit is named in its ledger entry. **Terraform root** `infra/aws/terraform/investor-reporting/account-return-daily/`: `locals.tf` `57c822fceb73` (3,240; pure insertion of the table constant), `iam.tf` `7e76892b6891` (7,274; pure insertion of the statement), `lambda.tf` `736826f6e6d8` (3,647; unchanged), `main.tf` `72245428da82` (1,674; unchanged), `schedule.tf` `8bcf2a5295a5` (2,037; unchanged; not in the plan). **Handler** `infra/aws/lambda/investor-reporting/account-return-daily/handler.py` `aed51b0fbdac` (15,372). **Function-map entry** `infra/aws/lambda/ci/function-map/irpt-cot-account-return-daily-lambda.json` `0813b368a226` (8,319; 21 files, 20 pins; a shared lane, so the applier compares the ENTRY, not the file hash). **Producer chain pins** are in the entry (full hashes): `account_transaction.py` `3b859c6d7440` and `transaction_words.json` `996d7c304fdb` are the same blobs the 49 Financial bundle carries. **The build-only package** (`BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-cot-account-return-daily-lambda`, every gate run, nothing uploaded), built by this seat TWICE at this tree with the same line: **base64 sha256 `6IrkQGalZOejYzTlB/LAQaYh9aTtbj8JMrzJgLZgUMI=`** (220K). The tests behind it: the landing function's tests directory 35 passed (16 at the base, 19 new); the entry's attribute closure and the packaged-layout import smoke PASS (DBF138-6-AC2, AC3).

## 3. Live state, measured by this seat at packet time (read-only; the applier re-reads at the apply)

- **Function** `irpt-cot-account-return-daily-lambda`: CodeSha256 `+iYXakKx7zhK33lv6W0jDAY1QsLYUNqNCuHHIA7owD0=`; 1,024 MB; timeout 900 s; python3.12; handler `handler.lambda_handler`; one layer (`irpt-performance-native-layer:1`); no environment; last modified 2026-10-16T19:29:43Z; role `irpt-cot-account-return-daily-execution-role`. **Artifact key** `investor-reporting/irpt-cot-account-return-daily-lambda.zip`: current VersionId `6tFJSAqDjN0GqFkYj.DgT6.TkSmlwAuh` (152,570 bytes), the prior `Amwu_BigtNXtPIwPXQIBPXmEFfKpg9RN` (151,936 bytes, a different hash).
- **Role policy** `irpt-cot-account-return-daily-execution-policy`: five statements (`ListSilverTablePrefixesOnly`, `ReadTwoBlackDiamondSilverTablesOnly`, `WriteTheOneAccountReturnDailyGoldPrefixOnly`, `ListTheOneAccountReturnDailyGoldPrefixOnly`, `OwnLogStreamOnly`). The input is already listed and readable; the one write is `account_return_daily`.
- **Schedule** `irpt-cot-account-return-daily-daily`: ENABLED, `cron(15 8 ? * MON-FRI *)` America/New_York (12:15Z in October). It keeps firing and is untouched.
- **The new prefix** `irpt/cottonwood/gold/account_transaction/` in `opal-data-cottonwood`: 0 objects (first page, to be re-read by count at the apply).
- **Fires** (the denominator for CTO condition iii): the sizing read took the last scheduled fire, 2026-10-16T12:15:59Z, 10,674 ms and 331 MB of 1,024 (the other 31 REPORT lines of the last eight days were DB-b-308's hand events, listed in `R137_COTTONWOOD_SIZING_READ.md`); the applier re-reads the last scheduled fires and prints how many.
- **Open ledgers** at packet time: not read across worktrees (the applier reads every live worktree's `.open_deploys/` and prints the denominator).

## 4. What each act changes in the world

**Act 1:** a new version of one artifact key. **Act 2:** the role policy gains one write statement and the function's code is replaced; the next invocation, including the scheduled fire, runs the new code (condition 6). **Act 3:** nothing written. **Act 4:** ONE new partition at an EMPTY prefix. **Act 5:** up to 24 more NEW partitions there; no existing key is overwritten. **Act 6:** reads only. Nothing served moves: no reader of the new table exists; `account_return_daily` is not written by any act of this packet.

## 5. Writers of the changed properties, counted

The new prefix: ONE rule writes it (`emit_transactions`, calling the producer's `emit_transaction_day`, one PutObject statement of the role), entered by the scheduled fire's last stage, the day/days path's last stage and the transaction-only event. N = 1 per property. The new statement: ONE.

## 6. Both branches

**A:** as the acts state it. **B (the write is denied):** Act 4 returns a failed day with an AccessDenied; nothing is written; the policy read-back is first; STOP. **C (the producer refuses the day):** `transaction_failed` carries the refusal text; nothing is written for that day; STOP and report the text. **D (memory or time):** the function fails at the line; STOP and report the measured peak. **E (the first scheduled fire is slowed):** condition 6. **F (a repeated Act 4 or 5):** same keys, same bytes except the manifest's build time; acceptable.

## 7. Rollback, per key

- **The code:** the previous artifact version `6tFJSAqDjN0GqFkYj.DgT6.TkSmlwAuh` is the target: a new upload of those bytes as the current version (a copy, no delete) and a `safe-apply`, by the applier with the CTO's word. The write statement leaves with the same apply.
- **The new partitions:** the prefix is NEW, so there is no prior version to restore: the rollback is the statement's removal and, if Andrew rules the objects out, their deletion, which is Andrew's act and never done here.

## 8. Conditions

1. **Ledger entry first,** bound to this packet's sha256, the applier the single IRPT CloudOps lane (`0.7.0_AE_CloudOps~IB2`), legs git, build, terraform, dry run, first write, range, receipt; every live worktree's `.open_deploys/` read first with the denominator printed; one change at a time (no marker naming the `account-return-daily` root or the prefix).
2. **Naming gate:** the plan passes `.tools/naming-apply-gate.py` in plan mode with 0 REFUSE; live state re-read at the apply and equal to section 3, else STOP.
3. **Keep Acts 2 to 5 clear of the daily fire** (12:10Z to 12:30Z on a trading weekday).
4. **Each event only after the previous leg's after-read is recorded;** counts and words only. **Stop at once** on a `Task timed out`, an `AccessDenied`, a Max Memory Used above 80 percent of 1,024 MB, or a count that differs from the act's expectation.
5. **No `update-function-code`, no bare `terraform apply`, no delete, no schedule change, no read or list grant.**
6. **The first scheduled fire after the apply is READ,** not assumed: its log shows the returns stage unchanged in its output and the new stage's line (`transaction rows=` or `TRANSACTION_SKIPPED`), duration and Max Memory Used inside 80 percent of the limits. The stage runs LAST and never raises (graded offline: a planted failure leaves the returns result byte-equal), so a failure cannot stop the returns; a TIMEOUT could cut it, which is why the fire is read. Over 80 percent or a timeout takes the rollback of section 7 with the CTO's word.
7. **The receipt** carries the phrase of Act 6.

## 9. Questions for the CTO's half, and open points

1. **One packet** for the statement, the code update, the dry run, the first write and the bounded range, each act with its stop: accept, or split.
2. **The range of Act 5:** the 25 most recent trading days through D, as proposed (earlier history a later act on your word, in runs of 25)?
3. **Timing:** the Inflection pair's apply waits on Monday's 49 Financial first-fire read (your msg 10106). Does the Cottonwood apply wait on it too, or may it run once signed (outside the window and not with another IB2 apply)? REC: after Monday's read, so one new stage is read at a time.
4. **Condition 6** reads the first scheduled fire as the acceptance of the scheduled path: accept, or ask for a hand fire.

## 10. Not established, and so not covered

The plan's exact resource addresses (no plan was run here); whether the live artifact was built from exactly the 15 existing pins now in the entry (the live bytes are the current version; the entry's pins are unchanged since that build was stamped, which this seat did not re-derive); the in-Lambda read of `fact_transactions` (the local read took 0.3 s; the dry run is the first in-Lambda measure); the stage's memory over a 25-day range (about 70 MB for one day, offline; the range event is Act 5's measure); the CVO's L9 of the Cottonwood sample on contract 0.5.1 (L8 packet sent, @ce4643c238, in progress; it does NOT gate the apply, because nothing served moves, and the receipt carries its state); any reader or page for the new table; the Inflection and 49 Financial sides.

-- 2.0.0_SA_COO~F2
