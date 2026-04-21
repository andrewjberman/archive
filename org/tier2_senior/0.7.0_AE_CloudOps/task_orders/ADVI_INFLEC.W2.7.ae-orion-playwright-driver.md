<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w2.7-playwright-driver</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Author `inf-exporter/src/orion_export.ts` Playwright driver using the W2.6 selector spec. Includes: login sequence, OTP relay polling wrapper (polls `s3://opal-data-inf/otp/current.txt` every 3-5s up to 5 min), post-login navigation, TRN/AUM/accounts export triggers, upload to `s3://opal-data-inf/bronze/orion/{YYYY-MM-DD}/{filename}.csv`. Deploy to inf-exporter EC2 via `safe-ec2-deploy.sh`.
  </objective>

  <context>PRD §6.3. OTP polling wrapper: exporter pauses at OTP screen, writes `WAITING_FOR_OTP` flag, polls `otp/current.txt` until present or 5-min timeout. On OTP received: enter value, clear OTP key. On timeout: write `FAILED_OTP_TIMEOUT` + SNS publish. S3 upload path: `bronze/orion/{YYYY-MM-DD}/{filename}.csv`. Blocked on W2.6 (selector spec).</context>

  <compiler_tools_mandate>
    Phase 1: <run>cat infra/aws/ec2/bd-exporter/src/exporter.ts (or equivalent bd-exporter script)</run> — pattern reference for playwright + S3 upload.
    Phase 3: (W2.8 first manual run validates this TO's output.)
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W2.6 selector spec + W2.4 EC2 + W2.5 OTP relay. All three must be complete."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `orion_export.ts` deployed to inf-exporter EC2 via `safe-ec2-deploy.sh`.
    2. Script polls `otp/current.txt` on 3-5s interval, max 5 min.
    3. On timeout: writes `FAILED_OTP_TIMEOUT` to `otp/status.txt`.
    4. Uploads: `bronze/orion/{date}/{filename}.csv` for TRN, AUM, accounts.
    5. No hardcoded credentials — all from Secrets Manager.
    6. Session log with deploy record + dry-run trace.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">inf-exporter/src/orion_export.ts (on EC2 via safe-ec2-deploy.sh)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Credentials from Secrets Manager only.</requirement>
    <requirement id="2">OTP timeout must write failure flag + SNS (if topic provisioned in W2.5).</requirement>
    <requirement id="3">S3 upload via AWS SDK — not CLI subprocess.</requirement>
    <requirement id="4">safe-ec2-deploy.sh per CLAUDE.md Rule 7.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">orion_export.ts source in repo (script-on-EC2 via safe-ec2-deploy.sh).</deliverable>
    <deliverable type="document">Session log with deploy record.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT hardcode credentials.</rule>
    <rule>Do NOT skip OTP polling wrapper — it's the core novel piece.</rule>
  </do_not>
</task_order>
