# ADVI_REBORN.W1-004 — DT: Terraform + CloudFront Verification

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-07-reborn-w1-004-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-07</date>
    <status>staged</status>
    <project_code>ADVI_REBORN</project_code>
    <phase>WS1</phase>
  </metadata>

  <objective>
    Using the manifest from W1-001, verify Terraform resources match: CloudFront behaviors route to correct S3 origins, Lambda@Edge shared-advisor-router serves correct firm data, no stale behaviors pointing to pre-restructure S3 keys.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_REBORN_WS1_WS3_VALIDATION.md</ref>
  </references>

  <deliverable>Terraform verification report.</deliverable>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_REBORN.W1-001" status="complete">Needs manifest for key list</dependency>
  </dependencies>

  <commit_pattern>audit(REBORN): Terraform path verification</commit_pattern>
</task_order>
