<task_order>
  <metadata>
    <id>0.6.0_AE_PartnerETL-2026-04-14-bdpl-astdim-w7</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>BDPL_ASTDIM</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/BD_ASSET_DIM_PIPELINE.md</ref>
    <ref type="prd_section">Acceptance Criteria (Project-Level)</ref>
  </references>

  <objective>
    Verify the first three consecutive scheduled prod runs land cleanly:
    - bronze xlsx written to s3://opal-data-bd/bronze/assets/ within 15 min of slot
    - silver/assets/{YYYY-MM-DD}.parquet partition written
    - silver/bd_assets.parquet regenerated (if applicable)
    - CloudWatch log + S3 runner log: zero ERROR lines
  </objective>

  <acceptance_criteria>
    1. Three consecutive Mon-Fri runs verified clean
    2. Per-run S3 + CloudWatch evidence captured in session log
    3. Project-level acceptance criteria 1-4 from PRD all satisfied
    4. MCP COMPLETE message to COO requesting project closure
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 3: Read CloudWatch log of each scheduled run; confirm artifacts.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.6.0_AE_PartnerETL" task="BDPL_ASTDIM.W6" status="staged" description="EventBridge rule must be live"/>
  </dependencies>

  <next>
    On COMPLETE: COO closes BDPL_ASTDIM in REGISTRY (Active → Completed). W8 (gold integration) spawns as separate project per PRD.
  </next>
</task_order>
