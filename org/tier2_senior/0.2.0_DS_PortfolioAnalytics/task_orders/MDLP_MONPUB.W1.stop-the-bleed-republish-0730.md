<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-08-03-monpub-w1</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics (primary) + 0.2.0_DT_PortfolioAnalytics (execution support)</issued_to>
    <date>2026-08-03</date>
    <status>staged</status>
    <project_code>MDLP_MONPUB</project_code>
  </metadata>

  <objective>
    STOP THE BLEED: the portal Model Portfolios benchmark surface is serving regressed data
    (data_as_of=2026-07-27 after a correct 2026-07-30 publish was silently clobbered).
    Re-run YangDataPipeline with the known-good 2026-07-30 manifest so the serve returns to 07-30
    pending the real 07-31 fix (W4).
  </objective>

  <context>
    Spec: docs/architecture/MDLP_MONPUB_MANIFEST_REGRESSION_FIX.md @d59fc15920 (read sections 1-3 first).
    Finding: 0.7.0_AE_CloudOps~F @99c3e50a36. The good 07-30 execution was 2394c6bf (13:10Z,
    data_pkl + model_pkl manifest); the clobbering 07-27 execution was 0d669fd1 (13:27Z).
    Use execution 2394c6bf's own executionStartedEventDetails.input as the re-run input.
    NOTE: this runs UN-GUARDED (W2 not yet live) -- it is safe only because 07-30 is NEWER than the
    served 07-27. Do not re-run anything else through this path before W2 lands.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before firing):
      <run>aws s3api head-object --bucket opal-data-portal-v2 --key json/benchmarks/model_portfolio_benchmarks.json</run>
      <expect>Body data_as_of reads 2026-07-27 (ETag 0a122e2c95ea9ed673c8977c581dc202 unless something moved since 2026-08-03T14:45Z)</expect>
      <if_mismatch>STOP. The serve moved since this TO was cut. Re-ground against live state and report to CTO before firing anything (08-01 lesson: a "rollback onto itself" once overwrote a deliberately-set vintage).</if_mismatch>
    Phase 3 (after the run):
      <run>aws s3 cp s3://opal-data-portal-v2/json/benchmarks/model_portfolio_benchmarks.json - | head -5 (and same for benchmark_returns.json + model_portfolio_timeseries.json)</run>
      <expect>All three keys read data_as_of=2026-07-30; LastModified &gt; run start</expect>
      <if_mismatch>Partial publish = mixed-vintage serve. Escalate to CTO immediately; do not leave half-landed.</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: opal-data-portal-v2/json/benchmarks/* (all three output keys)
    also_in_to: MDLP_MONPUB.W2 (guard on the same publish path), MDLP_MONPUB.W4 (07-31 re-upload)
    required_action: W1 fires FIRST, before W2 deploys. Do not run W4's re-upload until W2 is live.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. CORRECTNESS: served model_portfolio_benchmarks.json data_as_of == "2026-07-30" exactly,
       AND its ETag != 0a122e2c95ea9ed673c8977c581dc202, AND LastModified &gt; execution start time.
    2. ATOMICITY: all THREE output keys (benchmark_returns.json, model_portfolio_benchmarks.json,
       model_portfolio_timeseries.json) carry identical data_as_of=2026-07-30.
    3. PROVENANCE (forbidden shortcut named): the new artifacts MUST come from a YangDataPipeline
       execution whose ARN you cite -- hand-writing JSON to S3 satisfies criteria 1-2 and is a
       FORGED COMPLETION (Door-6 class); it fails this TO.
    4. THIRD STATE: if the Phase-1 pre-check does not read 07-27, the outcome is NEITHER pass nor
       fail -- it is RE-GROUND, reported to CTO before any mutation.
  </acceptance_criteria>
</task_order>
