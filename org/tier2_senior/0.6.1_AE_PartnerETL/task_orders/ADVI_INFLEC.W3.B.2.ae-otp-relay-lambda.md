<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-24-inflec-w3.b.2-ae-otp-relay-lambda</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <date>2026-04-24</date>
    <status>complete</status><!-- CLOSED COMPLETE 2026-04-27 by 2.0.0_SA_COO per PRD v2.0 (cc170c00). Lambda deployed with web-form OTP relay (01df38f1). Function URL live, public access confirmed. Slack-model ACs superseded by pivot. -->
    <project_code>ADVI_INFLEC</project_code>
    <wave>W3.B.2</wave>
    <parallel_with>W3.B.1</parallel_with>
    <unblocks>W3.B.3 (Function URL output needed for Slack slash-command config)</unblocks>
    <gates>W3.B.4</gates>
    <prd>docs/architecture/ADVI_INFLEC_BRONZERUN.md §5.2, §5.3</prd>
  </metadata>

  <objective>
    Author the `inf-otp-relay` Lambda (Python 3.12, Function URL), add it to the lambda source
    map, author Terraform for the Lambda + Function URL + EventBridge rule + Secrets Manager
    secrets + S3 bucket policy extensions. Run terraform apply in the inf-pipeline workspace.
    Capture the Function URL output — this is the gate input for W3.B.3 (Slack App config).
  </objective>

  <context>
    The inf-otp-relay Lambda is the relay between Slack slash commands and the EC2 Playwright
    process. Two inbound event types:
    1. Slack slash-command POST (X-Slack-Signature header present) — /orion-otp and /orion-status
    2. S3 EventBridge (otp/state.json PUT) — outbound Slack notification to #secure-ec2-auth

    Function URL (not API Gateway) is used because Slack needs a simple HTTPS callback endpoint
    with no managed auth — Slack HMAC-SHA256 signature verification is the auth layer.

    S3 OTP paths (canonical):
    - opal-data-inf/otp/current.txt — OTP value (Lambda writes, EC2 reads + deletes)
    - opal-data-inf/otp/state.json — state machine (EC2 writes, Lambda reads for Slack notify)
    - opal-data-inf/otp/debug/{YYYY-MM-DD}/ — screenshots

    This TO runs in parallel with W3.B.1. Neither depends on the other.
    W3.B.3 gates on THIS TO being applied (needs Function URL). W3.B.4 gates on all three.

    Architectural mandate (CTO — non-negotiable): OTP delivery is S3 polling. SSM SendCommand
    cannot inject into a blocking Playwright process. Do NOT reopen this decision.
  </context>

  <files_to_create>
    <file>infra/aws/lambda/inf-otp-relay/lambda_function.py</file>
    <file>infra/aws/terraform/inf-pipeline/lambda-otp-relay.tf</file>
    <file action="modify">infra/aws/terraform/inf-pipeline/secrets.tf (new or extend)</file>
    <file action="modify">infra/aws/terraform/inf-pipeline/s3.tf (extend with otp/ policy + lifecycle)</file>
    <file action="modify">infra/aws/lambda/ci/lambda-source-map.json</file>
  </files_to_create>

  <spec_summary>

    lambda_function.py (Python 3.12):
    - Distinguish event type: Slack headers (X-Slack-Signature present) vs EventBridge envelope
    - Slack verification on all slash-command requests:
        sig_basestring = f"v0:{timestamp}:{body.decode()}"
        expected = "v0=" + hmac.new(signing_secret, sig_basestring, sha256).hexdigest()
        Reject if abs(time.time() - int(timestamp)) > 300 (replay guard)
    - ALLOWED_USER_IDS = env SLACK_ALLOWED_USER_IDS split(",")
      ALLOWED_CHANNEL_ID = env SLACK_ALLOWED_CHANNEL_ID
      (values loaded from Secrets Manager slack/otp-relay at cold start)
    - /orion-otp handler:
        1. Verify signature + user_id allowlist + channel_id + code is 4-8 digits
        2. s3:PutObject opal-data-inf/otp/current.txt = code
        3. CloudWatch log: user_id={uid} timestamp={ts} code_prefix={code[:2]}****
        4. Return HTTP 200: {"response_type":"ephemeral","text":"OTP received. Delivering to Orion exporter."}
    - /orion-status handler:
        1. Verify signature + allowlist
        2. s3:GetObject opal-data-inf/otp/state.json
        3. Return state as Slack message
    - S3 EventBridge handler:
        1. Read otp/state.json
        2. Map state → Slack message (see PRD §5.2 table)
        3. chat.postMessage to #secure-ec2-auth via bot token from slack/otp-relay secret
    - from __future__ import annotations as first import (ADHC_DSFLOW.004 rule)
    - No emojis in any log lines (CloudWatch ASCII-only rule)

    lambda-source-map.json entry:
    "inf-otp-relay": {
      "source_path": "infra/aws/lambda/inf-otp-relay",
      "runtime": "python3.12",
      "memory_mb": 256,
      "timeout_s": 10,
      "layers": [],
      "pipeline": "inf-pipeline",
      "last_deployed_commit": null
    }

    lambda-otp-relay.tf:
    - module inf_otp_relay using yang-lambda (or equivalent standard module)
    - function_name: inf-otp-relay, runtime: python3.12, memory_size: 256, timeout: 10
    - environment_variables: INF_S3_BUCKET, SLACK_ALLOWED_CHANNEL_ID, SLACK_ALLOWED_USER_IDS,
      SLACK_SECRET_NAME=slack/otp-relay
    - aws_lambda_function_url: authorization_type=NONE, CORS allow_origins=["https://slack.com"],
      allow_methods=["POST"], allow_headers=[content-type, x-slack-signature, x-slack-request-timestamp]
    - aws_cloudwatch_event_rule inf-otp-state-change: S3 EventBridge on opal-data-inf otp/state.json PUT
    - aws_cloudwatch_event_target: route rule to inf_otp_relay.function_arn
    - aws_lambda_permission for EventBridge to invoke

    secrets.tf additions:
    - aws_secretsmanager_secret "orion/credentials": description for Orion login creds
      (value populated manually by AE post-apply per W3.B.3)
    - aws_secretsmanager_secret "slack/otp-relay": description for Slack App credentials
      (fields: signing_secret, bot_token, channel_id, allowed_user_ids — populated by W3.B.3)

    s3.tf extensions:
    - Bucket policy statements for opal-data-inf:
        s3:PutObject on otp/* — ALLOW inf-otp-relay-lambda-role only
        s3:GetObject + s3:DeleteObject on otp/current.txt — ALLOW inf-exporter-ec2-role only
        s3:PutObject + s3:GetObject on otp/state.json — ALLOW inf-exporter-ec2-role (write) + inf-otp-relay-lambda-role (read)
    - S3 lifecycle rule: delete all otp/ objects after 10 minutes (safety TTL if exporter crashes)
  </spec_summary>

  <compiler_tools_mandate>
    Phase 1 — before writing:
    <run>.tools/ds-commit-gate.sh infra/aws/lambda/inf-otp-relay/lambda_function.py</run>
    <expect>py_compile + AST scanner + ruff py39 all exit 0.</expect>

    Phase 2 — before commit:
    <run>comp-iam gaps</run>
    <expect>No missing permissions after iam.tf changes. Flag any gaps to COO.</expect>
    Confirm lambda-source-map.json entry added.
    Pre-commit gate must exit 0 on lambda_function.py.

    Phase 3 — after terraform apply:
    <run>terraform plan (inf-pipeline workspace)</run>
    <expect>0-diff post-apply.</expect>
    <run>aws lambda get-function-url-config --function-name inf-otp-relay</run>
    <expect>Function URL present in output. Capture the FunctionUrl value — required for W3.B.3.</expect>
    <run>aws s3api get-bucket-lifecycle-configuration --bucket opal-data-inf</run>
    <expect>otp/ prefix lifecycle rule present with 10-min (600s) expiration.</expect>
    <run>aws logs describe-log-groups --log-group-name-prefix /aws/lambda/inf-otp-relay</run>
    <expect>Log group exists.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    After terraform apply completes: MCP to 0.7.0_AE_CloudOps with the Function URL value.
    CloudOps needs it to configure Slack slash-command Request URL in W3.B.3.
    Subject: "ADVI_INFLEC W3.B.2 COMPLETE — Function URL: {url} — W3.B.3 unblocked"
  </cross_domain_coordination>

  <acceptance_criteria>
    1. lambda_function.py passes pre-commit gate (py_compile + AST + ruff py39). All three exit 0.
    2. from __future__ import annotations is the first import in lambda_function.py.
    3. Lambda Function URL created and captured. Output URL in session log.
    4. S3 write test: invoke Lambda with a valid test Slack payload — otp/current.txt appears in opal-data-inf.
    5. Slack signature verification rejects payload with bad signature.
    6. Freshness check rejects payload with X-Slack-Request-Timestamp older than 300s.
    7. User ID not in allowlist → returns 200 with "Not authorized"; does NOT write to S3.
    8. terraform plan 0-diff post-apply.
    9. S3 lifecycle rule confirmed: otp/ prefix, 10-min expiration.
    10. lambda-source-map.json entry added and committed.
    11. Function URL value MCPed to 0.7.0_AE_CloudOps to unblock W3.B.3.
  </acceptance_criteria>

  <deliverables>
    <deliverable type="commit">lambda_function.py + lambda-otp-relay.tf + secrets.tf extension + s3.tf extension + lambda-source-map.json update. Author: 0.6.1_AE_PartnerETL.</deliverable>
    <deliverable type="terraform">terraform apply in inf-pipeline workspace. Tag inf-pipeline-v{next} post-apply.</deliverable>
    <deliverable type="mcp">MCP to 0.7.0_AE_CloudOps with Function URL. MCP to COO on full completion.</deliverable>
    <deliverable type="document">Session log: Function URL, apply output, pre-commit gate results, S3 test evidence.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT use API Gateway — Function URL only (simpler; Slack doesn't need API GW features).</rule>
    <rule>Do NOT log full OTP values in CloudWatch — log user_id + timestamp + first 2 digits + **** only.</rule>
    <rule>Do NOT set authorization_type=AWS_IAM on the Function URL — incompatible with Slack callbacks.</rule>
    <rule>Do NOT commit Slack secrets or Orion credentials — Secrets Manager only.</rule>
    <rule>Do NOT reopen the SSM-vs-S3 OTP delivery decision. CTO override is final.</rule>
  </do_not>
</task_order>
