# ADVI_REBORN.W1-005 — DE: Portal Endpoint-to-Component Map

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-07-reborn-w1-005-de</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <!-- 2026-04-13 COO close-out (CTO memo, Andrew-directed cross-org reconciliation): DEPRECATED. Superseded by comp-* tool suite; endpoint->component map now produced on-demand by comp-routes/comp-transform/comp-platinum. -->
    <project_code>ADVI_REBORN</project_code>
    <phase>WS1</phase>
  </metadata>

  <objective>
    Map every API function in advisor-intelligence.ts to: the S3 key it resolves to (via CloudFront + router), the TypeScript type it casts to, which React component(s) consume it, and which fields are displayed.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_REBORN_WS1_WS3_VALIDATION.md</ref>
  </references>

  <deliverable>Endpoint-to-component map.</deliverable>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_REBORN.W1-001" status="complete">Needs manifest to cross-reference S3 keys</dependency>
  </dependencies>

  <commit_pattern>audit(REBORN): endpoint-to-component map</commit_pattern>
</task_order>
