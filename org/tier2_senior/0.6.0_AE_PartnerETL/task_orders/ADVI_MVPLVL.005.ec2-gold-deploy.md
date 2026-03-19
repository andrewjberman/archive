<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-16-005-ae-ec2-deploy</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-16</date>
    <status>complete</status>
    <thread_serial>ADVI_MVPLVL-005</thread_serial>
    <thread_ref>org/threads/ADVI_MVPLVL-005-addendum-a-mix-timeseries-alignment/</thread_ref>
  </metadata>

  <objective>
    Deploy 06b gold script to EC2 gold runner, wire into run_gold_layer.sh in both
    full and incremental modes, and execute the first full rebuild to backfill all
    ~2,081 positions_cube dates.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/run_gold_layer.sh</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Wire 06b into run_gold_layer.sh after `06_build_client_tax_liability.py`, before
      `07_build_nna_aua_by_geography.py`. Use `run_script()` (not `|| true`).
      Full mode: `run_script "$SCRIPTS_DIR/06b_build_client_mix_timeseries.py"`
      Incremental mode: `run_script "$SCRIPTS_DIR/06b_build_client_mix_timeseries.py" --incremental`
    </requirement>
    <requirement id="2">
      Deploy to EC2 via `safe-ec2-deploy.sh bd-gold-layer-runner deploy-to-ec2.sh`.
      Never deploy directly. Verify S3 script count = 17 (currently 16).
    </requirement>
    <requirement id="3">
      Trigger first full rebuild on EC2 (i-01003b035d2988dfb). Monitor until both
      artifacts appear at `s3://opal-data-bd/gold/client_mix_timeseries.parquet` and
      `s3://opal-data-bd/gold/client_concentration_timeseries.parquet`.
    </requirement>
    <requirement id="4">
      Validate Gate 2: pct sum ≈ 1.0 for all (date, relationship_id) in mix artifact.
      Download a sample and verify. Lambda deployment MUST NOT proceed until this passes.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">run_gold_layer.sh has 06b wired in both full and incremental sections</criterion>
    <criterion id="2">S3 script count = 17 after deploy</criterion>
    <criterion id="3">Both gold artifacts exist at confirmed S3 keys after full rebuild</criterion>
    <criterion id="4">Gate 2 pct sum validation passes on a sample of relationships</criterion>
    <criterion id="5">Next nightly incremental run completes without error (artifact timestamps update)</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Always use safe-ec2-deploy.sh — never direct EC2 deployment</constraint>
    <constraint>Do NOT deploy the Lambda endpoints — that is DT's task order</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MVPLVL.005.gold-script-and-endpoints" status="complete">
      06b gold script committed (6cae4815). run_gold_layer.sh wired (d1bd3a18). EC2 deployed (9ee5a752). Gate 2 validation pending.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">run_gold_layer.sh wiring committed to CLOUD</deliverable>
    <deliverable type="commit">EC2 deploy via safe-ec2-deploy.sh</deliverable>
    <deliverable type="document">Gate 2 validation results in session log</deliverable>
  </deliverables>
</task_order>
