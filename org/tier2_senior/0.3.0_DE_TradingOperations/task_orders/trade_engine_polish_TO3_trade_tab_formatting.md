# Task Order: Trade Engine Visual Polish — TO-3: Trade Tab Formatting

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-trade-polish-to3</id>
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
    Two formatting changes to PortfolioGrid.tsx AG Grid column definitions:
    zero-weight cells display as dash, and size column cells get color-coded backgrounds.
    Covers PRD items 7 and 10.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/PortfolioManagement/components/PortfolioGrid.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      PRD Item 7 — Zero weight to dash:
      For columns initialWeight, optimizedWeight, finalWeight, benchmarkWeight:
      When value === 0, display "–" (en-dash, U+2013) instead of "0.00%".
      Implement via value formatter: if value === 0, return "–"; else return the existing
      percentage format. Do not change non-zero formatting.
    </requirement>
    <requirement id="2">
      PRD Item 10 — Size column coloring:
      Size column currently shows raw S/M/L/O value, bold, centered, no background color.
      Add cellStyle (or cellRenderer) that sets a muted translucent background per value:
        L (Large):   rgba(34, 197, 94, 0.15)   — green muted
        M (Mid):     rgba(234, 179, 8, 0.15)   — yellow muted
        O (Other):   rgba(239, 68, 68, 0.15)   — red muted
        S (Small):   rgba(239, 68, 68, 0.15)   — red muted (same as O)
      These are background colors, not text colors. Keep existing text styling intact.
    </requirement>
    <requirement id="3">
      bunx tsc -b must pass clean after all changes.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Securities with 0.00% weight show "–" in all four weight columns. Non-zero weights unchanged.</criterion>
    <criterion id="2">Size column cells: L = green tint, M = yellow tint, O = red tint, S = red tint. No change to text or bold formatting.</criterion>
    <criterion id="3">No TypeScript errors.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not change value formatters for non-zero weights — only the zero case is affected.</constraint>
    <constraint>Use rgba with 0.15 alpha or similar muted value appropriate for the dark theme. Do not use full-opacity colors that clash with selected row highlighting.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal DEV commit with items 7 and 10 complete</deliverable>
    <deliverable type="document">Session log with commit hash and tsc confirmation</deliverable>
  </deliverables>
</task_order>
```
