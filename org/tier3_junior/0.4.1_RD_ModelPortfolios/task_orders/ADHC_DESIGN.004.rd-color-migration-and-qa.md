# Task Order: ModelPortfolios Color Migration + Design QA

<task_order>
  <metadata>
    <id>ADHC_DESIGN-004</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.1_RD_ModelPortfolios</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <project>ADHC_DESIGN</project>
  </metadata>

  <objective>
    Migrate all hardcoded hex colors in ModelPortfolios to imports from
    `@/lib/chartColors.ts`. Run Design QA checklist and fix all failures.
  </objective>

  <references>
    <ref type="prd">docs/architecture/PORTAL_DESIGN_NORMALIZATION_AND_COMPILER_TOOLS.md</ref>
    <ref type="design-qa">org/ref/design/PORTAL_DESIGN_QA.md</ref>
    <ref type="chart-colors">portal/src/lib/chartColors.ts</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/ModelPortfolios/</page>
    </pages>
    <estimated_hex_count>14</estimated_hex_count>
  </scope>

  <requirements>
    <requirement id="1">Read `org/ref/design/PORTAL_DESIGN_QA.md` (mandatory)</requirement>
    <requirement id="2">Read `portal/src/lib/chartColors.ts`</requirement>
    <requirement id="3">Grep for hardcoded hex, replace with chartColors.ts imports</requirement>
    <requirement id="4">Run Pre-Commit QA Checklist. Fix all failures.</requirement>
    <requirement id="5">Run `bun run build` to verify</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Zero hardcoded hex in ModelPortfolios/ page files</criterion>
    <criterion id="2">Design QA checklist passes</criterion>
    <criterion id="3">bun run build succeeds</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Preserve exact visual appearance. Commit to portal DEV branch.</constraint>
  </constraints>

  <dependencies>
    <dependency>None -- parallel</dependency>
  </dependencies>

  <commit_pattern>refactor(ModelPortfolios): migrate hex colors to chartColors + design QA pass</commit_pattern>
</task_order>
