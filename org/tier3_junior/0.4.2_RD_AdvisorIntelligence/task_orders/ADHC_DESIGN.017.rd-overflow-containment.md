# Task Order: AdvisorIntelligence Overflow Containment

<task_order>
  <metadata>
    <id>ADHC_DESIGN-017</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <!-- Completed 2026-04-07. Portal DEV commit pending. overflow-hidden on 8 chart PanelContents, overflow-x-hidden on ClientsTable, min-w-0 on flex containers. -->
    <project>ADHC_DESIGN</project>
    <phase>2</phase>
  </metadata>

  <objective>
    Audit and fix ALL overflow containment issues in the AdvisorIntelligence page.
    No child content should visually extend past its parent panel/card container.
    This is the largest page — check all tabs (PartnerAnalytics, Distribution, Advisors, Clients, Books).
  </objective>

  <references>
    <ref type="prd">docs/architecture/PORTAL_DESIGN_NORMALIZATION_AND_COMPILER_TOOLS.md</ref>
    <ref type="design-qa">org/ref/design/PORTAL_DESIGN_QA.md</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
  </scope>

  <requirements>
    <requirement id="1">Audit every Panel, Card, container div, and layout wrapper for overflow behavior</requirement>
    <requirement id="2">Charts: overflow-hidden. Tables: overflow-x-auto. Text: truncate/line-clamp/break-words. Tooltips: portal or scoped overflow-visible.</requirement>
    <requirement id="3">No absolutely-positioned child extends past relative parent</requirement>
    <requirement id="4">Test at viewport widths: 1920px, 1440px, 1280px, 1024px</requirement>
    <requirement id="5">Recharts/ApexCharts containers have explicit constraints or ResponsiveContainer</requirement>
    <requirement id="6">Run `bun run build` to verify</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Zero visual overflow past parent panels across all tabs</criterion>
    <criterion id="2">All dynamic-content containers have explicit overflow handling</criterion>
    <criterion id="3">bun run build succeeds</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Preserve visual appearance. Commit to portal DEV branch.</constraint>
  </constraints>

  <commit_pattern>fix(AdvisorIntelligence): overflow containment on all panel containers</commit_pattern>
</task_order>
