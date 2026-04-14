<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-bdpl-astdim-w3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>BDPL_ASTDIM</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/BD_ASSET_DIM_PIPELINE.md</ref>
    <ref type="analog">data/black_diamond/scripts/silver/convert_fees_to_silver.py</ref>
    <ref type="analog">data/black_diamond/scripts/silver/merge-daily-incremental.py</ref>
  </references>

  <objective>
    Write the silver converter + daily merge scripts and backfill silver/assets/ from
    all 16 bronze files.

    Deliverables:
    - `data/black_diamond/scripts/silver/convert_assets_to_silver.py` (bronze xlsx → silver/assets/{date}.parquet)
    - `data/black_diamond/scripts/silver/merge-daily-assets-incremental.py` (daily merge pattern)
    - `data/black_diamond/scripts/silver/bd_asset_join.py` (shared 4-tier join cascade helper per PRD D1)
    - Silver backfill: `silver/assets/{YYYY-MM-DD}.parquet` for every trade date covered by 16 bronze files
    - All scripts uploaded to `s3://opal-data-bd/code/silver/`
  </objective>

  <acceptance_criteria>
    1. All 3 .py scripts committed to CLOUD
    2. `aws s3 ls s3://opal-data-bd/silver/assets/` shows one parquet per trade date
    3. Spot-check parquet row count matches sum across overlapping bronze files
    4. `bd_asset_join.py` exposes a single resolve function with the 4-tier cascade
       (asset_id → cusip → ticker → alternative_identifier)
    5. MCP COMPLETE message to COO with commit hash + S3 listing
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io convert_fees_to_silver.py`.
    Phase 2: `python -m py_compile` on each new .py.
    Phase 3: `comp-pipescript deployed convert_assets_to_silver.py` — MATCH expected.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="BDPL_ASTDIM.W1" status="staged" description="Bronze files must exist in S3"/>
  </dependencies>

  <next>
    On COMPLETE: COO checks W2+W3 both done → sends GO for W4.
  </next>
</task_order>
