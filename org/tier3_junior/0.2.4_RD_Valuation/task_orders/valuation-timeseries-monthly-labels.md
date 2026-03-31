<task_order>
  <metadata>
    <id>adhc-valuation-timeseries-monthly-rd</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.2.4_RD_Valuation</issued_to>
    <date>2026-03-31</date>
    <status>complete</status>
  </metadata>

  <objective>
    Update the Valuation Time Series chart to display monthly x-axis labels instead
    of H1/H2 semi-annual labels. The backend is being changed to emit monthly data
    points (DS task in parallel). The frontend must format and space the labels
    accordingly.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/Valuation/tabs/ValuationTimeSeriesTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Change the x-axis tick formatter (lines 324-331) from H1/H2 to monthly
      abbreviation format. Target format: "Jan '24", "Jul '25", etc.

      Current code:
      ```
      tickFormatter={(value) => {
        const date = new Date(value + 'T12:00:00')
        const year = date.getFullYear()
        const month = date.getMonth()
        const half = month < 6 ? 'H1' : 'H2'
        return `${year} ${half}`
      }}
      ```

      Replace with monthly formatting. Use short month names (Jan, Feb, Mar, ...)
      and two-digit year. Keep the `+ 'T12:00:00'` timezone guard.
    </requirement>

    <requirement id="2">
      Change the tooltip date formatter (lines 50-55, inside CustomTooltip) to
      match. Currently formats as "YYYY H1/H2" -- change to full month + year
      (e.g., "January 2024" or "Jan 2024").
    </requirement>

    <requirement id="3">
      Update the x-axis tick interval calculation (lines 200-212). The current
      comment says "Semi-annual data: ~2 points per year" and the intervals are
      tuned for that density. With monthly data (~12 points per year), the
      intervals need adjustment to avoid x-axis label crowding.

      Suggested intervals for monthly data:
      - 1Y window (~12 points): interval=1 or 2 (show every 2nd-3rd month)
      - 5Y window (~60 points): interval=5 (show ~every 6 months)
      - 10Y window (~120 points): interval=11 (show ~yearly)
      - 20Y window (~240 points): interval=23 (show ~every 2 years)
      - Max (~420 points): interval=47 (show ~every 4 years)

      Tune these so labels don't overlap. The exact values may need visual
      adjustment -- use your judgment for readability.
    </requirement>

    <requirement id="4">
      Update the comment on line 201 from "Semi-annual data: ~2 points per year"
      to "Monthly data: ~12 points per year".
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">X-axis shows monthly labels (e.g., "Jan '24") instead of "2024 H1"</criterion>
    <criterion id="2">Tooltip shows monthly date instead of H1/H2</criterion>
    <criterion id="3">Labels do not overlap or crowd at any time period setting (1Y, 5Y, 10Y, 20Y, Max)</criterion>
    <criterion id="4">Chart renders correctly with both old (semi-annual) and new (monthly) data -- the formatter should work regardless of data density</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Keep the `+ 'T12:00:00'` timezone guard on all date parsing -- this prevents UTC midnight from shifting dates backwards in EST.</constraint>
    <constraint>Do not change the chart type, colors, percentile bands, or any other visual element. Only the x-axis labels and tooltip date format.</constraint>
    <constraint>Commit to portal DEV branch.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.2.0_DS_PortfolioAnalytics" task="backend-monthly-data" status="pending">Backend emitting monthly data points (parallel -- frontend change works with both semi-annual and monthly data)</dependency>
  </dependencies>

  <deliverables>
    <deliverable type="code">Modified ValuationTimeSeriesTab.tsx with monthly formatting</deliverable>
  </deliverables>
</task_order>
