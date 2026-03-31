# Task Order: ADVI_GLDRST.002 + ADVI_TICKID — Combined Gold Rerun

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-combined-gold-rerun</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
    <project_code>ADVI_GLDRST</project_code>
    <also_satisfies>ADVI_TICKID P2 execution sequence</also_satisfies>
  </metadata>

  <objective>
    Combined end-to-end run that satisfies BOTH ADVI_GLDRST.002 (canonical exclusion
    unification, pre-computed views, ghost account fix) AND ADVI_TICKID P2 (enriched
    ticker resolution, yahoo sweep, silver AUA override). One gold rerun covers both.

    Run the TICKID silver enrichment sequence first (steps 1-6), then a single FULL
    gold layer run (step 7) that picks up ALL committed changes from both projects.
    Validate both projects' acceptance criteria. Send DS the 05c gap result for .008 gate.

    This task order is AUTONOMOUS. Execute end-to-end without waiting for human input.
  </objective>

  <context>
    Commits already on origin/CLOUD that this run absorbs:

    ADVI_GLDRST:
    - 9bca5ff6: mix_timeseries.json alias in 06b + ghost exclusion in 06
    - 38faa34f: lib/exclusions.py creation + dedup scripts 05+06
    - df5e8004: Ghost exclusion added to script 05b
    - ae3403f5: Ghost exclusion added to 06b+12, shared insurance AP gate
    - 16c3139e: DFAC classified as equity / US Small Cap / active
    - 8d04e167: Pre-compute L3 relationship views + composition artifacts
    - 54d1f988: return ghost_account_ids from load_static_tables in 06b
    - 9bb2d7af: guard ZeroDivisionError in script 12
    - 101bd185: per-process S3 client in 05b ProcessPoolExecutor workers
    - 6266040f: ProcessPoolExecutor for CPU-bound partition processing

    ADVI_TICKID:
    - 48932e8a: resolve_tickers.py (TICKID.001)
    - 93ce0f69: holdings_lots ticker enrichment join (TICKID.002)
    - 35544c47: DynamoDB name alias backfill (TICKID.003)
    - 413094bd: detect_new_securities enhancement (TICKID.004)
    - 76c26f33: feedback bridge + method 5 in resolve_tickers.py (TICKID.005)
    - da272777: sweep-unlisted + diagnose-stale modes (TICKID.006)
    - 0253186a: silver AUA override in scripts 05 + 05b (TICKID.007)
  </context>

  <requirements>
    <!-- ============================================================ -->
    <!-- PHASE A: Upload scripts to S3 (CRITICAL: committed state only) -->
    <!-- ============================================================ -->

    <requirement id="1">
      CRITICAL: The working tree has UNCOMMITTED GLDRST P3 prep changes
      (lib/config.py import migration) across 17+ gold/silver scripts. These
      changes will BREAK the gold run because lib/config.py is untracked and
      won't exist on EC2.

      Before uploading ANY scripts to S3:
        git stash -- data/black_diamond/scripts/

      This reverts the working tree to the committed state. Upload from committed
      state. After upload is complete:
        git stash pop

      Verify the stash contains only `from lib.config import S3_BUCKET` type
      changes. If you see substantive logic changes in the stash, STOP and
      message COO.
    </requirement>

    <requirement id="2">
      Upload COMMITTED silver scripts to S3:
        aws s3 sync data/black_diamond/scripts/silver/ s3://opal-data-bd/code/silver/ --delete

      Upload COMMITTED gold scripts to S3:
        aws s3 sync data/black_diamond/scripts/gold/ s3://opal-data-bd/code/gold/ --delete

      Verify key files are present after upload:
        aws s3 ls s3://opal-data-bd/code/gold/lib/exclusions.py
        aws s3 ls s3://opal-data-bd/code/gold/lib/etf_classifier.py
        aws s3 ls s3://opal-data-bd/code/silver/resolve_tickers.py
        aws s3 ls s3://opal-data-bd/code/silver/fetch_historical_prices_yfinance.py
    </requirement>

    <!-- ============================================================ -->
    <!-- PHASE B: TICKID Silver Enrichment Sequence (on EC2)          -->
    <!-- ============================================================ -->

    <requirement id="3">
      Run the TICKID silver enrichment sequence on EC2 (bd-gold-layer-runner
      instance, c5.4xlarge or larger). Execute via SSM in this exact order:

      Step B1: resolve_tickers.py --upload
        Populates ticker_lookup.json and yahoo_safe_tickers.txt.
        Bridges $257M ticker gap into pricing pipeline.

      Step B2: fetch_historical_prices_yfinance.py --sweep-unlisted
        Validates and adds 493 unlisted tickers. $11.7M coverage.

      Step B3: fetch_historical_prices_yfinance.py --diagnose-stale
        Refreshes 38 stale tickers.

      Step B4: fetch_historical_prices_yfinance.py --backfill
        Backfills history for newly safe tickers.

      Step B5: build_canonical_prices_v2.py
        Rebuilds canonical prices with enriched T2 (ticker resolution data).

      These steps must complete successfully before Phase C. If any step fails,
      capture stderr and message COO. Do NOT proceed to gold if silver fails.
    </requirement>

    <!-- ============================================================ -->
    <!-- PHASE C: Full Gold Layer Run                                  -->
    <!-- ============================================================ -->

    <requirement id="4">
      Execute FULL gold layer run (not incremental):
        ./run_gold_layer.sh full

      Use c5.4xlarge or c6i.16xlarge. Full run is required because:
      - Script 05b needs ALL positions_cube partitions reprocessed (ghost exclusion + AUA override)
      - Script 06b needs ALL per-advisor mix.json + mix_timeseries.json aliases regenerated
      - Script 12 needs ALL composition artifacts with ghost + insurance AP gate
      - Ticker enrichment (.001-.007) changes propagate through scripts 03->05->06b->12

      Tee output to log and upload to S3:
        tee /var/log/gold-full-run.log
        aws s3 cp /var/log/gold-full-run.log \
          s3://opal-data-bd/logs/gold-layer/gold_full_combined_gldrst_tickid_$(date +%Y%m%d_%H%M%S).log

      Timeout: 7200s (2 hours). Poll via SSM get-command-invocation. Heartbeat
      every 2nd poll iteration.
    </requirement>

    <!-- ============================================================ -->
    <!-- PHASE D: Post-Run Validation (BOTH projects)                  -->
    <!-- ============================================================ -->

    <requirement id="5">
      GLDRST validation (all must pass):

      (a) Cross-validate 05 vs 05b: built-in cross_validate_vs_client_performance()
          should pass within 0.1% tolerance.

      (b) Verify mix_timeseries.json aliases:
          aws s3 ls s3://opal-data-bd/gold/advisors/ --recursive | grep mix_timeseries.json
          Expected: 20 files (one per advisor).

      (c) Spot-check one advisor:
          Compare book.json summary.total_aua vs architect_leaderboard.json.
          Delta should be less than 0.01%.

      (d) Verify DFAC classification:
          Download any composition.json. Confirm DFAC appears under "equity" asset class.
    </requirement>

    <requirement id="6">
      TICKID validation:

      (a) Download script 05c output (05c_validate_aua_vs_silver.py log or S3 artifact).
          Record the aggregate AUA divergence percentage.

      (b) Check ticker resolution coverage:
          Verify ticker_lookup.json on S3 has entries for the 493 unlisted tickers.

      (c) Record the 05c gap percentage — this is the .008 gate value.
    </requirement>

    <!-- ============================================================ -->
    <!-- PHASE E: Signal DS for .008 Gate                              -->
    <!-- ============================================================ -->

    <requirement id="7">
      After validation, send message to DS with 05c results:

      send_message(
        from="0.6.0_AE_PartnerETL",
        to="0.4.0_DS_ClientPlatform",
        subject="TICKID .008 gate: 05c gap result from combined gold run",
        body="Gold run complete. 05c aggregate AUA divergence: {X.X%}.
              If below 0.5%: mark .008 'not needed'.
              If above 0.5%: .008 bond classifier is needed."
      )

      Also send completion message to COO:

      send_message(
        from="0.6.0_AE_PartnerETL",
        to="2.0.0_SA_COO",
        subject="GLDRST.002 + TICKID combined gold run COMPLETE",
        body="All phases complete. GLDRST validation: {pass/fail details}.
              TICKID 05c gap: {X.X%}. DS notified for .008 gate."
      )
    </requirement>

    <requirement id="8">
      Write a session log at:
        org/tier2_senior/0.6.0_AE_PartnerETL/logs/{date}/
          advi_combined_gold_rerun_session.md

      Include: instance type, silver sequence duration, gold run duration,
      all validation results, 05c gap value, messages sent.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Silver enrichment sequence (B1-B5) completes without errors</criterion>
    <criterion id="2">Full gold layer run completes without errors</criterion>
    <criterion id="3">05b cross_validate_vs_client_performance passes within 0.1%</criterion>
    <criterion id="4">20 mix_timeseries.json alias files exist on S3</criterion>
    <criterion id="5">book.json and architect_leaderboard.json AUA match within 0.01%</criterion>
    <criterion id="6">05c gap value recorded and sent to DS</criterion>
    <criterion id="7">COO notified of completion</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>CRITICAL: git stash uncommitted changes before uploading to S3. Working tree has GLDRST P3 prep (lib/config.py imports) that will crash scripts. Upload ONLY committed state.</constraint>
    <constraint>Use FULL mode (not incremental) -- ghost exclusion + ticker enrichment must reprocess all historical partitions</constraint>
    <constraint>Do NOT modify any code. All changes are already committed on CLOUD.</constraint>
    <constraint>Prefer c5.4xlarge or c6i.16xlarge for full run (r6i.xlarge is too slow)</constraint>
    <constraint>Do NOT wait for human input at any phase. Execute end-to-end autonomously.</constraint>
    <constraint>If any phase fails, message COO with error details. Do NOT retry without diagnosis.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_GLDRST.001" status="complete">
      Pre-computed views + canonical methodology committed
    </dependency>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_TICKID.005" status="complete">
      Feedback bridge + method 5 (76c26f33)
    </dependency>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_TICKID.006" status="complete">
      Sweep-unlisted + diagnose-stale (da272777)
    </dependency>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_TICKID.007" status="complete">
      Silver AUA override (0253186a)
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="artifact">Regenerated silver pricing artifacts (canonical_prices, ticker_lookup)</deliverable>
    <deliverable type="artifact">Regenerated gold parquets + portal JSON artifacts on S3</deliverable>
    <deliverable type="message">05c gap result sent to DS for .008 gate</deliverable>
    <deliverable type="message">Completion notification to COO</deliverable>
    <deliverable type="document">Session log with all validation results</deliverable>
  </deliverables>
</task_order>
