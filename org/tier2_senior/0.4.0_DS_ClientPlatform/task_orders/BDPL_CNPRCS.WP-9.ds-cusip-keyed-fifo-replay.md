<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-bdpl-cnprcs-wp9</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>complete</status>
    <!-- CLOSED 2026-05-12 by 2.0.0_SA_COO per Andrew directive: bulk-close pending/unaddressed pre-May 2026 TOs. Inherits closure from parent project state or supersession. Re-author as new TO if work still required. -->
    <project_code>BDPL_CNPRCS</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md (WP-9 + Q8)</ref>
  </references>

  <objective>
    **DRY-RUN MODE (Andrew guardrail 2026-04-14):** Production UNCHANGED. Specifically:
      - adhc_histry_001/002/003/004/005_*.py UNCHANGED (existing compute_fifo stays live)
      - NAME_ALIASES dict LEFT IN PLACE
      - "silver allocations phantom gate" in 02b_build_canonical_holdings.py Step 5 LEFT IN PLACE
      - diag_phantom_fifo_replay.py UNCHANGED

    Build NEW `diag_phantom_fifo_cusip_dryrun.py` that applies CUSIP-keyed FIFO (account_id, cusip)
    as a comparison report only. 30-day parallel output + diff vs production phantom-detection
    before any cutover. Cutover (FIFO rewrite + deprecations) is EXPLICITLY out-of-scope.

    Dry-run report:
    1. Apply CUSIP-keyed FIFO on silver/transactions (read-only) + silver/bd_assets.
    2. Consume asset_dim Action granularity — distinguish ACAT Out, EF Transfer Out, JNL-SHORT,
       FTP-DEBIT, plain Transfer Out as reporting enums.
    3. Categorize the 10,832 flagged phantoms ($177M) into:
       - rotation_explained — matched to non-cash rotation event in asset_dim (report only)
       - genuine_data_issue — no matching event (feed into monthly BD-feed-quality report;
         >$1M or >100 count in a month triggers BD-account-manager escalation)
    4. Output: `data/black_diamond/scripts/diagnostics/output/phantom_resolution_dryrun_{YYYY-MM-DD}.json`
       with per-phantom cause tags.
  </objective>

  <acceptance_criteria>
    1. New `diag_phantom_fifo_cusip_dryrun.py` script shipped; no production scripts modified
    2. Dry-run projects residual unexplained phantom MV < $10M (vs current $177M production)
    3. NAME_ALIASES + silver-allocations phantom gate + adhc_histry_* all confirmed unchanged post-deploy
    4. 30 consecutive calendar days of stable dry-run output
    5. Diff report committed at `data/black_diamond/scripts/diagnostics/output/dryrun_diff_wp9_{YYYY-MM-DD}.json` (production-vs-dryrun rotation/genuine counts + residual MV deltas)
    6. First monthly bd_feed_quality report published (advisory; does not affect production)
    7. MCP COMPLETE to COO with commit + dry-run residual MV + rotation/genuine split + 30-day stability summary
  </acceptance_criteria>

  <rollback>
    Delete `diag_phantom_fifo_cusip_dryrun.py` + associated dryrun outputs. No production scripts, phantom gates, or FIFO logic were modified. Zero-risk rollback.
  </rollback>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io` on adhc_histry_005 + siblings + diag_phantom_fifo_replay; `comp-blast adhc_histry_005` (deprecation-candidate blast-check — confirm what depends on it before touching).
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
