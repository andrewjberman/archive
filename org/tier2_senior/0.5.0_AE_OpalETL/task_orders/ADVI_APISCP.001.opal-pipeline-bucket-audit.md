<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-opal-pipeline-bucket-audit</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-03-10</date>
    <status>pending</status>
  </metadata>

  <objective>
    Audit yang-pipeline, news-pipeline, and market-overview publisher output paths.
    Confirm all Opal-owned pipelines write exclusively to opal-data-portal-v2 and have
    ZERO overlap with opal-data-{firmId} partner bucket patterns. Document the bucket
    separation invariant in pipeline_inventory.xml.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Audit yang-pipeline publisher output: confirm all S3 writes go to
      opal-data-portal-v2/json/ or opal-data-portal-v2/json-tiered/ exclusively.
      Check yang-portal-publisher and any related publishers.
    </requirement>
    <requirement id="2">
      Audit news-pipeline publisher output: confirm all S3 writes go to
      opal-data-portal-v2/json/ exclusively. Check news-portal-publisher,
      opal-trending-topics-portal-publisher, etc.
    </requirement>
    <requirement id="3">
      Audit market-overview publisher output: confirm all S3 writes go to
      opal-data-portal-v2/json/ or opal-data-portal-v2/json-tiered/ exclusively.
    </requirement>
    <requirement id="4">
      Confirm NO Opal-owned pipeline writes to opal-data-bd/ or any opal-data-{firmId}/
      bucket. The opal-data-* pattern is reserved for partner data.
    </requirement>
    <requirement id="5">
      Update pipeline_inventory.xml to document the bucket separation:
        "Yang/News/MarketOverview pipelines write ONLY to opal-data-portal-v2.
         Partner pipelines write ONLY to opal-data-{firmId}.
         These are separate, non-overlapping patterns."
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All three Opal pipelines confirmed to write only to opal-data-portal-v2</criterion>
    <criterion id="2">No Opal pipeline writes to any opal-data-{firmId} bucket</criterion>
    <criterion id="3">pipeline_inventory.xml documents the bucket separation invariant</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>This is audit + documentation only. Do not modify Lambda code or deploy anything.</constraint>
    <constraint>Do not modify PartnerETL pipelines — 0.6.0_AE_PartnerETL has their own task order.</constraint>
  </constraints>

  <dependencies>
    <!-- No blocking dependencies. Can proceed immediately in parallel with all other agents. -->
  </dependencies>

  <references>
    <ref type="prd">docs/architecture/ADVI_APISCP_PRD.md</ref>
  </references>

  <deliverables>
    <deliverable type="document">Updated pipeline_inventory.xml with bucket separation invariant</deliverable>
    <deliverable type="document">Session log with audit findings per pipeline</deliverable>
  </deliverables>
</task_order>
