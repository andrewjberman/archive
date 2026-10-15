# NEVER-WIDEN PACKET -- DB-c-2 (round 114, workstream B-CW): the Cottonwood holdings_performance_daily schedule, its principal and the catch-up run

Status: an unsigned draft. It carries no signature and no approval. It applies nothing: no schedule is created, no principal is created, no key is written, and no Terraform is planned or applied. The CTO's half and the issuer's half must sign the pair before any apply or any catch-up run.

Measured on 2026-10-15 from the worktree at cf8ab92263 plus the DB-c-1 record (LANDING_AND_FRONTIER_R114.json). Every name below is output of lib/opal_naming.py name() or address(); none is typed by hand.

## Change set

Names (builder output, no refusal):
- schedule: `irpt-cot-holdings-performance-daily` from name("irpt","cottonwood","holdings-performance","daily")
- principal (the Lambda execution role): `irpt-cot-holdings-performance-role` from name(...,"role")
- principal policy: `irpt-cot-holdings-performance-policy` from name(...,"policy")
- scheduler invoke role: `irpt-cot-holdings-performance-scheduler-role` from name(...,"role","scheduler")
- scheduler policy: `irpt-cot-holdings-performance-scheduler-policy` from name(...,"policy","scheduler")
- target function: `irpt-cot-holdings-performance-lambda` from name(...,"lambda"); its own Terraform and package are not in this packet.

Schedule entry in words. One aws_scheduler_schedule in the group default, flexible time window OFF, cron(15 8 ? * MON-FRI *) in America/New_York. The time is the DB-c-1 proposal, 08:15 New York. The measured latest landing is 07:46 New York (all 15 of the last trading days landed at 11:46 UTC), so 08:15 sits about 28 minutes after it. The target is the Cottonwood function, and its input carries kind irpt_holdings_performance_daily and source blackdiamond_z09. The handler passes the event's source to the producer, and blackdiamond_z09 is the declaration key for this channel in sources.json. The scope is derived from the registry through a local, never typed, as the Inflection entry derives its firm. The state is ENABLED in the 49 Financial model; whether the first apply creates it DISABLED is question 7.

Desired entry, as text only (not written to any .tf file):

```hcl
module "irpt_holdings_performance_cot_schedule_name" {
  source   = "../../modules/opal_name"
  system   = "irpt"
  scope    = local.irpt_hp_cot_firm   # registry-derived, never typed
  function = "holdings-performance"
  kind     = "daily"
}

resource "aws_scheduler_schedule" "irpt_holdings_performance_cot" {
  name                         = module.irpt_holdings_performance_cot_schedule_name.name
  description                  = "DB-c-2 (proposed): Cottonwood holdings-performance daily trigger, 08:15 New York on trading weekdays"
  group_name                   = "default"
  state                        = "ENABLED"
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
      note   = "scheduled fire; handler.py resolves the target trading day itself"
      source = "blackdiamond_z09"
    })
  }
}
```

Principal in words. The execution role of the Cottonwood Lambda, trusted by lambda.amazonaws.com, modelled on the 49 Financial role in holdings-performance/iam.tf. The grants described here are proposed, not created:
- s3:ListBucket on opal-data-assets, condition s3:prefix blackdiamond/cottonwood/silver/fact_holdings/*, the declared silver. balance_prefix is null for this channel, so there is no balance statement.
- s3:GetObject on opal-data-assets, objects under blackdiamond/cottonwood/silver/fact_holdings/date=*/ only.
- s3:PutObject on opal-data-cottonwood, objects under irpt/cottonwood/gold/holdings_performance_daily/ and irpt/cottonwood/gold/holdings_performance_manifest/ only.
- s3:ListBucket on opal-data-cottonwood, condition s3:prefix irpt/cottonwood/gold/holdings_performance_daily/*, so the catch-up can see which days landed.
- logs on its own log group /aws/lambda/irpt-cot-holdings-performance-lambda.
No delete, no other table, no other firm's bucket or prefix.

Catch-up run, as commands (not executed). For each date D in the catch-up list, ascending:
`python data/assets/scripts/gold/irpt_holdings_performance/holdings_performance.py --date D --source blackdiamond_z09 --upload`
or the handler with the event {"date": D, "source": "blackdiamond_z09"}, which computes exactly that day (handler.py lines 108-109). Run under the principal's credentials, one date at a time, and stop at the first non-zero return code. The argv form is the one handler.py lines 145-147 build.

The scheduled path differs, and the CTO's half should read it. Once the schedule exists, a fire computes the trading days after the newest landed gold partition through the target day, oldest first, at most 5 per fire (handler.py lines 101-124). From the newest landed date 2026-09-25 that is 2026-09-28 onward. The date 2026-06-09 lies before that newest landed date, so the scheduled path does not reach it.

## Keys written

Count: 39 objects, which is 13 dates times 3. The dates are:

- 2026-06-09
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

For each date, in this order: holdings_performance_daily/date=D/data.parquet, then holdings_performance_manifest/date=D/data.parquet, then holdings_performance_manifest/date=D/manifest.json. The producer's emit_day() writes them in that order (holdings_performance.py lines 1164 to 1185): the daily parquet, the manifest parquet, then manifest.json.

The keys that move (the builder's address() output, in order):

```
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_daily/date=2026-06-09/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-06-09/data.parquet
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/date=2026-06-09/manifest.json
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

No other key moves. emit_day() addresses only the daily table and the manifest table, and the catch-up run writes only through emit_day().

Existence, from a fresh LIST on 2026-10-15 of both gold prefixes under each of the 13 dates: 0 of the 39 keys exist. The holdings gold has 75 date partitions, newest 2026-09-25, and the manifest prefix has 75 partitions, newest 2026-09-25. None of the 13 dates has a holdings partition, so no catch-up key would overwrite an existing object.

## Both branches

If the run succeeds: holdings_performance_daily gains 13 date partitions, and its newest date moves from 2026-09-25 to 2026-10-13. The manifests move the same way. The portal path reads the gold through infra/aws/lambda/investor-reporting/performance/holdings_gold.py, as RD_COTTONWOOD_PRODUCER_R110 records, so the served output changes on success. Whether that path reads the manifest objects too is not established here.

If the run fails midway: the handler stops at the first date with a non-zero return code and never skips it (handler.py lines 151 to 153). Dates before the failing date are complete, three objects each. Within one date the producer writes the daily parquet first, so a failure between writes leaves a partial date: a daily partition with no manifest, or a manifest parquet with no manifest.json. Dates after the failure have no objects. The newest gold partition could then be a partial date, which the portal path would read as served. This packet does not establish how the portal path treats a partial date.

## Rollback

Per key, the rollback is an S3 delete of that one object. It restores the absence of that object, and the pre-run state of these 39 keys is absence (fresh LIST above). Delete newest date first and manifest.json before the manifest parquet before the daily parquet, so no reader sees a daily partition without its manifest. An S3 delete is destructive and needs Andrew's word under CLAUDE.md section 5 and the agent autonomy rule; it is not authorised by this packet.

Schedule rollback: set its state to DISABLED, or remove the resource in a reviewed Terraform plan applied through safe-apply. Either restores the state with no schedule firing. Principal rollback: remove the role, the policy, the scheduler role and the scheduler policy in the same reviewed plan. Neither rollback step reads or writes the silver.

## Questions for the CTO's half

1. The proposed time, 08:15 New York, against the 06:00 ET fold and against ~P2. The DB-c-1 read measured all 15 landings at 07:46 New York, after 06:00, a count of 15 of 15. This packet does not claim what the 06:00 fold means. Whether ~P2 (2.0.0_SA_COO~P) holds a fire-time rule this proposal must meet is not established here.
2. The principal's identity and grants are described above. The bucket policy of opal-data-cottonwood, including any deny fence keyed on role names, was not read because it is a GET outside the LIST and HEAD grant. Confirm the grants before any apply.
3. Whether the early silver date 2026-06-09, which has no gold while gold starts 2026-06-10, is expected. The producer reads the prior trading day for each date (holdings_performance.py lines 983 to 987), and no silver partition exists before 2026-06-09. The scheduled path does not reach this date.
4. The three partitions 2026-09-23, 2026-09-24 and 2026-09-25, whose newest object is dated 2026-09-28. Were they rewritten after their landing? If a rewrite came after a gold run, the gold could disagree with the silver. A LIST does not separate the two cases.
5. Who applies, and on which AE instance. This order names no AE instance, so the applying seat is the CTO's to name.
6. The pair. The apply and the catch-up run are later acts under a never-widen pair, signed by both halves before any apply. This packet is not that pair.
7. The state at creation: ENABLED as in the 49 Financial model, or DISABLED until the first catch-up is read.
8. The rollback deletes need Andrew's word before they run.
9. The Cottonwood function's own Terraform and package are not in this packet. The schedule cannot fire until that exists, and whether it exists is not established.

## Not in this packet

- No Terraform plan or apply, and no .tf file is edited. The desired entry above is text.
- Whether the Cottonwood function, its package or its lambda-source-map entry exists: not established.
- The live state of any schedule or IAM principal named here (get-schedule, get-role): not read.
- The bucket policies of opal-data-cottonwood and opal-data-assets: not read.
- Whether the portal path reads the manifest objects, and how it treats a partial date: not established.
- Whether any catch-up date would compute: not run. No producer run was made, and no output of one was checked.
- The meaning of the 06:00 ET fold: not claimed.
- account_return_daily: not in the catch-up set and not packeted.
- The cause of the missing 2026-06-09 gold: not confirmed by any run; the reading of the code is in question 3.
