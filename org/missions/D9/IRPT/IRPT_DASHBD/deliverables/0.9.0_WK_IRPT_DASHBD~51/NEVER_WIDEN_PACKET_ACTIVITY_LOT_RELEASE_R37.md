# Never-widen sign-off packet, RE-CUT at HEAD (round 37) -- the reporting-gold function also writes `account_activity_daily`, `account_lot_realized` and `account_lot_unrealized_daily`, and carries the unapplied `account_class_daily` release, with the realized-lot key extended by `proceeds` and EVERY bundle member pinned to the commit that carries its HEAD bytes (IRPT_DASHBD DB-b-74; re-cut of `deliverables/0.9.0_WK_IRPT_DASHBD~46/NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE_R35.md`)

Author `0.9.0_WK_IRPT_DASHBD~51` for `2.0.0_SA_COO~D2`, 2026-10-09. Cell: `DB-b-74`. Halves owed: `1.0.0_SA_CTO` and `2.0.0_SA_COO~D2`, both UNSIGNED.
Status: RE-CUT; NOTHING APPLIED. No `terraform` command, no `aws lambda` call, no S3 write, no source-map or pin edit, no vendor call and no download was made by this cell. The only AWS calls were S3 `list-objects-v2` reads of the four new gold prefixes and the returns prefix (see Rollback). The apply and the first fire are the issuer's act under the two signed halves. This packet covers the WHOLE next apply of the root: the `account_class_daily` release (round 22, cell DB-b-34) AND the three activity and lot tables, which the round-36 rollback took off the live function.
Branch `wk-IRPT_DASHBD-51`, cut from `box/dell2` @`3026d29bbb` (DB-b-73 drained). This cell edits no member of the file list: every sha256 below is the bytes of the member at that base and at this branch's HEAD.

## Why the R35 packet was re-cut, and what the rollback changed

Round 36 applied the R35 packet and rolled it back (CTO msg 2393): four bundle members were packaged at older pins than the signed list (row IRPT_DASHBD-D2-W47-S4: `lib/opal_naming.py`, `infra/logic/registry/systems.json`, `exemptions.json`, `reporting_policies.json`), and the lots stage sizing failed on 2026-10-07 (row S5; repaired by DB-b-73). The rollback is in git: `0709c0a960` restored `iam.tf`, `locals.tf` and `lambda.tf` of the Terraform root to their bytes at `4c34d86104`; `bfd71e73c9` restored the source-map entry `irpt-49f-reporting-gold-lambda` (`staged_from` and `files`) to its content at `01661cf0da`; `310380d8cd` records the targeted rollback apply (0 to add, 3 to change, 0 to destroy) and the live CodeSha256 read back as `Mex71Y5gk9RYE9q885knj3Ph12xV2Y9eVqMl3uJ1Z44=` (the pre-release anchor).

**Two premises of the R35 packet no longer hold at HEAD, stated and not hidden (row IRPT_DASHBD-D2-W51-S1):**
1. R35 said the Terraform root had 0 changed files since the round-26 packet. At HEAD the root is the ROLLED-BACK state: `iam.tf`, `locals.tf` and `lambda.tf` differ from `efeb21df71` (3 files, 18 insertions and 83 deletions against `ec9c251de8`). The apply of this packet needs the three files back at the release bytes of `efeb21df71` (precondition 2 below). The root's other files have 0 changes.
2. R35 said the source-map entry listed the pins as the R26 packet found them and named `last_deployed_commit` `829e46ed7f`. At HEAD the entry is the pre-release content again (16 `files`, 15 `staged_from`) with `last_deployed_commit` `440f89bb56` (2026-10-09T04:32:33Z) and `deployed_code_sha256` `Mex71Y5gk9RYE9q885knj3Ph12xV2Y9eVqMl3uJ1Z44=`; 10 of its 15 `staged_from` rows carry a sha256 that differs from HEAD's bytes (the table below pins all 15 and the 3 members the release adds, at HEAD's bytes).

## What changed since the R35 packet (`ec9c251de8` .. `3026d29bbb`)

Measured by `git diff ec9c251de8..HEAD` on the 19 file-list members: 2 of the 19 differ, 17 are byte-equal. The file list below prints each member's state.

| Member | Commits | What it changes in behaviour | Widens the radius? |
|---|---|---|---|
| `data/assets/scripts/gold/irpt_reporting/account_activity_lots.py` | 1 (`c0afa6f55e`, DB-b-73) | The `account_lot_realized` primary key is now `(firm, account_id, business_date, lot_id, quantity, proceeds)`. The round-28 key `(firm, account_id, business_date, lot_id, quantity)` REFUSED the whole 2026-10-07 lots day on one repeat pair (2 rows of 3,245), the two halves of a wash-sale split lot: same order, opening event, acquired date and quantity, different proceeds. Both halves are real events and both are kept. The producer still refuses by name a row identical in every column to another, and a repeat of the whole new key with another column differing. `org/standards/IRPT_DASHBD_ACCOUNT_LOT_REALIZED_CONTRACT.json` (not a bundle member) carries the same key (DB37-1-AC1 of the DB-b-73 order). | No. No new read, write or action; the set of columns of the table is unchanged. |
| `infra/logic/registry/scopes.json` | 1 (`5f962296ae`, DB-b-75) | A new MASTER row `4698` (firm `inflection`, vendor `orion`) and `masters: ["4698"]` on the inflection FIRM row. The naming registry's record of a vendor-issued master; read by `lookup()`, which this function's data path calls only for the 49financial declaration's `registry_key`. This function reads and writes no inflection key. | No. |

Unchanged since R35 and unchanged by it: `handler.py` (still calls `compute_local_batched`, default batch 1000), `account_return_daily.py`, `account_class_daily.py`, `sources.json`, the classification table, the thresholds, `stream_parquet.py`, `trading_calendar.py`, `NAMING_SCHEMA.json`, `tiers.json`, `systems.json`, `exemptions.json`, `remediations.json`, `resources.json`, `reporting_policies.json`, `lib/opal_naming.py`, `etf_classifications_dynamodb.py`.

**Does the blast radius widen? Against the R35 packet: NO.** The set of prefixes written, the set of prefixes read, the actions and the DynamoDB table are exactly R35's, and the key extension adds no column and no object. The one thing that moves is the CONTENT of a table the packet already names: a realized partition for a day that repeats `(lot_id, quantity)` with different proceeds now LANDS (2026-10-07: 3,245 rows) where the R35 function would have logged `LOTS_SKIPPED` for the day. **Against the LIVE function (the rolled-back state), YES, by exactly the whole release R35 asked for and this packet re-asks:** four more gold write prefixes (`account_class_daily`, `account_activity_daily`, `account_lot_realized`, `account_lot_unrealized_daily`), three more silver read prefixes of the custody master the role already reads, the class and lot gold read prefixes, and `dynamodb:GetItem` on `table/etf-classifications`. Nothing beyond R35's list is added.

## The three conditions, with the values measured by DB-b-73

Values come from `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~50/LOTS_KEY_E1.json` (`kit_runs`, `runtime`), each printed by the process that produced it (kit runtime: Python 3.12.10, pandas 2.2.3, numpy 1.26.4, pyarrow 14.0.2; the kit prints `runtime: pandas 2.2.3, future.infer_string = False (served behaviour in force: True)`). The S32 read (the pandas 2.2.3 equalities, DB-b-43's test in served mode 4 of 4) is R35's and stands unchanged: DB-b-73 changed no code those arms read except `account_activity_lots.py`'s realized-key check.

**S31 -- the extended handler over the whole population, wall and peak against 900 s / 2048 MB.** MEASURED on the kit, default batch (1000), `--local`, one sequential process per day, 7,604 accounts of 7,604:

| Kit day | Accounts | Lots rows | `peak_mb` | `total_s` | Lots stage | Returns stage | Class stage |
|---|---|---|---|---|---|---|---|
| 2026-10-06 | 7,604 | 570,532 (realized 2,523; unrealized 568,009) | 1669.7 | 665.0 | 520.14 s | 48.48 s | 89.49 s |
| 2026-10-07 | 7,604 | 569,121 (realized 3,245; unrealized 565,876) | 1668.9 | 652.21 | 499.92 s | 49.36 s | 95.82 s |

Against the function's 900 s and 2048 MB (the peak is the process peak working set over the whole process; the lots stage peak equals it on both days):

| Kit day | Peak as a share of 2048 MB | Memory margin to 2048 MB | Time as a share of 900 s | Time margin to 900 s |
|---|---|---|---|---|
| 2026-10-06 | 81.5% | 378.3 MB | 73.9% | 235.0 s |
| 2026-10-07 | 81.5% | 379.1 MB | 72.5% | 247.79 s |

**The CTO's stop line is 85%.** 85% of 2048 MB is 1740.8 MB, so the margin to the line is 71.1 MB on 2026-10-06 and 71.9 MB on 2026-10-07; 85% of 900 s is 765 s, so the time margin to the line is 100.0 s and 112.79 s. Both days are under the line on both axes. R35's 2026-10-06 run read 1672.3 MB and 374.93 s total (264.36 s lots stage); the peak is flat (1669.7 MB, 2.6 MB lower) and the wall is 290 s longer, in the lots stage (520.14 s). This cell does not explain that difference. The peak is a Windows working set on dell2, not the Lambda's `Max Memory Used`, and dell2's cores are not the Lambda's: the Lambda's own REPORT line is read by the `dry_run` of precondition 3, against the same 85% line.

**S33 -- no refusal on the kit runs.** Two full kit runs (the S31 runs), one per day. The log lines matching `REFUSED`, `LOTS_SKIPPED` or `CLASS_SKIPPED`: 0 on 2026-10-06 and 0 on 2026-10-07 (`refusal_lines_in_log` 0 on both).

```
refusals: 0
```

`s33_holds: true` (S33 holds iff `refusals` is 0 on every day run). The 2026-10-07 day is the one the round-28 key refused; it now runs to completion with `account_lot_realized` at 3,245 rows.

## Root

`infra/aws/terraform/investor-reporting/reporting-gold` -- state the Terraform state bucket's key `investor-reporting/reporting-gold/tfstate` (the bucket name carries the AWS account id and is not typed here).
No other root is read for a write, planned or applied by this act.

## Preconditions the signed act does not cover

1. **PRECONDITION OF THE APPLY -- the bundle pins (the deploying lane's act, rule 13; `lambda-source-map.json` is outside this cell's grant and was not edited).** The pins table below is the whole list: one row per `staged_from` member of the entry `irpt-49f-reporting-gold-lambda` at HEAD (15) plus the three members the release adds (16 `files` at HEAD; 18 pinned rows, `handler.py` is staged from the source directory). Each `pin` is the newest commit on `origin/CLOUD` whose bytes of that path equal HEAD's (the commit that last touched the path on `origin/CLOUD`, whose blob is HEAD's blob); each `sha256` is `git show <pin>:<path> | sha256sum`, and it equals HEAD's bytes. `origin/CLOUD` here is the local remote-tracking ref at `3195077755` (2026-10-09T02:20:25-04:00); no fetch was made.

| repo path | pin | sha256 (equal at the pin and at HEAD) |
|---|---|---|
| `data/assets/scripts/gold/irpt_reporting/account_return_daily.py` | `ba544b60646d9b96e8bf126b4a47064dba0c70f5` | `9935f5c7bcd7bd9ca071ae7b7a672a49a5d96fcb0cd7d558c9fc3bc49157fc19` |
| `data/assets/scripts/gold/irpt_reporting/sources.json` | `efeb21df7147955a64f79a4f7b7ff2cc5d3d9426` | `5dd1f367d4d0f87aea6f15c077b2eb064b27bb6f5d74d1d572e4d7d6d16d76b2` |
| `org/tier1_exec/4.0.0_SA_CRO/deliverables/SCHWAB_TRANSACTION_CODE_CLASSIFICATION_20260811.json` | `3cb9f9b6d51febe101a77a3a5f973e7f177b95fb` | `8b803eecfd1417b1bd4c10a9e269a6a27e295ecb6304d90c288ec596b6ce0bae` |
| `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.4.0_DS_ClientPlatform~S/MEASURED_THRESHOLDS_R1.json` | `6be02af162eaeff01ca19d2e5b228ffce6091cc7` | `551920f0c364490d87cac260d5df2ad601ff7dac44f56043176065a3c3c2d177` |
| `data/assets/scripts/lib/stream_parquet.py` | `4cf86b48911190df03ae82f41d081e856e12bca9` | `2e3762e14b486ddb8c21a3025f0c62c501b2bd8b8b9bf5b1801a675802cf7437` |
| `lib/opal_naming.py` | `e15671f61147a88fcccab86f558a53b9d7ac53d3` | `9d301e1c0fe61a66384c9fdab5380b536767f3ef3927bb8414c0b93305ba9296` |
| `lib/trading_calendar.py` | `4b766e4e2d26a1b35e94016f01327f8ee26c476d` | `8ec8e43def5854f67a0dadcef7c735906f44aa07ae5916b2fc62c4c81ca9a3a8` |
| `org/standards/NAMING_SCHEMA.json` | `eb29bf7f377783fd38f76a49b2d76de39c2ccf03` | `00e744c8eabf0cfd5e6c2af413788cea13cb92eb50b11e5dc2e49596f2dd3e60` |
| `infra/logic/registry/systems.json` | `530ef17ff8e0f64661e5c4cfd8e29ecc7996382c` | `70cfd07e4555880ce96d084d7be0ea9e76b76c1f0f3666295ed0ac95f4569053` |
| `infra/logic/registry/scopes.json` | `5f962296ae07ad9b52c368391378e8346fa68097` | `13947f7f2b35c6c9ed403e6c21ba87d1abd00156c06a50dcd37cdd69dedeaade` |
| `infra/logic/registry/tiers.json` | `b282500581c67e8901000523ac85dc8d4b9f476d` | `d3d51e30150a4baefd9405ddfe9adfa1740e084dfb1857c8fcb0e87a3c1188f3` |
| `infra/logic/registry/exemptions.json` | `2a809c975e3e682dcb0fea85dd3faf7fac8f1d63` | `8c5ba7257f417fe6e94bc3d84d7dda5d528116de2eb2c0b205c198d07c51a186` |
| `infra/logic/registry/remediations.json` | `fd3b3b7bf24388d1558d72ff043f3b6e8f62b8d6` | `49cde7fb7a8d48cf1f9646df4ed66fa230b3863919e229b3a90d4f86866f6353` |
| `infra/logic/registry/resources.json` | `17ae4222c7c2061b17db706d6ea8d23d16e81832` | `1f98affd0eb8ed0c7fe159f742e5e708ea3230191c8ca42daf6b40144e17a7b6` |
| `infra/logic/registry/reporting_policies.json` | `0c35aeeaa8041ffd49deb0b2fb4f5ac27b9da50d` | `dc0eccfde86127327934064eec85ecd33f71ea56f2594dd3f032f78d0ca47e17` |
| `data/assets/scripts/gold/irpt_reporting/account_class_daily.py` | `7517444629ac5df1883d539fb84eff5b114a6f84` | `2def366fb5dea1abce76a08ca6e1c29ab8713127a47764695c9bd140178edc11` |
| `infra/aws/lambda/v2_portal/_shared/etf_classifications_dynamodb.py` | `a96e00c27975cd9067de97f9c4fc34b14679c068` | `92b64d97d69bfee9bc2d4b06fe13c8719a30856fc70f8588e1b29289f89afccc` |
| `data/assets/scripts/gold/irpt_reporting/account_activity_lots.py` | `c0afa6f55e7446fa7634d63b011c670b6b8a632c` | `63f9e20f1735f4f0003b41713ca1820d62b6ed716c047328a04458b854c8ea6c` |

   **Pin on box/dell2, not on `origin/CLOUD` (1 of 18):** `data/assets/scripts/gold/irpt_reporting/account_activity_lots.py` is pinned at `c0afa6f55e` (DB-b-73), which carries HEAD's bytes on `box/dell2` and is not on `origin/CLOUD` yet; `origin/CLOUD`'s newest commit for that path carries older bytes (the round-28 key). The pin is valid once the drain carries `c0afa6f55e` to CLOUD as the same commit (a merge keeps it); the lane re-reads `git show <pin>:<path> | sha256sum` at the apply and re-pins to the drain commit if the commit id changed. The other 17 pins are on `origin/CLOUD`. The 10 existing rows whose sha256 differs from HEAD today are `account_return_daily.py`, `sources.json`, `opal_naming.py`, `trading_calendar.py`, `NAMING_SCHEMA.json`, `systems.json`, `scopes.json`, `exemptions.json`, `resources.json` and `reporting_policies.json`; the lane sets EVERY row to the pin printed above (a row already at HEAD's bytes may keep its pin or take this one; the bytes are equal).

   The pairings hold as R35 stated: `sources.json` with `account_activity_lots.py` (the producer refuses by name without `lot_source`), and the HEAD `handler.py` with the HEAD `account_activity_lots.py` (the handler calls `compute_local_batched`; a HEAD handler with a round-26 producer logs `LOTS_SKIPPED` with an `AttributeError` on every day). Every row above is pinned at HEAD's bytes, so no member is older than the signed list. The lane then rebuilds `investor-reporting/irpt-reporting-gold-lambda.zip` and prints the drain commit and the sha256 values at the apply. Without the pins the function runs as it does today (Branch B).
2. **PRECONDITION OF THE APPLY -- restore the Terraform root to the release bytes (the issuer's or the deploying lane's act; the root is outside this cell's grant).** The rollback left `iam.tf`, `locals.tf` and `lambda.tf` at their `4c34d86104` bytes. The release needs them at the `efeb21df71` bytes (the five write prefixes, the class and lot reads, `ReadTheClassTableByKeyOnly`); `git show efeb21df71:<path>` reproduces them, and they were unchanged through `ec9c251de8`:

| Terraform root file | sha256 at HEAD (rolled-back state, equal to `4c34d86104`) | sha256 at `efeb21df71` (the release bytes, unchanged to `ec9c251de8`) | Restore from |
|---|---|---|---|
| `infra/aws/terraform/investor-reporting/reporting-gold/iam.tf` | `97b7ab2068cb7c2359fddabf26ec39514e8b37f9121a10d58a5fe7b61d57281b` | `2c0ed37714502decfc1ec3d1ebd5ae2c27eb9fee5f9685100f90bba7a6c594cb` | `efeb21df71` |
| `infra/aws/terraform/investor-reporting/reporting-gold/locals.tf` | `42be6713e71068451787f2731e160f8bd940f13a2cfe611600e4edad4434a6db` | `5fe82384a973d487bac6bd00feb26e797e341becda984b03e1efe36f69bf0980` | `efeb21df71` |
| `infra/aws/terraform/investor-reporting/reporting-gold/lambda.tf` | `977501b644b4b6d7fa6d5e8cc386d1289856a5a04967950efcaa4c8b74667282` | `9ae1871907fede7a8071cc0c49da740601d5c4d51d7b895a06c0002d6d848301` | `efeb21df71` |

   The root's other files have 0 changed files since `ec9c251de8`.
3. **The plan.** With the three files restored and the artifact rebuilt, the expected counts are those of R35 (below), read against the live state the rollback apply left (`310380d8cd`). The issuer reads the plan before the signed halves are used and STOPS if it differs from the expected counts (this cell does not run `terraform`). Without precondition 2 the plan shows the function change only: STOP.
4. **Sizing on the Lambda.** The kit runs above fit the limits on dell2 under the 85% line (S31). The Lambda's own duration and `Max Memory Used` are read by a `dry_run` invoke before the organic fire (see Unmeasured); row W23-S2 stays with its disarm owner `2.0.0_SA_COO~D2` until that read.

## Names and addresses (builder output, printed)

Printed by `lib/opal_naming.py` at HEAD (`address()` and `name()` called directly), with the firm from the declaration's `registry_key`. Identical to R35's lines. Nothing below is typed by hand:

```
address('irpt', '49financial', 'gold', 'account_activity_daily', 'date=2026-10-05') = s3://opal-data-49financial/irpt/49financial/gold/account_activity_daily/date=2026-10-05
address('irpt', '49financial', 'gold', 'account_lot_realized', 'date=2026-10-05') = s3://opal-data-49financial/irpt/49financial/gold/account_lot_realized/date=2026-10-05
address('irpt', '49financial', 'gold', 'account_lot_unrealized_daily', 'date=2026-10-05') = s3://opal-data-49financial/irpt/49financial/gold/account_lot_unrealized_daily/date=2026-10-05
address('irpt', '49financial', 'gold', 'account_return_daily', 'date=2026-10-05') = s3://opal-data-49financial/irpt/49financial/gold/account_return_daily/date=2026-10-05
address('irpt', '49financial', 'gold', 'account_class_daily', 'date=2026-10-05') = s3://opal-data-49financial/irpt/49financial/gold/account_class_daily/date=2026-10-05
name('irpt', '49financial', 'reporting-gold', 'lambda') = irpt-49f-reporting-gold-lambda
name('irpt', '49financial', 'reporting-gold', 'role')   = irpt-49f-reporting-gold-role
name('irpt', '49financial', 'reporting-gold', 'policy') = irpt-49f-reporting-gold-policy
name('irpt', None,          'reporting-gold', 'lambda') = irpt-reporting-gold-lambda          (the artifact)
```

The Terraform side mirrors each table name ONCE in `locals.tf` (`irpt_rg_gold_table_class`, `irpt_rg_gold_table_activity`, `irpt_rg_gold_table_realized`, `irpt_rg_gold_table_unrealized`) at the `efeb21df71` bytes, each cited to the producer's constant where it lives. The custodian's lot tables are not typed there either: the silver read prefixes are derived from the declaration's `lot_source`. Derived sets (from `sources.json` and `scopes.json`; the `scopes.json` change since R35 adds a MASTER row for another firm and alters none of these):

```
silver READ prefixes  (bucket opal-data-assets): schwab/<custody master>/silver/{dim_position,dim_balance,fact_trn,fact_rld,fact_uln,fact_ult}/
gold   READ prefixes  (bucket opal-data-49financial): irpt/49financial/gold/{holdings_performance_daily,account_return_daily,account_class_daily,account_activity_daily,account_lot_realized,account_lot_unrealized_daily}/
gold   WRITE prefixes (bucket opal-data-49financial): irpt/49financial/gold/{account_return_daily,account_class_daily,account_activity_daily,account_lot_realized,account_lot_unrealized_daily}/
```

## The act

ONE targeted `safe-apply` of `infra/aws/terraform/investor-reporting/reporting-gold/`, from a saved plan, with the rebuilt artifact, after preconditions 1 and 2.

Plan (TARGETED; one `-target=` per resource the apply may change; none outside this root):

```
cd infra/aws/terraform/investor-reporting/reporting-gold
terraform plan -out=<planfile> -target=aws_iam_role.irpt_reporting_gold -target=aws_iam_role_policy.irpt_reporting_gold -target=module.irpt_reporting_gold.aws_lambda_function.this
```

Expected: **Plan: 0 to add, 3 to change, 0 to destroy.** Why each:
- `aws_iam_role.irpt_reporting_gold` -- 1 change in place: the `description` text (it names the new tables and the lot-table reads). The trust policy and name do not change.
- `aws_iam_role_policy.irpt_reporting_gold` -- 1 change in place: the policy document (below).
- `module.irpt_reporting_gold.aws_lambda_function.this` -- 1 change in place: `s3_object_version` and `source_code_hash` from the rebuilt artifact. Schedule `cron(41 7 ? * MON-FRI *)` (America/New_York), timeout 900 s, memory 2048 MB and the layer are unchanged.

If the artifact is not rebuilt first, or the Terraform files are not restored, the plan shows fewer changes: STOP, the bundle is not what is signed. Any `add`, any `destroy`, or any resource outside the three: STOP.

The policy document changes as follows (the round-22 class changes and DB-b-41's, the same as R35's; nothing since touches it):
- write set `irpt_rg_gold_write_arns` becomes the returns, class, activity, realized and unrealized prefixes (`s3:PutObject` only);
- the gold read set and its ListBucket prefix pattern become the six gold prefixes;
- the silver read set and its ListBucket prefix pattern gain the three custodian lot-table prefixes `fact_rld`, `fact_uln`, `fact_ult` (`fact_trn` is the transactions prefix it already holds);
- the statement `ReadTheClassTableByKeyOnly` grants `dynamodb:GetItem` on `arn:aws:dynamodb:us-east-1:<account>:table/etf-classifications` and nothing else (round 22).

## Blast radius, by the producers' own rules

**What the act may touch.**
- THREE new gold prefixes, `.../gold/account_activity_daily/`, `.../gold/account_lot_realized/`, `.../gold/account_lot_unrealized_daily/` (two objects per table-day: `date=<D>/data.parquet` and `date=<D>/manifest.json`; a table with no row on a day writes no object for it). ONE new prefix from round 22, `.../gold/account_class_daily/`. Read by this cell with `list-objects-v2` at 2026-10-09T06:27Z: each of the four holds 0 objects (a positive control on the returns prefix lists objects). The round-36 apply is recorded in the source map at 2026-10-09T00:01 ET and its rollback at 00:33 ET, both before the 07:41 ET fire, so no scheduled fire ran with the release in place.
- The returns prefix `.../gold/account_return_daily/` is written exactly as before, byte-identically (R35's S32 arm: the returns table of 2026-10-06, 7,604 accounts, 6,888 rows, built from the deployed pin and from HEAD is byte-identical on the kit; `account_return_daily.py` is unchanged since). The scheduled fire writes only days AFTER the newest landed returns day, so it rewrites no landed returns key. A manual backfill event can rewrite landed returns, class and lot days, to the same bytes.
- DynamoDB: `GetItem` on `etf-classifications` (round 22), one item per distinct held identifier. No Scan, Query, index, write or Delete.
- S3 reads: the role's silver read set gains three prefixes of the SAME bucket and custody master it already reads (`opal-data-assets`); the gold read set gains the class, activity, realized and unrealized prefixes, which the handler lists for each table's newest landed day. Whether the silver bucket's own policy admits the role on the three added prefixes is not read by this cell (row W23-S1); a refusal is `AccessDenied` on the first lot read and lands as Branch B.

**What the act may not touch.** `.../gold/dim_return_method/` (another cell's served row; not in the write set); the holdings gold (read only); the silver prefixes (read only); any other firm's bucket or prefix; the platinum prefix and the publisher; any other Lambda, role or table; the schedule. The policy carries no `s3:Delete*`, no write to any table, no `dynamodb:Scan`, and no write grant beyond the five gold prefixes above.

**Writers of the property, counted.** Each of `account_activity_daily/`, `account_lot_realized/`, `account_lot_unrealized_daily/` has ONE writing rule, `account_activity_lots.emit_day`, called only from `handler.emit_lots`, reached by TWO paths: the scheduled fire (`catch_up_lots`) and an explicit backfill invocation by a seat (`run_backfill`, same code). DB-b-73's key change is inside the rule's validation (`realized_rows()`), before `emit_day`; it adds no writer and no path. The batching changes how `compute_local_batched` assembles the rows handed to `emit_day`, not who writes: the producer's own `--local` CLI has no upload path (a test asserts `put_object`, `upload_file`, `stream_to_parquet` and `s3://` occur only inside `emit_day`). `account_class_daily/` keeps its one rule (`emit_class_day` from `handler.emit_classes`, two paths). `account_return_daily/` keeps its one handler writer. N = 1 rule per property, N = 2 paths per rule; for the five properties that is 5 rules read.

**The manual path.** The Lambda event can carry `accounts`, `dry_run`, or `backfill` (`start`, `end`, at most 25 trading days, only days at or before the newest landed returns day, `accounts` "population" or a list). A backfill also rewrites the three tables for the same days. `dry_run` computes and prints and writes none of the five. It creates no state the schedule cannot reach: the days written are the returns days, and a backfill never extends the returns table. The handler's `--batch-size` exists only on the `--local` CLI, which refuses any upload (`REFUSED: the CLI is --local only`), so it is not a path to the five prefixes.

## Rollback, per key

The rollback below is the one round 36 ran and recorded (`0709c0a960`, `bfd71e73c9`, `310380d8cd`); this cell did not run it again.

- **Lambda.** The prior function (the live one now) is the artifact `investor-reporting/irpt-reporting-gold-lambda.zip` with `deployed_code_sha256` / live CodeSha256 `Mex71Y5gk9RYE9q885knj3Ph12xV2Y9eVqMl3uJ1Z44=` (source map `last_deployed_commit` `440f89bb56`, 2026-10-09T04:32:33Z). The issuer records the live CodeSha256 and the artifact object's S3 version id before the apply (not read by this cell; round 36 recorded the restoring version as `HJZgXM5o8nsaP1ED.7K_OJ2cCuD_RrMX`). Rollback is the Terraform route only (`aws lambda update-function-code` is barred): `copy-object` of the recorded prior version onto the same key so it is latest again, re-pin the source map entry, and run a targeted `safe-apply`.
- **Role policy and role description.** The applied state before this act is `iam.tf`/`locals.tf`/`lambda.tf` at their `4c34d86104` bytes (the hashes in the table above). Rollback restores those bytes (`git show 4c34d86104:<path>`, sha256 verified against the table) and runs the same targeted apply. The statements removed are the activity, realized and unrealized writes and reads, the lot-table silver reads, the class read and write, and the DynamoDB `GetItem`.
- **Source map.** Restore the entry `irpt-49f-reporting-gold-lambda` (`staged_from` and `files`) to its content at `01661cf0da`, as `bfd71e73c9` did.
- **Each new gold prefix** (`account_activity_daily`, `account_lot_realized`, `account_lot_unrealized_daily`, `account_class_daily`). Each holds 0 objects today, so there is no prior version of any key. Rollback is to delete the objects under the prefix AFTER the issuer's word (an S3 delete is not this packet's act and is not in the role's grant). Each fire adds two keys per table-day, listed in the fire's log line `<day> <table> rows=<n> LANDED`.
- **Returns prefix.** A day written by the extended function is byte-equal to what the prior function writes for it, so no key needs restoring. If a returns key is ever suspect, the bucket is versioned: restore the prior version by `copy-object` from its version id (read at that moment).

## BRANCH A

**The outcome, read from the rule at signing.** Each fire computes the days after the newest landed returns day through T-1, writes those days of `account_return_daily` FIRST (unchanged code path), then the same days of `account_class_daily`, then the same days of the three tables. The tables are the activity producer's own figures (`compute_local_batched`, batches of 1000, the same rows as one unbatched call) and are not recomputed in the handler. Within a day the two lot tables are written first and `account_activity_daily` LAST, so the activity table's newest landed day is the marker that the whole day landed. Measured over the whole population on the kit by DB-b-73: 2026-10-06 lots rows 570,532 (realized 2,523, unrealized 568,009) and 2026-10-07 lots rows 569,121 (realized 3,245, unrealized 565,876), 0 refusals on both days. (R35's returns, class and activity row counts for 2026-10-06 (6,888, 24,992, 6,888) are R35's measurement and DB-b-73 did not re-record them; the 20-account identity and window-grain evidence of the round-26 packet stands as R35 cited it.)

The first fire after the apply (a trading morning, 07:41 ET) lands T-1 of `account_return_daily` (and any backlog up to 10 days), the same days of `account_class_daily`, and the same days of `account_activity_daily`, `account_lot_unrealized_daily` and, on a day that closes a lot, `account_lot_realized`; each activity row carries `coverage` MEASURED where its gap is within `rounding_allowance` and GAP_ABOVE_ALLOWANCE where it is not (a real difference, carried, never plugged). The log carries `<day> class rows=<n> LANDED` and one `<day> <table> rows=<n> LANDED` per table-day, no `CLASS_SKIPPED` and no `LOTS_SKIPPED`. A realized table with no row on a day prints `<table> rows=0 NOT_WRITTEN`; that is not a failure. A realized day that holds a wash-sale split pair lands both halves (two rows with the same `lot_id` and `quantity`, different `proceeds`). The first fire never pulls history: the lots tables' history lands only by backfill events (25 trading days a chunk).

## BRANCH B

A day's class or lots stage is refused by name and the returns table is still written (class and lots failures are independent of each other). The log carries `CLASS_SKIPPED <day> <reason>` and/or `LOTS_SKIPPED <day> <reason>`, and the function returns `class_failed` / `lots_failed`. Reasons that can occur for the lots stage: the bundle pins are absent or mismatched (`account_activity_lots not importable`, or an `AttributeError` for `compute_local_batched` if the handler and the producer are pinned from different commits), the declaration lacks `lot_source` (`REFUSED: ... no 'lot_source' object`), `AccessDenied` on a silver lot prefix or a gold prefix (the role or the bucket policy), a partition unreadable, a producer refusal by name (a row identical in every column to another, or a repeat of the realized key `(firm, account_id, business_date, lot_id, quantity, proceeds)` with another column differing, a holding-term flag outside the declared map), or no activity row for the day. The reasons for the class stage are those of the round-22 packet. No object is written for a refused day's activity table; if a lot table was written before the refusal the activity marker is not, and the next fire rewrites the same bytes. **The next fire retries it:** on each scheduled fire the handler lists the three lots prefixes and emits every trading day after the ACTIVITY table's own newest day through the newest returns day just written (at most 10 days per fire, oldest first); a day that still fails is logged by name and the returns and class tables are never held. A timeout or out-of-memory kill in the lots stage (row W23-S2) ends the invocation in error AFTER the returns and class days are written, so no returns or class day is lost; the lots days of that fire are not written and are retried the same way, and a backfill event closes a day by hand.

Neither branch moves a returns key. Neither moves "Data through". No served consumer reads the class table or the three tables today.

## After-read the apply will run

On the first fire after the apply, with the issuer reading S3 and the function's log:
1. **A1, the log.** Zero `CLASS_SKIPPED` and zero `LOTS_SKIPPED` lines, one `<day> class rows=<n> LANDED` per day and one `<day> <table> rows=<n> LANDED` per table-day (realized may read `rows=0 NOT_WRITTEN`). Else Branch B: name the reason, and the function's duration and memory from its REPORT line against 900 s and 2048 MB (kit reference: 665.0 s and 1669.7 MB on 2026-10-06, 652.21 s and 1668.9 MB on 2026-10-07; the CTO's stop line is 85%: 765 s and 1740.8 MB).
2. **A2, the activity identity.** Pick one account-day with `coverage` MEASURED in `.../gold/account_activity_daily/date=<T-1>/data.parquet`; print `beginning_value + contributions - withdrawals + realized + unrealized_change + income - ending_value`, its `identity_gap` and its `rounding_allowance`: the absolute gap is within the allowance. Print the day's coverage census from the manifest.
3. **A3, the keys.** For each of the three partitions print rows and distinct values of the declared `primary_key` (`org/standards/IRPT_DASHBD_ACCOUNT_*_CONTRACT.json`; the realized key is `(firm, account_id, business_date, lot_id, quantity, proceeds)`): equal. Print `basis_source` counts on the two lot tables: every value among CUSTODIAN, IN_KIND_TRANSFER_VALUE, WASH_SALE_EXCLUDED_BASIS.
4. **A4, DELTA=0 on the served returns.** The `account_return_daily` partition for T-1 equals a local run of the round-25 handler (`git show 5ffd7b740d:infra/aws/lambda/investor-reporting/reporting-gold/handler.py`) for a named sample of accounts, row by row (this reads the effect of the `account_return_daily.py` re-pin as well).
5. **A5, the grant.** `get-role-policy` shows the write set is exactly the five gold prefixes with `s3:PutObject` only, the silver read statements list the six silver prefixes, and `dynamodb:GetItem` on `table/etf-classifications` is the only DynamoDB action.
6. **A6, the class release.** The round-22 after-read A2 (the class identity) and A3 (the unclassified share) stand as written in `NEVER_WIDEN_PACKET_ACCOUNT_CLASS_DAILY_RELEASE.md`, read from the class partition of the same fire.
7. **A7, the pins.** `get-function` CodeSha256 equals the rebuilt artifact's, and the issuer prints, for each of the 18 rows of the pins table, the `sha256` of the member inside the built zip: equal to the table's value (no member older than the signed list).

A1 to A7 are read, not waited on: an ad-hoc invoke with `dry_run` computes and prints without writing and may be used for QA, and for the Lambda sizing in Unmeasured, before the organic fire; it writes none of the five tables.

## The build's file list (every file the bundle carries; sha256 at this branch's HEAD, equal to `3026d29bbb`)

`handler.py` is staged from the source directory; every other member is a pinned blob (the pins table above gives each pin; the lane re-reads these values at the drain commit). Rows marked CHANGED differ from R35's value.

| Member (`repo_path`) | Since `ec9c251de8` (R35's base) | sha256 at HEAD |
|---|---|---|
| `infra/aws/lambda/investor-reporting/reporting-gold/handler.py` | same | `18851ddab0d77743d25a0b6c157cafe35eaa5673d7db2d83817b0abe525a2b34` |
| `data/assets/scripts/gold/irpt_reporting/account_return_daily.py` | same | `9935f5c7bcd7bd9ca071ae7b7a672a49a5d96fcb0cd7d558c9fc3bc49157fc19` |
| `data/assets/scripts/gold/irpt_reporting/account_class_daily.py` | same | `2def366fb5dea1abce76a08ca6e1c29ab8713127a47764695c9bd140178edc11` |
| `data/assets/scripts/gold/irpt_reporting/account_activity_lots.py` | CHANGED | `63f9e20f1735f4f0003b41713ca1820d62b6ed716c047328a04458b854c8ea6c` |
| `data/assets/scripts/gold/irpt_reporting/sources.json` | same | `5dd1f367d4d0f87aea6f15c077b2eb064b27bb6f5d74d1d572e4d7d6d16d76b2` |
| `org/tier1_exec/4.0.0_SA_CRO/deliverables/SCHWAB_TRANSACTION_CODE_CLASSIFICATION_20260811.json` | same | `8b803eecfd1417b1bd4c10a9e269a6a27e295ecb6304d90c288ec596b6ce0bae` |
| `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.4.0_DS_ClientPlatform~S/MEASURED_THRESHOLDS_R1.json` (packaged as `data/assets/scripts/gold/irpt_reporting/MEASURED_THRESHOLDS_R1.json`) | same | `551920f0c364490d87cac260d5df2ad601ff7dac44f56043176065a3c3c2d177` |
| `data/assets/scripts/lib/stream_parquet.py` | same | `2e3762e14b486ddb8c21a3025f0c62c501b2bd8b8b9bf5b1801a675802cf7437` |
| `lib/opal_naming.py` | same | `9d301e1c0fe61a66384c9fdab5380b536767f3ef3927bb8414c0b93305ba9296` |
| `lib/trading_calendar.py` | same | `8ec8e43def5854f67a0dadcef7c735906f44aa07ae5916b2fc62c4c81ca9a3a8` |
| `org/standards/NAMING_SCHEMA.json` | same | `00e744c8eabf0cfd5e6c2af413788cea13cb92eb50b11e5dc2e49596f2dd3e60` |
| `infra/logic/registry/systems.json` | same | `70cfd07e4555880ce96d084d7be0ea9e76b76c1f0f3666295ed0ac95f4569053` |
| `infra/logic/registry/scopes.json` | CHANGED | `13947f7f2b35c6c9ed403e6c21ba87d1abd00156c06a50dcd37cdd69dedeaade` |
| `infra/logic/registry/tiers.json` | same | `d3d51e30150a4baefd9405ddfe9adfa1740e084dfb1857c8fcb0e87a3c1188f3` |
| `infra/logic/registry/exemptions.json` | same | `8c5ba7257f417fe6e94bc3d84d7dda5d528116de2eb2c0b205c198d07c51a186` |
| `infra/logic/registry/remediations.json` | same | `49cde7fb7a8d48cf1f9646df4ed66fa230b3863919e229b3a90d4f86866f6353` |
| `infra/logic/registry/resources.json` | same | `1f98affd0eb8ed0c7fe159f742e5e708ea3230191c8ca42daf6b40144e17a7b6` |
| `infra/logic/registry/reporting_policies.json` | same | `dc0eccfde86127327934064eec85ecd33f71ea56f2594dd3f032f78d0ca47e17` |
| `infra/aws/lambda/v2_portal/_shared/etf_classifications_dynamodb.py` (packaged flat as `etf_classifications_dynamodb.py`) | same | `92b64d97d69bfee9bc2d4b06fe13c8719a30856fc70f8588e1b29289f89afccc` |

The issuer writes `infra/aws/lambda/ci/lambda-source-map.json` at the apply (this cell does not edit it). `account_activity_lots.py` imports only `account_return_daily`, `trading_calendar`, pandas, pyarrow and the standard library (and `gc`); `sample_accounts()` imports `handler` lazily and is reached only by the producer's own `--local` CLI.

## Unmeasured, stated

- **Duration and memory on the Lambda itself (row W23-S2, ARMED, disarm owner `2.0.0_SA_COO~D2`).** The kit runs are dell2's: 665.0 s / 1669.7 MB (2026-10-06) and 652.21 s / 1668.9 MB (2026-10-07) for 7,604 accounts, in batches of 1000, against the function's 900 s and 2048 MB and the CTO's 85% stop line. A 2048 MB function has its own CPU share and reports resident memory, not Windows working set; the margin to the memory limit is 378.3 MB and to the stop line 71.1 MB. The lots stage runs last, so a timeout or kill cannot lose a returns or class day; it would stop that fire's lots days and error the invocation. The issuer reads the Lambda's REPORT line from a `dry_run` invoke before the organic fire.
- **The 290 s wall difference** between R35's 2026-10-06 run (374.93 s) and DB-b-73's (665.0 s): measured, not explained here.
- **The silver bucket's own policy on the three added prefixes** (row W23-S1): the role grant is derived; the bucket's admission is not read here.
- **DB-b-43's test on pandas 2.2.3** (row W46-S1): the file as written forces the pandas-3 string mode and fails 0 of 4 on the kit, recorded in R35 as `forced_option_on`; in the served mode it passes 4 of 4. A property of the test, not of the producer; not re-run by DB-b-73 or this cell.
- **The live function, role and plan.** This cell reads the repo and S3 object listings, not the live Lambda, its role or a Terraform plan; the claim that the live state is the pre-release state is the record of `310380d8cd`.
- **`origin/CLOUD` vintage.** Pins are resolved against the local remote-tracking ref (`3195077755`); a CLOUD commit after it that touches a member is not seen. The lane re-reads each pin's sha256 against HEAD's bytes at the apply.

## CTO half -- 1.0.0_SA_CTO

UNSIGNED. Signing means: the blast radius above is the whole act -- FIVE gold write prefixes (returns byte-identical, class from round 22, and the activity, realized and unrealized prefixes new), three more silver READ prefixes of the custody master the role already reads, one DynamoDB table read by key; against R35 the only change is that the realized key gains `proceeds`, so a realized partition with a wash-sale split pair lands instead of skipping the day, and against the LIVE (rolled-back) function the radius widens by exactly R35's list and no more; both branches are read from the rules; the writers are counted (one rule per new prefix, two paths); the rollback is per key; the preconditions (the 18 pins at HEAD's bytes, the Terraform root restored to the `efeb21df71` bytes) are the deploying lane's and the issuer's and are met before the apply; a class or lots day that fails is retried by the next fire; the S32 read of R35 stands; and the sizing (both kit days under the 85% line on memory and time, with 71.1 MB and 100.0 s of margin to the line at the worse day) is accepted for the first fire with the `dry_run` read named in Unmeasured. **On both halves here signed, the R35 pair (`NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE_R35.md`), the round-22 class pair and the round-26 pair are superseded by this packet.**

## COO half -- 2.0.0_SA_COO~D2

UNSIGNED. Signing means: the issuer will have the deploying lane set the 18 pins printed above and restore the three Terraform files (preconditions 1 and 2), rebuild the artifact, read the plan against the expected `0 to add, 3 to change, 0 to destroy` and STOP on any difference (precondition 3), size the lots stage with a `dry_run` invoke against the 85% line (precondition 4), apply once from the saved plan, and run A1 to A7 on the first fire. A skipped class or lots day is retried by the next fire's catch-up, so no standing backfill is owed; the lots tables' history is a backfill the issuer orders separately. **On both halves here signed, the R35 pair, the round-22 class pair and the round-26 pair are superseded by this packet.**
