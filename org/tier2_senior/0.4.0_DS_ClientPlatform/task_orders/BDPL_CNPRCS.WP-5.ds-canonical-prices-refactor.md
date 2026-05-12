<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-bdpl-cnprcs-wp5</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>complete</status>
    <!-- CLOSED 2026-05-12 by 2.0.0_SA_COO per Andrew directive: bulk-close pending/unaddressed pre-May 2026 TOs. Inherits closure from parent project state or supersession. Re-author as new TO if work still required. -->
    <project_code>BDPL_CNPRCS</project_code>
    <co_owner>0.6.0_AE_PartnerETL (infra + backfill orchestration)</co_owner>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md (WP-5)</ref>
  </references>

  <objective>
    **DRY-RUN MODE (Andrew guardrail 2026-04-14):** Production `build_canonical_prices_v2.py` UNCHANGED.
    Write NEW script `build_canonical_prices_v3_dryrun.py` that outputs to
    `gold/canonical_prices_v3_dryrun/` in parallel. v2 production path untouched.
    30-day parallel running + diff reports before any cutover (cutover EXPLICITLY out-of-scope).

    v3 logic (CUSIP-primary + BD-SuperClass-aware routing):
      Equities -> Yahoo
      Fixed Income -> BD txn price from silver/assets; fallback accreted_cost
      To Be Classified -> latest BD txn price or carry_forward
      Cash & Cash Equivalents -> $1.00 unless BD says otherwise
      DIVERSIFIER / Unclassified -> carry_forward only

    Append-only daily ledger; `price_quality` enum column; deterministic + weekend/holiday roll-forward.
  </objective>

  <acceptance_criteria>
    1. New `build_canonical_prices_v3_dryrun.py` shipped; v2 production script untouched
    2. Output at `gold/canonical_prices_v3_dryrun/{YYYY-MM-DD}.parquet` (v2 output at prod path unchanged)
    3. No asset with BD SuperClass Fixed Income or To Be Classified has `price_quality='yahoo_equity'` in v3 output
    4. Deterministic: same input twice → byte-identical v3 output
    5. Ledger schema includes `price_quality` enum
    6. 30 consecutive calendar days of parallel runs stable (no exceptions, no schema drift)
    7. Diff report committed at `data/black_diamond/scripts/diagnostics/output/dryrun_diff_wp5_{YYYY-MM-DD}.json` (per-day v2-vs-v3 deltas by super_class + price_quality breakdown)
    8. MCP COMPLETE to COO with commit + final-day diff + 30-day stability summary
  </acceptance_criteria>

  <rollback>
    Delete `gold/canonical_prices_v3_dryrun/` prefix + remove `build_canonical_prices_v3_dryrun.py`. No production path modified; v2 continues unchanged. Zero-risk rollback.
  </rollback>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io build_canonical_prices_v2.py` before + after; `comp-pipescript overlap build_canonical_prices_v2 build_canonical_prices_v3_dryrun` (shared S3 reads — silver/prices + silver/assets).
    Phase 2: `python -m py_compile`.
    Phase 3: `comp-pipescript postdeps`; `comp-pipescript deployed build_canonical_prices_v3_dryrun.py`; `comp-validate` after full gold run.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="BDPL_CNPRCS.WP-4" status="staged"/>
  </dependencies>

  <next>
    On COMPLETE: unblocks WP-8.
  </next>
</task_order>
