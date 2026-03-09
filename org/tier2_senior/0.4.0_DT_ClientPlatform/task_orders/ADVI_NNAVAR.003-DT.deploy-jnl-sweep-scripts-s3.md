<task_order>
  <metadata>
    <id>ADVI_NNAVAR.003-DT.deploy-jnl-sweep-scripts-s3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-09</date>
    <status>pending</status>
  </metadata>

  <objective>
    Upload the JNL/sweep canonical fix scripts (05 and 05b) to S3 so bd-gold-layer-runner
    picks them up on next sync. DO NOT trigger a gold rebuild. This task is purely a
    code deployment -- the rebuild is deferred until ADVI_49FNV3 is complete.
  </objective>

  <context>
    Andrew authorized the JNL/sweep fix as part of the NNAVAR production rebuild bundle
    (COO decision log 2026-03-09). The fix removes non-NNA transactions (internal journals,
    Schwab-to-Schwab transfers, SEP and FDIC bank sweeps) from NNA computation in scripts
    05 and 05b. Commits 9bfb289b + b4f2d7a7 are on CLOUD branch.

    AUAVAR Script 02 (BKF forward-fill fix, commit 91b1918a) is already deployed.
    No further action needed for Script 02.

    The gold rebuild will be triggered in a future session after ADVI_49FNV3 completes.
  </context>

  <requirements>
    <requirement id="1">Upload the current CLOUD branch version of
      `data/black_diamond/scripts/gold/05_build_client_performance.py` to S3 at the
      canonical EC2 code path for this script. Follow EC2_CODE_DEPLOYMENT_STANDARD.md
      (S3 artifact model -- write locally, upload to S3, EC2 pulls from S3).</requirement>
    <requirement id="2">Upload the current CLOUD branch version of
      `data/black_diamond/scripts/gold/05b_build_account_performance.py` to the same
      S3 path pattern.</requirement>
    <requirement id="3">Verify both uploads by checking the S3 object timestamps or
      ETags after upload.</requirement>
    <requirement id="4">DO NOT run or trigger the gold layer pipeline. DO NOT invoke
      run-gold-layer.sh or any equivalent. Deploy only.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Both 05 and 05b uploaded to S3 at the correct code path for
      bd-gold-layer-runner (i-01003b035d2988dfb).</criterion>
    <criterion id="2">No rebuild triggered. No EC2 pipeline invocation.</criterion>
    <criterion id="3">Session log written confirming S3 object paths and ETags.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not trigger any gold rebuild or pipeline run. Deploy only.</constraint>
    <constraint>This task can be executed at any time -- no urgency. Complete it before
      ADVI_49FNV3 wraps up so the rebuild can be triggered immediately when authorized.</constraint>
  </constraints>

  <references>
    <ref type="decision_log">org/tier1_exec/2.0.0_SA_COO/logs/2026-03-09/nnavar_rebuild_decision.md</ref>
    <ref type="standard">docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md</ref>
    <ref type="commits">9bfb289b (script 05), b4f2d7a7 (script 05b)</ref>
  </references>
</task_order>
