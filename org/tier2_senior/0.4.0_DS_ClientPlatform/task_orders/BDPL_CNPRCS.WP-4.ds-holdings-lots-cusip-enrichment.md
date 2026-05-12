<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-bdpl-cnprcs-wp4</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>complete</status>
    <!-- CLOSED 2026-05-12 by 2.0.0_SA_COO per Andrew directive: bulk-close pending/unaddressed pre-May 2026 TOs. Inherits closure from parent project state or supersession. Re-author as new TO if work still required. -->
    <project_code>BDPL_CNPRCS</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md (WP-4)</ref>
  </references>

  <objective>
    Enrich gold/holdings_lots + gold/positions_cube with CUSIP, asset_id, bd_super_class,
    bd_segment. Plumb CUSIP through B_01.holdings_lots.py → B_02.canonical_lots.py.
    Fallback join on (ticker, asset_name) for lots that cannot be re-sourced.
  </objective>

  <acceptance_criteria>
    1. ≥90% of open 49F lots have non-null cusip OR asset_id
    2. 100% have non-null bd_super_class (fallback 'Unclassified' allowed)
    3. New columns visible in gold/holdings_lots and gold/positions_cube
    4. MCP COMPLETE to COO with commit + enrichment coverage snapshot
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io B_01.holdings_lots.py` + `comp-pipescript consumers gold/holdings_lots`; `comp-blast B_01.holdings_lots` + `comp-blast B_02.canonical_lots` (new CUSIP column blast-check — who reads these in gold).
    Phase 2: `python -m py_compile`.
    Phase 3: `comp-pipescript deployed`.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="BDPL_ASTDIM.W4" status="staged" description="silver/bd_assets.parquet must exist"/>
    <dependency agent="0.6.0_AE_PartnerETL" task="BDPL_CNPRCS.WP-3" status="staged" description="cusip in silver/transactions"/>
  </dependencies>

  <next>
    On COMPLETE: unblocks WP-5, WP-6, WP-9.
  </next>
</task_order>
