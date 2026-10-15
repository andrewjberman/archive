# NEVER-WIDEN PACKET -- DB-c-5 (round 115, workstream B-CW): the Cottonwood holdings_performance_daily pair, finalized on the DB-c-4 read

Status: UNSIGNED. This packet is an unsigned draft. It carries no signature, no approval and no sign-off from either half. It applies nothing: no schedule is created, no principal is created, no function is built, no key is written, and no Terraform is planned or applied. The CTO's half and the issuer's half must both sign the pair before any apply or any catch-up run.

Measured on 2026-10-15 from the worktree at 5045d0f2d8 (the amendment of this order), with the DB-c-4 record PRODUCER_READ_R115.json (commit 89ec40ff5d). Every name below is output of lib/opal_naming.py name() or address(); none is typed by hand. The silver and gold LIST reads were made on 2026-10-15 and are repeated in the Keys written section.

## Change set

Names (builder output, no refusal, confirmed by calling the builder):
- schedule: `irpt-cot-holdings-performance-daily` from name("irpt","cottonwood","holdings-performance","daily")
- principal (the Lambda execution role): `irpt-cot-holdings-performance-role` from name(...,"role")
- function (the target, mode BUILD, see Function): `irpt-cot-holdings-performance-lambda` from name(...,"lambda")

Schedule entry in words. One aws_scheduler_schedule in the group default, flexible time window OFF, expression cron(15 8 ? * MON-FRI *) in the time zone America/New_York. The fire time is 08:15 New York, as the CTO accepted. The target is the Cottonwood function. Its input carries kind irpt_holdings_performance_daily, a note, and the source key blackdiamond_z09, which is the declaration key of this channel in data/assets/scripts/gold/irpt_holdings_performance/sources.json. The handler passes that source to the producer. The state is DISABLED when the schedule is created, and it moves to ENABLED only after the catch-up's after-read (see Catch-up first). The input-frontier hold is not a schedule setting. It is the function's behaviour, written here as a requirement for the build: when the silver partition of the trading day T-1 is absent at fire time, the function HOLDS, logs the absence, and writes no key for that day, so it never stamps a stale day.

Desired schedule entry, as text only (not written to any .tf file). It is modelled on the 49 Financial schedule in infra/aws/terraform/investor-reporting/holdings-performance/schedule.tf, which is ENABLED with a cron of 07:30 in the same zone:

```hcl
module "irpt_holdings_performance_cot_schedule_name" {
  source   = "../../modules/opal_name"
  system   = "irpt"
  scope    = local.irpt_hp_cot_firm   # registry-derived through a local, never typed
  function = "holdings-performance"
  kind     = "daily"
}

resource "aws_scheduler_schedule" "irpt_holdings_performance_cot" {
  name                         = module.irpt_holdings_performance_cot_schedule_name.name
  description                  = "Cottonwood holdings-performance daily trigger, 08:15 New York on trading weekdays; created DISABLED, enabled after the catch-up's after-read"
  group_name                   = "default"
  state                        = "DISABLED"   # the CTO's ruling: ENABLED only after the catch-up's after-read
  schedule_expression          = "cron(15 8 ? * MON-FRI *)"
  schedule_expression_timezone = "America/New_York"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = module.irpt_holdings_performance_cot.function_arn
    role_arn = aws_iam_role.irpt_holdings_performance_cot_scheduler.arn
    input = jsonencode({
      kind   = "irpt_holdings_performance_daily"
      note   = "scheduled fire; the function resolves the target trading day itself and holds when T-1 silver is absent"
      source = "blackdiamond_z09"
    })
  }
}
```

Principal in words. The execution role of the Cottonwood function, trusted by lambda.amazonaws.com, modelled on the 49 Financial role in holdings-performance/iam.tf. The grants below are described, not created:
- PutObject only on the two gold tables, and nothing else: s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_daily/ and s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/ (the write prefixes, from address() with the partition tail cut).
- Read on the Black Diamond silver only: s3://opal-data-assets/blackdiamond/cottonwood/silver/fact_holdings/ (the read prefix, as the order names it).
- logs on its own log group /aws/lambda/irpt-cot-holdings-performance-lambda.
- No delete, no overwrite check, no other table, no other firm's bucket or prefix.
Open point, carried to the CTO's half as question 4: the scheduled path lists the daily gold prefix to find the newest landed day (handler.py, _landed_days), and the read prefix named by the order does not include it. The principal therefore needs ListBucket on the daily gold prefix for the scheduled path. This packet does not add that grant; the order names the read prefix as exactly the silver prefix.

## Function

Mode: BUILD. The verdict of the DB-c-4 read is AD_HOC, claim inferred, not FUNCTION. The evidence, from the record PRODUCER_READ_R115.json: no Lambda or scheduled job in the repo names the Cottonwood source; the two producer functions in infra/aws/terraform/investor-reporting/holdings-performance/lambda.tf are the 49 Financial one and the Inflection one, and their schedules pass the other two declared source keys as event input; the SSM holdings dispatch runs holdings_snapshot.py, which does not reference the performance producer. The gold manifests of 2026-09-25 and 2026-08-27 carry schema_version 1.1 with no partitions_read and no span_trading_days key, while HEAD's producer emits schema 1.2 with both (SCHEMA_VERSION at HEAD is 1.2; git history shows 1.2 first at de3d423dce on 2026-10-01). So the writer was an earlier emission, and a function built from HEAD would write 1.2 partitions beside 1.1 history. This is the finding of the DB-c-4 row IRPT_DASHBD-D2-W403-S2, which the CTO's half is asked to rule.

Whether a function named irpt-cot-holdings-performance-lambda already exists is NOT ESTABLISHED. The order grants no get-function, so no function was read. If it exists, the mode would be ADOPT by the rule of step 3, and the Terraform act would be an import; the CTO's half must confirm the absence before the build.

What the build cell must make, if BUILD stands:
1. The function irpt-cot-holdings-performance-lambda, whose handler is the scheduled wrapper in infra/aws/lambda/investor-reporting/holdings-performance/handler.py, with the event source blackdiamond_z09. The package follows the 49 Financial one: the producer at its original relative path, sources.json beside it, the same shared libraries.
2. Its Terraform, modelled on infra/aws/terraform/investor-reporting/holdings-performance/lambda.tf (one module, the same runtime, timeout and memory, its own log retention) and on its iam.tf (the principal of the section above).
3. The input-frontier hold: at fire time, when the silver partition of T-1 is absent, the function holds, logs the absence and writes nothing. The CTO ruled that this code is a build item in the function cell (decomposition decision (c)); the current handler does not hold. Today a day whose silver is absent returns a non-zero code and stops the catch-up.
4. The emission: the build must state which producer emission it packages. HEAD emits 1.2. The existing gold is 1.1 for every date it holds. The CTO's half must rule before the build.

## Catch-up first

The order of acts, each one only after the one before is complete and read:
1. The pair has the signatures of both halves (the CTO's half and the issuer's half). Nothing below starts before that.
2. The function irpt-cot-holdings-performance-lambda is adopted (if it exists) or built (if not), with its package and Terraform, and is applied through safe-apply by the applying seat the CTO names.
3. The principal irpt-cot-holdings-performance-role is created with the grants of the Change set section, and nothing else.
4. The catch-up runs one date at a time, in ascending order, through the handler with the event {"date": D, "source": "blackdiamond_z09"}, which computes exactly that day (handler.py, the event with a date). Each run is under the principal's credentials. It stops at the first non-zero return code, and that date is retried, never skipped.
5. The AFTER-READ, before any schedule exists: a fresh LIST shows that every key of the 12 dates in Keys written exists, that no key outside them moved, and that the newest gold daily partition is 2026-10-13, which is the T-1 frontier for the as-of date. Only if the after-read passes does step 6 run.
6. ONLY THEN the schedule irpt-cot-holdings-performance-daily is created ENABLED (the state changes from DISABLED to ENABLED at this act). The first scheduled fire, at 08:15 New York on the next trading weekday, then lands on a gold frontier at T-1.

## Keys written

The catch-up as-of date is 2026-10-13, the newest silver partition by a fresh LIST on 2026-10-15. The silver holds 93 partitions, from 2026-06-09 to 2026-10-13, with no trading day missing. The gold daily table holds 75 partitions, newest 2026-09-25, and the manifest table holds 75, newest 2026-09-25. No gold gap lies inside the range.

The catch-up dates are the silver trading days up to the as-of date that have no gold partition, minus the excluded date. There are 13 candidates; one is excluded:

Excluded: 2026-06-09. Its prior trading day 2026-06-08 has no silver partition, and the source declares no gap link, so the producer's rule has no base for 2026-06-09. The day gets no key. The reason is measured in the DB-c-4 record. The excluded date is a question for the CTO's half (question 3).

Catch-up dates, ascending (12, count of dates):

- 2026-09-28
- 2026-09-29
- 2026-09-30
- 2026-10-01
- 2026-10-02
- 2026-10-05
- 2026-10-06
- 2026-10-07
- 2026-10-08
- 2026-10-09
- 2026-10-12
- 2026-10-13

Keys: three per date, in this order for each date: the daily table's data.parquet, the manifest table's data.parquet, then the manifest table's manifest.json. The count is 36, which is 12 dates times 3. The keys are the builder's address() output:

```
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_daily/date=2026-09-28/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-09-28/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-09-28/manifest.json
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_daily/date=2026-09-29/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-09-29/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-09-29/manifest.json
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_daily/date=2026-09-30/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-09-30/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-09-30/manifest.json
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_daily/date=2026-10-01/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-10-01/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-10-01/manifest.json
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_daily/date=2026-10-02/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-10-02/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-10-02/manifest.json
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_daily/date=2026-10-05/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-10-05/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-10-05/manifest.json
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_daily/date=2026-10-06/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-10-06/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-10-06/manifest.json
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_daily/date=2026-10-07/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-10-07/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-10-07/manifest.json
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_daily/date=2026-10-08/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-10-08/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-10-08/manifest.json
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_daily/date=2026-10-09/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-10-09/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-10-09/manifest.json
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_daily/date=2026-10-12/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-10-12/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-10-12/manifest.json
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_daily/date=2026-10-13/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-10-13/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-10-13/manifest.json
```

No other key moves. The producer's emit_day() addresses only the daily table and the manifest table, and the catch-up writes only through emit_day(). A fresh LIST on 2026-10-15 of both gold prefixes found 0 of the 36 keys present, so no catch-up key would overwrite an existing object. The pre-run state of each key is absence.

## Both branches

If the run succeeds: the daily table gains 12 date partitions and its newest date moves from 2026-09-25 to 2026-10-13, and the manifest table moves the same way. The portal path reads the gold through infra/aws/lambda/investor-reporting/performance/holdings_gold.py, so the served output changes on success. Whether that path reads the manifest objects too is NOT ESTABLISHED here.

If the run fails midway: the catch-up stops at the first date with a non-zero return code and never skips it. The dates before the failing date are complete, three objects each. Within one date the producer writes the daily parquet first, so a failure between writes leaves a partial date: a daily partition with no manifest parquet, or a manifest parquet with no manifest.json. The dates after the failure have no objects. The newest gold partition could then be a partial date, which the portal path would read as served. This packet does NOT establish how the portal path treats a partial date.

A held fire, once the frontier hold is built: when the silver of T-1 is absent at 08:15 New York, the function logs the absence and writes no key, so the gold stays at its last complete date, and the next fire computes the missed day as a catch-up. Without the hold, which is the state of the current handler, the fire returns a non-zero code for that day and writes nothing for it either.

## Rollback

Per key: an S3 delete of that one object. It restores the absence of that object, and the pre-run state of all 36 keys is absence (the fresh LIST above). Delete the newest date first, the manifest.json before the manifest parquet, and the manifest parquet before the daily parquet, so that no reader sees a daily partition without its manifest. An S3 delete is destructive and needs Andrew's word under CLAUDE.md section 5 and the agent autonomy rule. This packet does not authorise it.

Schedule: set its state to DISABLED, or remove the resource in a reviewed Terraform plan applied through safe-apply. Either stops every scheduled fire.

Function: remove the function irpt-cot-holdings-performance-lambda and its package in the same reviewed plan, or leave it in place disabled. The function writes nothing unless invoked or fired.

Principal: remove the role irpt-cot-holdings-performance-role, its policy and the scheduler role and policy in the same reviewed plan. Neither rollback step reads or writes the silver.

## Questions for the CTO's half

1. Who applies, and on which AE instance. The order names the lane 0.0.0_AB_MSTR~DELL2 among the questions, but this packet does not confirm it as the applying lane. The CTO's half names the applying seat and its AE lane.
2. The principal's grants against the bucket policies. The bucket policy of opal-data-cottonwood, and of opal-data-assets, including any deny fence keyed on role names, was not read; the order grants no GET of a bucket policy. Confirm the grants before any apply.
3. The excluded date 2026-06-09. Its prior trading day 2026-06-08 has no silver partition, so the producer computes no 2026-06-09. The date becomes computable only if a 2026-06-08 silver partition is delivered, or if the CTO rules that this source may link across a gap (the declaration would then change, and that is a decision, not a fix this packet makes). Confirm the exclusion of this one date, and state what happens to its gold partition.
4. The principal's read of the daily gold prefix for the scheduled path. The scheduled path lists the daily gold prefix to find the newest landed day, so the principal needs ListBucket on that prefix, which the order's read prefix (silver only) does not name. Rule whether to add it.
5. The schema difference: the gold manifests carry schema 1.1 and the HEAD producer emits 1.2, which also adds the partitions_read and span_trading_days keys. Rule which emission the function packages, and whether the existing 1.1 partitions are rewritten before or after the catch-up. This is the finding of row IRPT_DASHBD-D2-W403-S2.
6. The function's existence. Whether a function named irpt-cot-holdings-performance-lambda exists is not established; a get-function is needed before the mode is final.
7. The state at creation: this packet creates the schedule DISABLED and enables it only after the after-read. The CTO accepted that order; the CTO's half confirms it.
8. Both halves sign the pair before any apply. This packet is not that pair, and it is UNSIGNED.
9. The rollback deletes need Andrew's word before they run.
10. The 08:15 fire time against the measured landing times and against the other schedules is the CTO's accepted ruling; this packet does not re-measure it.

## Not in this packet

- No Terraform plan or apply, and no .tf file is edited. The desired entries above are text.
- Whether the function irpt-cot-holdings-performance-lambda exists, and its package and lambda-source-map entry: NOT ESTABLISHED (no get-function).
- The live state of any schedule or IAM principal named here (get-schedule, get-role): not read.
- The bucket policies of opal-data-cottonwood and opal-data-assets: not read.
- Whether the portal path reads the manifest objects, and how it treats a partial date: NOT ESTABLISHED.
- Whether any catch-up date would compute: not run. No producer run was made and no output of one was checked.
- The cause of the missing 2026-06-09 gold beyond the code reading in question 3: not confirmed by any run.
- The writer of the existing gold: AD_HOC is inferred, and no run log was read.
- account_return_daily and any other table: not in the catch-up set and not packeted.
