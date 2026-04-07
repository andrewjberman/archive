# ADVI_REBORN.W2-002 — DS: Add QTD/1Y/3Y windows to fee efficiency scorecard

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-07-reborn-w2-002-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <project_code>ADVI_REBORN</project_code>
    <priority>high</priority>
    <phase>WS2</phase>
  </metadata>

  <objective>
    Expand C_08's advisor_fee_efficiency.json scorecard to include multiple
    time windows (QTD, YTD, 1Y, 3Y, Max). Currently it only produces
    trailing_12m and YTD. The Books N1 fee efficiency scatter plot and advisor
    list need to be interval-aware — when the user toggles the period selector,
    the scatter dots, regression line, and advisor metrics all change.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_NNAFEE_FEE_EFFICIENCY_VIEWS.md</ref>
    <ref type="design-note">org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI_NNAFEE.007.design-note-interval-aware-advisor-list.md</ref>
  </references>

  <context>
    Current scorecard shape (advisor_fee_efficiency.json):
    - Top-level: as_of_date, regression (single), advisors[] (single window)
    - Each advisor: implied_revenue_ytd, implied_revenue_trailing_12m, nna_ytd, nna_trailing_12m, etc.

    Needed shape — windowed like employee_leaderboard.json:
    - windows: { qtd: { regression, advisors[] }, ytd: { ... }, trailing_1y: { ... }, trailing_3y: { ... }, max: { ... } }
    - Each window computes its own regression (slope, intercept, R^2) from that period's data
    - Each advisor entry within a window has period-specific: implied_revenue, nna, growth, efficiency_ratio, fee_yield_bps, regression_residual

    The fee_detail parquet has daily data going back years — windowing is a filter on date range before aggregation.
  </context>

  <requirements>
    <requirement id="1">Add windowed structure to advisor_fee_efficiency.json matching employee_leaderboard.json pattern:
```json
{
  "as_of_date": "2026-04-07",
  "windows": {
    "qtd": {
      "regression": { "slope": ..., "intercept": ..., "r_squared": ..., "n_advisors": ... },
      "advisors": [{ "advisor": ..., "roles": [...], ... }]
    },
    "ytd": { ... },
    "trailing_1y": { ... },
    "trailing_3y": { ... },
    "max": { ... }
  }
}
```
    </requirement>
    <requirement id="2">Each window computes its own regression from that period's fee/NNA data — not just the same regression with different advisor metrics.</requirement>
    <requirement id="3">Keep backward compatibility: include a top-level `regression` and `advisors` array that mirrors the `trailing_1y` window (existing consumers won't break).</requirement>
    <requirement id="4">Window date ranges:
      - QTD: current quarter start to as_of_date
      - YTD: Jan 1 to as_of_date
      - trailing_1y: as_of_date minus 365 days
      - trailing_3y: as_of_date minus 1095 days
      - max: all available data</requirement>
    <requirement id="5">Commit and verify output. Spot-check that regression R^2 differs across windows (it should — different time horizons produce different fits).</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">JSON has windows object with qtd/ytd/trailing_1y/trailing_3y/max</criterion>
    <criterion id="2">Each window has its own regression + advisors array</criterion>
    <criterion id="3">Top-level regression + advisors still present (backward compat)</criterion>
    <criterion id="4">R^2 values differ across windows</criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency>None — C_08 already has the daily fee_detail data. This is a computation change.</dependency>
  </dependencies>

  <commit_pattern>feat(C_08): add windowed fee efficiency scorecard (QTD/YTD/1Y/3Y/Max)</commit_pattern>
</task_order>
