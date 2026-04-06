<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-gldrst-009-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
    <!-- Completed 2026-04-06. Run 5 (incremental) finished 16:29 UTC. 2,319 keys in new gold/timeseries/ layout (target 2,284+). Pipeline manifest confirmed. All 13 scripts succeeded. -->
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Full gold rerun after .004 Phase A (dual-write) to populate all new
    S3 key paths. Validate that new keys exist and match old keys.
    This enables .007 (Lambda migration) and .008 (CloudFront migration).
  </objective>

  <requirements>
    <requirement id="1">
      Pull latest CLOUD (must include .004 Phase A commits).
      Run full gold layer: ./run_gold_layer.sh full
    </requirement>

    <requirement id="2">
      Post-run validation: for each key in the migration map (.004 session log),
      verify the new S3 key exists and has the same file size as the old key.
      aws s3 ls old_key vs aws s3 ls new_key
    </requirement>

    <requirement id="3">
      Do NOT delete old keys. They remain until .008 (CloudFront) completes.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All new-layout S3 keys exist after gold rerun</criterion>
    <criterion id="2">New keys match old key file sizes within tolerance</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Requires .004 Phase A to be committed on CLOUD</constraint>
    <constraint>Do NOT remove old keys</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_GLDRST.004" status="pending">
      Phase A dual-write must be committed
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="artifact">New-layout S3 keys populated</deliverable>
    <deliverable type="document">Validation report: old vs new key comparison</deliverable>
  </deliverables>
  <tooling>
    <tool module="adapt.differential_regression" when="after_rerun">
      After gold rerun completes: diff new-layout S3 keys against old-layout keys.
      Every old key must have a corresponding new key with matching file size.
      Additions (new keys) expected. Removals (missing old keys) are regressions.
    </tool>

    <tool module="adapt.coverage_auditor" when="after_rerun">
      Compare: expected new-layout key set (from s3_layout.py registry) vs actual
      S3 keys produced by the rerun. Any expected key missing is a gap. Any
      unexpected key is an artifact of incomplete migration.
    </tool>
  </tooling>
</task_order>
