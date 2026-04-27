<task_order>
  <metadata>
    <id>ADVI_INFLEC.TO-A.ae-orion-infra-audit</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-27</date>
    <status>complete</status><!-- a070c3a9 inf-pipeline-v1.5.2 2026-04-27 -->
    <project_code>ADVI_INFLEC</project_code>
    <wave>TO-A</wave>
    <replaces>W3.B.3 (CANCELLED — Slack eliminated)</replaces>
    <priority>HIGH — no gate, do immediately</priority>
  </metadata>

  <prd_ref>docs/architecture/ADVI_INFLEC_BRONZERUN_V2.md §5 TO-A (cc170c00)</prd_ref>

  <objective>
    Verify and confirm the inf-otp-relay + inf-exporter infrastructure is production-ready
    for the Orion bronze runner. Five audit checks, no code changes expected.
  </objective>

  <scope>
    1. Verify orion/credentials Secrets Manager secret exists.
       aws secretsmanager describe-secret --secret-id orion/credentials
       If ABSENT: create resource (empty value — Andrew populates separately per A2).
       aws secretsmanager create-secret --name orion/credentials --description "Orion login credentials"

    2. Verify S3 lifecycle rule on otp/ prefix is active on opal-data-inf.
       aws s3api get-bucket-lifecycle-configuration --bucket opal-data-inf
       Expect: rule with otp/ prefix + expiration 600s (10 min).
       If ABSENT: add rule to infra/aws/terraform/{bucket-tf}/ → apply.

    3. Capture inf-otp-relay Function URL:
       aws lambda get-function-url-config --function-name inf-otp-relay
       Record FunctionUrl in session log. MCP to 2.0.0_SA_COO + Andrew with URL for phone bookmark (A3).

    4. Confirm inf-exporter-ec2-role IAM permissions on otp/ + bronze/orion/:
       comp-iam service inf-exporter
       Expect: s3:GetObject + s3:DeleteObject on otp/current.txt; s3:GetObject + s3:PutObject on otp/state.json.
       Also: s3:PutObject on bronze/orion/ prefix.
       Flag any gaps to COO before proceeding.

    5. Confirm inf-otp-relay Lambda IAM:
       comp-iam service inf-otp-relay
       Expect: s3:PutObject on otp/* (for Lambda POST handler).
       Flag any gaps to COO.
  </scope>

  <acceptance_criteria>
    1. orion/credentials secret exists in Secrets Manager (value may be empty — that is fine).
    2. S3 lifecycle rule on otp/ prefix: 10-min expiration confirmed active.
    3. inf-otp-relay Function URL captured and MCPed to 2.0.0_SA_COO + Andrew.
    4. comp-iam service inf-exporter exits clean (all otp/ + bronze/orion/ permissions present).
    5. comp-iam service inf-otp-relay exits clean (otp/ write permission present).
    6. Session log with all command outputs and findings.
    7. RAVC4 to 2.0.0_SA_COO with: Function URL, secret status, lifecycle rule status, IAM findings.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT populate orion/credentials with any password — Andrew does that via secure channel (A2).</rule>
    <rule>Do NOT share the Function URL in plain text in any logged channel — MCP to COO + Andrew only.</rule>
    <rule>Do NOT modify inf-otp-relay Lambda code — this is an audit, not a code change.</rule>
  </do_not>
</task_order>
