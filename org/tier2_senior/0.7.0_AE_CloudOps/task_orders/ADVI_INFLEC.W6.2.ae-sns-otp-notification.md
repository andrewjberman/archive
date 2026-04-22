<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w6.2-sns-notification</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Create SNS topic + SMS subscription to Andrew's phone for "OTP pending" notification. When `inf-exporter` pauses at OTP screen, it publishes to this topic → Andrew gets SMS → he sends OTP via relay. Eliminates need for Andrew to watch for the Orion SMS first.
  </objective>

  <context>PRD §5.3 Phase 3 + §6.3. SNS topic: `inf-otp-alert`. IAM: `inf-exporter` role gets SNS:Publish on this topic (verify W2.5 stub already has this). Andrew's phone: SMS subscription (Andrew provides phone number — do NOT hardcode in TF; use SSM Parameter Store or Andrew provides at apply time).</context>

  <compiler_tools_mandate>
    Phase 2: <run>.tools/terraform.exe plan</run> — SNS topic + subscription + IAM additions.
    Phase 3: <run>aws sns publish --topic-arn arn:aws:sns:us-east-1:313476888478:inf-otp-alert --message "TEST OTP pending"</run> — Andrew confirms SMS received.
    <run>comp-iam service inf-exporter</run> — SNS:Publish on inf-otp-alert included, 0 MISSING.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Andrew must provide phone number for SNS subscription. Get before apply."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. SNS topic `inf-otp-alert` created.
    2. Andrew's phone subscribed (confirmed SMS received on test publish).
    3. inf-exporter IAM has SNS:Publish on inf-otp-alert.
    4. Session log.
  </acceptance_criteria>

  <scope>
    <files><file action="modify">infra/aws/terraform/inf-pipeline/eventbridge.tf (or separate sns.tf)</file></files>
  </scope>

  <requirements>
    <requirement id="1">Phone number from Andrew — not hardcoded in TF.</requirement>
    <requirement id="2">Confirm SMS receipt before tagging.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">SNS TF resource + IAM update.</deliverable>
    <deliverable type="document">Session log with test publish confirmation.</deliverable>
  </deliverables>

  <do_not><rule>Do NOT hardcode phone number in TF.</rule></do_not>
</task_order>
