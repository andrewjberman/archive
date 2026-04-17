<task_order>
  <metadata>
    <id>ADVI_ROLLUP.CP-AE1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-17</date>
    <status>complete</status>
    <completed_date>2026-04-17</completed_date>
    <completed_commit>80917a1e</completed_commit>
    <completed_evidence>
      silver/transactions/2026-04-15.parquet re-emitted with cusip column:
      - 5,191 rows (unchanged)
      - 74 cols (was 73, +cusip)
      - cusip non-null: 5,074/5,191 = 97.75% (>95% threshold PASS)
      - unmapped asset_ids: 21 (CITs, stable-value, options, target-date pools — legitimately no CUSIP)
      - null cusip dtype: NoneType (not empty string)
      Scope narrowed by CTO GO (20260417T095246Z) to latest 2026-04-15 forward-shim
      + producer edit for forward runs. Full historical backfill available via
      backfill_cusip_in_transactions.py --all (not run, awaiting DS signal).
      Audit: data/black_diamond/scripts/diagnostics/output/cusip_backfill_audit_2026-04-17.json
    </completed_evidence>
    <project_code>ADVI_ROLLUP</project_code>
    <priority>P0 — unblocks B_01 chronic SAFETY HALT</priority>
    <supersedes>BDPL_CNPRCS.WP-3.ae-cusip-into-silver-transactions.md, BDPL_CNPRCS.WP-3.ae-cusip-backfill-silver-transactions.md</supersedes>
    <guardrail_override>30-day dry-run requirement lifted by Andrew 2026-04-17. Direct production cutover authorized.</guardrail_override>
  </metadata>

  <context>
    B_01.holdings_lots.py fires a SAFETY HALT (>200 accounts) every nightly run because
    _apply_rps_lot_corrections keys on (account_id, asset_name). Name drift on ~261 accounts
    causes false-mismatch force-closes that exceed the 200-account threshold. Fixing the key
    to (account_id, cusip) eliminates the chronic false-match cohort permanently.

    CUSIP must be in silver/transactions before DS can enrich B_01 or modify the RPS match key.
    silver/bd_assets.parquet (3.19M rows) is live via EventBridge (W7 complete, bd-v2.24.1) and
    carries asset_id -> cusip mapping. The join is already designed (WP-3 PRD).
  </context>

  <objective>
    Enrich silver/transactions/{date}.parquet with a `cusip` column in PRODUCTION.
    Join each row on `asset_id` against silver/bd_assets.parquet to populate CUSIP.
    Backfill full historical window. No dry-run — direct production write authorized.

    Wire contract: silver/transactions/{date}.parquet gains column `cusip` (string, nullable
    for cash/synthetic rows). All existing columns preserved. No schema-breaking rename.
    Downstream gold scripts can read `cusip` immediately; null-CUSIP rows do not break them.
  </objective>

  <tasks>
    1. Build a backfill script (or Lambda if schedule is needed) that:
       - Reads silver/bd_assets.parquet from S3 as a lookup table (asset_id -> cusip)
       - For each existing silver/transactions/{date}.parquet partition:
           - Reads the parquet
           - Left-joins on asset_id to add cusip column
           - Writes back to same S3 key (atomic overwrite)
       - Logs null-CUSIP count per partition (expected: cash rows, synthetic lots, pre-dim rows)
    2. Run the backfill on full historical window (match silver/bd_assets.parquet date range).
    3. Commit null-CUSIP audit to data/black_diamond/scripts/diagnostics/output/cusip_backfill_audit_{YYYY-MM-DD}.json.
    4. Verify one sample partition post-backfill: row count parity within 0.1%, cusip column present.
  </tasks>

  <acceptance_criteria>
    1. silver/transactions/{date}.parquet carries `cusip` column for all historical partitions.
    2. >= 95% non-null CUSIP on non-cash rows across the backfilled window.
    3. Row count per partition unchanged (within 0.1% tolerance).
    4. Null-CUSIP audit JSON committed to diagnostics/output/.
    5. comp-pipescript deployed MATCH on any modified Lambda (if Lambda path taken).
    6. MCP COMPLETE to COO with: date range covered, overall CUSIP coverage %, null-audit path, commit hash.
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1 (before write):
      comp-pipescript io silver/transactions — confirm existing column set + downstream consumers.
      comp-blast silver/transactions — confirm blast radius of adding nullable cusip column.
    Phase 2 (before commit):
      python -m py_compile on all modified scripts.
    Phase 3 (after backfill):
      Spot-check: aws s3 cp one partition locally, read with pandas, confirm cusip column + coverage.
  </compiler_tools_mandate>

  <dependencies>
    <dependency task="ADVI_ROLLUP.CP-W4" agent="0.4.0_DS_ClientPlatform" status="active"
      description="silver/bd_assets.parquet blend rule must be verified before backfill join.
      Coordinate: DS will signal COMPLETE on CP-W4 before AE runs the full historical backfill.
      AE may begin Phase 1 compiler pre-flight immediately."/>
  </dependencies>

  <next>
    CP-AE1 COMPLETE unblocks DS ADVI_ROLLUP.CP-DS1 (B_01 CUSIP cutover).
    Signal COO + DS on completion.
  </next>
</task_order>
