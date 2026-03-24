<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-23-debt-1strun-001-0.3.0_de_tradingoperations</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-03-23</date>
    <status>pending</status>
    <project_code>DEBT_1STRUN</project_code>
  </metadata>

  <objective>
    DUAL ROLE: (1) Scan your own domain (portal shared components, API wiring,
    types used by your pod's pages) for technical debt. (2) Aggregate the scan
    findings from your pod's DS and RD agents into a single pod-level report
    for COO.
  </objective>

  <scope>
    <files>
      <file action="scan">portal/src/ (shared components, hooks, utilities, types used by Pod 3 — PortfolioManagement, TradeSubmission, DataRefresh, SecurityScanner pages)</file>
      <file action="scan">API endpoint wiring for smartx/portfolio-mgmt/data-refresh pipelines</file>
      <file action="aggregate">org/tier2_senior/0.3.0_DS_TradingOperations/logs/2026-03-23/debt_1strun_scan.md</file>
      <file action="aggregate">org/tier3_junior/0.3.1_RD_PortfolioManagement/logs/2026-03-23/debt_1strun_scan.md</file>
      <file action="aggregate">org/tier3_junior/0.3.2_RD_TradeSubmission/logs/2026-03-23/debt_1strun_scan.md</file>
      <file action="aggregate">org/tier3_junior/0.3.3_RD_DataRefresh/logs/2026-03-23/debt_1strun_scan.md</file>
      <file action="aggregate">org/tier3_junior/0.3.4_RD_SecurityScanner/logs/2026-03-23/debt_1strun_scan.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      PART 1 — YOUR OWN SCAN: Scan portal shared infrastructure used by your
      pod for the following 6 categories. Focus on cross-page shared components,
      API endpoint definitions, TypeScript type files, shared hooks, and utility
      functions that your pod's pages depend on.

      CATEGORIES:

      C1 - DEAD CODE
      Unused exports in shared type files. API endpoint functions defined but
      never called by any page. Shared components imported nowhere. Hook
      functions that no page uses. Dead routes in routing config.

      C2 - DEPRECATED / SUPERSEDED
      Old type definitions kept for backwards compatibility. Legacy API
      endpoint wiring that points to routes the Lambda no longer serves.
      Deprecated utility functions replaced by newer versions. Types that
      no longer match the actual Lambda response shape.

      C3 - DUPLICATION / DRIFT RISK
      Same fetch pattern implemented in multiple pages instead of a shared
      hook. Type definitions that duplicate or shadow each other. Inline
      data transformations that should be shared utilities. Multiple pages
      implementing the same chart/table component slightly differently.

      C4 - HARDCODED CONFIGURATION
      Hardcoded API base URLs. Magic numbers for pagination, timeouts,
      retry counts. Inline color values that should reference theme tokens.
      Hardcoded feature flags or environment checks.

      C5 - ORPHANED INFRASTRUCTURE
      Routes in the router that lead to empty or placeholder pages. Lazy
      chunks that are never navigated to. API hooks defined but unused.
      Context providers wrapping components that don't consume the context.

      C6 - STALE ERROR HANDLING
      Generic error boundaries with no actionable messages. Fetch calls
      with no error handling. Loading states that never resolve on error.
      Error messages referencing old data field names.
    </requirement>

    <requirement id="2">
      PART 2 — AGGREGATION: After completing your own scan AND after your pod's
      DS and RD agents have completed their scans, collect their findings from:

      - org/tier2_senior/0.3.0_DS_TradingOperations/logs/2026-03-23/debt_1strun_scan.md
      - org/tier3_junior/0.3.1_RD_PortfolioManagement/logs/2026-03-23/debt_1strun_scan.md
      - org/tier3_junior/0.3.2_RD_TradeSubmission/logs/2026-03-23/debt_1strun_scan.md
      - org/tier3_junior/0.3.3_RD_DataRefresh/logs/2026-03-23/debt_1strun_scan.md
      - org/tier3_junior/0.3.4_RD_SecurityScanner/logs/2026-03-23/debt_1strun_scan.md

      Produce an aggregate pod report at:
        org/tier2_senior/0.3.0_DE_TradingOperations/logs/2026-03-23/debt_1strun_pod_aggregate.md

      The aggregate report must:
      (a) Include your own findings
      (b) Include all DS and RD findings
      (c) Deduplicate — if DS and RD both found the same issue from different
          angles (e.g., DS found a dead Lambda endpoint, RD found the dead
          frontend call to it), merge into one finding noting both perspectives
      (d) Cross-reference — flag cases where a DS finding implies an RD issue
          or vice versa (e.g., DS found a deprecated data shape that RD is
          still consuming)
      (e) Rank the top 10 pod debt items by severity and blast radius
      (f) Categorize findings as QUICK WIN (< 1 hour fix), MODERATE (1-4 hours),
          or SIGNIFICANT (> 4 hours / requires coordination)

      This aggregate report goes to 2.0.0_SA_COO.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Own scan covers all 6 categories — none skipped</criterion>
    <criterion id="2">Every finding has file path, line numbers, category, severity, and description</criterion>
    <criterion id="3">Own scan log written to logs/2026-03-23/debt_1strun_scan.md</criterion>
    <criterion id="4">Aggregate pod report written to logs/2026-03-23/debt_1strun_pod_aggregate.md</criterion>
    <criterion id="5">Aggregate includes all DS + RD findings, deduplicated and cross-referenced</criterion>
    <criterion id="6">Top 10 ranked findings with effort estimates (quick/moderate/significant)</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not fix anything — this is a scan-only task. Fixes come in .002+ task orders.</constraint>
    <constraint>Wait for DS and RD scan logs before producing the aggregate. If any are missing after reasonable time, note them as PENDING in the aggregate and proceed with what you have.</constraint>
    <constraint>Report the aggregate to 2.0.0_SA_COO.</constraint>
    <constraint>Be concrete: name files, line numbers, function names. No vague findings.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="document">logs/2026-03-23/debt_1strun_scan.md (your own findings)</deliverable>
    <deliverable type="document">logs/2026-03-23/debt_1strun_pod_aggregate.md (pod-level aggregate for COO)</deliverable>
  </deliverables>
</task_order>
