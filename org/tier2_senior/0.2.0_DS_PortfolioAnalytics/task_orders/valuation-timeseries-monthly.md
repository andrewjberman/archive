<task_order>
  <metadata>
    <id>adhc-valuation-timeseries-monthly-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
    <date>2026-03-31</date>
    <status>complete</status>
  </metadata>

  <objective>
    Change the yang-generate-valuation Lambda to emit monthly data points instead of
    semi-annual. The valuation time series chart on the portal currently shows H1/H2
    labels because the backend downsamples monthly data to every 6th row. Yang has
    requested monthly granularity.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/v2_portal/yang_pipeline/valuation/yang-generate-valuation/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      In `generate_time_series()` (line 233), change the default `sample_months`
      parameter from `6` to `1`. This removes the downsampling that skips 5 of
      every 6 monthly data points.

      Before: `def generate_time_series(df: pd.DataFrame, sample_months: int = 6) -> dict:`
      After:  `def generate_time_series(df: pd.DataFrame, sample_months: int = 1) -> dict:`

      The sampling logic on line 255 (`sampled = index_data.iloc[::sample_months]`)
      stays unchanged -- with sample_months=1, it passes through all rows.
    </requirement>

    <requirement id="2">
      Verify the output JSON size is acceptable. With monthly data going back to ~1989,
      the S&P 500 trailing_pe series will go from ~70 data points (semi-annual) to
      ~420 (monthly). Three indices x three metrics = ~3,780 data points total. This
      should be well under 1MB and fine for the Lambda response and S3 storage.
    </requirement>

    <requirement id="3">
      Update the docstring for `generate_time_series()` to reflect monthly output.
      Remove the "sample_months" comment referencing semi-annual sampling.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">generate_time_series() outputs all monthly data points (no downsampling)</criterion>
    <criterion id="2">Output JSON validates -- same structure, more data points per series</criterion>
    <criterion id="3">Thresholds (percentiles) still calculated from the full dataset (line 256), not the sampled subset -- verify this is unchanged</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT change the threshold calculation -- it already uses the full unsampled index_data (line 256). Only the series output changes.</constraint>
    <constraint>Commit to CLOUD. Do not deploy -- DT handles the Lambda deploy.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.2.4_RD_Valuation" task="frontend-monthly-labels" status="pending">Frontend tick formatter change (independent, can proceed in parallel)</dependency>
  </dependencies>

  <deliverables>
    <deliverable type="code">Modified lambda_function.py with sample_months=1</deliverable>
  </deliverables>
</task_order>
