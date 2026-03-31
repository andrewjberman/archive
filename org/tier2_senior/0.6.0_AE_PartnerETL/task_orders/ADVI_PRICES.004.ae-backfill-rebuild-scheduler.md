<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-24-prices-004-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-24</date>
    <status>complete</status>
    <project_code>ADVI_PRICES</project_code>
  </metadata>

  <objective>
    Four phases, strictly sequential (except Phase 4 which can parallel Phase 3).

    DS .004 is COMPLETE. Deliverables:
    - 32 ticker corrections in _TICKER_CORRECTIONS (commits 61b34f77, 1c7bbb4a,
      2e9e90a4, 16c8ea84)
    - Yahoo-safe ticker list: data/black_diamond/config/yahoo_safe_tickers.txt
      (2,880 verified tickers, commit 4f4a7fc1)
    - Full audit: org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-03-24/
      advi_prices_004_ticker_audit.md

    Phase 1: Backfill historical_prices for verified tickers
    Phase 2: Rebuild canonical prices
    Phase 3: Full gold rerun + reconciliation
    Phase 4: Diagnose and fix the historical-prices-scheduler
  </objective>

  <scope>
    <files>
      <file action="reference">data/black_diamond/config/yahoo_safe_tickers.txt</file>
      <file action="upload-to-s3">data/black_diamond/scripts/silver/bd_price_update.py</file>
      <file action="upload-to-s3">data/black_diamond/scripts/silver/build_canonical_prices_v2.py</file>
      <file action="run-on-ec2">build_canonical_prices_v2.py</file>
      <file action="run-on-ec2">bd_price_update.py</file>
      <file action="run-on-ec2">run_gold_layer.sh full</file>
      <file action="run-on-ec2">recon_lots_vs_allocations.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      PHASE 1 — Historical prices backfill.

      The yahoo-safe ticker list is at data/black_diamond/config/yahoo_safe_tickers.txt
      (2,880 tickers, committed at 4f4a7fc1). This is the DEFINITIVE list — only
      tickers on this list should receive yahoo pricing.

      Step 1a: Upload the latest code (with all 32 corrections) to S3:
        aws s3 cp data/black_diamond/scripts/silver/bd_price_update.py \
          s3://opal-data-bd/code/silver/bd_price_update.py
        aws s3 cp data/black_diamond/scripts/silver/build_canonical_prices_v2.py \
          s3://opal-data-bd/code/silver/build_canonical_prices_v2.py

      Step 1b: For each ticker on the yahoo-safe list, check against
      historical_prices.parquet on S3. Three categories:

        MISSING (not in historical_prices at all):
          DS identified 505 tickers in canonical with no yahoo data, plus 18
          newly corrected tickers that need backfill:
            CBLL, SERV, IUSG, IWR, USXF, BAI, QQQM, PSLV, FLRN,
            VBTIX, VTIAX, VTSNX, VTPSX, VSMSX, VEMIX, SWAGX, SWTSX, SWPPX

          For each: fetch full yfinance history and append to historical_prices.

        STALE (latest date > 7 days old):
          DS identified ~706 tickers that went dark around Feb 12, plus a
          second cluster around Feb 24-Mar 10. Examples:
            IDVZ, PFOE, XLE, VUSB (Feb 12 cutoff)
            VXUS, QUAL, SLV, V, QQQ, NVDA (Feb 24 - Mar 10)

          For each: fetch from last available date to present and append.

        CURRENT (latest date within 7 days):
          Skip — already good.

      Step 1c: After backfill, verify coverage. For every ticker on the
      yahoo-safe list, confirm it has rows through at least 2026-03-21:
        python -c "
        import pandas as pd
        hp = pd.read_parquet('historical_prices.parquet')
        safe = open('yahoo_safe_tickers.txt').read().splitlines()
        latest = hp.groupby('ticker')['date'].max()
        for t in safe:
            d = latest.get(t)
            if d is None: print(f'MISSING: {t}')
            elif d.date() < pd.Timestamp('2026-03-21').date(): print(f'STALE: {t} last={d.date()}')
        "

      Upload updated historical_prices.parquet to S3.

      NOTE: AE already has a local fetch script at
      C:\Users\AndrewBerman\AppData\Local\Temp\fetch_missing_tickers.py.
      Adapt it to read the yahoo-safe list instead of hardcoding 6 tickers.
      The script must handle yfinance rate limits gracefully (batch, sleep
      between requests).
    </requirement>

    <requirement id="2">
      PHASE 2 — Canonical prices rebuild.

      Run build_canonical_prices_v2.py on EC2 (full rebuild). This:
      - Applies the hierarchy: scoped_override > yahoo > T1 > carry_forward
      - Uses all 32 ticker corrections in _TICKER_CORRECTIONS
      - Picks up the backfilled historical_prices

      Then run bd_price_update.py for the latest date to produce the dated
      canonical output with scoped overrides applied.

      Verify (all 3 are required before proceeding):

      a. BNP PARIBAS SA canary:
         - In build_canonical_prices_v2 output: ticker=None (correction removes it),
           source should be transaction_observed or linear_interpolation, NOT yahoo
         - In bd_price_update output: source=scoped_override, price=$0.75

      b. Source distribution improvement:
         - Premature rebuild was: 82.3% interpolation, 15.8% yahoo, 1.9% T1
         - After backfill expect: yahoo % should increase significantly
         - Report the exact counts

      c. Spot-check 5 previously broken tickers:
         - IEFA: should be ~$89 (was $57.43 from 2020)
         - IEMG: should be ~$70 (was $48.22 from 2020)
         - IJK (was IJH): should be ~$103 (was $1.00)
         - VBTIX (was BND): should be ~$9.66 (was $73.45 ETF price)
         - CBLL (was CRBL): should be ~$19 (was $0.05 penny stock)
    </requirement>

    <requirement id="3">
      PHASE 3 — Gold layer rerun + reconciliation.

      Run: bash run_gold_layer.sh full

      After completion:
        python recon_lots_vs_allocations.py --date {latest_alloc_date}

      Compare to baselines:

      | Baseline | Net Gap | % |
      |----------|---------|---|
      | Pre-fix (2026-03-19) | +$296M | +18.6% |
      | Post PRICES.001 (phantom fix) | -$57.7M | -3.6% |
      | Post PRICES.003+004 (yahoo priority) | TARGET | < -1.5% |

      Report the full waterfall: RC1 phantom, RC2 alloc-only, RC3 insurance,
      RC4 non-investment, RC5 normal (split by pricing over/under).

      If net gap > -1.5%: flag remaining root causes to COO.
      If net gap <= -1.5%: structural gaps are the accepted remainder.
    </requirement>

    <requirement id="4">
      PHASE 4 — Scheduler diagnosis and fix (can run parallel with Phase 3).

      The historical-prices-scheduler stopped updating ~706 tickers around Feb 12.

      a. Identify: what script/cron/service is the scheduler? Where is its config?
         What ticker list does it read? Where does it run (EC2, Lambda, local)?

      b. Diagnose: what happened around Feb 12? Possible causes:
         - VM restarted without cron restoration
         - yfinance API rate limiting or version change
         - Config file corruption or ticker list truncation
         - Script crash without error reporting

      c. Fix: ensure the scheduler:
         - Reads the yahoo-safe ticker list (data/black_diamond/config/yahoo_safe_tickers.txt)
           OR reads ticker_lookup.json on S3 (already patched with 9 corrections in .003)
         - Runs daily and writes to s3://opal-data-bd/silver/historical_prices.parquet
         - Completes within a reasonable window (the list is 2,880 tickers)

      d. Verify: run manually and confirm it completes with current-day closes.

      e. Monitor: confirm it runs automatically the next business day.

      f. Document: what was the root cause, what was fixed, and where the
         scheduler config lives for future reference.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All 2,880 yahoo-safe tickers current in historical_prices.parquet (verified by coverage check)</criterion>
    <criterion id="2">Canonical prices rebuilt — yahoo % increased, BNP canary passed, 5 spot-checks passed</criterion>
    <criterion id="3">Gold rerun complete, reconciliation within -1.5% of BD AUA</criterion>
    <criterion id="4">Scheduler root cause identified, fixed, confirmed running daily</criterion>
    <criterion id="5">Session log documents all 4 phases with verification output</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>ONLY use tickers from data/black_diamond/config/yahoo_safe_tickers.txt for backfill</constraint>
    <constraint>DO NOT start Phase 2 until Phase 1 coverage check passes</constraint>
    <constraint>DO NOT start Phase 3 until Phase 2 spot-checks pass</constraint>
    <constraint>Phase 4 can start anytime (investigation doesn't require gold rerun)</constraint>
    <constraint>No emojis in code or log output (CLAUDE.md rule 13)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_PRICES.004" status="complete">
      DS delivered: 32 ticker corrections (4 commits), yahoo-safe list (2,880 tickers
      at data/black_diamond/config/yahoo_safe_tickers.txt, commit 4f4a7fc1), full audit
      log at org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-03-24/advi_prices_004_ticker_audit.md.
    </dependency>
    <dependency agent="0.6.0_AE_PartnerETL" task="ADVI_PRICES.003" status="in_progress">
      .003 partial work: IYF correction committed (1c7bbb4a), scripts uploaded to S3,
      ticker_lookup.json patched, premature canonical rebuild done (needs re-run after
      backfill). EC2 runner is RUNNING.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="deploy">historical_prices backfilled for 2,880 tickers, canonical rebuilt, gold rerun complete</deliverable>
    <deliverable type="verify">Reconciliation waterfall showing improvement from -3.6% baseline</deliverable>
    <deliverable type="deploy">Scheduler fixed and running daily for yahoo-safe ticker list</deliverable>
    <deliverable type="document">Session log covering all 4 phases with verification output</deliverable>
  </deliverables>
</task_order>
