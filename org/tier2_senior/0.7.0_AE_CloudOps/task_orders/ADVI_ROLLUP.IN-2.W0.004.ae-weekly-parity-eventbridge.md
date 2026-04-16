<task_order>
  <metadata>
    <id>ADVI_ROLLUP.IN-2.W0.004</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- GO 2026-04-16T13:42Z; complete 2026-04-16. Commits b37262c7 + beda05a6. Tag bd-v2.24.4. Lambda-direct substitution (CTO GO 20260416T165521Z). -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>7 — IN Wave 0 Foundation</wave>
    <priority>P1 (defense-in-depth — catches silent FIFO drift post-promotion)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/INCREMENTAL_RUNS_DESIGN.md §5 (weekly parity check) + §7 Wave 0 + §9 acceptance #3</ref>
    <ref type="prereq">ADVI_ROLLUP.IN-2.W0.003 (comp-incrparity tool)</ref>
  </references>

  <objective>
    Wire EventBridge rule to fire `comp-incrparity ALL --mode quick` every Sunday 06:00 UTC. Any FAIL pages COO + CTO via CloudWatch alarm + SNS topic.

    **Execution target:** bd-gold-qa-runner (QA runner, not PROD) — parity checks are non-production verification, appropriate for QA instance. Run via SSM command, same pattern as existing gold chain dispatch but with `comp-incrparity ALL --mode quick` invocation instead of `gold_dispatch.sh`.

    **Alert route:**
    - CloudWatch alarm `ExecIncrParityFailure` fires on EXIT 1 from comp-incrparity.
    - SNS topic routes to existing COO + CTO oncall notification channel (same as other P1 alarms — reuse infra, don't create new).
    - Payload includes script_id + diff report S3 path for immediate triage.

    **Initial state:** `gold/meta/incremental_promoted.json` is empty `[]` at W0.004 ship time (no scripts promoted yet). `comp-incrparity ALL` exits 0 cleanly on empty list. Alarm is armed but won't fire until Wave 2+ scripts promote.

    **Terraform resources:**
    - `aws_cloudwatch_event_rule.incrparity_weekly` (Sunday 06:00 UTC)
    - `aws_cloudwatch_event_target` invoking SSM command on bd-gold-qa-runner
    - `aws_cloudwatch_metric_alarm.incrparity_failure`
    - IAM role for EventBridge → SSM → CloudWatch
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/terraform/bd-pipeline/eventbridge.tf (add incrparity_weekly rule)</file>
      <file action="modify">infra/aws/terraform/bd-pipeline/alarms.tf (add incrparity_failure alarm)</file>
      <file action="modify">infra/aws/terraform/bd-pipeline/iam.tf (EventBridge + SSM invoke permissions if not present)</file>
    </files>
  </scope>

  <wire_contract>
    Sunday 06:00 UTC: EventBridge fires SSM command on bd-gold-qa-runner → executes `comp-incrparity ALL --mode quick`. On EXIT 1, CloudWatch alarm `ExecIncrParityFailure` fires → SNS → oncall. When empty promoted list, clean pass.
  </wire_contract>

  <acceptance_criteria>
    1. EventBridge rule `incrparity_weekly` created with cron `cron(0 6 ? * SUN *)`.
    2. SSM target invokes `comp-incrparity ALL --mode quick` on bd-gold-qa-runner.
    3. CloudWatch alarm `ExecIncrParityFailure` armed, SNS route confirmed to oncall channel.
    4. IAM permissions verified (events:PutTargets, ssm:SendCommand, cloudwatch:PutMetricAlarm, sns:Publish all in place).
    5. `comp-iam gaps` returns no new permission gaps.
    6. Terraform 0-diff post-apply.
    7. Tag appropriate to pipeline (likely `bd-v2.24.x` if modifying bd-pipeline eventbridge.tf).
    8. Manual test fire: trigger EventBridge rule once via `aws events put-events` OR console; verify SSM command invokes + Lambda/comp-incrparity runs + alarm evaluates (clean PASS on empty promoted list).
    9. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.
    10. MCP COMPLETE to COO + CTO with: rule ARN, alarm ARN, tag + CHANGELOG entry, manual-fire verification transcript.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>ls infra/aws/terraform/bd-pipeline/ | grep -E '(eventbridge|alarm|iam)'</run>
        <expect>Existing Terraform files present for extension.</expect>
        <if_mismatch>Locate where EventBridge rules + alarms live in bd-pipeline module.</if_mismatch>
      </step>
      <step>
        <run>comp-iam service bd-gold-qa-runner | grep -iE '(ssm|events)'</run>
        <expect>Existing SSM + EventBridge permissions enumerated. Confirms IAM delta needed.</expect>
        <if_mismatch>Determine which IAM additions required.</if_mismatch>
      </step>
      <step>
        <run>aws sns list-topics | grep -i oncall</run>
        <expect>Existing oncall SNS topic ARN enumerable. Reuse, don't create new.</expect>
        <if_mismatch>Surface to COO — find/create the oncall route.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before apply">
      <step>
        <run>terraform plan</run>
        <expect>Only adds/modifies: EventBridge rule + alarm + minimal IAM; no unintended drift.</expect>
        <if_mismatch>Investigate.</if_mismatch>
      </step>
      <step>
        <run>terraform apply</run>
        <expect>Apply success.</expect>
        <if_mismatch>Surface to COO.</if_mismatch>
      </step>
      <step>
        <run>terraform plan</run>
        <expect>0-diff.</expect>
        <if_mismatch>Drift; fix before tag.</if_mismatch>
      </step>
      <step>
        <run>comp-iam gaps</run>
        <expect>No new gaps anywhere.</expect>
        <if_mismatch>Audit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after apply">
      <step>
        <run>aws events put-events --entries '[{"Source":"aws.events","DetailType":"Scheduled Event","Detail":"{}","Resources":["{incrparity_weekly rule ARN}"]}]'</run>
        <expect>SSM command invoked on bd-gold-qa-runner; comp-incrparity ALL runs (empty promoted list = exits 0 cleanly).</expect>
        <if_mismatch>Debug EB→SSM wiring.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - Reuses comp-incrparity tool from W0.003.
    - Reuses oncall SNS topic (no new topic); cross-team responsibility boundary.
    - bd-pipeline eventbridge.tf shared with gold-chain rules per bd-v2.24.1; coordinate commit window with AE 0.6 if they're editing bd-pipeline simultaneously.
  </cross_domain_coordination>

  <dependencies>
    <dependency to="ADVI_ROLLUP.IN-2.W0.003" status="complete" evidence="e05d2567"/>
  </dependencies>

  <next>
    W0.004 close = IN Wave 0 COMPLETE. Wave 1 (dispatcher whitelist) can dispatch once DH-1..DH-7 also closes. Wave 2+ can start per-script conversions with parity-gate coverage.
  </next>
</task_order>
