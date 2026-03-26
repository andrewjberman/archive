<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-gldrst-008-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>blocked</status>
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Update CloudFront origin path mappings to serve portal artifacts
    from the new GLDRST S3 layout. After this, the portal reads from
    gold/artifacts/ and gold/entities/ instead of the old flat paths.

    This is the final consumer migration step. After this, old S3 keys
    can be cleaned up.
  </objective>

  <context>
    CloudFront shared-advisor-router rewrites:
      /api/scoped/advisor-intelligence/* -> gold/* in opal-data-bd

    After GLDRST, these routes change:
      /api/scoped/advisor-intelligence/architect_leaderboard.json
        -> gold/artifacts/architect_leaderboard.json (was gold/architect_leaderboard.json)
      /api/scoped/advisor-intelligence/advisors/{id}/book.json
        -> gold/entities/advisors/{id}/book.json (was gold/advisors/{id}/book.json)
      etc.

    Terraform manages CloudFront behaviors.
  </context>

  <requirements>
    <requirement id="1">
      Update CloudFront origin path rewrite rules to map portal API
      routes to the new S3 key layout.
    </requirement>

    <requirement id="2">
      Verify all portal routes work end-to-end against the new paths
      before removing dual-write from publishers.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All portal API routes serve from new S3 paths</criterion>
    <criterion id="2">End-to-end verified: portal loads all tabs without errors</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Requires .007 (Lambda dual-write to new paths) to be deployed</constraint>
    <constraint>Must follow Terraform deployment protocol</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="ADVI_GLDRST.007" status="blocked">
      Lambda dual-write must be deployed first
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="deploy">CloudFront behavior Terraform update</deliverable>
  </deliverables>
</task_order>
