<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-01-ADHC_HISTRY-002-ds-schwab-injection</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-01</date>
    <status>complete</status><!-- committed 2666dc1f, rotation scripts deployed, AUA $1,582M (0.3% from silver) -->
    <priority>high</priority>
    <type>feature</type>
    <project>ADHC_HISTRY</project>
  </metadata>

  <objective>
    REVISED 2026-04-01 (CTO, per Andrew's direction): Use silver/RPS/ as the Schwab
    authority instead of silver/TRN/ reconstruction.

    RPS = Schwab's daily position snapshot file. It reports quantity_settled per
    (account, security) directly -- no FIFO reconstruction, no sign convention analysis.
    Schwab tells us exactly what each account holds on each date.

    Two deliverables:
    1. LATEST-DATE MATCHING: For the most recent RPS date, compute
       injection_units = rps.quantity_settled - fifo_units per (account, asset).
       This is the core Schwab-authority injection calculation.
    2. TIME SERIES: Iterate over all available RPS dates. For each date build the
       same (account, asset, gap) table. This gives a time series of when positions
       diverge -- identifying exactly when BD's feed fell behind Schwab.

    Focus on the 49Financial account universe (all accounts in the 6,510-account mapping).

    Prerequisite: AE must build silver/RPS/ first (ADHC_HISTRY.003). Wait for AE's
    MCP message confirming silver/RPS/ is ready before running on EC2.
  </objective>

  <references>
    <ref type="investigation_log">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-03-31/adhc_histry_schwab_crossref_and_rotation_capital.md</ref>
    <ref type="ae_session_log">org/tier2_senior/0.6.0_AE_PartnerETL/logs/2026-03-31/adhc_histry_schwab_silver_layer.md</ref>
    <ref type="account_mapping">s3://opal-data-bd/gold/dimensions/schwab_bd_account_mapping.parquet</ref>
    <ref type="schwab_rps_silver">s3://opal-data-schwab/silver/RPS/ (built by AE.003 -- wait for GO from AE)</ref>
    <ref type="schwab_trn_silver">s3://opal-data-schwab/silver/TRN/ (337 partitions, fallback reference)</ref>
    <ref type="rps_converter">data/black_diamond/scripts/bronze/convert_schwab_rps_to_parquet.py (schema reference)</ref>
    <ref type="prior_injection_scripts">data/black_diamond/scripts/diagnostics/schwab_authority_injection_test.py (prior TRN approach -- superseded)</ref>
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
      WAIT for AE's MCP message confirming silver/RPS/ is built (ADHC_HISTRY.003).
      Do not start EC2 runs until AE confirms the data is there. You can write and
      stage the scripts locally while AE runs the converter.
    </requirement>

    <requirement id="2">
      PHASE 1 -- LATEST-DATE MATCHING (diagnostic):
      Write `data/black_diamond/scripts/diagnostics/adhc_histry_006_rps_matching.py`

      The script must:
      a) Load account mapping: `schwab_bd_account_mapping.parquet` (6,510 rows)
      b) Load the latest RPS date partition from `silver/RPS/` -- list the keys,
         take the most recent date=YYYYMMDD partition.
         Key fields from RPS: `account_id` (Schwab), `cusip`, `ticker`,
         `quantity_settled`, `market_value`, `closing_price`.
      c) Map Schwab account_id -> BD account_id via the mapping parquet.
      d) Load BD FIFO positions (existing logic from schwab_authority_injection_test.py
         or load directly from gold cube output if available on EC2).
         Key: compute net open positions per (bd_account_id, asset_name).
      e) Join on (bd_account_id, cusip or asset_name):
         - Build a ticker->asset_name bridge from silver/unrealized/ (same as prior scripts).
         - gap = rps.quantity_settled - fifo_units
      f) Report:
         - Total positions compared, matched, unmatched
         - Positions where gap > 0 (FIFO undercounts): count, total units, total MV
         - Positions where gap &lt; 0 (FIFO overcounts): count, total units, total MV
         - Top 20 undercount positions by MV
         - DIVZ: RPS units vs FIFO units, gap, accounts affected
         - If FIFO+injection were applied: estimated total gold MV vs silver MV
      g) Write results to s3://opal-data-bd/diagnostics/rps_matching_latest.json

      Upload script to S3 at s3://opal-data-bd/code/schwab/adhc_histry_006_rps_matching.py
      and run via SSM on EC2.
    </requirement>

    <requirement id="3">
      PHASE 2 -- TIME SERIES MATCHING:
      Extend the script (or write a separate one) to iterate over ALL available RPS dates.
      For each date:
        rps_date_df = silver/RPS/date={date}/data.parquet
        For each (account, cusip): compute gap vs FIFO-as-of-that-date

      "FIFO as of date" requires loading only transactions up to that date. Use the
      cumulative daily approach from adhc_histry_schwab_crossref scripts (sort by
      trade_date, cumsum up to date). This is the time series.

      Output: one row per (date, bd_account_id, asset_name, rps_units, fifo_units, gap)
      Save as s3://opal-data-bd/diagnostics/rps_timeseries_holdings.parquet

      Key question to answer: on which date did positions first diverge for the top-gap
      accounts? Does the divergence date match the known onboarding event (~2024-04-30)?

      NOTE: This is computationally heavier. Run Phase 1 first and validate before
      running Phase 2.
    </requirement>

    <requirement id="4">
      Commit scripts with author attribution:
      ```
      git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
          -m "diag(ADHC_HISTRY P1): RPS-based position matching (latest + timeseries)"
      ```
      Do NOT push -- AE deploys to EC2 from S3. Upload to S3 yourself after committing.
    </requirement>

    <requirement id="5">
      Report results in session log at:
      org/tier2_senior/0.4.0_DS_ClientPlatform/logs/YYYY-MM-DD/adhc_histry_p1_rps_matching.md

      Required sections:
      - Phase 1: latest-date match summary (total gap MV, DIVZ numbers, under vs over counts)
      - Phase 2 (if completed): time series summary -- when did divergence begin, pattern
      - Recommendation: does the RPS data support full injection? Is the DIVZ target hit?
      - Next step recommendation for Phase 2 (script 02 implementation)

      Send results to CTO (1.0.0_SA_CTO) and COO (2.0.0_SA_COO) via MCP when complete.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">adhc_histry_006_rps_matching.py committed and uploaded to S3.</criterion>
    <criterion id="2">Phase 1 diagnostic output at s3://opal-data-bd/diagnostics/rps_matching_latest.json produced by EC2 run.</criterion>
    <criterion id="3">Phase 2 time series at s3://opal-data-bd/diagnostics/rps_timeseries_holdings.parquet produced.</criterion>
    <criterion id="4">Session log contains gap summary with MV estimates, DIVZ numbers, and divergence date.</criterion>
    <criterion id="5">CTO and COO notified via MCP with results summary.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Use silver/RPS/ quantity_settled as the Schwab authority -- do NOT use TRN-reconstructed positions for this task.</constraint>
    <constraint>Use CUSIP as the primary join key between Schwab RPS and BD asset_name (more reliable than ticker).</constraint>
    <constraint>Build ticker->asset_name bridge from silver/unrealized/ (same as prior scripts -- it has both ticker and CUSIP).</constraint>
    <constraint>Do NOT deploy RC3/RC4 changes (held per Andrew's direction from 2026-03-31 session).</constraint>
    <constraint>Do NOT remove RC1 (name aliasing). It is correct, deployed, and must stay.</constraint>
    <constraint>Do NOT run a full gold layer rebuild until Phase 1 diagnostic is reviewed.</constraint>
    <constraint>Do NOT inject negative gaps (FIFO > Schwab). Flag them, do not inject.</constraint>
    <constraint>Follow EC2_CODE_DEPLOYMENT_STANDARD.md: write locally -> upload to S3 -> EC2 pulls and executes.</constraint>
    <constraint>No emojis in code per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.6.0_AE_PartnerETL" task="ADHC_HISTRY.003" status="pending">
      AE must build silver/RPS/ before Phase 1 can run on EC2. Wait for AE's MCP message.
      You can write and stage scripts locally while AE is running the converter.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="code-commit">data/black_diamond/scripts/diagnostics/adhc_histry_005_schwab_authority_calc.py</deliverable>
    <deliverable type="s3-artifact">s3://opal-data-bd/diagnostics/schwab_authority_calc.csv (diagnostic results)</deliverable>
    <deliverable type="document">Session log with injection gap summary and Phase 2 recommendation</deliverable>
  </deliverables>
</task_order>
