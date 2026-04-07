# Task Order: Positioning Color Migration + Design QA

<task_order>
  <metadata>
    <id>ADHC_DESIGN-002</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.1_RD_Positioning</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <project>ADHC_DESIGN</project>
  </metadata>

  <objective>
    Migrate ALL hardcoded hex colors in the Positioning page directory to imports
    from `@/lib/chartColors.ts`. Then run the Design QA checklist and fix all failures.
  </objective>

  <references>
    <ref type="prd">docs/architecture/PORTAL_DESIGN_NORMALIZATION_AND_COMPILER_TOOLS.md</ref>
    <ref type="design-qa">org/ref/design/PORTAL_DESIGN_QA.md</ref>
    <ref type="chart-colors">portal/src/lib/chartColors.ts</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/Positioning/</page>
    </pages>
    <estimated_hex_count>53 (highest single-page count)</estimated_hex_count>
  </scope>

  <requirements>
    <requirement id="1">Read `org/ref/design/PORTAL_DESIGN_QA.md` (mandatory)</requirement>
    <requirement id="2">Read `portal/src/lib/chartColors.ts` to understand available exports</requirement>
    <requirement id="3">Grep Positioning/ for hardcoded hex (#[0-9a-fA-F]{6}). For each: find matching chartColors.ts export, replace local definition with import. If no match, add to chartColors.ts.</requirement>
    <requirement id="4">NOTE: holdings-shared.tsx (Attribution) was already migrated by .001. If Positioning imports from it, verify the import still works after .001's changes.</requirement>
    <requirement id="5">Run Pre-Commit QA Checklist from PORTAL_DESIGN_QA.md. Fix all failures.</requirement>
    <requirement id="6">Run `bun run build` to verify</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Zero hardcoded hex values in Positioning/ page files</criterion>
    <criterion id="2">Design QA checklist passes</criterion>
    <criterion id="3">bun run build succeeds</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify files outside Positioning/ (except chartColors.ts if adding new colors)</constraint>
    <constraint>Preserve exact visual appearance</constraint>
    <constraint>Commit to portal DEV branch</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.2.2_RD_Attribution" task="ADHC_DESIGN-001" status="complete">holdings-shared.tsx must be migrated first</dependency>
  </dependencies>

  <commit_pattern>refactor(Positioning): migrate hex colors to chartColors + design QA pass</commit_pattern>
</task_order>
