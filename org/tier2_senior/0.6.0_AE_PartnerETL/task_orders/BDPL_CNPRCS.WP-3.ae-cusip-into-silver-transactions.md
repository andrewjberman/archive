<task_order>
  <metadata>
    <id>0.6.0_AE_PartnerETL-2026-04-14-bdpl-cnprcs-wp3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>BDPL_CNPRCS</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md (WP-3 + Q4)</ref>
    <ref type="spec_from_ds">data/black_diamond/specs/silver_transactions_cusip_addition.md (DS to author first)</ref>
  </references>

  <objective>
    Add `cusip` column to silver/transactions via `merge-daily-incremental.py`.
    Re-materialize historical partitions with cusip populated. Append-only (new nullable column).
  </objective>

  <acceptance_criteria>
    1. `merge-daily-incremental.py` preserves cusip column
    2. ≥95% of silver/transactions rows have non-null cusip
    3. Smoke test every gold script consuming silver/transactions — no breakage
    4. MCP COMPLETE to COO with commit + backfill row counts
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io merge-daily-incremental.py` — list consumers.
    Phase 2: `python -m py_compile`.
    Phase 3: Smoke test each consumer listed by comp-pipescript.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="DS writes silver_transactions_cusip_addition.md spec (Q4)" status="pending" description="One-page schema spec precedes AE implementation"/>
  </dependencies>

  <next>
    On COMPLETE: unblocks WP-4 (DS) + feeds WP-9 (DS).
  </next>
</task_order>
