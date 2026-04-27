<task_order>
  <metadata>
    <id>ADVI_INFLEC.TO-D.ae-bronze-scraper-unit-tests</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-27</date>
    <status>staged</status><!-- Gate: TO-B (selector spec + Andrew confirm). Parallelizable with TO-C after TO-B. -->
    <project_code>ADVI_INFLEC</project_code>
    <wave>TO-D</wave>
    <reassigned_from>0.6.1_AE_PartnerETL W3.B.1 (offline 3+ days)</reassigned_from>
    <gates_on>TO-B RAVC4 (selector spec + Andrew confirmation)</gates_on>
    <parallel_with>TO-C (after TO-B completes)</parallel_with>
  </metadata>

  <prd_ref>docs/architecture/ADVI_INFLEC_BRONZERUN_V2.md §5 TO-D (cc170c00)</prd_ref>

  <objective>
    Author and run three-stage Orion login unit tests on inf-exporter EC2.
    Confirms real Orion login behavior against the selector spec from TO-B.
    Parallelizable with TO-C once TO-B completes.
  </objective>

  <scope>
    Author three test scripts in infra/aws/ec2/inf-exporter/src/stepwise/:
    1. test-login-stage-1.ts — username entry + screenshot
       - Navigate to login URL
       - Fill username field (from ORION_SELECTORS)
       - Take screenshot → upload to s3://opal-data-inf/otp/debug/{date}/stage1.png
       - Exit 0 on success

    2. test-login-stage-2.ts — password submit + page classification
       - Continue from Stage 1 state
       - Fill password field + click submit
       - Classify result: OTP page vs export page vs error page
       - Screenshot → debug prefix
       - Exit 0 on success

    3. test-login-stage-3.ts — 2FA detection + state output
       - If OTP page detected: write otp/state.json = {state:"WAITING_FOR_OTP"}
       - If no OTP: write otp/state.json = {state:"LOGGED_IN"}
       - Screenshot both branches
       - Exit 0 on success

    Deploy all three via safe-ec2-deploy.sh. Run each via SSM SendCommand on inf-exporter.
    Document actual Orion behavior (exit codes, state observed, any selector mismatches vs spec).

    If any selector mismatch vs TO-B spec: update types.ts, document delta, RAVC to AE for
    TO-C awareness if TO-C is concurrent.
  </scope>

  <acceptance_criteria>
    1. test-login-stage-1.ts: tsc --noEmit exits 0. SSM run: navigates to login, fills username,
       screenshot uploaded.
    2. test-login-stage-2.ts: tsc --noEmit exits 0. SSM run: submits credentials, page classified.
    3. test-login-stage-3.ts: tsc --noEmit exits 0. SSM run: 2FA detected/skipped, state.json written.
    4. safe-ec2-deploy.sh used for EC2 deploy of all three.
    5. All three source files committed to infra/aws/ec2/inf-exporter/src/stepwise/.
    6. AC7: Actual selector values confirmed from TO-B spec match live Orion page. If mismatch:
       update types.ts and document delta vs spec.
    7. AC8: Session log includes raw exit codes + stdout for all three stage runs.
    8. RAVC4 to 2.0.0_SA_COO with: exit codes, S3 screenshot paths, selector match/mismatch status.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT guess selectors — use only values from TO-B selector spec.</rule>
    <rule>Do NOT skip safe-ec2-deploy.sh — CLAUDE.md Rule 7.</rule>
  </do_not>
</task_order>
