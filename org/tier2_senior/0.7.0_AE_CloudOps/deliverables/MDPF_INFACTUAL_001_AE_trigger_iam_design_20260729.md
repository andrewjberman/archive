# MDPF_INFACTUAL.001 -- AE half: trigger + IAM design for the CONSUME re-point

**Author:** `0.7.0_AE_CloudOps~A` · 2026-07-29 ~0110Z
**Charter:** COO 20260729T003956Z + deliverable change 004830Z + CONSUME ruling 010220Z (COO 010149Z, CTO gate-lean adopted)
**Status: DESIGN ONLY. Deploy freeze in force (CTO 234106Z). NOTHING in this file is applied.**
**Deliberately NOT landed as edits to `infra/**`** -- the 4c precedent (an emitter zip already carrying
unapplied behavior, where any sweep-apply activates it early) is exactly why a freeze-gated design does
not sit in the live TF tree waiting to be swept. The diffs below are applied by the executing agent
AFTER the freeze lifts, as their own reviewed commit.

---

## 1. The ruling this design serves

COO ruled **CONSUME**: MDPF's inflection ETF leg re-points to the existing ETFS_SETUP artifact
`s3://opal-data-etfs/daily/inflection/{date}.json` instead of landing DS~A's orion recompute feeder
(that feeder becomes the cross-check instrument). The ruling attached a **hard blocking gate**:

> inf-etf-ownership-daily is SENTINEL/EVENT-ONLY with no schedule of its own -> **BLOCKED.**
> It gets a schedule BEFORE or WITH the re-point. Not after, not as a follow-up.

**Measured verdict (this session, live primitives): it IS sentinel-only.** `list-rule-names-by-target`
on the function ARN returns exactly one rule -- `inf-etf-ownership-on-gold-complete` (ENABLED,
event-pattern: ObjectCreated on `opal-data-inf`, key suffix `pipeline-complete.json`). No
ScheduleExpression anywhere beneath it. So the gate binds, and this design is the unblock.

Producer liveness context (full evidence: MCP 010157Z to COO):
- `inf-etf-ownership-daily` ALIVE, artifact `2026-07-28.json` written 15:04Z on 07-28 (T-0 fresh).
- `cot-etf-ownership-daily` ALIVE on its own `cron(30 10 * * ? *)` -- the estate already runs BOTH
  trigger philosophies inside one product family; this design converges inf toward the cot/floor model.
- `bd-49f-etf-ownership-daily` DEAD both halves (no rule, no resource policy); not in scope here --
  MDPF's 49F leg is already correct via RPS and does not consume it.

---

## 2. Design A (THE GATE): `inf-etf-ownership-scheduled-floor`

### 2.1 Zero code change required -- measured, not assumed

`infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily/lambda_function.py`:
- `:96` `target_date = event.get("date") if isinstance(event, dict) else None` -- the handler never
  parses the S3 event body. A scheduled-fire payload carries no `"date"` key, so it takes the default
  path: `:65` resolve the NEWEST `gold/canonical/holdings_*` partition and emit that slice.
- `:13-14` "Idempotent: writes daily/inflection/{date}.json overwrite-per-date." A floor fire after a
  same-day sentinel fire re-emits the identical slice (LastModified advances, content converges).
- `:78-85` an explicit-`date` invoke stays available for backfill and fails LOUD on a bad date.

So the floor is **pure infra**: one rule + one target + one permission.

### 2.2 The TF diff (to `infra/aws/terraform/inf-pipeline/inf-etf-ownership-daily.tf`, post-freeze)

```hcl
# NEVER#4 floor (mirrors mdpf-scheduled-floor, scheduled-floor.tf): a production pipeline
# must have a schedule of its own; the gold-complete sentinel rule is RETAINED as the
# accelerator. Daily INCLUDING WEEKENDS (the mdpf floor's weekday-only-cron incident:
# a MON-FRI cron missed the Sat T+1 reconciliation -- do not narrow this).
resource "aws_cloudwatch_event_rule" "inf_etf_ownership_scheduled_floor" {
  name        = "inf-etf-ownership-scheduled-floor"
  description = "Scheduled floor beneath inf-etf-ownership-on-gold-complete (MDPF_INFACTUAL.001 consume-gate; NEVER#4). 19:00Z daily incl weekends: ~4h after the sentinel's observed ~15:04Z fire, 1h before the (declared, pending) mdpf-scheduled-floor at 20:00Z so the floor-run of the MDPF chain always finds a same-day artifact."
  schedule_expression = "cron(0 19 * * ? *)"
}

resource "aws_cloudwatch_event_target" "inf_etf_ownership_scheduled_floor" {
  rule      = aws_cloudwatch_event_rule.inf_etf_ownership_scheduled_floor.name
  target_id = "InfEtfOwnershipScheduledFloor"
  arn       = module.inf_etf_ownership_daily.function_arn
}

resource "aws_lambda_permission" "sched_floor_inf_etf_ownership_daily" {
  statement_id  = "SchedFloorInfEtfOwnershipDaily"
  action        = "lambda:InvokeFunction"
  function_name = module.inf_etf_ownership_daily.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.inf_etf_ownership_scheduled_floor.arn
}
```

### 2.3 Timing rationale (19:00Z)

- Sentinel normally fires ~15:0xZ (observed 15:04Z on 07-28); by 19:00Z the floor's re-emit is a
  no-op-equivalent idempotent overwrite of the same slice.
- If the INF spine DIES (the six-day-freeze shape), the floor still emits the newest available
  holdings partition at 19:00Z -- the artifact's `source_as_of` honestly carries the older vintage
  (`:137-141`, TRUE data vintage, never the run date). The consumer sees an honest lag, not a freeze.
- 1h BEFORE the declared `mdpf-scheduled-floor` `cron(0 20 * * ? *)` (TF-declared, NOT yet landed --
  verified `ResourceNotFoundException` live), so once the 4c set lands, the chain's floor-run always
  consumes a same-day floor artifact. Ordering holds under both accelerators too.
- Daily incl weekends: inf artifacts demonstrably land on weekends (07-26 Sun observed); the mdpf
  floor's own header documents the weekday-only incident.

### 2.4 Price

| Item | Cost |
|---|---|
| Code change | **Zero** (measured, §2.1) |
| TF resources | +3 (rule, target, permission), one file |
| IAM role change | **Zero** (invoke permission is a Lambda resource policy, not a role grant) |
| Plan blast radius | 3 adds, 0 changes, 0 destroys expected; `-target` the 3 addresses if the inf-pipeline tree carries unrelated drift |
| Apply | post-freeze, `.tools/safe-apply.sh`, 0-diff verify, tag `inf-pipeline-v{next}` per `git tag -l "inf-pipeline-v*"` at apply time |

### 2.5 Post-apply verification (the exercise, not the config read)

1. `aws events describe-rule --name inf-etf-ownership-scheduled-floor` -> ENABLED + the cron.
2. `aws lambda get-policy --function-name inf-etf-ownership-daily` -> BOTH Sids present
   (`EventBridgeInfEtfOwnershipDaily` + `SchedFloorInfEtfOwnershipDaily`).
3. Next day ~19:05Z: TriggeredRules datapoint on the floor rule AND
   `daily/inflection/{date}.json` LastModified advanced past 19:00Z (idempotent re-emit observed).
   That third check is the behavioral one; 1-2 alone are config reads (Rule 22a).

---

## 3. Design B (CTO condition 3): the MDPF compute role's read of the consumed artifact

**Measured tonight:** `mdpf-daily-runner-ec2-role` -> `s3:GetObject` on
`arn:aws:s3:::opal-data-etfs/daily/inflection/2026-07-28.json` = **implicitDeny** (single-arn
simulate; positive control `silver/*` allowed and negative control `opal-data-cot` implicitDeny, each
a separate invocation). `opal-data-etfs` has NO bucket policy; the identity policy is the whole story.

### 3.1 The edit (inline policy `mdpf-runner-scoped` on `mdpf-daily-runner-ec2-role`, via its TF source, post-freeze)

```jsonc
// NEW statement (narrowest that serves the re-point -- inflection only, not daily/*):
{
  "Sid": "EtfsDailyInflectionReadMdpfConsume",
  "Effect": "Allow",
  "Action": ["s3:GetObject"],
  "Resource": "arn:aws:s3:::opal-data-etfs/daily/inflection/*"
}

// EXISTING Sid EtfsListScoped -- extend the prefix condition:
"Condition": { "StringLike": { "s3:prefix": ["silver/*", "daily/inflection/*"] } }
```

Scope note: `daily/inflection/*` only. The cot/bd legs are not consumed by MDPF; wider read
(`daily/*`) is cheap but unearned -- widen when a consumer exists, not before.

### 3.2 Post-apply verification

- simulate `s3:GetObject` on the exact next-day key -> allowed [single-arn], positive control
  (`silver/*`) + negative control (`daily/cottonwood/*` -> expect implicitDeny, proving the narrow
  scope held) as separate invocations.
- Behavioral: the first post-re-point chain run's own log reading the artifact.

### 3.3 What needs NO change (verified, not assumed)

- Feeder-output write path: N/A under CONSUME (DS~A's feeder becomes a cross-check, runs where QA
  runs it).
- Fan-in fence: `opal-assets-one-way-fan-in-fence` is NOT attached to the runner role (full census:
  `[AmazonSSMManagedInstanceCore]` + inline `mdpf-runner-scoped`). CLOSED for the runner path;
  re-opens only if some future activation lands a new Lambda/new role.
- Runner input reads for the cross-check feeder (orion silver) already allowed
  (`AssetsRevampSilverRead`), exercised simulate-allowed.

---

## 4. Sequencing (per the COO verdict: BEFORE or WITH, never after)

1. Freeze lifts (07-29's three unattended fires land -- owner: base AE / CTO; not this lane).
2. **One apply window, both designs:** A (floor) + B (read grant) as targeted safe-apply legs;
   NEVER#6 finish-in-session discipline; deploy-completion ledger opened at start, closed at end.
3. The aggregator-side consume change (DS lane, Rule 13) lands WITH or AFTER the apply -- never
   before it (the read grant must exist before the code that needs it runs).
4. DS~A's feeder stays DORMANT as the cross-check instrument; activation of anything remains CTO GO.

## 5. Standing-prohibition conformance

- **No alarms, monitors, SNS, SES, freshness checkers built or designed** (moratorium, Andrew-direct
  07-28). The mdpf floor's DLQ pattern was deliberately NOT mirrored here -- it is not required for
  the gate, and reliability machinery on an unsettled route is the exact anti-pattern named. If CTO
  wants DLQ parity with mdpf-scheduled-floor at apply time, that is a one-resource add he can rule on.
- The finding "inf leg was sentinel-only" lands as this GATE design (owned blocking item), not as
  notification machinery.
- No apply, no deploy, no activation performed tonight. Commit-no-push (COO is push operator).
