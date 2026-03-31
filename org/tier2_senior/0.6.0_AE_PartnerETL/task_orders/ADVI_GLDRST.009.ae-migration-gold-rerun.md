<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-gldrst-009-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-26</date>
    <status>staged</status>
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
</task_order>
