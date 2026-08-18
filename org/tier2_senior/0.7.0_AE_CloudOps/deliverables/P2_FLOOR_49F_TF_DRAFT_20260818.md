# P2-FLOOR-49F -- TF DRAFT + EXPECTED PLAN ROWS (pre-apply read for COO+CTO)

**Author:** 0.7.0_AE_CloudOps, 2026-08-18 ~16:15Z. **TO:** OPAL_ADVIPOINTERS.P2-FLOOR-49F (GO 160648Z @49dd8469d1).
**Status: DRAFT -- nothing applied, nothing in infra/ yet.** Apply gates: (1) tonight's 23:01Z bd platinum
fixture verdict, (2) DS~A's P2D-4 written contract in hand, (3) CTO per-apply gate on this draft.
**Authority:** push plan @a2f27c8d0a s3 row 2; CTO host ruling (own scheduled stage under the S3-code
standard, NOT appended to the legacy bd chain's stage list); ratified P2 spec
`org/tier1_exec/4.0.0_SA_CRO/deliverables/P2_UNIFIED_MORNING_SCHEDULE_TIMING_MAP_SPEC_20260811.md`.

## 1. Shape (mdpf scheduled-floor pattern, transposed)

```
aws_scheduler_schedule.advi_49f_gold_floor          cron(<PROPOSED> * * ? *) UTC, window OFF
        |  role: advi_49f_floor_scheduler (InvokeFunction on dispatcher + DLQ SendMessage ONLY)
        v
aws_lambda_function.advi_49f_gold_dispatch          THIN DISPATCHER (DS~A preliminary concurrence 160948Z:
        |                                           option (a)) -- mutex surface + retry + DLQ home;
        |                                           input jsonencode{source, floor, run_class:"production"}
        v
SSM SendCommand -> <HOST from P2D-4 contract>       EC2 pulls DS~A's entrypoint from S3 (Rule 12) and runs
                                                    the canonical 49F runner chain as its OWN stage
        v
opal-data-assets/portal/gold/advi/49financial/{table}/date={T-1}/data.parquet
```

Accelerator (second act, floor-only first fire -- DS~A concurrence 160948Z): S3 event on the Schwab
silver-completeness marker -> same dispatcher. **Marker existence is UNGROUNDED today** -- DS~A grounds
it in P2D-4; if none exists the accelerator waits on the producer minting one (DS lane). NEVER#4 is
satisfied by the floor alone. **Homing note:** the S3 notification config lives in
`infra/aws/terraform/portal-notifications/` (charter: all S3 notification configs homed there, never
inside pipeline modules); the schedule/dispatcher/DLQ live in `infra/aws/terraform/opal-assets/`
(the runners' pipeline; product-gold home is opal-data-assets/portal/gold, 17b amendment).

## 2. Expected plan rows (P2F-1) -- opal-assets root, all ADDS, zero destroys

| # | resource | note |
|---|---|---|
| 1 | `aws_scheduler_schedule.advi_49f_gold_floor` | cron PROPOSED (s3 below); tz UTC; flexible_time_window OFF |
| 2 | `aws_iam_role.advi_49f_floor_scheduler` | trust scheduler.amazonaws.com |
| 3 | `aws_iam_role_policy.advi_49f_floor_scheduler` | InvokeFunction on dispatcher ARN + sqs:SendMessage on DLQ ARN, nothing wider |
| 4 | `aws_sqs_queue.advi_49f_floor_dlq` | DEDICATED (not the mdpf shared DLQ -- cross-pipeline coupling refused; decision row for CTO) |
| 5 | `aws_lambda_function.advi_49f_gold_dispatch` | thin dispatcher; sized deliberately (256MB/60s -- dispatcher, not data processing); env: HOST_INSTANCE_ID, SSM_DOC/command shape, ENTRYPOINT_S3_KEY, MODE=production (values from P2D-4) |
| 6 | `aws_iam_role.advi_49f_gold_dispatch` + policy | ssm:SendCommand scoped to the named instance ARN + document; logs; DLQ send |
| 7 | `aws_cloudwatch_log_group.advi_49f_gold_dispatch` | explicit retention |
| 8 | `aws_lambda_permission.scheduler_advi_49f_gold_floor` | estate parity: every Scheduler->Lambda edge carries the resource-based grant for auditability |

Second act (separate apply, portal-notifications root): the accelerator notification row(s) --
enumerated in their own pre-apply read when the marker key is pinned.

Source-map entry (Rule 4) + `git tag -a opal-assets-v{X.Y.Z}` + `--follow-tags` (Rule 6) ride the apply.
NO alarm/SNS/SES/monitor resources anywhere in this draft (moratorium self-check: the DLQ is a delivery
dead-letter, not a notification; no alarm reads it -- consistent with mdpf floor precedent where the
DLQ-depth alarm belonged to a PRE-moratorium vintage and its K3 disposition).

## 3. Floor expression (PROPOSED, not ruled)

Window: after ~12:18Z Schwab silver landing with margin, <=13:30Z (ratified CRO retarget of Group W's
14:30Z). **Proposal: `cron(45 12 * * ? *)` = 12:45Z daily** -- +27min margin on the ~12:18Z landing,
45min ahead of the mdpf floor so the mdpf-gold 13:30Z read of any 49F-adjacent artifact sees today's
run. Exact value tunes on DS~A's P2D-3 measured full-chain duration (their 160948Z: per-stage seconds
measured, full-chain S3-path duration pending) -- **the cron value in the applied TF is whatever the
P2D-4 contract + CTO gate settle; this row exists so the plan-read has a concrete candidate.**
Weekends included (T-1 trading-calendar logic lives in the chain, not the schedule -- mdpf precedent).

## 4. Both-namespace sweep + trigger characterization (ratified spec s3, run at build 08-19)

Before calling the floor final: `aws events list-rules` + `aws scheduler list-schedules` materialized
(auto-paginated, client-side filtered, denominators printed) for any pre-existing 49F gold dispatch;
paired with the S3-event-notification config read + lambda invoke-source characterization so an
absence resolves DEAD vs EVENT-ONLY, never ambiguous. (Known today: the canonical chain's only trigger
is a session act -- the NEVER#4 defect this TO closes.)

## 5. Open parameters (all owned, none blocking the draft read)

| param | owner | state |
|---|---|---|
| invocation mechanism (a/b/c) | DS~A P2D-4 | preliminary (a) thin dispatcher, 160948Z |
| host instance + SSM doc/command | DS~A P2D-4 | open |
| entrypoint S3 key + arg/env shape | DS~A P2D-4 | open |
| mutex location + refusal signature | DS~A P2D-4 | open (dispatcher surfaces a refused fire LOUD) |
| silver-completeness marker key | DS~A P2D-4 (ground, not recall) | open; floor-only first fire regardless |
| final cron value | CTO gate on this draft + P2D-3 duration | 12:45Z candidate |
| dedicated vs shared DLQ | CTO (decision row) | draft = dedicated |

---

# REV 2 (17:4xZ) -- P2D-4 CONTRACT FOLDED IN (@4dadd1354c; DS~A 173547Z)

The written invocation contract landed and changes the shape in three load-bearing ways. This
revision supersedes s1/s2 above where they conflict; s3-s5 stand.

## R2.1 Contract facts folded
- **Host is STOPPED at fire time** (bd-gold-layer-runner self-halts; measured stopped ~14:29Z,
  started 23:01Z by the legacy trigger; live read this hour: `i-01003b035d2988dfb` state=stopped,
  profile=bd-exporter-profile). The dispatcher takes the ENSURE-RUNNING duty (accrual pattern):
  start-if-stopped -> wait status-ok -> SSM SendCommand -> the command self-halts the box only if
  the dispatcher started it (idiom inside the SSM doc per the contract).
- **Own SSM document** (CTO host ruling): the 49F chain is fired by a NEW dedicated SSM doc whose
  command body is the contract's verbatim (s3 sync `_code/` -> `python3 chain_49f_entrypoint.py
  --production` -> log upload -> conditional self-halt). Args: `--production` and NOTHING else
  (T-1 derived internally, trading-day frontier).
- **Code home RULED** (CTO 172006Z): `s3://opal-data-assets/portal/gold/advi/_code/` -- first-minted
  by DS~A, 51 objects ETag-verified.
- **No silver-completeness marker exists** (grounded: converter manifests land under meta/, RULED
  non-triggering, conversion_manifest.py:50-53) -- FLOOR-ONLY at first fire is now the contract
  form, not just my default; the accelerator is a follow-on producer-side act in DS~A's lane,
  separately contracted when built. The portal-notifications second act DEFERS until then.
- **Mutex refusal is a real event**: `CHAIN REFUSED: live lock` rc=3 -- the dispatcher polls
  get-command-invocation and logs the refusal signature LOUD (ERROR log line; no alarm -- moratorium).

## R2.2 Expected plan rows, REVISED -- now TWO ROOTS

**Root A: opal-assets (schedule + dispatcher), 9 rows, all ADDS:**
rows 1-8 as s2 above (unchanged: schedule advi_49f_gold_floor @ cron(45 12 * * ? *) candidate;
scheduler role+policy; DEDICATED advi_49f_floor_dlq [CTO-approved G-A]; dispatcher lambda 256MB/
awaiting-timeout-sizing vs the ensure-running wait -- bumped to timeout=900s, still a dispatcher;
dispatcher role+policy; log group; scheduler->lambda permission), PLUS:
| 9 | `aws_ssm_document.advi_49f_chain_dispatch` | command body = contract verbatim; own doc, never the legacy chain's |
Dispatcher policy adds vs s2: `ec2:StartInstances` + `ec2:DescribeInstanceStatus`/`DescribeInstances` scoped to
`i-01003b035d2988dfb` (+ ec2:DescribeInstanceStatus is unconditionally resource-`*` by AWS API shape -- noted),
`ssm:SendCommand` scoped to the instance ARN + the new document ARN, `ssm:GetCommandInvocation`.

**Root B: bd-pipeline (instance-role grants for the chain's measured access surface), ADDS to
bd-exporter-ec2-role (the profile the host carries -- the SAME role that received this morning's
monolith_schwab_advi_read fact_rps grant @7b706eec4c):**
| B1 | S3 read `opal-data-assets/schwab/08335338/silver/*` (widens this morning's fact_rps-only grant to the fact_*/dim_* set the chain reads) |
| B2 | S3 read `opal-data-assets/blackdiamond/49f/silver/dim_advisor_fee_role/*` |
| B3 | S3 read `opal-data-assets/schwab/08335338/meta/conversions/*` |
| B4 | S3 read the a07 bd-securities transitional substrate (exact prefix pinned at build from a07's source; CTO 160826Z annotation: grant required, never a deletion warrant) |
| B5 | S3 read+write `opal-data-assets/portal/gold/advi/49financial/*` |
| B6 | S3 read `opal-data-assets/portal/gold/advi/_code/*` |
| B7 | DynamoDB read `ETFClassifier` (a07) |
Each new-resource grant verified at apply per Rule 22a: simulate-principal-policy ONE
--resource-arns per call, isolated positive control, negative on an ungranted sibling prefix.

**Cross-root note for the plan read:** two roots, two applies, one window; Root B applies FIRST
(grants before the first scheduled fire can need them), Root A second; each root 0-diff + tagged
(bd-pipeline-vX.Y.Z / opal-assets-vX.Y.Z). Source-map entries: dispatcher lambda added to
lambda-source-map.json.

## R2.3 What this revision does NOT change
Floor cron candidate 12:45Z (CTO G-A approved-as-candidate; final pin on DS~A's P2D-3 measured
duration, MCP'd same-day 08-19). NEVER#4 satisfied by the floor alone. No alarms/monitors/SNS/SES
anywhere. Apply gates unchanged: 23:01Z fixture verdict -> CTO per-apply gate at the apply.
