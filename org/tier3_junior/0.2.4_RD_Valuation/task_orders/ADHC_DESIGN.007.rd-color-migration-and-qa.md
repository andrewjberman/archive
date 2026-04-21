# Task Order: Valuation Color Migration + Design QA

<task_order>
  <metadata>
    <id>ADHC_DESIGN-007</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.4_RD_Valuation</issued_to>
    <date>2026-04-07</date>
    <status>complete</status><!-- CANCELLED 2026-04-21 — surface not under active investment; see org/tier1_exec/1.0.0_SA_CTO/logs/2026-04-21/session36_five_item_decisions.md §4. ADHC_DESIGN closed at 28/32 effective; Attribution + Valuation sub-pages deferred per Andrew directive (no product driver). 0.2.4_RD_Valuation agent not spawned; no code shipped. -->
    <project>ADHC_DESIGN</project>
  </metadata>

  <objective>
    Migrate all hardcoded hex colors in Valuation to imports from
    `@/lib/chartColors.ts`. Run Design QA checklist and fix all failures.
    SPECIFIC: Replace `PageThemeProvider accentColor="#f59e0b"` with a CSS variable.
  </objective>

  <references>
    <ref type="prd">docs/architecture/PORTAL_DESIGN_NORMALIZATION_AND_COMPILER_TOOLS.md</ref>
    <ref type="design-qa">org/ref/design/PORTAL_DESIGN_QA.md</ref>
    <ref type="chart-colors">portal/src/lib/chartColors.ts</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/Valuation/</page>
    </pages>
    <estimated_hex_count>12</estimated_hex_count>
  </scope>

  <requirements>
    <requirement id="1">Read `org/ref/design/PORTAL_DESIGN_QA.md` (mandatory)</requirement>
    <requirement id="2">Read `portal/src/lib/chartColors.ts`</requirement>
    <requirement id="3">Grep for hardcoded hex, replace with chartColors.ts imports</requirement>
    <requirement id="4">SPECIFIC FIX: Replace `PageThemeProvider accentColor="#f59e0b"` with a CSS variable (see PRD Phase 2 known issues)</requirement>
    <requirement id="5">Run Pre-Commit QA Checklist. Fix all failures.</requirement>
    <requirement id="6">Run `bun run build` to verify</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Zero hardcoded hex in Valuation/ page files</criterion>
    <criterion id="2">accentColor uses CSS variable, not hardcoded hex</criterion>
    <criterion id="3">Design QA checklist passes</criterion>
    <criterion id="4">bun run build succeeds</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Preserve exact visual appearance. Commit to portal DEV branch.</constraint>
  </constraints>

  <dependencies>
    <dependency>None -- parallel</dependency>
  </dependencies>

  <commit_pattern>refactor(Valuation): migrate hex colors to chartColors + design QA pass</commit_pattern>
</task_order>
