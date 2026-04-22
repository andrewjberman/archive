<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w4.8-B-chain-holdings-prices</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>complete</status>
    <completed>2026-04-22</completed>
    <commit>af3c4963</commit>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Author the full B-chain holdings/lots/prices pipeline for INF — two parts:

    PART A — Canonical prices pipeline (mirror BD 4-tier hierarchy, per CTO + Andrew directive):
    - `data/inf/scripts/silver/backfill_yahoo_prices_inf.py` — Yahoo historical price backfill
    - `data/inf/scripts/gold/build_canonical_prices_inf.py` — 4-tier price build (T1 observed, T2 Yahoo, T3 interp, T4 carry-forward)
    - `data/inf/scripts/silver/inject_scoped_overrides.py` — stub empty for v1
    - `data/inf/scripts/gold/lib/ticker_overrides.py` — FID:CASH and known Orion aliases
    - `data/inf/config/ticker_lookup.json` — from Orion TRN distinct(ticker, asset_name)
    - `data/inf/config/yahoo_safe_tickers.txt` — starts empty, populated by first backfill

    PART B — B-chain holdings/lots scripts:
    - `data/inf/scripts/gold/I_B01.holdings_lots.py`
    - `data/inf/scripts/gold/I_B01b.classify_new_securities.py`
    - `data/inf/scripts/gold/I_B02.canonical_lots.py`
    - `data/inf/scripts/gold/I_B03.account_gains.py`

    Blocked on W4.7 complete (B-chain reads I_A03 positions_cube and ticker_lookup.json
    built at W4.7 time from accounts_dimension/positions_cube silver pass).
  </objective>

  <context>
    CTO directive 2026-04-21: "borrow from how bd-pipeline does it with yahoo finance backfill
    and historical prices etc." Full BD 4-tier architecture is the mandate. Andrew confirmed.

    PRICES — 4-tier hierarchy (non-negotiable per CTO):
    - T1 transaction_observed: median daily nav_price per (ticker, date) from Orion TRN
      where quantity != 0 and transaction_type in trade-type set. Source: silver/transactions/
    - T2 yahoo_finance: from silver/historical_prices.parquet (built by backfill_yahoo_prices_inf.py)
    - T3 linear_interpolation: fill gaps between T1/T2 known price points
    - T4 carry_forward: fill trailing gaps after last known price
    Each tier exists to handle a specific failure mode — do NOT collapse tiers.

    TICKER SPECIAL CASES (from CTO):
    - FID:CASH (Orion's Fidelity cash alias): treat as cash asset, price=1.0 ALWAYS.
      Handle in ticker_overrides.py, NOT via Yahoo. Gold layer applies, not silver.
    - Any other Orion-specific ticker alias that Yahoo won't price: add to ticker_overrides.py.

    YAHOO BACKFILL:
    - Mirror data/black_diamond/scripts/silver/backfill_yahoo_prices_safe.py exactly.
    - Parameterize S3_BUCKET to opal-data-inf. Do NOT hardcode opal-data-bd.
    - Same rate-limit + checkpoint + resume logic (do not simplify — rate-limit logic exists
      for a reason: Yahoo throttles at ~2000 req/day per IP).
    - Output: silver/historical_prices.parquet in opal-data-inf
    - Upload to: s3://opal-data-inf/code/silver/backfill_yahoo_prices_inf.py

    ISOLATION: Zero cross-bucket reads. All prices output to opal-data-inf. No dependency on BD prices.

    Q2 2024 GAP: silver TRN is continuous 2019-09-17 to 2026-04-20. Yahoo backfill is
    dates-agnostic — covers Q2 2024 automatically. No special handling needed.

    ticker_lookup.json: Build from Orion TRN silver distinct(ticker, asset_name) pairs.
    DS should build this at W4.7 time (during positions_cube silver pass) and save to
    data/inf/config/ticker_lookup.json. Coordinate with W4.7 — if not built there, build
    it as part A first step of W4.8.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before authoring):
    <run>comp-pipescript io build_canonical_prices_v2 (BD precedent)</run>
    <expect>4-tier structure, column inputs, S3 output path. Adapt for INF.</expect>
    <run>comp-pipescript io B_01 (BD precedent)</run>
    <expect>holdings_lots reads canonical_prices.parquet precondition — confirm INF equivalent.</expect>

    Phase 2 (after authoring — prices first):
    <run>python -m py_compile data/inf/scripts/silver/backfill_yahoo_prices_inf.py</run>
    <run>python -m py_compile data/inf/scripts/gold/build_canonical_prices_inf.py</run>
    <run>python -m py_compile data/inf/scripts/silver/inject_scoped_overrides.py</run>
    <run>python -m py_compile data/inf/scripts/gold/lib/ticker_overrides.py</run>
    <expect>All exit 0.</expect>
    <run>.tools/ds-commit-gate.sh data/inf/scripts/silver/backfill_yahoo_prices_inf.py data/inf/scripts/gold/build_canonical_prices_inf.py data/inf/scripts/silver/inject_scoped_overrides.py data/inf/scripts/gold/lib/ticker_overrides.py data/inf/scripts/gold/I_B01.holdings_lots.py data/inf/scripts/gold/I_B01b.classify_new_securities.py data/inf/scripts/gold/I_B02.canonical_lots.py data/inf/scripts/gold/I_B03.account_gains.py</run>
    <expect>All pass.</expect>

    <run>comp-pipescript io build_canonical_prices_inf.py</run>
    <expect>0 COLUMN GAPS. Verifies positions_cube downstream column alignment.</expect>

    Phase 3 (after first backfill run + prices build):
    <run>aws s3 ls s3://opal-data-inf/silver/prices/canonical_prices.parquet</run>
    <expect>Object present. Size > 0.</expect>
    <run>comp-pipescript deployed build_canonical_prices_inf</run>
    <expect>MATCH on inf-gold-runner.</expect>
    <run>comp-pipescript deployed I_B01</run>
    <expect>MATCH on inf-gold-runner.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    blocked_on: "W4.7 A-chain complete (positions_cube + ticker_lookup.json built)."
    ае_0.6.1_coordination: "AE 0.6.1 handles upload of backfill_yahoo_prices_inf.py to
    s3://opal-data-inf/code/silver/ — coordinate handoff after DS commits."
    required_action: "After canonical_prices.parquet is confirmed in S3, signal COO.
    W4.9 (C-chain) unblocks immediately."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. backfill_yahoo_prices_inf.py: py_compile exit 0 + ds-commit-gate PASS.
       First backfill run completes: silver/historical_prices.parquet in opal-data-inf.
    2. build_canonical_prices_inf.py: 4 tiers implemented (T1/T2/T3/T4).
       canonical_prices.parquet written to opal-data-inf/silver/prices/.
       comp-pipescript io: 0 COLUMN GAPS.
    3. ticker_overrides.py: FID:CASH → price=1.0 at gold layer. Orion aliases documented.
    4. inject_scoped_overrides.py: stub exit 0 (no overrides for v1).
    5. ticker_lookup.json: populated with Inflection distinct tickers from Orion TRN silver.
    6. All 4 B-chain scripts (I_B01-I_B03): py_compile exit 0 + ds-commit-gate PASS.
    7. No Schwab/ACAT logic in any B-chain script.
    8. NaT guard on all date columns.
    9. comp-pipescript deployed MATCH on inf-gold-runner for all scripts.
    10. Session log: backfill duration, ticker count, unclassified ticker list (I_B01b),
        pricing coverage % (must be > 80% per gold_pipeline_deps.yaml warning threshold).
    11. MCP COO: canonical_prices LIVE (W4.9 gate signal).
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">data/inf/scripts/silver/backfill_yahoo_prices_inf.py</file>
      <file action="create">data/inf/scripts/gold/build_canonical_prices_inf.py</file>
      <file action="create">data/inf/scripts/silver/inject_scoped_overrides.py</file>
      <file action="create">data/inf/scripts/gold/lib/ticker_overrides.py</file>
      <file action="create">data/inf/config/ticker_lookup.json</file>
      <file action="create">data/inf/config/yahoo_safe_tickers.txt</file>
      <file action="create">data/inf/scripts/gold/I_B01.holdings_lots.py</file>
      <file action="create">data/inf/scripts/gold/I_B01b.classify_new_securities.py</file>
      <file action="create">data/inf/scripts/gold/I_B02.canonical_lots.py</file>
      <file action="create">data/inf/scripts/gold/I_B03.account_gains.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">4-tier price hierarchy (T1/T2/T3/T4) — non-negotiable per CTO + Andrew.</requirement>
    <requirement id="2">Mirror BD build_canonical_prices_v2.py — copy + adapt, do NOT redesign.</requirement>
    <requirement id="3">Yahoo backfill: same rate-limit + checkpoint + resume as BD equivalent.</requirement>
    <requirement id="4">FID:CASH → price=1.0 in ticker_overrides.py (gold layer, not silver).</requirement>
    <requirement id="5">Zero cross-bucket reads — all outputs to opal-data-inf.</requirement>
    <requirement id="6">Pricing coverage > 80% before signaling W4.9 (gold_pipeline_deps.yaml threshold).</requirement>
    <requirement id="7">NaT guard on all date columns (d87377a5 mandate).</requirement>
    <requirement id="8">ds-commit-gate + commit + push + S3 upload (opal-data-inf/code/gold/ and opal-data-inf/code/silver/).</requirement>
    <requirement id="9">comp-pipescript io on build_canonical_prices_inf.py before commit.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">10 files committed + pushed to CLOUD.</deliverable>
    <deliverable type="s3">Scripts uploaded to opal-data-inf/code/gold/ and opal-data-inf/code/silver/. canonical_prices.parquet in opal-data-inf/silver/prices/.</deliverable>
    <deliverable type="document">Session log: backfill duration, ticker count, coverage %, unclassified list.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT collapse price tiers — each tier handles a distinct failure mode.</rule>
    <rule>Do NOT read from opal-data-bd for prices (bucket isolation mandate).</rule>
    <rule>Do NOT skip Yahoo rate-limit logic — throttle protection is not optional.</rule>
    <rule>Do NOT signal W4.9 until pricing_coverage_pct > 80.</rule>
    <rule>Do NOT hardcode S3 bucket — parameterize as S3_BUCKET=opal-data-inf.</rule>
  </do_not>
</task_order>
