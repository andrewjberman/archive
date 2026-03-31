<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-gldrst-010-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-26</date>
    <status>staged</status>
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Remove old-layout S3 keys and disable dual-write in gold scripts.
    This is the final cleanup step after all consumers (scripts, Lambdas,
    CloudFront) have been migrated to new paths.
  </objective>

  <requirements>
    <requirement id="1">
      Verify ALL consumers read from new paths:
      - Gold scripts (.004 Phase B complete)
      - Lambdas (.007 deployed)
      - CloudFront (.008 deployed)
      - Portal (.003 deployed)
    </requirement>

    <requirement id="2">
      Remove dual-write code from gold scripts (DS provides the commit).
      Scripts write only to new paths.
    </requirement>

    <requirement id="3">
      Delete old S3 keys listed in the .004 migration map.
      aws s3 rm for each old key. Log all deletions.
    </requirement>

    <requirement id="4">
      Run one more full gold layer to confirm clean single-write works.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Old S3 keys deleted</criterion>
    <criterion id="2">Scripts no longer dual-write</criterion>
    <criterion id="3">Full gold rerun succeeds with single-write</criterion>
    <criterion id="4">Portal end-to-end verified after cleanup</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>LAST step in GLDRST. All other TOs must be complete.</constraint>
    <constraint>Take S3 inventory backup before deleting old keys</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_GLDRST.004" status="pending">Phase B complete</dependency>
    <dependency agent="0.4.0_DT_ClientPlatform" task="ADVI_GLDRST.007" status="blocked">Lambda migration deployed</dependency>
    <dependency agent="0.4.0_DT_ClientPlatform" task="ADVI_GLDRST.008" status="blocked">CloudFront migration deployed</dependency>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_GLDRST.003" status="blocked">Portal wired to new artifacts</dependency>
  </dependencies>

  <deliverables>
    <deliverable type="artifact">Old S3 keys removed</deliverable>
    <deliverable type="document">Cleanup log with deleted keys inventory</deliverable>
  </deliverables>
</task_order>
