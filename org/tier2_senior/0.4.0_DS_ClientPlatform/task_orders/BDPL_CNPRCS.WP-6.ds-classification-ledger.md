<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-bdpl-cnprcs-wp6</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>BDPL_CNPRCS</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md (WP-6 + Q1 mapping + Q5 migration)</ref>
  </references>

  <objective>
    BD-primary append-only classification ledger. Demote DDB ETFClassifier to fallback.
    Migrate ticker_overrides.json into ledger and delete the JSON file.

    1. New ledger `silver/bd_asset_classifications/{YYYY-MM-DD}.parquet` (immutable daily).
    2. Primary classification = BD SuperClass via Q1 mapping:
         Equities -> equity; Fixed Income -> fixed_income; Cash&CE -> cash;
         DIVERSIFIER -> alternatives; To Be Classified -> alternatives;
         Unclassified -> other.
    3. ETFClassifier (DDB) demoted to fallback for assets not in silver/bd_assets.
    4. Deprecate B_01b.classify_new_securities.py keyword heuristics for BD-covered universe.
    5. Migrate ticker_overrides.json entries with source='manual_override'; DELETE the JSON.
    6. Update lib/mix_views.py MIX_ASSET_CLASSES to read from ledger.
    7. Also absorb the tactical 3-bond scoped_price_exceptions entries as source='custodial_override'
       once the ledger is live; retire scoped_price_exceptions.json.
  </objective>

  <acceptance_criteria>
    1. ≥98% of 49F holdings classified source='bd'
    2. Remainder source in {etf_classifier_fallback, manual_override, custodial_override}
    3. Zero classified via keyword-heuristic
    4. ticker_overrides.json deleted from repo
    5. MCP COMPLETE to COO with commit + coverage breakdown + migration audit row counts
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io B_01b.classify_new_securities.py` + `comp-pipescript consumers` on ledger.
    Phase 2: `python -m py_compile`.
    Phase 3: `comp-pipescript deployed`.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="BDPL_CNPRCS.WP-4" status="staged"/>
    <dependency agent="0.4.0_DS_ClientPlatform" task="3-bond-phantom-scoped-exceptions (tactical)" status="staged" description="Tactical fix must land first; WP-6 absorbs it"/>
  </dependencies>

  <next>
    On COMPLETE: unblocks WP-8.
  </next>
</task_order>
