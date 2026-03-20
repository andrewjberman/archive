<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-19-bkscmp-002-rd</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-19</date>
    <status>complete</status>
    <project_code>ADVI_BKSCMP</project_code>
  </metadata>

  <objective>
    Extend types.ts with optional per-class top_holdings fields, and update the
    holdings derivation block in ConsolidatedOverviewPanel to be schema-adaptive:
    N1/L2 use pre-aggregated per-class top_holdings from the new artifacts; L3/L4
    continue to use the existing flat concentration.items path. No other changes
    to ConsolidatedOverviewPanel. RD can work in parallel with DS/DT/AE — the
    adapter is backward-compatible and falls through to synthesis when the new
    Lambda routes return 404.
  </objective>

  <context>
    Reference: docs/architecture/ADVI_BKSCMP_PRD.md §WS3a (types), §WS3b (component),
    §3 (schema), §5 (sequencing — RD parallel track).

    Current state (verified):
    - types.ts MixItem does NOT have top_holdings or other optional fields yet.
    - BooksCompositionResponse scope does NOT have advisor_id or firm_id fields yet.
    - Holdings block at ClientsTab.tsx lines 875–884 is the ONLY change in the component.
    - showFilteredOther render is at lines 1039–1050 — replaced by unified showOther.
    - showOther render is at lines 1055–1068 — replace with PRD version using otherEntry.
    - Empty state at line 1073: `allItems.length === 0 ? 'No holdings data at this level'`

    The ConsolidatedOverviewPanel's donut, legend, quarterly bar, and all other logic
    are completely unaffected by this change. The holdings block is the only code section
    touched.

    advisor_id consistency note: `handleSelectAdvisor` at line 383 sanitizes the advisor
    name to produce the `entity_id` used in `fetchComposition('advisor', id, ...)`.
    Script 12 uses the identical transform to generate S3 keys. These are consistent
    by PRD constraint — no change needed in ClientsTab.tsx for this.
  </context>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1" workstream="WS3a-types">
      In `portal/src/pages/AdvisorIntelligence/types.ts`:

      A. Extend MixItem with two optional fields (add at the end of the interface):
        export interface MixItem {
          asset_class: string
          label: string
          market_value: number
          pct: number
          // N1/L2 schema only -- per-class top holdings (pct relative to class market_value)
          top_holdings?: ConcentrationItem[]
          other?: { market_value: number; pct: number }
        }

      B. Extend BooksCompositionResponse scope and add optional root-level fields:
        export interface BooksCompositionResponse {
          generated_at: string
          data_as_of: string
          scope: {
            relationship_id?: string
            account_id?: string
            advisor_id?: string   // new -- N1/L2 schema
            firm_id?: string      // new -- N1/L2 schema
          }
          mix: MixItem[]
          concentration: {
            top_n: number
            items: ConcentrationItem[]
            other: { market_value: number; pct: number }
          }
          // N1/L2 schema only -- global top holdings (pct relative to total_market_value)
          top_holdings?: ConcentrationItem[]
          other?: { market_value: number; pct: number }  // global other
          unclassified: { count: number; market_value: number }
        }

      ConcentrationItem is unchanged. No other type additions.
    </requirement>

    <requirement id="2" workstream="WS3b-holdings-block">
      In `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx`,
      replace ONLY the block at lines 875–884 and the render blocks that use
      showOther / showFilteredOther.

      Replace lines 875–884:
        const allItems = composition?.concentration.items ?? []
        const filteredItems = selectedAssetClass
          ? allItems.filter(it => it.asset_class === selectedAssetClass)
          : allItems

        const MAX_ITEMS = 9
        const cappedItems = filteredItems.slice(0, MAX_ITEMS)
        const showOther = !selectedAssetClass && composition && composition.concentration.other.pct > 0
        const showFilteredOther = Boolean(selectedAssetClass && filteredItems.length > MAX_ITEMS)
        const maxPct = cappedItems.length > 0 ? cappedItems[0].pct : 1

      With the schema-adaptive version from PRD §WS3b (exact code):
        // Detect schema: N1/L2 (per-class top_holdings) vs L3/L4 (flat concentration.items)
        const hasPreAggregated = (composition?.mix.some(m => (m.top_holdings?.length ?? 0) > 0)) ?? false

        const MAX_ITEMS = 9

        // Resolved display items
        const cappedItems: ConcentrationItem[] = (() => {
          if (!composition) return []
          if (hasPreAggregated) {
            if (selectedAssetClass) {
              // Per-class top holdings already pre-capped at 9 by script 12
              return composition.mix.find(m => m.asset_class === selectedAssetClass)?.top_holdings ?? []
            } else {
              // Global top 9
              return composition.top_holdings ?? []
            }
          } else {
            // L3/L4: filter flat list, cap at 9
            const all = composition.concentration.items
            const filtered = selectedAssetClass
              ? all.filter(it => it.asset_class === selectedAssetClass)
              : all
            return filtered.slice(0, MAX_ITEMS)
          }
        })()

        // "Other" bucket display
        const otherEntry: { pct: number; market_value: number } | null = (() => {
          if (!composition) return null
          if (hasPreAggregated) {
            if (selectedAssetClass) {
              return composition.mix.find(m => m.asset_class === selectedAssetClass)?.other ?? null
            } else {
              return composition.other ?? null
            }
          } else {
            // L3/L4 schema
            if (!selectedAssetClass &amp;&amp; composition.concentration.other.pct > 0) {
              return composition.concentration.other
            }
            return null
          }
        })()

        const showOther = otherEntry !== null &amp;&amp; otherEntry.pct > 0
        const maxPct = cappedItems.length > 0 ? cappedItems[0].pct : 1
    </requirement>

    <requirement id="3" workstream="WS3b-render-other">
      Remove showFilteredOther. Replace the two existing "Other" render blocks
      (lines 1039–1068: the showFilteredOther block at 1039–1050 AND the showOther
      block at 1055–1068) with a SINGLE unified block using otherEntry (PRD §WS3b):

        {showOther &amp;&amp; otherEntry &amp;&amp; (
          &lt;div className="flex items-center gap-2.5"&gt;
            &lt;span className="text-[10px] text-white/20 w-4 text-right flex-shrink-0"&gt;~&lt;/span&gt;
            &lt;div className="flex-1"&gt;
              &lt;div className="flex items-baseline justify-between mb-1"&gt;
                &lt;span className="text-[11px] text-white/40 italic"&gt;Other&lt;/span&gt;
                &lt;span className="text-[11px] text-white/30 ml-2"&gt;{(otherEntry.pct * 100).toFixed(1)}%&lt;/span&gt;
              &lt;/div&gt;
              &lt;div className="h-1.5 bg-white/[0.05] rounded-full overflow-hidden"&gt;
                &lt;div className="h-full rounded-full bg-white/20"
                  style={{ width: `${(otherEntry.pct / maxPct) * 100}%` }} /&gt;
              &lt;/div&gt;
            &lt;/div&gt;
          &lt;/div&gt;
        )}
    </requirement>

    <requirement id="4" workstream="WS3b-empty-state">
      Update the empty state condition at line 1073.

      Current:
        allItems.length === 0 ? 'No holdings data at this level'

      Replace with:
        !hasPreAggregated &amp;&amp; composition.concentration.items.length === 0
          ? 'No holdings data at this level'

      This ensures that when hasPreAggregated is true (N1/L2), an empty cappedItems array
      does not show "No holdings data" — it correctly falls through to the loading state
      (the composition itself is non-null, so "No holdings for selected class" is the right message).
    </requirement>

    <requirement id="5" workstream="commit">
      Commit both files together to portal DEV:
        git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" \
          -m "feat(portal): schema-adaptive holdings block for N1/L2 composition (ADVI_BKSCMP WS3)"

      Report commit SHA to COO. This is a WS6 portal merge gate.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">MixItem has optional top_holdings?: ConcentrationItem[] and other?: {market_value, pct}</criterion>
    <criterion id="2">BooksCompositionResponse scope has optional advisor_id and firm_id</criterion>
    <criterion id="3">BooksCompositionResponse has optional root-level top_holdings and other</criterion>
    <criterion id="4">hasPreAggregated detection uses mix.some(m => top_holdings?.length > 0)</criterion>
    <criterion id="5">When hasPreAggregated and selectedAssetClass: uses mix[class].top_holdings (pct / class_mv)</criterion>
    <criterion id="6">When hasPreAggregated and no selectedAssetClass: uses composition.top_holdings (global)</criterion>
    <criterion id="7">L3/L4 path unchanged: filters concentration.items, caps at 9</criterion>
    <criterion id="8">Single unified showOther block using otherEntry — showFilteredOther removed</criterion>
    <criterion id="9">Empty state updated: !hasPreAggregated &amp;&amp; concentration.items.length === 0</criterion>
    <criterion id="10">bunx tsc -b passes (no new type errors)</criterion>
    <criterion id="11">All other ConsolidatedOverviewPanel code (donut, legend, quarterly bar) unmodified</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Touch ONLY lines 875–884 (derivation block) and the two render blocks (showOther/showFilteredOther) in ClientsTab.tsx</constraint>
    <constraint>Do NOT modify handleSelectAdvisor, fetchComposition, synthesizeFrom*, or any other ClientsTab function</constraint>
    <constraint>Do NOT add features, comments, or refactors beyond the specified changes</constraint>
    <constraint>All portal changes commit to portal DEV (not CLOUD parent repo)</constraint>
    <constraint>No emojis in code or commit messages (CLAUDE.md rule 13)</constraint>
    <constraint>RD does NOT push -- DT pushes portal DEV to remote</constraint>
    <constraint>Do NOT gate this work on DS/DT/AE -- the adapter is backward-compatible (404 falls through to synthesis)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" status="clear">
      No upstream gates. Frontend is backward-compatible when Lambda routes return 404.
      Commit to portal DEV immediately.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">types.ts + ClientsTab.tsx committed to portal DEV (ADVI_BKSCMP WS3)</deliverable>
  </deliverables>
</task_order>
