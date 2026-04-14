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
    **DRY-RUN MODE (Andrew guardrail 2026-04-14):** Production UNTOUCHED. Specifically:
      - B_01b.classify_new_securities.py UNCHANGED (keyword heuristics remain live)
      - ETFClassifier DDB UNCHANGED (NOT demoted)
      - ticker_overrides.json UNCHANGED (NOT deleted, NOT migrated)
      - scoped_price_exceptions.json UNCHANGED (stays as durable tactical guard)
      - lib/mix_views.py MIX_ASSET_CLASSES UNCHANGED

    Build parallel `silver/bd_asset_classifications_dryrun/{YYYY-MM-DD}.parquet` (immutable daily)
    implementing the target design for comparison only. 30-day parallel running + diff reports
    before any cutover. Migrate-and-delete is EXPLICITLY out-of-scope for this project.

    Dry-run ledger content:
      - Primary classification = BD SuperClass via Q1 mapping:
          Equities -> equity; Fixed Income -> fixed_income; Cash&CE -> cash;
          DIVERSIFIER -> alternatives; To Be Classified -> alternatives;
          Unclassified -> other.
      - ETFClassifier-fallback rows for assets not in silver/bd_assets (READ only, no DDB changes)
      - Simulated manual_override rows from ticker_overrides.json (READ only, source JSON unchanged)
      - Simulated custodial_override rows from scoped_price_exceptions.json (READ only)
  </objective>

  <acceptance_criteria>
    1. `silver/bd_asset_classifications_dryrun/` ledger materialized daily
    2. ≥98% of 49F holdings classified source='bd' in the dry-run ledger
    3. Remainder source in {etf_classifier_fallback, manual_override, custodial_override} in dry-run
    4. Zero keyword-heuristic classifications in dry-run (production B_01b still runs, this measures what the target design would produce)
    5. ticker_overrides.json + scoped_price_exceptions.json + ETFClassifier DDB + B_01b.py all confirmed unchanged post-deploy
    6. 30 consecutive calendar days of parallel runs stable
    7. Diff report committed at `data/black_diamond/scripts/diagnostics/output/dryrun_diff_wp6_{YYYY-MM-DD}.json` (per-asset classification deltas dryrun-vs-production)
    8. MCP COMPLETE to COO with commit + coverage breakdown + 30-day stability summary
  </acceptance_criteria>

  <rollback>
    Delete `silver/bd_asset_classifications_dryrun/` prefix. No production scripts, DDB entries, or JSON files were modified. ticker_overrides.json, scoped_price_exceptions.json, ETFClassifier, B_01b all remain in original state. Zero-risk rollback.
  </rollback>

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
