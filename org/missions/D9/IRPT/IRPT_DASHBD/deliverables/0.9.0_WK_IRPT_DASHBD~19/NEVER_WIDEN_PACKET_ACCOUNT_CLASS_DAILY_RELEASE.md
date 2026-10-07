# Never-widen sign-off packet -- the reporting-gold function also writes `account_class_daily` (IRPT_DASHBD DB-b-34; round-21 analysis E1, corrected by msg 463)

Author `0.9.0_WK_IRPT_DASHBD~19` for `2.0.0_SA_COO~D2`, 2026-10-07. Cell: `DB-b-34`. Halves owed: `1.0.0_SA_CTO` and `2.0.0_SA_COO~D2`.
Status: PREPARED AND PROVEN LOCALLY; NOTHING APPLIED. No `terraform` command, no `aws lambda` call and no S3 write was made by this
cell. The apply and the first fire are the issuer's act under the two signed halves.

## Preconditions the signed act does not cover

1. **PRECONDITION OF THE APPLY -- the bundle pins (row IRPT_DASHBD-W19-S2; ruled by `2.0.0_SA_COO~D2`, amendment 1
   @e765698322: not this cell's act, because a pin names the commit that carries the files on CLOUD, which does not exist until
   this branch drains; it is a release act, rule 13).** The bundle is pinned in `infra/aws/lambda/ci/lambda-source-map.json`, entry
   `irpt-49f-reporting-gold-lambda`. This cell does NOT edit that file. Before the apply, the DEPLOYING LANE sets exactly THREE
   `staged_from` entries there (and the matching `files` members), each `{repo_path, pin, packaged_as, sha256}`, `pin` = the drain
   commit that carries the files on CLOUD, `sha256` = `git show <drain-commit>:<repo_path> | sha256sum`:

   | # | `repo_path` | `packaged_as` | note |
   |---|---|---|---|
   | 1 | `data/assets/scripts/gold/irpt_reporting/account_class_daily.py` | `data/assets/scripts/gold/irpt_reporting/account_class_daily.py` | new member |
   | 2 | `infra/aws/lambda/v2_portal/_shared/etf_classifications_dynamodb.py` | `etf_classifications_dynamodb.py` | the class client, packaged flat |
   | 3 | `data/assets/scripts/gold/irpt_reporting/sources.json` | `data/assets/scripts/gold/irpt_reporting/sources.json` | the existing entry RE-PINNED: the declaration changed (trade-leg tokens moved in); today's entry pins `bc50d5711e`, sha256 `7ff90fef...1e34`, which is the BASE declaration |

   It does NOT add `_shared/etf_classification.py`. The deploying lane then rebuilds the artifact
   `investor-reporting/irpt-reporting-gold-lambda.zip`. The values (drain commit, three sha256) are not known to this cell and are
   printed by the lane at the apply, not predicted here. Without the pins the function runs unchanged: the handler's import of the
   class producer is guarded, the class stage logs `CLASS_SKIPPED <day> account_class_daily not importable`, and the returns table is
   written as today (Branch B below). Note the base declaration with the extended handler is NOT a supported pairing: the producer
   reads the trade-leg tokens from the declaration, so pin 3 and pin 1 land together.
2. **The plan.** `terraform` is not on this box, so no plan was read. The expected plan is 0 to add, 1 to change (the role policy),
   0 to destroy, plus the Lambda's code hash from the rebuilt artifact. The issuer reads the plan before the signed halves are used.

## Names and addresses (builder output, printed)

Printed by `lib/opal_naming.py` at this cell's commit, with the firm from `lookup("08335338")`:

```
name("irpt", <firm>, "reporting-gold", "lambda") = irpt-49f-reporting-gold-lambda
name("irpt", <firm>, "reporting-gold", "role")   = irpt-49f-reporting-gold-role
name("irpt", <firm>, "reporting-gold", "policy") = irpt-49f-reporting-gold-policy
name("irpt", None,   "reporting-gold", "lambda") = irpt-reporting-gold-lambda          (the artifact)
address("irpt", <firm>, "gold", "account_return_daily", "date=2026-10-05") = s3://opal-data-49financial/irpt/49financial/gold/account_return_daily/date=2026-10-05
address("irpt", <firm>, "gold", "account_class_daily",  "date=2026-10-05") = s3://opal-data-49financial/irpt/49financial/gold/account_class_daily/date=2026-10-05
```

The Terraform side mirrors the table name once, in `locals.tf` as `irpt_rg_gold_table_class`, cited to the producer's `TABLE_CLASS`.
Nothing is typed by hand.

## The act

ONE targeted `safe-apply` of `infra/aws/terraform/investor-reporting/reporting-gold/`, from a saved plan, with the rebuilt artifact. It
changes:
- the function's code (the artifact above), unchanged in its schedule (`cron(41 7 ? * MON-FRI *)`, America/New_York), timeout (900 s),
  memory (2048 MB) and layer;
- the role policy `irpt-49f-reporting-gold-policy`: write set `irpt_rg_gold_write_arns` becomes the returns prefix and the class
  prefix; the read set gains the class prefix; one new statement `ReadTheClassTableByKeyOnly` grants `dynamodb:GetItem` on
  `arn:aws:dynamodb:us-east-1:<account>:table/etf-classifications` and nothing else.

## Blast radius, by the producers' own rules

**What the act may touch.**
- ONE new prefix written: `s3://opal-data-49financial/irpt/49financial/gold/account_class_daily/` (two objects per day:
  `date=<D>/data.parquet` and `date=<D>/manifest.json`). It holds no object today.
- The returns prefix `.../gold/account_return_daily/` is written exactly as before, byte-identically: the extended and the
  unextended handler produced the same returns parquet for the same day and accounts, sha256 `11453fc7...ae2e1` on both (record
  `RELEASE_LOCAL_RUN.json`, 20 accounts, 2026-10-05). The scheduled fire writes only days AFTER the newest landed returns day, so it
  rewrites no landed returns key. A manual backfill event (below) can rewrite landed returns days and class days, to the same bytes.
- DynamoDB: `GetItem` on `etf-classifications`, one item per distinct held identifier (78 reads for the 61-account sample). The table
  is the canonical, cross-firm classification registry keyed by ticker; it carries no client data. The role gains no Scan, Query,
  index, write or Delete on it.
- S3 reads: the role's read set gains the class prefix, which the handler lists for its newest landed day (the catch-up, row
  IRPT_DASHBD-W19-S6); that grant was read-only and unused before the catch-up (row IRPT_DASHBD-W19-S3).

**What the act may not touch.** `.../gold/dim_return_method/` (another cell's served row; not in the write set); the holdings gold
(read only); the silver prefixes (read only); any other firm's bucket or prefix; the platinum prefix and the publisher; any other
Lambda, role or table; the schedule. The policy carries no `s3:Delete*`, no write to any table, and no `dynamodb:Scan`.

**Writers of the property, counted.** `account_class_daily/` has ONE writing rule, `account_class_daily.emit_class_day` called from
`handler.emit_classes`, reached by TWO paths: the scheduled fire, and an explicit backfill invocation by a seat (same code, covered
below). The producer's own `--local` CLI has no upload path. `account_return_daily/` keeps its one handler writer (plus the
producer's own `main --upload`, which no seat runs and this act does not touch). N = 1 rule for the new property.

**The manual path.** The Lambda event can carry `accounts`, `dry_run`, or `backfill` (`start`, `end`, at most 25 trading days, only
days at or before the newest landed returns day, `accounts` "population" or a list). A backfill now rewrites the class table for the
same days as the returns table. It creates no state the schedule cannot reach, and no date override exists beyond the landed range.

## Rollback, per key

- **Lambda.** The prior function is the artifact recorded in the source map at `last_deployed_commit` `829e46ed7f`
  (2026-10-05T00:12:52Z): `investor-reporting/irpt-reporting-gold-lambda.zip`, `deployed_code_sha256`
  `Mex71Y5gk9RYE9q885knj3Ph12xV2Y9eVqMl3uJ1Z44=`. The issuer records the live CodeSha256 and the artifact object's S3 version id before
  the apply (not read by this cell). Rollback is the Terraform route only (`aws lambda update-function-code` is barred): re-pin the prior
  artifact version in the source map and run a targeted `safe-apply`.
- **Role policy.** The prior policy is `iam.tf`/`locals.tf` at `4c34d86104`: revert the two files and run the same targeted apply. The
  statements removed are the class read, the class write and the DynamoDB `GetItem`.
- **Class prefix.** It is new, so there is no prior version of any key. Rollback is to delete the objects under
  `.../gold/account_class_daily/` AFTER the issuer's word (an S3 delete is not this packet's act and is not in the role's grant). Each
  fire adds two keys per day, listed in the fire's log line `class rows=<n> LANDED`.
- **Returns prefix.** A day written by the extended function is byte-equal to what the prior function writes for it, so no key needs
  restoring. If a returns key is ever suspect, the bucket is versioned: restore the prior version by `copy-object` from its version id
  (read it at that moment, as in the reporting-publish packet).

## Branch A / Branch B of the expected outcome

**The outcome, read from the rule at signing.** Each fire computes the days after the newest landed returns day through T-1, writes
those days of `account_return_daily` FIRST (unchanged code path), then splits the same days into classes and writes them. The class
split is the account producer's own figure and flow, imported unchanged; nothing is recomputed. Locally, on 20 accounts for one day:
19 account-days, 18 MEASURED with the classes summing to the account within 1.56e-16, 1 refused by name
(`CLASS_VALUES_DO_NOT_SUM_TO_ACCOUNT`, null return, no plug), 76 class rows.

- **Branch A, the expected one.** The first fire after the apply (a trading morning, 07:41 ET) lands T-1 of `account_return_daily`
  (and any backlog up to 10 days), and lands the same days of `account_class_daily` with `coverage` MEASURED on the account-days whose
  class values tie to the account, the identity holding to within 1e-9, and the manifest's `unclassified_share_of_value` printed. The
  log carries `<day> class rows=<n> LANDED` for each day and no `CLASS_SKIPPED`.
- **Branch B.** A day's class stage is refused by name and the returns table is still written. The log carries
  `CLASS_SKIPPED <day> <reason>` and the function returns `class_failed`. Reasons that can occur: the bundle pins of precondition 1
  are absent (`account_class_daily not importable`); `etf-classifications` unreadable (`ClassTableUnreadable`, so a read failure never
  reads as every holding unclassified); a partition unreadable (`REFUSED ... could not be read`); no class rows. No class object is
  written for that day. **The next fire retries it** (row IRPT_DASHBD-W19-S4, disarmed in code by the class catch-up, row
  IRPT_DASHBD-W19-S6): on each scheduled fire the handler lists the class prefix and emits every trading day after the class table's
  own newest day through the newest returns day just written (at most 10 days per fire, oldest first; a day older than this fire's
  returns days is recomputed by a read, nothing is written to the returns table for it); a day that still fails is logged by name
  (`CLASS_SKIPPED <day>`) and the returns table is never held. No class day is ever written beyond the newest returns day. A day
  can still be closed by hand with the backfill event, which rewrites both tables to the same returns bytes.

Neither branch moves a returns key. Neither moves "Data through". The class table is not read by any served consumer today.

## After-read the apply will run (the CTO's criteria 2 and 3)

On the first fire after the apply, with the issuer reading S3 and the function's log:
1. **A1, the log.** Zero `CLASS_SKIPPED` lines and one `<day> class rows=<n> LANDED` per day written. Else Branch B: name the reason.
2. **A2, criterion 2 (the identity).** Pick one account-day with `coverage` MEASURED in
   `.../gold/account_class_daily/date=<T-1>/data.parquet`; its `class_return_daily` values summed over its class rows equal
   `total_return_daily` of the same account-day in `.../gold/account_return_daily/date=<T-1>/data.parquet` to within 1e-9. Print the
   account-day's class-row count and the absolute gap.
3. **A3, criterion 3 (the share).** From the same class partition print the unclassified share: the sum of `market_value_eod` over
   `asset_class = unclassified` divided by the sum over all rows, with BOTH sums, the account count and the class-row count. The
   manifest's `unclassified_share_of_value` must equal it. (Local sample, 61 accounts: 0.153 percent against the old module's 1.804
   percent; the all-account figure is what A3 measures for the first time.)
4. **A4, DELTA=0 on the served returns.** The `account_return_daily` partition for T-1 equals a local run of the unextended handler
   (`git show 954983d543:infra/aws/lambda/investor-reporting/reporting-gold/handler.py`) for a named sample of accounts, row by row.
5. **A5, the grant.** `get-role-policy` shows the write set is exactly the returns and class prefixes and that `dynamodb:GetItem` on
   `table/etf-classifications` is the only DynamoDB action.

A1 to A5 are read, not waited on: an ad-hoc invoke with `dry_run` computes and prints without writing and may be used for QA before
the organic fire; it writes neither table.

## Unmeasured, stated

- **Duration of a catch-up fire.** A fire that owes class days older than its returns days recomputes them through the producer's
  own pipeline (reads only), up to 10 days, inside the same 900 s ceiling; this was not measured at population scale.
- **Duration at population scale.** The class stage reads positions, cash lines and trade legs for the run's days and one `GetItem` per
  distinct ticker. It was measured on 20 and 61 accounts only. The function's 900 s ceiling is unchanged. The returns table is written
  BEFORE the class stage, so a timeout in the class stage cannot lose a returns day, but it would skip that fire's class days
  (Branch B, backfill to close).
- **The table's all-account coverage.** See A3.

## CTO half -- 1.0.0_SA_CTO

UNSIGNED. Signing means: the blast radius above (one new prefix, the returns prefix byte-identical, one table read by key) is the whole
act; both branches are read from the rule; the writers are counted (one rule, two paths); the rollback is per key; the preconditions
are the deploying lane's and the issuer's and are met before the apply; a class day that fails is retried by the next fire.

## COO half -- 2.0.0_SA_COO~D2

UNSIGNED. Signing means: the issuer will have the deploying lane set the three `staged_from` pins and rebuild the artifact
(precondition 1), read the plan (precondition 2), apply once from the saved plan, and run A1 to A5 on the first fire. A skipped class
day is retried by the next fire's catch-up (rows IRPT_DASHBD-W19-S4, W19-S6), so no standing backfill is owed.
