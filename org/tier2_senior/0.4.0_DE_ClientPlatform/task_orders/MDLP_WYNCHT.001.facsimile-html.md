<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-11-facsimile-html</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-11</date>
    <status>complete</status>
  </metadata>

  <objective>
    Duplicate the Model Portfolios benchmark tab as a standalone HTML file with all
    data hardcoded from the reference CSV. This is a static clone of the existing page
    for screenshot capture — not a dynamic tool. Keep it excessively simple.
  </objective>

  <scope>
    <files>
      <file action="create">tools/wyncht/facsimile.html</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Single HTML file at tools/wyncht/facsimile.html. All CSS and JS inline.
      Open it in a browser, it looks like the portal benchmark tab. That's it.
    </requirement>

    <requirement id="2">
      Hardcode ALL data values directly from model_portfolio_return_vol_20260227.csv
      (at repo root). 5 models x 9 periods x 6 values. No JSON loading, no file picker,
      no dynamic data. Just paste the numbers into the HTML/JS.
    </requirement>

    <requirement id="3">
      Component 1 — Return vs Volatility Scatter Chart:
      Duplicate portal/src/components/ReturnVolatilityScatter.tsx visually.
      - Can use Chart.js via CDN, inline SVG, or plain canvas — whatever is simplest
      - X=Volatility, Y=Return, circles for models, diamonds for benchmarks
      - Model colors: UST=#f97316, ST=#f59e0b, INT=#10b981, LTC=#3b82f6, LTA=#ef4444
      - Period toggle buttons (9 periods), default YTD
      - Legend with model names and shape key
    </requirement>

    <requirement id="4">
      Component 2 — Benchmark Heatmap:
      Duplicate portal/src/components/BenchmarkHeatmap.tsx visually.
      - HTML table or CSS grid, 3 rows per model (Model / Benchmark / Spread)
      - Green text positive, red text negative
      - Green/red/yellow background on spread cells
      - Model color left border and name styling
      - Format: +X.XX% / -X.XX%
    </requirement>

    <requirement id="5">
      Index/ETF toggle switches between Index and ETF benchmark values (both sets
      are in the CSV — hardcode both, toggle switches which set is displayed).
      Default: Index.
    </requirement>

    <requirement id="6">
      Gross/Net toggle. Net formula: net = gross - (trading_days/252) * 0.36.
      Fixed day counts: 1D=1, 1M=21, 1Q=63, 1Y=252, SI=252.
      To-date: WTD/MTD/QTD/YTD count weekdays from period start to 2026-02-27.
      Net applies to model and spread rows only. Default: Gross.
    </requirement>

    <requirement id="7">
      Dark theme: page bg #0f1724, panel bg #131d2e, white text, dark borders.
      Match the portal's look closely enough for screenshot use.
    </requirement>

    <requirement id="8">
      Show "Data as of: 2026-02-27" somewhere visible.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Open facsimile.html in Chrome — looks like the portal benchmark tab</criterion>
    <criterion id="2">Numbers match the reference CSV</criterion>
    <criterion id="3">Index/ETF and Gross/Net toggles work</criterion>
    <criterion id="4">Period toggle on scatter chart works</criterion>
    <criterion id="5">Screenshot-ready — dark theme, correct colors, no broken layout</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify any file in portal/</constraint>
    <constraint>Keep it simple — this is a static page clone, not a dynamic application</constraint>
    <constraint>No npm/bun/build steps</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" task="none" status="n/a"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">tools/wyncht/facsimile.html</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/MDLP_WYNCHT_PRD.md</ref>
    <ref type="component">portal/src/components/ReturnVolatilityScatter.tsx</ref>
    <ref type="component">portal/src/components/BenchmarkHeatmap.tsx</ref>
    <ref type="component">portal/src/pages/ModelPortfolios.tsx (lines 1440-1548)</ref>
    <ref type="colors">portal/src/lib/modelPortfolioColors.ts</ref>
    <ref type="data">model_portfolio_return_vol_20260227.csv (hardcode these values)</ref>
  </references>
</task_order>
