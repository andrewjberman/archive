<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w2.4-inf-exporter-ec2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>complete</status><!-- Verified 2026-04-29 AE TO sweep: inf-exporter i-081ae6aafb394fb1a active in EC2_MANIFEST + ec2.tf. -->
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Provision `inf-exporter` EC2 (t3.medium, Amazon Linux 2023) in `inf-pipeline/ec2.tf`. Mirrors `bd-exporter` pattern: bun + playwright + xvfb bootstrap via user_data. EBS root volume KMS-encrypted with `inf-ebs-key` (same CMK as W2.1 — shared within inf-pipeline only, never with bd). Dedicated security group `inf-exporter-sg` (no overlap with bd-pipeline SGs). IAM role `inf-exporter`: Secrets Manager read (Orion credentials), S3 RW on `opal-data-inf/bronze/orion/` + `opal-data-inf/otp/`, SSM Session Manager, SNS publish on OTP-alert topic (Phase 3). Register in EC2_MANIFEST.json (update W1.9 stub).
  </objective>

  <context>
    PRD §4.1 row 10 + §6.3. Blocked on W0.3 (Andrew + AE Orion walkthrough) for the Playwright script — BUT EC2 infrastructure itself does not require the walkthrough. AE can provision EC2 + IAM + user_data bootstrap concurrent with W0.3. The Playwright driver (`orion_export.ts`) ships in W2.7 after W0.3.
  </context>

  <compiler_tools_mandate>
    Phase 1: <run>cat infra/aws/terraform/bd-pipeline/ec2.tf</run> — bd-exporter block (bun+playwright user_data).
    Phase 3: <run>aws ec2 describe-instances --filters Name=tag:Name,Values=inf-exporter --query 'Reservations[*].Instances[*].{ID:InstanceId,State:State.Name}'</run> — 1 instance returned.
    <run>comp-iam service inf-exporter</run> — 0 MISSING.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "W0.3 (Andrew-AE Orion walkthrough) must precede W2.6/W2.7 Playwright driver — but NOT this EC2 provisioning. Provision concurrently."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. inf-exporter EC2 provisioned (t3.medium).
    2. user_data installs bun + playwright + xvfb (mirror bd-exporter).
    3. IAM role scoped: Secrets Manager read (Orion creds secret path), S3 RW opal-data-inf/bronze/orion/ + opal-data-inf/otp/, SSM Session Manager.
    4. EBS root volume encrypted=true, KmsKeyId = inf-ebs-key (same key as W2.1 gold runner). Verify: `aws ec2 describe-volumes ... --query Volumes[*].Encrypted`.
    5. Security group `inf-exporter-sg` created fresh. No shared membership with bd-pipeline SGs.
    6. comp-iam service inf-exporter: 0 MISSING.
    7. EC2_MANIFEST.json updated with real instance ID.
    8. Tag inf-pipeline-v1.3.0.
    9. Session log with encrypted-volume and SG verification output.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">infra/aws/terraform/inf-pipeline/ec2.tf</file>
      <file action="modify">infra/aws/terraform/inf-pipeline/iam.tf</file>
      <file action="modify">infra/aws/ec2/EC2_MANIFEST.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">t3.medium — OTP relay exporter doesn't need heavy compute.</requirement>
    <requirement id="2">Orion credentials go in Secrets Manager — NOT hardcoded in user_data.</requirement>
    <requirement id="3">otp/ S3 prefix: read + write + delete for inf-exporter only.</requirement>
    <requirement id="4">EBS encryption: use `inf-ebs-key` KMS CMK (created in W2.1). encrypted=true on root volume.</requirement>
    <requirement id="5">Security group: dedicated `inf-exporter-sg`. No shared rules or group membership with bd-pipeline SGs. INF-to-INF traffic only within inf SGs.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">ec2.tf + iam.tf + EC2_MANIFEST.json.</deliverable>
    <deliverable type="tag">inf-pipeline-v1.3.0.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT hardcode Orion credentials anywhere. Secrets Manager only.</rule>
    <rule>Do NOT wait for W0.3 to start this TO — infrastructure and Playwright script are independent.</rule>
    <rule>Do NOT share security groups with bd-pipeline resources.</rule>
    <rule>Do NOT reuse bd-pipeline KMS key — use inf-ebs-key created in W2.1.</rule>
  </do_not>
</task_order>
