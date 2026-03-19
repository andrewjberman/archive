# Task Order: Trade Engine Visual Polish — TO-5: Reset Zero Button

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-trade-polish-to5</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-03-04</date>
    <status>pending</status>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/TRADE_ENGINE_VISUAL_POLISH.md</ref>
    <ref type="cto-handoff">org/tier1_exec/1.0.0_SA_CTO/deliverables/coo_handoff_trade_engine_visual_polish.md</ref>
  </references>

  <objective>
    Add "Reset Zero" button to the Trade tab button group. When clicked, sets finalTrade = 0 for
    ALL securities (hold everything as-is; propose no trades). Covers PRD item 12.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/TradeTab.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/PortfolioManagement.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Button placement: in TradeTab.tsx button group (line ~368), insert "Reset Zero" between
      "Reset All" and "Export". The button group currently has:
        Reset Selected | Reset All | Export | Submit
      After change:
        Reset Selected | Reset All | Reset Zero | Export | Submit
    </requirement>
    <requirement id="2">
      Button behavior — "Reset Zero":
      Sets finalTrade = 0 for ALL securities.
      Implementation: finalWeight = initialWeight for every security.
      This is the "hold everything" state — tell the optimizer to make no changes.
      This is DISTINCT from "Reset All" which sets finalWeight = optimizedWeight (optimizer's suggestion).
    </requirement>
    <requirement id="3">
      TradeTab.tsx: add onResetZero prop (callback, no arguments). Wire the button to call it.
      Match the pattern of the existing onResetAll prop — read TradeTab.tsx before implementing
      to confirm the exact prop signature pattern.
    </requirement>
    <requirement id="4">
      PortfolioManagement.tsx: implement handleResetZero. It should iterate over all securities
      in state and set each security's finalWeight to its initialWeight (and finalTrade to 0).
      Read PortfolioManagement.tsx and usePortfolioEditStore to understand the correct state
      mutation path before implementing. Do not assume — cite the state update mechanism.
    </requirement>
    <requirement id="5">
      bunx tsc -b must pass clean.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Reset Zero button appears in the correct position between Reset All and Export.</criterion>
    <criterion id="2">Clicking Reset Zero sets finalTrade = 0 for all securities and finalWeight = initialWeight for all securities.</criterion>
    <criterion id="3">Reset All still works correctly (finalWeight = optimizedWeight) — no regression.</criterion>
    <criterion id="4">No TypeScript errors.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Read TradeTab.tsx (around line 368) and PortfolioManagement.tsx BEFORE implementing. The existing button callbacks are the implementation pattern to follow.</constraint>
    <constraint>Do not use finalWeight = 0 — that would set holdings to zero. The correct operation is finalWeight = initialWeight (hold current positions).</constraint>
    <constraint>No backend changes, no API calls, no Lambda changes. Pure frontend state operation.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal DEV commit with item 12 complete</deliverable>
    <deliverable type="document">Session log with commit hash and tsc confirmation</deliverable>
  </deliverables>
</task_order>
```
