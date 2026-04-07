# Task Order: Macroeconomics Overflow Containment

<task_order>
  <metadata>
    <id>ADHC_DESIGN-013</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.5_RD_Macroeconomics</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <project>ADHC_DESIGN</project>
    <phase>2</phase>
  </metadata>

  <objective>
    Audit and fix ALL overflow containment issues in the Macroeconomics page.
    No child content (charts, tables, text, tooltips, legends) should visually
    extend past the bounds of its parent panel/card container. This is Phase 2
    of the portal design normalization.
  </objective>

  <references>
    <ref type="prd">docs/architecture/PORTAL_DESIGN_NORMALIZATION_AND_COMPILER_TOOLS.md</ref>
    <ref type="design-qa">org/ref/design/PORTAL_DESIGN_QA.md</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/Macroeconomics/</page>
    </pages>
  </scope>

  <requirements>
    <requirement id="1">Audit every Panel, Card, container div, and layout wrapper in your page for overflow behavior</requirement>
    <requirement id="2">For each container that holds dynamic content (charts, tables, lists, long text): ensure it has `overflow-hidden`, `overflow-auto`, or `overflow-x-auto` as appropriate:
      - Charts/visualizations: `overflow-hidden` (clip, never scroll)
      - Tables with many columns: `overflow-x-auto` (horizontal scroll)
      - Text content: ensure `truncate`, `line-clamp`, or `break-words` prevents bleed
      - Tooltips/popovers: verify they use portal rendering or `overflow-visible` only on the immediate tooltip container</requirement>
    <requirement id="3">Check that no absolutely-positioned child extends past its relative parent without intentional overflow-visible</requirement>
    <requirement id="4">Test at viewport widths: 1920px, 1440px, 1280px, 1024px. Content must not overflow at any width.</requirement>
    <requirement id="5">Ensure Recharts/ApexCharts containers have explicit width/height constraints or use ResponsiveContainer correctly</requirement>
    <requirement id="6">Run `bun run build` to verify no compilation errors</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Zero visual overflow — no chart, table, text, or legend bleeds past its parent panel</criterion>
    <criterion id="2">All dynamic-content containers have explicit overflow handling</criterion>
    <criterion id="3">bun run build succeeds</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Preserve exact visual appearance — only add overflow containment, do not redesign layouts</constraint>
    <constraint>Commit to portal DEV branch</constraint>
  </constraints>

  <commit_pattern>fix(Macroeconomics): overflow containment on all panel containers</commit_pattern>
</task_order>
