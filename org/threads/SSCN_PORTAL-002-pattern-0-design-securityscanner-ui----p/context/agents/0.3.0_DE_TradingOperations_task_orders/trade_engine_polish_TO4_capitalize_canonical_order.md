# Task Order: Trade Engine Visual Polish — TO-4: Capitalize + Canonical Group Ordering

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-trade-polish-to4</id>
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
    Create shared CANONICAL_GROUP_ORDER constant, apply capitalize CSS to all group name cells,
    and replace alphabetical group sort with canonical order in AlphaTab, ModelTab, and
    SecurityDetailModal. Covers PRD items 1, 11, and 13.
  </objective>

  <scope>
    <files>
      <file action="create">portal/src/pages/PortfolioManagement/utils/factorOrder.ts</file>
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/AlphaTab.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/ModelTab.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/components/SecurityDetailModal.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Create portal/src/pages/PortfolioManagement/utils/factorOrder.ts with:

        export const CANONICAL_GROUP_ORDER = [
          'size',
          'efficiency',
          'growth',
          'management',
          'profitability',
          'quality',
          'value',
          'analyst',
          'governance',
          'crowding',
          'insider',
          'short',
          'beta',
          'momentum',
          'technical',
        ] as const

        export type CanonicalGroup = typeof CANONICAL_GROUP_ORDER[number]

        export function canonicalGroupIndex(group: string): number {
          const idx = (CANONICAL_GROUP_ORDER as readonly string[]).indexOf(group.toLowerCase())
          return idx === -1 ? CANONICAL_GROUP_ORDER.length : idx
        }

      This order matches the signal DataFrame row order in Yang's alpha PKL. Source of truth
      is portal/src/pages/PortfolioManagement/utils/factorDescriptions.ts (comment order).
      Implementation pattern mirrors ECONOMY_ORDER in TradeTab.tsx (line 249).
    </requirement>
    <requirement id="2">
      PRD Item 13 — AlphaTab.tsx By Group sort (line 74):
      Replace the .localeCompare sort with canonicalGroupIndex sort:
        - Before: a.group.localeCompare(b.group)
        - After:  canonicalGroupIndex(a.group) - canonicalGroupIndex(b.group)
      Import canonicalGroupIndex from utils/factorOrder.ts.
    </requirement>
    <requirement id="3">
      PRD Item 1 — AlphaTab.tsx By Factor view group cells (line 421):
      Add CSS class "capitalize" (or style text-transform: capitalize) to group name cells.
      The By Group view already has capitalize at line 273 — leave that intact.
    </requirement>
    <requirement id="4">
      PRD Item 13 — ModelTab.tsx By Group sort:
      Apply the same canonical group ordering via canonicalGroupIndex to ModelTab's By Group
      aggregated view (where groups are currently sorted alphabetically or by Lambda response order).
      Read ModelTab.tsx before implementing to confirm where the sort happens.
    </requirement>
    <requirement id="5">
      PRD Item 1 — ModelTab.tsx:
      Apply capitalize CSS to group column cells (wherever group names appear in the table).
    </requirement>
    <requirement id="6">
      PRD Item 11 — SecurityDetailModal.tsx:
      1. Apply capitalize CSS class to group name cells in the factor list.
      2. Sort the factor list by canonical group order (canonicalGroupIndex on the group field).
         Within each group, preserve the original factor order from the data array.
    </requirement>
    <requirement id="7">
      bunx tsc -b must pass clean after all changes.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">factorOrder.ts exists with the 15-group CANONICAL_GROUP_ORDER array, exactly as specified.</criterion>
    <criterion id="2">AlphaTab By Group view: groups appear in canonical order (size first, technical last), not alphabetical.</criterion>
    <criterion id="3">AlphaTab By Factor view: group name cells show capitalized text (Size, Efficiency, etc.).</criterion>
    <criterion id="4">ModelTab By Group view: groups in canonical order; group cells capitalized.</criterion>
    <criterion id="5">SecurityDetailModal: factor list sorted by canonical group order; group cells capitalized.</criterion>
    <criterion id="6">No TypeScript errors. No regression on the By Factor views (which are already correct).</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>CANONICAL_GROUP_ORDER must live in factorOrder.ts — do not inline it in each component file. All three components import from the shared util.</constraint>
    <constraint>Groups not in CANONICAL_GROUP_ORDER sort to the end (canonicalGroupIndex returns CANONICAL_GROUP_ORDER.length for unknown groups). This is the fallback pattern — do not throw on unknown groups.</constraint>
    <constraint>Do not modify factorDescriptions.ts. It is the source of truth (read-only reference).</constraint>
    <constraint>Capitalize is a CSS presentation concern only — do not transform the data string. The underlying group value remains lowercase in the data model.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal DEV commit(s) with factorOrder.ts + items 1, 11, 13 complete</deliverable>
    <deliverable type="document">Session log with commit hash and tsc confirmation</deliverable>
  </deliverables>
</task_order>
```
