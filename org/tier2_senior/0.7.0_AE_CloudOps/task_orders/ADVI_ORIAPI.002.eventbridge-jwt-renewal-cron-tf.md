<task_order>
<metadata>
  <to_id>ADVI_ORIAPI.002</to_id>
  <project>ADVI_ORIAPI</project>
  <title>Orion JWT Pre-Emptive Renewal Cron — EventBridge + SSM + CW Alarm + SNS Terraform (Phase 2)</title>
  <assigned_to>0.7.0_AE_CloudOps~B</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-04-27</issued_date>
  <status>pending</status>
  <priority>MEDIUM</priority>
  <references>
    <ref type="prd">docs/architecture/ADVI_ORIAPI.md (v0.4 FINAL, commit c232b4ec)</ref>
    <ref type="prd_section">PRD §B.5 — Phase 2: Pre-emptive renewal cron. EventBridge cron(0 12 * * ? *) (08:00 ET) -> SSM opal-inf-jwt-fetch on inf-gold-runner EC2.</ref>
    <ref type="existing_infra">inf-otp-relay Lambda (commit 01df38f1) + inf-exporter EC2 (ADVI_INFLEC.W3.B) already deployed — this TO wires the scheduled invocation of jwt-extract mode.</ref>
  </references>
  <dependencies>
    <dependency agent="0.6.1_AE_PartnerETL" task="ADVI_ORIAPI.001" status="phase0_complete">AE 0.6.1 Phase 0 RAVC confirming --mode jwt-extract is working and s3://opal-data-inf/orion/jwt/current.json is being populated. COO will flip this TO from staged to pending on receipt of that RAVC.</dependency>
    <dependency>Confirm opal-inf-jwt-fetch SSM document name does not conflict with existing SSM documents in inf-pipeline namespace.</dependency>
  </dependencies>
</metadata>

<scope>
Provision Terraform for the daily pre-emptive Orion JWT renewal (Phase 2 per PRD §B.5). JWT TTL is 10h; daily 08:00 ET refresh keeps it always fresh during business hours when Andrew is reachable for occasional OTP prompts.

RESOURCES TO CREATE (in inf-pipeline Terraform workspace):

1. EventBridge rule:
   - Name: opal-inf-jwt-fetch
   - Schedule: cron(0 12 * * ? *) (12:00 UTC = 08:00 ET, daily)
   - Target: SSM Run Command on inf-gold-runner EC2 (i-0ed5afded2ebd4ed4 or equivalent via tag filter)
   - Description: "Daily pre-emptive Orion JWT renewal via inf-exporter --mode jwt-extract"

2. SSM document: opal-inf-jwt-fetch
   - Type: Command
   - Content: runs inf-exporter with --mode jwt-extract on the EC2 instance
   - Parameters: none required (credentials already in inf-exporter SSM doc env vars)

3. CloudWatch metric alarm: orion-otp-timeout-alert
   - Fires if jwt-extract exits with OTP timeout error (FAILED_OTP_TIMEOUT exit code)
   - Threshold: 1 occurrence in 1 evaluation period
   - Action: SNS notification

4. SNS topic: orion-otp-alert (or reuse existing if present under inf-pipeline)
   - Subscriber: Andrew notification (existing pattern from ADVI_INFLEC W6.2 inf-otp-alert)
   - Message: "Orion JWT renewal failed: OTP required. Visit bookmarked phone URL to enter OTP."

IAM additions required:
   - EventBridge execution role: events:PutRule + ssm:SendCommand on inf-gold-runner
   - inf-gold-runner EC2 role: existing ssm:* should cover — verify, do not add redundant permissions

Pipeline tag target: inf-pipeline-vX.Y.Z (check current tag, increment appropriately).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-iam gaps</run>
      <expect>Baseline IAM gap count documented. No existing gaps related to EventBridge -> SSM target invocation for inf-gold-runner.</expect>
      <if_mismatch>Document pre-existing gaps; do not introduce new ones. Surface to COO if baseline has unexpected gaps.</if_mismatch>
    </step>
    <step>
      <run>aws ssm list-documents --filters Key=Name,Values=opal-inf --query "DocumentIdentifiers[*].Name"</run>
      <expect>No existing document named opal-inf-jwt-fetch (would indicate name collision).</expect>
      <if_mismatch>STOP. If name already taken: pick alternate name, update TO, MCP COO with change.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/terraform.exe plan -var-file=terraform.tfvars</run>
      <expect>Plan shows 4-6 new resources (EventBridge rule + target + SSM doc + CW alarm + SNS topic + IAM role/policy if needed). Zero destructive changes. Exit 0.</expect>
      <if_mismatch>STOP. Any destructive change requires COO review before apply.</if_mismatch>
    </step>
    <step>
      <run>comp-iam gaps</run>
      <expect>Same baseline gap count as Phase 1 scan. No new gaps introduced by Terraform additions.</expect>
      <if_mismatch>Fix iam.tf before committing.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after terraform apply">
    <step>
      <run>aws events list-rules --name-prefix opal-inf-jwt</run>
      <expect>Rule present, State=ENABLED, ScheduleExpression=cron(0 12 * * ? *).</expect>
      <if_mismatch>EventBridge rule not deployed correctly. Review apply output.</if_mismatch>
    </step>
    <step>
      <run>git tag -l "inf-pipeline-v*" | sort -V | tail -5</run>
      <expect>New tag present and pushed. Version incremented correctly vs previous tag.</expect>
      <if_mismatch>Tag and push before closing RAVC.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. EventBridge rule deployed: schedule cron(0 12 * * ? *) (08:00 ET), targets SSM Run Command on inf-gold-runner EC2, State=ENABLED.
2. SSM document opal-inf-jwt-fetch created. Manually invocable via aws ssm send-command (test run confirmed).
3. CW alarm + SNS topic wired: FAILED_OTP_TIMEOUT triggers SNS notification to Andrew.
4. Terraform plan at 0-diff after apply.
5. Pipeline tag pushed: inf-pipeline-vX.Y.Z. CHANGELOG.json updated.
6. Session log includes Compiler Tools section with all runs and explicit pass/fail vs expect. Missing rows = REWORK.
7. RAVC4 to COO with apply output summary + plan hash + tag + manual SSM test invocation result.
</acceptance_criteria>

<cross_domain_coordination>
- ADVI_ORIAPI.001 (AE 0.6.1): this TO is staged until Phase 0 RAVC received; COO flips to pending at that time.
- ADVI_INFLEC inf-pipeline Terraform workspace: confirm namespace alignment for SSM doc name + EventBridge rule.
- Do NOT create duplicate SNS topic if orion-otp-alert already exists — check before creating.
</cross_domain_coordination>
</task_order>
