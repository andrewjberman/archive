# Task Order: Attribution Color Migration + Design QA (CRITICAL PATH)

<task_order>
  <metadata>
    <id>ADHC_DESIGN-001</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.2_RD_Attribution</issued_to>
    <date>2026-04-07</date>
    <status>complete</status><!-- CANCELLED 2026-04-21 — surface not under active investment; see org/tier1_exec/1.0.0_SA_CTO/logs/2026-04-21/session36_five_item_decisions.md §4. ADHC_DESIGN closed at 28/32 effective; Attribution + Valuation sub-pages deferred per Andrew directive (no product driver). 0.2.2_RD_Attribution agent not spawned; no code shipped. -->
    <project>ADHC_DESIGN</project>
  </metadata>

  <objective>
    Migrate ALL hardcoded hex colors in the Attribution page directory to imports
    from `@/lib/chartColors.ts`. This includes the CRITICAL shared file
    `Attribution/constants/holdings-shared.tsx` which is imported by Positioning
    and other consumers. This file MUST be migrated first.

    Then run the full Design QA checklist from `org/ref/design/PORTAL_DESIGN_QA.md`
    against your page and fix all failures.
  </objective>

  <references>
    <ref type="prd">docs/architecture/PORTAL_DESIGN_NORMALIZATION_AND_COMPILER_TOOLS.md</ref>
    <ref type="design-qa">org/ref/design/PORTAL_DESIGN_QA.md</ref>
    <ref type="chart-colors">portal/src/lib/chartColors.ts</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/Attribution/</page>
    </pages>
    <critical_file>portal/src/pages/Attribution/constants/holdings-shared.tsx</critical_file>
    <estimated_hex_count>46+ (holdings-shared alone)</estimated_hex_count>
  </scope>

  <requirements>
    <requirement id="1">Read `org/ref/design/PORTAL_DESIGN_QA.md` (mandatory before any changes)</requirement>
    <requirement id="2">Read `portal/src/lib/chartColors.ts` to understand all available exports</requirement>
    <requirement id="3">FIRST: Migrate `Attribution/constants/holdings-shared.tsx` -- replace every local hex constant with an import from chartColors.ts. Find matching exports by hex value. If no match, add the color to chartColors.ts with a semantic name.</requirement>
    <requirement id="4">Then migrate all other files in Attribution/ that contain hardcoded hex (#[0-9a-fA-F]{6})</requirement>
    <requirement id="5">Run the Pre-Commit QA Checklist from PORTAL_DESIGN_QA.md against Attribution/. Fix all failures (labels, color tokens, panel primitives, interactions).</requirement>
    <requirement id="6">Specific QA items to check: Valuation-style accentColor overrides, text-sm vs text-xs, non-standard opacities (/40, /60, /80 where /50 is canonical)</requirement>
    <requirement id="7">Run `bun run build` to verify no compilation errors</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Zero hardcoded hex values in Attribution/ page files (all from chartColors.ts imports)</criterion>
    <criterion id="2">holdings-shared.tsx exports are now imports from @/lib/chartColors</criterion>
    <criterion id="3">Design QA checklist passes for all Attribution page files</criterion>
    <criterion id="4">bun run build succeeds</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify files outside Attribution/ directory (except chartColors.ts if adding new colors)</constraint>
    <constraint>Preserve exact visual appearance -- same hex values, just centralized imports</constraint>
    <constraint>Commit to portal DEV branch</constraint>
  </constraints>

  <dependencies>
    <dependency>None -- this is the critical path task. All other RD color migrations wait for this.</dependency>
  </dependencies>

  <commit_pattern>refactor(Attribution): migrate hex colors to chartColors + design QA pass</commit_pattern>
</task_order>
