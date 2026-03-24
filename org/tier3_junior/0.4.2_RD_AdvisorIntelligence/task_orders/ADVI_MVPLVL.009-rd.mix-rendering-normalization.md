<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-23-mvplvl-009-rd</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-23</date>
    <status>complete</status>
    <project_code>ADVI_MVPLVL</project_code>
    <thread_serial>ADVI_MVPLVL-006</thread_serial>
    <thread_ref>org/threads/ADVI_MVPLVL-006-mix-and-composition-e2e-trace----broken/</thread_ref>
  </metadata>

  <objective>
    Fix rendering normalization in PartnerAnalytics.tsx for the Mix toggle's
    stacked bar chart. The backend returns "cash" as a separate field but the
    acceptance criteria require merging cash into "Other" for display. The Mix
    chart currently stacks "cash" explicitly and labels it "Cash" -- this must
    be changed to show 4 series: Equity, Fixed Income, Alternatives, Other.

    DE is concurrently fixing ClientsTab.tsx (Books tab wiring + normalization).
    RD should NOT modify ClientsTab.tsx to avoid merge conflicts unless DE
    explicitly delegates a slice.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      In PartnerAnalytics.tsx Mix chart data mapping:
      - Remove the "cash" series from the stacked bar
      - Add an "other" series whose value = cash.value (from firm_mix_views.json)
      - Label: "Other" (not "Cash")
      - Stack order: equity, fixed_income, alternatives, other (consistent with
        NMEC/NMNC Clients stacked bar format)
    </requirement>

    <requirement id="2">
      Update tooltip label map:
      - Remove cash: 'Cash' entry
      - Add other: 'Other' entry
      - Ensure tooltip shows: Equity, Fixed Income, Alternatives, Other
    </requirement>

    <requirement id="3">
      Update color mapping:
      - other should use the same gray as existing "Other" elsewhere in AdvisorIntelligence
        (likely #6B7280 or similar)
      - Remove any separate cash color
    </requirement>

    <requirement id="4">
      Verify that the aggregate numbers tie:
      - sum(equity.value + fixed_income.value + alternatives.value + other.value) = total_aua
        for each period point
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Mix toggle renders stacked bar with exactly 4 series: Equity, Fixed Income, Alternatives, Other</criterion>
    <criterion id="2">No "Cash" label appears in chart, tooltip, or legend</criterion>
    <criterion id="3">Colors match CMA taxonomy: equity blue, fixed_income green, alternatives orange, other gray</criterion>
    <criterion id="4">Same visual format as NMEC/NMNC stacked bars in Clients toggle</criterion>
    <criterion id="5">Aggregate values tie to total AUA per period</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Only modify files inside portal/src/pages/AdvisorIntelligence/ (RD page-only commit scope).</constraint>
    <constraint>Do NOT modify ClientsTab.tsx -- DE is working on that file concurrently.</constraint>
    <constraint>Do NOT modify portal/src/api/endpoints/advisor-intelligence.ts -- DE owns API client changes.</constraint>
    <constraint>Commit with --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;"</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13).</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_MVPLVL.009-de.api-wiring-normalization" status="pending">
      DE may introduce a shared normalization helper. If DE exports normalizeMixTo4Class(),
      RD should use it in PartnerAnalytics.tsx instead of duplicating. If DE has not
      committed yet, RD can implement inline and DE will reconcile.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Portal DEV commit: PartnerAnalytics.tsx Mix cash-to-other normalization</deliverable>
  </deliverables>
</task_order>
