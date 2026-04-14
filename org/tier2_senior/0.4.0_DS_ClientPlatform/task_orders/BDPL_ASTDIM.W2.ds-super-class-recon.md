<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-bdpl-astdim-w2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>BDPL_ASTDIM</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/BD_ASSET_DIM_PIPELINE.md</ref>
    <ref type="prd_section">D3 — BD asset_super_class vs ETFClassifier (blend, do not supersede)</ref>
  </references>

  <objective>
    Enumerate BD's distinct `asset_super_class` values across all 16 bronze xlsx files
    with row counts. Output: `data/black_diamond/recon/bd_asset_super_class_values.md`.
    This recon is the GATE for W4 blend rule — DS cannot write
    `build_bd_assets_dim.py` (W4) without it.
  </objective>

  <acceptance_criteria>
    1. `data/black_diamond/recon/bd_asset_super_class_values.md` committed to CLOUD
    2. Doc lists every distinct `asset_super_class` value + total row count + nullable %
    3. Doc proposes the BD→ETFClassifier blend mapping (which BD values are "coarse"
       and trigger ETFClassifier fallback)
    4. MCP COMPLETE message to COO with commit hash + summary line
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io convert_fees_to_silver.py` (xlsx-to-pandas read pattern).
    Phase 2: `python -m py_compile` on any helper script used.
    Phase 3: Recon doc has all distinct values from the 16 xlsx files (DS verifies count).
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="BDPL_ASTDIM.W1" status="staged" description="Bronze files in S3 enable repeatable recon path; local xlsx is acceptable too"/>
  </dependencies>

  <next>
    On COMPLETE: COO sends parallel GO for W3 + W4. W4 blend rule references this recon doc.
  </next>
</task_order>
