<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-23-mvplvl-009-de</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-23</date>
    <status>complete</status>
    <project_code>ADVI_MVPLVL</project_code>
    <thread_serial>ADVI_MVPLVL-006</thread_serial>
    <thread_ref>org/threads/ADVI_MVPLVL-006-mix-and-composition-e2e-trace----broken/</thread_ref>
  </metadata>

  <objective>
    Fix the frontend API wiring and data normalization for both broken views:
    (1) Assets Overview "Mix" toggle, (2) Books tab "Asset Mix" + "Top Holdings".

    Thread ADVI_MVPLVL-006 diagnosed the root cause as:
    - ClientsTab.tsx uses a local fetchComposition() helper that silently returns
      null on non-200, bypassing the canonical API client
    - Missing getBooksAdvisorComposition() endpoint function
    - Cash displayed as separate label instead of merged into "Other"
    - L3/L4 per-class "Other" not computed in ConsolidatedOverviewPanel

    This is the primary fix task. DE owns API client wiring, ClientsTab refactor,
    and the normalization helper shared between views.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="modify">portal/src/api/endpoints/advisor-intelligence.ts</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Add getBooksAdvisorComposition() endpoint function in advisor-intelligence.ts:
      - Signature: getBooksAdvisorComposition(advisorId: string, firmOverride?: string): Promise&lt;BooksCompositionResponse&gt;
      - URL: /api/scoped/partners/books/advisor/${advisorId}/composition?firmId=${mappedFirmId}
      - Use LAMBDA_FIRM_ID mapping (same as existing endpoint functions)
    </requirement>

    <requirement id="2">
      Remove the local fetchComposition() helper and FIRM_KEY mapping from ClientsTab.tsx.
      Replace all usages:
      - N1 firm composition: use getBooksFirmComposition(effectiveFirm)
      - L2 advisor composition: use new getBooksAdvisorComposition(selectedAdvisorId, effectiveFirm)
      Keep synthesis fallback only as a catch-all if the endpoint throws.
    </requirement>

    <requirement id="3">
      Implement normalizeMixTo4Class() helper for display taxonomy normalization:
      - Input: mix items array (from composition response or mix views)
      - Output: normalized array with exactly 4 classes: equity, fixed_income, alternatives, other
      - Merge cash + other into single "other" bucket with label "Other"
      - Recompute pct from market_value / total
      - For preaggregated schema (script 12): merge top_holdings arrays for cash+other classes
      - Apply in both PartnerAnalytics.tsx (Mix stacked bar) and ClientsTab.tsx (Books donut)
    </requirement>

    <requirement id="4">
      Fix L3/L4 per-class "Other" computation in ConsolidatedOverviewPanel:
      - When selectedAssetClass is set and we are in the non-preaggregated schema:
        - filtered = concentration.items.filter(it => it.asset_class === selectedAssetClass)
        - top9 = filtered.slice(0, 9)
        - otherMv = sum(filtered.map(i => i.market_value)) - sum(top9.map(i => i.market_value))
        - Show "Other" bar when filtered.length > 9 and otherMv > 0
        - otherPct = otherMv / sum(filtered.map(i => i.market_value))
      - Note: this is an approximation for L3/L4 since Lambda only returns top-10 global.
        Accept this limitation for now per thread consensus.
    </requirement>

    <requirement id="5">
      Ensure Mix stacked bar in PartnerAnalytics.tsx uses the same normalization:
      - Stack order: equity, fixed_income, alternatives, other (bottom to top or as consistent with Clients NMEC/NMNC)
      - Tooltip labels: Equity, Fixed Income, Alternatives, Other
      - Colors: match CMA color scheme used elsewhere in AdvisorIntelligence
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Assets Overview "Mix" toggle renders stacked bar with Equity, Fixed Income, Alternatives, Other at firm level</criterion>
    <criterion id="2">Books tab Overview "Asset Mix" radial renders at firm, advisor, and relationship levels</criterion>
    <criterion id="3">Books tab Overview "Top Holdings" renders top 9 + Other at all drill levels</criterion>
    <criterion id="4">Clicking a class in the radial filters Top Holdings to that class's top 9 + Other</criterion>
    <criterion id="5">No "Cash" label appears anywhere -- merged into "Other"</criterion>
    <criterion id="6">bunx tsc -b passes with zero errors</criterion>
    <criterion id="7">Colors and labels match CMA taxonomy consistently</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Coordinate with RD: RD may apply rendering-only changes to PartnerAnalytics.tsx concurrently. DE owns the normalization helper and API client changes; RD owns visual tweaks. Avoid merge conflicts by communicating.</constraint>
    <constraint>"Other" in Mix context = residual AUA not in equity/fixed_income/alternatives. Primarily cash. Do NOT add "Cash" as a separate visual label.</constraint>
    <constraint>Mix stacked bar MUST follow the exact same visual format as NMEC/NMNC in the Clients toggle.</constraint>
    <constraint>Commit with --author="0.4.0_DE_ClientPlatform &lt;0.4.0_DE_ClientPlatform@opal.agent&gt;"</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13).</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MVPLVL.009-ds.verify-s3-data" status="pending">
      DS verifies S3 data exists. If 404, AE runs gold rerun first. DE can proceed
      with wiring changes regardless -- they are correct even if backend returns 404.
    </dependency>
    <dependency agent="0.6.0_AE_PartnerETL" task="ADVI_MVPLVL.009-ae.verify-lambda-routes" status="pending">
      AE verifies Lambda routes return 200. Informational -- DE proceeds regardless.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Portal DEV commit with API wiring fix + normalization + L3/L4 Other computation</deliverable>
  </deliverables>
</task_order>
