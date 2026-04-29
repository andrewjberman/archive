<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w2.5-otp-relay</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>complete</status><!-- Verified 2026-04-29 AE TO sweep: lambda-otp-relay.tf deployed; function URL live at swk4gc6kd7k3osowr3464l7u540exjbp.lambda-url.us-east-1.on.aws. -->
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Set up OTP relay infrastructure: S3 path `s3://opal-data-inf/otp/current.txt` as the ephemeral relay key, Andrew-scoped IAM policy for writing OTP (pre-signed URL or IAM user policy), and optionally an SNS topic for Phase 3 SMS callback. Wire OTP timeout flag path (`FAILED_OTP_TIMEOUT`). Per PRD §6.3 — Andrew picks delivery method (Q11): CLI one-liner, iOS Shortcut, web form, or Slack slash-command. Default recommendation: CLI + iOS Shortcut.
  </objective>

  <context>
    PRD §6.3. OTP relay mechanism: Orion login triggers SMS OTP to Andrew's phone → inf-exporter pauses → writes WAITING_FOR_OTP flag to S3 → Andrew writes OTP to `otp/current.txt` → exporter polls (3-5s) → picks up OTP → completes login. Andrew-accessible path needs either: (a) a pre-signed URL AE generates on each exporter run, (b) an AWS IAM policy on Andrew's user/role allowing s3:PutObject on `opal-data-inf/otp/*` only, or (c) a minimal web relay form. Implement (b) as the baseline; document (a) as fallback.

    PRD §10 Q11 (OTP delivery method) is OPEN — Andrew hasn't picked. AE implements the S3 infrastructure and IAM now; Andrew's delivery choice only affects how he invokes the CLI (pre-signed vs direct `aws s3 cp`).
  </context>

  <compiler_tools_mandate>
    Phase 1: <run>comp-iam service inf-exporter</run> — confirm existing otp/ permissions in scope from W2.4.
    Phase 3: <run>aws s3 cp /dev/stdin s3://opal-data-inf/otp/current.txt <<< 'TEST'</run> — Andrew's test write (or AE from a test role). <run>aws s3 rm s3://opal-data-inf/otp/current.txt</run> — cleanup.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "W2.4 (inf-exporter EC2 IAM) must be complete — otp/ S3 perms should already exist on inf-exporter role."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `opal-data-inf/otp/` prefix exists in bucket.
    2. Andrew can write to `opal-data-inf/otp/current.txt` via CLI (IAM policy or pre-signed URL documented).
    3. inf-exporter can read + delete `otp/current.txt`.
    4. OTP timeout convention documented: exporter writes `FAILED_OTP_TIMEOUT` to `otp/status.txt` on 5-min timeout.
    5. SNS topic stubbed (optional but recommended for Phase 3 hook — AE judgment call).
    6. Q11 delivery preference noted as pending Andrew answer; baseline (direct CLI) implemented.
    7. Session log.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">infra/aws/terraform/inf-pipeline/iam.tf (Andrew write policy on otp/)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">otp/ write access: Andrew only (or pre-signed URL scoped to inf-exporter-run context). No broad write access.</requirement>
    <requirement id="2">OTP key ephemeral: delete after successful read. inf-exporter deletes on success.</requirement>
    <requirement id="3">Document the exact CLI one-liner Andrew uses to poke the OTP in the session log.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">iam.tf (Andrew OTP write policy).</deliverable>
    <deliverable type="document">Session log with CLI one-liner for Andrew + timeout convention.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT block on Q11 answer — implement baseline CLI path now.</rule>
    <rule>Do NOT leave otp/ world-writable.</rule>
  </do_not>
</task_order>
