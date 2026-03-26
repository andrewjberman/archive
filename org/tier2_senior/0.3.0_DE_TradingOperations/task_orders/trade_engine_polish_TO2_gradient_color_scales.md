# Task Order: Trade Engine Visual Polish — TO-2: Gradient Color Scales

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-trade-polish-to2</id>
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
    Apply continuous gradient background color scales to Model tab (items 6) and Trade tab
    (items 8, 9). Adds initialBet gradient and a new derived finalBet column. Pattern is
    getGradientBackground already used by PortfolioGrid.tsx (lines 466-516).
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/ModelTab.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/components/PortfolioGrid.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      PRD Item 6 — Model tab (ModelTab.tsx):
      Apply continuous gradient to Coefficient and Weight columns.
      Scale: white (low) to green (high) — same direction as positive values = good.
      Reuse getGradientBackground from PortfolioGrid.tsx. If not currently importable,
      extract it to a shared util (e.g., portal/src/pages/PortfolioManagement/utils/colorUtils.ts)
      and update both files to import from there.
    </requirement>
    <requirement id="2">
      PRD Item 8 — Trade tab (PortfolioGrid.tsx): apply gradient to totalRisk and specRisk columns.
      Scale: INVERTED — green (low risk) to red (high risk). Higher value = more red.
      getGradientBackground likely needs an invert flag or a separate inverted-gradient call.
      Read the existing implementation (lines 466-516) before implementing.
    </requirement>
    <requirement id="3">
      PRD Item 9a — Trade tab: apply same gradient as optimizedBet to initialBet column.
      optimizedBet already has the full red-yellow-green gradient via getGradientBackground.
      initialBet currently shows black text with no gradient. Apply the same treatment.
    </requirement>
    <requirement id="4">
      PRD Item 9b — Trade tab: add new finalBet column.
      finalBet = finalWeight - benchmarkWeight (derived client-side, same pattern as finalTrade).
      Place finalBet adjacent to optimizedBet and initialBet in column order.
      Apply the same gradient coloring as optimizedBet and initialBet.
      Use a valueGetter (not a data field) to compute finalBet from finalWeight and benchmarkWeight.
    </requirement>
    <requirement id="5">
      bunx tsc -b must pass clean after all changes.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Model tab Coefficient and Weight cells show white-to-green gradient backgrounds.</criterion>
    <criterion id="2">Trade tab totalRisk and specRisk cells show green-to-red (inverted) gradient.</criterion>
    <criterion id="3">initialBet has same gradient treatment as optimizedBet.</criterion>
    <criterion id="4">finalBet column present, positioned adjacent to initialBet/optimizedBet, gradient applied, value = finalWeight - benchmarkWeight.</criterion>
    <criterion id="5">No TypeScript errors. getGradientBackground is either still in place or cleanly refactored to a shared util used by both callers.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Read getGradientBackground (PortfolioGrid.tsx lines 466-516) before writing any gradient code. Do not duplicate the logic; import or extract it.</constraint>
    <constraint>finalBet is a derived field only — do not add it to any TypeScript interface or data contract. It is computed in the valueGetter at render time.</constraint>
    <constraint>No Lambda, Terraform, or API changes. This is pure frontend.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal DEV commit(s) with items 6, 8, 9 complete</deliverable>
    <deliverable type="document">Session log with commit hashes and tsc confirmation</deliverable>
  </deliverables>
</task_order>
```
