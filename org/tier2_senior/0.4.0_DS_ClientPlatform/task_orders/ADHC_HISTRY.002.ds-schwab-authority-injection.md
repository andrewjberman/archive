<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-01-ADHC_HISTRY-002-ds-schwab-injection</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-01</date>
    <status>staged</status>
    <priority>high</priority>
    <type>feature</type>
    <project>ADHC_HISTRY</project>
  </metadata>

  <objective>
    Implement Schwab-authority injection in scripts 02 and 03. Replace the current
    residual-based synthetic buy injection with direct Schwab unit targets derived
    from the 6,510-account mapping breakthrough (P0 investigation).

    The core insight: BD's transaction feed is missing sell transactions (50,887
    positions / $513M). The current rotation-capital injection uses residual back-solve
    to estimate what was missing. Schwab TRN has the exact unit counts. Use them.

    Formula: injection_units = schwab_net_units - fifo_units (for accounts in the mapping).
    This eliminates estimation error and makes the injection data-driven.
  </objective>

  <references>
    <ref type="investigation_log">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-03-31/adhc_histry_schwab_crossref_and_rotation_capital.md</ref>
    <ref type="account_mapping">s3://opal-data-bd/gold/dimensions/schwab_bd_account_mapping.parquet</ref>
    <ref type="schwab_silver">s3://opal-data-schwab/silver/ (2.73M rows, 554 daily files, 2024-01-16 to 2026-03-30)</ref>
    <ref type="script_02">data/black_diamond/scripts/gold/02_build_positions_cube.py</ref>
    <ref type="script_03">data/black_diamond/scripts/gold/03_build_holdings_lots.py</ref>
  </references>

  <pre_verified_facts>
    COO verified from DS session log (2026-03-31):

    1. Account mapping is at `s3://opal-data-bd/gold/dimensions/schwab_bd_account_mapping.parquet`
       with 6,417 direct matches (zero-padded account_number) + 93 fingerprint matches = 6,510 total.

    2. Schwab TRN data in silver has exact unit counts per (account_id, ticker, trade_date).
       Schwab `account_id` = zero-padded BD `account_number` (e.g., BD 85238265 -> Schwab 0085238265).

    3. DIVZ validation on mapped accounts: accounts with BD=0, Schwab>0 are the injection targets.
       Schwab sees 9,789 DIVZ accounts; BD unrealized only sees 5,117. The delta is the gap.

    4. RC1 (name aliasing in script 02) is DEPLOYED and working. DO NOT touch it.
       RC2, RC3, RC4 are HELD per Andrew's direction. This task supersedes RC2-RC4.

    5. Rotation capital is the correct model: synthetic sells free capital, that capital funds
       synthetic buys for the missing positions. Total gold MV stays flat.

    6. Do NOT run a full gold layer rebuild until the Schwab-authority injection logic is
       validated as a diagnostic first. Run diagnostic, report results to COO, wait for GO.
  </pre_verified_facts>

  <requirements>

    <requirement id="1">
      PHASE 1 (DIAGNOSTIC): Write a diagnostic script at
      `data/black_diamond/scripts/diagnostics/adhc_histry_005_schwab_authority_calc.py`

      The diagnostic must:
      a) Load `schwab_bd_account_mapping.parquet` from S3 (6,510 rows with BD and Schwab account IDs)
      b) Aggregate Schwab TRN silver by (schwab_account_id, cusip) -> net_schwab_units
         (sum quantity; use signed convention matching BD: buy=+, sell=-)
         Filter to the 6,510 mapped accounts only.
      c) Load the current gold cube positions (script 02 output or silver positions) for
         the same accounts and tickers -> fifo_units per (bd_account_id, cusip)
      d) Compute: injection_units = schwab_net_units - fifo_units
         Positive injection_units = BD under-counts (need to inject more units)
         Negative injection_units = BD over-counts (would remove units -- flag these, do NOT inject)
      e) Report summary statistics:
         - Total injection needed (sum of positive injection_units)
         - Total over-count (sum of abs(negative injection_units)) -- these are suspect
         - Top 20 accounts by injection gap
         - DIVZ injection total and account count
         - Aggregate MV at current prices
      f) Write results to S3 (diagnostic output path: s3://opal-data-bd/diagnostics/schwab_authority_calc.csv)
         and print summary to stdout.

      Upload this script to S3 per EC2_CODE_DEPLOYMENT_STANDARD.md before running on EC2.
      Run via SSM as the diagnostic first. Do NOT modify scripts 02/03 until diagnostic
      results are reviewed and approved.
    </requirement>

    <requirement id="2">
      PHASE 1 (DIAGNOSTIC): Report the diagnostic results in your session log with:
      - Total injection gap (units and estimated MV at spot prices)
      - Number of accounts affected
      - DIVZ-specific numbers (since DIVZ is the primary target from P0 analysis)
      - Any accounts with large negative injection_units (BD sees more than Schwab -- these need investigation)
      - Percentage of the $341M confirmed-open undershoot explained by Schwab injection targets

      Do NOT proceed to Phase 2 until COO reviews these numbers and sends a GO.
    </requirement>

    <requirement id="3">
      PHASE 2 (IMPLEMENTATION -- wait for GO after Phase 1):
      Modify script 02 (`_load_synthetic_buy_events` or equivalent) to use Schwab unit
      targets instead of residual back-solve for accounts in the 6,510-account mapping.

      Implementation approach:
      a) Load schwab_bd_account_mapping.parquet at script startup (or lazily before injection)
      b) For each (bd_account_id, cusip) in the mapping with positive injection_units:
         - If bd_account_id has no FIFO history for this ticker: inject a synthetic buy
           for injection_units at the position's weighted-average Schwab price
         - If bd_account_id has FIFO history: compare and inject the delta
      c) Accounts NOT in the 6,510-account mapping fall back to the existing rotation-capital
         residual approach (do not regress non-mapped accounts)
      d) Continue to exclude CASH from injection targets
      e) Continue to apply sell injection (RC1 sell logic) before the buy injection
    </requirement>

    <requirement id="4">
      PHASE 2: Also modify script 03 if it contains a separate injection step that
      would conflict with script 02's changes. Read script 03 completely before touching it.
      If injection logic is only in script 02, make no change to script 03.
    </requirement>

    <requirement id="5">
      Commit diagnostic script with author attribution:
      ```
      git commit --author="0.4.0_DS_ClientPlatform <0.4.0_DS_ClientPlatform@opal.agent>" \
          -m "diag(ADHC_HISTRY P1): schwab-authority injection calculator (Phase 1 diagnostic)"
      ```
      Phase 2 implementation commits separately after GO.
      Do NOT push -- AE deploys to EC2 from S3.
    </requirement>

    <requirement id="6">
      Write a session log at:
      org/tier2_senior/0.4.0_DS_ClientPlatform/logs/YYYY-MM-DD/adhc_histry_p1_schwab_injection.md

      Include the diagnostic results table and a clear recommendation (proceed with Phase 2 
      or investigation needed).
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">Diagnostic script at data/black_diamond/scripts/diagnostics/adhc_histry_005_schwab_authority_calc.py committed and uploaded to S3.</criterion>
    <criterion id="2">Diagnostic output at s3://opal-data-bd/diagnostics/schwab_authority_calc.csv produced by EC2 run.</criterion>
    <criterion id="3">Session log contains injection gap summary with MV estimates and DIVZ-specific numbers.</criterion>
    <criterion id="4">(Phase 2, after GO) script 02 injection logic uses Schwab unit targets for mapped accounts.</criterion>
    <criterion id="5">(Phase 2, after GO) Scripts committed and uploaded to S3 for AE deploy.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT deploy RC3/RC4 changes (held per Andrew's direction from 2026-03-31 session).</constraint>
    <constraint>Do NOT remove RC1 (name aliasing). It is correct, deployed, and must stay.</constraint>
    <constraint>Do NOT run a full gold layer rebuild until Phase 1 diagnostic is reviewed by COO and Andrew.</constraint>
    <constraint>Do NOT inject negative injection_units (accounts where BD > Schwab). Flag them, investigate separately.</constraint>
    <constraint>Schwab TRN data may have older ticker symbols (e.g., SPLG not SPYM). Verify ticker matching against the mapping. Use CUSIP as the authoritative join key, not ticker.</constraint>
    <constraint>Follow EC2_CODE_DEPLOYMENT_STANDARD.md: write locally -> upload to S3 -> EC2 pulls from S3 -> execute. Never run scripts locally against production data.</constraint>
    <constraint>No emojis in code per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.6.0_AE_PartnerETL" task="schwab_trn_silver_ready" status="complete">
      Schwab TRN silver is already in S3 (confirmed by DS 2026-03-31 log: 2.73M rows, 
      554 daily files through 2026-03-30). AE needs to set up automated daily ingestion
      separately (this is a future TO, not a blocker for Phase 1 diagnostic).
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="code-commit">data/black_diamond/scripts/diagnostics/adhc_histry_005_schwab_authority_calc.py</deliverable>
    <deliverable type="s3-artifact">s3://opal-data-bd/diagnostics/schwab_authority_calc.csv (diagnostic results)</deliverable>
    <deliverable type="document">Session log with injection gap summary and Phase 2 recommendation</deliverable>
  </deliverables>
</task_order>
