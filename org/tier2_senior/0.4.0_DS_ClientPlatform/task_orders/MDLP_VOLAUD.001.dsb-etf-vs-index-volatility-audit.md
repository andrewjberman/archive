<task_order>
  <metadata>
    <id>MDLP_VOLAUD.001</id>
    <slug>dsb-etf-vs-index-volatility-audit</slug>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-19</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED via Andrew-direct CTO authorization 2026-05-19 ~13:40Z. Read-only investigation; no upstream gates.</dispatch_unblock_condition>
    <project_code>MDLP_VOLAUD</project_code>
    <priority>P1 -- Andrew-direct CTO directive 2026-05-19. The ETF-vs-INDEX volatility gap visible in the Model Portfolios -> Benchmarks tab -> Return vs Volatility (period volatility) chart needs empirical confirmation that the difference is explainable microstructure noise, not a data-construction defect. Investigation only; output is a finding brief, no code/artifact write.</priority>
    <sla>~3-5h wall -- empirical inspection of the source pickle + the published JSON, statistical characterization, brief authored. No script modified.</sla>
  </metadata>

  <references>
    <lambda>infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-model-portfolio-benchmarks/lambda_function.py -- produces `model_portfolio_benchmarks.json` with `index_benchmark_volatility` + `etf_benchmark_volatility` fields. Both are computed via `calculate_volatility` (line 470-477): `np.std(daily_returns_decimal, ddof=1) * sqrt(252) * 100`, applied independently to `index_series` and `etf_series` extracted from `data.pkl -> return_daily` per INDEX_NAME_MAP (line 65-91). Methodology is identical across the two series; only the input series differ.</lambda>
    <source_artifact>s3://opal-data-portal-v2/benchmarks/data_*.pkl -- the source pickle. `return_daily` DataFrame contains 15 series of interest: {model, index_benchmark, etf_benchmark} x {UST, ST, INT, LTC, LTA}, keyed by `index_name`. LTC + LTA share the same Long-Term Benchmark + Long-Term ETF series (4 distinct INDEX-vs-ETF pairs, since LTC/LTA collapse to one).</source_artifact>
    <published_artifact>s3://opal-data-portal-v2/json/benchmarks/model_portfolio_benchmarks.json -- the live published period-vol values; the artifact the FE chart consumes.</published_artifact>
    <cto_grounding>The period-volatility methodology is empirically identical for INDEX and ETF (same `calculate_volatility` function; series-agnostic). The numeric difference comes entirely from the underlying daily-return-series difference. Structurally ETF vol >= INDEX vol expected because ETF return = INDEX return + microstructure overlay (premium/discount-to-NAV, bid-ask spread effects, tracking error, dividend cadence, embedded ETF fees BIL ~14bps / AGG ~3bps / IVV ~3bps). This audit empirically verifies that framing.</cto_grounding>
  </references>

  <context>
    The Model Portfolios -> Benchmarks tab -> Return vs Volatility chart (period-volatility view) displays scatter points for both INDEX-benchmark volatility and ETF-benchmark volatility per period, switchable via the page-level Index/ETF toggle. Andrew flagged today that the visible ETF-vs-INDEX volatility gap warrants empirical confirmation -- "it is possible its explainable but need to make sure." This TO answers that question by pulling the raw daily-return series for both INDEX and ETF benchmarks from the source pickle, quantifying the difference statistically per model and per window, reproducing the Lambda's published vol numbers, and verifying the difference is consistent with explainable microstructure noise (or surfacing a specific anomaly that isn't).
  </context>

  <scope>
    <in_scope>
      - **Source extraction:** load the most-recent `data.pkl` from `s3://opal-data-portal-v2/benchmarks/` (resolve key via `benchmarks/LATEST.json -> data_pkl`); extract `return_daily` filtered to `index_name` containing "Term" + weekday-only + non-zero-row mirror of the Lambda's `get_term_returns` (line 333-367). Pivot to wide format with date index and `index_name` columns.
      - **Per-model series extraction:** for each of the 5 model codes (UST, ST, INT, LTC, LTA), extract the INDEX-benchmark series and the ETF-benchmark series per `INDEX_NAME_MAP` (Lambda line 65-91). LTC and LTA share the same Long-Term Benchmark + Long-Term ETF series -- 4 distinct INDEX-vs-ETF pairs to audit.
      - **Structural inspection per series:** row count, date range (first/last), NaN count, zero-return-day count, max absolute single-day move (with date). Flag any series where the structure differs meaningfully from its INDEX counterpart -- e.g., ETF series starts later than INDEX, has materially more or fewer zero-return rows, or has unrelated absolute scale.
      - **Pairwise difference quantification** for each (INDEX, ETF) pair over three windows (1Y last 252 weekday entries / YTD 2026-01-01 forward / Since Inception 2024-04-30 forward):
        - Pearson correlation of the daily-return decimals
        - stdev ratio (ETF stdev / INDEX stdev)
        - daily ETF-minus-INDEX residual: mean, stdev, max absolute residual + date of the max
        - autocorrelation of the residual at lag 1 (material positive lag-1 autocorrelation suggests persistent tracking-error, not random noise)
      - **Reproduce published vols:** for each of the 9 periods (1D, WTD, MTD, 1M, QTD, 1Q, YTD, 1Y, Since Inception) and each model: run the Lambda's exact `calculate_volatility` formula against both series; compare the recomputed value against the live `model_portfolio_benchmarks.json` published `index_benchmark_volatility` and `etf_benchmark_volatility`. Any discrepancy >0.01% rounded -> surface as a separate finding (would indicate a drift between the Lambda code and the live published artifact -- not the focus of this audit but caught for free).
      - **Microstructure-noise hypothesis test** per (model pair, window):
        - Correlation expected >=0.95 (typical >0.98 in calm windows; may drop to ~0.93-0.95 in stress windows)
        - ETF/INDEX stdev ratio expected ~1.00-1.20 in calm windows; can reach ~1.30 in stress windows
        - Residual mean expected near zero, with small negative drift from embedded fees plausible (~1-2bps/day decimal equivalent for AGG/IVV; up to ~14bps/year for BIL = ~0.5bps/day)
        - Residual extremes expected to cluster around ETF dividend ex-dates, FOMC days, or known market-stress days; isolated unexplained extremes -> flag
      - **Anomaly inventory** -- explicitly check + report on:
        - Any model/period where ETF vol < INDEX vol (structurally implausible; suggests inverted construction or data-flip)
        - Any model/window where the stdev ratio >1.30 in a calm-market period (no stress event, no dividend ex-date) -- suggests defect
        - Any window where correlation <0.90 -- suggests construction-level mismatch (different universe, different rebalance cadence, different reinvestment treatment)
        - Persistent residual drift that exceeds plausible-fee-drag magnitude (>5bps/day mean residual) -- suggests methodology mismatch
        - Material zero-return-day asymmetry between INDEX and ETF series (one has many more than the other) -- suggests calendar/holiday handling defect in source pickle construction
      - **Brief verdict** -- ONE sentence answering Andrew's framing: *"Is the published ETF-vs-INDEX volatility difference explainable as microstructure noise per the framing above, or is there a specific anomaly that requires a data-construction or methodology fix?"* Backed by AC1-AC5 evidence.
    </in_scope>
    <out_of_scope>
      - Modifying yang-model-portfolio-benchmarks Lambda or any data path. Investigation only. If a defect is surfaced, the brief identifies it; a separate fix TO scopes the change (AE 0.5.0 Yang-pipeline lane).
      - Investigating the timeseries-data-shape gap (why Rolling Sharpe / Max Drawdown / Up-Down Capture views lack ETF versions). That is a separate question downstream of this audit -- CTO scoping pending Andrew's call.
      - Product-level questions about whether ETF benchmarks are the "right" benchmark for the model portfolios. Audit is data-quality + methodology-fidelity only.
      - Auditing the model-portfolio RETURN values vs benchmark return values. Returns are not in scope; vol differences only.
      - Modifying the source pickle or the upstream Yang-team data process. Read-only consumer of the published artifact.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="grounding the probe">
      <step>
        <run>aws s3 ls s3://opal-data-portal-v2/benchmarks/ | tail -5</run>
        <expect>Recent pickle artifacts. The data_pkl key for the audit comes from `aws s3 cp s3://opal-data-portal-v2/benchmarks/LATEST.json - | jq -r '.data_pkl'`.</expect>
        <if_mismatch>If LATEST.json is missing/malformed, fall back to most-recent `data_*.pkl` by mtime and document the fallback in the brief.</if_mismatch>
      </step>
      <step>
        <run>aws s3 cp s3://opal-data-portal-v2/json/benchmarks/model_portfolio_benchmarks.json - | jq '.data_as_of, .models[0].code, .models[0].returns.YTD'</run>
        <expect>The currently-served `data_as_of` + a sample period's INDEX + ETF + model vol fields. Provides the published reference values for AC3 reproduce-check.</expect>
        <if_mismatch>If jq parses fail or fields differ from `ModelPortfolioPeriodReturn` shape (portal-proxy.ts:703), flag and read the raw JSON; the API contract drift would itself be a finding.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io yang-model-portfolio-benchmarks</run>
        <expect>Lambda I/O surface. May return empty per the existing comp-graph gap for Lambda paths -- if so, document and substitute direct source-read of `lambda_function.py:470-477` (`calculate_volatility`) + `:333-367` (`get_term_returns`) for the methodology reference. Either path satisfies the mandate.</expect>
        <if_mismatch>Empty result acceptable -- the Lambda may not be indexed in the comp-graph. Direct file read of the methodology is the canonical reference.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Read-only inspection of the source pickle + the published JSON. No silver/bronze touch. No Lambda invoke. Produces a finding brief in `docs/briefs/`, no script modified, no artifact written.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    None -- read-only inspection. yang-model-portfolio-benchmarks Lambda is owned by AE 0.5.0 (Yang pipeline). This TO does not touch the Lambda. If the audit surfaces a Lambda-level finding (series-construction defect in `get_term_returns`, a methodology drift, or a per-period filter bug in `calculate_period_returns`), surface to CTO base (1.0.0_SA_CTO) for a separate Yang-pipeline fix TO -- do NOT amend the Lambda in this TO. Source pickle is produced by an upstream Yang-team process; if the audit suggests the pickle itself is the issue (e.g., the ETF series carries upstream-known noise the INDEX series doesn't), surface that finding -- the fix is upstream.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">For all 5 model codes (UST, ST, INT, LTC, LTA) treating LTC/LTA shared Long-Term pair as one: INDEX-benchmark and ETF-benchmark daily-return series are extracted from the latest `data.pkl -> return_daily` (post-Lambda `get_term_returns` filter -- weekday-only, holiday-row-dropped). Structural inspection table reported per series: row count, date range, NaN count, zero-return-day count, max absolute daily-return with date.</ac>
    <ac id="AC2">For each of the 4 distinct (INDEX, ETF) pairs: Pearson correlation, stdev ratio (ETF / INDEX), residual mean + stdev + max-abs-residual with date, residual lag-1 autocorrelation -- computed over each of three windows: 1Y / YTD / Since Inception. Tables in the brief.</ac>
    <ac id="AC3">For each (model, period) combination (5 models x 9 periods = 45 cells): the Lambda's `calculate_volatility` is reproduced against both series; recomputed values cross-checked vs the live `model_portfolio_benchmarks.json` published values. Any discrepancy >0.01% absolute surfaced as a separate finding in the brief.</ac>
    <ac id="AC4">Microstructure-noise hypothesis tested per (pair, window) against the criteria: correlation >=0.95, stdev ratio 1.00-1.30, residual mean within plausible-fee-drag magnitude, residual lag-1 autocorrelation discussed. Each cell gets a verdict: consistent-with-microstructure OR flagged.</ac>
    <ac id="AC5">Anomaly inventory complete: explicit pass/fail report on each of the 5 anomaly classes (ETF<INDEX vol; ratio>1.30 in calm window; correlation<0.90; persistent residual drift exceeding fee-drag magnitude; calendar/zero-day asymmetry). Each anomaly: (model, period/window, magnitude, date if applicable, candidate root cause). If no anomalies -- explicit "no anomalies surfaced" statement, not silent.</ac>
    <ac id="AC6">Brief verdict: ONE sentence answering "is the published ETF-vs-INDEX volatility difference explainable as microstructure noise or is there a specific anomaly that needs a Lambda/source fix?" Backed by AC1-AC5 evidence.</ac>
    <ac id="AC7">Finding brief committed to `docs/briefs/mdlp-etf-vs-index-volatility-audit-20260519.md` with all tables, anomaly inventory, verdict, methodology-reproduction evidence.</ac>
    <ac id="AC8">Session log under `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-19/` with the Compiler Tools section. RAVC2 to 1.0.0_SA_CTO (Andrew-direct CTO routing for this audit, not via COO).</ac>
  </acceptance_criteria>

  <deliverables>
    - docs/briefs/mdlp-etf-vs-index-volatility-audit-20260519.md -- the audit brief (AC1-AC6).
    - Session log under org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-19/ with Compiler Tools section.
    - RAVC2 to 1.0.0_SA_CTO -- the brief is the input to the CTO's decision on whether to spin a Lambda-fix TO (if anomaly) or close the audit (if clean).
  </deliverables>
</task_order>
