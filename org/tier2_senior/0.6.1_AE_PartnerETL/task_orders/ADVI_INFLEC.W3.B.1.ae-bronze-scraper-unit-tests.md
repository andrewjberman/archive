<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-24-inflec-w3.b.1-ae-bronze-scraper</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <date>2026-04-24</date>
    <status>cancelled</status><!-- CANCELLED/REASSIGNED 2026-04-27 by 2.0.0_SA_COO per PRD v2.0. AE 0.6.1 offline 3+ days. Reassigned to 0.7.0_AE_CloudOps as TO-D (ADVI_INFLEC.TO-D.ae-bronze-scraper-unit-tests.md). Spec unchanged except agent. -->
    <project_code>ADVI_INFLEC</project_code>
    <wave>W3.B.1</wave>
    <parallel_with>W3.B.2</parallel_with>
    <gates>W3.B.4</gates>
    <prd>docs/architecture/ADVI_INFLEC_BRONZERUN.md §5.1</prd>
  </metadata>

  <objective>
    Author all TypeScript scripts in `infra/aws/ec2/inf-exporter/src/stepwise/` for the Orion
    bronze exporter. Includes the types file, three staged login unit tests, and the main export
    script. Deploy to inf-exporter EC2 via S3-pull model. Run all three stage tests live to
    confirm selector fidelity and page-state detection before authoring the full export script.
  </objective>

  <context>
    The inf-exporter EC2 (i-081ae6aafb394fb1a, t3.medium) is fully provisioned with bun,
    Playwright, chromium, and xvfb per `infra/aws/ec2/inf-exporter/user-data.sh`. App dir
    `/opt/inf-exporter/src/stepwise/` exists on EC2 but is empty — no scripts are deployed.
    The repo dir `infra/aws/ec2/inf-exporter/src/` does not exist yet.

    BD precedent for Playwright pattern: `infra/aws/ec2/bd-exporter/src/stepwise/download-daily-fees.ts`
    and `infra/aws/ec2/bd-exporter/src/stepwise/test-login.ts` — use stealth settings, screenshot
    on state change, S3 upload, exit codes.

    IMPORTANT: Orion CSS selectors are UNKNOWN until Stage 1/2/3 run live against
    https://login.orionadvisor.com/. The multi-selector fallbacks in types.ts are starting points.
    AE must run the stage tests with HEADLESS=false, inspect screenshots, and refine types.ts
    to the confirmed selectors before authoring orion_export.ts.

    Silver converter `data/orion/scripts/silver/convert_orion_to_silver.py` is complete and
    awaits bronze CSVs in `s3://opal-data-inf/bronze/orion/`. Bronze → silver → gold chain
    confirmed correct via comp-pipescript io on gold entry scripts.

    This TO runs in parallel with W3.B.2 (OTP Lambda). Neither depends on the other.
    W3.B.3 (Slack App) and W3.B.4 (E2E validation) gate on this TO completing.
  </context>

  <files_to_create>
    <file>infra/aws/ec2/inf-exporter/src/stepwise/types.ts</file>
    <file>infra/aws/ec2/inf-exporter/src/stepwise/test-login-stage-1.ts</file>
    <file>infra/aws/ec2/inf-exporter/src/stepwise/test-login-stage-2.ts</file>
    <file>infra/aws/ec2/inf-exporter/src/stepwise/test-login-stage-3.ts</file>
    <file>infra/aws/ec2/inf-exporter/src/stepwise/orion_export.ts</file>
  </files_to_create>

  <spec_summary>

    types.ts:
    - ORION_URLS: { login, export } (export URL discovered during Stage 3 test — leave as TODO stub)
    - ORION_SELECTORS: login object with multi-selector fallbacks for username, password, submit,
      otpInput, otpSubmit (refine to confirmed values after Stage 1/2/3 live runs)
    - ExporterState enum: STARTING, WAITING_FOR_OTP, OTP_RECEIVED, EXPORT_IN_PROGRESS,
      EXPORT_COMPLETE, FAILED_OTP_TIMEOUT, FAILED_LOGIN, FAILED_EXPORT

    test-login-stage-1.ts (username entry):
    - Navigate to https://login.orionadvisor.com/
    - Wait for username field, fill with ORION_USERNAME env var
    - Screenshot to /tmp/inf-stage1-username.png, upload to s3://opal-data-inf/otp/debug/test-{date}/stage1.png
    - Exit 0: username field populated, no error banner
    - Exit 1: username field not found (selector mismatch)
    - Exit 2: error banner detected after fill

    test-login-stage-2.ts (password + submit):
    - Run Stage 1, then fill password (ORION_PASSWORD env var), click submit, wait for nav
    - Screenshot uploaded to otp/debug/test-{date}/stage2.png
    - Exit 0: page changed after submit (OTP or export page reached)
    - Exit 1: login page still visible (credentials rejected or no nav)
    - Exit 2: unexpected navigation (error page or timeout)

    test-login-stage-3.ts (2FA detection):
    - Run Stage 1 + Stage 2, then classify post-auth page:
      URL still login.orionadvisor.com → exit 3 (Stage 2 failure)
      OTP field present → print "STATE: OTP_REQUIRED" → exit 1 (expected nominal)
      Export/dashboard URL → print "STATE: NO_OTP_REQUIRED" → exit 0
      Else → print "STATE: UNKNOWN_PAGE" → upload screenshot → exit 2
    - Screenshot to otp/debug/test-{date}/stage3.png

    orion_export.ts (main scraper — author AFTER Stage 3 confirms detection logic):
    - Credentials: fetch from Secrets Manager `orion/credentials` (username + password)
    - Stealth: AutomationControlled disabled, custom UA, locale en-US, timezone America/New_York,
      navigator.webdriver = undefined init script (mirror BD pattern)
    - HEADLESS env var: default true; HEADLESS=false for debug
    - Login → 2FA branch → S3 poll for OTP (poll every 5s, timeout 5 min)
    - OTP cleanup: delete otp/current.txt immediately after reading
    - State machine: write otp/state.json on every ExporterState transition
    - Screenshots at every state: upload to s3://opal-data-inf/otp/debug/{date}/
    - Export templates: TRN + AUM + SlickGrid (actual names discovered on first live run)
    - File naming: keep native Orion filenames, upload to s3://opal-data-inf/bronze/orion/{YYYY-MM-DD}/{filename}.csv
    - S3 upload: AWS SDK v3 @aws-sdk/client-s3 PutObject, ContentType text/csv
    - Exit codes: 0=complete, 1=login failed, 2=OTP timeout, 3=export/download failed, 4=S3 upload failed
    - SKIP_S3=true env var supported for dry-run without writing to bronze bucket (test gate)

    Deployment to EC2:
    - Upload scripts to s3://opal-data-inf/code/exporter/ via aws s3 cp
    - EC2 pulls from S3 before run (same S3-pull model as BD gold scripts)
  </spec_summary>

  <compiler_tools_mandate>
    Phase 1 — before writing:
    <run>comp-iam service inf-exporter</run>
    <expect>S3 RW on opal-data-inf/bronze/orion/* + opal-data-inf/otp/* present.
    Secrets Manager read on orion/credentials present. If any missing: flag to COO before proceeding.</expect>

    Phase 2 — before commit:
    <run>cd infra/aws/ec2/inf-exporter &amp;&amp; bun run tsc --noEmit</run>
    <expect>Exit 0. Zero TypeScript errors across all 5 files.</expect>
    Note: ds-commit-gate.sh does NOT apply (TypeScript, not Python). Use tsc as the gate.

    Phase 3 — after deploy + stage tests:
    <run>Stage 1 via SSM with HEADLESS=false — check screenshot at otp/debug/test-{date}/stage1.png</run>
    <expect>Username field populated. Exit 0.</expect>
    <run>Stage 2 via SSM — check screenshot at otp/debug/test-{date}/stage2.png</run>
    <expect>Page changed after submit. Exit 0. Document actual post-submit URL in session log.</expect>
    <run>Stage 3 via SSM — check screenshot at otp/debug/test-{date}/stage3.png</run>
    <expect>Exit 0 (NO_OTP_REQUIRED) or exit 1 (OTP_REQUIRED). stdout includes STATE: line.
    Does NOT exit 2 (UNKNOWN_PAGE). Document actual Orion selector values in session log.</expect>
    <run>bun run src/stepwise/orion_export.ts with SKIP_S3=true HEADLESS=false via SSM</run>
    <expect>Exit 0 or 2 (OTP timeout acceptable in test). No unhandled exceptions.</expect>
  </compiler_tools_mandate>

  <acceptance_criteria>
    1. Stage 1 exits 0 on live Orion URL. Screenshot shows username field populated.
    2. Stage 2 exits 0. Screenshot shows post-submit page (OTP challenge or export page) — NOT login page unchanged.
    3. Stage 3 exits 0 or 1. stdout contains "STATE: OTP_REQUIRED" or "STATE: NO_OTP_REQUIRED". Does NOT exit 2.
    4. All scripts compile: bun run tsc --noEmit exits 0.
    5. Screenshots uploaded to s3://opal-data-inf/otp/debug/test-{date}/stage{1,2,3}.png.
    6. orion_export.ts runs with SKIP_S3=true HEADLESS=false — exits 0 or 2; no unhandled exception.
    7. All 5 source files committed to CLOUD branch under infra/aws/ec2/inf-exporter/src/stepwise/.
    8. Scripts uploaded to s3://opal-data-inf/code/exporter/.
    9. Actual Orion selector values documented in session log (for types.ts confirmation).
  </acceptance_criteria>

  <deliverables>
    <deliverable type="commit">5 TypeScript files committed to CLOUD under infra/aws/ec2/inf-exporter/src/stepwise/. Author: 0.6.1_AE_PartnerETL.</deliverable>
    <deliverable type="s3">All 5 scripts uploaded to s3://opal-data-inf/code/exporter/.</deliverable>
    <deliverable type="ssm_evidence">Stage 1/2/3 exit codes + screenshot S3 paths + actual selector values logged in session log.</deliverable>
    <deliverable type="mcp">MCP to COO on completion with stage test results + session log path. MCP is the gate signal for W3.B.4.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT hardcode assumed CSS selectors before live Stage 1/2/3 test results confirm them.</rule>
    <rule>Do NOT author orion_export.ts until Stage 3 exits 0 or 1 with a classified state.</rule>
    <rule>Do NOT fetch credentials from environment variables in orion_export.ts — Secrets Manager only.</rule>
    <rule>Do NOT commit Orion credentials, OTP values, or screenshots to git.</rule>
    <rule>Do NOT reopen the SSM-vs-S3 OTP delivery architecture. CTO decision: S3 polling. This is final.</rule>
  </do_not>
</task_order>
