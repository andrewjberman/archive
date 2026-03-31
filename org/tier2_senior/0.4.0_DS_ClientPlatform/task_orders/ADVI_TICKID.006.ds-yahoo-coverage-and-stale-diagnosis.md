# Task Order: ADVI_TICKID.006 — Yahoo Coverage Sweep + Stale Ticker Diagnosis

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-yahoo-coverage-stale</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
  </metadata>

  <objective>
    Close two yahoo pricing gaps: (F2) 493 assets have tickers in ticker_lookup.json
    but are NOT in yahoo_safe_tickers.txt — they get no T2 prices and fall through to
    T3/T4. (F3) 38 assets have Yahoo data that stops before 2026-03-24 — some are
    delisted, some just need a refresh. Combined gross impact: $11.7M.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/silver/fetch_historical_prices_yfinance.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Add --sweep-unlisted mode to fetch_historical_prices_yfinance.py:
      (a) load all tickers from ticker_lookup.json (filtering UNKNOWN/empty),
      (b) load current yahoo_safe_tickers.txt,
      (c) find tickers in lookup but NOT in safe list,
      (d) batch-validate each against Yahoo Finance (50/batch, 3s delay — same pattern as daily mode),
      (e) append verified tickers to safe list,
      (f) log count added and any tickers that failed validation.</requirement>
    <requirement id="2">Add --diagnose-stale mode to fetch_historical_prices_yfinance.py:
      (a) load historical_prices.parquet,
      (b) for each ticker find max date,
      (c) flag tickers where max_date < today - 7 days,
      (d) attempt re-fetch for each stale ticker,
      (e) if Yahoo returns data: append to parquet,
      (f) if Yahoo returns no data: log as "delisted or symbol changed."</requirement>
    <requirement id="3">For symbol-changed tickers identified by --diagnose-stale: investigate
      and add the new ticker to TICKER_CORRECTIONS in lib/ticker_overrides.py if the
      mapping is deterministic. Log ambiguous cases for manual review.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">yahoo_safe_tickers.txt grows by the count of verified tickers from the 493 unlisted</criterion>
    <criterion id="2">Those tickers now show T2 prices in canonical_prices.parquet after next pricing rebuild</criterion>
    <criterion id="3">Stale ticker count drops to only genuinely-delisted securities</criterion>
    <criterion id="4">Active tickers resume daily price updates</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Maintain batch sizes (50/batch, 3s delay) for Yahoo requests. Do not exceed ~500 new tickers per run to avoid rate limiting.</constraint>
    <constraint>Delisted securities with last known price carry-forward are correct behavior — no action beyond logging.</constraint>
    <constraint>Check git history of yahoo_safe_tickers.txt to see if any of the 38 stale tickers were previously removed during a prior cleanup.</constraint>
    <constraint>After completion, a re-run of --backfill on EC2 is needed for newly-added tickers. AE responsibility.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_TICKID.005" status="pending"/>
  </dependencies>

  <references>
    <ref type="prd">docs/architecture/ADVI_TICKID_PRICING_DIVERGENCE_ADDENDUM.md</ref>
  </references>

  <deliverables>
    <deliverable type="commit">Modified fetch_historical_prices_yfinance.py with --sweep-unlisted and --diagnose-stale modes</deliverable>
  </deliverables>
</task_order>
