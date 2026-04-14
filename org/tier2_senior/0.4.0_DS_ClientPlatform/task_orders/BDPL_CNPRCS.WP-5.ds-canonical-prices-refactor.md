<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-bdpl-cnprcs-wp5</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>BDPL_CNPRCS</project_code>
    <co_owner>0.6.0_AE_PartnerETL (infra + backfill orchestration)</co_owner>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md (WP-5)</ref>
  </references>

  <objective>
    Refactor build_canonical_prices_v2.py to CUSIP-primary + BD-SuperClass-aware routing.
    Never-Yahoo for Fixed Income and To Be Classified. Append-only daily ledger at
    `gold/canonical_prices/{YYYY-MM-DD}.parquet`. Deterministic + weekend/holiday roll-forward.
    Add `price_quality` enum column.

    Routing rules:
      Equities -> Yahoo
      Fixed Income -> BD txn price from silver/assets; fallback accreted_cost
      To Be Classified -> latest BD txn price or carry_forward
      Cash & Cash Equivalents -> $1.00 unless BD says otherwise
      DIVERSIFIER / Unclassified -> carry_forward only

    Dark-launch pattern: write new ledger alongside old output; diff; flip once clean.
    AE orchestrates backfill after DS logic ships.
  </objective>

  <acceptance_criteria>
    1. No asset with BD SuperClass Fixed Income or To Be Classified has price_quality='yahoo_equity'
    2. WP-7 phantom-scan diagnostic returns 0 hits post-deploy
    3. Deterministic: same input twice = byte-identical output
    4. Ledger schema includes price_quality enum
    5. MCP COMPLETE to COO with commit + dark-launch diff summary + final-flip confirmation
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io build_canonical_prices_v2.py` before + after.
    Phase 2: `python -m py_compile`.
    Phase 3: `comp-pipescript postdeps`; `comp-validate` after full gold run.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="BDPL_CNPRCS.WP-4" status="staged"/>
  </dependencies>

  <next>
    On COMPLETE: unblocks WP-8.
  </next>
</task_order>
