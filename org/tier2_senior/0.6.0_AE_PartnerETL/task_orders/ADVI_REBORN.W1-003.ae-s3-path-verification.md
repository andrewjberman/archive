# ADVI_REBORN.W1-003 — AE: S3 Key Existence + Freshness Check

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-07-reborn-w1-003-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <!-- 2026-04-13 COO close-out (CTO memo, Andrew-directed cross-org reconciliation): SUPERSEDED by ADVI_GLDRST.014 + comp-pipescript/comp-routes authoritative I/O mapping. Never GOed. -->
    <project_code>ADVI_REBORN</project_code>
    <phase>WS1</phase>
  </metadata>

  <objective>
    Using the manifest from W1-001, verify every S3 key: exists, has fresh LastModified (< 24h for daily artifacts), and is accessible via CloudFront URL.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_REBORN_WS1_WS3_VALIDATION.md</ref>
  </references>

  <deliverable>Path verification report with pass/fail per key.</deliverable>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_REBORN.W1-001" status="complete">Needs manifest for S3 key list</dependency>
  </dependencies>

  <commit_pattern>audit(REBORN): S3 path verification report</commit_pattern>
</task_order>
