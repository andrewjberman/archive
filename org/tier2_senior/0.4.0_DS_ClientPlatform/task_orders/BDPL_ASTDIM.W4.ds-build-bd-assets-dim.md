<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-bdpl-astdim-w4</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>BDPL_ASTDIM</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/BD_ASSET_DIM_PIPELINE.md</ref>
    <ref type="prd_section">D3 blend rule + W4 acceptance</ref>
    <ref type="recon">data/black_diamond/recon/bd_asset_super_class_values.md (W2 deliverable)</ref>
  </references>

  <objective>
    Write `build_bd_assets_dim.py` producing `silver/bd_assets.parquet` — the
    point-in-time asset dimension table. Apply the BD→ETFClassifier blend rule
    derived from W2 recon: BD `asset_super_class` wins unless null/empty/coarse,
    in which case ETFClassifier (DDB `etf-classifications`) provides super_class.

    **Scope update 2026-04-14 post-W5 AE absorption:** AE compacted silver/bd_assets.parquet
    (3.19M rows) from the xlsx set, but CTO flagged unclear whether AE applied the BD-first /
    ETFClassifier-fallback blend rule (D3). DS's W4 work:
      (a) inspect the compacted file for blend-rule presence (super_class source provenance column / sampling)
      (b) if blend already applied — confirm + flip to complete
      (c) if not applied — rebuild via build_bd_assets_dim.py with the blend rule, atomically replace
    AE has been flagged to confirm from their side; coordinate before overwriting.
  </objective>

  <acceptance_criteria>
    1. `silver/bd_assets.parquet` row count ≥ 10,000 (or document why lower)
    2. `asset_id` column has zero duplicates
    3. `super_class` column is non-null for ≥ 95% of rows after blend
    4. Blend recon log: count of (BD-wins, ETFClassifier-fallback, both-null) printed
    5. Script committed + uploaded to `s3://opal-data-bd/code/silver/`
    6. MCP COMPLETE message to COO with commit hash + recon counts
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: Read W2 recon doc + ETFClassifier DDB schema (`infra/aws/dynamodb/etf-classifications/`); `comp-pipescript io convert_assets_to_silver.py` (input pattern reference); `comp-platinum reverse silver/bd_assets.parquet` (confirm consumer set — critical because BDPL_CNPRCS WP-4 + WP-5 will consume this; blend rule must match what they expect).
    Phase 2: `python -m py_compile build_bd_assets_dim.py`.
    Phase 3: `comp-pipescript deployed build_bd_assets_dim.py` — MATCH expected.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="BDPL_ASTDIM.W2" status="staged" description="Recon doc gates blend rule design"/>
    <dependency agent="0.4.0_DS_ClientPlatform" task="BDPL_ASTDIM.W3" status="staged" description="Silver converter must exist to read partitions"/>
  </dependencies>

  <next>
    On COMPLETE: DS work for this project is done. COO confirms AE is in W5-W7.
  </next>
</task_order>
