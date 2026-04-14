<task_order>
  <metadata>
    <id>0.6.0_AE_PartnerETL-2026-04-14-bdpl-astdim-w5</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-14</date>
    <status>complete</status><!-- 2026-04-14: TS shipped, layout migrated to backfill_v2/forwardfill_v2 pattern, full silver history backfilled (1823 partitions, 3.19M txns), W1 absorbed into W5 by AE per Andrew direction -->
    <project_code>BDPL_ASTDIM</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/BD_ASSET_DIM_PIPELINE.md</ref>
    <ref type="analog">infra/aws/ec2/bd-exporter/src/stepwise/download-daily-fees.ts</ref>
  </references>

  <objective>
    Write `download-daily-asset-dim.ts` mirroring `download-daily-fees.ts`.
    Hard-code `TEMPLATE_NAME = 'AssetDimTXNs_OpalCapital_Daily'` and default
    `S3_PREFIX = 'bronze/assets'`. No env override for template name (PRD discipline).
    Deploy to `bd-exporter` EC2 via standard EC2 code deployment standard
    (write locally → upload to S3 → EC2 pulls from S3).
  </objective>

  <acceptance_criteria>
    1. `infra/aws/ec2/bd-exporter/src/stepwise/download-daily-asset-dim.ts` committed
    2. `tsc` compile passes locally
    3. Manual test invocation on bd-exporter (via SSM RunCommand) writes a test xlsx to bronze/assets/
    4. MCP COMPLETE message to COO with commit hash + S3 test-file path
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: Read `download-daily-fees.ts` in full.
    Phase 2: `tsc --noEmit` exits 0.
    Phase 3: SSM test invocation S3-uploaded test file confirmed via `aws s3 ls`.
  </compiler_tools_mandate>

  <dependencies>
    <none/>
  </dependencies>

  <next>
    On COMPLETE: COO sends GO for W6 (SSM doc + Lambda trigger + EventBridge + terraform apply).
  </next>
</task_order>
