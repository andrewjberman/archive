<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-23-debt-1strun-001-coo</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>2.0.0_SA_COO</issued_to>
    <date>2026-03-23</date>
    <status>complete</status>
    <!-- Completed 2026-04-08. Pod aggregate reports compiled by reassigned RDs during session 19. All 4 pod reports delivered. -->
    <project_code>DEBT_1STRUN</project_code>
  </metadata>

  <objective>
    Collect the 5 aggregate reports (4 DE pod reports + 1 AE infrastructure
    report) and produce a final org-wide technical debt synthesis for CTO
    and Andrew. This is the decision document for issuing targeted .002+
    cleanup task orders.
  </objective>

  <scope>
    <files>
      <file action="aggregate">org/tier2_senior/0.1.0_DE_MarketIntelligence/logs/2026-03-23/debt_1strun_pod_aggregate.md</file>
      <file action="aggregate">org/tier2_senior/0.2.0_DE_PortfolioAnalytics/logs/2026-03-23/debt_1strun_pod_aggregate.md</file>
      <file action="aggregate">org/tier2_senior/0.3.0_DE_TradingOperations/logs/2026-03-23/debt_1strun_pod_aggregate.md</file>
      <file action="aggregate">org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-03-23/debt_1strun_pod_aggregate.md</file>
      <file action="aggregate">org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-03-23/debt_1strun_infra_aggregate.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Collect all 5 aggregate reports. If any are missing, note as PENDING
      and proceed with available data.
    </requirement>

    <requirement id="2">
      Produce the final synthesis at:
        org/tier1_exec/2.0.0_SA_COO/deliverables/debt_1strun_synthesis.md

      Structure:
        # DEBT_1STRUN — Org-Wide Technical Debt Synthesis

        ## Executive Summary
        Total findings across all pods and infrastructure.
        Top 5 org-wide themes (patterns that appear across multiple pods).

        ## Cross-Pod Patterns
        Debt that spans pods — e.g., all 4 pods have the same hardcoded
        bucket name pattern, or 3 pods duplicate the same fetch utility.
        These are the highest-value cleanup targets because one fix
        benefits everyone.

        ## Pod-by-Pod Summary
        For each pod: finding count, top 3 items, estimated effort.

        ## Infrastructure Summary
        AE findings: orphaned resources, Terraform drift, stale layers.

        ## Recommended .002 Task Orders
        Prioritized list of cleanup task orders to issue, with:
        - Target agent(s)
        - Scope (specific files/functions)
        - Estimated effort (quick/moderate/significant)
        - Why it matters (blast radius if left unfixed)

        ## Parking Lot
        Low-priority items that can wait for future sweeps.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All available aggregate reports collected and synthesized</criterion>
    <criterion id="2">Cross-pod patterns identified and ranked</criterion>
    <criterion id="3">Recommended .002 task orders with agent assignment and effort estimates</criterion>
    <criterion id="4">Synthesis document written to deliverables/debt_1strun_synthesis.md</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not issue .002 task orders yourself — present recommendations to CTO + Andrew for decision</constraint>
    <constraint>Wait for aggregate reports. If after reasonable time some are missing, synthesize what you have and note gaps.</constraint>
    <constraint>Focus on cross-pod patterns — these have the highest ROI for cleanup.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="document">deliverables/debt_1strun_synthesis.md — the decision document</deliverable>
  </deliverables>
</task_order>
