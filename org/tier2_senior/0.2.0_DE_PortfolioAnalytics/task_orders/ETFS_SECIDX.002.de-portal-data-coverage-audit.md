<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-06-etfs-secidx-002-de</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.0_DE_PortfolioAnalytics</issued_to>
    <date>2026-04-06</date>
    <status>complete</status>
    <project_code>ETFS_SECIDX</project_code>
  </metadata>

  <objective>
    Audit the portal's current securities and index data coverage. Map every ticker,
    index, and benchmark the portal currently serves — where it comes from, what
    pages use it, and what API endpoints deliver it. This is the portal-side half
    of the gap analysis (DS .001 covers the dashboard side).
  </objective>

  <scope>
    <files>
      <file action="read">portal/src/lib/tickerRegistry.ts</file>
      <file action="read">portal/src/pages/Positioning/constants/etf-categories.ts</file>
      <file action="read">portal/src/pages/MarketPerformance/</file>
      <file action="read">portal/src/pages/Positioning/</file>
      <file action="read">portal/src/pages/Attribution/</file>
      <file action="read">infra/aws/lambda/v2_portal/yang_pipeline/positioning/</file>
      <file action="read">infra/aws/lambda/v2_portal/market_overview/</file>
      <file action="write">data/etf_dashboards/portal_coverage_audit.json</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="portal_audit">
      **Portal Data Coverage Audit** (portal_coverage_audit.json)

      For every ticker/index/benchmark currently in the portal, record:

      - ticker: Symbol as used in portal code
      - full_name: Human-readable name
      - pages: Array of portal pages that display this ticker (MarketPerformance, Positioning, Attribution, etc.)
      - data_source: Which Lambda/pipeline serves it (yang-pipeline, market-overview, news, etc.)
      - api_endpoint: The API path that delivers the data
      - fields_served: What data fields the portal currently renders (price, return, weight, etc.)
      - etf_relevant: Boolean — is this ticker in any of the 4 Opal ETF holdings or benchmarks?

      Also produce a summary section:
      - total_tickers: Count of unique tickers in portal
      - total_etf_overlap: Count that overlap with ETF dashboard securities
      - gaps: Tickers in ETF dashboards not in portal (leave empty — DS .001 fills this)
      - excess: Tickers in portal not in any ETF dashboard
    </deliverable>
  </deliverables>

  <notes>
    - Focus on the data layer, not the UI components. What tickers does the portal
      KNOW about, and through what pipelines?
    - Check tickerRegistry.ts as the primary source, but also scan page-specific
      constants files and Lambda handler configs for tickers not in the registry.
    - The yang-pipeline positioning Lambdas and market-overview Lambdas are the
      main data sources — check their configs for ticker lists.
  </notes>

  <references>
    <ref type="prd">docs/architecture/ETFS_SECIDX_PRD.md</ref>
  </references>

  <dependencies>
    None. Can run in parallel with DS .001.
  </dependencies>
</task_order>
