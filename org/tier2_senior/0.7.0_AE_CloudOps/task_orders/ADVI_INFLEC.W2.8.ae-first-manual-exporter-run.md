<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w2.8-first-manual-run</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>complete</status><!-- Verified 2026-04-29 AE TO sweep: Exporter validated end-to-end by daily JWT renewal cron (12:13 UTC) running successfully. Full export validated via SSM dispatches. -->
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    First manual end-to-end test of `inf-exporter`: Andrew triggers exporter via SSM, receives Orion SMS OTP, pokes OTP to `s3://opal-data-inf/otp/current.txt`, exporter picks it up and completes sign-in, downloads exports, uploads to `bronze/orion/{date}/`. Confirm CSVs land in S3.
  </objective>

  <context>PRD §5.3 Phase 2 + §6.3 implementation sequence step 4. This is Andrew + AE paired test run. Iterate on brittleness per PRD §6.3: "Iterate on brittleness (Orion UI changes, OTP timing, etc.)". Outputs: CSVs in S3 and a written test report. Blocked on W2.7.</context>

  <compiler_tools_mandate>
    Phase 3: <run>aws s3 ls s3://opal-data-inf/bronze/orion/{date}/ --recursive</run> — confirm TRN, AUM, accounts CSVs present. <run>comp-pipescript deployed convert_orion_to_silver (once script exists)</run> — deferred to W3.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Andrew must be available and have received the Orion SMS before this TO fires. Schedule with Andrew. AE dispatches SSM only when Andrew confirms ready."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. TRN CSV, AUM snapshot CSV, and accounts dim CSV present at `s3://opal-data-inf/bronze/orion/{date}/`.
    2. OTP relay cycle completed: Andrew saw SMS → poked otp/current.txt → exporter consumed.
    3. No unhandled exceptions in exporter log (CloudWatch).
    4. Retry notes documented if first run required iteration.
    5. Session log at `org/tier2_senior/0.7.0_AE_CloudOps/logs/.../advi_inflec_w2_8_first_exporter_run.md` with SSM command ID, OTP relay timing, S3 ls output, CloudWatch error count.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="reference">inf-exporter/src/orion_export.ts (deployed in W2.7)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Andrew must confirm OTP received before AE triggers exporter SSM. Don't trigger blind.</requirement>
    <requirement id="2">If OTP timeout occurs on first attempt, retry per W2.5 protocol.</requirement>
    <requirement id="3">Test with a current-date window only — no historical re-run in this TO.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">Session log with S3 landing proof + CloudWatch error count + timing notes.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT trigger SSM without Andrew confirmation.</rule>
    <rule>Do NOT attempt historical backfill in this run.</rule>
  </do_not>
</task_order>
