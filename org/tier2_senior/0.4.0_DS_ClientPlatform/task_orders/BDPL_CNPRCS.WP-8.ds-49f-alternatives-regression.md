<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-bdpl-cnprcs-wp8</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>BDPL_CNPRCS</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md (WP-8)</ref>
  </references>

  <objective>
    Rebuild 49F monthly Alternatives time series from 2024-01 through 2026-04 using the
    new classification + canonical prices. Document the delta vs pre-refactor series.
  </objective>

  <acceptance_criteria>
    1. No month-to-month swing > $10M unexplained by a real flow/transaction
    2. 04-07 → 04-10 swing ($33M) and 2025-06-10 single-day drop ($18M) disappear or are structurally explained
    3. Report committed to data/black_diamond/diagnostics/49f_alternatives_regression_2026-04-14.md
    4. MCP COMPLETE to COO with commit + final-delta summary
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: Read prior-series source data.
    Phase 3: `comp-validate` on regression report against gold_validate_config.yaml thresholds.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="BDPL_CNPRCS.WP-5" status="staged"/>
    <dependency agent="0.4.0_DS_ClientPlatform" task="BDPL_CNPRCS.WP-6" status="staged"/>
  </dependencies>
</task_order>
