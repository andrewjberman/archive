# CG-s-18 -- the four `:latest` producers pinned by digest (NFRA_CLDGRPH.TO-CG-E-2)

**Seat:** `0.9.0_WK_NFRA_CLDGRPH~1` (spine-v3 worker of `2.0.0_SA_COO~A`) · **Branch:** `wk-cldgrph-5-1`, LOCAL, never pushed
**Worktree:** `C:/tmp/wk-cldgrph-5-1` · **Spawn HEAD:** `de466829e0` · **Terraform:** `.tools/terraform.exe` v1.9.8, provisioned by the issuer, never the PATH substitute
**Ledger:** `org/critical_paths/change_management/20260909T1555Z_cldgrph-cgs18-four-producers-digest-pin_deploy_completion.md` -- CLOSED, 5 of 5 legs proven

```json
{
  "row": "CG-s-18",
  "rule": "R13 (PRD v0.5 s.6) -- no globgrph task family references a mutable image tag; every image act's change-management entry names every family that pulls the tag it moves",
  "pinned_digest": "sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778",
  "digest_source": "local.globgrph_image_digest, infra/aws/terraform/globgrph/serving.tf:22 @de466829e0 -- the 2026-09-04T08:03:52Z build of HEAD 5644fee152 carrying the C-3 deriver fix b5bc1c8b27",
  "families": [
    {"family": "globgrph-comp-learns-producer",       "role": "MOVED BY THIS ACT", "before": {"revision": 1, "image": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner:latest"}, "after": {"revision": 2, "image": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778"}, "launcher": "aws_cloudwatch_event_target.comp_learns_producer_nightly -- EventBridge rule opal-globgrph-comp-learns-producer-nightly, cron(0 4 * * ? *), ENABLED; live TaskDefinitionArn .../globgrph-comp-learns-producer:2 (was :1)"},
    {"family": "globgrph-cse-producer",                "role": "MOVED BY THIS ACT", "before": {"revision": 1, "image": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner:latest"}, "after": {"revision": 2, "image": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778"}, "launcher": "aws_scheduler_schedule.cse_producer_nightly -- EventBridge Scheduler globgrph-cse-producer-nightly, cron(30 3 * * ? *) UTC, ENABLED; live TaskDefinitionArn .../globgrph-cse-producer:2 (was :1)"},
    {"family": "globgrph-fedobs-producer",             "role": "MOVED BY THIS ACT", "before": {"revision": 1, "image": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner:latest"}, "after": {"revision": 2, "image": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778"}, "launcher": "aws_cloudwatch_event_target.fedobs_producer_nightly -- EventBridge rule opal-globgrph-fedobs-producer-nightly, cron(30 4 * * ? *), ENABLED; live TaskDefinitionArn .../globgrph-fedobs-producer:2 (was :1)"},
    {"family": "globgrph-resource-summaries-producer", "role": "MOVED BY THIS ACT", "before": {"revision": 1, "image": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner:latest"}, "after": {"revision": 2, "image": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778"}, "launcher": "NONE -- no declared launcher and none on the applied plane either (rules, schedules and pipes all censused). Hand-run: ecs run-task. Row W1-S28"},
    {"family": "globgrph-derive-runner",     "role": "ALREADY PINNED BY CG-s-15, NOT TOUCHED", "before": {"revision": 7, "image": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778"}, "after": {"revision": 7, "image": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778"}, "launcher": "aws_cloudwatch_event_rule opal-globgrph-derive-runner-nightly -- live TaskDefinitionArn .../globgrph-derive-runner:7, UNCHANGED by this apply"},
    {"family": "globgrph-projection-worker", "role": "ALREADY PINNED BY CG-s-15, NOT TOUCHED", "before": {"revision": 4, "image": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778"}, "after": {"revision": 4, "image": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778"}, "launcher": "EventBridge Pipe opal-globgrph-projection-worker, UNCHANGED by this apply"},
    {"family": "globgrph-serving",           "role": "ALREADY PINNED BY CG-s-15, NOT TOUCHED", "before": {"revision": 2, "image": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778"}, "after": {"revision": 2, "image": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778"}, "launcher": "aws_ecs_service.globgrph_serving (always-on), UNCHANGED by this apply"}
  ],
  "not_in_this_population": ["globgrph-nessie", "globgrph-trino"],
  "not_in_this_population_reason": "both run OTHER images and reference no opal-globgrph-derive-runner tag, so a pin has nothing to move for them; named here because R13's manifest obligation is about the families that PULL THE TAG",
  "address_list_applied": [
    "aws_ecs_task_definition.comp_learns_producer",
    "aws_ecs_task_definition.cse_producer",
    "aws_ecs_task_definition.fedobs_producer",
    "aws_ecs_task_definition.resource_summaries_producer",
    "aws_cloudwatch_event_target.comp_learns_producer_nightly",
    "aws_cloudwatch_event_target.fedobs_producer_nightly",
    "aws_scheduler_schedule.cse_producer_nightly",
    "aws_iam_role_policy.comp_learns_producer_events_ecs",
    "aws_iam_role_policy.cse_producer_scheduler_ecs",
    "aws_iam_role_policy.fedobs_producer_events_ecs"
  ],
  "plan_lines": {
    "targeted_pre":  "Plan: 4 to add, 6 to change, 4 to destroy.   (targeted_plan_e2.txt; exactly the ten addresses, no foreign address)",
    "apply":         "Apply complete! Resources: 4 added, 6 changed, 4 destroyed.   (targeted_apply_e2.txt, rc 0)",
    "targeted_post": "No changes. Your infrastructure matches the configuration.   (targeted_plan_post_e2.txt)",
    "unscoped_control": "Plan: 6 to add, 8 to change, 4 to destroy.   (unscoped_plan_pre_e2.txt, run before the apply, NEVER applied; 14 addresses = the ten above plus four foreign)"
  },
  "unscoped_foreign_items_left_as_found": [
    "aws_glue_partition.tool_activity[\"rolling_log\"] -- update in place",
    "aws_glue_partition.tool_activity[\"rolling_log_summary\"] -- update in place",
    "aws_glue_partition.tool_activity[\"routing\"] -- create",
    "aws_sns_topic_subscription.critical_surface_alerts_email -- create"
  ],
  "ecr_latest_digest": {
    "before": "sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778",
    "after":  "sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778",
    "moved": false
  },
  "criteria": {
    "E2-AC1": "PINNED_BY_DIGEST=7 of 7",
    "E2-AC2": "DIGEST_MATCHES_LOCAL=4 of 4",
    "E2-AC3": "TARGETS_ON_PINNED_REVISION=3 of 3 declared launcher(s)",
    "E2-AC4": "LATEST_DIGEST_UNCHANGED=true",
    "E2-AC5": "1",
    "E2-AC6": "FMT_RC=0",
    "E2-AC7": "RECORDED (judgment; graded by 3.0.0_SA_CVO at L9)"
  },
  "rows_filed": ["NFRA_CLDGRPH-W1-S27", "NFRA_CLDGRPH-W1-S28", "NFRA_CLDGRPH-W1-S29", "NFRA_CLDGRPH-W1-S30", "NFRA_CLDGRPH-W1-S31"]
}
```

## E2-AC7 -- the blast-radius reading under R13 (a reading act; no verdict, graded by `3.0.0_SA_CVO` at L9)

**Which families moved, which did not, and why.** Four moved: `globgrph-comp-learns-producer`,
`globgrph-cse-producer`, `globgrph-fedobs-producer`, `globgrph-resource-summaries-producer`, each from
ACTIVE revision 1 to ACTIVE revision 2, each from the tag `opal-globgrph-derive-runner:latest` to
`opal-globgrph-derive-runner@sha256:1b89853f...`. Three did not: `globgrph-derive-runner` (rev 7),
`globgrph-projection-worker` (rev 4), `globgrph-serving` (rev 2) were pinned to this same digest by
CG-s-15 and their revisions read identically before and after this apply -- which is the evidence that
the act moved four families and not seven, rather than a claim that it did.

**The pin changed WHICH REFERENCE, not WHICH BYTES.** The ECR tag `:latest` resolved to
`sha256:1b89853f...` before this order's first act and resolves to the same digest now, and that is the
digest the three CG-s-15 families have run since 2026-09-04. So the four producers were already pulling
these exact bytes on every nightly fire; nothing about their runtime behaviour changes today. What
changes is the failure mode they were exposed to: a tag is a mutable pointer, and until this apply a
rebuild anywhere in the estate would have re-pointed four production families silently and with no
Terraform-plane diff to see it. That is NEVER-2's whole subject and R13's whole subject.

**What the targeted plan carried beyond the four task definitions, and why `-target` was right to pull
it.** Ten addresses, not four. Beyond the four task definitions:

- **Three declared launchers** -- `aws_cloudwatch_event_target.comp_learns_producer_nightly`,
  `aws_cloudwatch_event_target.fedobs_producer_nightly`, `aws_scheduler_schedule.cse_producer_nightly`.
  Each references `aws_ecs_task_definition.<x>.arn`, and an ECS task-definition ARN *carries its
  revision*. A task-definition edit is a REPLACE (4 destroyed + 4 added in the apply line is the
  revision bump, not a deletion of anything running), so every launcher had to be re-pointed from `:1`
  to `:2` in the same apply. All three read `:1` before and `:2` after, so the re-point is measured as
  a move.
- **Three launcher-role IAM policies** -- `aws_iam_role_policy.comp_learns_producer_events_ecs`,
  `.cse_producer_scheduler_ecs`, `.fedobs_producer_events_ecs`. Their `ecs:RunTask` `Resource` is the
  SAME revision-scoped ARN (`comp_learns_producer.tf:131`: `Resource = aws_ecs_task_definition.comp_learns_producer.arn`).
  **This is the leg that makes the difference between a green apply and a broken pipeline.** Had the
  apply been scoped to the four task definitions and the three launchers, each launcher would have been
  pointed at revision 2 while its role remained authorized only for revision 1, and the next nightly
  fire of all three producers would have failed AccessDenied -- silently, from a deploy that reported
  success. That is precisely the hazard row `NFRA_CLDGRPH-W1-S2` recorded on CG-s-15's apply, where the
  face named four addresses and the plan carried eight; the same shape recurred here with four named
  and ten carried, and it was found the same way: by reading the plan's address census rather than the
  face's list.

**What the unscoped plan's foreign items were, and why they were left.** The unscoped plan (run against
the live S3 backend *before* the apply, never applied) carried 14 addresses -- the ten above plus four:
`aws_glue_partition.tool_activity["rolling_log"]` and `["rolling_log_summary"]` (in-place),
`aws_glue_partition.tool_activity["routing"]` (create), and
`aws_sns_topic_subscription.critical_surface_alerts_email` (create). All four are pre-existing drift
that CG-s-15's own unscoped control recorded on 2026-09-04, and all four are outside this row's cell.
The SNS subscription is the one that matters to name: it is the alert wiring the standing posture keeps
DOWN and the C3 moratorium forbids this order to land, so an unscoped `apply` here would have armed an
email alert nobody asked for as a side effect of an image pin. That is the reason the unscoped plan is
a **control asserted by address list** and never an apply. (One foreign item present in D-1's control,
`aws_codebuild_project.stitch_produce`, is absent from this one -- it has been resolved since, and I
note the difference rather than assume the two lists must match.)

**Whether the change-management entry names every family that pulls the tag.** Yes, and by construction
rather than by good intent: the entry
`org/critical_paths/change_management/20260909T1555Z_cldgrph-cgs18-four-producers-digest-pin_deploy_completion.md`
was opened BEFORE any edit and BEFORE the apply, and its `**Deploy:**` line enumerates all seven
families with their pre-act ACTIVE revisions -- the four moved (each rev 1) and the three already pinned
(revs 7, 4, 2) -- and states explicitly that `globgrph-nessie` and `globgrph-trino` are not in this
population because they run other images. Every leg L1..L5 carries its own measured proof and the entry
is CLOSED. The R13 obligation is on the entry, and the entry satisfies it.

**How `resource_summaries_producer` is launched.** By hand, and the absence is not merely local to this
Terraform tree. Three independent live instruments were run and none finds an automated launcher:
`events list-rules` over the whole default bus with `list-targets-by-rule` on every rule returns exactly
three rules carrying an ECS `TaskDefinitionArn` (comp-learns, derive-runner, fedobs); `scheduler
list-schedules` returns 19 schedules of which one is globgrph (`globgrph-cse-producer-nightly`); `pipes
list-pipes` returns one pipe (`opal-globgrph-projection-worker`). Its Terraform declares only an output
(`resource_summaries_producer.tf:185-189`) whose own description reads *"manual run-task: the create +
AC-2 seed + the append-only re-fire"*, and its log group holds exactly three streams, all inside a
13-minute window on 2026-07-18 (20:58:14Z, 21:08:15Z, 21:11:04Z) -- one seeding session, matching that
description exactly, and nothing since. So E2-AC3's denominator is the launchers FOUND (3 of 3), as the
criterion words it, and this family is printed by name rather than counted as a miss. **The consequence
for the L9 read is worth stating plainly:** the "next scheduled fire" acceptance exists for cse
(03:30Z), comp-learns (04:00Z) and fedobs (04:30Z) and does NOT exist for this fourth family. Its pin is
verified on the DECLARED and APPLIED planes and cannot be verified at EXERCISED without someone running
it -- which this order is forbidden to do (BOUNDS: no `run-task`). Filed as row W1-S28.

**What this order did NOT do, stated because a reader cannot see an absence.** No image was rebuilt,
pushed or re-tagged (E2-AC4's before/after bracket is the control and it can fail); no
`ecs update-service`, no `run-task`, no `stop-task`, so no launch was provoked; no marker, pointer or
`projection/` object was written; nothing in `.tools/` was edited; the three fmt-dirty files elsewhere
in the tree were left dirty because they are outside the write grant; `serving.tf` was read and not
written, which is why its now-false comment travels as row W1-S30 instead of a fix.

## Surprise rows filed (5)

| id | class | standing | one-line |
|---|---|---|---|
| `NFRA_CLDGRPH-W1-S27` | OBSERVATION | ARMED (`1.0.0_SA_CTO`) | W1-S11 recurred unchanged on a fresh worktree: the halt gate's worker limb is intact in VALIDATION but unreachable because RESOLUTION reads only the session-keyed serial file, never `OPAL_AGENT_SERIAL` |
| `NFRA_CLDGRPH-W1-S28` | OBSERVATION | INERT | `globgrph-resource-summaries-producer` has no launcher on the applied plane either -- hand-run; three log streams, one session, 2026-07-18 |
| `NFRA_CLDGRPH-W1-S29` | OBSERVATION | ARMED (`2.0.0_SA_COO~A`) | three of the four files were fmt-dirty AT HEAD in regions the eight lines never touch, so E2-AC6 and the "nothing else in Terraform" bound could not both be met by the eight |
| `NFRA_CLDGRPH-W1-S30` | OBSERVATION | ARMED (`2.0.0_SA_COO~A`) | this act falsified `serving.tf:11-16` ("the four producers stay on `:latest` by design") and `serving.tf` is read-only for this order |
| `NFRA_CLDGRPH-W1-S31` | OBSERVATION | ARMED (`2.0.0_SA_COO~A`) | one slot's deliverables folder is reused across rounds: the plan/apply captures collided with TO-CG-D-1's and were silently replaced; repaired same turn, verified byte-identical |
