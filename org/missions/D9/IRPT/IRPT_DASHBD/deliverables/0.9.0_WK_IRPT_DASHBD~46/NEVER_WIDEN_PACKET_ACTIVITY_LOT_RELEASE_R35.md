# Never-widen sign-off packet, RE-CUT at HEAD (round 35) -- the reporting-gold function also writes `account_activity_daily`, `account_lot_realized` and `account_lot_unrealized_daily`, and carries the unapplied `account_class_daily` release (IRPT_DASHBD DB-b-69; re-cut of the round-26 packet `deliverables/0.9.0_WK_IRPT_DASHBD~23/NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE.md` @efeb21df71)

Author `0.9.0_WK_IRPT_DASHBD~46` for `2.0.0_SA_COO~D2`, 2026-10-09. Cell: `DB-b-69`. Halves owed: `1.0.0_SA_CTO` and `2.0.0_SA_COO~D2`, both UNSIGNED.
Status: RE-CUT AND MEASURED LOCALLY; NOTHING APPLIED. No `terraform` command, no `aws lambda` call, no S3 write, no source-map or pin edit and
no network call was made by this cell. The apply and the first fire are the issuer's act under the two signed halves. This packet covers the WHOLE
next apply of the root: the `account_class_daily` release already in the handler and the role (round 22, cell DB-b-34) AND the three tables below.
Branch `wk-IRPT_DASHBD-46`, cut from `box/dell2` @`ec9c251de8`. This cell edits no member of the file list: the sha256 values below are the bytes of
each member at that base and at this branch's HEAD, and they are what the lane re-reads at the drain commit.

## What changed since the round-26 packet (`efeb21df71` .. `ec9c251de8`)

Measured by `git diff efeb21df71..HEAD` on the 19 file-list members, the Terraform root and the source map. 6 of the 19 members differ; 13 are
byte-equal; the Terraform root `infra/aws/terraform/investor-reporting/reporting-gold/` has 0 changed files, so the expected plan below stands
unchanged; the source map entry `irpt-49f-reporting-gold-lambda` still names `last_deployed_commit` `829e46ed7f` (2026-10-05T00:12:52Z), so nothing was
deployed from this root since (the map is the repo's record; the live function is not read by this cell).

| Member | Commits | What it changes in behaviour | Widens the radius? |
|---|---|---|---|
| `infra/aws/lambda/investor-reporting/reporting-gold/handler.py` | 1 (`440f89bb56`, DB-b-48) | `lots_days()` takes `batch_size` and calls `aal.compute_local_batched(...)` instead of `aal.compute_local(...)`; `None` means the producer's `DEFAULT_BATCH_SIZE` (1000). `local()` and the CLI take `--batch-size`, a `--local`-only option. The scheduled fire and a backfill event pass no batch size, so they run the lots stage in batches of 1000. Output is the same three tables over the same accounts; only the stage's peak memory changes. | No. No new read, write or action. |
| `data/assets/scripts/gold/irpt_reporting/account_activity_lots.py` | 4 (`18105e4a07` DB-b-47, `440f89bb56` DB-b-48, `1a922d8734` DB-b-52 set the default batch to 2000, `18a7702338` DB-b-55 set it back to 1000) | (1) The `account_lot_realized` primary key is `(firm, account_id, business_date, lot_id, quantity)`: on 2026-10-06 87 realized lot ids repeat over 175 rows in 36 accounts, none identical in every column, and the round-26 producer REFUSED the whole lots day on the first repeat. The producer now refuses only a row identical in every column, or one that repeats the whole key. (2) `compute_local_batched` runs the accounts in sorted disjoint batches (default 1000), scans the balance history once for all of them, and sorts every table by `(business_date, account_id, lot_id, quantity)` so batched and unbatched runs give the same bytes. (3) `DEFAULT_BATCH_SIZE` is 1000 (set to 2000 by DB-b-52, back to 1000 by DB-b-55 on the p95 of 5 runs). The three table names, schemas and S3 addresses are unchanged. | No new prefix, action or role statement. ONE data-level difference, stated here and not hidden: the `account_lot_realized` partition for a day with a repeated lot id now LANDS (2,523 rows on 2026-10-06) where the round-26 function would have logged `LOTS_SKIPPED` for the day and written none of the three tables. |
| `lib/opal_naming.py` | 2 (`b419746eca` BF-q-4, `e15671f611` FWD-9 hookup) | A second naming-census switch `FUNCTION_LITERAL_WIDE` and a `census --all-roots` CLI option (LGIC_BLANKFIX BF-q-4, FWD-9). Both are in the census/gate tooling path; `address()` and `name()` return the same strings (re-printed below). | No. |
| `infra/logic/registry/systems.json` | 2 (`530ef17ff8`, plus a merge) | A new VENDOR row `yahoo` (MDPF demand queue). Read by no part of this function's data path. | No. |
| `infra/logic/registry/exemptions.json` | 2 (`173f98f24b`, `2a809c975e`) | The three `cloudops-dell1-agent-user` fence rows (49financial, inflection, cottonwood buckets) move from a scoped read of the platinum holdings prefix to a FULL admission, under Andrew's word of 2026-10-08 and a signed pair (NFRA_CTLPLN). It is the naming registry's record of a bucket-policy exemption; this Lambda's role has no statement about that principal and the exemption is not read by the handler's code path. | No change to THIS function's grants. (The exemption row itself is another project's widening, signed there.) |
| `infra/logic/registry/reporting_policies.json` | 2 (`8530114ff9`, `0c35aeeaa8`) | A new policy `irpt-custody-reporting` (revision `irpt-custody-x10-v1`, ACTIVE, family `CUSTODY_REPORT`, table `custody_reports`, platinum). `irpt-x10-v1` is byte-unchanged. This function writes no `custody_reports` key. | No. |

Packaged-but-unchanged for this release: `account_return_daily.py` (HEAD equals the round-26 sha256; the deployed pin `bc50d5711e` differs from it by the 4 lines of `ba544b6064`, read by the
returns comparison below), `account_class_daily.py`, `sources.json`, the classification table, the thresholds, `stream_parquet.py`, `trading_calendar.py`, `NAMING_SCHEMA.json`, `scopes.json`, `tiers.json`, `remediations.json`, `resources.json`, `etf_classifications_dynamodb.py`.

**Does the blast radius widen? No: the set of prefixes written, the set of prefixes read, the actions and the DynamoDB table are exactly the round-26 packet's.** The one thing that
moves is the CONTENT of a table the packet already names (the realized partition lands on a day it would have been skipped). `org/standards/IRPT_DASHBD_ACCOUNT_LOT_REALIZED_CONTRACT.json` (not a bundle member)
carries the revised key; after-read A3 below reads it.

## The three conditions, with the values measured by this cell

Values come from `S32_READ_E1.json` in this folder, each printed by the process that produced it (kit runtime: Python 3.12.10, pandas 2.2.3, numpy 1.26.4, pyarrow 14.0.2; the
kit is the zip with sha256 `c76af678143a5f92c4a9638a8ac25e47d2f2c294a014cd3a457af96c55ff17bf`, installed offline into a venv; boto3, psutil and pytest side-loaded from dell2's own
site-packages, rows W44-S1 and W46-S2; tested version: dell2's default Python 3.14.7, pandas 3.0.6, numpy 2.5.3, pyarrow 25.0.1).

**S31 -- the extended handler over the whole population for one trading day, wall and peak against 900 s / 2048 MB.** MEASURED on the kit, 2026-10-06, default batch (1000; 8 batches of 1000, 1000, 1000, 1000, 1000, 1000, 1000, 604), `--local`:

| Item | Value | Limit |
|---|---|---|
| Population / accounts run | 7,604 / 7,604 | |
| Lots stage completed | True | |
| Lots peak (process peak working set, Windows) | 1672.3 MB | 2048 MB |
| Lots wall / total wall | 264.36 s / 374.93 s | 900 s |
| Returns / class stage peak | 292.4 MB / 320.8 MB | |
| Rows | returns 6,888, class 24,992, activity 6,888, realized 2,523, unrealized 568,009 | |

Round 34 (DB-b-67) measured the same run at 1,500.7 MB and 447.07 s; this cell's run is 1672.3 MB and 374.93 s: the run-to-run spread of the peak is 171.6 MB and both fit. The peak is a
Windows working set on dell2, not the Lambda's `Max Memory Used`, and dell2's cores are not the Lambda's: the Lambda's own REPORT line is read by the `dry_run` of precondition 3.

**S32 -- the pandas 2.2.3 read.** Three arms, all measured:
- `classify_and_sum`, kit against tested version: fixture = the custodian `fact_trn` partitions of 2026-10-06, 2026-10-05 and 2026-10-02, read from S3 through the producer's own `FlowCache`, classified whole and filtered to the 7,604-account set. `equal: true`; `differences: 0` (per-account entries compared across the 3 days: flow 328, income 10738, unvalued 14, cash_unknown 1, plus the census and the partition-absent flag). Floats are compared with `==`, no tolerance; a negative control (one value moved by 0.01) is reported as a difference.
- The returns table for 2026-10-06 (6,888 rows, 7,604 accounts) built on the kit by the HEAD handler's own `--local` compute, once with `account_return_daily.py` executed from `git show bc50d5711e:<path>` (the deployed pin) and once from HEAD: sha256 old pin `20ec963f5c8c1976ff589c255e9a081a99e7e6103bd1b533527ed04c373ecf14`, sha256 HEAD `20ec963f5c8c1976ff589c255e9a081a99e7e6103bd1b533527ed04c373ecf14`, `identical: true`. The two source files differ (`cb38fe16...` against `9935f5c7...`), so two different codes produced one table.
- DB-b-43's own test on the kit: **0 passed, 4 failed** (on the tested version: 4 passed, 0 failed). The four failures are all `TypeError: expected bytes, re.Pattern found`, raised where pandas 2.2.3's experimental pyarrow-string dtype, which the test switches ON through `future.infer_string`, hands a compiled regex to pyarrow in `str.contains`. The served runtime never enters that mode (the producer holds `future.infer_string` OFF at its entry; the full run's log prints `future.infer_string = False (served behaviour in force: True)`). The same four test bodies with the option left at the kit's default give 4 passed, 0 failed. **This is not a pass of DB-b-43's test on the kit and this packet does not call it one**: row IRPT_DASHBD-W46-S1 (BLOCKING, INERT) holds it, and the CTO decides whether the option-off run plus the two equalities above are the S32 read or the test is amended for pandas below 3. The two equalities above are what this cell can show about the producer on 2.2.3; the failing arm is a property of the test.

**S33 -- no refusal on the kit run.** One full kit run (the S31 run) over 7,604 accounts. The log has 56 lines; the lines matching `REFUSED`, `LOTS_SKIPPED` or `CLASS_SKIPPED`:

```
refusals: 0
```

`s33_holds: true` (S33 holds iff `refusals` is 0).

## Root

`infra/aws/terraform/investor-reporting/reporting-gold` -- state the Terraform state bucket's key `investor-reporting/reporting-gold/tfstate` (the bucket name carries the AWS account id and is not typed here).
No other root is read for a write, planned or applied by this act.

## Preconditions the signed act does not cover

1. **PRECONDITION OF THE APPLY -- the bundle pins (the deploying lane's act, rule 13; a pin names the commit that carries the files
   on CLOUD, which does not exist until this branch drains; `lambda-source-map.json` is outside this cell's grant).** The bundle is pinned in
   `infra/aws/lambda/ci/lambda-source-map.json`, entry `irpt-49f-reporting-gold-lambda`. At HEAD the entry lists 16 `files` and 15 `staged_from` rows, the same as the round-26 packet found. Before the
   apply, the lane sets these `staged_from` entries (and the matching `files` members), each `{repo_path, pin, packaged_as, sha256}`,
   `pin` = the drain commit that carries the file on CLOUD, `sha256` = `git show <drain-commit>:<repo_path> | sha256sum`:

   | # | repo path | `packaged_as` | note |
   |---|---|---|---|
   | 0 | `data/assets/scripts/gold/irpt_reporting/account_return_daily.py` | same path | the existing entry RE-PINNED: today `bc50d5711e`, sha256 `cb38fe16...4529`; HEAD's file differs by the 4 lines of `ba544b6064`. The returns table built from the two on the kit is byte-identical (S32 above) |
   | 1 | `data/assets/scripts/gold/irpt_reporting/account_class_daily.py` | same path | new member (round 22) |
   | 2 | `infra/aws/lambda/v2_portal/_shared/etf_classifications_dynamodb.py` | `etf_classifications_dynamodb.py` | new member, the class client, packaged flat (round 22) |
   | 3 | `data/assets/scripts/gold/irpt_reporting/sources.json` | same path | the existing entry RE-PINNED: the declaration changed twice (the trade-leg tokens, round 22; the `lot_source` object, DB-b-41); today's entry pins `bc50d5711e` |
   | 4 | `data/assets/scripts/gold/irpt_reporting/account_activity_lots.py` | same path | new member (DB-b-41; its HEAD bytes carry DB-b-47 and DB-b-48) |

   Pins 1 to 4 land together: the activity producer reads the lot tables' names from the declaration, so a re-pinned `sources.json`
   without pin 4 is harmless (the handler's import is guarded) and pin 4 without pin 3 is NOT a supported pairing (the producer refuses
   by name: `REFUSED: the source declaration carries no 'lot_source' object`, and the lots day is logged `LOTS_SKIPPED`). The HEAD `handler.py` calls
   `compute_local_batched`, which only the HEAD `account_activity_lots.py` has, so the handler and pin 4 also land together: a HEAD handler with a round-26 producer would log `LOTS_SKIPPED` with an `AttributeError` on every day.
   The lane then rebuilds `investor-reporting/irpt-reporting-gold-lambda.zip`. The values (drain commit, sha256 values) are printed by the lane at the
   apply, not predicted here. Without the pins the function runs as it does today (Branch B).
2. **The plan.** The root has 0 changed files since the round-26 packet, so its expected counts stand. The issuer reads the plan before the signed halves are used and STOPS if it differs from the expected counts (this cell does not run `terraform`).
3. **Sizing on the Lambda.** The kit run above fits the limits on dell2 (S31). The Lambda's own duration and `Max Memory Used` are read by a `dry_run` invoke before the organic fire (see Unmeasured); row W23-S2 stays with its disarm owner `2.0.0_SA_COO~D2` until that read.

## Names and addresses (builder output, printed)

Printed by `lib/opal_naming.py` at HEAD (`address()` and `name()` called directly), with the firm from the declaration's `registry_key`. Identical to the round-26 packet's lines. Nothing below is typed by hand:

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

The Terraform side mirrors each table name ONCE in `locals.tf` (`irpt_rg_gold_table_class`, `irpt_rg_gold_table_activity`,
`irpt_rg_gold_table_realized`, `irpt_rg_gold_table_unrealized`), each cited to the producer's constant where it lives. The custodian's lot
tables are not typed there either: the silver read prefixes are derived from the declaration's `lot_source`. Derived sets (from `sources.json` and `scopes.json`, unchanged since the round-26 packet):

```
silver READ prefixes  (bucket opal-data-assets): schwab/<custody master>/silver/{dim_position,dim_balance,fact_trn,fact_rld,fact_uln,fact_ult}/
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

The policy document changes as follows (the round-22 class changes and DB-b-41's; nothing from rounds 28 to 34 touches it):
- write set `irpt_rg_gold_write_arns` becomes the returns, class, activity, realized and unrealized prefixes (`s3:PutObject` only);
- the gold read set and its ListBucket prefix pattern become the six gold prefixes;
- the silver read set and its ListBucket prefix pattern gain the three custodian lot-table prefixes `fact_rld`, `fact_uln`, `fact_ult` (`fact_trn` is the transactions prefix it already holds);
- the statement `ReadTheClassTableByKeyOnly` grants `dynamodb:GetItem` on `arn:aws:dynamodb:us-east-1:<account>:table/etf-classifications` and nothing else (round 22).

## Blast radius, by the producers' own rules

**What the act may touch.**
- THREE new gold prefixes, `.../gold/account_activity_daily/`, `.../gold/account_lot_realized/`, `.../gold/account_lot_unrealized_daily/` (two objects per table-day: `date=<D>/data.parquet` and `date=<D>/manifest.json`; a table with no row on a day writes no object for it). They hold no object today. ONE new prefix from round 22, `.../gold/account_class_daily/`, also holds none.
- The returns prefix `.../gold/account_return_daily/` is written exactly as before, byte-identically: the round-25 and round-26 handlers produced the same returns parquet for 20 accounts (sha256 `8d18f775...073e` on both, `RELEASE_LOCAL_RUN.json`), and this cell re-measured it for the WHOLE population: the returns table of 2026-10-06 (7,604 accounts, 6,888 rows) built from the deployed pin `bc50d5711e` and from HEAD is byte-identical on the kit (S32). The scheduled fire writes only days AFTER the newest landed returns day, so it rewrites no landed returns key. A manual backfill event can rewrite landed returns, class and lot days, to the same bytes.
- DynamoDB: `GetItem` on `etf-classifications` (round 22), one item per distinct held identifier. No Scan, Query, index, write or Delete.
- S3 reads: the role's silver read set gains three prefixes of the SAME bucket and custody master it already reads (`opal-data-assets`); the gold read set gains the class, activity, realized and unrealized prefixes, which the handler lists for each table's newest landed day. Whether the silver bucket's own policy admits the role on the three added prefixes is not read by this cell (row W23-S1); a refusal is `AccessDenied` on the first lot read and lands as Branch B.

**What the act may not touch.** `.../gold/dim_return_method/` (another cell's served row; not in the write set); the holdings gold (read only); the silver prefixes (read only); any other firm's bucket or prefix; the platinum prefix and the publisher; any other Lambda, role or table; the schedule. The policy carries no `s3:Delete*`, no write to any table, no `dynamodb:Scan`, and no write grant beyond the five gold prefixes above.

**Writers of the property, counted.** Each of `account_activity_daily/`, `account_lot_realized/`, `account_lot_unrealized_daily/` has ONE writing rule, `account_activity_lots.emit_day`, called only from `handler.emit_lots`, reached by TWO paths: the scheduled fire (`catch_up_lots`) and an explicit backfill invocation by a seat (`run_backfill`, same code). The batching of round 28 changed how `compute_local_batched` assembles the rows handed to `emit_day`, not who writes: the producer's own `--local` CLI has no upload path (a test asserts `put_object`, `upload_file`, `stream_to_parquet` and `s3://` occur only inside `emit_day`). `account_class_daily/` keeps its one rule (`emit_class_day` from `handler.emit_classes`, two paths). `account_return_daily/` keeps its one handler writer. N = 1 rule per new property.

**The manual path.** The Lambda event can carry `accounts`, `dry_run`, or `backfill` (`start`, `end`, at most 25 trading days, only days at or before the newest landed returns day, `accounts` "population" or a list). A backfill also rewrites the three tables for the same days. `dry_run` computes and prints and writes none of the five. It creates no state the schedule cannot reach: the days written are the returns days, and a backfill never extends the returns table. The handler's `--batch-size` exists only on the `--local` CLI, which refuses any upload (`REFUSED: the CLI is --local only`), so it is not a path to the five prefixes.

## Rollback, per key

- **Lambda.** The prior function is the artifact recorded in the source map at `last_deployed_commit` `829e46ed7f` (2026-10-05T00:12:52Z): `investor-reporting/irpt-reporting-gold-lambda.zip`, `deployed_code_sha256` `Mex71Y5gk9RYE9q885knj3Ph12xV2Y9eVqMl3uJ1Z44=`. The issuer records the live CodeSha256 and the artifact object's S3 version id before the apply (not read by this cell). Rollback is the Terraform route only (`aws lambda update-function-code` is barred): re-pin the prior artifact version in the source map and run a targeted `safe-apply`.
- **Role policy and role description.** The applied state is `iam.tf`/`locals.tf` at `4c34d86104`; those files are unchanged since `efeb21df71`. Reverting `efeb21df71` restores the round-22 policy (returns + class write set); reverting round 22's files too restores `4c34d86104`. Run the same targeted apply. The statements removed are the activity, realized and unrealized writes and reads, the lot-table silver reads, and (to `4c34d86104`) the class read, write and the DynamoDB `GetItem`.
- **Each new gold prefix** (`account_activity_daily`, `account_lot_realized`, `account_lot_unrealized_daily`, `account_class_daily`). Each is new, so there is no prior version of any key. Rollback is to delete the objects under the prefix AFTER the issuer's word (an S3 delete is not this packet's act and is not in the role's grant). Each fire adds two keys per table-day, listed in the fire's log line `<day> <table> rows=<n> LANDED`.
- **Returns prefix.** A day written by the extended function is byte-equal to what the prior function writes for it, so no key needs restoring. If a returns key is ever suspect, the bucket is versioned: restore the prior version by `copy-object` from its version id (read at that moment).

## BRANCH A

**The outcome, read from the rule at signing.** Each fire computes the days after the newest landed returns day through T-1, writes those days of `account_return_daily` FIRST (unchanged code path), then the same days of `account_class_daily`, then the same days of the three tables. The tables are the activity producer's own figures (`compute_local_batched`, batches of 1000, the same rows as one unbatched call) and are not recomputed in the handler. Within a day the two lot tables are written first and `account_activity_daily` LAST, so the activity table's newest landed day is the marker that the whole day landed. Measured over the whole population on the kit for 2026-10-06: 6,888 returns rows, 24,992 class rows, 6,888 activity rows, 2,523 realized-lot rows and 568,009 open-lot rows, and a lots stage with no refusal. (The round-26 packet's sample figures, 20 accounts, stand as the identity and window-grain evidence: 18 activity rows MEASURED, 58 of 91 account-windows within one cent and the rest within the 0.05 tolerance of the activity contract.)

The first fire after the apply (a trading morning, 07:41 ET) lands T-1 of `account_return_daily` (and any backlog up to 10 days), the same days of `account_class_daily`, and the same days of `account_activity_daily`, `account_lot_unrealized_daily` and, on a day that closes a lot, `account_lot_realized`; each activity row carries `coverage` MEASURED where its gap is within `rounding_allowance` and GAP_ABOVE_ALLOWANCE where it is not (a real difference, carried, never plugged). The log carries `<day> class rows=<n> LANDED` and one `<day> <table> rows=<n> LANDED` per table-day, no `CLASS_SKIPPED` and no `LOTS_SKIPPED`. A realized table with no row on a day prints `<table> rows=0 NOT_WRITTEN`; that is not a failure. The first fire never pulls history: the lots tables' history lands only by backfill events (25 trading days a chunk).

## BRANCH B

A day's class or lots stage is refused by name and the returns table is still written (class and lots failures are independent of each other). The log carries `CLASS_SKIPPED <day> <reason>` and/or `LOTS_SKIPPED <day> <reason>`, and the function returns `class_failed` / `lots_failed`. Reasons that can occur for the lots stage: the bundle pins are absent or mismatched (`account_activity_lots not importable`, or an `AttributeError` for `compute_local_batched` if the handler and the producer are pinned from different commits), the declaration lacks `lot_source` (`REFUSED: ... no 'lot_source' object`), `AccessDenied` on a silver lot prefix or a gold prefix (the role or the bucket policy), a partition unreadable, a producer refusal by name (a row identical in every column to another, or a repeat of the realized key `(firm, account_id, business_date, lot_id, quantity)`, a holding-term flag outside the declared map), or no activity row for the day. The reasons for the class stage are those of the round-22 packet. No object is written for a refused day's activity table; if a lot table was written before the refusal the activity marker is not, and the next fire rewrites the same bytes. **The next fire retries it:** on each scheduled fire the handler lists the three lots prefixes and emits every trading day after the ACTIVITY table's own newest day through the newest returns day just written (at most 10 days per fire, oldest first); a day that still fails is logged by name and the returns and class tables are never held. A timeout or out-of-memory kill in the lots stage (row W23-S2) ends the invocation in error AFTER the returns and class days are written, so no returns or class day is lost; the lots days of that fire are not written and are retried the same way, and a backfill event closes a day by hand.

Neither branch moves a returns key. Neither moves "Data through". No served consumer reads the class table or the three tables today.

## After-read the apply will run

On the first fire after the apply, with the issuer reading S3 and the function's log:
1. **A1, the log.** Zero `CLASS_SKIPPED` and zero `LOTS_SKIPPED` lines, one `<day> class rows=<n> LANDED` per day and one `<day> <table> rows=<n> LANDED` per table-day (realized may read `rows=0 NOT_WRITTEN`). Else Branch B: name the reason, and the function's duration and memory from its REPORT line against 900 s and 2048 MB (kit reference: 374.93 s, 1672.3 MB).
2. **A2, the activity identity.** Pick one account-day with `coverage` MEASURED in `.../gold/account_activity_daily/date=<T-1>/data.parquet`; print `beginning_value + contributions - withdrawals + realized + unrealized_change + income - ending_value`, its `identity_gap` and its `rounding_allowance`: the absolute gap is within the allowance. Print the day's coverage census from the manifest.
3. **A3, the keys.** For each of the three partitions print rows and distinct values of the declared `primary_key` (`org/standards/IRPT_DASHBD_ACCOUNT_*_CONTRACT.json`; the realized key is `(firm, account_id, business_date, lot_id, quantity)`): equal. Print `basis_source` counts on the two lot tables: every value among CUSTODIAN, IN_KIND_TRANSFER_VALUE, WASH_SALE_EXCLUDED_BASIS.
4. **A4, DELTA=0 on the served returns.** The `account_return_daily` partition for T-1 equals a local run of the round-25 handler (`git show 5ffd7b740d:infra/aws/lambda/investor-reporting/reporting-gold/handler.py`) for a named sample of accounts, row by row (this reads the effect of pin 0 as well; the whole-population old-pin against HEAD equality for 2026-10-06 is already in S32).
5. **A5, the grant.** `get-role-policy` shows the write set is exactly the five gold prefixes with `s3:PutObject` only, the silver read statements list the six silver prefixes, and `dynamodb:GetItem` on `table/etf-classifications` is the only DynamoDB action.
6. **A6, the class release.** The round-22 after-read A2 (the class identity) and A3 (the unclassified share) stand as written in `NEVER_WIDEN_PACKET_ACCOUNT_CLASS_DAILY_RELEASE.md`, read from the class partition of the same fire.

A1 to A6 are read, not waited on: an ad-hoc invoke with `dry_run` computes and prints without writing and may be used for QA, and for the Lambda sizing in Unmeasured, before the organic fire; it writes none of the five tables.

## The build's file list (every file the bundle carries; sha256 at this branch's HEAD, equal to `ec9c251de8`)

`handler.py` is staged from the source directory; every other member is a pinned blob (the lane sets the pins and re-reads these values at the drain commit). Rows marked CHANGED differ from the round-26 packet's value.

| Member (`repo_path`) | Since `efeb21df71` | sha256 |
|---|---|---|
| `infra/aws/lambda/investor-reporting/reporting-gold/handler.py` | CHANGED | `18851ddab0d77743d25a0b6c157cafe35eaa5673d7db2d83817b0abe525a2b34` |
| `data/assets/scripts/gold/irpt_reporting/account_return_daily.py` | same | `9935f5c7bcd7bd9ca071ae7b7a672a49a5d96fcb0cd7d558c9fc3bc49157fc19` |
| `data/assets/scripts/gold/irpt_reporting/account_class_daily.py` | same | `2def366fb5dea1abce76a08ca6e1c29ab8713127a47764695c9bd140178edc11` |
| `data/assets/scripts/gold/irpt_reporting/account_activity_lots.py` | CHANGED | `4f3eff0b0959d8be409f78a6d6c8583dc766317da7b3bf7eed2868a4a52be457` |
| `data/assets/scripts/gold/irpt_reporting/sources.json` | same | `5dd1f367d4d0f87aea6f15c077b2eb064b27bb6f5d74d1d572e4d7d6d16d76b2` |
| `org/tier1_exec/4.0.0_SA_CRO/deliverables/SCHWAB_TRANSACTION_CODE_CLASSIFICATION_20260811.json` | same | `8b803eecfd1417b1bd4c10a9e269a6a27e295ecb6304d90c288ec596b6ce0bae` |
| `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.4.0_DS_ClientPlatform~S/MEASURED_THRESHOLDS_R1.json` (packaged as `data/assets/scripts/gold/irpt_reporting/MEASURED_THRESHOLDS_R1.json`) | same | `551920f0c364490d87cac260d5df2ad601ff7dac44f56043176065a3c3c2d177` |
| `data/assets/scripts/lib/stream_parquet.py` | same | `2e3762e14b486ddb8c21a3025f0c62c501b2bd8b8b9bf5b1801a675802cf7437` |
| `lib/opal_naming.py` | CHANGED | `9d301e1c0fe61a66384c9fdab5380b536767f3ef3927bb8414c0b93305ba9296` |
| `lib/trading_calendar.py` | same | `8ec8e43def5854f67a0dadcef7c735906f44aa07ae5916b2fc62c4c81ca9a3a8` |
| `org/standards/NAMING_SCHEMA.json` | same | `00e744c8eabf0cfd5e6c2af413788cea13cb92eb50b11e5dc2e49596f2dd3e60` |
| `infra/logic/registry/systems.json` | CHANGED | `70cfd07e4555880ce96d084d7be0ea9e76b76c1f0f3666295ed0ac95f4569053` |
| `infra/logic/registry/scopes.json` | same | `8fcd28d3e2b339bda4d3cb12f860d9a06b7c7bb79d578a731fed4a9f37cb65d1` |
| `infra/logic/registry/tiers.json` | same | `d3d51e30150a4baefd9405ddfe9adfa1740e084dfb1857c8fcb0e87a3c1188f3` |
| `infra/logic/registry/exemptions.json` | CHANGED | `8c5ba7257f417fe6e94bc3d84d7dda5d528116de2eb2c0b205c198d07c51a186` |
| `infra/logic/registry/remediations.json` | same | `49cde7fb7a8d48cf1f9646df4ed66fa230b3863919e229b3a90d4f86866f6353` |
| `infra/logic/registry/resources.json` | same | `1f98affd0eb8ed0c7fe159f742e5e708ea3230191c8ca42daf6b40144e17a7b6` |
| `infra/logic/registry/reporting_policies.json` | CHANGED | `dc0eccfde86127327934064eec85ecd33f71ea56f2594dd3f032f78d0ca47e17` |
| `infra/aws/lambda/v2_portal/_shared/etf_classifications_dynamodb.py` (packaged flat as `etf_classifications_dynamodb.py`) | same | `92b64d97d69bfee9bc2d4b06fe13c8719a30856fc70f8588e1b29289f89afccc` |

The issuer writes `infra/aws/lambda/ci/lambda-source-map.json` at the apply (this cell does not edit it). `account_activity_lots.py` imports only `account_return_daily`, `trading_calendar`, pandas, pyarrow and the standard library (and `gc`, added by DB-b-48); `sample_accounts()` imports `handler` lazily and is reached only by the producer's own `--local` CLI.

## Unmeasured, stated

- **Duration and memory on the Lambda itself (row W23-S2, ARMED, disarm owner `2.0.0_SA_COO~D2`).** The kit run is dell2's: 374.93 s and 1672.3 MB peak working set for 7,604 accounts, in batches of 1000, against the function's 900 s and 2048 MB. A 2048 MB function has its own CPU share and reports resident memory, not Windows working set; the margin to the memory limit is 375.7 MB. The lots stage runs last, so a timeout or kill cannot lose a returns or class day; it would stop that fire's lots days and error the invocation. The issuer reads the Lambda's REPORT line from a `dry_run` invoke before the organic fire.
- **The silver bucket's own policy on the three added prefixes** (row W23-S1): the role grant is derived; the bucket's admission is not read here.
- **DB-b-43's test on pandas 2.2.3** (row W46-S1): fails as written on the kit, as stated under S32; not resolved by this cell.
- **The live function and plan.** This cell reads the repo and S3, not the live Lambda, its role or a Terraform plan; the claim that nothing was deployed since `829e46ed7f` is the source map's record.

## CTO half -- 1.0.0_SA_CTO

UNSIGNED. Signing means: the blast radius above is the whole act -- FIVE gold write prefixes (returns byte-identical, class from round 22, and the activity, realized and unrealized prefixes new), three more silver READ prefixes of the custody master the role already reads, one DynamoDB table read by key; the only change since the round-26 packet is that a realized partition with repeated lot ids now lands instead of skipping the day; both branches are read from the rules; the writers are counted (one rule per new prefix, two paths); the rollback is per key; the preconditions are the deploying lane's and the issuer's and are met before the apply; a class or lots day that fails is retried by the next fire; the S32 arm of DB-b-43's test (failed on the kit, row W46-S1) is ruled on, and the sizing risk in Unmeasured is accepted for the first fire with the `dry_run` read named there. **On both halves here signed, the round-22 class pair (the CTO half and the COO half of `NEVER_WIDEN_PACKET_ACCOUNT_CLASS_DAILY_RELEASE.md`) and the round-26 pair of the superseded packet are superseded by this packet**, which carries that release in the same act.

## COO half -- 2.0.0_SA_COO~D2

UNSIGNED. Signing means: the issuer will have the deploying lane set pins 0 to 4 and rebuild the artifact (precondition 1), read the plan against the expected `0 to add, 3 to change, 0 to destroy` and STOP on any difference (precondition 2), size the lots stage with a `dry_run` invoke (precondition 3), apply once from the saved plan, and run A1 to A6 on the first fire. A skipped class or lots day is retried by the next fire's catch-up, so no standing backfill is owed; the lots tables' history is a backfill the issuer orders separately. **On both halves here signed, the round-22 class pair and the round-26 pair are superseded by this packet.**
