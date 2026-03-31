# Task Order: ADVI_TICKID.005 — Ticker Resolution Feedback Bridge + Method 5

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-ticker-feedback-bridge</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
  </metadata>

  <objective>
    Build a feedback bridge from resolve_tickers.py into the pricing pipeline.
    Currently, resolved tickers enrich holdings_lots (script 03) but do NOT feed
    back into ticker_lookup.json or yahoo_safe_tickers.txt. Result: 6,146 assets
    with no ticker in the pricing pipeline even though many are resolvable.
    This is the single largest pricing divergence at $257M gross impact.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/classification/resolve_tickers.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Add sync_to_ticker_lookup() function in resolve_tickers.py. After
      ticker_resolution.parquet is written: (a) load current config/ticker_lookup.json from S3,
      (b) read the just-produced ticker_resolution.parquet, (c) for each resolved entry with
      confidence >= 0.85 where the asset_name_raw is not already in ticker_lookup.json with a
      real ticker, append {"asset_name": asset_name_raw, "ticker": resolved_ticker,
      "added_date": today, "source": "resolve_tickers"}, (d) write enriched ticker_lookup.json
      back to S3, (e) log count of new entries added and total entries before/after.</requirement>
    <requirement id="2">Append verified tickers to yahoo_safe_tickers.txt. For each
      newly-added ticker from Step 1: validate it returns data from Yahoo Finance
      (yfinance.download(ticker, period='5d')). If valid, append to config/yahoo_safe_tickers.txt
      on S3. If invalid, log as unresolvable but leave in ticker_lookup.json.</requirement>
    <requirement id="3">Implement method 5 (individual_stock_pattern) in resolve_tickers.py.
      Currently a stub returning empty dict (line 248). Individual stocks like
      "WALMART INC COM -> WMT" will NOT resolve without this. Use deterministic
      approach against a known-companies lookup, or adapt the GPT-based --discover mode
      from fetch_historical_prices_yfinance.py (lines 454+). Without method 5, only ETFs
      and mutual funds resolve — individual equities do not.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">ticker_lookup.json entry count increases after resolve_tickers.py runs</criterion>
    <criterion id="2">yahoo_safe_tickers.txt entry count increases for verified tickers</criterion>
    <criterion id="3">Method 5 resolves individual equity names to tickers (test with "WALMART INC COM" -> "WMT" type patterns)</criterion>
    <criterion id="4">canonical_prices.parquet shows T2 (yahoo_finance) source for previously-unpriced assets on next pricing rebuild</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT overwrite existing entries in ticker_lookup.json that have different tickers. TICKER_CORRECTIONS (34 entries in lib/ticker_overrides.py) takes final precedence in load_ticker_lookup(). The feedback bridge merge is append-only for new asset_names.</constraint>
    <constraint>Do NOT bypass yahoo_safe_tickers.txt by fetching ALL tickers from ticker_lookup.json. The safe list exists because Yahoo throttles at 10K+ tickers. Grow the safe list incrementally with verified tickers only.</constraint>
    <constraint>After Steps 1-2 complete, a re-run of fetch_historical_prices_yfinance.py --backfill on EC2 is needed to populate historical prices for newly-added safe tickers. This is an AE responsibility — flag it in your session log for AE handoff.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_TICKID.001-004" status="complete"/>
  </dependencies>

  <references>
    <ref type="prd">docs/architecture/ADVI_TICKID_PRICING_DIVERGENCE_ADDENDUM.md</ref>
  </references>

  <deliverables>
    <deliverable type="commit">Modified resolve_tickers.py with sync_to_ticker_lookup() and method 5 implementation</deliverable>
  </deliverables>
</task_order>
