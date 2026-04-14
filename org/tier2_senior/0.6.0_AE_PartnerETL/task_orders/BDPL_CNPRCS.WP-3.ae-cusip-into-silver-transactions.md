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
    **DRY-RUN MODE (Andrew guardrail 2026-04-14):** Production `silver/transactions/` UNTOUCHED.
    Build parallel `silver/transactions_v2_dryrun/` with cusip column populated. Original
    merge-daily-incremental.py UNCHANGED. 30-day parallel running + diff reports before any cutover
    (cutover is EXPLICITLY out-of-scope for this project).
  </objective>

  <acceptance_criteria>
    1. New dry-run materializer writes to `silver/transactions_v2_dryrun/` (production path untouched)
    2. ≥95% of `silver/transactions_v2_dryrun/` rows have non-null cusip
    3. Row-count parity vs production within 0.1% (per date partition)
    4. Diff report committed at `data/black_diamond/scripts/diagnostics/output/dryrun_diff_wp3_{YYYY-MM-DD}.json` (row counts, cusip-coverage, per-partition deltas)
    5. Smoke test: every gold script consuming silver/transactions still reads production path cleanly (no breakage)
    6. MCP COMPLETE to COO with commit + diff report path + parity numbers
  </acceptance_criteria>

  <rollback>
    Delete `silver/transactions_v2_dryrun/` prefix. No production path was modified; no state to restore. Merge-daily-incremental.py unchanged. Zero-risk rollback.
  </rollback>

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
