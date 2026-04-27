<task_order>
  <metadata>
    <id>ADVI_INFLEC.TO-C.ae-orion-playwright-driver</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-27</date>
    <status>staged</status><!-- Gate: TO-A (infra audit PASS) + TO-B (selector spec + Andrew confirm). -->
    <project_code>ADVI_INFLEC</project_code>
    <wave>TO-C</wave>
    <supersedes>W2.7.ae-orion-playwright-driver.md (material spec change: web-form OTP model, Slack removed)</supersedes>
    <gates_on>TO-A RAVC4 + TO-B RAVC4 (Andrew confirmation in spec)</gates_on>
  </metadata>

  <prd_ref>docs/architecture/ADVI_INFLEC_BRONZERUN_V2.md §5 TO-C (cc170c00)</prd_ref>

  <objective>
    Author infra/aws/ec2/inf-exporter/src/stepwise/orion_export.ts — the main Playwright
    driver that logs into Orion, handles 2FA via web-form OTP relay, and downloads CSVs
    to S3. This is the core deliverable that has never been built.
  </objective>

  <scope>
    Author:
    - infra/aws/ec2/inf-exporter/src/stepwise/orion_export.ts — main driver (spec below)
    - infra/aws/ec2/inf-exporter/src/stepwise/types.ts — selector constants (from TO-B spec) + ExporterState enum

    OTP relay spec (web-form model):
    - Credentials: fetch from Secrets Manager orion/credentials at runtime (NEVER env vars in prod)
    - OTP flow when 2FA triggered:
        await s3.putObject({ Bucket, Key: 'otp/state.json', Body: JSON.stringify({state:'WAITING_FOR_OTP', ts: new Date().toISOString()}) })
        // W6.3 HOOK: add sns.publish(TopicArn, Message including FUNCTION_URL) here
        const otp = await pollForOTP({ bucket: INF_S3_BUCKET, key: 'otp/current.txt', intervalMs: 5000, timeoutMs: 300000 })
        if (!otp) { await writeState('FAILED_OTP_TIMEOUT'); process.exit(2) }
        await s3.deleteObject({ Bucket, Key: 'otp/current.txt' })
        await page.fill(ORION_SELECTORS.login.otpInput, otp)
        await page.click(ORION_SELECTORS.login.otpSubmit)
    - S3 SDK: AWS SDK v3 (not CLI subprocess)
    - Screenshot discipline: upload to s3://opal-data-inf/otp/debug/{date}/ at each state transition
      (stage1-username, stage2-post-submit, stage3-2fa-detect, export-page)
    - Export: navigate to TRN, AUM, SlickGrid templates, download each CSV, upload to
      s3://opal-data-inf/bronze/orion/YYYY-MM-DD/{file}.csv
    - Write otp/state.json = {state:"EXPORT_COMPLETE"} on success

    Exit codes:
    - 0 = export complete, all files uploaded
    - 1 = login failed (bad credentials)
    - 2 = OTP timeout (no code in 5 min)
    - 3 = export/download failed
    - 4 = S3 upload failed

    Deploy: safe-ec2-deploy.sh (CLAUDE.md Rule 7). Source committed to repo first.
    tsc --noEmit must exit 0 before commit.
  </scope>

  <acceptance_criteria>
    1. tsc --noEmit exits 0.
    2. Credentials fetched from Secrets Manager only (never env vars for production run).
    3. Stage-1, Stage-2 dry-run via SSM: script reaches OTP state (or export page if no 2FA) and
       writes correct otp/state.json. Screenshots uploaded to debug prefix.
    4. OTP polling loop verified: manually write test value to otp/current.txt during paused run;
       script reads + deletes + continues.
    5. Export: at least 3 CSV files uploaded to bronze/orion/{date}/.
    6. safe-ec2-deploy.sh used per CLAUDE.md Rule 7.
    7. infra/aws/ec2/inf-exporter/src/stepwise/ committed to repo.
    8. Session log with SSM run trace + S3 artifact list.
    9. RAVC4 to 2.0.0_SA_COO with: tsc result, SSM run trace summary, S3 artifact list.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT use CLI subprocess for S3 uploads — use AWS SDK v3.</rule>
    <rule>Do NOT hardcode credentials — Secrets Manager only.</rule>
    <rule>Do NOT skip the W6.3 HOOK comment — TO-E needs that hook point.</rule>
    <rule>Do NOT use safe-ec2-deploy.sh alternative or direct EC2 push — CLAUDE.md Rule 7.</rule>
  </do_not>
</task_order>
