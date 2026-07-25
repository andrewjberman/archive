<task_order>
  <metadata>
    <id>1.0.0_SA_CTO~Z-2026-07-25-critical-surface-alerts-email-sub</id>
    <issued_by>1.0.0_SA_CTO~Z</issued_by>
    <issued_to>0.8.0_AE_CloudComp</issued_to>
    <date>2026-07-25</date>
    <status>staged</status>
    <project_code>NFRA_TOOLUNIFY</project_code>
  </metadata>

  <objective>
    Apply the already-declared-but-never-applied email subscription on the `opal-critical-surface-alerts`
    SNS topic, so a real SEV1/SEV2 finding (from `derive_runner`'s nightly scan or `incremental_updater`'s
    commit-failure path) reaches a human. This is the "visibility fix, do NOW" item from NFRA_TOOLUNIFY's
    census (§0.2 through-line, instance: "alerting queue with 476+ unconsumed messages, missing email sub")
    -- Andrew-approved this session ("Agreed proceed it").
  </objective>

  <context>
    Census finding (`org/tier1_exec/1.0.0_SA_CTO/deliverables/NFRA_TOOLUNIFY_CENSUS/base.md` §7): the SNS
    topic's own Terraform (`infra/aws/terraform/globgrph/item2c_surface_alarm.tf:30-34`) ALREADY DECLARES
    an email subscription to `andrew@opalinvest.com` -- this is a DESIRED-vs-APPLIED gap (Rule 22a), not a
    missing-design gap. Live AWS state at census time showed exactly 2 subscriptions (an SQS queue
    `opal-critical-surface-alerts-coo` and an SMS number) and explicitly **no email subscription, confirmed
    or pending**. The `.tf` file's own comment documents the full remediation plan: email is the PRIMARY
    channel (SES/email is non-sandboxed; SNS-SMS is sandboxed and confirmed non-delivering,
    Delivered=0/Failed=1); SMS is retained as a stopgap ONLY until email is confirmed-delivering, then
    removed in a LATER pass (not this TO -- that removal is gated on Andrew's confirmation, do not do it
    now).

    Ground truth first: `terraform plan` scoped to this file may already show the drift directly. Confirm
    against LIVE AWS (`aws sns list-subscriptions-by-topic --topic-arn <arn>`), not just the plan output --
    a plan can be stale relative to a manually-modified topic.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before applying):
      <run>comp-iam gaps</run>
      <expect>no new permission gaps introduced by this file (it's pre-existing, unchanged policy)</expect>
      <if_mismatch>flag to CTO~Z before proceeding -- unexpected IAM drift on an unrelated apply is worth a pause</if_mismatch>
      <run>aws sns list-subscriptions-by-topic --topic-arn <critical_surface_alerts topic ARN, from `terraform output critical_surface_alerts_topic_arn` or `aws sns list-topics`></run>
      <expect>confirms the PRE-apply live state: 2 subscriptions (SQS + SMS), 0 email -- matches the census finding exactly</expect>
      <if_mismatch>if live state has already changed since the census (e.g. an email sub now exists), STOP -- do not apply, the finding may be stale. Report to CTO~Z instead of proceeding.</if_mismatch>

    Phase 2 (before committing -- N/A, no code change; this is a state-reconciliation apply of an
    already-committed .tf file, not a new commit):
      <run>none -- item2c_surface_alarm.tf is unchanged; this TO applies existing Terraform, does not edit it</run>

    Phase 3 (after apply):
      <run>aws sns list-subscriptions-by-topic --topic-arn <same ARN></run>
      <expect>3 subscriptions now: SQS + SMS (unchanged) + email to andrew@opalinvest.com with
      SubscriptionArn == "PendingConfirmation" (NOT yet "Confirmed" -- that requires Andrew's manual
      one-time email click, out of this TO's scope)</expect>
      <if_mismatch>if the email sub still doesn't appear after apply, the apply itself failed silently or
      hit a different error -- do not report SAFE, escalate to CTO~Z with the full apply output</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
    (Single-file Terraform apply, no other active TO touches item2c_surface_alarm.tf or the
    opal-critical-surface-alerts topic.)
  </cross_domain_coordination>

  <acceptance_criteria>
    <!-- Easiest-pass test applied: "terraform apply exits 0" is NOT sufficient -- that could pass against
    a stale/cached state without ever touching live AWS, or could apply a NO-OP if the resource already
    exists in state but was deleted out-of-band. The criterion below is grounded on the LIVE PRIMITIVE.

    Missing-third-state test applied: three states exist for the email subscription -- ABSENT (fails),
    PENDING CONFIRMATION (this TO's actual, achievable target), CONFIRMED (requires Andrew's manual click,
    NOT achievable by this TO -- do not write a criterion that can only pass once Andrew acts, that would
    silently block the TO on a step outside the assignee's control). -->

    1. `aws sns list-subscriptions-by-topic --topic-arn <arn>` (LIVE, post-apply) shows exactly 3
       subscriptions: the pre-existing SQS + SMS (unchanged) PLUS a new email subscription to
       `andrew@opalinvest.com` with `SubscriptionArn: "PendingConfirmation"`. Anything else (still 2 subs,
       or an email sub that errored) = NOT complete.
    2. `terraform plan` scoped to `item2c_surface_alarm.tf` after apply shows 0 pending changes for the
       `aws_sns_topic_subscription.critical_surface_alerts_email` resource specifically (DESIRED == APPLIED
       for this one resource -- do not assert this for the whole file/state, only this resource).
    3. The SMS subscription (`+17862617679`) is UNCHANGED and still present -- this TO does NOT remove it
       (that removal is gated on email confirming-delivering, a later and separate action).
    4. Session log states the exact `SubscriptionArn` value returned for the new email sub (not "it worked"
       -- the actual PendingConfirmation ARN string, so it's independently verifiable).
  </acceptance_criteria>

  <scope>
    <files>
      <file action="reference">infra/aws/terraform/globgrph/item2c_surface_alarm.tf</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Apply via `.tools/safe-apply.sh` only (never bare `terraform apply`) -- CLAUDE.md
    Deployment Rule / NEVER-rule.</requirement>
    <requirement id="2">Scope the apply to this resource if possible (`-target=aws_sns_topic_subscription.critical_surface_alerts_email`)
    to avoid touching unrelated drift elsewhere in the same state; if a scoped apply isn't clean, escalate
    to CTO~Z rather than applying the whole file blind.</requirement>
    <requirement id="3">After apply, tell Andrew directly (not just log it) that a confirmation email will
    land at andrew@opalinvest.com and needs a one-time click -- the subscription is not live until he
    confirms it.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">None expected -- Terraform file is unchanged, this is a state-reconciliation apply. If `terraform plan` surfaces unexpected additional drift beyond the email subscription, STOP and report -- do not silently apply more than this TO scopes.</deliverable>
    <deliverable type="document">Session log with Compiler Tools section, the live pre/post subscription list, and the PendingConfirmation ARN.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT remove the SMS subscription -- that's a separate, later action gated on email confirming-delivering.</rule>
    <rule>Do NOT touch the SQS queue (`opal-critical-surface-alerts-coo`, 477 unconsumed messages, 0 consumers) -- that is a SEPARATE open question (does it need a Lambda consumer wired, or is it an intentional passive drain?) and is explicitly OUT OF SCOPE for this TO. Flag it back to CTO~Z as a distinct follow-on if you have a view, do not fix it unilaterally.</rule>
    <rule>Do NOT run a bare `terraform apply` -- `.tools/safe-apply.sh` only.</rule>
    <rule>Do NOT report SAFE/complete based on `terraform apply` exit code alone -- the acceptance criteria require the LIVE `list-subscriptions-by-topic` read, both before and after.</rule>
  </do_not>
</task_order>
