# Task Order: AdvisorIntelligence Color Migration + Design QA

<task_order>
  <metadata>
    <id>ADHC_DESIGN-003</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <!-- Completed 2026-04-07. Portal DEV commit pending. 10 files migrated: DistributionTab, PartnerAnalytics, AdvisorsTab, ClientsTab, AUATrendChart, AUACompositionChart, TimeSeriesPanel, PortfolioBalancePanel, MixTimeseriesPanel, ConcentrationPanel, AssetIntelligenceTab. Zero hex remaining. chartColors.ts extended with PALETTE entries (purple600, fuchsia500, neutral400, violet300, green300, nmncGreen), SURFACE, NNA_BAR, CATEGORY_ALT, PERCENTILE_MARKERS, TAX_COLORS, withOpacity. -->
    <project>ADHC_DESIGN</project>
  </metadata>

  <objective>
    Migrate ALL hardcoded hex colors in the AdvisorIntelligence page directory to
    imports from `@/lib/chartColors.ts`. Then run Design QA checklist and fix all failures.
    This page has the highest total hex count (~124 across PartnerAnalytics, DistributionTab,
    AdvisorsTab, ClientsTab).
  </objective>

  <references>
    <ref type="prd">docs/architecture/PORTAL_DESIGN_NORMALIZATION_AND_COMPILER_TOOLS.md</ref>
    <ref type="design-qa">org/ref/design/PORTAL_DESIGN_QA.md</ref>
    <ref type="chart-colors">portal/src/lib/chartColors.ts</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <estimated_hex_count>124 (PartnerAnalytics 46 + DistributionTab 42 + AdvisorsTab 20 + ClientsTab 16)</estimated_hex_count>
  </scope>

  <requirements>
    <requirement id="1">Read `org/ref/design/PORTAL_DESIGN_QA.md` (mandatory)</requirement>
    <requirement id="2">Read `portal/src/lib/chartColors.ts` to understand available exports</requirement>
    <requirement id="3">Grep AdvisorIntelligence/ for hardcoded hex. For each: find matching chartColors.ts export, replace with import. If no match, add to chartColors.ts with semantic name.</requirement>
    <requirement id="4">Run Pre-Commit QA Checklist. Fix all failures.</requirement>
    <requirement id="5">Run `bun run build` to verify</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Zero hardcoded hex values in AdvisorIntelligence/ page files</criterion>
    <criterion id="2">Design QA checklist passes</criterion>
    <criterion id="3">bun run build succeeds</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify files outside AdvisorIntelligence/ (except chartColors.ts if adding new colors)</constraint>
    <constraint>Preserve exact visual appearance</constraint>
    <constraint>Commit to portal DEV branch</constraint>
  </constraints>

  <dependencies>
    <dependency>None -- parallel with all except .001/.002</dependency>
  </dependencies>

  <commit_pattern>refactor(AdvisorIntelligence): migrate hex colors to chartColors + design QA pass</commit_pattern>
</task_order>
