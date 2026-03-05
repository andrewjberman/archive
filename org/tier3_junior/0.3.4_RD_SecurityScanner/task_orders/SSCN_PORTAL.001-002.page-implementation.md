# Task Order: SSCN — SecurityScanner Page Implementation

```xml
<task_order>
  <metadata>
    <id>0.3.0_DE_TradingOperations-2026-03-05-sscn-page-implementation</id>
    <issued_by>0.3.0_DE_TradingOperations</issued_by>
    <issued_to>0.3.4_RD_SecurityScanner</issued_to>
    <date>2026-03-05</date>
    <status>complete</status>
    <thread_serial>SSCN_PORTAL-002</thread_serial>
    <thread_ref>org/tier3_junior/0.3.4_RD_SecurityScanner/threads/SSCN_PORTAL-002-pattern-0-design-securityscanner-ui----p_0.3.1_RD_PortfolioManagement+0.3.0_DE_TradingOperations.md</thread_ref>
  </metadata>

  <objective>
    Build the SecurityScanner portal page from scratch. All design and architecture decisions
    are locked in SSCN_PORTAL-002. You committed to authoring DESIGN_SPEC.md in thread turn 8.
    This task order formalizes that commitment and extends it to full page implementation.
    The data contract is at docs/architecture/SSCN_DATA_CONTRACT.md.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/SecurityScanner/</page>
    </pages>
    <files>
      <!-- Design spec (you committed to this in SSCN_PORTAL-002 turn 8) -->
      <file action="create">portal/src/pages/SecurityScanner/DESIGN_SPEC.md</file>
      <!-- Types (from SSCN_DATA_CONTRACT.md Section 5) -->
      <file action="create">portal/src/pages/SecurityScanner/types.ts</file>
      <!-- SSCN-local category ordering (SSCN_DESIGN_CONTRACT.md Section 7) -->
      <file action="create">portal/src/pages/SecurityScanner/utils/categoryOrder.ts</file>
      <!-- Quintile bucket helper (SSCN_DESIGN_CONTRACT.md Section 3D) -->
      <file action="create">portal/src/pages/SecurityScanner/utils/quintileUtils.ts</file>
      <!-- Factor chip display (SSCN_DESIGN_CONTRACT.md Section 3D — start inline, split here if it grows) -->
      <file action="create">portal/src/pages/SecurityScanner/components/FactorChip.tsx</file>
      <!-- Page shell -->
      <file action="create">portal/src/pages/SecurityScanner/SecurityScanner.tsx</file>
      <!-- Always-visible sticky header panel -->
      <file action="create">portal/src/pages/SecurityScanner/components/ScannerHeaderPanel.tsx</file>
      <!-- 4 tabs -->
      <file action="create">portal/src/pages/SecurityScanner/tabs/FactorBankTab.tsx</file>
      <file action="create">portal/src/pages/SecurityScanner/tabs/UniverseDataTab.tsx</file>
      <file action="create">portal/src/pages/SecurityScanner/tabs/FactorDataTab.tsx</file>
      <file action="create">portal/src/pages/SecurityScanner/tabs/UniverseScannerTab.tsx</file>
      <!-- State + API hooks -->
      <file action="create">portal/src/pages/SecurityScanner/hooks/useScannerState.ts</file>
      <file action="create">portal/src/pages/SecurityScanner/hooks/useScannerApi.ts</file>
      <!-- Update page inventory when first code ships -->
      <file action="modify">org/tier3_junior/0.3.4_RD_SecurityScanner/deliverables/page_inventory.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      READ BEFORE STARTING — in this order:

      PRIMARY (these two documents are the SoT for all design and data decisions):
      1. docs/architecture/SSCN_DESIGN_CONTRACT.md — authoritative record of every component
         reuse decision, table primitive ruling, gradient semantics, page shell composition,
         ScannerHeaderPanel layout, DESIGN_SPEC.md gate, and SSCN-local utility specs.
         Every requirement below is anchored to a section of this document.
      2. docs/architecture/SSCN_DATA_CONTRACT.md — all field names, TypeScript interface
         definitions, API route paths, null semantics, and universe ID mapping.

      SUPPORTING:
      3. org/tier3_junior/0.3.4_RD_SecurityScanner/threads/SSCN_PORTAL-002-... (your thread
         receipt) — full context for how decisions were reached
      4. portal/src/pages/PortfolioManagement/tabs/AlphaTab.tsx — AlphaTab visual language
         to replicate for Tabs 1 + 3 (per SSCN_DESIGN_CONTRACT.md Section 3C)
      5. portal/src/pages/PortfolioManagement/components/PortfolioGrid.tsx — AG Grid
         column-definition patterns to follow for Tabs 2 + 4 (per Section 4)
      6. portal/src/pages/PortfolioManagement/components/OptimizationSummaryHeader.tsx —
         sticky header layout conventions to mirror for ScannerHeaderPanel (per Section 9)
      7. docs/architecture/security-scanner-source/SECURITY_SCANNER_XLSM_AUDIT_COMPACT.md
         or equivalent — Factor Metadata Sample section lists the 11 SSCN categories needed
         for categoryOrder.ts and DESIGN_SPEC.md (per SSCN_DESIGN_CONTRACT.md Section 7 + 10)

      DEPENDENCY: DE must complete SSCN_PORTAL.001-002.shared-utils-extraction-proxy-routes.md
      before you wire imports from portal/src/utils/colorUtils.ts or
      portal/src/api/endpoints/security-scanner.ts. You may author DESIGN_SPEC.md and
      types.ts immediately. Do not import from shared paths until DE signals extraction committed.
    </requirement>
    <requirement id="2">
      DESIGN_SPEC.md — GATE: this is your FIRST deliverable. No .tsx file may be written
      until DESIGN_SPEC.md is committed to portal DEV AND DE (0.3.0_DE_TradingOperations)
      has reviewed and approved it. This gate is specified in SSCN_DESIGN_CONTRACT.md Section 10.

      Author portal/src/pages/SecurityScanner/DESIGN_SPEC.md using the ASCII layout skeleton
      from SSCN_PORTAL-002 thread turn 5 as the base. The document must reflect all contracted
      decisions from SSCN_DESIGN_CONTRACT.md and must include:

      Required content per SSCN_DESIGN_CONTRACT.md Section 10:
        1. ASCII layout for each of the 4 tabs and the page shell (Section 8 + your turn 5 skeleton)
        2. AG Grid mandate for Tabs 2 + 4 (Section 4) with justification
        3. Tab 4 default column layout: Rank | Ticker | Name | Composite | Mkt Val | (Country) |
           [Percentile columns]; raw values hidden by default; toggle at far right (Section 6)
        4. Shared util import paths: portal/src/utils/colorUtils.ts, portal/src/utils/factorOrder.ts
        5. SSCN-local category order path: portal/src/pages/SecurityScanner/utils/categoryOrder.ts
        6. ScannerHeaderPanel sticky above TabNavigation (Section 9 layout verbatim)
        7. The 11 SSCN factor categories — populate from XLSM compact audit Factor Metadata Sample
        8. Panel component hierarchy for each tab (which Panel variant wraps each tab content area)
        9. Reference to shared design tokens: portal/src/lib/designTokens.ts

      This document is the blueprint DE and DT use to review your implementation.
    </requirement>
    <requirement id="3">
      TYPES (types.ts):
      Implement all 6 TypeScript interfaces exactly as specified in SSCN_DATA_CONTRACT.md Section 5:
        FactorDefinition
        UniverseDataRow
        ScannerRow
        FactorMetadataResponse
        UniverseDataResponse
        ScannerDataResponse
      Also add client-computed types:
        ScannerRowWithScore extends ScannerRow {
          compositeScore: number | null
          rank: number
        }
      Do NOT define these interfaces in the endpoint file or elsewhere — types.ts is the single
      source of truth. Import from types.ts in all other SSCN files.
    </requirement>
    <requirement id="4">
      CATEGORY ORDER (utils/categoryOrder.ts):
      Per SSCN_DESIGN_CONTRACT.md Section 7. Path and exports are contracted:

        export const CANONICAL_CATEGORY_ORDER = [
          // 11 SSCN factor categories — populate from XLSM Tab 3 "Factor Metadata Sample"
          // Category column in docs/architecture/security-scanner-source/ audit.
          // Order must match XLSM Tab 3 display order.
        ] as const
        export type CanonicalCategory = typeof CANONICAL_CATEGORY_ORDER[number]
        export function canonicalCategoryIndex(category: string): number {
          const idx = (CANONICAL_CATEGORY_ORDER as readonly string[]).indexOf(category.toLowerCase())
          return idx === -1 ? CANONICAL_CATEGORY_ORDER.length : idx
        }

      Pattern mirrors portal/src/utils/factorOrder.ts (post-extraction) exactly — same structure,
      different content. These are different taxonomies: 15 PM/Yang groups vs 11 SSCN categories.
      Do not conflate. Use shared canonicalGroupIndex only if SSCN renders PM 15-group concepts
      (not in Phase 0).

      The 11 categories must also appear in DESIGN_SPEC.md (Section 10 requirement).
    </requirement>
    <requirement id="5">
      PAGE SHELL (SecurityScanner.tsx):
      Follow SSCN_DESIGN_CONTRACT.md Section 8 exactly. The JSX composition tree is:

        PageThemeProvider                          // portal/src/contexts/PageThemeContext.tsx
          PageHeaderCleanBadge                     // portal/src/components/PageHeaderVariants.tsx
            title="Security Scanner"
            icon={&lt;ScanLine /&gt;}              // lucide-react ScanLine (not ScanSearch)
            badge={{ label: 'Dev', variant: 'dev' }}  // requiresDev: true per PRD
          ScannerHeaderPanel                       // sticky, Section 9
          TabNavigation                            // portal/src/components/TabNavigation.tsx
          div (tabContentRef)
            {activeTab === 'factor-bank'      &amp;&amp; &lt;FactorBankTab /&gt;}
            {activeTab === 'universe-data'    &amp;&amp; &lt;UniverseDataTab /&gt;}
            {activeTab === 'factor-data'      &amp;&amp; &lt;FactorDataTab /&gt;}
            {activeTab === 'universe-scanner' &amp;&amp; &lt;UniverseScannerTab /&gt;}

      4 tabs: Factor Bank | Universe Data | Factor Data | Universe Scanner
      Use useTabNavigation hook (portal/src/hooks/useTabNavigation.ts).
      Shared components per SSCN_DESIGN_CONTRACT.md Section 3A:
        PageHeaderCleanBadge, useTabNavigation, TabNavigation, PageThemeProvider,
        Panel/PanelHeader/PanelContent, ErrorBoundary — all import directly, no changes.
    </requirement>
    <requirement id="6">
      SCANNER HEADER PANEL (components/ScannerHeaderPanel.tsx):
      Follow SSCN_DESIGN_CONTRACT.md Section 9 exactly. Summary:

      Always visible above TabNavigation. Sticky positioning matching OptimizationSummaryHeader.tsx
      (position sticky, top-0, z-40 or equivalent). Use Panel / PanelHeader / PanelContent primitives.

      PanelHeader:
        title: "Scanner Controls"
        helpText: "Select universe, add factors, and set weights to 100%."
        actions (right):
          &lt;select&gt; Universe — 6 options (labels from UNIVERSE_IDS in security-scanner.ts)
          [Equal Weight] button
          [Clear] button

      PanelContent:
        Row 1: Selected factor chips (scrollable wrap) + count badge "N factors"
               Each chip shows factor code or short name + X to remove.
               FactorChip component (portal/src/pages/SecurityScanner/components/FactorChip.tsx)
        Row 2: Compact weight editor — one numeric input per selected factor (0-100)
               (inline or collapsible "Manage Weights" section — your choice)
        Row 3: Validation strip
               Total Weight = {sum}%
               success token (hsl(var(--success))) if sum === 100
               danger token (hsl(var(--danger))) otherwise
               Error text: "Weights must sum to 100%" when invalid

      State: all scanner state (selectedUniverse, selectedFactors, weights) lives in
      useScannerState.ts. ScannerHeaderPanel receives these as props + callback props.
    </requirement>
    <requirement id="7">
      TAB 1 — FactorBankTab.tsx (Factor Bank):
      HTML table pattern (AlphaTab.tsx visual language — see portal/src/pages/PortfolioManagement/tabs/AlphaTab.tsx).
      PanelHeader actions: search input + category filter dropdown.
      Two sections: "Selected Factors" (top panel) + "Factor Bank" (bottom panel).
      Columns: Category | Factor Name | Code | IC | Coverage % | Relationship | Systematic | YES/NO toggle
      Category column: capitalize CSS (text-transform: capitalize).
      Sort: 3-state (canonical → desc → asc → canonical) using canonicalCategoryIndex from categoryOrder.ts.
      Yellow IC highlight: highest IC per category (SSCN-specific, no PM equivalent).
      YES/NO toggle: adds/removes factor from useScannerState selectedFactors.
      Row styling: odd:bg-white/[0.05] hover:bg-white/10 (match AlphaTab).
    </requirement>
    <requirement id="8">
      TAB 2 — UniverseDataTab.tsx (Universe Data):
      AG Grid (Community edition, same import as PortfolioGrid.tsx).
      Columns: Ticker (pinned left) | Name (pinned left) | Mkt Val | (Country, hidden for US universes) | Sector | Industry Group | [dynamic factor columns for selected factors, raw values]
      Dynamic factor columns: one column per selected factor from useScannerState. Column header = factor code.
      Read-only grid (no editing). Sort + filter enabled (AG Grid built-in).
      Data source: useQuery for getUniverseData(selectedUniverseId) from portal/src/api/endpoints/security-scanner.ts.
      Country column visibility: hidden for sp500, r1000, r1000v; shown for acwx, eafe, eafev.
    </requirement>
    <requirement id="9">
      TAB 3 — FactorDataTab.tsx (Factor Data):
      HTML table (AlphaTab.tsx pattern). Independent of header selections (shows ALL factors always).
      Columns: Code | Name | Category | Relationship | Asset Class | Coverage % | IC
      PanelHeader actions: search + category filter.
      Data source: useQuery for getSecurityScannerFactors() from security-scanner.ts.
      Category column: capitalize CSS + sort by canonicalCategoryIndex.
    </requirement>
    <requirement id="10">
      TAB 4 — UniverseScannerTab.tsx (Universe Scanner):
      AG Grid (mandate per SSCN_DESIGN_CONTRACT.md Section 4). Primary interactive tab.

      Client-side composite + rank per SSCN_DATA_CONTRACT.md Section 8:
        compositeScore = sum(pctls[code] * weight[code]) / 100  (skip null pctls)
        if all selected factors null for a row: compositeScore = null (sorts to bottom)
        rank = sort order by compositeScore descending (nulls last)
      Recompute on every weight change. No server round-trip.

      Default visible columns (per SSCN_DESIGN_CONTRACT.md Section 6):
        Rank (pinned left) | Ticker (pinned left) | Name (pinned left) | Composite Score
        | Mkt Val | Country (conditional — hidden for sp500/r1000/r1000v, visible for
        acwx/eafe/eafev) | [per selected factor: Percentile column]
        Raw value columns: HIDDEN by default.

      Toggle in PanelHeader actions (per Section 6):
        [Percentiles]  [Percentiles + Raw]
        When raw active: raw columns appended at far right (after all percentile columns).
        Percentile columns stay contiguous. Do not interleave.

      Gradient coloring (per SSCN_DESIGN_CONTRACT.md Section 5 — use this formula exactly):
        import { getGradientBackground } from '@/utils/colorUtils'
        For percentile p: getGradientBackground(p - 50, -50, 50, false)
        For compositeScore c: getGradientBackground(c - 50, -50, 50, false)
        Null cell: display "—" (em dash) + text-white/40 + no gradient background.

      quintileUtils.ts: place any percentile-to-display helpers (top IC per category
      highlight, null detection, cell style factory) in
      portal/src/pages/SecurityScanner/utils/quintileUtils.ts (per Section 3D).

      Data source: useQuery for getUniverseScanner(selectedUniverseId).
      Auto-sort: grid re-sorts by compositeScore desc on every weights change.
    </requirement>
    <requirement id="11">
      STATE HOOK (hooks/useScannerState.ts):
      Manages:
        selectedUniverseId: UniverseId (default 'sp500')
        selectedFactors: FactorDefinition[]  (ordered by user addition)
        weights: Record&lt;string, number&gt;  (factor code -> weight, 0-100)
        totalWeight: number (derived: sum of weights.values())
        isWeightValid: boolean (totalWeight === 100)
      Actions:
        setUniverse(id: UniverseId)
        addFactor(factor: FactorDefinition)
        removeFactor(code: string)
        setWeight(code: string, value: number)
        setEqualWeight()  (100 / selectedFactors.length, distributed evenly)
        clearSelection()  (clear factors + weights)
    </requirement>
    <requirement id="12">
      API HOOK (hooks/useScannerApi.ts):
      Wraps all three API calls with useQuery:
        useFactorMetadata() — calls getSecurityScannerFactors(), staleTime: Infinity (static monthly data)
        useUniverseData(universeId) — calls getUniverseData(universeId), staleTime: 5 minutes
        useUniverseScanner(universeId) — calls getUniverseScanner(universeId), staleTime: 5 minutes
      Import from portal/src/api/endpoints/security-scanner.ts (DE's file).
    </requirement>
    <requirement id="13">
      PAGE INVENTORY UPDATE:
      Update org/tier3_junior/0.3.4_RD_SecurityScanner/deliverables/page_inventory.xml in the
      same commit as the first code shipped. Add entries for each file created. Update status
      from "scaffold -- no files shipped yet" to "in progress" or "complete" as appropriate.
    </requirement>
    <requirement id="14">
      TSC GATE:
      Run bunx tsc -b (from the portal/ directory) before signaling DT to push.
      Must pass with zero errors. No any-casts except the temporary ones noted in useScannerApi.ts
      before the endpoint types are wired.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">DESIGN_SPEC.md committed to portal DEV and reviewed/approved by 0.3.0_DE_TradingOperations before any .tsx file is written. Contains all 9 required content items from SSCN_DESIGN_CONTRACT.md Section 10 including the 11 SSCN factor categories and Panel hierarchy per tab.</criterion>
    <criterion id="2">types.ts defines all 6 interfaces from SSCN_DATA_CONTRACT.md Section 5 with exact field names and types.</criterion>
    <criterion id="3">categoryOrder.ts exports CANONICAL_CATEGORY_ORDER (11 categories), CanonicalCategory type, canonicalCategoryIndex(). 15-group factorOrder is imported from portal/src/utils/ (never from PM-local path).</criterion>
    <criterion id="4">SecurityScanner.tsx composes PageHeaderCleanBadge -> ScannerHeaderPanel -> TabNavigation -> tab content.</criterion>
    <criterion id="5">ScannerHeaderPanel: universe dropdown, factor chips, weight inputs, total weight validation strip — all wired to useScannerState.</criterion>
    <criterion id="6">Tab 1 (Factor Bank): two-panel layout, search + category filter, YES/NO toggle, yellow IC highlight, canonical category sort, AlphaTab visual language.</criterion>
    <criterion id="7">Tab 2 (Universe Data): AG Grid, dynamic factor columns for selected factors, country column hidden for US universes.</criterion>
    <criterion id="8">Tab 3 (Factor Data): HTML table, all factors shown independently of header selection, category filter + sort.</criterion>
    <criterion id="9">Tab 4 (Universe Scanner): AG Grid, composite + rank client-computed from pctls + weights, gradient coloring using getGradientBackground(p-50, -50, 50), nulls as "--" + muted, raw columns default-hidden with toggle, auto-sort on weight change.</criterion>
    <criterion id="10">bunx tsc -b passes. No imports from portal/src/pages/PortfolioManagement/utils/ (must use portal/src/utils/). Implementation matches SSCN_DESIGN_CONTRACT.md in component structure, gradient formula (Section 5), column layout (Section 6), and page shell composition (Section 8).</criterion>
    <criterion id="11">page_inventory.xml updated.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>DESIGN_SPEC.md gate (SSCN_DESIGN_CONTRACT.md Section 10): do not write a single .tsx file until DESIGN_SPEC.md is committed to portal DEV AND 0.3.0_DE_TradingOperations has reviewed and approved it. DESIGN_SPEC.md is your first deliverable.</constraint>
    <constraint>docs/architecture/SSCN_DESIGN_CONTRACT.md is the SoT for all component, utility, table primitive, gradient, and layout decisions. Any conflict between this task order and SSCN_DESIGN_CONTRACT.md resolves in favor of the design contract. Flag the conflict to DE rather than guessing.</constraint>
    <constraint>Import colorUtils from '@/utils/colorUtils' (shared, post-DE extraction). Never from PortfolioManagement/utils/. Wrong path = PM dependency that breaks when PM moves.</constraint>
    <constraint>Import factorOrder from '@/utils/factorOrder' (shared). SSCN categoryOrder.ts is for SSCN's 11 categories only — different taxonomy from PM's 15 groups.</constraint>
    <constraint>AG Grid for Tab 2 + Tab 4. HTML tables for Tab 1 + Tab 3. Non-negotiable (SSCN_DESIGN_CONTRACT.md Section 4).</constraint>
    <constraint>compositeScore and rank are client-side only — not in JSON, not in ScannerRow interface. Use ScannerRowWithScore as the computed extension type.</constraint>
    <constraint>Do NOT push — signal 0.3.0_DT_TradingOperations when commits are ready.</constraint>
    <constraint>Handle loading/error/empty states in all tab components so the page renders before S3 data exists (AE deploy may lag portal deploy).</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.3.0_DE_TradingOperations" task="SSCN_PORTAL.001-002.shared-utils-extraction-proxy-routes.md" status="pending">
      Do not import from portal/src/utils/colorUtils.ts or portal/src/api/endpoints/security-scanner.ts
      until DE has committed these files. Scaffold types.ts and DESIGN_SPEC.md while waiting.
    </dependency>
    <dependency agent="0.5.0_AE_OpalETL" task="SSCN_PORTAL.001-002.terraform-infra.md" status="pending">
      Live data will not be available until AE deploys the processing Lambda and triggers.
      Build against mock/empty states in loading/error branches so the page renders before data exists.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="document">portal/src/pages/SecurityScanner/DESIGN_SPEC.md</deliverable>
    <deliverable type="commit">portal DEV commit(s) covering all files in scope</deliverable>
    <deliverable type="document">page_inventory.xml updated</deliverable>
  </deliverables>
</task_order>
```
