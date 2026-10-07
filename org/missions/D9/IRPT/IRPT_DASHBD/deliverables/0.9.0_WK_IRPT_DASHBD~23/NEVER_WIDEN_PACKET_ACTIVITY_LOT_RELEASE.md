# Never-widen sign-off packet -- the reporting-gold function also writes `account_activity_daily`, `account_lot_realized` and `account_lot_unrealized_daily`, and carries the unapplied `account_class_daily` release (IRPT_DASHBD DB-b-41; round-25 analysis E1)

Author `0.9.0_WK_IRPT_DASHBD~23` for `2.0.0_SA_COO~D2`, 2026-10-07. Cell: `DB-b-41`. Halves owed: `1.0.0_SA_CTO` and `2.0.0_SA_COO~D2`.
Status: PREPARED AND PROVEN LOCALLY; NOTHING APPLIED. No `terraform` command, no `aws lambda` call and no S3 write was made by this
cell. The apply and the first fire are the issuer's act under the two signed halves. This packet covers the WHOLE next apply of the
root: the `account_class_daily` release already in the handler and the role (round 22, cell DB-b-34) AND the three tables below.
Branch `wk-IRPT_DASHBD-23`, build commit `efeb21df71` (the sha256 values below are `git show efeb21df71:<path>`).

## Root

`infra/aws/terraform/investor-reporting/reporting-gold` -- state `s3://opal-313476888478-terraform-state/investor-reporting/reporting-gold/tfstate`.
No other root is read for a write, planned or applied by this act.

## Preconditions the signed act does not cover

1. **PRECONDITION OF THE APPLY -- the bundle pins (the deploying lane's act, rule 13; a pin names the commit that carries the files
   on CLOUD, which does not exist until this branch drains; `lambda-source-map.json` is outside this cell's grant, as in the round-22
   packet).** The bundle is pinned in `infra/aws/lambda/ci/lambda-source-map.json`, entry `irpt-49f-reporting-gold-lambda`. Before the
   apply, the lane sets these `staged_from` entries (and the matching `files` members), each `{repo_path, pin, packaged_as, sha256}`,
   `pin` = the drain commit that carries the file on CLOUD, `sha256` = `git show <drain-commit>:<repo_path> | sha256sum`:

   | # | `repo_path` | `packaged_as` | note |
   |---|---|---|---|
   | 0 | `data/assets/scripts/gold/irpt_reporting/account_return_daily.py` | same path | the existing entry RE-PINNED (row IRPT_DASHBD-W23-S6): today `bc50d5711e`, sha256 `cb38fe16...4529`; HEAD's file differs by 4 lines (`ba544b6064`, DB-b-40) |
   | 1 | `data/assets/scripts/gold/irpt_reporting/account_class_daily.py` | same path | new member (round 22) |
   | 2 | `infra/aws/lambda/v2_portal/_shared/etf_classifications_dynamodb.py` | `etf_classifications_dynamodb.py` | new member, the class client, packaged flat (round 22) |
   | 3 | `data/assets/scripts/gold/irpt_reporting/sources.json` | same path | the existing entry RE-PINNED: the declaration changed twice (the trade-leg tokens, round 22; the `lot_source` object, this cell); today's entry pins `bc50d5711e` |
   | 4 | `data/assets/scripts/gold/irpt_reporting/account_activity_lots.py` | same path | new member (this cell) |

   Pins 1 to 4 land together: the activity producer reads the lot tables' names from the declaration, so a re-pinned `sources.json`
   without pin 4 is harmless (the handler's import is guarded) and pin 4 without pin 3 is NOT a supported pairing (the producer refuses
   by name: `REFUSED: the source declaration carries no 'lot_source' object`, and the lots day is logged `LOTS_SKIPPED`). The lane then
   rebuilds `investor-reporting/irpt-reporting-gold-lambda.zip`. The values (drain commit, sha256 values) are printed by the lane at the
   apply, not predicted here. Without the pins the function runs as it does today (Branch B).
2. **The plan.** `terraform` is not on this box, so no plan was read (row IRPT_DASHBD-W23-S5); the counts below are derived from the
   diff. The issuer reads the plan before the signed halves are used and STOPS if it differs from the expected counts.
3. **Sizing is unmeasured at population scale (row IRPT_DASHBD-W23-S2, ARMED, disarm owner `2.0.0_SA_COO~D2`).** See Unmeasured.

## Names and addresses (builder output, printed)

Printed by `lib/opal_naming.py` at this cell's commit, through the producer's own `builder_output()` for the address lines, with the
firm from the declaration's `registry_key` (`ard.firm_scope`). Nothing below is typed by hand:

```
address('irpt', '49financial', 'gold', 'account_activity_daily', 'date=2026-10-05') = s3://opal-data-49financial/irpt/49financial/gold/account_activity_daily/date=2026-10-05
address('irpt', '49financial', 'gold', 'account_lot_realized', 'date=2026-10-05') = s3://opal-data-49financial/irpt/49financial/gold/account_lot_realized/date=2026-10-05
address('irpt', '49financial', 'gold', 'account_lot_unrealized_daily', 'date=2026-10-05') = s3://opal-data-49financial/irpt/49financial/gold/account_lot_unrealized_daily/date=2026-10-05
address("irpt", <firm>, "gold", "account_return_daily", "date=2026-10-05") = s3://opal-data-49financial/irpt/49financial/gold/account_return_daily/date=2026-10-05
address("irpt", <firm>, "gold", "account_class_daily",  "date=2026-10-05") = s3://opal-data-49financial/irpt/49financial/gold/account_class_daily/date=2026-10-05
name("irpt", <firm>, "reporting-gold", "lambda") = irpt-49f-reporting-gold-lambda
name("irpt", <firm>, "reporting-gold", "role")   = irpt-49f-reporting-gold-role
name("irpt", <firm>, "reporting-gold", "policy") = irpt-49f-reporting-gold-policy
name("irpt", None,   "reporting-gold", "lambda") = irpt-reporting-gold-lambda          (the artifact)
```

The Terraform side mirrors each table name ONCE in `locals.tf` (`irpt_rg_gold_table_class`, `irpt_rg_gold_table_activity`,
`irpt_rg_gold_table_realized`, `irpt_rg_gold_table_unrealized`), each cited to the producer's constant where it lives. The custodian's lot
tables are not typed there either: the silver read prefixes are derived from the declaration's `lot_source` (row IRPT_DASHBD-W23-S1).
Derived sets (emulated in Python from `sources.json` and `scopes.json`, since `terraform` is absent):

```
silver READ prefixes  (bucket opal-data-assets): schwab/08335338/silver/{dim_position,dim_balance,fact_trn,fact_rld,fact_uln,fact_ult}/
gold   READ prefixes  (bucket opal-data-49financial): irpt/49financial/gold/{holdings_performance_daily,account_return_daily,account_class_daily,account_activity_daily,account_lot_realized,account_lot_unrealized_daily}/
gold   WRITE prefixes (bucket opal-data-49financial): irpt/49financial/gold/{account_return_daily,account_class_daily,account_activity_daily,account_lot_realized,account_lot_unrealized_daily}/
```

## The act

ONE targeted `safe-apply` of `infra/aws/terraform/investor-reporting/reporting-gold/`, from a saved plan, with the rebuilt artifact.

Plan (TARGETED; one `-target=` per resource the apply may change; none outside this root):

```
cd infra/aws/terraform/investor-reporting/reporting-gold
terraform plan -out=<planfile> -target=aws_iam_role.irpt_reporting_gold -target=aws_iam_role_policy.irpt_reporting_gold -target=module.irpt_reporting_gold.aws_lambda_function.this
```

Expected: **Plan: 0 to add, 3 to change, 0 to destroy.** Why each:
- `aws_iam_role.irpt_reporting_gold` -- 1 change in place: the `description` text (it names the new tables and the lot-table reads). The trust policy and name do not change.
- `aws_iam_role_policy.irpt_reporting_gold` -- 1 change in place: the policy document (below).
- `module.irpt_reporting_gold.aws_lambda_function.this` -- 1 change in place: `s3_object_version` and `source_code_hash` from the rebuilt artifact. Schedule `cron(41 7 ? * MON-FRI *)` (America/New_York), timeout 900 s, memory 2048 MB and the layer are unchanged.

If the artifact is not rebuilt first the function shows no change and the count is 0 to add, 2 to change, 0 to destroy: STOP, the bundle is not what is signed. Any `add`, any `destroy`, or any resource outside the three: STOP.

The policy document changes as follows (the round-22 class changes and this cell's):
- write set `irpt_rg_gold_write_arns` becomes the returns, class, activity, realized and unrealized prefixes (`s3:PutObject` only);
- the gold read set and its ListBucket prefix pattern become the six gold prefixes;
- the silver read set and its ListBucket prefix pattern gain the three custodian lot-table prefixes `fact_rld`, `fact_uln`, `fact_ult` (`fact_trn` is the transactions prefix it already holds);
- the statement `ReadTheClassTableByKeyOnly` grants `dynamodb:GetItem` on `arn:aws:dynamodb:us-east-1:<account>:table/etf-classifications` and nothing else (round 22).

## Blast radius, by the producers' own rules

**What the act may touch.**
- THREE new gold prefixes written by this cell, `.../gold/account_activity_daily/`, `.../gold/account_lot_realized/`, `.../gold/account_lot_unrealized_daily/` (two objects per table-day: `date=<D>/data.parquet` and `date=<D>/manifest.json`; a table with no row on a day writes no object for it). They hold no object today. ONE new prefix from round 22, `.../gold/account_class_daily/`, also holds none.
- The returns prefix `.../gold/account_return_daily/` is written exactly as before, byte-identically: the round-25 handler and the extended handler produced the same returns parquet for the same day and accounts, sha256 `8d18f775...073e` on both, and the same class parquet, sha256 `199c6362...aa5e` on both (record `RELEASE_LOCAL_RUN.json`, 20 accounts, 2026-10-05). The scheduled fire writes only days AFTER the newest landed returns day, so it rewrites no landed returns key. A manual backfill event can rewrite landed returns, class and lot days, to the same bytes. The re-pin of `account_return_daily.py` (pin 0, row W23-S6) is not covered by that equality and is read by A4.
- DynamoDB: `GetItem` on `etf-classifications` (round 22), one item per distinct held identifier. No Scan, Query, index, write or Delete.
- S3 reads: the role's silver read set gains three prefixes of the SAME bucket and custody master it already reads (`opal-data-assets`, `schwab/08335338/silver/`); the gold read set gains the class, activity, realized and unrealized prefixes, which the handler lists for each table's newest landed day. Whether the silver bucket's own policy admits the role on the three added prefixes is not read by this cell (row W23-S1); a refusal is `AccessDenied` on the first lot read and lands as Branch B.

**What the act may not touch.** `.../gold/dim_return_method/` (another cell's served row; not in the write set); the holdings gold (read only); the silver prefixes (read only); any other firm's bucket or prefix; the platinum prefix and the publisher; any other Lambda, role or table; the schedule. The policy carries no `s3:Delete*`, no write to any table, no `dynamodb:Scan`, and no write grant beyond the five gold prefixes above.

**Writers of the property, counted.** Each of `account_activity_daily/`, `account_lot_realized/`, `account_lot_unrealized_daily/` has ONE writing rule, `account_activity_lots.emit_day`, called only from `handler.emit_lots`, reached by TWO paths: the scheduled fire (`catch_up_lots`) and an explicit backfill invocation by a seat (`run_backfill`, same code). The producer's own `--local` CLI has no upload path (a test asserts `put_object`, `upload_file`, `stream_to_parquet` and `s3://` occur only inside `emit_day`). `account_class_daily/` keeps its one rule (`emit_class_day` from `handler.emit_classes`, two paths). `account_return_daily/` keeps its one handler writer. N = 1 rule per new property.

**The manual path.** The Lambda event can carry `accounts`, `dry_run`, or `backfill` (`start`, `end`, at most 25 trading days, only days at or before the newest landed returns day, `accounts` "population" or a list). A backfill now also rewrites the three tables for the same days. `dry_run` computes and prints and writes none of the five. It creates no state the schedule cannot reach: the days written are the returns days, and a backfill never extends the returns table.

## Rollback, per key

- **Lambda.** The prior function is the artifact recorded in the source map at `last_deployed_commit` `829e46ed7f` (2026-10-05T00:12:52Z): `investor-reporting/irpt-reporting-gold-lambda.zip`, `deployed_code_sha256` `Mex71Y5gk9RYE9q885knj3Ph12xV2Y9eVqMl3uJ1Z44=`. The issuer records the live CodeSha256 and the artifact object's S3 version id before the apply (not read by this cell). Rollback is the Terraform route only (`aws lambda update-function-code` is barred): re-pin the prior artifact version in the source map and run a targeted `safe-apply`.
- **Role policy and role description.** The applied state is `iam.tf`/`locals.tf` at `4c34d86104`. Reverting `efeb21df71` restores the round-22 policy (returns + class write set); reverting round 22's files too restores `4c34d86104`. Run the same targeted apply. The statements removed are the activity, realized and unrealized writes and reads, the lot-table silver reads, and (to `4c34d86104`) the class read, write and the DynamoDB `GetItem`.
- **Each new gold prefix** (`account_activity_daily`, `account_lot_realized`, `account_lot_unrealized_daily`, `account_class_daily`). Each is new, so there is no prior version of any key. Rollback is to delete the objects under the prefix AFTER the issuer's word (an S3 delete is not this packet's act and is not in the role's grant). Each fire adds two keys per table-day, listed in the fire's log line `<day> <table> rows=<n> LANDED`.
- **Returns prefix.** A day written by the extended function is byte-equal to what the prior function writes for it, so no key needs restoring. If a returns key is ever suspect, the bucket is versioned: restore the prior version by `copy-object` from its version id (read at that moment).

## BRANCH A

**The outcome, read from the rule at signing.** Each fire computes the days after the newest landed returns day through T-1, writes those days of `account_return_daily` FIRST (unchanged code path), then the same days of `account_class_daily`, then the same days of the three tables. The tables are the activity producer's own figures (`compute_local`) and are not recomputed in the handler. Within a day the two lot tables are written first and `account_activity_daily` LAST, so the activity table's newest landed day is the marker that the whole day landed. Locally, on 20 accounts for one day: 18 activity rows (18 MEASURED, the identity within the rounding allowance), 1,330 open-lot rows, 0 realized-lot rows (no lot closed that day for these accounts), 0 repeated primary keys; over 24 trading days for the same accounts: 432 / 30 / 30,183 rows and 0 repeated keys. At the window grain 58 of 91 account-windows tie within one cent and the other 33 within the 0.05 per-account-window rounding tolerance (`WINDOWS_E1.json`; the tolerance is stated in the activity contract).

The first fire after the apply (a trading morning, 07:41 ET) lands T-1 of `account_return_daily` (and any backlog up to 10 days), the same days of `account_class_daily`, and the same days of `account_activity_daily`, `account_lot_unrealized_daily` and, on a day that closes a lot, `account_lot_realized`; each activity row carries `coverage` MEASURED where its gap is within `rounding_allowance` and GAP_ABOVE_ALLOWANCE where it is not (a real difference, carried, never plugged). The log carries `<day> class rows=<n> LANDED` and one `<day> <table> rows=<n> LANDED` per table-day, no `CLASS_SKIPPED` and no `LOTS_SKIPPED`. A realized table with no row on a day prints `<table> rows=0 NOT_WRITTEN`; that is not a failure. The first fire never pulls history: the lots tables' history lands only by backfill events (25 trading days a chunk).

## BRANCH B

A day's class or lots stage is refused by name and the returns table is still written (class and lots failures are independent of each other). The log carries `CLASS_SKIPPED <day> <reason>` and/or `LOTS_SKIPPED <day> <reason>`, and the function returns `class_failed` / `lots_failed`. Reasons that can occur for the lots stage: the bundle pins are absent (`account_activity_lots not importable`), the declaration lacks `lot_source` (`REFUSED: ... no 'lot_source' object`), `AccessDenied` on a silver lot prefix or a gold prefix (the role or the bucket policy), a partition unreadable, a producer refusal by name (a repeated primary key, a holding-term flag outside the declared map, a realized-lot id repeated in one partition), or no activity row for the day. The reasons for the class stage are those of the round-22 packet. No object is written for a refused day's activity table; if a lot table was written before the refusal the activity marker is not, and the next fire rewrites the same bytes. **The next fire retries it:** on each scheduled fire the handler lists the three lots prefixes and emits every trading day after the ACTIVITY table's own newest day through the newest returns day just written (at most 10 days per fire, oldest first); a day that still fails is logged by name and the returns and class tables are never held. A timeout or out-of-memory kill in the lots stage (row W23-S2) ends the invocation in error AFTER the returns and class days are written, so no returns or class day is lost; the lots days of that fire are not written and are retried the same way, and a backfill event closes a day by hand.

Neither branch moves a returns key. Neither moves "Data through". No served consumer reads the class table or the three tables today.

## After-read the apply will run

On the first fire after the apply, with the issuer reading S3 and the function's log:
1. **A1, the log.** Zero `CLASS_SKIPPED` and zero `LOTS_SKIPPED` lines, one `<day> class rows=<n> LANDED` per day and one `<day> <table> rows=<n> LANDED` per table-day (realized may read `rows=0 NOT_WRITTEN`). Else Branch B: name the reason, and the function's duration and memory from its REPORT line.
2. **A2, the activity identity.** Pick one account-day with `coverage` MEASURED in `.../gold/account_activity_daily/date=<T-1>/data.parquet`; print `beginning_value + contributions - withdrawals + realized + unrealized_change + income - ending_value`, its `identity_gap` and its `rounding_allowance`: the absolute gap is within the allowance. Print the day's coverage census from the manifest.
3. **A3, the keys.** For each of the three partitions print rows and distinct values of the declared `primary_key` (`org/standards/IRPT_DASHBD_ACCOUNT_*_CONTRACT.json`): equal. Print `basis_source` counts on the two lot tables: every value among CUSTODIAN, IN_KIND_TRANSFER_VALUE, WASH_SALE_EXCLUDED_BASIS.
4. **A4, DELTA=0 on the served returns.** The `account_return_daily` partition for T-1 equals a local run of the round-25 handler (`git show 5ffd7b740d:infra/aws/lambda/investor-reporting/reporting-gold/handler.py`) for a named sample of accounts, row by row (this reads the effect of pin 0 as well).
5. **A5, the grant.** `get-role-policy` shows the write set is exactly the five gold prefixes with `s3:PutObject` only, the silver read statements list the six silver prefixes, and `dynamodb:GetItem` on `table/etf-classifications` is the only DynamoDB action.
6. **A6, the class release.** The round-22 after-read A2 (the class identity) and A3 (the unclassified share) stand as written in `NEVER_WIDEN_PACKET_ACCOUNT_CLASS_DAILY_RELEASE.md`, read from the class partition of the same fire.

A1 to A6 are read, not waited on: an ad-hoc invoke with `dry_run` computes and prints without writing and may be used for QA, and for the sizing in Unmeasured, before the organic fire; it writes none of the five tables.

## The build's file list (every file the bundle carries; sha256 at `efeb21df71`)

`handler.py` is staged from the source directory; every other member is a pinned blob (the lane sets the pins and re-reads these values at the drain commit).

| Member (`repo_path`) | sha256 at `efeb21df71` |
|---|---|
| `infra/aws/lambda/investor-reporting/reporting-gold/handler.py` | `0294a5418de4e1a8fb942223a4ee4d2bdc611611380fb8b19065d1fe3b37b06c` |
| `data/assets/scripts/gold/irpt_reporting/account_return_daily.py` | `9935f5c7bcd7bd9ca071ae7b7a672a49a5d96fcb0cd7d558c9fc3bc49157fc19` |
| `data/assets/scripts/gold/irpt_reporting/account_class_daily.py` | `2def366fb5dea1abce76a08ca6e1c29ab8713127a47764695c9bd140178edc11` |
| `data/assets/scripts/gold/irpt_reporting/account_activity_lots.py` | `fe7ea305d66d5fe19f019a2e71e3ca8ecca11a783d60ba905ca1682f1d4cbcc2` |
| `data/assets/scripts/gold/irpt_reporting/sources.json` | `5dd1f367d4d0f87aea6f15c077b2eb064b27bb6f5d74d1d572e4d7d6d16d76b2` |
| `org/tier1_exec/4.0.0_SA_CRO/deliverables/SCHWAB_TRANSACTION_CODE_CLASSIFICATION_20260811.json` | `8b803eecfd1417b1bd4c10a9e269a6a27e295ecb6304d90c288ec596b6ce0bae` |
| `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.4.0_DS_ClientPlatform~S/MEASURED_THRESHOLDS_R1.json` (packaged as `data/assets/scripts/gold/irpt_reporting/MEASURED_THRESHOLDS_R1.json`) | `551920f0c364490d87cac260d5df2ad601ff7dac44f56043176065a3c3c2d177` |
| `data/assets/scripts/lib/stream_parquet.py` | `2e3762e14b486ddb8c21a3025f0c62c501b2bd8b8b9bf5b1801a675802cf7437` |
| `lib/opal_naming.py` | `7a75974236c72511cfe8b70a57d9e656bdab20412daf9e3b2e55e9f8128b63e2` |
| `lib/trading_calendar.py` | `8ec8e43def5854f67a0dadcef7c735906f44aa07ae5916b2fc62c4c81ca9a3a8` |
| `org/standards/NAMING_SCHEMA.json` | `00e744c8eabf0cfd5e6c2af413788cea13cb92eb50b11e5dc2e49596f2dd3e60` |
| `infra/logic/registry/systems.json` | `c2c9cc5551ff98a7bddc23d15267683544f244a2f22fa84a3c6d831bd5877cf7` |
| `infra/logic/registry/scopes.json` | `8fcd28d3e2b339bda4d3cb12f860d9a06b7c7bb79d578a731fed4a9f37cb65d1` |
| `infra/logic/registry/tiers.json` | `d3d51e30150a4baefd9405ddfe9adfa1740e084dfb1857c8fcb0e87a3c1188f3` |
| `infra/logic/registry/exemptions.json` | `e449fe0bba48118d0f51324baf2e463dd140a5c6f62672f0dad1af6f9c9e9735` |
| `infra/logic/registry/remediations.json` | `49cde7fb7a8d48cf1f9646df4ed66fa230b3863919e229b3a90d4f86866f6353` |
| `infra/logic/registry/resources.json` | `1f98affd0eb8ed0c7fe159f742e5e708ea3230191c8ca42daf6b40144e17a7b6` |
| `infra/logic/registry/reporting_policies.json` | `cb0167ec4aa98d52ef071670c46384ec5b8627e09ef18359194fdd47080b0e8f` |
| `infra/aws/lambda/v2_portal/_shared/etf_classifications_dynamodb.py` (packaged flat as `etf_classifications_dynamodb.py`) | `92b64d97d69bfee9bc2d4b06fe13c8719a30856fc70f8588e1b29289f89afccc` |

The issuer writes `infra/aws/lambda/ci/lambda-source-map.json` at the apply (this cell does not edit it). `account_activity_lots.py` imports only `account_return_daily`, `trading_calendar`, pandas, pyarrow and the standard library; `sample_accounts()` imports `handler` lazily and is reached only by the producer's own `--local` CLI.

## Unmeasured, stated

- **Duration and memory at population scale (row W23-S2, ARMED).** The 20-account, one-day run took 69.5 s and a 992.2 MB peak working set, against 34.6 s and 228.4 MB for the round-25 handler on the same day. The population is 7,597 accounts (380 times the sample); the lots stage reads and loops over every open lot of every account for each day it emits. The function's ceiling is 900 s and 2048 MB and this order does not change them. The lots stage runs last, so a timeout cannot lose a returns or class day; it would stop that fire's lots days and error the invocation. The issuer sizes it with a `dry_run` invoke before the organic fire.
- **The silver bucket's own policy on the three added prefixes** (row W23-S1): the role grant is derived; the bucket's admission is not read here.
- **The served returns producer pin** (row W23-S6): see pin 0 and A4.
- **`terraform fmt` and `validate`** were not run (no binary on this box, row W23-S5).

## CTO half -- 1.0.0_SA_CTO

UNSIGNED. Signing means: the blast radius above is the whole act -- FIVE gold write prefixes (returns byte-identical, class from round 22, and the activity, realized and unrealized prefixes new), three more silver READ prefixes of the custody master the role already reads, one DynamoDB table read by key; both branches are read from the rules; the writers are counted (one rule per new prefix, two paths); the rollback is per key; the preconditions are the deploying lane's and the issuer's and are met before the apply; a class or lots day that fails is retried by the next fire; the sizing risk in Unmeasured is accepted for the first fire with the `dry_run` read named there. **On both halves here signed, the round-22 class pair (the CTO half and the COO half of `NEVER_WIDEN_PACKET_ACCOUNT_CLASS_DAILY_RELEASE.md`) is superseded by this packet**, which carries that release in the same act.

## COO half -- 2.0.0_SA_COO~D2

UNSIGNED. Signing means: the issuer will have the deploying lane set pins 0 to 4 and rebuild the artifact (precondition 1), read the plan against the expected `0 to add, 3 to change, 0 to destroy` and STOP on any difference (precondition 2), size the lots stage with a `dry_run` invoke (precondition 3), apply once from the saved plan, and run A1 to A6 on the first fire. A skipped class or lots day is retried by the next fire's catch-up, so no standing backfill is owed; the lots tables' history is a backfill the issuer orders separately. **On both halves here signed, the round-22 class pair is superseded by this packet.**
