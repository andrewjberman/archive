<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-24-prices-003-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-24</date>
    <status>complete</status>
    <project_code>ADVI_PRICES</project_code>
  </metadata>

  <objective>
    Deploy the yahoo-priority pricing hierarchy change (DS commit 61b34f77) and
    execute 6 specific steps to propagate corrected prices through the full stack.

    Final hierarchy: scoped_override (-2) > yahoo_finance (-1) > transaction_observed (0) > carry_forward (3)

    DS also added 8 ticker corrections and a _TICKER_CORRECTIONS map. These need
    to be propagated to S3 artifacts and the EC2 scheduler.
  </objective>

  <scope>
    <files>
      <file action="upload-to-s3">data/black_diamond/scripts/silver/bd_price_update.py</file>
      <file action="upload-to-s3">data/black_diamond/scripts/silver/build_canonical_prices_v2.py</file>
      <file action="run-on-ec2">bd_price_update.py</file>
      <file action="run-on-ec2">run_gold_layer.sh full</file>
      <file action="run-on-ec2">recon_lots_vs_allocations.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="0">
      PREREQUISITE — Audit and fix historical_prices.parquet BEFORE canonical rebuild.

      COO audited all ~145 T1 assets that would switch to yahoo under the new
      hierarchy. Three categories of problems found:

      CATEGORY A — Feb 12 scheduler stoppage (4 tickers):
        IDVZ, XLE, VUSB, PFOE — all stopped at exactly 2026-02-12.
        These are in the scheduler but stopped fetching. Investigate root cause
        (scheduler config change? API failure? ticker delist?). Refresh all 4.

      CATEGORY B — Stale 14-36 days (17 tickers, Feb 24 to Mar 10):
        VXUS (3 share classes map here), QUAL, SLV, V, URA, OUSA, TECB,
        VNLA, SCHB, VGSH, VLUE, MTUM, QQQ, NVDA, REET.
        These are MAJOR liquid names. Investigate why they dropped from the
        daily scheduler. Refresh all.
        NOTE: VXUS has a Vanguard share-class problem — "Vanguard Total Intl
        Stock Index Admiral" should probably map to VTIAX not VXUS. Flag this
        for DS to evaluate as a potential ticker correction.

      CATEGORY C — Not in historical_prices at all (12 tickers):
        SMH, SOXX, PFDE, VEU, XLP, SCHG, VEIPX, PCHI, ETLG, XLY, SH, BTCX.
        These are mostly large liquid ETFs that should absolutely be in the
        scheduler. Add them and backfill.
        NOTE: VEIPX is a Vanguard mutual fund share class — same issue as
        Category B VXUS. Flag for DS.

      DS ticker corrections (from commit 61b34f77) also require:
        GLTR — add to scheduler (corrected from GLDM)
        VTMGX — add to scheduler (corrected from VEA)

      TOTAL: Fix 4 stale + 17 dropped + 12 missing + 2 DS corrections = 35 tickers
      to resolve before the canonical rebuild will work correctly for all switchers.
      The other 110+ are fine (fresh yahoo data <= 7 days).

      After fixing: verify ALL tickers in the switching pool have rows through
      at least 2026-03-20 in historical_prices.parquet. Run a count check:
        SELECT ticker, MAX(date), COUNT(*) FROM historical_prices
        WHERE ticker IN ({switching_tickers}) GROUP BY ticker
    </requirement>

    <requirement id="1">
      Deploy code to EC2. Upload both pricing scripts to S3:
        aws s3 cp data/black_diamond/scripts/silver/bd_price_update.py \
          s3://opal-data-bd/code/silver/bd_price_update.py
        aws s3 cp data/black_diamond/scripts/silver/build_canonical_prices_v2.py \
          s3://opal-data-bd/code/silver/build_canonical_prices_v2.py

      Next bd_price_update run will use the corrected hierarchy + ticker fixes.
    </requirement>

    <requirement id="2">
      Repair BNP PARIBAS canonical data. The 2026-03-19 and 2026-03-20 rows in
      canonical_prices.parquet show $95.03 for BNP PARIBAS SA (from yahoo matching
      BNPQF before the scoped_override priority fix). These need to be patched back
      to $0.75 (the scoped override price).

      After deploying the new code, a full rebuild of canonical_prices will fix this
      automatically since scoped_override now has highest priority. Verify after
      rebuild that BNP PARIBAS SA shows source=scoped_override, price=0.75.
    </requirement>

    <requirement id="3">
      Add GLTR and VTMGX to the EC2 historical-prices-scheduler ticker list.
      These are corrected tickers from DS's _TICKER_CORRECTIONS:
        - GLDM was corrected to GLTR (Aberdeen Physical Precious Metals Basket)
        - VEA was corrected to VTMGX (Vanguard Tax-Managed Int'l Fund)

      Both need to be in historical_prices.parquet for yahoo prices to be available.
      Add them to whatever config the scheduler reads and trigger a refresh.
    </requirement>

    <requirement id="4">
      Patch ticker_lookup.json on S3 to align with the code corrections.
      The _TICKER_CORRECTIONS map in bd_price_update.py fixes tickers at runtime,
      but the S3 ticker_lookup.json (if it exists as a shared artifact) should
      also reflect:
        - BNP PARIBAS SA: ticker = None (removed)
        - SONY FINL GROUP INC: ticker = None (removed)
        - FNDA -> FNX
        - GLDM -> GLTR
        - IJH -> IJK
        - VBR -> VSIAX
        - VEA -> VTMGX
        - VO -> VMCPX
    </requirement>

    <requirement id="5">
      Run full gold layer rerun to propagate corrected prices to positions_cube,
      holdings_lots, composition artifacts, and all downstream outputs.
        bash run_gold_layer.sh full

      This is the SAME gold rerun gated on MVPLVL.009. If MVPLVL.009 gold rerun
      already happened via PRICES.001, this is a second pass with corrected prices.
    </requirement>

    <requirement id="6">
      Run reconciliation diagnostic after gold rerun:
        python recon_lots_vs_allocations.py --date {latest_date}

      Compare to PRICES.001 post-fix baseline (-$57.7M, -3.6%):
      - Pricing undershoot component should drop from ~-$41M toward ~-$5M
        (DS dry-run predicted significant recovery from the 5 core ETFs alone)
      - Structural gaps (~-$15M) unchanged
      - Target: net gap within -1.5% of BD AUA

      Also verify the before/after price source distribution:
      - How many assets switched to yahoo_finance
      - Confirm scoped_override count is unchanged (overrides protected)
      - Confirm BNP PARIBAS SA is scoped_override at $0.75, not yahoo at $95
    </requirement>

    <requirement id="7">
      iShares U.S. Financials ETF ticker correction: XLF -> IYF.
      DS flagged this as a -16.5% error but did not include it in commit 61b34f77.
      Add IYF correction to _TICKER_CORRECTIONS in both bd_price_update.py and
      build_canonical_prices_v2.py before deploying. Commit separately:
        fix(silver): correct iShares US Financials ticker XLF -> IYF (ADVI_PRICES-003)
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Both pricing scripts deployed to S3</criterion>
    <criterion id="2">BNP PARIBAS SA confirmed at scoped_override $0.75 in rebuilt canonical_prices</criterion>
    <criterion id="3">GLTR and VTMGX added to historical-prices-scheduler</criterion>
    <criterion id="4">ticker_lookup.json on S3 patched with 8 corrections</criterion>
    <criterion id="5">Gold rerun completes without errors</criterion>
    <criterion id="6">Reconciliation shows reduced pricing undershoot vs -$57.7M baseline</criterion>
    <criterion id="7">iShares US Financials ticker corrected to IYF</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify _SCOPED_OVERRIDE_MAP entries -- only ticker corrections</constraint>
    <constraint>Verify BNP PARIBAS stays at $0.75 after rebuild -- this is the canary</constraint>
    <constraint>No emojis in code or log output (CLAUDE.md rule 13)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_PRICES.003.ds-yahoo-priority-validation" status="complete">
      DS committed hierarchy fix + ticker corrections at 61b34f77. Diagnostic at 08b6d557.
    </dependency>
    <dependency agent="0.6.0_AE_PartnerETL" task="ADVI_PRICES.001.ae-recon-run-and-gold-rerun" status="pending">
      PRICES.001 gold rerun should complete first (shared gate with MVPLVL.009).
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="deploy">Pricing scripts deployed, canonical_prices rebuilt, gold rerun complete</deliverable>
    <deliverable type="commit">iShares US Financials ticker correction (XLF -> IYF)</deliverable>
    <deliverable type="verify">Reconciliation comparison vs PRICES.001 baseline</deliverable>
    <deliverable type="document">Session log with before/after price source distribution + recon waterfall</deliverable>
  </deliverables>
</task_order>
