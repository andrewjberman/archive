<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-06-etfs-secidx-001-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
    <date>2026-04-06</date>
    <status>complete</status>
    <project_code>ETFS_SECIDX</project_code>
  </metadata>

  <objective>
    Parse the 3 ETF Bloomberg/FactSet dashboards (DIVZ, IDVZ, PFOE) and produce
    a comprehensive, deduplicated securities + index inventory with data source mapping.
    Covers PRD deliverables D1, D2, and D3.
  </objective>

  <scope>
    <files>
      <file action="read">data/etf_dashboards/DIVZ Dashboard 2026 02 18_v1.xlsx</file>
      <file action="read">data/etf_dashboards/IDVZ Dashboard 2026 02 18_v1.xlsx</file>
      <file action="read">data/etf_dashboards/PFOE Dashboard 2026 02 18_v1.xlsx</file>
      <file action="read">portal/src/lib/tickerRegistry.ts</file>
      <file action="read">portal/src/pages/Positioning/constants/etf-categories.ts</file>
      <file action="read">portal/src/pages/MarketPerformance/</file>
      <file action="read">infra/aws/lambda/v2_portal/yang_pipeline/positioning/</file>
      <file action="write">data/etf_dashboards/securities_inventory.json</file>
      <file action="write">data/etf_dashboards/index_benchmark_inventory.json</file>
      <file action="write">data/etf_dashboards/data_source_mapping.json</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="D1">
      **Securities Inventory** (securities_inventory.json)

      Parse each dashboard's holdings sheets (Main, Top Holdings, Actual Holdings/TruShares).
      Extract every unique security with these fields:

      - ticker: Bloomberg ticker (e.g., "GS US EQUITY")
      - us_ticker: US-listed ticker (e.g., "GS")
      - adr_ticker: ADR ticker if applicable (IDVZ international holdings)
      - name: Company name
      - country: Country of domicile
      - sector: GICS sector
      - etfs: Array of which ETF(s) hold this security
      - model_weight: Target weight per ETF (from model weight column)
      - asset_class: Equity, Fixed Income, Commodity

      Deduplicate across ETFs. Flag securities held by multiple funds.
    </deliverable>

    <deliverable id="D2">
      **Index and Benchmark Inventory** (index_benchmark_inventory.json)

      Enumerate all indices and benchmarks referenced across:
      - ETF dashboard performance sheets (SPX, MXWD, M1WDUDY, RLG, Bloomberg Agg, etc.)
      - ETF dashboard screening universes
      - Portal tickerRegistry.ts
      - Portal MarketPerformance page config
      - Yang pipeline positioning constants

      For each index, record: ticker, full name, source (dashboard/portal/both),
      which ETFs reference it, whether portal currently serves it.

      Identify overlaps (in both dashboard + portal) and gaps (dashboard only or portal only).
    </deliverable>

    <deliverable id="D3">
      **Data Source Mapping** (data_source_mapping.json)

      For each security and index in D1+D2, map:
      - current_source: Where data comes from today (Bloomberg terminal, FactSet, FRED, Yahoo Finance, yang-pipeline, custom)
      - fields_needed: What data fields the dashboards use (price, return, dividend, EPS, P/E, ROE, EV, div yield, etc.)
      - refresh_frequency: Real-time, daily, or weekly
      - portal_coverage: Whether an existing pipeline already serves this data
      - pipeline_name: If covered, which pipeline (yang, market-overview, news, bd)
    </deliverable>
  </deliverables>

  <notes>
    - PFDE holdings are NOT in the zip. Proceed with DIVZ/IDVZ/PFOE. PFDE will be
      added when Andrew provides the data.
    - Each dashboard has multiple sheets (holdings, performance, screening, trade analysis,
      FX impact, dividend calendar). Parse ALL sheets — not just the main holdings.
    - IDVZ has international securities with ADR tickers — capture both local and ADR.
    - Output JSON files to data/etf_dashboards/. Use arrays of objects, not nested dicts.
    - Cross-reference against portal/src/lib/tickerRegistry.ts for portal coverage check.
  </notes>

  <references>
    <ref type="prd">docs/architecture/ETFS_SECIDX_PRD.md</ref>
  </references>

  <dependencies>
    None. Can begin immediately on GO.
  </dependencies>
</task_order>
