# Task Order: Trade Engine Visual Polish — TO-1: Threshold Highlighting

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-trade-polish-to1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-03-04</date>
    <status>complete</status>
    <!-- CTO audit 2026-03-26: All 13 PFMG_VISPOL items delivered by outside consultant prior to agent system. Project closed 2026-03-10. -->
  </metadata>

  <references>
    <ref type="prd">docs/architecture/TRADE_ENGINE_VISUAL_POLISH.md</ref>
    <ref type="cto-handoff">org/tier1_exec/1.0.0_SA_CTO/deliverables/coo_handoff_trade_engine_visual_polish.md</ref>
  </references>

  <objective>
    Apply threshold-based conditional text coloring to Risk Decomposition, Alpha tab, and Sector tab
    columns. Covers PRD items 2, 3, 4, and 5. All changes are cosmetic — no data contract changes,
    no API changes. Route to 0.3.1_RD_PortfolioManagement or handle directly.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/PortfolioManagement/components/OptimizationSummaryHeader.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/AlphaTab.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/SectorTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      PRD Item 2 — Risk Decomposition Exposure columns (OptimizationSummaryHeader.tsx lines 359-367):
        Initial Exposure:   green if > 0.1,  red if &lt; -0.1, neutral otherwise
        Optimized Exposure: green if > 0.1,  red if &lt; -0.1, neutral otherwise
        Trade (Exposure):   green if > 0.05, red if &lt; -0.05, neutral otherwise
      Apply text color: hsl(var(--success)) for green, hsl(var(--danger)) for red,
      text-white/70 for neutral.
    </requirement>
    <requirement id="2">
      PRD Item 3 — Risk Decomposition Contribution columns (OptimizationSummaryHeader.tsx lines 373-381):
        Initial Contribution:   red if > 5, no green threshold (one-directional)
        Optimized Contribution: red if > 5, no green threshold (one-directional)
        Delta (Contribution):   green if &lt; -2 (reducing risk = good), red if > 2
      Same color tokens as above.
    </requirement>
    <requirement id="3">
      PRD Item 4 — Alpha tab (AlphaTab.tsx). Currently only Trade uses getTradeColor with +-0.01.
      Change ALL three columns (Initial Bet, Optimized Bet, Trade) to +-0.1 threshold:
        green if > 0.1, red if &lt; -0.1, neutral otherwise
      Apply in both the By Factor view (line 431, 434-438) and the By Group view (lines 278-282).
      Update or replace the getTradeColor function if it is hardcoded to +-0.01 for these columns.
    </requirement>
    <requirement id="4">
      PRD Item 5 — Sector tab (SectorTab.tsx). Currently Trade columns use +-0.01 threshold.
      New thresholds:
        Initial Bet:   green if > 2,   red if &lt; -2
        Optimized Bet: green if > 2,   red if &lt; -2
        Trade:         green if > 0.5, red if &lt; -0.5
    </requirement>
    <requirement id="5">
      bunx tsc -b must pass clean after all changes.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Risk Decomp table: Exposure and Contribution columns color per spec. Neutral band renders white/70.</criterion>
    <criterion id="2">Alpha tab By Factor + By Group: all three columns use +-0.1 thresholds. Old +-0.01 threshold replaced.</criterion>
    <criterion id="3">Sector tab: bet columns use +-2, trade column uses +-0.5.</criterion>
    <criterion id="4">No TypeScript errors. No regression on other PortfolioManagement tabs.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>No data contract changes. No new props through component boundaries if avoidable — these are purely local styling decisions.</constraint>
    <constraint>Reuse existing color token pattern (hsl(var(--success)), hsl(var(--danger))) that is already in use in the file. Do not introduce new CSS classes or Tailwind utilities that do not already exist in the portal.</constraint>
    <constraint>DT pushes portal DEV after DE reviews. DE must not signal DT push until DE has visually inspected the changes.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal DEV commit(s) with items 2-5 complete</deliverable>
    <deliverable type="document">Session log noting commit hashes and a brief confirmation that tsc passes</deliverable>
  </deliverables>
</task_order>
```
