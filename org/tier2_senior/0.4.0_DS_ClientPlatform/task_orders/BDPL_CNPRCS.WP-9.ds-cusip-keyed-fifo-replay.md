<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-bdpl-cnprcs-wp9</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>BDPL_CNPRCS</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md (WP-9 + Q8)</ref>
  </references>

  <objective>
    CUSIP-keyed FIFO replay + phantom reclassification.

    1. Rewrite compute_fifo() in adhc_histry_005_phantom_schwab.py AND adhc_histry_001/002/003/004.py
       AND diag_phantom_fifo_replay.py: key on (account_id, cusip) instead of (account_id, asset_name).
    2. Consume asset_dim Action granularity — distinguish ACAT Out, EF Transfer Out, JNL-SHORT,
       FTP-DEBIT, plain Transfer Out as reporting enums (not blanket SELL).
    3. Re-run phantom hunt post-WP-3/4. Categorize the 10,832 flagged phantoms ($177M) into:
       - rotation_explained — matched to non-cash rotation event in asset_dim. Silent close
         in FIFO ledger with audit-tag row (resolution='rotation_explained', matched_event, matched_cusip) per Q8.
       - genuine_data_issue — no matching event. Feed into monthly BD-feed-quality report
         (docs/data_quality/bd_feed_quality_{YYYY-MM}.md). Material threshold: >$1M or >100 count
         in a single month triggers out-of-band BD-account-manager escalation.
    4. Output: data/black_diamond/scripts/diagnostics/output/phantom_resolution_{YYYY-MM-DD}.json
       with per-phantom cause tags.
    5. Deprecate NAME_ALIASES dict in adhc_histry_005 AND the "silver allocations phantom gate"
       in 02b_build_canonical_holdings.py Step 5 — both were patches for the
       (account_id, asset_name) fragility that CUSIP resolves structurally.
  </objective>

  <acceptance_criteria>
    1. Residual unexplained phantom MV < $10M (vs current $177M)
    2. NAME_ALIASES and silver-allocations phantom gate either removed OR session log documents why they stayed
    3. First monthly bd_feed_quality report published
    4. MCP COMPLETE to COO with commit + residual MV + rotation/genuine split
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io` on adhc_histry_005 + siblings + diag_phantom_fifo_replay.
    Phase 2: `python -m py_compile` on all edited scripts.
    Phase 3: `comp-pipescript deployed`.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.6.0_AE_PartnerETL" task="BDPL_CNPRCS.WP-3" status="staged"/>
    <dependency agent="0.4.0_DS_ClientPlatform" task="BDPL_CNPRCS.WP-4" status="staged"/>
  </dependencies>

  <next>
    Parallel with WP-5 and WP-6. Independent of WP-8.
  </next>
</task_order>
