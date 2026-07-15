# OPAL_STNDRD phase 3 -- twin schedules, STAGED PATCH (not committed into family modules)

**From:** 0.7.0_AE_CloudOps~Z | **Date:** 2026-07-15 ~21:1xZ | **Status:** STAGED -- these blocks
land in their family modules ONLY in the arm-window commit immediately preceding the CTO-gated
apply. Committing them earlier would inject my resources into ~B's / CTO's / 0.5.0's next plan on
shared modules mid-drive (the concurrent-writer surprise the Z1 scope pin forbids), and would read
as module drift on drift-check-resource-map until applied.

**Prereq:** the checker module (infra/aws/terraform/opal-assets-absence/, plan 5/0/0) is APPLIED
first -- family twins resolve it live via data sources (no remote-state coupling):

```hcl
data "aws_lambda_function" "absence_check" {
  function_name = "opal-assets-absence-check"
}

data "aws_iam_role" "absence_twin_scheduler" {
  name = "opal-assets-absence-twin-scheduler-role"
}

locals {
  absence_cfg = jsondecode(file("${path.module}/../../lambda/ci/absence-config.json"))
}
```

Every twin renders Target.input from the REGISTRY (absence-config.json) -- config change = plan
diff at the gate, zero lambda code (CTO pin i). One `aws_lambda_permission` per family module is
NOT needed: Scheduler invokes via the twin-scheduler ROLE (lambda:InvokeFunction grant lives in
the checker module), not via resource policy.

## opal-assets module (mirror-cot + bd49f) -- ~B-adjacent: inf twin EXCLUDED (paused row, no schedule)

```hcl
# cot mirror lands 03:30Z -> twin 05:00Z
resource "aws_scheduler_schedule" "mirror_cot_absence_twin" {
  name                = "opal-assets-ingest-mirror-cot-absence-check-daily"
  state               = "ENABLED"
  schedule_expression = "cron(0 5 * * ? *)"
  flexible_time_window { mode = "OFF" }
  target {
    arn      = data.aws_lambda_function.absence_check.arn
    role_arn = data.aws_iam_role.absence_twin_scheduler.arn
    input = jsonencode(merge(
      local.absence_cfg.units["opal-assets-ingest-mirror-cot"],
      { alarm_topic_arn = local.absence_cfg.alarm_topic_arn }
    ))
  }
}

# bd49f pull 02:30Z + reattempt 04:30Z -> twin 06:00Z (post-reattempt)
resource "aws_scheduler_schedule" "bd49f_absence_twin" {
  name                = "opal-assets-bd49f-daily-pull-absence-check-daily"
  state               = "ENABLED"
  schedule_expression = "cron(0 6 * * ? *)"
  flexible_time_window { mode = "OFF" }
  target {
    arn      = data.aws_lambda_function.absence_check.arn
    role_arn = data.aws_iam_role.absence_twin_scheduler.arn
    input = jsonencode(merge(
      local.absence_cfg.units["opal-assets-bd49f-daily-pull"],
      { alarm_topic_arn = local.absence_cfg.alarm_topic_arn }
    ))
  }
}
```

## canonical-schwab-ec2 module (si2 x2) -- twin fires after each master's LAST daily pull

```hcl
# 0824 pulls 10:15/22:15Z -> twin 23:45Z
resource "aws_scheduler_schedule" "si2_0824_absence_twin" {
  name                = "canonical-schwab-si2-08242234-absence-check-daily"
  state               = "ENABLED"
  schedule_expression = "cron(45 23 * * ? *)"
  flexible_time_window { mode = "OFF" }
  target {
    arn      = data.aws_lambda_function.absence_check.arn
    role_arn = data.aws_iam_role.absence_twin_scheduler.arn
    input = jsonencode(merge(
      local.absence_cfg.units["canonical-schwab-si2-08242234"],
      { alarm_topic_arn = local.absence_cfg.alarm_topic_arn }
    ))
  }
}

# 0833 pulls 09:45/21:45Z -> twin 23:15Z
resource "aws_scheduler_schedule" "si2_0833_absence_twin" {
  name                = "canonical-schwab-si2-08335338-absence-check-daily"
  state               = "ENABLED"
  schedule_expression = "cron(15 23 * * ? *)"
  flexible_time_window { mode = "OFF" }
  target {
    arn      = data.aws_lambda_function.absence_check.arn
    role_arn = data.aws_iam_role.absence_twin_scheduler.arn
    input = jsonencode(merge(
      local.absence_cfg.units["canonical-schwab-si2-08335338"],
      { alarm_topic_arn = local.absence_cfg.alarm_topic_arn }
    ))
  }
}
```

NOTE: path depth differs per module -- `${path.module}/../../lambda/ci/...` assumes the module
sits at infra/aws/terraform/<module>/; verify relative depth at land time per module.

## etfs-netassets module (etf twin) -- arms ONLY after the C4 parity window proves the scheduled leg

```hcl
# run 22:00Z -> twin 23:30Z
resource "aws_scheduler_schedule" "etfs_absence_twin" {
  name                = "etfs-netassets-daily-absence-check-daily"
  state               = "ENABLED"
  schedule_expression = "cron(30 23 * * ? *)"
  flexible_time_window { mode = "OFF" }
  target {
    arn      = data.aws_lambda_function.absence_check.arn
    role_arn = data.aws_iam_role.absence_twin_scheduler.arn
    input = jsonencode(merge(
      local.absence_cfg.units["etfs-netassets-daily"],
      { alarm_topic_arn = local.absence_cfg.alarm_topic_arn }
    ))
  }
}
```

## Sequencing (all at CTO's safe-apply gate, plan-shape RAVC each)

1. Checker module apply (plan 5/0/0 saved: phase3-checker.tfplan) -- post-apply: LIVE
   simulate-principal-policy on the checker role (one --resource-arns per call, positive control
   separate, Rule 22a) + a controlled live-alarm exercise at CTO's word (real SNS publish once).
2. opal-assets twins (cot + bd49f) -- expect 2/0/0. (inf twin: NO schedule until ~B's hold-lift
   MCP; the paused registry row is the visible record.)
3. si2 twins -- expect 2/0/0.
4. etf twin -- expect 1/0/0, sequenced behind C4 parity (3 trading days).
5. Post-apply each wave: trigger-census.py --build re-emits trigger-map.json (the census's
   absence_twin linkage picks the new schedules up); tag modules per Rule 6.

## Census refinement owed at arm time

The `conforms` heuristic compares the name's unit segment to the TARGET's name -- an absence twin
targets the shared CHECKER, so twins will read grammar-debt falsely. Refinement: for
function == absence-check rows, conforms = name matches `{registry-unit}-absence-check-{cadence}`
against absence-config.json. Land with the first twin wave so the census never lies about its own
instrument family.
