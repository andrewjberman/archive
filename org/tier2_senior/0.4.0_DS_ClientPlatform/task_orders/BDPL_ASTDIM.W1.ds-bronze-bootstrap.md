<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-bdpl-astdim-w1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>BDPL_ASTDIM</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/BD_ASSET_DIM_PIPELINE.md</ref>
    <ref type="analog">data/black_diamond/scripts/silver/convert_fees_to_silver.py</ref>
  </references>

  <objective>
    One-time bronze bootstrap. Write `upload_bd_assets_xlsx.py` and upload all 16
    `AssetDimTXNs_OpalCapital_Daily` xlsx files to `s3://opal-data-bd/bronze/assets/`.
    Preserve BD's native filenames. No silver work in this wave.
  </objective>

  <scope>
    <file>data/black_diamond/scripts/silver/upload_bd_assets_xlsx.py</file>
    <s3_target>s3://opal-data-bd/bronze/assets/{native_filename}.xlsx</s3_target>
  </scope>

  <acceptance_criteria>
    1. All 16 xlsx files visible in `aws s3 ls s3://opal-data-bd/bronze/assets/`
    2. Per-file row count printed by upload script (sanity-check the manifest)
    3. Script committed to CLOUD with --author=0.4.0_DS_ClientPlatform
    4. MCP COMPLETE message to COO with commit hash + S3 listing snippet
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1 (before write): `comp-pipescript io convert_fees_to_silver.py` to confirm IO contract pattern.
    Phase 2 (before commit): `python -m py_compile upload_bd_assets_xlsx.py` exits 0.
    Phase 3 (after upload): `aws s3 ls s3://opal-data-bd/bronze/assets/ | wc -l` returns 16.
  </compiler_tools_mandate>

  <dependencies>
    <none/>
  </dependencies>

  <next>
    On COMPLETE: COO sends GO for W2 (super_class recon).
  </next>
</task_order>
