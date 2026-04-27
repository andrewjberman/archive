<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-24-inflec-w3.b.3-ae-slack-app-secrets</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-24</date>
    <status>cancelled</status><!-- CANCELLED 2026-04-27 by 2.0.0_SA_COO per PRD v2.0 (cc170c00). Slack eliminated by W3.B pivot (a2dd1e33). No longer needed. Replaced by TO-A (orion infra audit). -->
    <project_code>ADVI_INFLEC</project_code>
    <wave>W3.B.3</wave>
    <gates_on>W3.B.2 (Function URL output) + Andrew answers to 5 open questions below</gates_on>
    <gates>W3.B.4</gates>
    <prd>docs/architecture/ADVI_INFLEC_BRONZERUN.md §5.3, §5.4, §6</prd>
  </metadata>

  <objective>
    Create the Orion OTP Relay Slack App in the Opal Capital workspace. Configure slash commands
    pointing to the inf-otp-relay Function URL (from W3.B.2). Populate Secrets Manager
    `slack/otp-relay` with all Slack credentials and `orion/credentials` with the Orion login
    password. Confirm Lambda is reachable from Slack and responds correctly.
  </objective>

  <blocking_questions_for_andrew>
    This TO cannot start until Andrew answers these five questions.
    COO to surface these to Andrew before dispatching AE 0.7.0.

    Q1: Slack workspace authorization — confirm AE 0.7.0 is authorized to create a new Slack App
        ("Orion OTP Relay") in the Opal Capital workspace. Also confirm channel name preference
        (PRD default: #secure-ec2-auth) or specify an alternate.

    Q2: OTP timeout — PRD default is 5 minutes (Playwright polls 5s intervals, gives up at 300s).
        Confirm this is acceptable or specify a different timeout.

    Q3: Orion credential delivery path — AE needs the current Orion password to populate
        Secrets Manager `orion/credentials`. Preferred path: 1Password direct share, or AE opens
        AWS Console and Andrew types the value directly. Must NOT go through Slack, chat, or any
        logged channel.

    Q4: Slack allowed_user_ids — provide Andrew's Slack user ID (format: U...) for the OTP
        allowlist. Any additional users to include?

    Q5: inf-exporter security group S3 egress — confirm that the inf-exporter-sg outbound rules
        include the S3 VPC endpoint (or NAT path to opal-data-inf). AE 0.7.0 to verify via
        EC2 security group before this TO starts.
  </blocking_questions_for_andrew>

  <context>
    W3.B.2 creates the inf-otp-relay Lambda with a Function URL. That URL is the Request URL
    for the Slack slash commands. AE 0.7.0 receives the Function URL via MCP from AE 0.6.1
    when W3.B.2 apply completes.

    This TO is infrastructure configuration only — no code authored, no git commits required.
    Secrets Manager population happens via AWS CLI (no commit). Slack App setup happens via
    Slack API/UI (no commit).

    Secrets to populate:
    - slack/otp-relay: signing_secret, bot_token, channel_id (#secure-ec2-auth C... ID), allowed_user_ids
    - orion/credentials: {"username": "andrew@opalinvest.com", "password": "{Andrew-provided}"}

    Security note: Orion password must arrive via a secure path. AE requests it from Andrew
    directly per Q3 above. It must never transit Slack, any logged chat channel, or any file.

    W3.B.4 (E2E validation) gates on this TO completing. Once Secrets Manager is populated and
    slash commands are verified, AE 0.6.1 can trigger the full bronze run.
  </context>

  <steps>
    1. Receive Function URL from AE 0.6.1 via MCP (W3.B.2 completion signal).
    2. Confirm Andrew's answers to 5 blocking questions above.
    3. Verify inf-exporter security group egress (Q5): confirm S3 endpoint reachable.
    4. Create Slack App "Orion OTP Relay" at api.slack.com/apps in Opal Capital workspace.
       - OAuth scopes (bot token): chat:write, commands
       - Slash command /orion-otp: Request URL = {Function URL}, Description = "Submit Orion 2FA OTP"
       - Slash command /orion-status: Request URL = {Function URL}, Description = "Check Orion exporter state"
    5. Install app to workspace. Invite bot to #secure-ec2-auth (create channel if absent, private, Andrew + bot only).
    6. Retrieve from Slack App dashboard:
       - signing_secret (Basic Information > App Credentials)
       - bot_token (OAuth & Permissions > Bot User OAuth Token, starts with xoxb-)
       - channel_id (right-click #secure-ec2-auth > Copy Link or Slack API > C... format)
    7. Retrieve Andrew's Slack user_id (format: U...).
    8. Populate Secrets Manager:
       aws secretsmanager put-secret-value --secret-id slack/otp-relay \
         --secret-string '{"signing_secret":"...","bot_token":"xoxb-...","channel_id":"C...","allowed_user_ids":"U..."}'
    9. Obtain Orion password from Andrew via secure channel (per Q3). Populate:
       aws secretsmanager put-secret-value --secret-id orion/credentials \
         --secret-string '{"username":"andrew@opalinvest.com","password":"..."}'
       IMMEDIATELY close secure channel / discard password after entry.
    10. Verify Lambda env vars SLACK_ALLOWED_CHANNEL_ID + SLACK_ALLOWED_USER_IDS match populated values
        (these should be set via Terraform in W3.B.2; update Lambda config if needed).
    11. Smoke test:
        - From #secure-ec2-auth: /orion-status → Lambda responds with state (or "No active session")
        - From a different channel: /orion-otp 123456 → Lambda responds "Not authorized"
  </steps>

  <compiler_tools_mandate>
    Phase 1 — before starting:
    N/A — this TO is infrastructure configuration, not code authoring.

    Phase 2 — before signing off:
    <run>aws secretsmanager describe-secret --secret-id slack/otp-relay</run>
    <expect>Secret exists. ARN present.</expect>
    <run>aws secretsmanager describe-secret --secret-id orion/credentials</run>
    <expect>Secret exists. ARN present.</expect>
    <run>/orion-status from #secure-ec2-auth in Slack</run>
    <expect>Lambda responds with current exporter state or "No active session".</expect>

    Phase 3 — security group egress check (Q5 verification):
    <run>aws ec2 describe-security-groups --group-ids {inf-exporter-sg-id} --query "SecurityGroups[0].IpPermissionsEgress"</run>
    <expect>Outbound rules include S3 endpoint (HTTPS 443) access — either VPC endpoint or 0.0.0.0/0 NAT path.
    If S3 egress missing: flag to COO before proceeding — Playwright S3 polling will fail silently.</expect>
  </compiler_tools_mandate>

  <acceptance_criteria>
    1. /orion-otp 123456 from Andrew's Slack account in #secure-ec2-auth → Lambda responds "OTP received." ephemeral message.
    2. /orion-otp from any other user or channel → Lambda responds "Not authorized"; does NOT write to S3.
    3. /orion-status returns current state from otp/state.json (or "No active session" if key absent).
    4. Both Secrets Manager secrets exist and contain all required fields (verified via describe-secret).
    5. Orion credentials validate: AE 0.6.1 runs test-login-stage-2.ts with creds fetched from Secrets Manager — exits 0.
    6. inf-exporter security group egress confirmed for S3 VPC endpoint / NAT (Q5 cleared).
  </acceptance_criteria>

  <deliverables>
    <deliverable type="infrastructure">Slack App "Orion OTP Relay" created, slash commands configured, bot in #secure-ec2-auth.</deliverable>
    <deliverable type="secrets">slack/otp-relay + orion/credentials populated in Secrets Manager.</deliverable>
    <deliverable type="mcp">MCP to 0.6.1_AE_PartnerETL when complete — W3.B.4 (E2E validation) is unblocked. MCP to COO.</deliverable>
    <deliverable type="document">Session log: Slack App URL, channel_id, slash-command smoke-test results, security group egress confirmation.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT transmit the Orion password via Slack, this chat, any MCP message, or any committed file.</rule>
    <rule>Do NOT create the #secure-ec2-auth channel as public. Private only.</rule>
    <rule>Do NOT skip the security group egress check (Q5) — silent S3 poll failures are hard to debug mid-run.</rule>
    <rule>Do NOT start this TO until W3.B.2 apply is complete and Function URL is received.</rule>
    <rule>Do NOT start this TO until Andrew answers all 5 blocking questions above.</rule>
  </do_not>
</task_order>
