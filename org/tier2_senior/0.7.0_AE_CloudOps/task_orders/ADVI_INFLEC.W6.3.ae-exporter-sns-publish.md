<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w6.3-exporter-sns-publish</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>complete</status><!-- Verified 2026-04-29 AE TO sweep: inf-otp-alert SNS topic + exporter SNS:Publish IAM deployed (commit 554785087, W6.2 batch). -->
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Wire `orion_export.ts` to publish to `inf-otp-alert` SNS topic when exporter pauses at OTP screen. Replaces the passive "Andrew watches for Orion SMS" flow with an active push notification. Update script on inf-exporter EC2 via `safe-ec2-deploy.sh`.
  </objective>

  <context>PRD §6.3 + §5.3 Phase 3. Blocked on W6.2 (SNS topic + subscription) + W2.7 (exporter script already deployed). Small code change: add `sns.publish(TopicArn, Message="OTP pending for Orion export — poke s3://opal-data-inf/otp/current.txt with OTP")` at the OTP-wait entry point in orion_export.ts.</context>

  <compiler_tools_mandate>
    Phase 3:
    <run>comp-iam service inf-exporter</run> — SNS:Publish confirmed.
    Manual test: trigger exporter → Andrew receives "OTP pending" SMS before Orion OTP SMS.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W6.2."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. SNS publish call added at OTP-wait entry in orion_export.ts.
    2. Script deployed via safe-ec2-deploy.sh.
    3. End-to-end test: exporter pauses → Andrew gets "OTP pending" SMS → pokes OTP → exporter completes.
    4. Session log.
  </acceptance_criteria>

  <scope>
    <files><file action="modify">inf-exporter/src/orion_export.ts (on EC2 via safe-ec2-deploy.sh)</file></files>
  </scope>

  <requirements>
    <requirement id="1">Blocked on W6.2.</requirement>
    <requirement id="2">safe-ec2-deploy.sh per CLAUDE.md Rule 7.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Updated orion_export.ts.</deliverable>
    <deliverable type="document">Session log with test run record.</deliverable>
  </deliverables>

  <do_not><rule>Do NOT skip safe-ec2-deploy.sh.</rule></do_not>
</task_order>
