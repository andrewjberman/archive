<task_order>
  <metadata>
    <id>ADVI_INFLEC.TO-E.ae-sns-otp-alert-url</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-27</date>
    <status>staged</status><!-- Gate: TO-C (orion_export.ts deployed). W6.2 already COMPLETE (af3c4963). -->
    <project_code>ADVI_INFLEC</project_code>
    <wave>TO-E</wave>
    <supersedes>W6.3.ae-exporter-sns-publish.md (spec change: SNS message must include Lambda Function URL)</supersedes>
    <gates_on>TO-C RAVC4</gates_on>
  </metadata>

  <prd_ref>docs/architecture/ADVI_INFLEC_BRONZERUN_V2.md §5 TO-E (cc170c00)</prd_ref>

  <objective>
    Wire SNS publish at the W6.3 HOOK in orion_export.ts (added by TO-C) so Andrew receives
    an SMS with the Lambda Function URL when Orion triggers OTP. Without the URL in the alert,
    Andrew cannot complete the 2FA step on mobile.
  </objective>

  <scope>
    Add SNS publish call at the W6.3 HOOK comment in orion_export.ts:

    ```typescript
    const FUNCTION_URL = process.env.OTP_RELAY_URL  // or constant in types.ts — see below
    await sns.publish({
      TopicArn: process.env.OTP_ALERT_TOPIC_ARN,
      Message: `Orion export: OTP required. Open to submit code: ${FUNCTION_URL}`,
      Subject: 'Orion OTP Required',
    })
    ```

    OTP_RELAY_URL source: Option (b) preferred — hardcode as constant in types.ts.
    URL is non-sensitive; UUID in the Function URL provides security. Document choice in session log.
    If AE prefers SSM Parameter Store (/inf/otp-relay-url), that is acceptable — document and implement.

    OTP_ALERT_TOPIC_ARN: fetch from env or SSM (inf-otp-alert topic ARN, deployed at af3c4963).
    Confirm topic ARN via: aws sns list-topics | grep inf-otp-alert

    Deploy updated orion_export.ts via safe-ec2-deploy.sh.

    End-to-end test: trigger export run → confirm Andrew receives SMS with Function URL →
    Andrew opens URL on phone → submits OTP via form → exporter continues to export.
  </scope>

  <acceptance_criteria>
    1. SNS publish added at WAITING_FOR_OTP state transition in orion_export.ts.
    2. Message body includes Lambda Function URL (confirmed in CW log output).
    3. End-to-end test: trigger export → Andrew receives SMS with URL → opens URL → enters OTP →
       exporter continues. CW logs show OTP_RECEIVED state + EXPORT_COMPLETE.
    4. safe-ec2-deploy.sh used for EC2 update.
    5. tsc --noEmit exits 0 after change.
    6. Session log with: OTP_RELAY_URL source choice, test run CW log trace.
    7. RAVC4 to 2.0.0_SA_COO with: CW log excerpt showing SMS + OTP flow, export completion.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT skip the end-to-end test — TO-F (E2E validation) requires this path to be confirmed first.</rule>
    <rule>Do NOT use safe-ec2-deploy.sh alternative — CLAUDE.md Rule 7.</rule>
  </do_not>
</task_order>
