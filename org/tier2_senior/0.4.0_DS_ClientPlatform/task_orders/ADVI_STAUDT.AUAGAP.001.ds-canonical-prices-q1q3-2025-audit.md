<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-22-auagap-001-prices-audit</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-22</date>
    <status>active</status>
    <project_code>ADVI_STAUDT</project_code>
    <urgency>URGENT — Andrew watching. Preliminary findings target: 1-2 hours.</urgency>
  </metadata>

  <objective>
    Audit canonical_prices per-ticker for Q1-Q3 2025. Flag any ticker whose median price
    in this window is less than 70% of Q4 2024 OR Q4 2025 median. This tests
    Hypothesis A: systematic price underestimation causing uniform AUA suppression.
    Output: data/black_diamond/diagnostics/aua25q_price_coverage.md
  </objective>

  <context>
    Andrew flagged: 49F portal AUA chart (quarterly view) shows ~70% drop for Q1-Q3 2025
    (Q4 2024 ~$1.4B normal → Q1 2025 ~$300M → Q3 2025 low → Q4 2025 recovers to ~$1.4B).
    Both New and Existing client segments affected proportionally = uniform suppression,
    rules out filter/classification bugs. CTO Hypothesis A: canonical_prices has systematic
    underestimation for Q1-Q3 2025 (bad yahoo backfill, cents/dollars unit flip,
    T3/T4 interpolation pulling stale values).

    Also audit scoped_overrides — recent commits d45fc0dc + 178d0cce touched canonical_prices.
    Did inject_scoped_overrides wipe price overrides for this range?

    DO NOT attempt fixes. Diagnostic only. MCP CTO + COO when smoking gun found.
  </context>

  <spec>
    Source: silver/prices/canonical_prices.parquet (S3: s3://opal-data-bd/silver/prices/)
    Window: 2025-01-01 through 2025-09-30
    Baseline: Q4 2024 (2024-10-01 through 2024-12-31) and Q4 2025 (2025-10-01 through 2025-12-31)

    Analysis:
    1. Per-ticker per-month: count non-null prices vs expected trading days for Q1-Q3 2025.
       Flag any ticker with >20% missing days in any month of the window.
    2. Per-ticker: compute median(price) for Q1-Q3 2025, Q4 2024, Q4 2025.
       Flag any ticker where Q1-Q3 2025 median is less than 70% of Q4 2024 OR Q4 2025 median.
    3. Cross-check silver/historical_prices.parquet (yahoo source) for same window —
       is the underlying data missing there too, or is the T2-merge dropping it?
    4. Check silver/prices/scoped_overrides.parquet — any rows with dates in Q1-Q3 2025
       that may have been wiped by a recent inject_scoped_overrides.py run.
       Reference commits: d45fc0dc + 178d0cce.

    Output: data/black_diamond/diagnostics/aua25q_price_coverage.md
    Content: top-20 worst-covered tickers (ticker, month, pct_covered, median_q1q3,
    median_q42024, median_q42025, ratio_vs_q42024). Summary line: HYP A CONFIRMED or
    HYP A NOT ROOT CAUSE with supporting evidence.
  </spec>

  <acceptance_criteria>
    1. canonical_prices queried for full Q1-Q3 2025 window.
    2. Per-ticker price coverage + median price delta computed vs both baseline windows.
    3. Flag list: tickers with median <70% of Q4 2024 or Q4 2025 baseline.
    4. Yahoo source cross-check completed.
    5. Scoped overrides checked for Q1-Q3 2025 range.
    6. Output file committed: data/black_diamond/diagnostics/aua25q_price_coverage.md.
    7. MCP CTO + COO with findings. Include HYP A verdict.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT attempt fixes. Diagnostic only.</rule>
    <rule>Do NOT run pipeline scripts — S3 query only.</rule>
    <rule>Do NOT wait for AUAGAP.002 or .003 before reporting if you find a clear smoking gun.</rule>
  </do_not>
</task_order>
