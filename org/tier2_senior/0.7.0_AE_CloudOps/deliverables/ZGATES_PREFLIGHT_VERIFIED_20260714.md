# Z-plane gate-opener: Gate A + Gate B PRE-FLIGHT VERIFIED (execution HELD pending Andrew routing)

**Lane:** 0.7.0_AE_CloudOps~Z (gate-opener) | **Date:** 2026-07-14 ~08:2xZ | **archetype:** VALIDATE
**Authority/brief:** 1d9f9c4f6 (0.7.0~Z hand-in) + bd825cc93 (amend-1) | **Payload source:** 0.8.0~Z GATE-OPENER msg 20260714T081638Z

## Posture (binding)
Both gates are **read-only pre-flighted and match the delivered facts exactly**. The two irreversible
executions -- Gate A `--go` (CodeBuild) and Gate B `safe-apply` -- **remain HELD pending Andrew routing to
this lane** (per my brief + CTO~Z: both gates await Andrew routing; the one-applier base-0.7.0 concurrent-
apply residual is surfaced-not-adjudicated). 0.8.0~Z's payload is the FACTS, not the apply-GO.

## GATE A -- derive-image rebuild -- VERIFIED, helper landed
- **Mechanism:** CodeBuild `globgrph-derive-build`, source = S3 zip
  `s3://opal-313476888478-globgrph/build-source/derive-runner-source.zip` (repo-root arcnames; buildspec
  context = zip root). A missing Dockerfile COPY source fails the docker build LOUDLY (fail-safe, never
  ships broken).
- **Durable helper LANDED:** `infra/aws/globgrph/build-derive-image.sh` @ **fa46d289d** (NFRA_GRAPHUNI
  P1-B durable fix, homed to 0.7.0 per the note). Zip file set DERIVED from the Dockerfile COPY lines
  (never static) -> the fedobs follow-on COPY auto-syncs. DRY-RUN default (no cloud mutation); `--go`
  uploads + starts + polls the build. Rule 16: `zip` absent -> python zipfile.
- **Exercised (dry-run PASS):** 17 zip entries; all 15 COPY sources + Dockerfile + buildspec PRESENT;
  the new `infra/aws/globgrph/fedobs/fedobs_observe.py` present at the required path. Zip will NOT COPY-fail.

## GATE B -- globgrph one-applier module -- VERIFIED, target set pinned
- **State isolation:** backend key `globgrph/tfstate` (main.tf:19) -- DISTINCT from base's `opal-assets/
  tfstate`. No state-lock contention with the live base 0.7.0 session. (One-applier logical residual is a
  separate, Andrew-not-adjudicated concern; a plan holds no durable lock.)
- **Full module plan:** `terraform plan` = **7 add / 1 change / 0 destroy** (matches 0.8.0~Z EXACTLY).
  - 6 fedobs creates: `aws_cloudwatch_log_group.fedobs_producer`, `aws_ecs_task_definition.fedobs_producer`,
    `aws_iam_role.fedobs_producer_events`, `aws_iam_role_policy.fedobs_producer_events_ecs`,
    `aws_cloudwatch_event_rule.fedobs_producer_nightly`, `aws_cloudwatch_event_target.fedobs_producer_nightly`.
  - **THE EXCLUSION (must NOT land):** `aws_sns_topic_subscription.critical_surface_alerts_email`
    (item2c_surface_alarm.tf:30, andrew@opalinvest.com) -- Andrew cfb741306 no-alerts posture; CVO~Z cert flag.
  - **THE 1-CHANGE (out of scope, leave):** `aws_lambda_function.freeze_monitor` in-place -- benign
    `source_code_hash` drift (`mgiyqef...` -> `NYx6OG8...`); the `data.archive_file` recomputes the compdiff
    zip hash each plan and the source drifted after its 2026-07-08 apply. Not mine to land.
- **Targeted plan (the 6 only):** `terraform plan -target=<6 fedobs>` = **6 add / 0 change / 0 destroy**
  (proves the SNS sub AND freeze_monitor are both excluded by the target set). APPLY COMMAND WHEN ROUTED:
  `.tools/safe-apply.sh` in `infra/aws/terraform/globgrph/` with exactly those 6 `-target=` flags.

## Reconciliations (map-vs-territory, verification law 6)
- **item2d header "*** PROPOSED -- NOT YET APPLIED ***" is STALE** -- `freeze_monitor` IS live
  (id `opal-globgrph-freeze-monitor`, last_modified 2026-07-08). The declarative record drifted from the
  applied truth. (Not correcting the comment mid-gate; flagged for the item2d owner.)
- **item2c SMS sub already applied** -- `critical_surface_alerts_sms` is absent from the plan (in state);
  only the email sub is the pending create. The 7/1/0 is fully accounted.

## Post-apply handshake (checklist items 4-5, run AFTER the routed apply)
1. `simulate-principal-policy` on the NEW `opal-globgrph-fedobs-producer-events` role: `ecs:RunTask` on the
   task-def ARN, ONE `--resource-arns`/call, positive control a SEPARATE invocation (role does not exist
   pre-apply, so this is strictly post-apply).
2. First-run exercise (scheduled 04:30Z or a manual `ecs run-task`) -> `marker_pin.pinned=true` +
   `verified_stable=true` on served `fedobs_observations.json`. CVO~Z re-takes the UNVERIFIED-PENDING-APPLY
   limb on that evidence; 0.8.0~Z's 7 held PROMOTE candidates start advancing.
3. NEVER#5 deploy-completion ledger opened at apply-start, closed at handshake.
4. PREREQ ordering: Gate A (image with fedobs) must be rebuilt BEFORE the first fedobs producer run
   succeeds -- but Gate B (the task-def/schedule) can land first; the schedule is 04:30Z.

## Compiler Tools
| Tool | Situation | Result |
|---|---|---|
| terraform init/plan (full + targeted) | Gate B delta enumeration | PASS -- 7/1/0 full, 6/0/0 targeted |
| build-derive-image.sh --dry-run | Gate A zip verification | PASS -- 17 entries, fedobs present |
| commit-gate | n/a (.sh not .py) | build helper is bash; bash -n clean |
