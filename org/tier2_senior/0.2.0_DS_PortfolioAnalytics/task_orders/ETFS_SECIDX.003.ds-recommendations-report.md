<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-06-etfs-secidx-003-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
    <date>2026-04-06</date>
    <status>complete</status>
    <project_code>ETFS_SECIDX</project_code>
  </metadata>

  <objective>
    Synthesize DS .001 (securities/index inventory + data source mapping) and
    DE .002 (portal coverage audit) into a unified gap analysis and recommendations
    report. This is PRD deliverable D4.
  </objective>

  <scope>
    <files>
      <file action="read">data/etf_dashboards/securities_inventory.json</file>
      <file action="read">data/etf_dashboards/index_benchmark_inventory.json</file>
      <file action="read">data/etf_dashboards/data_source_mapping.json</file>
      <file action="read">data/etf_dashboards/portal_coverage_audit.json</file>
      <file action="write">data/etf_dashboards/ETFS_SECIDX_recommendations.md</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="D4">
      **Recommendations Report** (ETFS_SECIDX_recommendations.md)

      Structured report containing:

      1. **Gap Summary**: Securities/indices in ETF dashboards but NOT in portal.
         Count, list, and categorize by: new equities, new indices, new data fields.

      2. **Existing Infrastructure Reuse**: Which gaps can be served by extending
         existing pipelines (yang-pipeline, market-overview, news) vs requiring
         entirely new data sources. For each, specify the pipeline and what change
         is needed (add ticker to config, add new Lambda, new data feed).

      3. **New Pipeline Needs**: Securities/fields that require new data sources
         (Bloomberg API, FactSet API, new scrapers). Estimate complexity (config
         change vs new Lambda vs new external integration).

      4. **Proposed Portal Page Structure**: Recommend page layout for ETF Operations
         surface area. Based on what the Bloomberg dashboards contain: holdings,
         performance attribution, trade analysis, screening, dividend calendar.
         Map each proposed page to required data sources.

      5. **Priority Ordering**: Rank Phase 1 implementation items by:
         - Value (what Andrew uses most in the Bloomberg dashboards)
         - Feasibility (what can be served from existing infrastructure)
         - Dependencies (what requires new external data feeds)
    </deliverable>
  </deliverables>

  <notes>
    - This is a planning document, not code. The output informs the CTO's Phase 1 PRD.
    - Be specific about pipeline extensions — name the Lambda, the config file, the
      ticker list that needs updating. Generic "extend yang pipeline" is not useful.
    - If PFDE holdings have been provided by the time you run this, include them.
      If not, note PFDE as a gap with unknown scope.
  </notes>

  <references>
    <ref type="prd">docs/architecture/ETFS_SECIDX_PRD.md</ref>
    <ref type="dependency">.001 DS securities/index inventory</ref>
    <ref type="dependency">.002 DE portal coverage audit</ref>
  </references>

  <dependencies>
    <dependency agent="0.2.0_DS_PortfolioAnalytics"
                task="ETFS_SECIDX.001"
                status="pending"/>
    <dependency agent="0.2.0_DE_PortfolioAnalytics"
                task="ETFS_SECIDX.002"
                status="pending"/>
  </dependencies>
</task_order>
